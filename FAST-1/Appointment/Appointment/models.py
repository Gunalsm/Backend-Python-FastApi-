import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Appointment(Base):
    __tablename__="appointments"

    app_id = Column(Integer,primary_key=True,index = True)
    name=Column(String(255))
    phone_number=Column(String(255))
    email=Column(String(255))
    date=Column(String(255))
    doc_id=Column(Integer)
    slot_id=Column(Integer)
    pat_id=Column(Integer)


class SlotBook(Base):
    __tablename__ = "SlotBook"
    
   
    slot_id=Column(Integer,primary_key=True,index=True)
    doc_id=Column(Integer)
    days=Column(String(255))
    slots=Column(Integer)
   



