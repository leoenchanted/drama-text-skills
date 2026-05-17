#!/usr/bin/env python3
"""Extract sparse video context frames for drama-text-skills.

The script is intentionally dependency-free. It uses ffmpeg/ffprobe from PATH
when available, otherwise it can cache a local copy on macOS and Windows.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


VERSION = "1.0.0"
VIDEO_EXTENSIONS = (".mp4", ".mov", ".mkv", ".m4v", ".webm", ".avi")
TIME_CODE = r"\d{1,2}:\d{2}:\d{2}(?:[,.]\d{1,3})?"
TIME_RANGE_RE = re.compile(
    rf"(?P<start>{TIME_CODE})\s*-->\s*(?P<end>{TIME_CODE})"
)
LOW_COVERAGE_THRESHOLD = 0.35
LOW_CHARS_PER_MINUTE = 450
DEFAULT_SHEET_SIZE = 12


class ToolSetupError(RuntimeError):
    """Raised when ffmpeg/ffprobe cannot be found or prepared."""


@dataclass
class SubtitleEntry:
    start: float
    end: float
    text: str


@dataclass
class Gap:
    start: float
    end: float
    duration: float


@dataclass
class SamplePoint:
    index: int
    time_seconds: float
    timecode: str
    reason: str
    source_gap: Optional[dict[str, float]] = None
    frame_path: Optional[str] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build sparse visual context from a drama video and timed subtitle txt."
    )
    parser.add_argument("--subtitle", required=True, help="Timed subtitle .txt file")
    parser.add_argument("--video", help="Video path. Defaults to same stem as subtitle.")
    parser.add_argument(
        "--out",
        help="Output directory. Defaults to .drama_video_context/<subtitle-stem> next to subtitle.",
    )
    parser.add_argument(
        "--max-points",
        type=int,
        default=18,
        help="Maximum visual sample points to extract. Defaults to 18.",
    )
    parser.add_argument(
        "--gap-threshold",
        type=float,
        default=3.0,
        help="Seconds without subtitles before a gap is considered important. Defaults to 3.0.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Extract frames even when the subtitle is not classified as sparse.",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Do not auto-download ffmpeg/ffprobe when they are missing.",
    )
    return parser.parse_args()


def parse_timecode(value: str) -> float:
    value = value.strip().replace(",", ".")
    main, _, fraction = value.partition(".")
    hours_s, minutes_s, seconds_s = main.split(":")
    milliseconds = 0
    if fraction:
        milliseconds = int((fraction + "000")[:3])
    return (
        int(hours_s) * 3600
        + int(minutes_s) * 60
        + int(seconds_s)
        + milliseconds / 1000
    )


def format_timecode(seconds: float) -> str:
    total = max(0, int(round(seconds)))
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_filename_time(seconds: float) -> str:
    return format_timecode(seconds).replace(":", "-")


def format_ffmpeg_time(seconds: float) -> str:
    total_ms = max(0, int(round(seconds * 1000)))
    total_seconds, milliseconds = divmod(total_ms, 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"


def read_subtitles(path: Path) -> list[SubtitleEntry]:
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    entries: list[SubtitleEntry] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = TIME_RANGE_RE.search(line)
        if not match:
            i += 1
            continue

        start = parse_timecode(match.group("start"))
        end = parse_timecode(match.group("end"))
        cue_lines: list[str] = []
        inline_text = line[match.end() :].strip(" -\t")
        if inline_text:
            cue_lines.append(inline_text)
        i += 1
        while i < len(lines):
            stripped = lines[i].strip()
            if not stripped:
                i += 1
                break
            if TIME_RANGE_RE.search(stripped):
                break
            if not stripped.isdigit():
                cue_lines.append(stripped)
            i += 1
        text = " ".join(cue_lines).strip()
        if end > start:
            entries.append(SubtitleEntry(start=start, end=end, text=text))
    return entries


def count_effective_chars(entries: Iterable[SubtitleEntry]) -> int:
    text = "".join(entry.text for entry in entries)
    return sum(1 for char in text if not char.isspace())


def cache_root() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Caches" / "drama-text-skills" / "ffmpeg"
    if system == "Windows":
        base = os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / "drama-text-skills" / "ffmpeg"
    return Path.home() / ".cache" / "drama-text-skills" / "ffmpeg"


def executable_name(name: str) -> str:
    return f"{name}.exe" if platform.system() == "Windows" else name


def find_cached_tool(name: str) -> Optional[str]:
    target = executable_name(name)
    root = cache_root()
    for candidate in (root / "bin" / target, root / target):
        if candidate.exists():
            return str(candidate)
    return None


def find_tool(name: str) -> Optional[str]:
    return shutil.which(name) or find_cached_tool(name)


def download_url(url: str, dest: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "drama-text-skills/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        with dest.open("wb") as handle:
            shutil.copyfileobj(response, handle)


def extract_zip(zip_path: Path, dest: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(dest)


def find_extracted_binary(root: Path, name: str) -> Optional[Path]:
    target = executable_name(name)
    for path in root.rglob(target):
        if path.is_file():
            return path
    if platform.system() != "Windows":
        for path in root.rglob(name):
            if path.is_file():
                return path
    return None


def make_executable(path: Path) -> None:
    if platform.system() != "Windows":
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install_darwin_tools(bin_dir: Path) -> None:
    sources = {
        "ffmpeg": "https://evermeet.cx/ffmpeg/getrelease/zip",
        "ffprobe": "https://evermeet.cx/ffmpeg/getrelease/ffprobe/zip",
    }
    bin_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="drama-ffmpeg-") as temp_name:
        temp_dir = Path(temp_name)
        for tool, url in sources.items():
            target = bin_dir / executable_name(tool)
            if target.exists():
                continue
            zip_path = temp_dir / f"{tool}.zip"
            extract_dir = temp_dir / tool
            extract_dir.mkdir()
            download_url(url, zip_path)
            extract_zip(zip_path, extract_dir)
            binary = find_extracted_binary(extract_dir, tool)
            if not binary:
                raise ToolSetupError(f"Downloaded archive did not contain {tool}.")
            shutil.copy2(binary, target)
            make_executable(target)


def install_windows_tools(bin_dir: Path) -> None:
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    bin_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="drama-ffmpeg-") as temp_name:
        temp_dir = Path(temp_name)
        zip_path = temp_dir / "ffmpeg-release-essentials.zip"
        extract_dir = temp_dir / "extract"
        extract_dir.mkdir()
        download_url(url, zip_path)
        extract_zip(zip_path, extract_dir)
        for tool in ("ffmpeg", "ffprobe"):
            target = bin_dir / executable_name(tool)
            if target.exists():
                continue
            binary = find_extracted_binary(extract_dir, tool)
            if not binary:
                raise ToolSetupError(f"Downloaded archive did not contain {tool}.")
            shutil.copy2(binary, target)


def install_tools() -> None:
    system = platform.system()
    bin_dir = cache_root() / "bin"
    if system == "Darwin":
        install_darwin_tools(bin_dir)
        return
    if system == "Windows":
        install_windows_tools(bin_dir)
        return
    raise ToolSetupError(
        "Automatic ffmpeg download is only supported on macOS and Windows. "
        "Install ffmpeg and ffprobe with your package manager, then run again."
    )


def ensure_tools(allow_download: bool) -> tuple[str, str, bool]:
    ffmpeg = find_tool("ffmpeg")
    ffprobe = find_tool("ffprobe")
    if ffmpeg and ffprobe:
        return ffmpeg, ffprobe, False
    if not allow_download:
        raise ToolSetupError(
            "ffmpeg/ffprobe not found. Install them or rerun without --no-download."
        )
    install_tools()
    ffmpeg = find_tool("ffmpeg")
    ffprobe = find_tool("ffprobe")
    if not ffmpeg or not ffprobe:
        raise ToolSetupError("ffmpeg/ffprobe could not be prepared.")
    return ffmpeg, ffprobe, True


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def probe_duration(ffprobe: str, video: Path) -> float:
    result = run_command(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed to read video duration.")
    try:
        return float(result.stdout.strip())
    except ValueError as exc:
        raise RuntimeError(f"Invalid ffprobe duration output: {result.stdout!r}") from exc


def merge_intervals(entries: list[SubtitleEntry], duration: float) -> list[tuple[float, float]]:
    intervals = sorted(
        (max(0.0, entry.start), min(duration, entry.end))
        for entry in entries
        if entry.end > 0 and entry.start < duration
    )
    merged: list[tuple[float, float]] = []
    for start, end in intervals:
        if end <= start:
            continue
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    return merged


def compute_gaps(
    intervals: list[tuple[float, float]], duration: float, threshold: float
) -> list[Gap]:
    gaps: list[Gap] = []
    cursor = 0.0
    for start, end in intervals:
        if start - cursor >= threshold:
            gaps.append(Gap(start=cursor, end=start, duration=start - cursor))
        cursor = max(cursor, end)
    if duration - cursor >= threshold:
        gaps.append(Gap(start=cursor, end=duration, duration=duration - cursor))
    return gaps


def subtitle_stats(
    entries: list[SubtitleEntry], duration: float, intervals: list[tuple[float, float]], gaps: list[Gap]
) -> dict[str, object]:
    subtitle_seconds = sum(end - start for start, end in intervals)
    coverage = subtitle_seconds / duration if duration > 0 else 0.0
    char_count = count_effective_chars(entries)
    chars_per_minute = char_count / (duration / 60) if duration > 0 else 0.0
    reasons: list[str] = []
    if coverage < LOW_COVERAGE_THRESHOLD:
        reasons.append(f"subtitle_coverage_lt_{int(LOW_COVERAGE_THRESHOLD * 100)}pct")
    if chars_per_minute < LOW_CHARS_PER_MINUTE:
        reasons.append(f"subtitle_chars_per_minute_lt_{LOW_CHARS_PER_MINUTE}")
    if len(gaps) >= 3:
        reasons.append("long_gaps_ge_3")
    return {
        "entry_count": len(entries),
        "char_count": char_count,
        "subtitle_seconds": round(subtitle_seconds, 3),
        "subtitle_coverage": round(coverage, 4),
        "chars_per_minute": round(chars_per_minute, 2),
        "long_gap_count": len(gaps),
        "low_subtitle": bool(reasons),
        "low_subtitle_reasons": reasons,
    }


def add_sample(
    samples: list[SamplePoint],
    seconds: float,
    duration: float,
    reason: str,
    source_gap: Optional[Gap],
    min_distance: float = 1.0,
) -> None:
    if duration <= 0:
        return
    seconds = min(max(0.25, seconds), max(0.25, duration - 0.25))
    if any(abs(sample.time_seconds - seconds) < min_distance for sample in samples):
        return
    gap_payload = None
    if source_gap:
        gap_payload = {
            "start": round(source_gap.start, 3),
            "end": round(source_gap.end, 3),
            "duration": round(source_gap.duration, 3),
        }
    samples.append(
        SamplePoint(
            index=0,
            time_seconds=round(seconds, 3),
            timecode=format_timecode(seconds),
            reason=reason,
            source_gap=gap_payload,
        )
    )


def select_sample_points(
    gaps: list[Gap], duration: float, max_points: int, gap_threshold: float, low_subtitle: bool
) -> list[SamplePoint]:
    samples: list[SamplePoint] = []
    extra_long_threshold = max(gap_threshold * 3, 8.0)
    for gap in sorted(gaps, key=lambda item: item.duration, reverse=True):
        if len(samples) >= max_points:
            break
        if gap.duration >= extra_long_threshold and len(samples) + 1 < max_points:
            add_sample(samples, gap.start + gap.duration * 0.33, duration, "extra_long_gap", gap)
            add_sample(samples, gap.start + gap.duration * 0.66, duration, "extra_long_gap", gap)
        else:
            add_sample(samples, gap.start + gap.duration / 2, duration, "long_gap", gap)

    if low_subtitle and len(samples) < min(max_points, 8):
        target = min(max_points, 8)
        candidate_count = target * 2
        for i in range(candidate_count):
            if len(samples) >= target:
                break
            seconds = duration * (i + 1) / (candidate_count + 1)
            add_sample(samples, seconds, duration, "global_sample", None, min_distance=2.0)

    samples = sorted(samples, key=lambda item: item.time_seconds)[:max_points]
    for index, sample in enumerate(samples, start=1):
        sample.index = index
    return samples


def escape_drawtext(text: str) -> str:
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def extract_frame(
    ffmpeg: str, video: Path, sample: SamplePoint, output: Path, with_label: bool
) -> None:
    vf = "scale=320:-1"
    if with_label:
        label = escape_drawtext(sample.timecode)
        vf += (
            f",drawtext=text='{label}':x=8:y=h-th-8:fontsize=22:"
            "fontcolor=white:box=1:boxcolor=black@0.65"
        )
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-ss",
        format_ffmpeg_time(sample.time_seconds),
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        "-vf",
        vf,
        str(output),
    ]
    result = run_command(command)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"ffmpeg failed for {sample.timecode}")


def extract_frames(
    ffmpeg: str, video: Path, samples: list[SamplePoint], frames_dir: Path
) -> list[str]:
    warnings: list[str] = []
    frames_dir.mkdir(parents=True, exist_ok=True)
    for sample in samples:
        output = frames_dir / f"frame_{sample.index:03d}_{format_filename_time(sample.time_seconds)}.jpg"
        try:
            extract_frame(ffmpeg, video, sample, output, with_label=True)
        except RuntimeError as exc:
            warnings.append(f"drawtext_fallback_{sample.index}: {exc}")
            extract_frame(ffmpeg, video, sample, output, with_label=False)
        sample.frame_path = str(output.resolve())
    return warnings


def create_contact_sheets(
    ffmpeg: str,
    samples: list[SamplePoint],
    sheets_dir: Path,
    sheet_size: int = DEFAULT_SHEET_SIZE,
) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    sheet_paths: list[str] = []
    if not samples:
        return sheet_paths, warnings
    sheets_dir.mkdir(parents=True, exist_ok=True)
    chunks = [samples[i : i + sheet_size] for i in range(0, len(samples), sheet_size)]
    for sheet_index, chunk in enumerate(chunks, start=1):
        cols = min(4, max(1, math.ceil(math.sqrt(len(chunk)))))
        rows = math.ceil(len(chunk) / cols)
        with tempfile.TemporaryDirectory(prefix=f"sheet-{sheet_index:03d}-", dir=sheets_dir) as temp_name:
            temp_dir = Path(temp_name)
            for item_index, sample in enumerate(chunk, start=1):
                if not sample.frame_path:
                    continue
                shutil.copy2(sample.frame_path, temp_dir / f"tile_{item_index:03d}.jpg")
            output = sheets_dir / f"sheet_{sheet_index:03d}.jpg"
            command = [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-framerate",
                "1",
                "-i",
                str(temp_dir / "tile_%03d.jpg"),
                "-vf",
                f"tile={cols}x{rows}:padding=6:margin=6:color=black",
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(output),
            ]
            result = run_command(command)
            if result.returncode != 0:
                warnings.append(
                    f"sheet_{sheet_index:03d}_failed: "
                    f"{result.stderr.strip() or 'ffmpeg tile failed'}"
                )
                continue
            sheet_paths.append(str(output.resolve()))
    return sheet_paths, warnings


def auto_match_video(subtitle: Path) -> Optional[Path]:
    for extension in VIDEO_EXTENSIONS:
        candidate = subtitle.with_suffix(extension)
        if candidate.exists():
            return candidate
    lower_stem = subtitle.stem.lower()
    for candidate in subtitle.parent.iterdir():
        if candidate.suffix.lower() in VIDEO_EXTENSIONS and candidate.stem.lower() == lower_stem:
            return candidate
    return None


def default_output_dir(subtitle: Path) -> Path:
    return subtitle.parent / ".drama_video_context" / subtitle.stem


def build_manifest(
    subtitle: Path,
    video: Path,
    output_dir: Path,
    video_duration: float,
    stats: dict[str, object],
    gaps: list[Gap],
    samples: list[SamplePoint],
    sheets: list[str],
    frame_triggered: bool,
    args: argparse.Namespace,
    tools_downloaded: bool,
    warnings: list[str],
) -> dict[str, object]:
    return {
        "version": VERSION,
        "subtitle": str(subtitle.resolve()),
        "video": str(video.resolve()),
        "output_dir": str(output_dir.resolve()),
        "video_duration": round(video_duration, 3),
        "gap_threshold": args.gap_threshold,
        "max_points": args.max_points,
        "force": args.force,
        "tools_downloaded": tools_downloaded,
        "stats": stats,
        "frame_triggered": frame_triggered,
        "gaps": [
            {"start": round(gap.start, 3), "end": round(gap.end, 3), "duration": round(gap.duration, 3)}
            for gap in gaps
        ],
        "samples": [
            {
                "index": sample.index,
                "time_seconds": sample.time_seconds,
                "timecode": sample.timecode,
                "reason": sample.reason,
                "source_gap": sample.source_gap,
                "frame_path": sample.frame_path,
            }
            for sample in samples
        ],
        "sheets": sheets,
        "warnings": warnings,
    }


def main() -> int:
    args = parse_args()
    subtitle = Path(args.subtitle).expanduser()
    if not subtitle.exists():
        print(f"ERROR: Subtitle file not found: {subtitle}", file=sys.stderr)
        return 2
    video = Path(args.video).expanduser() if args.video else auto_match_video(subtitle)
    if not video:
        print(
            "ERROR: No matching video found. Provide --video or place a same-name video next to the subtitle.",
            file=sys.stderr,
        )
        return 2
    if not video.exists():
        print(f"ERROR: Video file not found: {video}", file=sys.stderr)
        return 2

    entries = read_subtitles(subtitle)
    if not entries:
        print(
            "ERROR: No SRT-style timeline found in subtitle txt. "
            "Use lines like 00:00:01,000 --> 00:00:03,000 or provide manual visual notes.",
            file=sys.stderr,
        )
        return 2

    try:
        ffmpeg, ffprobe, tools_downloaded = ensure_tools(allow_download=not args.no_download)
        duration = probe_duration(ffprobe, video)
    except (RuntimeError, ToolSetupError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    output_dir = Path(args.out).expanduser() if args.out else default_output_dir(subtitle)
    output_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = output_dir / "frames"
    sheets_dir = output_dir / "sheets"

    intervals = merge_intervals(entries, duration)
    gaps = compute_gaps(intervals, duration, args.gap_threshold)
    stats = subtitle_stats(entries, duration, intervals, gaps)
    frame_triggered = bool(stats["low_subtitle"]) or args.force
    warnings: list[str] = []
    samples: list[SamplePoint] = []
    sheets: list[str] = []

    if frame_triggered:
        samples = select_sample_points(
            gaps=gaps,
            duration=duration,
            max_points=max(1, args.max_points),
            gap_threshold=args.gap_threshold,
            low_subtitle=bool(stats["low_subtitle"]),
        )
        warnings.extend(extract_frames(ffmpeg, video, samples, frames_dir))
        sheets, sheet_warnings = create_contact_sheets(ffmpeg, samples, sheets_dir)
        warnings.extend(sheet_warnings)

    manifest = build_manifest(
        subtitle=subtitle,
        video=video,
        output_dir=output_dir,
        video_duration=duration,
        stats=stats,
        gaps=gaps,
        samples=samples,
        sheets=sheets,
        frame_triggered=frame_triggered,
        args=args,
        tools_downloaded=tools_downloaded,
        warnings=warnings,
    )
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path.resolve()), "frame_triggered": frame_triggered}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
