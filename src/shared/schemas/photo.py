from pydantic import BaseModel


class PhotoView(BaseModel):
    url: str


class PhotoCreate(PhotoView):
    restaurant_id: int
