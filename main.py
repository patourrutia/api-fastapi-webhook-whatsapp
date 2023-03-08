from typing import Union
from fastapi import FastAPI, Request, Response
import requests
import json

from google.cloud import translate_v2 as translate

import openai
import random
import datetime, time
import requests_async as requestsasc
# import asyncio




import os
from whatsapp_client import WhatsAppWrapper
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

HOOK_TOKEN = os.environ.get('WHATSAPP_HOOK_TOKEN')

app = FastAPI()


API_URL = "https://graph.facebook.com/v15.0/"

API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
NUMBER_ID = os.environ.get("WHATSAPP_NUMBER_ID")

ARCHIVO_JSON =  os.environ.get('ARCHIVO_JSON_GOOGLE')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= ARCHIVO_JSON

headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
}
API_URL = API_URL + NUMBER_ID

def send_message(message, phone_number):

    payload =  json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    })
    requests.request("POST", f"{API_URL}/messages", headers=headers, data=payload)
    
 
    # response =   requests.request("POST", f"{API_URL}/messages", headers=headers, data=payload)
    
    # assert  response.status_code == 200, "Error sending message"

    # return  response.status_code

def send_message_image( phone_number,url_image):
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "image",
            "image": {
                "link": url_image
            }
        })
        requests.request("POST", f"{API_URL}/messages", headers=headers, data=payload)
        

        # response =   requests.request("POST", f"{API_URL}/messages", headers=headers, data=payload)
        
        # assert response.status_code == 200, "Error sending message"

        # return response.status_code

@app.get("/")
def read_root():
    print("hola")
    return {"Hello": "World"}


@app.get("/webhook/")
def verify(request: Request):
    if request.query_params['hub.verify_token'] == HOOK_TOKEN:
        return Response(content=request.query_params["hub.challenge"])
        #return request.query_params['hub.challenge']
    return "Authentication failed. Invalid Token."



@app.post("/webhook/")
async def verify(request: Request):
    data_json = await request.json()
    print(data_json)

    response = []
    changes =   data_json['entry'][0]['changes'][0]['value']
    print(changes)
    connection = pymysql.connect(host='10.10.1.216',
    user='root',
    password='123456',
    database='grammar_bot',
    cursorclass=pymysql.cursors.DictCursor)
    
    print(changes)
    messages =   changes.get("messages")
    if messages:
        phone_number = "56952244429"
        url_image= "https://app.idealsoft.cloud/grammarbot.png"
        send_message_image(
            phone_number=phone_number,
            url_image=url_image
        )
        # print("image" + str(response))

        send_message(        
                            message="👋Hola, soy tu asistente virtual, estoy aquí para ayudarte a practicar y mejorar tu inglés de forma fácil y divertida. Con MyGrammarBot🤖 podrás responder ejercicios💪 interactivos, practicar tu vocabulario y gramática.",
                            phone_number=phone_number
        )
        # print("saludo" + str(response))
    #print(data_json)
    # client = WhatsAppWrapper()
    # client.process_webhook_notification(data_json)
    # asyncio.run(client.process_webhook_notification(data_json))
    