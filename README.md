# drama-text-skills v4.1

English short drama recap scriptwriting skill.

It rewrites Chinese short drama scripts, subtitles, dialogue transcripts, or cleaned outlines into high-retention English voiceover recap scripts for TikTok, Reels, and YouTube Shorts.

This skill does not translate line by line.  
It reconstructs the story around the strongest hook, emotional pressure, villain conflict, regret, revenge/payoff, and cliffhanger.

## What Changed

The default output is now:

- English only
- short voiceover lines
- no paragraphs
- no bullet points
- no title
- no analysis
- localized English names
- cliffhanger ending
- automatic genre detection
- template selection by genre
- final quality score and scoring logic

## File Structure

```text
drama-text-skills/
├── SKILL.md
├── references/
│   ├── english-recap-rules.md
│   ├── english-style-polish.md
│   └── retention-rules.md
├── templates/
│   └── en-recap-reference/
│       └── modern-urban（现代都市）/
│           ├── revenge-face-slap（复仇打脸）/
│           ├── family-wealth（豪门家产）/
│           ├── workplace-counterattack（职场反击）/
│           ├── female-growth（女性成长）/
│           └── marriage-betrayal（婚姻背叛）/
└── README.md
```

## Template Folders

### `templates/en-recap-reference/`

Primary and only active reference folder for v4.1.

These are English short drama recap samples organized by a two-level folder structure:

- First level: broad genre/world, such as `modern-urban（现代都市）`, `costume（古装）`, `fantasy（奇幻）`.
- Second level: emotional engine, such as `marriage-betrayal（婚姻背叛）`, `revenge-face-slap（复仇打脸）`.

The skill does not blindly read all templates by default. It detects the broad genre and emotional engine, then selects 2-4 matching templates from the closest folder(s).

The skill learns:

- hook placement
- short-line rhythm
- emotional escalation
- twist timing
- cliffhanger style
- transition phrases
- English recap tone

It should imitate the format, not copy the content.

To add new reference scripts later, put the file into the closest emotional-engine folder. If the topic is truly new, create a new folder using English plus Chinese note, for example:

```text
costume（古装）/palace-revenge（宫斗复仇）/
fantasy（奇幻）/rebirth（重生）/
suspense-crime（悬疑犯罪）/hidden-truth（真相揭露）/
```

## Input

The user may provide:

- raw Chinese script
- short drama subtitle transcript
- dialogue-only transcript
- cleaned Chinese plot outline
- scene-by-scene summary
- list of key events
- minimal input card plus raw script

Useful marked fields:

```text
最大爆点：
人物关系：
核心误会：
女主死心点：
男主追悔点：
结尾卡点：
必须保留设定：
长度/时长：
```

Marked fields have highest priority.

## Default Workflow

1. Read `references/english-recap-rules.md` and `references/english-style-polish.md`.
2. Inspect the category folders under `templates/en-recap-reference/`.
3. Understand the Chinese source material.
4. Detect the story category from the source, unless the user specifies it.
5. Select 2-4 matching reference templates from the closest folder(s).
6. Extract the heroine pain point, male lead mistake, villain scheme, biggest twist, regret point, and cliffhanger.
7. Reorder the story around the strongest hook, not the original scene order.
8. Localize Chinese names and institutions into natural fictional English names.
9. Write the final English voiceover recap.
10. Run the Quality Gate and revise internally if any score is below 4.
11. Output the script, final quality score, and scoring logic.

## Output Format

Output the final English recap script first.

Use short lines:

```text
She took off the wedding ring
she had worn for five years
and said
in another life
she would never love him again
Then she poured gasoline
all over the villa
the man used to trap her
```

Do not output:

- title
- analysis
- notes
- bullet points
- scene headings
- camera directions
- timestamps
- Chinese comments
- delimiter markers

After the script, output:

```text
Quality Score: [overall]/5
Opening Hook: [score]/5
Emotional Pressure: [score]/5
Twist Density: [score]/5
English Naturalness: [score]/5
Cliffhanger Strength: [score]/5
Scoring Logic: [1-3 short English sentences explaining the recap logic.]
```

## Length

The user controls length.

If the user gives a word count, runtime, or platform requirement, follow it.

If the user does not specify length, the skill chooses a suitable length based on story complexity, confirmed plot information, and retention needs.

If the source is very long, the skill should not include everything. It should choose the most viral emotional storyline.

## Key Rules

- First line must be shocking.
- First 30 seconds must include conflict, emotional reason to keep watching, and at least one twist.
- Do not start with slow background setup.
- Add a new twist or emotional beat every 20-30 seconds.
- Make the heroine's pain clear.
- Make the male lead's mistake obvious.
- Make the villain hateable.
- Put the strongest viral point early.
- End with a cliffhanger.
- Localize Chinese names into natural fictional English names.

## Low-Context Input

If the transcript is dialogue-only or missing visuals, the skill reconstructs scene blocks internally.

It should not invent unsupported visual actions.  
If speaker ownership or location is unclear, it should use neutral narration instead of forcing details.
