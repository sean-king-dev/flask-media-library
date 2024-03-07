import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory, url_for
from flask_humanize import Humanize

from werkzeug.utils import secure_filename

app = Flask(__name__)
humanize = Humanize(app)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

path = os.getcwd()

ffmpeg_path = '/usr/bin/ffmpeg'

UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'mp4', 'mov', 'avi'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_video(input_path, compression_percentage):
    output_path = os.path.splitext(input_path)[0] + f'_compressed_{compression_percentage}percent.mp4'
    os.system(f'{ffmpeg_path} -i {input_path} -c:v libx264 -crf {compression_percentage} {output_path}')
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
        compression_percentage = int(request.form.get('compressionPercentage', 50))

        if video_file and allowed_file(video_file.filename):
            filename = secure_filename(video_file.filename)
            video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video_file.save(video_file_path)

            compressed_video_path = compress_video(video_file_path, compression_percentage)
            
            
            file_url = url_for('uploaded_file', filename=os.path.basename(compressed_video_path))
            
            
            original_size = os.path.getsize(video_file_path)
            compressed_size = os.path.getsize(compressed_video_path)
            popup_message = f'Video successfully uploaded and compressed at {compression_percentage}%. ' \
                            f'Original size: {original_size} bytes, Compressed size: {compressed_size} bytes'
            
            return render_template('upload.html', title='Video:', file_url=file_url, file_type='video',
                                   original_size=original_size, compressed_size=compressed_size, popup_message=popup_message)

        else:
            flash('Invalid file type or no file selected')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
