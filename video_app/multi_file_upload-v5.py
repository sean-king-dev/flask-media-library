import os
import subprocess
from flask import Flask, flash, request, redirect, render_template, send_from_directory, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

path = os.getcwd()

ffmpeg_path = '/usr/bin/ffmpeg'

UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'mp4'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_video(input_path):
    output_path = os.path.splitext(input_path)[0] + '_compressed.mp4'
    subprocess.run([
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libx265',
        '-crf', '28',
        output_path
    ])
    return output_path

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        video_file = request.files.get('videoFile')

        if video_file and allowed_file(video_file.filename):
            filename = secure_filename(video_file.filename)
            video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video_file.save(video_file_path)

            compressed_video_path = compress_video(video_file_path)
            file_url = url_for('uploaded_file', filename=compressed_video_path)
            flash('Video successfully uploaded and compressed')
            return render_template('upload.html', title='Copy Video URL:', file_url=file_url, file_type='video')

        else:
            flash('Invalid file type or no file selected')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
