from datetime import datetime

from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    location: str


class RestaurantPreview(RestaurantBase):
    restaurant_id: int
    logo_url: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantView(RestaurantPreview):
    owner_name: str
    email: str
    created_at: datetime


class RestaurantUpdate(RestaurantBase):
    pass
