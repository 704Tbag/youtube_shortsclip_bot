"""
video_builder.py
Builds a simple, original animated vertical (1080x1920) video for YouTube Shorts:
  - A gradient background (color scheme depends on content type)
  - The script text fading in line-by-line, timed to the narration length
  - The narration audio
  - A quiet, generated (royalty-free, not sampled from anywhere) background tone bed

No external video/image assets are used, so there are no copyright concerns
with the visuals or the background audio.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip, AudioArrayClip

WIDTH, HEIGHT = 1080, 1920
FPS = 24

COLOR_SCHEMES = {
    "poem": {"top": (30, 20, 60), "bottom": (90, 40, 120)},
    "football": {"top": (10, 50, 30), "bottom": (20, 110, 60)},
}


def _make_gradient(top_color, bottom_color):
    base = Image.new("RGB", (WIDTH, HEIGHT), top_color)
    top = np.array(top_color, dtype=float)
    bottom = np.array(bottom_color, dtype=float)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = tuple((top * (1 - ratio) + bottom * ratio).astype(int))
        ImageDraw.Draw(base).line([(0, y), (WIDTH, y)], fill=color)
    return base


def _wrap_text(text, font, draw, max_width):
    words = text.split()
    lines, current = [], ""
    for w in words:
        trial = (current + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def _frame_with_text(background, lines, visible_count, font):
    img = background.copy()
    draw = ImageDraw.Draw(img)
    line_height = 80
    total_height = line_height * len(lines)
    start_y = (HEIGHT - total_height) // 2

    for i, line in enumerate(lines):
        if i >= visible_count:
            break
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (WIDTH - line_width) // 2
        y = start_y + i * line_height
        draw.text((x + 3, y + 3), line, font=font, fill=(0, 0, 0))  # soft shadow
        draw.text((x, y), line, font=font, fill=(255, 255, 255))
    return img


def _generate_tone_bed(duration_sec, sample_rate=44100):
    """Generates a soft, low-volume ambient pad -- entirely synthesized, no samples."""
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    freqs = [110, 165, 220]  # simple harmonic chord
    wave = sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
    fade_len = int(sample_rate * 0.5)
    envelope = np.ones_like(wave)
    envelope[:fade_len] = np.linspace(0, 1, fade_len)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    wave = wave * envelope * 0.08  # keep it quiet, sits under narration
    stereo = np.column_stack([wave, wave])
    return stereo, sample_rate


def build_video(script_text: str, narration_path: str, content_type: str, output_path: str = "short.mp4") -> str:
    narration = AudioFileClip(narration_path)
    duration = narration.duration + 1.0  # small tail at the end

    scheme = COLOR_SCHEMES.get(content_type, COLOR_SCHEMES["poem"])
    background = _make_gradient(scheme["top"], scheme["bottom"])

    font = ImageFont.load_default(size=58)
    draw_helper = ImageDraw.Draw(background)
    raw_lines = script_text.split("\n") if "\n" in script_text else [script_text]
    lines = []
    for raw in raw_lines:
        lines.extend(_wrap_text(raw, font, draw_helper, WIDTH - 120))

    total_frames = int(duration * FPS)
    frames = []
    for f_idx in range(total_frames):
        t = f_idx / FPS
        progress = min(t / max(duration - 1.0, 0.1), 1.0)
        visible_count = max(1, int(progress * len(lines)) + 1)
        frame_img = _frame_with_text(background, lines, visible_count, font)
        frames.append(np.array(frame_img))

    video_clip = ImageSequenceClip(frames, fps=FPS)

    tone_array, sample_rate = _generate_tone_bed(duration)
    tone_clip = AudioArrayClip(tone_array, fps=sample_rate)
    final_audio = CompositeAudioClip([tone_clip, narration.set_start(0)])

    final_clip = video_clip.set_audio(final_audio).set_duration(duration)
    final_clip.write_videofile(output_path, fps=FPS, codec="libx264", audio_codec="aac", verbose=False, logger=None)
    return output_path


if __name__ == "__main__":
    from tts_generator import generate_narration

    sample_script = "Think of the first light of morning,\nhow it asks for nothing, yet gives so much,\nand for a moment, the noise in me goes still."
    narration_file = generate_narration(sample_script, "test_narration.mp3")
    build_video(sample_script, narration_file, "poem", "test_short.mp4")
    print("Saved test_short.mp4")
