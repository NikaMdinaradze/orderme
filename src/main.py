from fastapi import FastAPI, status

from src import schemas
from src.db import get_pool

app = FastAPI()
pool = get_pool()


@app.post("/")
def create_restaurant(restaurant: schemas.RestaurantCreate):
    with pool.connection() as conn:
        conn.execute(
            "insert into restaurant (name, location, owner_name,"
            "email, password, contact_number) values (%s, %s, %s, %s, %s, %s)",
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
