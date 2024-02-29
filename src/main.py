from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.db import db_url
from src.owners.router import router as owners_router
from src.restaurants.router import router as restaurants_router

app = FastAPI()

app.include_router(owners_router, prefix="/restaurants", tags=["restaurants"])
app.include_router(restaurants_router, prefix="/owners", tags=["owners"])

register_tortoise(
    app,
    db_url=db_url,
    modules={
        "models": ["src.owners.models", "src.restaurants.models", "src.shared.models"]
    },
    generate_schemas=True,
    add_exception_handlers=True,
)
