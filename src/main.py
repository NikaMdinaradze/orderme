from fastapi import FastAPI, status
from psycopg.rows import class_row

from src import schemas
from src.db import get_pool

app = FastAPI()
pool = get_pool()


@app.post("/")
def create_restaurant(restaurant: schemas.RestaurantCreate):
    with pool.connection() as conn:
        conn.execute(
            "insert into restaurant (name, location, owner_name,"
            "email, password, contact_number) values (%s, %s, %s, %s, %s, %s);",
            (
                restaurant.name,
                restaurant.location,
                restaurant.owner_name,
                restaurant.email,
                restaurant.password,
                restaurant.contact_number,
            ),
        )
    return {"detail": "Restaurant Has Created", "status": status.HTTP_201_CREATED}


@app.get("/")
def get_restaurants():
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(schemas.RestaurantPreview))
        result = cur.execute("SELECT * FROM restaurant;").fetchall()
    return {"detail": result, "status": status.HTTP_200_OK}


@app.get("/{id}")
def get_restaurant(restaurant_id: int):
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(schemas.RestaurantView))
        result = cur.execute(
            "SELECT * FROM restaurant WHERE id = %s;", (restaurant_id,)
        ).fetchone()
    return {"detail": result, "status": status.HTTP_200_OK}


@app.put("/{id}")
def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate):
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(schemas.RestaurantView))
        result = cur.execute(
            "UPDATE restaurant SET "
            "name=%s, location=%s,"
            "owner_name=%s, email=%s,"
            "contact_number=%s"
            " WHERE id = %s"
            "RETURNING *;",
            (
                restaurant.name,
                restaurant.location,
                restaurant.owner_name,
                restaurant.email,
                restaurant.contact_number,
                restaurant_id,
            ),
        ).fetchone()
    return {"detail": result, "status": status.HTTP_200_OK}


@app.delete("/{id}")
def delete_restaurant(restaurant_id: int):
    with pool.connection() as conn:
        conn.execute("DELETE FROM restaurant WHERE id = %s;", (restaurant_id,))
    return {
        "detail": "restaurant successfully deleted",
        "status": status.HTTP_204_NO_CONTENT,
    }
