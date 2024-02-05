from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.db import get_pool
from src.JWT import create_token
from src.utils import verify

router = APIRouter()
pool = get_pool()


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
