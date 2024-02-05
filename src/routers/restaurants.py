from fastapi import APIRouter, status
from psycopg.rows import class_row

from src.db import get_pool
from src.schemas.restaurant import RestaurantPreview, RestaurantView

router = APIRouter()
pool = get_pool()


@router.get("/")
def get_restaurants():
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(RestaurantPreview))
        result = cur.execute("SELECT * FROM restaurant;").fetchall()
    return {"detail": result, "status": status.HTTP_200_OK}


@router.get("/{id}")
def get_restaurant(restaurant_id: int):
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(RestaurantView))
        result = cur.execute(
            "SELECT * FROM restaurant WHERE id = %s;", (restaurant_id,)
        ).fetchone()
    return {"detail": result, "status": status.HTTP_200_OK}


@router.delete("/{id}")
def delete_restaurant(restaurant_id: int):
    with pool.connection() as conn:
        conn.execute("DELETE FROM restaurant WHERE id = %s;", (restaurant_id,))
    return {
        "detail": "restaurant successfully deleted",
        "status": status.HTTP_204_NO_CONTENT,
    }
