from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from database import Base
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# ============================================
# SHABLON: Har bir jadval uchun
# ============================================

# ------------------------- Users section -----------------------

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String(250))
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str | None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    role: str
    phone_number: str | None

    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)



class CurrentPasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)


# ------------------ Todos section --------------------

class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(15))
    description = Column(String(50))
    priority = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    complete = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# ---------------- Token ----------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

