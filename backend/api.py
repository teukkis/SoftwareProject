from flask import Blueprint
from flask_restful import Api
from backend import db

from backend.resources.user import User, Users

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(User, "/users/<id>")
api.add_resource(Users, "/users/")

@api_bp.route("/")
def entrypoint():
  
  return "the entrypoint"

