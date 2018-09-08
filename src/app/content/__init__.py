from flask import Blueprint

bp = Blueprint('content', __name__)

from .routes import *
