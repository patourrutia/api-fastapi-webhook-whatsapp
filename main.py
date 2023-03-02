from typing import Union
from fastapi import FastAPI
import os
from whatsapp_client import WhatsAppWrapper
import pymysql.cursors
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}