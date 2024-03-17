from flask.cli import FlaskGroup
from docid_app import create_app

cli = FlaskGroup(create_app)

if __name__ == '__main__':
    cli()
