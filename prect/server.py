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

#https://metanit.com/python/fastapi/2.1.php про бд

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


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