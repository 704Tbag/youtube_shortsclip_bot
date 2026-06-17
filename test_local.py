"""
test_local.py
Run this locally to test the entire pipeline WITHOUT needing YouTube credentials.
Generates content -> narration -> video, saves to disk, no upload.
Useful for verifying everything works before pushing to GitHub.

Usage: python test_local.py
"""

import os
import sys

# Add current dir to path so imports work
sys.path.insert(0, os.path.dirname(__file__))

from content_generator import get_today_content
from tts_generator import generate_narration
from video_builder import build_video


def test_pipeline():
    print("=" * 60)
    print("LOCAL TEST: Content -> TTS -> Video (no YouTube upload)")
    print("=" * 60)

    print("\n[TEST] Step 1: Generate today's content...")
    content = get_today_content()
    print(f"  Type: {content['type']}")
    print(f"  Title: {content['title']}")
    print(f"  Script:\n    {content['script']}\n")

    print("[TEST] Step 2: Generate narration audio...")
    try:
        narration_path = generate_narration(content["script"], "test_narration.mp3")
        print(f"  ✓ Saved: {narration_path}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        print("    (This is OK — gTTS might not be installed yet.)")
        print("    Run: pip install gTTS")
        return False

    print("\n[TEST] Step 3: Build video...")
    try:
        video_path = build_video(
            content["script"],
            narration_path,
            content["type"],
            "test_short.mp4",
        )
        print(f"  ✓ Saved: {video_path}")
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"  ✓ File size: {file_size_mb:.1f} MB")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        print("    (This is OK — moviepy / ffmpeg might not be installed yet.)")
        print("    Run: pip install moviepy && sudo apt-get install ffmpeg")
        return False

    print("\n" + "=" * 60)
    print("✓ LOCAL TEST PASSED")
    print("=" * 60)
    print("\nNext: Follow the OAUTH setup in README.md to get credentials,")
    print("then push to GitHub and test the full upload.")
    return True


if __name__ == "__main__":
    success = test_pipeline()
    sys.exit(0 if success else 1)
