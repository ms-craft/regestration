from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  Column, Integer, String
 
from fastapi import FastAPI
 
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
 
 
class Base(DeclarativeBase): pass
class User(Base):
    __tablename__ = "client"
 
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    email = Column(String)
    login = Column(String)
 
SessionLocal = sessionmaker(autoflush=False, bind=engine)