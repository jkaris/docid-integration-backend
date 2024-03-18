import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from .db import db

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app_settings = os.getenv("APP_SETTINGS")
        app.config.from_object(app_settings)
        app.config.from_prefixed_env("DOCID_APP_SETTINGS")
    else:
        app.config.from_mapping(test_config)
    CORS(app)

    @app.route('/')
    def index():
        return jsonify("Welcome to the DOCID Integration app!")

    from . import auth, doi, utils
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(doi.bp)
    app.register_blueprint(utils.bp)
    # docid_app.register_blueprint(save.bp)

    return app
