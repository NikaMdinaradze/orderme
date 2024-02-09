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
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username

    with pool.connection() as conn:
        cur = conn.cursor()
        result = cur.execute(
            "SELECT password FROM owner WHERE username=%s;", [username]
        ).fetchone()
    password = form_data.password

    if not verify(password, result[0]):
        raise HTTPException(
            detail="Invalid Credentials", status_code=status.HTTP_400_BAD_REQUEST
        )

    access_token = create_token(
        data={"sub": username}, expires_delta=timedelta(minutes=3)
    )
    refresh_token = create_token(data={"sub": username}, expires_delta=timedelta(days=7))

    return {"access_token": access_token, "refresh_token": refresh_token}
