import os
import subprocess
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


path = os.getcwd()

UPLOAD_FOLDER = os.path.join(path, 'uploads')


if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'avi', 'mkv', 'mov'])


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                
                file.save(filepath)

                
                if allowed_file(filename, ALLOWED_IMAGE_EXTENSIONS):
                    
                    compress_image(filepath)
                elif allowed_file(filename, ALLOWED_VIDEO_EXTENSIONS):
                    
                    compress_video(filepath)

        flash('File(s) successfully uploaded')
        return redirect('/')


def compress_image(filepath):
    
    image = Image.open(filepath)

    
    image.save(filepath, quality=85)


def compress_video(filepath):
    
    output_filepath = os.path.splitext(filepath)[0] + '_compressed.mp4'

    
    subprocess.run([
        'ffmpeg',
        '-i', filepath,             
        '-c:v', 'libx265',          
        '-preset', 'medium',        
        '-crf', '28',               
        '-c:a', 'aac',              
        '-strict', 'experimental',  
        output_filepath
    ], check=True)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
