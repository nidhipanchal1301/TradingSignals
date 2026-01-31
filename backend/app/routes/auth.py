from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from ..schemas.user import UserCreate, UserResponse
from ..schemas.token import Token
from ..crud.user import create_user, get_user_by_email, get_user_by_id
from ..core.security import verify_password, create_access_token
from ..core.config import settings
from ..database.db import get_db


router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -----------------------------------------
# GET CURRENT USER (JWT)
# -----------------------------------------
def get_current_user(
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: str | None = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# -----------------------------------------
# SIGNUP
# -----------------------------------------
@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    new_user = create_user(db, user.email, user.password)
    return new_user


# -----------------------------------------
# LOGIN
# -----------------------------------------
@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)

    if not db_user or not verify_password(
        user.password, db_user.password_hash
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials",
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_access_token(
        data={"user_id": str(db_user.id)},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# -----------------------------------------
# CURRENT USER PROFILE
# -----------------------------------------
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user
