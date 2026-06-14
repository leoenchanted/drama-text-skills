# drama-text-skills v4.0

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

## File Structure

```text
drama-text-skills/
├── SKILL.md
├── references/
│   ├── english-recap-rules.md
│   └── retention-rules.md
├── templates/
│   ├── en-recap-reference/
│   │   ├── 01-terminal-illness-divorce.txt
│   │   ├── 02-blind-wife-birthday-betrayal.txt
│   │   └── ...
│   └── legacy-cn-reference/
│       ├── 1.txt
│       └── ...
└── README.md
```

## Template Folders

### `templates/en-recap-reference/`

Primary reference folder.

These are English short drama recap samples. The skill reads them first and learns:

- hook placement
- short-line rhythm
- emotional escalation
- twist timing
- cliffhanger style
- transition phrases
- English recap tone

It should imitate the format, not copy the content.

### `templates/legacy-cn-reference/`

Old Chinese reference scripts.

These are kept only for legacy comparison or Chinese-style reference. They are not the default reference source for English recap generation.

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
```

Marked fields have highest priority.

## Default Workflow

1. Read all English reference scripts in `templates/en-recap-reference/`.
2. Read `references/english-recap-rules.md`.
3. Understand the Chinese source material.
4. Extract the heroine pain point, male lead mistake, villain scheme, biggest twist, regret point, and cliffhanger.
5. Reorder the story around the strongest hook, not the original scene order.
6. Localize Chinese names and institutions into natural fictional English names.
7. Write the final English voiceover recap.
8. Internally check whether the first 30 seconds are strong enough.
9. If weak, rewrite before output.

## Output Format

Output only the final English recap script.

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
- explanation
- notes
- bullet points
- scene headings
- camera directions
- timestamps
- Chinese comments
- delimiter markers

## Length

Default:

- 900-1200 English words

If requested:

- short version: 500-700 words
- long version: 1500-2000 words

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
