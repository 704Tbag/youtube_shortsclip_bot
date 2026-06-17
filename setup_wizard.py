#!/usr/bin/env python3
"""
setup_wizard.py
Interactive guide to walk through the setup process step by step.
Run this after cloning the repo to your computer.
"""

import os
import sys

def print_header(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def print_step(step_num, description):
    print(f"\n✓ STEP {step_num}: {description}")
    print("-" * 70)

def input_with_validation(prompt, validator=None):
    while True:
        response = input(prompt).strip()
        if validator and not validator(response):
            print("  ✗ Invalid. Try again.")
            continue
        return response

def main():
    print_header("YOUTUBE SHORTS BOT — SETUP WIZARD")
    
    print("""
This wizard will guide you through a one-time 5-minute setup to connect your
YouTube channel to the daily shorts bot.

You'll need:
  • Your YouTube channel's Google account
  • A web browser
  • This computer
    """)
    
    input("Press ENTER to start...")
    
    # Step 1
    print_step(1, "Create a Google Cloud Project")
    print("""
Next, you'll create a free Google Cloud project. This takes ~2 minutes:

1. Open https://console.cloud.google.com/ in your browser
2. At the top, click "Select a Project" → "NEW PROJECT"
3. Name it: youtube-shorts-bot
4. Click CREATE
5. Wait ~30 seconds for setup to finish
6. Come back here and press ENTER
    """)
    input("Press ENTER once you've created the project...")
    
    # Step 2
    print_step(2, "Enable YouTube Data API v3")
    print("""
Now enable the API your bot will use:

1. In the same Cloud Console, click "APIs & Services" (left sidebar)
2. Click "+ ENABLE APIS AND SERVICES" (top center)
3. Search for: YouTube Data API v3
4. Click the result
5. Click ENABLE
6. Wait ~10 seconds
7. Come back here and press ENTER
    """)
    input("Press ENTER once you've enabled the API...")
    
    # Step 3
    print_step(3, "Create OAuth Credentials")
    print("""
Now create the credentials your bot will use to upload videos:

1. In Cloud Console, click "Credentials" (left sidebar)
2. Click "+ CREATE CREDENTIALS" (top left)
3. Choose "OAuth Client ID"
4. If prompted for "Consent Screen":
   - Pick "External"
   - Fill in:
     - App name: YouTube Shorts Bot
     - User support email: (your email)
     - Developer contact: (your email)
   - Click SAVE AND CONTINUE twice (skip optional scopes)
   - Click BACK TO CREDENTIALS
5. Now click "+ CREATE CREDENTIALS" → "OAuth Client ID" again
6. Application type: "Desktop application"
7. Name: youtube-shorts-bot-desktop
8. Click CREATE
9. Click DOWNLOAD (saves client_secret.json to your Downloads folder)
10. Come back here and press ENTER
    """)
    input("Press ENTER once you've downloaded client_secret.json...")
    
    # Step 4
    print_step(4, "Get Your Refresh Token")
    print("""
You're about to run a script that will ask you to log in to your YouTube account
in your browser. This is safe — you're granting permission to YOUR OWN bot.

Instructions:
1. Paste client_secret.json into this folder (daily_shorts_bot/)
2. In this terminal, run:
   
   pip install google-auth-oauthlib
   python get_refresh_token.py

3. A browser window will open asking you to log in
4. Log in with your YouTube channel's Google account
5. Click ALLOW when asked for permission
6. Copy the three printed values (CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
   and paste them somewhere safe (a text file, Notes app, etc.)
7. Come back here and press ENTER
    """)
    input("Press ENTER once you've run get_refresh_token.py and saved the values...")
    
    # Step 5
    print_step(5, "Push to GitHub")
    print("""
Create a GitHub repository and push this code:

1. Go to https://github.com/new
2. Name it: youtube-shorts-bot
3. Choose Public or Private (doesn't matter)
4. Click CREATE REPOSITORY
5. Follow the instructions to push your local code (you'll see git commands)
   
   Or, if you're not familiar with git, you can:
   - Click "uploading an existing file"
   - Select all files from this folder
   - Commit them
   
6. Come back here and press ENTER
    """)
    input("Press ENTER once you've pushed to GitHub...")
    
    # Step 6
    print_step(6, "Add Secrets to GitHub")
    print("""
Now add your credentials as GitHub secrets (they'll be hidden):

1. Go to your new GitHub repo
2. Click Settings (top right)
3. Click Secrets and variables → Actions (left sidebar)
4. Click "New repository secret"
5. Add these THREE (copy-paste the values from Step 4):
   
   Name: YOUTUBE_CLIENT_ID
   Value: (paste the CLIENT_ID from Step 4)
   
   Name: YOUTUBE_CLIENT_SECRET
   Value: (paste the CLIENT_SECRET from Step 4)
   
   Name: YOUTUBE_REFRESH_TOKEN
   Value: (paste the REFRESH_TOKEN from Step 4)

6. Come back here and press ENTER
    """)
    input("Press ENTER once you've added all three secrets...")
    
    # Step 7
    print_step(7, "Test the Bot")
    print("""
Time for the first test:

1. Go to your GitHub repo
2. Click the Actions tab (top)
3. Click "Daily YouTube Short" (left sidebar)
4. Click "Run workflow" (blue button, top right)
5. Wait 1-2 minutes for it to finish
6. Go to your YouTube channel — a new Short should be there!
   (Check your Shorts feed or the "Uploads" playlist)

If you see a video, you're done! It will run every day automatically at 12:00 UTC.

If something fails:
  - Click on the failed job to see error logs
  - Check OAUTH_SETUP.md in the repo for troubleshooting
  - Most common issue: secrets not copied exactly (no extra spaces)
    """)
    input("Press ENTER to finish...")
    
    print_header("SETUP COMPLETE!")
    print("""
Your YouTube Shorts bot is now live. It will:
  • Generate a poem OR football summary daily (alternates)
  • Narrate it with AI voice
  • Create an animated video
  • Upload to your YouTube channel automatically

Every day at 12:00 UTC.

You can adjust the upload time by editing:
  .github/workflows/daily_short.yml
  (Change the cron line)

Enjoy your automated content!
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)
