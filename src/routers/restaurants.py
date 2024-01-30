from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from psycopg.errors import UniqueViolation
from psycopg.rows import class_row

from src import schemas
from src.db import get_pool
from src.JWT import create_token
from src.utils import hashing, verify

router = APIRouter()
pool = get_pool()


@router.post("/")
def create_restaurant(restaurant: schemas.RestaurantCreate):
    with pool.connection() as conn:
        try:
            conn.execute(
                "INSERT INTO restaurant (name, location, owner_name,"
                "email, password, contact_number) VALUES (%s, %s, %s, %s, %s, %s);",
                (
                    restaurant.name,
                    restaurant.location,
                    restaurant.owner_name,
                    restaurant.email,
                    hashing(restaurant.password),  # hashing password
                    restaurant.contact_number,
                ),
            )
        except UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Credentials already exists",
            )
    return {"detail": "Restaurant Has Created", "status": status.HTTP_201_CREATED}


@router.post("/login")
def login(response: OAuth2PasswordRequestForm = Depends()):
    with pool.connection() as conn:
        cur = conn.cursor()
        user = cur.execute(
            "SELECT id, password FROM restaurant WHERE email=%s;", (response.username,)
        ).fetchone()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="There is no username or password",
        )
    user_id, password = user
    if not verify(response.password, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )
    access_token = create_token(
        {"user_id": user_id, "type": "access"}, timedelta(minutes=5)
    )
    refresh_token = create_token(
        {"user_id": user_id, "type": "refresh"}, timedelta(days=7)
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/")
def get_restaurants():
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(schemas.RestaurantPreview))
        result = cur.execute("SELECT * FROM restaurant;").fetchall()
    return {"detail": result, "status": status.HTTP_200_OK}


@router.get("/{id}")
def get_restaurant(restaurant_id: int):
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(schemas.RestaurantView))
        result = cur.execute(
            "SELECT * FROM restaurant WHERE id = %s;", (restaurant_id,)
        ).fetchone()
    return {"detail": result, "status": status.HTTP_200_OK}


@router.put("/{id}")
def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate):
    with pool.connection() as conn:
        cur = conn.cursor(row_factory=class_row(schemas.RestaurantView))
        result = cur.execute(
            "UPDATE restaurant SET "
            "name=%s, location=%s,"
            "owner_name=%s, email=%s,"
            "contact_number=%s,"
            "password=%s,"
            " WHERE id = %s"
            "RETURNING *;",
            (
                restaurant.name,
                restaurant.location,
                restaurant.owner_name,
                restaurant.email,
                restaurant.contact_number,
                restaurant.password,
                restaurant_id,
            ),
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
