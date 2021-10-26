from flask import Flask, jsonify, request
from .kenzie import image

app = Flask(__name__)

@app.get('/files')
def list_files():
    files = image.files_list()
    return files
    
@app.get('/files/<extension>')
def list_files_by_extension(extension):
    files_by_extension = image.files_extension_list(extension)
    return files_by_extension

@app.get('/download/<filename>')
def download_file(filename):
    return image.download_file(filename)

@app.get('/download-zip')
def download_zip():
    extension = str(request.args.get('file_extension'))
    compression = int(request.args.get('compression_ratio'))
    return image.download_files_zip(extension, compression)

@app.post('/upload')
def upload_file():
    return image.save_file()
