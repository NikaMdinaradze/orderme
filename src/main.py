from fastapi import FastAPI

from src.routers import restaurants

app = FastAPI()

app.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
