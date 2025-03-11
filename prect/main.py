from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
import os, datetime, time, sys, json, traceback, html, importlib, glob
from collections import defaultdict
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import Response, HTMLResponse, JSONResponse, PlainTextResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
 
# создаем таблицы
Base.metadata.create_all(bind=engine)
 
app = FastAPI()
 
# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_user_exists(db: Session, login: str, email: str) -> bool:
    user = db.query(User).filter((User.login == login) | (User.email == email)).first()
    return user is not None  # Если нашли пользователя, возвращаем True
  
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("register.html", {"request": request}) 

@app.get("/api/users")
def get_people(db: Session = Depends(get_db)):
    return db.query(User).all()
  
@app.get("/api/users/{id}")
def get_User(id, db: Session = Depends(get_db)):
    # получаем пользователя по id
    
    person = db.query(User).filter(User.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person==None:  
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    #если пользователь найден, отправляем его
    return person
  
  
@app.post("/api/users") 
def create_person(data  = Body(), db: Session = Depends(get_db)):
    if check_user_exists(db, data["login"], data["email"]):
        return JSONResponse(status_code=404, content={ "message": "Пользователь уже существует"})
    else:
        person = User(password=data["password"], login=data["login"], email=data["email"])
        db.add(person)
        db.commit()
        db.refresh(person)
        return person
  
@app.put("/api/users")
def edit_person(data = Body(), db: Session = Depends(get_db)):
   
    # получаем пользователя по id
    person = db.query(User).filter(User.id == data["user_id"]).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None: 
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    person.login = data["login"]
    person.password = data["password"]
    person.email = data["email"]
    db.commit() # сохраняем изменения 
    db.refresh(person)
    return person
  
  
@app.delete("/api/users/{id}")
def delete_person(id, db: Session = Depends(get_db)):
    # получаем пользователя по id
    person = db.query(User).filter(User.id == id).first()
   
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse( status_code=404, content={ "message": "Пользователь не найден"})
   
    # если пользователь найден, удаляем его
    db.delete(person)  # удаляем объект
    db.commit()     # сохраняем изменения
    return person


class DisableCacheMiddleware(BaseHTTPMiddleware): #Отклчение хэширования
    async def dispatch(self, request, call_next):
        response = await call_next(request) #передает запрос дальше по цепочке, в конечную обработку или в другой middleware.
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0" #Устаревший пакет
        return response

app.add_middleware(DisableCacheMiddleware) #Добавление при каждом получениии app


# app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/static/{file_path:path}")
async def get_static(file_path: str, request: Request):
  full_path = os.path.join("static", file_path) #полный путь к файлу который лежит в static
  if not os.path.exists(full_path): # Проверка существования файла
    return Response(status_code=404)
  file_stat = os.stat(full_path) #Информация о файле
  last_modified = datetime.datetime.fromtimestamp(file_stat.st_mtime) #Время последнего изменения файла
  if_modified_since = request.headers.get("If-Modified-Since") # Если есть время последней отправки файла
  if if_modified_since:
    if_modified_since = datetime.datetime.strptime(if_modified_since, "%a, %d %b %Y %H:%M:%S GMT") #Время последнего запроса 
    if last_modified <= if_modified_since:
      return Response(status_code=304)
  response = FileResponse(full_path)
  response.headers["Last-Modified"] = last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT") # Время последнего изменения файла
  return response

templates = Jinja2Templates(directory="templates")