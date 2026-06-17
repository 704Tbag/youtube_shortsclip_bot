# YouTube OAuth Setup (One-Time, Takes ~5 Minutes)

This is the ONE step that requires your direct interaction with Google. After this, everything runs automatically in GitHub Actions.

## Step 1: Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click **"Select a Project"** at the top → **"NEW PROJECT"**
3. Name it: `youtube-shorts-bot` (or whatever)
4. Click **CREATE**
5. Wait for it to finish (might take 30 seconds)

## Step 2: Enable YouTube Data API v3

1. In the Cloud Console, go to **APIs & Services** (left sidebar)
2. Click **+ ENABLE APIS AND SERVICES** (top center)
3. Search for: `YouTube Data API v3`
4. Click the result
5. Click **ENABLE**
6. Wait ~10 seconds for it to show "API enabled"

## Step 3: Create OAuth Credentials

1. In **APIs & Services**, click **Credentials** (left sidebar)
2. Click **+ CREATE CREDENTIALS** (top left)
3. Choose **OAuth Client ID**
4. If prompted: click **CREATE CONSENT SCREEN** first
   - Choose **External** user type
   - Fill in:
     - App name: `YouTube Shorts Bot`
     - User support email: your email
     - Developer contact: your email
   - Click **SAVE AND CONTINUE** twice (skip optional scopes)
   - Click **BACK TO CREDENTIALS**
5. Now click **+ CREATE CREDENTIALS → OAuth Client ID** again
6. Application type: **Desktop application**
7. Name it: `youtube-shorts-bot-desktop`
8. Click **CREATE**
9. Click **DOWNLOAD** (saves `client_secret.json`)

## Step 4: Get Your Refresh Token

On your own computer (terminal/PowerShell):

```bash
# 1. Navigate to this bot folder
cd daily_shorts_bot

# 2. Install helper (one-time)
pip install google-auth-oauthlib

# 3. Put the client_secret.json you just downloaded in this folder

# 4. Run the token getter
python get_refresh_token.py
```

A browser window will open. Log in with the Google account that owns your YouTube channel. Click **Allow** when asked for permission.

After you allow it, the script will print three values:

```
YOUTUBE_CLIENT_ID: 1234567890-abc...xyz.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET: GOCSPX-abc...xyz
YOUTUBE_REFRESH_TOKEN: 1//0abc...xyz
```

**Keep these three values somewhere safe** — you'll paste them into GitHub in the next step.

## Step 5: Add Secrets to GitHub

1. Go to your GitHub repo → **Settings** (top right)
2. **Secrets and variables** → **Actions** (left sidebar)
3. Click **New repository secret** and add these THREE:

| Name | Value |
|---|---|
| `YOUTUBE_CLIENT_ID` | Paste from Step 4 |
| `YOUTUBE_CLIENT_SECRET` | Paste from Step 4 |
| `YOUTUBE_REFRESH_TOKEN` | Paste from Step 4 |

(Optional: add `ANTHROPIC_API_KEY` for better poems, or `SPORTS_API_KEY` for more reliable football data.)

## Step 6: Test It

1. Go to your GitHub repo → **Actions** tab
2. Click **Daily YouTube Short** (left sidebar)
3. Click **Run workflow** (blue button, top right)
4. Watch the logs. After ~2 minutes, check your YouTube channel — a new Short should be there.

If it works, you're done. It'll run every day automatically at 12:00 UTC from then on.

---

**Troubleshooting:**
- **"Invalid Client"**: Make sure the three secrets match exactly (copy-paste, no extra spaces)
- **"Upload failed"**: Check that your YouTube channel's Google account is the same one you logged in with in Step 4
- **No video appears**: Wait 2–3 minutes; YouTube sometimes takes time to process new Shorts

---

That's it. Once you do this once, the bot runs itself every day forever (or until you pause the GitHub Actions workflow).
