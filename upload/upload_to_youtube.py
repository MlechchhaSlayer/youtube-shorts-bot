import os
import pickle
import google.auth
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "client_secrets.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

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

    media_file = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    print("📤 Uploading video...")
    response = request.execute()
    print(f"✅ Uploaded successfully: https://youtu.be/{response['id']}")

if __name__ == "__main__":
    title = "🔥 Daily Motivation: Never Give Up!"
    description = "This motivational short will kickstart your day. 💪\n#motivation #shorts"
    tags = ["motivation", "shorts", "inspiration"]

    upload_video("video/video_1.mp4", title, description, tags)
