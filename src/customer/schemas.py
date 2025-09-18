from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class CustomerCreate(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    phone_number: int = Field(...)

class CustomerLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
