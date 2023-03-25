from sqlalchemy.orm import Session
from fastapi import HTTPException,status
import models, schemas
from typing import List
from sqlalchemy import update
from models import SlotBook
from schemas import ShowslotBook

# def createAppointment(request: schemas.Showappointment,db : Session):
#     appoint = models.Appointment(name=request.name,email=request.email,phone_number=request.phone_number,date=request.date,doc_id=request.doc_id,slot_id=request.slot_id,pat_id=request.pat_id)
#     user = db.query(models.Appointment).filter(models.Appointment.doc_id==request.doc_id).filter(models.Appointment.slot_id==request.slot_id).all()
#     if user:
#         db.add(appoint)
#         db.commit()
#         db.refresh(appoint)
#         db.close()
#         return appoint
#     raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail='Slot Already Exists Choose another slot')

def get_all_appoint(db:Session):
    appoint = db.query(models.Appointment).all()
    return appoint

def get_appoint_by_app_id(app_id:int,db:Session):
    appoint = db.query(models.Appointment).filter(models.Appointment.app_id == app_id).first()
    return appoint

def get_appointment_by_doc(doc_id:int,db:Session):
    doc = db.query(models.Appointment).filter(models.Appointment.doc_id == doc_id).all()
    return doc

def get_appointment_by_pid(pat_id:int,db:Session)->List[schemas.Showappointment]:
    pat = db.query(models.Appointment).filter(models.Appointment.pat_id == pat_id).all()
    return pat

# def delete_slot_after_book(slot_id:int,doc_id:int,date:str,db:Session):
#     slots=db.query(models.SlotBook).filter(models.SlotBook.slots==slot_id,models.SlotBook.doc_id==doc_id,models.SlotBook.days==date).first()
#     db.delete(slots)
#     db.commit()
#     db.close()

# def delete_slot_after_book(slot_id: int, doc_id: int, day: str, db: Session):
#     appointment = db.query(models.Appointment).filter(models.Appointment.slot_id == slot_id).first()
#     if appointment:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete a slot that has already been booked.")
#     else:
#         slot = db.query(models.SlotBook).filter(models.SlotBook.slot_id == slot_id, models.SlotBook.doc_id == doc_id, models.SlotBook.days == day).first()
#         if slot:
#             db.delete(slot)
#             db.commit()
#             return slot
#         else:
#             return None


def get_slot_by_id(slot_id:int,db:Session):
    slot = db.query(models.SlotBook).filter(models.SlotBook.slot_id == slot_id).first()
    return slot



def get_all_slots(db:Session):
    slots = db.query(models.SlotBook).all()
    return slots

def get_slots_by_doc(doc_id:int,db:Session):
    slots = db.query(models.SlotBook).filter(models.SlotBook.doc_id == doc_id).all()
    return slots

def get_slots_by_day(doc_id:int,day:str,db:Session):
    slots = db.query(models.SlotBook).filter(models.SlotBook.doc_id == doc_id,models.SlotBook.days==day).all()
    return slots

def update_slot_booked_status(slot_id: int, db: Session, booked: bool ):
    db.query(models.SlotBook).filter(models.SlotBook.slot_id == slot_id).first()
    db.commit()
    # db.refresh()
       

def createSlot(request: schemas.ShowslotBook,db :Session):
    slot=models.SlotBook(doc_id=request.doc_id,days=request.days,slots=request.slots)
    db.add(slot)
    db.commit()
    db.refresh(slot)
    db.close()
    return slot
