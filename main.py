import time
import os

from script.generate_script import generate_script
from tts.generate_tts import generate_tts
from video.fetch_bg import fetch_background
from video.combine import create_final_video
from upload.upload_to_youtube import upload_video

# 🔧 Utility functions for metadata
def generate_title(text: str) -> str:
    words = text.split()
    title = " ".join(words[:8])
    return f"🔥 {title}... #Shorts"

def generate_description(text: str) -> str:
    return f"{text}\n\nStart your day with motivation! 💪\n#motivation #success #inspiration #shorts"

def generate_tags(text: str) -> list:
    return ["motivation", "success", "shorts", "inspiration", "dailyquotes"]

# 🕒 Create timestamped filenames for uniqueness
timestamp = time.strftime("%Y%m%d_%H%M%S")
video_path = f"video/video_{timestamp}.mp4"
audio_path = f"audio/audio_{timestamp}.mp3"
bg_path = f"video/bg_{timestamp}.mp4"

# 🧠 Step 1: Generate motivational script
text = generate_script()

# 🗣️ Step 2: Convert text to speech
generate_tts(text, audio_path)

# 🎥 Step 3: Fetch a background video
fetch_background(bg_path)

# 🧩 Step 4: Combine TTS and background into final video
create_final_video(
    text=text,
    background_path=bg_path,
    audio_path=audio_path,
    output_path=video_path
)

# 🚀 Step 5: Upload the video to YouTube
upload_video(
    video_file=video_path,
    title=generate_title(text),
    description=generate_description(text),
    tags=generate_tags(text)
)

# 🧹 Step 6: Clean up local files to save space
os.remove(video_path)
os.remove(audio_path)
os.remove(bg_path)
