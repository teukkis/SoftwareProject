import click
from flask.cli import with_appcontext
from backend import db


class Userm(db.Model):
  id = db.Column(db.String(128), primary_key=True)
  status = db.Column(db.String(32)) # superuser, admin, user
  privateKey = db.Column(db.String(256))
  publicKey = db.Column(db.String(256))
  password = db.Column(db.String(64))


class VirtualMachinem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  state = db.Column(db.String(8))

@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()

@click.command("testgen")
@with_appcontext
def generate_test_data():
 
  v0 = VirtualMachinem(
    id = 0,
    state = "down",
  )
  v1 = VirtualMachinem(
    id = 1,
    state = "down",
  )
  v2 = VirtualMachinem(
    id = 2,
    state = "down",
  )
  v3 = VirtualMachinem(
    id = 3,
    state = "down",
  )

  db.session.add(v0)
  db.session.add(v1)
  db.session.add(v2)
  db.session.add(v3)
  db.session.commit()
