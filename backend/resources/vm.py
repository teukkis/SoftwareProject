import json
from flask import Response, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError
from backend import db
from software import database_commands
from software import vm_commands


class Vm(Resource):

  # Modify the state of a virtual machine, 
  def put(self, id):

    success = database_commands.empty_vm(id)
    vm_commands.CloseVM(id)

    if success == True:
      return Response(status=204)

    else:
      return Response(status=400)

  # Delete the virtual machine (propably not needed at this point)
  def delete(self, id):
    pass

class Vms(Resource):

  # Fetch all virtual machines from the DB
  def get(self):
    vms = database_commands.get_vms()
    print(vms)
    data = []
    for vm in vms:
      print(vm)
      tempData = {
        "id": vm.id,
        "user": vm.user,
      }
      data.append(tempData)

    return Response(json.dumps(data), status=200, mimetype='application/json')

