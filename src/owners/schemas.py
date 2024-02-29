from datetime import datetime

from pydantic import BaseModel, EmailStr


class OwnerBase(BaseModel):
    username: str
    email: EmailStr
    contact_number: str
    picture_url: str


class OwnerView(OwnerBase):
    owner_id: int
    created_at: datetime


class OwnerCreate(OwnerBase):
    password: str
