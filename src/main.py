from fastapi import FastAPI

from src import schemas
from src.db import get_pool

app = FastAPI()
pool = get_pool()


@app.get("/")
def create_restaurant(restaurant: schemas.Restaurant):
    with pool.connection() as conn:
        conn.execute(
            "insert into restaurants (, completed) values (%s, %s)",
            [restaurant],
        )
