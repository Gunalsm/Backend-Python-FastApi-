from pydantic import BaseModel
from typing import Optional

class Doctor(BaseModel):
    name : str
    email : str
    phone_number : int
    catagory : str
    password : str
    doc_degree : str

class Showdoctor(BaseModel):
    doc_id : int
    name : str
    email : str
    phone_number : int
    catagory : str
    doc_degree : str
    class Config():
        orm_mode = True

class Login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token : str
    token_data : str

class TokenData(BaseModel):
    name : Optional[str] = None
    doc_id:int

class Admin(BaseModel):
    username : str
    password : str