from flask import Blueprint
from flask_restful import Api
from backend import db

from backend.resources.user import User, Users
from backend.resources.vm import Vm, Vms
from backend.resources.port import Port

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(User, "/users/<id>")
api.add_resource(Users, "/users/")
api.add_resource(Vm, "/vms/<id>")
api.add_resource(Vms, "/vms/")
api.add_resource(Port, "/ports/<id>")

@api_bp.route("/")
def entrypoint():
  
  return "the entrypoint"

