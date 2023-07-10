import enum
from pathlib import Path

import yaml


def get_project_root() -> Path:
    return Path(__file__).parent.parent


PROJECT_ROOT = get_project_root()
CONFIG_DIR = PROJECT_ROOT / 'config'
MESSAGE_DIR = PROJECT_ROOT / 'messages'
TESTS_FOLDER = PROJECT_ROOT / 'src/tests'

with open(CONFIG_DIR / 'prod.yaml') as config_file:
    config = yaml.safe_load(config_file)

with open(MESSAGE_DIR / 'messages_eng.yaml') as message_file:
    messages = yaml.safe_load(message_file)

BUCKET_NAME = config['bucket']
TEST_BUCKET = config['test_bucket']
RECOGNITION_MODEL = config['recognition_model']
INDEXES = config['index_folder']

LOG_DIR = PROJECT_ROOT / config['log_dir']


class BotActions(enum.Enum):
    """
    Enum representing actions available in the bot through interactive menu
    """
    LIST_ALBUMS = messages['list_albums']
    LOAD_ALBUM = messages['load_new_album']
