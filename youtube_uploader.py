"""
youtube_uploader.py
Uploads a finished video to your YouTube channel as a Short, using OAuth
credentials. Expects three environment variables / secrets to already exist
(see get_refresh_token.py for how to obtain the refresh token one time):

  YOUTUBE_CLIENT_ID
  YOUTUBE_CLIENT_SECRET
  YOUTUBE_REFRESH_TOKEN
"""

import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _get_credentials() -> Credentials:
    client_id = os.environ["YOUTUBE_CLIENT_ID"]
    client_secret = os.environ["YOUTUBE_CLIENT_SECRET"]
    refresh_token = os.environ["YOUTUBE_REFRESH_TOKEN"]

    return Credentials(
        token=None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )


def upload_short(video_path: str, title: str, description: str, tags=None) -> str:
    """
    Uploads the video and returns the resulting YouTube video ID.
    """
    creds = _get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags or [],
            "categoryId": "24",  # Entertainment
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": True,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[youtube_uploader] Upload progress: {int(status.progress() * 100)}%")

    video_id = response["id"]
    print(f"[youtube_uploader] Uploaded: https://youtube.com/shorts/{video_id}")
    return video_id


if __name__ == "__main__":
    # quick manual test -- requires a real video file and real env vars set
    upload_short("test_short.mp4", "Test Upload #Shorts", "Automated test upload.", ["test"])
