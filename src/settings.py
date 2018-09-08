import os, sys, yaml

BASEDIR = os.path.abspath(os.path.dirname(__file__))

API_VERSION_TABLE = {"stable": "v1", "oldstable": "v1", "dev": "v1"}


class Config:

    SECRETSFILE = os.path.abspath(os.environ.get("FLASK_APPSECRETS", ".secrets.yml"))
    if os.path.exists(SECRETSFILE):
        secrets = None
        with open(SECRETSFILE, "r") as sfile:
            try:
                secrets = yaml.load(sfile, Loader=yaml.SafeLoader)
            except yaml.YAMLError:
                tb = sys.exc_info()[2]
                raise RuntimeError("Failed loading secrets file.").with_traceback(tb)
    else:
        raise FileNotFoundError("could not find secretsfile.")

    try:
        SECRET_KEY = secrets["secret_key"]
    except TypeError:
        tb = sys.exc_info()[2]
        raise RuntimeError("Could not find a secret key in secrets.").with_traceback(tb)

    SQLALCHEMY_DATABASE_URI = "sqlite:////srv/data/db/brickwall.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CONTENTPATH = os.path.abspath("/srv/data/content")
    if not os.path.isdir(CONTENTPATH):
        os.mkdir(CONTENTPATH)
    CONTENT_ROOT = CONTENTPATH.split("/")[-1:]

    APIVERSION = os.environ.get("APIVERSION", "stable").lower()
    if APIVERSION in API_VERSION_TABLE.keys():
        APIPREFIX = "/{}".format(API_VERSION_TABLE[APIVERSION])
    else:
        raise RuntimeError(
            "Invalid api-version. Must be one of stable, oldstable or dev."
        )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SERVER_NAME = "localhost.localdomain"
    FLASK_COVERAGE = 1


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
