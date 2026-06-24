---
name: drama-text-skills-v4-1
description: "English short drama recap scriptwriting skill. Rewrites Chinese short drama scripts, subtitles, or cleaned outlines into high-retention TikTok/Reels/YouTube Shorts English voiceover recap scripts with strong hooks, short lines, emotional escalation, localized names, villain conflict, regret, revenge/payoff, and cliffhanger endings. Trigger words: short drama recap, English recap, TikTok recap, drama copywriting, 短剧英文解说, 英文短剧文案."
metadata:
  tags: copywriting, short-drama, english-recap, retention, voiceover
---

# drama-text-skills v4.1

## Core Positioning

This skill writes **English short drama recap voiceover scripts** from Chinese short drama material.

Do not produce a plot summary.  
Do not translate line by line.  
Reconstruct the story into a viral English-language recap format.

Default output is an English ready-to-record voiceover script with short lines, high emotional pressure, frequent twists, localized names, and an unresolved cliffhanger.

## Required Reference Loading

Before writing any final recap script:

1. Read `references/english-recap-rules.md`.
2. Read `references/english-style-polish.md`.
3. Inspect the category folders under `templates/en-recap-reference/`.
4. Infer the story category from the user input unless the user explicitly names the category.
5. Select 2-4 matching reference scripts from the closest category folder(s).
6. Use `references/retention-rules.md` only as secondary retention support.

Read all templates only if the user explicitly asks to reference all templates or if the source story clearly combines many categories.

Learn from reference scripts:

- structure
- pacing
- short-line rhythm
- hook placement
- emotional escalation
- twist placement
- cliffhanger style
- common transition phrases
- recap voiceover tone

Do not copy exact sentences, paragraphs, character relationships, plot points, or names from the references.

## Inputs

The user may provide any of these:

- raw Chinese script
- dialogue-only transcript
- cleaned Chinese plot outline
- scene-by-scene summary
- list of key events
- minimal input card plus raw script

User-marked fields have highest priority:

- `最大爆点`
- `人物关系`
- `核心误会`
- `女主死心点`
- `男主追悔点`
- `结尾卡点`
- `必须保留设定`
- requested length or duration

Do not require the user to fill a long form. Infer missing information when reasonable. Ask follow-up questions only when relationship logic is impossible to understand.

## Internal Workflow

Do all analysis internally unless the user asks for analysis.

### Step 1 - Understand The Chinese Material

Read the full user input first. Extract:

- drama type
- main characters
- heroine's pain point
- male lead's misunderstanding or mistake
- villain or mistress scheme
- strongest viral element
- biggest twist
- best opening scene
- truth reveal
- male lead regret point
- revenge or emotional payoff
- ending cliffhanger point

Be careful with Chinese relationship terms such as 小三, 白月光, 替身, 养女, 亲生女儿, 继母, 未婚妻, 前妻, 小叔, 舅舅, 哥哥, 养父, and 亲生父母.

If user-provided cleaned notes conflict with raw dialogue, prioritize the user's marked notes.

### Step 2 - Detect Genre And Select Templates

If the user states the genre, use it.

If the user does not state the genre, infer it from:

- relationship logic
- betrayal type
- villain goal
- heroine pain point
- male lead mistake
- wealth/inheritance conflict
- child or paternity conflict
- workplace/company conflict
- revenge or regret engine

Use the folder structure under `templates/en-recap-reference/` as the category map.

Folder structure rule:

- First level = broad genre/world, written as English plus Chinese note, e.g. `modern-urban（现代都市）`, `costume（古装）`, `fantasy（奇幻）`.
- Second level = emotional engine or story engine, e.g. `marriage-betrayal（婚姻背叛）`, `revenge-face-slap（复仇打脸）`.

Current active folders:

- `modern-urban（现代都市）/revenge-face-slap（复仇打脸）`
- `modern-urban（现代都市）/family-wealth（豪门家产）`
- `modern-urban（现代都市）/workplace-counterattack（职场反击）`
- `modern-urban（现代都市）/female-growth（女性成长）`
- `modern-urban（现代都市）/marriage-betrayal（婚姻背叛）`

Select 2-4 matching reference scripts:

- First choose the broad genre folder.
- Then choose the closest emotional-engine folder.
- If the story crosses engines, read 1-2 related emotional-engine folders.
- If an emotional-engine folder contains multiple templates, prefer the most topically similar filenames.
- Do not read unrelated folders unless the user asks.

Do not expose this template-selection analysis unless the user asks.

### Step 3 - Handle Dialogue-Only Transcripts

If the input is mainly subtitles or dialogue, assume it may be missing visuals, speakers, scene changes, and actions.

Internally reconstruct scene blocks:

- scene location if supported
- characters present if supported
- speaker ownership of important lines
- visible actions if supported
- emotional conflict
- villain action
- heroine pain point
- male lead misunderstanding
- story function of the scene

Do not invent unsupported visual actions. If a speaker or location is unclear, use neutral narration such as "at that moment" instead of forcing a specific scene.

