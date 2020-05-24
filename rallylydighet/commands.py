import os
import os.path
from mimetypes import guess_type

import click
from flask import current_app
from flask.cli import with_appcontext

from rallylydighet.db import get_db
from rallylydighet.signs.dblayer import insert_sign
from rallylydighet.sequences.dblayer import new_sequence

@click.command("init-db")
@with_appcontext
def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))

    click.echo("Initialized the database.")

@click.command("populate-db")
@click.argument("image_dir")
@with_appcontext
def populate_db(image_dir):
    for root, _, files, rootfd in os.fwalk(image_dir):
        for f in files:
            name, _ = os.path.splitext(f)
            mime, _ = guess_type(f)
            if mime is None:
                continue
            elif mime not in ["image/jpeg", "image/png"]:
                continue

            info = os.stat(f, dir_fd=rootfd)
            with open(os.path.join(root, f), "rb") as f:
                insert_sign(name, mime, info.st_size, f.read())
    click.echo("Populated the database.")

@click.command("generate-sequences")
@with_appcontext
def generate_sequences():
    for _ in range(5):
        sequence_id = new_sequence()
        click.echo("Generated sequence: {}".format(sequence_id))

def init_app(app):
    app.cli.add_command(init_db)
    app.cli.add_command(populate_db)
    app.cli.add_command(generate_sequences)
