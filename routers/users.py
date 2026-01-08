from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todos, TodoRequest, Users, UserResponse, CurrentPasswordRequest
from database import SessionLocal
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# BU FUNKSIYANI YODLAB OLING!
# Har bir loyihada BIR XILDA!

# ============================================
# QADAM 3.4: Dependency Annotation (DOIM SHUNDAY!)
# ============================================

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/me', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency,
                   db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail='User not found')

    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,
                          db: db_dependency,
                          password_request: CurrentPasswordRequest):
    # 1. Token tekshirish
    if not user:
        raise HTTPException(status_code=401, detail='User not found')

    # 2. DB dan user olish
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Eski parolni tekshirish
    if not bcrypt_context.verify(
        password_request.current_password,
        user_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail='Current password is incorrect')

    # 4. Yangi parolni hash qilish
    user_model.hashed_password = bcrypt_context.hash(
        password_request.new_password
    )
    # 5. Saqlash
    db.add(user_model)
    db.commit()


@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency,
                          db: db_dependency, phone_number: str):
    # 1. Token tekshirish
    if not user:
        raise HTTPException(status_code=401, detail='User not found')

    # 2. DB dan user olish
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")


    user_model.phone_number = phone_number
    # 5. Saqlash
    db.add(user_model)
    db.commit()