import json
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from backend import db
from software import database_commands
from software import file_commands
from Crypto.PublicKey import RSA

# This bad boy is executed when request comes to the endpoint /api/user/
class User(Resource):

  # Fetch one user based on its id
  def get(self, id):
    student = database_commands.get_student_by_id(id)
    if student is None:
      data = {
      "message": "Not found"
    }
      return Response(json.dumps(data), status=404)

    data = {
      "id": student.id,
      "connect_time": str(student.connect_time),
      "disconnect_time": str(student.disconnect_time),
    }
    return Response(json.dumps(data), status=200, mimetype='application/json')

  # Delete the user based on its id
  def delete(self, id):
    
    failure = database_commands.delete_user(id)

    if failure == False:
      file_commands.delete_user(id)
      return Response(status=204)

    else:
      print(failure)
      return Response(status=404)


  def put(self, id):

    key = RSA.generate(1024)
    privateKey = key.exportKey('PEM')
    
    pubkey = key.publickey()
    publicKey = pubkey.exportKey('OpenSSH')

    new_privateKey=str(privateKey)
    new_publicKey=str(publicKey)

    success = database_commands.changePublicKey(id)

    if success:
      data = {
        "privateKey": new_privateKey,
      }
      return Response(json.dumps(data), status=201)

    else:
      return Response(status=404)

class Users(Resource):

  # Fecth all users from the DB
  def get(self):
    students = database_commands.get_students()
    data = []
    for student in students:
      isActive = database_commands.check_active_users(student.id)
      tempData = {
        "id": student.id,
        "connect_time": str(student.connect_time),
        "disconnect_time": str(student.disconnect_time),
        "isActive": isActive
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
    
    privateKey = str(privateKey),
    publicKey = str(publicKey),
    id = str(request.json["id"])
    
    message, success = file_commands.add_student(id, publicKey)

    if not success:
      fail = message

    else:
      fail = database_commands.add_student(id)

    if fail == False:
      data = {
        "privateKey": privateKey
      }
      return Response(json.dumps(data), status=201)

    else:
      file_commands.delete_user(id)
      data = {
        "privateKey": ""
      }
      return Response(json.dumps(data), status=400)

    

