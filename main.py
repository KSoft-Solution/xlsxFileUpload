import time
import os
import pandas
import json
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from config.db import file_collection
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openpyxl


app = FastAPI()
templates = Jinja2Templates(directory="public")

origins = ['http://localhost:300']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/uploadfile")
def create_upload_file(file: UploadFile = File()):
    if not file:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        filename = file.filename
        readfile = pandas.read_excel(os.path.join(
            os.getcwd(), filename))
        docs = json.loads(readfile.T.to_json()).values()
        file_collection.insert_many(docs)
        return{
            "data": readfile.to_dict(orient='records')
        }
