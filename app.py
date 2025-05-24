from flask import Flask, request, jsonify
from upload.upload_to_youtube import upload_video

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube Upload Bot is running!"

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json

    video_file = data.get("video_file")
    title = data.get("title", "Default Title")
    description = data.get("description", "")
    tags = data.get("tags", [])

    if not video_file:
        return jsonify({"error": "Missing 'video_file' parameter"}), 400

    try:
        upload_video(video_file, title, description, tags)
        return jsonify({"status": "Video uploaded successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
