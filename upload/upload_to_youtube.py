import os
import json
import random
import pickle
from datetime import datetime

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

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
            scopes=SCOPES,
        )
        creds = flow.run_console()
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def load_metadata():
    with open("metadata.json", "r") as f:
        return json.load(f)

def load_uploaded_log():
    if os.path.exists("uploaded_log.json"):
        with open("uploaded_log.json", "r") as f:
            return json.load(f)
    return []

def save_uploaded_log(log):
    with open("uploaded_log.json", "w") as f:
        json.dump(log, f, indent=2)

def choose_unuploaded_video(metadata, uploaded_log):
    unuploaded = [item for item in metadata if item["filename"] not in uploaded_log]
    return random.choice(unuploaded) if unuploaded else None

def upload_video(youtube, video_data):
    video_file = os.path.join("video", video_data["filename"])
    request_body = {
        "snippet": {
            "categoryId": "22",
            "title": video_data["title"],
            "description": video_data["description"],
            "tags": video_data["tags"]
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

    print(f"📤 Uploading: {video_data['filename']} — {video_data['title']}")
    response = request.execute()
    print(f"✅ Uploaded successfully: https://youtu.be/{response['id']}")

if __name__ == "__main__":
    youtube = get_authenticated_service()
    metadata = load_metadata()
    uploaded_log = load_uploaded_log()

    video_to_upload = choose_unuploaded_video(metadata, uploaded_log)

    if video_to_upload:
        try:
            upload_video(youtube, video_to_upload)
            uploaded_log.append(video_to_upload["filename"])
            save_uploaded_log(uploaded_log)
        except HttpError as e:
            print(f"❌ Upload failed: {e}")
    else:
        print("🚫 No unuploaded videos left.")
