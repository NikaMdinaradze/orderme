from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.db import db_url
from src.routers import owners, restaurants

app = FastAPI()

app.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
app.include_router(owners.router, prefix="/owners", tags=["owners"])

register_tortoise(
    app,
    db_url=db_url,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
