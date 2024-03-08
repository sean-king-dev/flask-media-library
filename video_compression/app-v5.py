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

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'mp4', 'mov', 'avi'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_video(input_path, output_path, scale_percent):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (new_width, new_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (new_width, new_height))
        out.write(resized_frame)

    cap.release()
    out.release()

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
        lossless = bool(request.form.get('lossless', False))
        resize_percentage = int(request.form.get('resizePercentage', 50))  # Add a new form field for resizing

        if video_file and allowed_file(video_file.filename):
            filename = secure_filename(video_file.filename)
            video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video_file.save(video_file_path)

            # Resize the video before compression
            resized_video_path = os.path.join(app.config['UPLOAD_FOLDER'], f'resized_{filename}')
            resize_video(video_file_path, resized_video_path, resize_percentage)

            # Compress the resized video
            compressed_video_path = compress_video(resized_video_path, compression_percentage, lossless)
            
            if compressed_video_path:
                file_url = url_for('uploaded_file', filename=os.path.basename(compressed_video_path))
                original_size = os.path.getsize(video_file_path)
                compressed_size = os.path.getsize(compressed_video_path)
                popup_message = f'Video successfully uploaded, resized, and compressed. ' \
                                f'Original size: {original_size} bytes, Compressed size: {compressed_size} bytes'
                
                return render_template('upload.html', title='Video:', file_url=file_url, file_type='video',
                                       original_size=original_size, compressed_size=compressed_size, popup_message=popup_message)
            else:
                flash('Error during video compression.')
                return redirect(request.url)

        else:
            flash('Invalid file type or no file selected')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
