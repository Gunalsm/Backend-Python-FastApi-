from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app=FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:80",
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/doctors',response_model=schemas.Showdoctor,tags = ['doctors'])
def create_doctor(request : schemas.Doctor,db : Session = Depends(get_db)):
    new_doctor = models.Doctor(name=request.name,email=request.email,password=Hash.bcrypt(request.password),phone_number=request.phone_number,catagory=request.catagory,doc_degree=request.doc_degree)
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

@app.get('/doctors/{doc_id}',response_model=schemas.Showdoctor,tags = ['doctors'])
def get_doctor(doc_id,db:Session =Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doc_id == doc_id).first()

    return doctor


@app.get('/doctors',response_model=List[schemas.Showdoctor],tags = ['doctors'])
def get(db:Session =Depends(get_db)):
    doctors = db.query(models.Doctor).all()
    return doctors

@app.put('/doctors/{doc_id}',status_code=status.HTTP_202_ACCEPTED,tags = ['doctors'])
def update(doc_id,request : schemas.Doctor,db : Session = Depends(get_db)):
    db.query(models.Doctor).filter(models.Doctor.doc_id == doc_id).update(request.dict())
    db.commit()
    return 'updated'

@app.delete('/doctors/{doc_id}',status_code=status.HTTP_204_NO_CONTENT,tags = ['doctors'])
def delete(doc_id,db : Session = Depends(get_db)):
    db.query(models.Doctor).filter(models.Doctor.doc_id == doc_id).delete(synchronize_session=False)
    db.commit()
    return 'Done'


@app.post('/login',tags=['Authentication'])
def login(request:schemas.Login,db:Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.email == request.username).first()
    if not doctor:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'Invalid Credentials')

    access_token=Token.create_access_token(data={"subid":doctor.doc_id})
    current_user = oauth.get_current_user(access_token)
    return {"access_token": access_token,"user":current_user}

@app.post('/admin',tags=['Admin'])
def login(request:schemas.Admin,db:Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.email == request.username).first()
    if not doctor:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'Invalid Credentials')

    access_token=Token.create_access_token(data={"sub":doctor.email}
    )
    return {"access_token": access_token,"token_type":"bearer"}




@app.get('/showappointments{doc_id}',tags=["Appointment"])
def showappointment(doc_id:int,callback_url:str = 'http://localhost:60/appointments/{doc_id}'):
    appointments_response = httpx.get(callback_url.format(doc_id=doc_id))
    appointment=appointments_response.json()
    return appointment


if __name__ == "__main__":
    app.run(debug=True)




















































# @app.post('/login',tags=['Authentication'])
# def login(request:schemas.Login,db:Session = Depends(get_db)):
#     doctor = db.query(models.Doctor).filter(models.Doctor.email == request.username).first()
#     if not doctor:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'Invalid Credentials')

#     access_token=Token.create_access_token(data={"subid":doctor.doc_id})
#     current_user = oauth.get_current_user(access_token)
#     return {"access_token": access_token,"user":current_user}
