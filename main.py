from typing import Union
from fastapi import FastAPI, Request, Response
import requests
import json
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

    response = requests.request("POST", f"{API_URL}/messages", headers=headers, data=payload)
    
    assert  response.status_code == 200, "Error sending message"

    return  response.status_code

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
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        
        assert response.status_code == 200, "Error sending message"

        return response.status_code

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
    phone_number = "56952244429"
    url_image= "https://app.idealsoft.cloud/grammarbot.png"
    response =   await  send_message_image(
        phone_number=phone_number,
        url_image=url_image
    )
    response =   await send_message(        
                        message="👋Hola, soy tu asistente virtual, estoy aquí para ayudarte a practicar y mejorar tu inglés de forma fácil y divertida. Con MyGrammarBot🤖 podrás responder ejercicios💪 interactivos, practicar tu vocabulario y gramática.",
                        phone_number=phone_number
    )
    #print(data_json)
    # client = WhatsAppWrapper()
    # client.process_webhook_notification(data_json)
    # asyncio.run(client.process_webhook_notification(data_json))
    