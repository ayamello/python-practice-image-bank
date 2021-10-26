import os 
import dotenv
import re
from flask.helpers import safe_join

dotenv.load_dotenv()
FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS')
MAX_SIZE_FILE = int(os.environ.get('MAX_CONTENT_LENGTH'))

if not os.path.isdir(FILES_DIRECTORY):
    os.mkdir(FILES_DIRECTORY)

filenames = list(ALLOWED_EXTENSIONS.split(','))

for filename in filenames:
    filename = re.sub(r'[\W_]+', "", filename)
    if not os.path.isdir(safe_join(FILES_DIRECTORY, filename)):
        os.mkdir(safe_join(FILES_DIRECTORY, filename))
