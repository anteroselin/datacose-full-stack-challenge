from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core import security
from core.settings import settings

from db.schemas import UserCreate, User
from db.repositories import UserRepository
from db.session import get_db

router = APIRouter()

@router.post('/login')
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = UserRepository.get_user_by_username(db, username = form_data.username)
    if not user or not (form_data.password == user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)

    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post('/register', response_model=User)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = UserRepository.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered',
        )

    created_user = UserRepository.create_user(db, user)
    return created_user