from datetime import datetime

from pydantic import BaseModel, EmailStr

from src.db import get_pool

pool = get_pool()


class RestaurantBase(BaseModel):
    name: str
    location: str


class RestaurantPreview(RestaurantBase):
    id: int


class RestaurantCreate(RestaurantBase):
    contact_number: str
    owner_name: str
    email: EmailStr
    password: str


class RestaurantView(RestaurantPreview):
    owner_name: str
    email: str
    password: str
    contact_number: str
    created_at: datetime


class RestaurantUpdate(RestaurantBase):
    contact_number: str
    owner_name: str
    email: EmailStr
    contact_number: str
    password: str