### Step 4 - Choose The Opening Hook

Do not follow original scene order blindly. Open with the strongest retention moment.

Preferred hook types:

- terminal illness
- fake death
- rebirth
- revenge return
- wedding humiliation
- hidden identity reveal
- public humiliation
- pregnancy or paternity reveal
- memory loss twist
- male lead discovering the truth too late
- heroine giving up completely

Use one of these opening structures when suitable:

- Truth Reveal First
- Death or Disappearance First
- Public Slap-in-the-Face First
- Regret First
- Revenge Return First

The first line must be shocking. The first 30 seconds must include the main conflict, an emotional reason to keep watching, and at least one twist or secret.

Never start with slow background setup, childhood, ordinary marriage life, company setup, family introduction, or slow romance unless it is immediately tied to a shocking event.

### Step 5 - Rebuild The Story Order

A strong recap usually follows:

1. shocking high-energy scene
2. immediate emotional conflict
3. short flashback explaining why it happened
4. repeated humiliation or misunderstanding
5. villain manipulation
6. heroine pain point
7. male lead makes the wrong choice
8. truth begins to surface
9. male lead regrets
10. heroine refuses to forgive or disappears
11. cliffhanger

Compress or remove daily conversations, repeated arguments, business details with no emotional function, low-stakes dialogue, side characters with no viral purpose, and slow romance setup.

Keep and amplify betrayal, misunderstanding, humiliation, sacrifice, injury, terminal illness, pregnancy, identity reversal, regret, revenge, public confrontation, emotional breaking point, final goodbye, and cliffhanger.

### Step 6 - Localize Names

Localize Chinese names, families, companies, hospitals, schools, and organizations into natural fictional English-speaking names.

Do not use pinyin unless the user specifically asks.  
Do not use real celebrity names or famous real companies.  
Keep names easy for AI voiceover and consistent throughout.

Examples:

- 顾寒州 -> Benjamin Kingsley
- 沈晚 -> Anna Sterling
- 林雪 -> Linda Whitmore
- 顾氏集团 -> Kingsley Corporation
- 傅氏集团 -> Sterling Group

Do not explain name changes in the final output.

### Step 7 - Write The English Recap

Length:

- Follow the user's requested length, word count, runtime, or platform requirement when provided.
- If the user does not specify length, choose the length based on story complexity and retention needs.
- Do not force a fixed word count.
- Do not add repetitive emotion or filler just to make the script longer.
- If the source is short or thin, keep the recap tight.
- If the source has many strong twists, allow a longer recap.

Voiceover rules:

- English only.
- Use simple, direct, dramatic English.
- Use short lines.
- Each line should contain one action, one reveal, or one emotion.
- Do not write paragraphs.
- Do not write bullet points.
- Do not write scene headings.
- Do not write camera directions.
- Do not write timestamps.
- Do not include analysis or explanations inside the recap script.
- Avoid Chinese-style translated phrasing.
- Avoid complicated grammar and literary descriptions.
- Apply `references/english-style-polish.md` before final output.

Use transition phrases naturally:

- but he did not know
- what he did not know was
- only then did he realize
- at that moment
- the next second
- however
- just then
- meanwhile
- even worse
- what broke her completely was
- from that day on
- for the first time
- he finally understood
- but it was already too late
- the truth was even crueler
- this was only the beginning

### Step 8 - Ending

The ending must not feel fully complete. End with a cliffhanger.

Good ending patterns:

- someone suddenly appears
- the person at the door makes everyone freeze
- the truth is even more terrifying
- this is only the beginning
- the woman they thought was dead returns
- she walks in with another man
- he does not know she has already prepared her revenge

Do not end with a moral lesson or a fully resolved happy ending.

### Step 9 - Quality Gate

Before final output, score internally from 1-5:

- Opening Hook
- Emotional Pressure
- Twist Density
- English Naturalness
- Cliffhanger Strength

If any score is below 4, revise internally before final output.

Also check:

1. Does the first 3 seconds create curiosity?
2. Does the first 30 seconds include a strong hook?
3. Is the strongest viral point placed early?
4. Are the lines short enough for voiceover?
5. Is the heroine's pain clear?
6. Is the male lead's mistake clear?
7. Is the villain hateable enough?
8. Are Chinese names localized into natural English names?

Final output must include the script, the quality score, and a concise scoring logic explanation.

## Final Output Rules

Output the English recap voiceover script first, then a compact quality score section.

Do not include:

- title
- notes
- bullet points
- scene directions
- timestamps
- Chinese comments
- self-evaluation
- delimiter markers

Use this ending format after the script:

```text
Quality Score: [overall]/5
Opening Hook: [score]/5
Emotional Pressure: [score]/5
Twist Density: [score]/5
English Naturalness: [score]/5
Cliffhanger Strength: [score]/5
Scoring Logic: [1-3 short English sentences explaining the opening logic, emotional escalation, twist/reveal structure, and cliffhanger.]
```

The script itself should still look like a ready-to-record English short drama recap.
