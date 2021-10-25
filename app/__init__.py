from flask import Flask, jsonify, request
from .kenzie import image

app = Flask(__name__)

@app.get('/files')
def list_files():
    files = image.files_list()
    extension = request.args.get('extension')
    if extension is None:
        return jsonify(files), 200
    else:
        files_by_extension = image.files_extension_list(extension)
        return jsonify(files_by_extension), 200


@app.get('/download/<string:filename>')
def download_file(filename: str):
    return download_file

@app.get('/download-zip')
def download_zip():
    extension = str(request.args.get('file_extension'))
    compression = int(request.args.get('compression_ratio'))
    return image.download_zip(extension, compression)

@app.post('/upload')
def upload_file():
    files = []
    for file in request.files:     
        filename = image.save_file(request.files[file])
        files.append(filename)    
        return jsonify(files), 201
