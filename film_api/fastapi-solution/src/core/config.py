import os
from logging import config as logging_config

from core.logger import LOGGING
from dotenv import load_dotenv

logging_config.dictConfig(LOGGING)
load_dotenv()

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6380))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'elasticsearch')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9201))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.environ.get('DEBUG', False) == 'True'
