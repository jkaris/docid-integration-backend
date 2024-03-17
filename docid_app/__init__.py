import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .db import db

# from .models import init_db

# from . import insert_data

load_dotenv()


def create_app(test_config=None):
    docid_app = Flask(__name__)
    # set config
    app_settings = os.getenv("APP_SETTINGS")
    docid_app.config.from_object(app_settings)
    docid_app.config.from_prefixed_env("DOCID_APP_SETTINGS")
    CORS(docid_app)

    from . import auth, doi, utils

    db.init_app(docid_app)
    # Create all database tables
    # with docid_app.app_context():
    #     init_db()
    #     insert_data.insert_data()
    #     insert_data.generate_pids()
    # Register blueprints
    docid_app.register_blueprint(auth.bp)
    docid_app.register_blueprint(doi.bp)
    docid_app.register_blueprint(utils.bp)
    # docid_app.register_blueprint(save.bp)

    return docid_app
