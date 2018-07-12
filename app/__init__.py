from flask import Flask
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension

from logging.config import dictConfig

from app.config import LOGGER_DICT

dictConfig(LOGGER_DICT)

app = Flask(__name__)
app.config.from_pyfile('config.py')

dtb = DebugToolbarExtension(app)
babel = Babel(app)
