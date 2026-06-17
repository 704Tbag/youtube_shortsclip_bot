# Project Structure

```
youtube-shorts-bot/
│
├── setup_wizard.py             ← START HERE (interactive setup guide)
├── test_local.py               ← Test the pipeline without YouTube
│
├── main.py                     ← Daily orchestrator (what GitHub Actions runs)
├── content_generator.py        ← Generates poems or football summaries
├── tts_generator.py            ← Text → narration audio (using gTTS)
├── video_builder.py            ← Audio + text → animated MP4
├── youtube_uploader.py         ← Uploads MP4 to your YouTube channel
├── get_refresh_token.py        ← One-time helper to get OAuth token
│
├── requirements.txt            ← Python dependencies (pip install -r ...)
├── .gitignore                  ← Prevents committing secrets
│
├── README.md                   ← Project overview
├── OAUTH_SETUP.md              ← Manual OAuth setup (if not using wizard)
│
└── .github/
    └── workflows/
        └── daily_short.yml     ← GitHub Actions schedule (runs daily)
```

## Which file does what?

### To get started
- **`setup_wizard.py`** — Run this first. It guides you through the entire setup.
- **`test_local.py`** — Test the video generation locally (no YouTube) before committing to GitHub.

### The bot itself
- **`main.py`** — Orchestrates everything. GitHub Actions runs this once per day.
- **`content_generator.py`** — Creates original poems or football summaries.
- **`tts_generator.py`** — Converts text to spoken narration (MP3).
- **`video_builder.py`** — Builds the animated vertical video from narration + text.
- **`youtube_uploader.py`** — Uploads the finished video to YouTube.

### Setup & config
- **`get_refresh_token.py`** — One-time script to authenticate with your YouTube account.
- **`.github/workflows/daily_short.yml`** — Tells GitHub Actions when/how to run the bot.
- **`requirements.txt`** — Python libraries needed (installed automatically by GitHub Actions).

### Documentation
- **`README.md`** — Overview & quick start.
- **`OAUTH_SETUP.md`** — Detailed manual OAuth setup steps (if you skip the wizard).

## Typical workflow

1. Download / clone this folder
2. `python setup_wizard.py` (follows you through everything)
3. Push to GitHub
4. GitHub Actions runs automatically every day at 12:00 UTC
5. Videos post to your YouTube channel (check your Shorts feed)

---

**That's it!** The bot runs itself from then on.
