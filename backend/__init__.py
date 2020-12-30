import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

db = SQLAlchemy()

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  CORS(app, resources={r"/*": {"origins": "*"}})
  

  from . import api
  from software import database_commands
  
  app.register_blueprint(api.api_bp)

  return app