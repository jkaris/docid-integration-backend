import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .db import db
from .models import init_db

from . import insert_data

load_dotenv()


def create_app(test_config=None):
    docid_app = Flask(__name__)
    docid_app.config.from_prefixed_env()
    docid_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    docid_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(docid_app)
    if test_config is None:
        docid_app.config.from_pyfile('config.py', silent=True)
    else:
        docid_app.config.from_mapping(test_config)

    try:
        os.makedirs(docid_app.instance_path)
    except OSError:
        pass

    from . import auth, doi, save, utils
    db.init_app(docid_app)
    # Create all database tables
    with docid_app.app_context():
        init_db()
        insert_data.insert_data()
        insert_data.generate_pids()
    # Register blueprints
    docid_app.register_blueprint(auth.bp)
    docid_app.register_blueprint(doi.bp)
    docid_app.register_blueprint(utils.bp)
    docid_app.register_blueprint(save.bp)

    return docid_app
