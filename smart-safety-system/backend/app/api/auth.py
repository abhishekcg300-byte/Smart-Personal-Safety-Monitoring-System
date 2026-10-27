from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import User
from app.schemas.schemas import RegisterIn, LoginIn, TokenOut, UserOut
from app.security.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(email=data.email, full_name=data.full_name,
                hashed_password=hash_password(data.password),
                role=data.role if data.role in ("owner", "trusted") else "owner")
    db.add(user)
    db.commit()
    db.refresh(user)
    # default settings
    from app.models.models import UserSettings
    db.add(UserSettings(user_id=user.id))
    db.commit()
    return user


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    return TokenOut(access_token=create_access_token(user.id, user.role))


@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
