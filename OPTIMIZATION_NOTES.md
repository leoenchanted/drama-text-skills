# drama-text-skills v4.1 优化说明

## 2026-06-24 v4.1 内部增强：模板分类、英文润色、质量评分

这次不改版本名，仍然保持：

```yaml
name: drama-text-skills-v4-1
```

但增强了 v4.1 的实际工作流。

新增：

```text
references/english-style-polish.md
```

### 模板分类文件夹

当前 10 篇模板已按“两层分类”放入 `templates/en-recap-reference/`。

第一层是大题材/世界观，使用英文 slug + 中文括号。  
第二层是情绪引擎/故事引擎，也使用英文 slug + 中文括号。

现在 skill 使用时会：

1. 先判断大题材，比如现代都市、古装、奇幻、悬疑犯罪。
2. 再判断情绪引擎，比如婚姻背叛、复仇打脸、豪门家产、职场反击、女性成长。
3. 如果用户指定题材，就按用户题材选模板。
4. 如果用户没指定题材，就根据字幕/剧情自动判断。
5. 从最接近的情绪引擎文件夹中选择 2-4 篇最相关参考模板。
6. 不再默认盲读全部模板。

当前目录结构：

```text
templates/en-recap-reference/
└── modern-urban（现代都市）/
    ├── revenge-face-slap（复仇打脸）/
    ├── family-wealth（豪门家产）/
    ├── workplace-counterattack（职场反击）/
    ├── female-growth（女性成长）/
    └── marriage-betrayal（婚姻背叛）/
```

后续新增模板时，直接把文案放入对应情绪引擎文件夹即可。  
如果出现新题材，可以新增类似：

```text
costume（古装）/palace-revenge（宫斗复仇）/
fantasy（奇幻）/rebirth（重生）/
suspense-crime（悬疑犯罪）/hidden-truth（真相揭露）/
```

### English Polish Rules

`english-style-polish.md` 用来减少机翻腔和僵硬表达。

重点优化：

- 减少 `after hearing this`、`at this moment`、`the woman felt very sad` 等重复表达。
- 把平淡情绪改成更适合英文 recap 的动作和后果。
- 控制 transition phrase 过度重复。
- 强化女主从受伤到反击的稳定感。
- 让旁白更像英文短剧解说，而不是中文直译。

### Quality Gate

新增最终质量评分机制。

生成后内部评分：

- Opening Hook
- Emotional Pressure
- Twist Density
- English Naturalness
- Cliffhanger Strength

任意低于 4 分，先内部重写。

最终输出除了脚本，还会附上：

```text
Quality Score
Opening Hook
Emotional Pressure
Twist Density
English Naturalness
Cliffhanger Strength
Scoring Logic
```

### 长度规则调整

固定默认长度已取消。

现在规则是：

- 用户指定长度/字数/时长时，按用户要求。
- 用户不指定时，根据剧情复杂度和 retention 需要自动决定。
- 不为了凑字数重复情绪。
- 不为了参考模板长度而强行写长。

## 2026-06-24 最新升级：v4.1 模板替换

这次更新把旧模板参考文案全部替换掉，只保留用户新提供的 10 篇英文 recap 参考稿。

当前 active 模板目录：

```text
templates/en-recap-reference/
```

当前 v4.1 参考文案：

```text
01-swapped-daughters-inheritance-scheme.txt
02-fathers-secret-double-family-revenge.txt
03-best-friend-husband-affair-revenge.txt
04-wealthy-brothers-lost-sister.txt
05-inheritance-fight.txt
06-company-betrayal-after-saving-business.txt
07-woman-chooses-herself.txt
08-mistaken-opening-husband-affair.txt
09-cheating-husband-wife-divorce.txt
10-chasing-wife-regret.txt
```

已移除旧参考：

- v4.0 的 12 篇英文参考文案。
- 旧的中文 legacy 模板目录。

Skill 内部名称已更新为：

```yaml
name: drama-text-skills-v4-1
```

文件夹目录名保持不变，仍然是：

```text
drama-text-skills/
```

## 2026-06-14 最新升级：英文 Recap 模式

这次继续优化后，`drama-text-skills-v4-0` 已从“中文短剧文案 + 确认后英文翻译”的两阶段模式，升级为 **直接生成英文短剧 recap voiceover script**。

最新默认输出：

- 英文短剧解说脚本。
- 短行 voiceover 格式。
- 不分段成大段落。
- 不输出标题、分析、解释、分隔符。
- 不逐句翻译中文。
- 根据中文素材重构故事顺序。
- 自动本地化中文人名、家族、公司、医院、学校等名称。
- 结尾必须保留 cliffhanger。

### 新增参考文案目录

新增主参考目录：

```text
templates/en-recap-reference/
```

