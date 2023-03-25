from sqlalchemy import Column, Integer, String
from database import Base

class Doctor(Base):
    __tablename__="doctors"

    doc_id = Column(Integer,primary_key=True,index = True)
    name = Column(String(255))
    email = Column(String(255))
    phone_number = Column(Integer)
    catagory = Column(String(255))
    password = Column(String(255))
    doc_degree = Column(String(255))

