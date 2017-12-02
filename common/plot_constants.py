import os
from backend.util.config import EXPERIMENT_NAME
DATA_PATH = r'.\data'
ROOT_PATH = os.path.join(r'.\data', EXPERIMENT_NAME)

USER_PATH = os.path.join(ROOT_PATH, 'user')
SCORE_PATH = os.path.join(ROOT_PATH, 'score')
TIME_PATH = os.path.join(ROOT_PATH, 'time')
COPY_PATH = os.path.join(ROOT_PATH, 'copy')
INSERT_PATH = os.path.join(ROOT_PATH, 'insert')
DEBUG_PATH = os.path.join(ROOT_PATH, 'debug')
BUILD_PATH = os.path.join(ROOT_PATH, 'build')
OTHER_PATH = os.path.join(ROOT_PATH, 'other')
