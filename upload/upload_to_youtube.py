import os
import pickle
import random
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                }
            },
            SCOPES
        )
        creds = flow.run_console()
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def upload_video(video_file, title, description, tags):
    youtube = get_authenticated_service()

    request_body = {
        "snippet": {
            "categoryId": "22",  # People & Blogs
            "title": title,
            "description": description,
            "tags": tags
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media_file = MediaFileUpload(video_file, chunksize=256 * 1024, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    print("📤 Uploading video...")
    response = request.execute()
    video_id = response["id"]
    print(f"✅ Uploaded: https://youtu.be/{video_id}")

    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} - Uploaded {video_file} as {title} - https://youtu.be/{video_id}\n")

if __name__ == "__main__":
    videos = [f for f in os.listdir("video") if f.endswith(".mp4")]
    if not videos:
        print("❌ No videos found in the 'video' folder.")
        exit(1)

    chosen_video = random.choice(videos)
    title = "🔥 Daily Motivation"
    description = "Stay inspired! 💪\n#motivation #shorts"
    tags = ["motivation", "shorts", "inspiration"]

    upload_video(os.path.join("video", chosen_video), title, description, tags)
