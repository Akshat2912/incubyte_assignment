from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SweetCreate(BaseModel):
    name: str
    price: float
    quantity: int
    category: Optional[str] = None


class SweetRead(SweetCreate):
    id: int

class SweetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
