import subprocess
import os

def create_video_with_text_overlay(
    bg_video_path="assets/background_1.mp4",
    audio_path="audio/voice_1.mp3",
    script_path="scripts/script_1.txt",
    output_path="video/video_1.mp4"
):
    # Read the text
    with open(script_path, "r") as f:
        text = f.read().replace("'", "").replace("\n", " ")

    font_path = "assets/font.ttf"  # Add a TTF font here
    os.makedirs("video", exist_ok=True)

    # Build ffmpeg command
    command = [
        "ffmpeg",
        "-y",  # overwrite
        "-i", bg_video_path,
        "-i", audio_path,
        "-filter_complex",
        f"[0:v]crop=in_h*9/16:in_h,scale=1080:1920,format=yuv420p,drawtext=fontfile={font_path}:text='{text}':fontcolor=white:fontsize=48:borderw=2:x=(w-text_w)/2:y=h-200",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        "-c:v", "libx264",
        "-c:a", "aac",
        output_path
    ]

    print("🎬 Creating video with FFmpeg...")
    subprocess.run(command)
    print(f"✅ Video saved to {output_path}")

if __name__ == "__main__":
    create_video_with_text_overlay()
