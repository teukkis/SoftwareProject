import json
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from backend import db
from backend.models import Userm

# This bad boy is executed when request comes to the endpoint /api/user/
class User(Resource):
  def get(self, id):

    # query db for user
    found_user = Userm.query.filter_by(id=id).first()
    if found_user is None:
      data = {
      "message": "Not found"
    }
      return Response(json.dumps(data), status=404)

    # TODO, Encrypt password and check if it matches with the one in db

    data = {
      "id": found_user.id,
      "status": found_user.status,
      "privateKey": found_user.privateKey
    }
    return Response(json.dumps(data), status=200, mimetype='application/json')

  def put(self, id):
    pass

  def delete(self, id):
    pass


class Users(Resource):
  def get(self):
    found_user = Userm.query.all()

  def post(self):
    if not request.json:
      data = {
      "message": "Unsupported media type"
    }
      return Response(json.dumps(data), status=415)

    # Create a new user object
    # TODO status, and private key generation (if needed in this stage)
    newUser = Userm(
      id = str(request.json["id"]),
      password = str(request.json["password"]),
      privateKey = str(request.json["privateKey"]),
      status = str(request.json["status"])
    )

    # TODO user has to register with a given id, so check if it found in db
    # Use IntegrityError

    # Add new user and commit changes!!
    db.session.add(newUser)
    db.session.commit()

    return Response(status=201)
