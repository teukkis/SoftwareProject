import json
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from backend import db
from backend.models import Userm
from Crypto.PublicKey import RSA
import uuid

# This bad boy is executed when request comes to the endpoint /api/user/
class User(Resource):

  # Fetch one user based on its id
  def get(self, id):

    # query db for user
    found_user = Userm.query.filter_by(id=id).first()
    if found_user is None:
      data = {
      "message": "Not found"
    }
      return Response(json.dumps(data), status=404)


    data = {
      "id": found_user.id,
      "status": found_user.status,
      "privateKey": found_user.privateKey,
      "publicKey": found_user.publicKey
    }
    return Response(json.dumps(data), status=200, mimetype='application/json')

  # Delete the user based on its id
  def delete(self, id):
    found_user = Userm.query.filter_by(id=id).first()
    if found_user is None:
      data = {
        "message": "Not found"
      }
      return Response(json.dumps(data), status=404)

    db.session.delete(found_user)
    db.session.commit()

    return Response(status=204)

  def put(self, id):
    found_user = Userm.query.filter_by(id=id).first()
    if found_user is None:
        data = {
          "message": "Not found"
        }
        return Response(json.dumps(data), status=404)

    key = RSA.generate(1024)
    privateKey = key.exportKey('PEM')
    
    pubkey = key.publickey()
    publicKey = pubkey.exportKey('OpenSSH')

    
    # Create a new user object
    new_privateKey=str(privateKey)
    new_publicKey=str(publicKey)

    data = {
      "privateKey": new_privateKey,
      "publicKey": new_publicKey
    }

    db.session.commit()

    return Response(json.dumps(data), status=201)

class Users(Resource):

  # Fecth all users from the DB
  def get(self):
    data = []
    for user in Userm.query.all():
      tempData = {
        "id": user.id,
        "status": user.status,
        "privateKey": str(user.privateKey),
        "publicKey": str(user.publicKey)
      }
      data.append(tempData)

    return Response(json.dumps(data), status=200, mimetype='application/json')

  # Create a new user
  def post(self):

    #https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
    # Generate public and private keys
    key = RSA.generate(1024)
    privateKey = key.exportKey('PEM')
    
    pubkey = key.publickey()
    publicKey = pubkey.exportKey('OpenSSH')

    uniqueID = str(uuid.uuid4())
    
    # Create a new user object
    newUser = Userm(
      id = uniqueID,
      password = None,
      privateKey = str(privateKey),
      publicKey = str(publicKey),
      status = str(request.json["status"])
    )

    data = {
      "id": uniqueID
    }

    # Add new user and commit changes!!
    db.session.add(newUser)
    db.session.commit()

    return Response(json.dumps(data), status=201)
