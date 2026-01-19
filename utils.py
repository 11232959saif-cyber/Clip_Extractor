import logging
import platform
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Device detection
def is_windows():
    return platform.system() == 'Windows'

def is_linux():
    return platform.system() == 'Linux'

def is_mac():
    return platform.system() == 'Darwin'

# File management
def create_file(filepath):
    with open(filepath, 'w') as f:
        logging.info(f'Created file: {filepath}')

def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        logging.info(f'Deleted file: {filepath}')
    else:
        logging.warning(f'File not found: {filepath}')