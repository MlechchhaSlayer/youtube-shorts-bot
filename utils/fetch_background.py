import requests
import os

PEXELS_API_KEY = "QhK2jETaZq09gFDUVobHWVY2Ul0SZlYCClHz6GJ1CoasMViCW7B1BHVc"  # <-- paste your API key here
QUERY = "nature landscape"  # You can change this
VIDEO_DIR = "assets"

def fetch_background_video():
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": QUERY,
        "per_page": 1
    }

    response = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        video_url = data["videos"][0]["video_files"][0]["link"]
        filename = os.path.join(VIDEO_DIR, "background_1.mp4")

        with requests.get(video_url, stream=True) as r:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✅ Downloaded background video to {filename}")
        return filename
    else:
        print("❌ Failed to fetch video:", response.text)
        return None

if __name__ == "__main__":
    fetch_background_video()
