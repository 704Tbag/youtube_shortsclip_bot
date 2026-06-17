"""
tts_generator.py
Converts script text to a spoken narration audio file (mp3) using gTTS.
gTTS is free and requires no API key, which keeps this pipeline runnable
with zero ongoing cost. For noticeably better voice quality, swap this
module out for ElevenLabs or Google Cloud Text-to-Speech later -- the
function signature below (text -> output mp3 path) is all main.py expects.
"""

from gtts import gTTS


def generate_narration(text: str, output_path: str = "narration.mp3") -> str:
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(output_path)
    return output_path


if __name__ == "__main__":
    generate_narration("This is a test of the narration system.", "test_narration.mp3")
    print("Saved test_narration.mp3")
