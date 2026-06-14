---
name: drama-text-skills-v4-0
description: "English short drama recap scriptwriting skill. Rewrites Chinese short drama scripts, subtitles, or cleaned outlines into high-retention TikTok/Reels/YouTube Shorts English voiceover recap scripts with strong hooks, short lines, emotional escalation, localized names, villain conflict, regret, revenge/payoff, and cliffhanger endings. Trigger words: short drama recap, English recap, TikTok recap, drama copywriting, 短剧英文解说, 英文短剧文案."
metadata:
  tags: copywriting, short-drama, english-recap, retention, voiceover
---

# drama-text-skills v4.0

## Core Positioning

This skill writes **English short drama recap voiceover scripts** from Chinese short drama material.

Do not produce a plot summary.  
Do not translate line by line.  
Reconstruct the story into a viral English-language recap format.

Default output is an English ready-to-record voiceover script with short lines, high emotional pressure, frequent twists, localized names, and an unresolved cliffhanger.

## Required Reference Loading

Before writing any final recap script:

1. Read all files in `templates/en-recap-reference/`.
2. Read `references/english-recap-rules.md`.
3. Use `references/retention-rules.md` only as secondary retention support.
4. Use `templates/legacy-cn-reference/` only if the user explicitly asks for Chinese-style comparison or legacy Chinese references.

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

### Step 2 - Handle Dialogue-Only Transcripts

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

### Step 3 - Choose The Opening Hook

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

### Step 4 - Rebuild The Story Order

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

### Step 5 - Localize Names

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

### Step 6 - Write The English Recap

Default length:

- 900-1200 English words
- 500-700 words if the user asks for short
- 1500-2000 words if the user asks for long

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
- Do not include analysis or explanations.
- Avoid Chinese-style translated phrasing.
- Avoid complicated grammar and literary descriptions.

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

### Step 7 - Ending

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

### Step 8 - Self-Check

Before final output, check internally:

1. Is the first line shocking enough?
2. Does the first 3 seconds create curiosity?
3. Does the first 30 seconds include a strong hook?
4. Is the strongest viral point placed early?
5. Are the lines short enough for voiceover?
6. Is there a new twist or emotional beat every 20-30 seconds?
7. Is the heroine's pain clear?
8. Is the male lead's mistake clear?
9. Is the villain hateable enough?
10. Are Chinese names localized into natural English names?
11. Is the ending a cliffhanger?

If any answer is no, rewrite before final output.

## Final Output Rules

Output only the English recap voiceover script.

Do not include:

- title
- analysis
- explanation
- notes
- bullet points
- scene directions
- timestamps
- Chinese comments
- self-evaluation
- delimiter markers

The final text should look like a ready-to-record English short drama recap script.
