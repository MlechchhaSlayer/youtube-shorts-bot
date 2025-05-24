import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    else:
        # Create credentials using client_id and client_secret directly
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                }
            },
            scopes=SCOPES
        )
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

    media_file = MediaFileUpload(video_file, chunksize=256 * 1024, resumable=True)

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
