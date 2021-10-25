import os 
import dotenv
from flask.helpers import safe_join

dotenv.load_dotenv()
FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS')
MAX_SIZE_FILE = os.environ.get('MAX_CONTENT_LENGTH'), 1 * 1024 * 1024

if not os.path.isdir(FILES_DIRECTORY):
    os.mkdir(FILES_DIRECTORY)

filenames = ['png', 'jpg', 'gif']

for filename in filenames:
    if not os.path.isdir(safe_join(FILES_DIRECTORY, filename)):
        os.mkdir(safe_join(FILES_DIRECTORY, filename))
