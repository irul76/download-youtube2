from flask import Flask, render_template, request, Response
from yt_dlp import YoutubeDL
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download")
def download():
    url = request.args.get("url")
    format_type = request.args.get("type")  # mp3 / mp4
    quality = request.args.get("quality")

    if format_type == "mp3":
        cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "-o", "-",
            url
        ]
        mimetype = "audio/mpeg"
        filename = "audio.mp3"
    else:
        cmd = [
            "yt-dlp",
            "-f", f"bestvideo[height<={quality}]+bestaudio/best",
            "-o", "-",
            url
        ]
        mimetype = "video/mp4"
        filename = "video.mp4"

    def generate():
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        while True:
            chunk = process.stdout.read(1024)
            if not chunk:
                break
            yield chunk

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }

    return Response(generate(), headers=headers, mimetype=mimetype)

if __name__ == "__main__":
    app.run(debug=False)
