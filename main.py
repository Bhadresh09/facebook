# app.py
from flask import Flask, render_template, request, send_file
import os
import yt_dlp

app = Flask(__name__)

DOWNLOADS_FOLDER = "downloads"

if not os.path.exists(DOWNLOADS_FOLDER):
    os.makedirs(DOWNLOADS_FOLDER)


def download_video(url, platform):
    ydl_opts = {
        'outtmpl': f'{DOWNLOADS_FOLDER}/%(title)s.%(ext)s',
        'format': 'best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    platform = request.form.get('platform')

    try:
        filename = download_video(url, platform)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error downloading video: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
