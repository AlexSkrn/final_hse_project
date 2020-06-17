import logging
import os
import sys


FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d — %(message)s")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_logger(*, logger_name):
    """Get logger with prepared handlers."""

    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    logger.addHandler(get_console_handler())
    logger.propagate = False

    return logger


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret').encode()
    SERVER_PORT = 5000
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///clustered_data.db'
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024


class ProductionConfig(Config):
    DEBUG = False
    SERVER_ADDRESS: os.environ.get('SERVER_ADDRESS', '0.0.0.0')
    SERVER_PORT: os.environ.get('SERVER_PORT', '5000')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
