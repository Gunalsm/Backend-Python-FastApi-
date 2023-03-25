from pydantic import BaseModel
from pydantic.schema import Optional
import datetime

from datetime import date
class Appointment(BaseModel):
    name:str
    phone_number:str
    email:str
    date:date

class Showappointment(BaseModel):
    app_id:int
    name:str
    phone_number:str
    email:str
    date:str
    doc_id:int
    slot_id:int
    pat_id:int

    class Config():
        orm_mode=True

class SlotBook(BaseModel):
    doc_id:int
    days : str
    slots :int
 

class ShowslotBook(BaseModel):
    
    slot_id:str
    doc_id:int
    days : str 
    slots:int
    # isbook:int
    class Config():
        orm_mode=True
    





    
    