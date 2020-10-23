import click
from flask.cli import with_appcontext
from backend import db


class Userm(db.Model):
  id = db.Column(db.String(32), primary_key=True)
  status = db.Column(db.String(32)) # superuser, admin, user
  privateKey = db.Column(db.String(256))
  password = db.Column(db.String(64))

  def __repr__(self):
    return "{} <{}>".format(self.status, self.id)


@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()

@click.command("testgen")
@with_appcontext
def generate_test_data():
  u = Userm(
    id = "R2D2",
    password = "shit",
    status = "admin",
    privateKey = "anotherShit"
  )

  db.session.add(u)
  db.session.commit()
