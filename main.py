from typing import Union
from fastapi import FastAPI, Request, Response



import os
from whatsapp_client import WhatsAppWrapper
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

HOOK_TOKEN = os.environ.get('WHATSAPP_HOOK_TOKEN')

app = FastAPI()


@app.get("/")
async def read_root():
    print("hola")
    return {"Hello": "World"}


@app.get("/webhook/")
async def verify(request: Request):
    if request.query_params['hub.verify_token'] == HOOK_TOKEN:
        return Response(content=request.query_params["hub.challenge"])
        #return request.query_params['hub.challenge']
    return "Authentication failed. Invalid Token."

@app.post("/webhook/")
def verify(request: Request):
    data_json = request.json()
    client = WhatsAppWrapper()
    response =  client.process_webhook_notification(data_json)
    