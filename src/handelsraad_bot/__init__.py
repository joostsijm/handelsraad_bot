"""
Handelsraad bot

Telegram bot for the handelsraad
"""

import os
import logging

import pathlib2
from appdirs import user_data_dir
from dotenv import load_dotenv
import telegram
from telegram.ext import Updater


load_dotenv()

DATA_DIR = user_data_dir('rival_regions_wrapper', 'bergc')
pathlib2.Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

# get logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
TELEGRAM_LOGGER = logging.getLogger('telegram')
TELEGRAM_LOGGER.setLevel(logging.INFO)

# create file handler
FILE_HANDLER = logging.FileHandler('{}/output.log'.format(DATA_DIR))
FILE_HANDLER.setLevel(logging.DEBUG)

# create console handler
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)

# create formatter and add it to the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
STREAM_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setFormatter(FORMATTER)

# add the handlers to logger
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
TELEGRAM_LOGGER.addHandler(STREAM_HANDLER)
TELEGRAM_LOGGER.addHandler(FILE_HANDLER)

TELEGRAM_KEY = os.environ['TELEGRAM_KEY']
TELEGRAM_BOT = telegram.Bot(token=TELEGRAM_KEY)
TELEGRAM_UPDATER = Updater(TELEGRAM_KEY, use_context=True)

TELEGRAM_GROUP = int(os.environ['TELEGRAM_GROUP'])
