from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.db import get_pool
from src.JWT import create_token
from src.schemas.owner import OwnerCreate
from src.utils import hashing, verify

router = APIRouter()
pool = get_pool()


@router.post("", status_code=status.HTTP_201_CREATED)
def register(response: OwnerCreate):
    with pool.connection() as conn:
        conn.execute(
            "INSERT INTO owner ("
            "username,"
            " email,"
            " password,"
            " contact_number,"
            " picture_url)"
            "VALUES (%s, %s, %s, %s, %s)",
            (
                response.username,
                response.email,
                hashing(response.password),  # hashing password
                response.contact_number,
                response.picture_url,
            ),
        )

    return {"detail": "successfully registered"}


@router.post("/login")
def login(response: OAuth2PasswordRequestForm = Depends()):
    with pool.connection() as conn:
        cur = conn.cursor()
        owner = cur.execute(
            "SELECT owner_id, password FROM owner WHERE username=%s;",
            (response.username,),
        ).fetchone()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
        )
    owner_id, password = owner
    if not verify(response.password, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )
    access_token = create_token(
        {"user_id": owner_id, "type": "access"}, timedelta(minutes=5)
    )
    refresh_token = create_token(
        {"user_id": owner_id, "type": "refresh"}, timedelta(days=7)
    )

    return {"Access_token": access_token, "Refresh_token": refresh_token}
