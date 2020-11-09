import json
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from backend import db
from backend.models import VirtualMachinem
from backend.models import Userm


class Port(Resource):

  # Fetch a vm --> return the port address
  def get(self, id):
    
    found_user = Userm.query.filter_by(id=id).first()
    if found_user is None:
      data = {
      "message": "Not found"
    }
      return Response(json.dumps(data), status=404)

    data = {
      "message": "Success",
      "port": "12345"
    }

    # TODO, forward the port of a user who requested help

    return Response(json.dumps(data), status=200)
