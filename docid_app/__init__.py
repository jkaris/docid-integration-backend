import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_prefixed_env()
    CORS(app)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db, auth, doi, save, utils
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(doi.bp)
    app.register_blueprint(utils.bp)
    app.register_blueprint(save.bp)
    print(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    print(f"Using Database: {app.config.get('FLASK_DATABASE')}")

    return app