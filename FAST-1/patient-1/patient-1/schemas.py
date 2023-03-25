from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):
    name : str
    email : str
    phone_number : str
    password : str
    


class Showpatient(BaseModel):
    pat_id : str
    name : str
    email : str
    phone_number : str
    password : str

    class Config():
        orm_mode = True

class Login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token : str
    token_data : str

class TokenData(BaseModel):
    # name : Optional[str] = None
    pat_id:int
