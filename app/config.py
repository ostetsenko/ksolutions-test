import os

APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
DEBUG = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECRET_KEY = 'xv3gavkxc04n3mzx7oksd6q'
CSRF_ENABLED = True
BABEL_TRANSLATION_DIRECTORIES = os.path.join(APPLICATION_DIR, 'translations')
BABEL_DEFAULT_LOCALE = 'ru'
LANGUAGES = {
    'en': 'English',
    'ru': 'Russian'
}

LOGGER_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
        'advanced': {
            'format': '%(asctime)s [%(levelname)s]{%(pathname)s:%(lineno)d}: %(message)s',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'debug_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'filename': os.path.join(APPLICATION_DIR, 'logs', 'debug.log'),
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': os.path.join(APPLICATION_DIR, 'logs', 'info.log'),
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'advanced',
            'filename': os.path.join(APPLICATION_DIR, 'logs', 'error.log'),
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'error_file_handler', 'info_file_handler'],
    }
}
