import os
from flask.helpers import safe_join, send_file, send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from . import FILES_DIRECTORY, ALLOWED_EXTENSIONS, MAX_SIZE_FILE, filenames


def get_path(file: str):
    file_extension = file.split('.')[-1]
    path = safe_join(safe_join(FILES_DIRECTORY, f'{file_extension}/'), file)
    return path


def files_list():
    files = []
    for _, _, filename in os.walk(FILES_DIRECTORY):
        files.extend(filename)
    return files


def files_extension_list(file_extension: str):
    if filenames.count(file_extension) != 0:
        path = safe_join(FILES_DIRECTORY, file_extension)
        files = os.listdir(path)
        return files
    else:
        return {"message": "Formato inexistente no sistema."}       


def download_file(filename):
    try:
        path = get_path(filename)
        return send_file(path, as_attachment=True), 200
    except NameError:
        return {"message": "Arquivo não encontrado"}, 404


def download_zip(extension: str, compression: int):
    path = f'{FILES_DIRECTORY}{extension}'
    list_files_of_extension = os.listdir(path)
    
    if len(list_files_of_extension) == 0:
        return {"message": "Não há arquivos desse formato para download"}, 404
    else:
        os.system(f'zip /tmp/{extension}-files-zip {path} -{compression}')
    return send_file(f'/tmp/{extension}-files-zip.zip', as_attachment=True), 200


def save_file(file: FileStorage):
    extension = file.filename.split('.')[-1]
    file.save(f'/tmp/{file.filename}')
    file_size = os.stat(f'/tmp/{file.filename}').st_size

    if not extension in ALLOWED_EXTENSIONS:
        return {"message": "Formato de arquivo não suportado"}, 415
    
    if file_size > MAX_SIZE_FILE:
        return {"message": "Tamanho de arquivo não passado"}, 403
    
    for _, _, filename in os.walk(f'{FILES_DIRECTORY}/{extension}'):
        if file.filename == filename: 
            return {"message": "Arquivo já existe no banco"}, 409

    filename = secure_filename(file.filename) 
    path = get_path(file.filename)
    file.save(path)

    return filename