本次导入了 12 篇英文短剧 recap 参考文案，并按题材重命名，例如：

```text
01-terminal-illness-divorce.txt
02-blind-wife-birthday-betrayal.txt
03-academic-betrayal-revenge.txt
04-rebirth-give-up-toxic-love.txt
05-pregnancy-child-betrayal.txt
06-ninety-nine-divorces-remarriage.txt
07-ex-wife-billionaire-reversal.txt
08-fake-death-heart-donation.txt
09-secret-marriage-certificate.txt
10-blind-wife-identity-stolen.txt
11-fire-memory-loss-regret.txt
12-wedding-uncle-reversal.txt
```

这些文件现在是默认优先读取的参考文案。

### 旧模板已归档

旧的中文模板已移动到：

```text
templates/legacy-cn-reference/
```

它们不再作为英文 recap 的默认参考源，只在需要中文风格对照或 legacy 参考时使用。

### 新增英文 Recap 规则文件

新增：

```text
references/english-recap-rules.md
```

它沉淀了这次新增的完整英文 recap 规则：

- 角色定位。
- 参考文案学习方式。
- 英文 voiceover 短行格式。
- 开头 3 秒 hook 规则。
- 前 30 秒留存规则。
- 爆款元素优先级。
- 故事重排规则。
- 女主痛点、男主错误、反派冲突处理。
- 中文人物关系理解。
- 人名和机构名本地化。
- dialogue-only transcript 处理。
- 默认长度 900-1200 English words。
- cliffhanger ending。
- final output only script。

### 核心行为变化

旧模式：

```text
中文脚本 → 用户确认 → 英文翻译
```

新模式：

```text
中文素材理解 → 爆点提取 → 英文结构重构 → 英文短剧 recap 输出
```

这意味着 skill 不再把英文当作中文稿的翻译结果，而是直接生成适合 TikTok / Reels / YouTube Shorts 的英文短剧解说稿。

## 一句话总结

这次优化把 `drama-text-skills-v4-0` 从“根据字幕写一篇短剧解说文案”，升级成了“按短视频留存节奏强制生成高爽感爆款文案”的 skill。

旧版更像：讲清楚剧情。  
新版更像：控制观众每隔几秒获得一次刺激。

## 旧版主要能力

旧版已经具备这些基础能力：

- 读取短剧字幕文件。
- 可选读取剧情简介。
- 读取 `templates/` 里的爆款文案模板。
- 生成 800-1000 字中文解说脚本。
- 用户确认后翻译成口语化英文。
- 使用固定分隔符输出，方便 Electron 桌面应用解析。
- 禁止人物名、禁止直接对话、一整段输出。

这些能力保留了，没有删除。

## 旧版核心问题

旧版更重视：

- 剧情概述是否完整。
- 模板风格是否模仿。
- 文案是否讲清楚。
- 字数是否达标。

但短剧爆款真正依赖的是：

- 开头 3 秒是否抓人。
- 爽点是否足够密。
- 反转是否持续出现。
- 冲突是否不断升级。
- 每一小段是否都有情绪奖励。

所以旧版可能写出“能看”的文案，但不一定“上头”。

## 新版新增内容

### 1. 新定位：Retention-first

新版在 `SKILL.md` 开头明确了核心定位：

> 这个 Skill 不是普通故事改写器，而是短视频留存节奏控制器。

生成目标从“写好故事”调整为：

- 3 秒内抓住观众。
- 每 60-100 个中文字给一次刺激。
- 每 150-250 个中文字出现一次反转、打脸或升级。
- 冲突越来越大，身份越来越反差，爽点越来越密。

### 2. 新增 Retention Beat Map

新版要求在正式写文案前，内部先规划 8-12 个节奏点。

每个节奏点要考虑：

- 3 秒钩子。
- 冲突点。
- 打脸点。
- 反转点。
- 视觉高潮。
- 升级点。
- 结尾悬念。

这个 Beat Map 不输出给用户，只用来约束最终文案。

### 3. 新增爽点密度硬约束

旧版只要求短句、口语化、有情绪张力。  
新版增加了明确节奏指标：

- 开头 60-80 字必须直接抛出强冲突或反差。
- 每 60-100 字必须有一个刺激点。
- 每 150-250 字必须升级一次冲突。
- 每 200-300 字安排一次视觉高潮。
- 不能连续 120 字以上只有解释、铺垫或背景说明。

这让 AI 不容易写成慢节奏剧情复述。

### 4. 新增短剧爽点类型识别

新版会先内部判断本集属于哪类短剧爽点：

- 隐藏大佬 / 扮猪吃虎
- 重生复仇 / 改命
- 闪婚霸总 / 隐婚撑腰
- 真假千金 / 豪门身份
- 追妻火葬场
- 逆袭打脸 / 被羞辱后反杀
- 灾难逃生 / 末日求生
- 甜宠误会 / 同居拉扯

