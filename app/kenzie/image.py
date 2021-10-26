import os
from flask.helpers import safe_join, send_file
from flask import jsonify, request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from . import FILES_DIRECTORY, ALLOWED_EXTENSIONS, MAX_SIZE_FILE


def get_path(file: str):
    file_extension = file.split('.')[-1]
    path = safe_join(safe_join(FILES_DIRECTORY, f'{file_extension}/'), file)
    return path


def files_list():
    files = []
    for _, _, filename in os.walk(FILES_DIRECTORY):
        files.extend(filename)
    return jsonify(files), 200


def files_extension_list(file_extension: str):
    filenames = []
    for _, _, filename in os.walk(safe_join(FILES_DIRECTORY, file_extension)):
        filenames.extend(filename)
    print(filenames)
    if len(filenames) != 0:
        path = safe_join(FILES_DIRECTORY, file_extension)
        files = os.listdir(path)
        return jsonify(files), 200
    else:
        return {"message": "Não há arquivos nesse formato."}, 404       


def download_file(filename: str):
    extension = filename.split('.')[-1]
    path = safe_join(FILES_DIRECTORY, extension)
    
    try:
        return send_file(f'{path}/{filename}', as_attachment=True), 200
    except:
        return {"message": "Arquivo não encontrado"}, 404        


def download_files_zip(extension: str, compression: int):
    path = f'{FILES_DIRECTORY}{extension}'
    list_files_of_extension = os.listdir(path)
    
    if len(list_files_of_extension) == 0:
        return {"message": "Não há arquivos desse formato para download"}, 404
    else:
        os.system(f'zip /tmp/{extension}-files-zip {path} -{compression}')
    return send_file(f'/tmp/{extension}-files-zip.zip', as_attachment=True), 200


def save_file():
    files = []
    for file in request.files:
        extension = request.files[file].filename.split('.')[-1]
        request.files[file].save(f'/tmp/{request.files[file].filename}')
        file_size = os.stat(f'/tmp/{request.files[file].filename}').st_size
        request.files[file].filename = secure_filename(request.files[file].filename)

        if not extension in ALLOWED_EXTENSIONS:
            return {"message": "Formato de arquivo não suportado"}, 415

        if file_size > MAX_SIZE_FILE:
            return {"message": "Tamanho de arquivo não suportado"}, 403

        for filename in os.listdir(f'{FILES_DIRECTORY}/{extension}'):
            if request.files[file].filename == filename: 
                return {"message": "Arquivo já existe no banco"}, 409
        
        path = get_path(request.files[file].filename)
        request.files[file].save(path)
        files.append(request.files[file].filename)
        
    return jsonify(files), 201
