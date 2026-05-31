# drama-text-skills

Retention-first 短剧解说文案生成器。输入短剧字幕、可选剧情简介和视频，生成适合抖音 / TikTok / Reels 的高爽感解说脚本，并支持确认后翻译成口语化英文。

这个 skill 的核心不是“把故事讲完整”，而是强制控制：

- 3 秒钩子
- 高频冲突
- 每 10-20 秒一次爽点
- 打脸、反转、震惊、身份反差
- 越来越大的升级感

## 文件结构

```text
drama-text-skills/
├── SKILL.md
├── references/
│   └── retention-rules.md
├── scripts/
│   └── video_context.py
├── templates/
│   ├── 1.txt
│   ├── 2.txt
│   └── ...
└── README.md
```

## 输入建议

### 1. 字幕文件

提供 `.txt` 或 SRT 风格字幕。带时间轴更好：

```text
1
00:00:01,000 --> 00:00:03,000
这里是字幕内容
```

### 2. 剧情简介（可选）

如果字幕来自中间集，建议在对话中粘贴：

```text
剧情简介：
[前情、人物关系、核心矛盾]
```

也可以提供文件名包含 `剧情`、`简介`、`summary`、`plot` 的文本文件。

### 3. 视频文件（可选）

如果对白少、很多剧情靠画面表现，把视频和字幕放在同一目录并保持同名：

```text
episode01.mp4
episode01.txt
```

字幕稀疏时，skill 会用 `scripts/video_context.py` 抽取关键画面辅助理解。

## 模板

把爆款短剧解说文案放入 `templates/`。推荐 8-10 篇。

模板不会被机械复制。skill 会提炼：

- 开头钩子
- 爽点间隔
- 打脸方式
- 反转方式
- 结尾悬念

如果模板语言比较机翻，skill 会保留节奏，重写表达。

如果模板为空，skill 也可以先基于内置 retention 规则生成；后续补充模板后，风格会更贴近你的账号。

## 使用方式

示例：

```text
帮我根据这个字幕写一个短剧爆款解说文案
```

也可以指定方向：

```text
帮我写成抖音风格，高爽感，隐藏大佬一路打脸，节奏要非常快
```

或者：

```text
帮我写成 TikTok 英文号适合翻译的中文底稿，冲突密一点，结尾留强悬念
```

## 工作流程

1. 读取字幕、剧情简介、可选视频画面。
2. 内部压缩剧情事实。
3. 判断短剧爽点类型，比如重生复仇、隐藏大佬、闪婚霸总、灾难逃生。
4. 分析模板结构。
5. 内部制作 Retention Beat Map。
6. 生成 800-1000 字中文一整段文案。
7. 等用户确认。
8. 用户确认后再生成英文翻译。

## 中文输出格式

```text
<<<DRAMA_SCRIPT>>>
[800-1000 字中文解说文案，一整段，不使用人物名，无直接对话]
<<<END_SCRIPT>>>
```

## 英文输出格式

```text
<<<DRAMA_ENGLISH>>>
[口语化英文翻译，一整段，不使用人物名，无直接对话]
<<<END_ENGLISH>>>
```

## 关键规则

- 不出现人物名，全部改成他、她、男人、女人、男主、女主、对方等泛称。
- 不使用直接引号或完整对话。
- 不分段，输出一整段。
- 前 60-80 字必须有强钩子。
- 每 60-100 字至少一个刺激点。
- 每 150-250 字升级一次冲突。
- 结尾必须留下悬念、身份反转或下一集爆点。

## 视频抽帧工具

手动运行：

```bash
python3 scripts/video_context.py --subtitle path/to/episode.txt --video path/to/episode.mp4
```

可选参数：

```bash
python3 scripts/video_context.py --subtitle path/to/episode.txt --video path/to/episode.mp4 --max-points 18 --gap-threshold 3.0 --out path/to/output
```

输出：

- `manifest.json`：记录字幕稀疏判断、抽帧时间点和图片路径。
- `sheets/sheet_001.jpg`：带时间戳拼图，优先用于画面理解。
- `frames/frame_001_00-01-12.jpg`：必要时查看单帧。

抽帧结果默认只给 AI 内部理解，不主动输出给用户。
