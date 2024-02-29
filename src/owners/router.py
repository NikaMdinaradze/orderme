from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.JWT import create_token, refresh_access_token
from src.owners import schemas

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def register(response: schemas.OwnerCreate):
    return {"detail": "successfully registered"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": ..., "refresh_token": ...}


@router.post("/refresh")
def refresh_token(user: str = Depends(refresh_access_token)):
    token = create_token(data={"sub": user})
    return {"access_token": token, "token_type": "bearer"}
