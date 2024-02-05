from fastapi import FastAPI

from src.routers import owners, restaurants

app = FastAPI()

app.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
app.include_router(owners.router, prefix="/owners", tags=["owners"])
