from pydantic import BaseModel,Field
from typing import List, Optional

class User(BaseModel):    
    username: str
    email : str
    otp : str
    password : str
 
    id: Optional[int] = None
    full_name: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False     
    otp: Optional[int] = None

class UserLogin(BaseModel):
    identifier : str
    password : str