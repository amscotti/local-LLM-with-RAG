from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer)
    department_id = Column(Integer)
    access_id = Column(Integer)

class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(255), nullable=False)

class Access(Base):
    __tablename__ = "access"

    id = Column(Integer, primary_key=True, index=True)
    access_name = Column(String(255), nullable=False)

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # Название контента
    description = Column(Text, nullable=True)  # Описание контента
    file_path = Column(String(255), nullable=False)  # Путь к файлу
    access_level = Column(Integer, ForeignKey("access.id"), nullable=False)  # Уровень доступа

    access = relationship("Access")  # Связь с таблицей Access

