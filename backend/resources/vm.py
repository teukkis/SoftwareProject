import json
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from backend import db
from backend.models import VirtualMachinem


class Vm(Resource):

  # Modify the state of a virtual machine, DOWN or UP
  def put(self, id):
    found_vm = VirtualMachinem.query.filter_by(id == id).first()
    if found_vm is None:
      data = {
        "message": "Not found"
      }
      return Response(json.dumps(data), status=404)

    if request.json["state"] == "UP":
      #TODO a script for starting the vm based on it's id
      found_vm.state=request.json["state"]

    elif request.json["state"] == "DOWN":
      #TODO a script for shutting down the vm based on it's id
      found_vm.state=request.json["state"]
    
    db.session.commit()

  # Delete the virtual machine (propably not needed at this point)
  def delete(self, id):
    found_vm = VirtualMachinem.query.filter_by(id == id).first()
    if found_vm is None:
      data = {
        "message": "Not found"
      }
      return Response(json.dumps(data), status=404)

    db.session.delete(found_vm)
    db.session.commit()

    return Response(status=204)

class Vms(Resource):

  # Fetch all virtual machines from the DB
  def get(self):
    data = []
    for vm in VirtualMachinem.query.all():
      tempData = {
        "id": vm.id,
        "state": vm.state,
      }
      data.append(tempData)

    return Response(json.dumps(data), status=200, mimetype='application/json')

