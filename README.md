# Daily YouTube Shorts Bot (Poems + Football, alternating)

A simple, free-to-run pipeline that, once a day:
1. Generates an original short poem **or** a football scores roundup (alternates daily)
2. Narrates it with text-to-speech
3. Builds a short animated vertical video with a quiet background tone
4. Uploads it to your YouTube channel as a Short

It runs on **GitHub Actions**, which is free for this kind of light daily job and needs no server of your own.

## What you need before starting

- A GitHub account (free)
- The Google account that owns your YouTube channel
- ~5 minutes
- A terminal/command line (Windows, Mac, or Linux)

## Quick Start — Setup Wizard

The easiest way is to run the setup wizard on your computer:

```bash
python setup_wizard.py
```

This walks you through everything interactively:
1. Creating a Google Cloud project (free)
2. Enabling the YouTube Data API
3. Creating OAuth credentials
4. Getting your YouTube refresh token
5. Pushing to GitHub
6. Adding secrets
7. Running your first video generation test

**That's it.** Once the test passes, your bot posts daily to your channel automatically.

### Alternative: Manual Setup

If you prefer to do steps manually, see `OAUTH_SETUP.md` for detailed instructions.

### Optional Upgrades

Add these as GitHub secrets for better quality (but not required):

| Secret name | What it does |
|---|---|
| `ANTHROPIC_API_KEY` | Uses Claude to generate better poems (instead of free built-in templates) |
| `SPORTS_API_KEY` | More reliable football data (get free key from thesportsdb.com) |

## How content alternates
`content_generator.py` picks poem vs. football based on whether the day-of-year is even or odd — so it's a clean 50/50 split with zero stored state between runs.

## Things worth knowing

- **Quota**: each upload uses about 1,600 of YouTube's 10,000 daily API quota units — one video a day is nowhere near the limit.
- **Copyright**: poems are generated fresh (template or Claude), never copied from existing published poems. The background music is a synthesized tone, not a sampled/copyrighted track. Football content is a stats/scores summary, not real match footage or player likenesses — uploading actual broadcast clips or depicting real players visually would risk takedowns/strikes.
- **Voice quality**: the default uses gTTS (free, no key, slightly robotic). For a more natural voice, swap `tts_generator.py` to call ElevenLabs or Google Cloud Text-to-Speech — `main.py` doesn't need to change, since it just calls `generate_narration(text) -> mp3_path`.
- **Visual style**: currently a simple gradient background with fading-in text lines — intentionally simple so it runs reliably in CI without heavy GPU/AI video generation. If you want richer animation later, swap out `video_builder.py` similarly.
- **Costs**: as configured (gTTS + template poems + free sports API), this runs at $0/day. The only optional cost is `ANTHROPIC_API_KEY` usage if you turn that on.

## File overview
```
main.py                 - orchestrates the daily run
content_generator.py    - poem / football script + title generation
tts_generator.py        - text -> narration mp3
video_builder.py        - narration + text -> finished mp4
youtube_uploader.py     - uploads the mp4 to your channel
get_refresh_token.py    - one-time local script to get OAuth credentials
requirements.txt        - Python dependencies
.github/workflows/      - the daily schedule definition
```
