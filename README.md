# drama-text-skills

短剧解说文案生成器 — Claude Code Skill。输入短剧字幕文件，结合你的爆款文案模板，自动生成 800-1000 字短视频解说脚本，并支持口语化英文翻译。字幕较少、画面承载剧情时，可用视频抽帧辅助理解。

## 安装

将整个 `drama-text-skills` 文件夹放到你的项目 `.claude/skills/` 目录下：

```
your-project/
└── .claude/
    └── skills/
        └── drama-text-skills/
            ├── SKILL.md
            ├── scripts/
            ├── templates/
            └── README.md
```

Claude Code 会自动识别并加载该 Skill。

## 准备工作

### 1. 放入爆款文案模板

把你收集的爆款解说文案（约 8-10 篇）放到 `templates/` 文件夹里，支持 `.txt` 或 `.md` 格式。

```
templates/
├── 爆款1.txt
├── 爆款2.txt
├── ...
└── 爆款10.txt
```

Skill 触发时会自动读取全部模板，分析风格并模仿。

### 2. 准备字幕文件

准备好你要解说的短剧字幕 `.txt` 文件，放在任意位置即可。推荐使用带时间轴的 SRT 风格 TXT：

```
1
00:00:01,000 --> 00:00:03,000
这里是字幕内容
```

### 3. （可选）准备视频文件

如果一集短剧对白很少、很多剧情靠画面表现，可以把视频和字幕放在同一目录并保持同名：

```
episode01.mp4
episode01.txt
```

当字幕信息稀疏时，Skill 会使用 `scripts/video_context.py` 调用 `ffmpeg/ffprobe` 抽取无字幕区间的关键画面，生成给 AI 内部分析的带时间戳拼图。

### 4. （可选）准备剧情简介

如果字幕来自中间集数，建议提供剧情简介帮助理解前情和人物关系。你可以用两种方式提供：

- **对话粘贴（推荐）**：在对话中以 `剧情简介：` 开头，后面直接粘贴简介正文（可多行）
- **文件**：提供一个 `.txt` 简介文件，文件名包含“剧情/简介/summary/plot”等关键词

## 使用方式

在 Claude Code 对话中，把字幕文件拖进来或指定路径，然后说：

> 「帮我给这个短剧写解说文案」

Skill 会自动触发，工作流程：

1. **内部分析**：读取剧情简介（可选）→ 读取字幕 → 生成剧情概述，读取 templates/ 分析爆款文案风格
2. **视频辅助（可选）**：如果字幕带时间轴、同名视频存在且字幕稀疏，抽帧分析画面事实
3. **输出中文脚本**：生成 800-1000 字解说文案（不使用人物名，用他/她/男人/女人代替）
4. **等待确认**：你可以要求调整语气、字数、段落，直到满意
5. **英文翻译**：你说「确认」或「翻译吧」，生成口语化英文版本

## 视频抽帧工具

也可以手动运行：

```
python3 scripts/video_context.py --subtitle path/to/episode.txt --video path/to/episode.mp4
```

可选参数：

```
python3 scripts/video_context.py --subtitle path/to/episode.txt --video path/to/episode.mp4 --max-points 18 --gap-threshold 3.0 --out path/to/output
```

输出包括：

- `manifest.json`：记录低字幕判断、抽帧时间点和图片路径
- `sheets/sheet_001.jpg`：优先给 AI 分析的带时间戳拼图
- `frames/frame_001_00-01-12.jpg`：必要时查看的单帧

工具会优先使用系统已有 `ffmpeg/ffprobe`。如果没有安装，macOS 和 Windows 会首次自动下载到用户缓存目录；Linux 会提示手动安装。

## 示例对话

```
你：帮我写短剧解说文案 [附上字幕文件]

Claude：
<<<DRAMA_SCRIPT>>>
[生成的800-1000字文案...]
<<<END_SCRIPT>>>

你：结尾有点平淡，改得更有悬念感

Claude：
<<<DRAMA_SCRIPT>>>
[修改后的文案...]
<<<END_SCRIPT>>>

你：可以了，翻译吧

Claude：
<<<DRAMA_ENGLISH>>>
[口语化英文翻译...]
<<<END_ENGLISH>>>
```

你也可以在同一轮消息中直接粘贴剧情简介：

```
你：帮我写短剧解说文案 [附上字幕文件]
剧情简介：
[把剧情简介正文粘贴在这里...]
```

如果你没有提供剧情简介，Skill 会先提示你确认是否不提供，再继续生成。

## 规则说明

- **剧情概述**是内部步骤，只给 Claude 自己理解剧情用，不会输出
- **视频抽帧**只在字幕稀疏时辅助生成内部画面事实清单，不会直接输出给用户
- **解说文案**严格禁止出现人物名，全部用代词（他/她/男人/女人/男主/女主）
- **英文翻译**是口语化风格，不是书面直译，适合 TikTok/Reels 等平台