不同类型走不同的爽点循环。

例如：

- 隐藏大佬：被轻视 → 露一手 → 全场震惊 → 更高身份压场。
- 重生复仇：前世背叛 → 这一世预判 → 反派入套 → 命运改写。
- 霸总撑腰：被羞辱 → 孤立无援 → 权势人物出现 → 当众反杀。
- 灾难逃生：无人相信 → 危机证据出现 → 倒计时逼近 → 生死选择。

### 5. 新增循环爽点结构

新版强制优先采用：

```text
压制 → 质疑 → 主角出手 → 众人震惊 → 反派不服 → 升级挑战 → 再次打脸
```

这让文案不只是“讲剧情”，而是不断制造情绪奖励。

### 6. 强化主角人设约束

新版新增主角稳定感规则：

- 主角要冷静、神秘、强大、情绪稳定。
- 面对羞辱时尽量淡定，靠行动反杀。
- 永远留有底牌。
- 如果原剧情主角弱或慌，也要把解说重心放在“即将反杀 / 已经看透 / 开始布局”的爽感上。

这样可以避免 AI 把爽文写成苦情剧或普通成长文。

### 7. 模板分析逻辑升级

旧版主要是“模仿模板风格”。  
新版改成从模板中提炼结构：

- 开头钩子。
- 爽点间隔。
- 打脸方式。
- 反转方式。
- 结尾悬念。

同时新增规则：

> 模板是结构参考，不是质量上限。遇到模板语言别扭时，保留节奏，重写表达。

这很重要，因为现有模板里有一些机翻腔，新版不会盲目复制。

### 8. 新增内部自检清单

新版输出前必须内部检查：

- 是否包含人物名。
- 是否包含引号或直接对话。
- 是否是一整段。
- 前 80 字是否有强钩子。
- 是否存在 120 字以上纯解释或铺垫。
- 是否有至少 5 个明确爽点。
- 结尾是否让人想看下一集。

这能减少格式错误和节奏跑偏。

### 9. 剧情简介逻辑更顺滑

旧版在没有剧情简介时更容易先停下来询问。  
新版改成：

- 如果字幕能支撑理解，就直接保守生成。
- 只有当字幕明显来自中间集、人物关系会严重影响准确性时，才询问用户是否补充。

这样更适合批量生产短剧文案，不会动不动卡住。

### 10. 新增独立规则文件

新增文件：

```text
references/retention-rules.md
```

里面沉淀了完整留存规则，包括：

- 高频爽点元素。
- 标准爽点循环。
- 不同题材的爽点变体。
- 800-1000 字文案的节奏换算。
- 开头钩子公式。
- 主角稳定感。
- 禁止内容。
- 自检问题。

这样 `SKILL.md` 不会变得太臃肿，以后也方便继续扩展。

### 11. README 更新

新版 `README.md` 从安装说明型文档，改成了使用和定位说明。

重点说明：

- 这个 skill 是 retention-first。
- 如何提供字幕和剧情简介。
- 模板的正确用法。
- 中文和英文输出格式。
- 关键节奏规则。

### 12. 移除视频抽帧步骤

后续优化中，视频抽帧步骤已移除。

原因：

- 使用率不高。
- 依赖 `ffmpeg/ffprobe`，增加维护成本。
- 自动抽帧会让流程变重，不适合高频批量生成文案。
- 大多数短剧文案任务只需要字幕和剧情简介即可完成。

现在如果字幕对白太少，skill 会要求用户补充剧情简介或关键画面描述，而不是自动抽帧分析视频。

## 文件变化汇总

本次主要修改：

```text
SKILL.md
README.md
references/retention-rules.md
```

已移除：

```text
scripts/video_context.py
```

未修改：

```text
templates/
```

也就是说，这次优化集中在 prompt 工作流和文案生成逻辑，并进一步去掉了低使用率的视频抽帧链路。

## 优化后的预期效果

新版输出会更倾向于：

- 开头更猛。
- 铺垫更少。
- 冲突更密。
- 打脸更频繁。
- 反转更靠前。
- 主角更稳。
- 结尾更有追看欲。

它会尽量避免：

- 普通故事复述。
- 长篇背景解释。
- 情绪慢热。
- 逻辑完整但不爽。
- 文笔顺但不抓人。

## 后续可继续优化方向

后续如果要进一步增强，可以继续加：

- 不同题材的专用 prompt 模块。
- 账号风格配置，比如土味强爽、悬疑强钩子、TikTok 英文翻译友好型。
- 文案评分器，对钩子强度、爽点密度、升级感打分。
- 自动检测输出中每 100 字是否真的有刺激点。
- 更多高质量模板，替换当前偏机翻的样本文案。
