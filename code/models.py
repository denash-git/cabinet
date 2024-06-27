from pydantic import BaseModel, field_validator
from typing import List
import re
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# ТУТ ТОЛЬКО МОДЕЛИ ДАННЫХ, Модели Pydantic

# модель пользователя в базе
Base = declarative_base()
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")


# для проверки ввода пароля
class UserValid(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Длина пароля должна составлять не менее 8 символов')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать заглавную букву')
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
        #     raise ValueError('Пароль должен содержать специальный символ')
        if not re.match(r'^[A-Za-z0-9!@#$%^&*(),.?":{}|<>]+$', v):
            raise ValueError('Пароль должен содержать только буквы, цифры и специальные символы')
        return v

 # для структуры меню sidebar
class SubItem(BaseModel):
    title: str
    url: str

class MenuItem(BaseModel):
    title: str
    role: str
    subitems: List[SubItem]