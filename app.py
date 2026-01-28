from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/prepare", methods=["POST"])
def prepare():
    url = request.form["url"]
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "outtmpl": filepath,
        "format": "mp4",
        "quiet": True
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return f"/download/{filename}"

@app.route("/download/<filename>")
def download(filename):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
