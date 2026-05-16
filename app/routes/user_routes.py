from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.auth.hashing import hash_password

from app.schemas.user_schema import UserLogin
from app.auth.hashing import verify_password
from app.auth.token import create_access_token

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        return {
            "error": "Email already exists"
        }

    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    return {
        "message": "User created successfully"
    }

@router.post("/login")
def login(
    user: UserLogin,
    # db: Session = Depends(get_db)
    # request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:

        return {
            "error": "User not found"
        }

    if not verify_password(
        user.password,
        existing_user.password
    ):

        return {
            "error": "Invalid password"
        }

    token = create_access_token(
        data = {"sub": existing_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }