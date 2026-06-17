"""
get_refresh_token.py
RUN THIS ONCE, LOCALLY ON YOUR OWN COMPUTER (not in GitHub Actions).
It opens a browser, asks you to log in to the Google account that owns your
YouTube channel, and prints a refresh token you'll paste into your GitHub
repo secrets as YOUTUBE_REFRESH_TOKEN.

Prerequisites:
  1. In Google Cloud Console, create a project, enable the "YouTube Data API v3".
  2. Create an OAuth Client ID (type: Desktop app) and download the JSON as
     client_secret.json in this same folder.
  3. pip install google-auth-oauthlib
"""

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
credentials = flow.run_local_server(port=0)

print("\n--- Save these as GitHub repo secrets ---")
print("YOUTUBE_CLIENT_ID:", credentials.client_id)
print("YOUTUBE_CLIENT_SECRET:", credentials.client_secret)
print("YOUTUBE_REFRESH_TOKEN:", credentials.refresh_token)
