import os
from flask import Flask, json, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.exceptions import HTTPException
from ..settings import config as conf

app = Flask(__name__, static_folder="content")
app.wsgi_app = ProxyFix(app.wsgi_app)

config = conf[os.environ.get("FLASK_ENV", "default")]
config.init_app(app)
app.config.from_object(config)

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

from .content import bp as content_blueprint

app.register_blueprint(content_blueprint, url_prefix="/api")


@app.errorhandler(Exception)
def __api_error_handler(e):
    """
    Catch any request-triggered exception and
    return a json-friendly response.
    """
    code = 500
    msg = "Internal Server Error"
    if isinstance(e, HTTPException):
        code = e.code
        msg = str(e)
    if app.config["DEBUG"]:
        app.logger.warning({"Error": e, "Context": request.__dict__})
        msg = str(e)
    return jsonify({"Error": msg}), code
