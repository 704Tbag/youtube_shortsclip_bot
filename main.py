"""
main.py
Daily orchestrator: generate content -> narrate -> build video -> upload to YouTube.
This is the single entry point that GitHub Actions runs every day.
"""

from content_generator import get_today_content
from tts_generator import generate_narration
from video_builder import build_video
from youtube_uploader import upload_short


def run():
    print("[main] Generating today's content...")
    content = get_today_content()
    print(f"[main] Type: {content['type']} | Title: {content['title']}")
    print(f"[main] Script:\n{content['script']}")

    print("[main] Generating narration audio...")
    narration_path = generate_narration(content["script"], "narration.mp3")

    print("[main] Building video...")
    video_path = build_video(content["script"], narration_path, content["type"], "short.mp4")

    description = (
        f"{content['script']}\n\n"
        "Daily automated short. #Shorts"
        + (" #Poetry" if content["type"] == "poem" else " #Football")
    )
    tags = ["shorts", "poetry" if content["type"] == "poem" else "football"]

    print("[main] Uploading to YouTube...")
    video_id = upload_short(video_path, content["title"], description, tags)
    print(f"[main] Done. https://youtube.com/shorts/{video_id}")


if __name__ == "__main__":
    run()
