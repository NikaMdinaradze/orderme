from datetime import datetime

from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    location: str


class RestaurantPreview(RestaurantBase):
    id: int


class RestaurantCreate(RestaurantBase):
    owner_name: str
    email: str
    password: str


class RestaurantView(RestaurantPreview):
    owner_name: str
    email: str
    password: str
    contact_number: str
    created_at: datetime
