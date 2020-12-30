from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey, String, DateTime, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
import datetime
Base = declarative_base()




class VirtualMachine(Base):
    __tablename__ = 'virtual_machine'
    id = Column(Integer, primary_key=True)
    user = Column(String, ForeignKey('student.id'), nullable = True)

class Student(Base):
    __tablename__ = 'student'
    id = Column(String, primary_key = True)
    connect_time = Column(DateTime, nullable = True)
    disconnect_time = Column(DateTime, nullable = True)

engine = create_engine("sqlite:////home/teukka/Desktop/SoftwareProject/software/chipwhisperer.db")

Session = sessionmaker(bind=engine)


def get_students():
    session = Session()
    students = session.query(Student).order_by(Student.id).all()
    session.close()
    return students

def get_student_by_id(id, session):
    try:
        student = session.query(Student).filter(Student.id == id).first()
        return student
    except:
        print("Error querying student from the database with id: {}".format(id))
        return None

def get_vms():
    session = Session()
    vms = session.query(VirtualMachine).all()
    return vms

def check_free_vm(session):
    vms = get_vms(session)
    for vm in vms:
        if vm.user == None:
            return True
    return False

def get_vm_by_user(id, session):
    try:
        return session.query(VirtualMachine).filter(VirtualMachine.user == id).first()
    except:
        print("Didn't find virtual machine with user id: {}".format(id))
        return None

def check_active_users(id):
    session = Session()
    try:
        vm = session.query(VirtualMachine).filter(VirtualMachine.user == id).first()
        print(str(vm.id))
        return True
    except:
        return False

def get_first_free_vm(session):
    try:
        vm = session.query(VirtualMachine).filter(VirtualMachine.user==None).first()
        return vm
    except:
        print("Couldn't find free virtual machine")
        return None

def get_vm_by_id(id, session):
    try:
        return session.query(VirtualMachine).filter(VirtualMachine.id == id).first()
    except:
        print("Didn't find virtual machine with id: {}".format(id))
        return None

def set_student_on_vm(id):
    session = Session()
    isfree = check_free_vm(session)
    if not isfree:
        print("No free vms available")
        return False
    
    student = get_student_by_id(id, session)
    vmt = get_vm_by_user(id, session)
    vm = get_first_free_vm(session)
    if (not vmt == None):
        student.connect_time = datetime.datetime.now()
        print("Student {} logged back in on vm: {}".format(id, vmt.id))
        vmid = vmt.id
        session.commit()
        session.close()
        return vmid, False
    if vm == None or student == None:
        session.close()
        return False, False
    vm.user = student.id
    vmid = vm.id
    student.connect_time = datetime.datetime.now()
    session.commit()
    session.close()
    return vmid, True

def free_student_from_vm(id):
    session = Session()
    student = get_student_by_id(id, session)
    vm = get_vm_by_user(id, session)
    if vm == None or student == None:
        session.close()
        return False
    vm.user = None
    toreturn =  "Succesfully removed user {} from machine {}".format(student.id, vm.id)
    port = vm.id
    print(toreturn)
    student.disconnect_time = datetime.datetime.now()
    session.commit()
    session.close()
    return port

def empty_vm(id):
    session = Session()
    vm = get_vm_by_id(id, session)
    if vm == None:
        return False
    vm.user = None
    session.commit()
    session.close()
    return True

def disconnect_student(id):
    session = Session()
    student = get_student_by_id(id, session)
    if student == None:
        session.close()
        return False
    student.disconnect_time = datetime.datetime.now()
    session.commit()
    session.close()
    return True

def add_student(id):
    session = Session()
    ret = False
    try:
        student = Student()
        student.id = id
        student.password = get_random_string(6)
        session.add(student)
        session.commit()
    except Exception as e:
        session.rollback()
        ret = e
    finally:
        session.close()
        return ret

def delete_user(id):
    session = Session()
    ret = False
    try:
        student = get_student_by_id(id, session)
        session.delete(student)
        session.commit()
    except Exception as e:
        session.rollback()
        ret = e
    finally:
        session.close()
        return ret

def changePublicKey():
    session = Session()
    