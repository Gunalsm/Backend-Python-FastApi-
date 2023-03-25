from fastapi import FastAPI,Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import schemas
import models
from fastapi import Depends
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi import status,HTTPException
from typing import List
import Token
import oauth
import httpx
from oauth import oauth2_scheme


models.Base.metadata.create_all(engine)

app=FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
origins = [
    "http://localhost:4200", #frontend angular url
    "https://localhost:8000", #backend fastapi url
    "https://localhost:60" #backend service url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.post('/patients',response_model=schemas.Showpatient,tags = ['Users'])
def create_patient(request : schemas.Patient,db : Session = Depends(get_db)):
    new_patient = models.Patient(name=request.name,email=request.email,password=Hash.bcrypt(request.password),phone_number=request.phone_number)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    db.close()
    return new_patient

@app.get('/patients/{pat_id}',response_model=schemas.Showpatient,tags = ['Users'])
def get_patient(pat_id,db:Session =Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.pat_id == pat_id).first()
    return patient


@app.put('/patients/{pat_id}',status_code=status.HTTP_202_ACCEPTED,tags = ['Users'])
def update(pat_id,request : schemas.Patient,db : Session = Depends(get_db)):
    db.query(models.Patient).filter(models.Patient.pat_id == pat_id).update(request.dict())
    db.commit()
    return 'updated' 

@app.delete('/patients/{pat_id}',status_code=status.HTTP_204_NO_CONTENT,tags = ['Users'])
def delete(pat_id,db : Session = Depends(get_db)):
    db.query(models.Patient).filter(models.Patient.pat_id == pat_id).delete(synchronize_session=False)
    db.commit()
    return 'Done'


@app.post('/login',tags=['Authentication'])
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.email == request.username).first()
    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail='Invalid Credentials')

    access_token=Token.create_access_token(data={"subid":patient.pat_id})
    current_user = oauth.get_current_user(access_token)
    return {"access_token":access_token, "user":current_user}

@app.get('/showappointments/{pat_id}', tags=["Appointment"])
def show_appointment(pat_id: int, authorization: str = Depends(oauth2_scheme)):
    current_user = oauth.get_current_user(authorization)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
    
    callback_url = 'http://localhost:60/appoint/{pat_id}'
    appointments_response = httpx.get(callback_url.format(pat_id=pat_id), headers={"Authorization": authorization})
    appointment = appointments_response.json()
    return appointment






















# @app.get('/patients',response_model=List[schemas.Showpatient],tags = ['Users'])
# def get(db:Session =Depends(get_db)):
#     patients = db.query(models.Patient).all()
#     return patients 
