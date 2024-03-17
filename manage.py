import click
from flask.cli import FlaskGroup
from docid_app import create_app
from docid_app.db import db
from docid_app.seed_db import insert_data, generate_pids

cli = FlaskGroup(create_app)


@cli.command("recreate_db")
@click.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("insert_datas")
@click.command()
def insert_datas():
    insert_data()


@cli.command("generate_pids")
@click.command()
def generate_pids():
    generate_pids()


if __name__ == "__main__":
    cli()
