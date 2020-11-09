import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

db = SQLAlchemy()

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  CORS(app, resources={r"/*": {"origins": "*"}})
  app.config.from_mapping(
    SECRET_KEY="nothingyet",
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "chipwhisperer.db"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
  )

  if test_config is None:
    app.config.from_pyfile("config.py", silent=True)

  else:
    app.config.from_mapping(test_config)

  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  db.init_app(app)

  from . import models
  from . import api
  app.cli.add_command(models.init_db_command)
  app.cli.add_command(models.generate_test_data)


  
  # Propably the place to call init functions
  # app.cli.add_command()
  
  app.register_blueprint(api.api_bp)

  return app