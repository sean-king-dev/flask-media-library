import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

            # Return the compressed file path or an identifier
            return jsonify({
                'message': 'File uploaded and processed successfully',
                'compressed_file_path': compressed_video_path,
            })

        else:
            return jsonify({'error': 'Invalid file type or no file selected'}), 400

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)