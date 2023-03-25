from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal,engine
import models
import schemas
from sqlalchemy.orm import session
from datetime import datetime, timedelta
from typing import List
import crud



app=FastAPI()


origins = [
    "http://localhost:4200",
    "https://localhost:60",
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/appointment',tags = ['appointments'])
def create_appointment(request: schemas.Showappointment,db : session = Depends(get_db)):
     appoint = models.Appointment(name=request.name,email=request.email,phone_number=request.phone_number,date=request.date,doc_id=request.doc_id,slot_id=request.slot_id,pat_id=request.pat_id)
     user = db.query(models.Appointment).filter(models.Appointment.doc_id==request.doc_id).filter(models.Appointment.slot_id==request.slot_id).filter(models.Appointment.date==request.date).all()
     if user:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail='Slot Already Exists Choose another slot')
     db.add(appoint)
     db.commit()
     db.refresh(appoint)
     db.close()     
     return appoint
     
       
    

@app.get('/appointments',response_model=List[schemas.Showappointment],tags = ['appointments'])
def get_all(db:session=Depends(get_db)):
    return crud.get_all_appoint(db)



@app.get('/appointment/{app_id}',response_model=schemas.Showappointment,tags = ['appointments'])
def get_appoint(app_id,db:session =Depends(get_db)):
    appointment = crud.get_appoint_by_app_id(app_id,db)
    return appointment
        

@app.get('/appointments/{doc_id}',response_model=List[schemas.Showappointment],tags = ['appointments'])
def get_doc_appoints_with_doc(doc_id:int,db:session=Depends(get_db)):
    docapps=crud.get_appointment_by_doc(doc_id,db)
    return docapps

@app.get('/appoint/{pat_id}',response_model=List[schemas.Showappointment],tags = ['appointments'])
def get_pat_appoints(pat_id:int,db:session=Depends(get_db)):
    pat=crud.get_appointment_by_pid(pat_id,db)
    return pat




@app.put('/appointupdate/{app_id}', status_code=status.HTTP_202_ACCEPTED, tags=['appointments'])
def update(app_id:int, request: schemas.Showappointment, db: session = Depends(get_db)):
    u = db.query(models.Appointment).filter(models.Appointment.doc_id == request.doc_id).filter(models.Appointment.slot_id == request.slot_id).filter(models.Appointment.date == request.date).all()
    if u :
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail='Slot Already Exists Choose another slot')
    db.query(models.Appointment).filter(models.Appointment.app_id == app_id).update(request.dict())
    db.commit()
    return 'updated'




@app.delete('/appointments/{app_id}',tags = ['appointments'])
def delete(app_id,db : session = Depends(get_db)):
    db.query(models.Appointment).filter(models.Appointment.app_id == app_id).delete(synchronize_session=False)
    db.commit()
    return 'Done'
    
# #slots

@app.post('/slot' ,tags=['slots'])
def create_slot(request: schemas.ShowslotBook,db : session = Depends(get_db)):
    if crud.get_slot_by_id(request.slot_id,db):
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail='slot with id already exist')
    else:
        slot=crud.createSlot(request,db)
        return slot
    

@app.get('/slots',response_model=List[schemas.ShowslotBook],tags = ['slots'])
def getSlots(db:session=Depends(get_db)):
    return crud.get_all_slots(db)


@app.get('/slots/{doc_id}',response_model=List[schemas.ShowslotBook],tags=['slots'])
def docslot(doc_id:int,db:session=Depends(get_db)):
    slot=crud.get_slots_by_doc(doc_id,db)
    return slot




@app.get('/slots/{doc_id}/{day}',response_model=List[schemas.ShowslotBook],tags=['slots'])
def docdayslot(doc_id:int,day:str,db:session=Depends(get_db)):
    slot=crud.get_slots_by_day(doc_id,day,db)
    return slot


