from datetime import datetime

from pydantic import BaseModel


class OwnerBase(BaseModel):
    username: str
    email: str
    contact_number: str
    picture_url: str


class OwnerView(OwnerBase):
    owner_id: int
    created_at: datetime


class OwnerCreate(OwnerBase):
    password: str
