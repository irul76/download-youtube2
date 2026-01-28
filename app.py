from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download")
def download():
    url = request.args.get("url")
    filename = "video.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "outtmpl": filepath,
        "format": "mp4",
        "quiet": True
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
