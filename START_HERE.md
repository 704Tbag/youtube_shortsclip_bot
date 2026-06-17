# 🎬 START HERE

## What is this?

A bot that automatically creates and uploads **daily YouTube Shorts** to your channel:
- **Poems** or **Football scores** (alternates daily)
- Narrated with AI voice
- Animated vertical video
- Posted automatically at 12:00 UTC

**Zero cost to run.** Runs on GitHub (free).

---

## How to set it up (5 minutes)

### Step 1: Make sure you have Python
Open a terminal and check:
```bash
python --version
```
Should show `Python 3.8+`. If not, download from https://python.org

### Step 2: Run the setup wizard
In this folder, run:
```bash
python setup_wizard.py
```

Follow the on-screen prompts. It will:
1. Guide you to create a Google Cloud project (free)
2. Get your YouTube OAuth credentials
3. Help you push to GitHub
4. Test your first video

**That's it.** Your bot will post daily from then on.

---

## What happens next?

Once setup is complete:
- Every day at 12:00 UTC, GitHub automatically runs your bot
- It generates content, creates an MP4 video, and uploads it to your YouTube channel
- A new Short appears in your channel's Shorts feed

You can change the upload time by editing `.github/workflows/daily_short.yml` (line with `cron:`).

---

## Questions?

- **I want to test locally first** → Run `python test_local.py`
- **I prefer manual setup** → Read `OAUTH_SETUP.md`
- **What does each file do?** → See `FILE_STRUCTURE.md`
- **Can I customize the poems/football?** → See `README.md` → "Things worth knowing"

---

## TL;DR

```bash
python setup_wizard.py
```

That's literally all you need to do. The wizard handles the rest.

**Questions?** Open `OAUTH_SETUP.md` or `README.md`.

**Ready?** Run the wizard above. ⬆️
