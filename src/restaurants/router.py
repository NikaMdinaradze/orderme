from fastapi import APIRouter, status

from src.restaurants import schemas

router = APIRouter()


@router.get("/", response_model=schemas.RestaurantPreview)
def get_restaurants():
    return {"detail": ...}


@router.get("/{id}", response_model=schemas.RestaurantView)
def get_restaurant(restaurant_id: int):
    return {"detail": ...}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int):
    return {"detail": "restaurant successfully deleted"}
