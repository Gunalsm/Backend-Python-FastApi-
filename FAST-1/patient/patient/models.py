from sqlalchemy import Column, Integer, String
from database import Base

class Patient(Base):
    __tablename__="patients"

    pat_id = Column(Integer,primary_key=True,index = True)
    name = Column(String(255))
    email = Column(String(255),unique=True)
    phone_number = Column(String(255))
    password = Column(String(255))




