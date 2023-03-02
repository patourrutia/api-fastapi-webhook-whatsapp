from typing import Union
from fastapi import FastAPI,jsonify, request

import os
from whatsapp_client import WhatsAppWrapper
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

HOOK_TOKEN = os.environ.get('WHATSAPP_HOOK_TOKEN')

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.route("/send_message_auto/")
def send_message_auto():
    # connection = pymysql.connect(host='localhost',
    #                         user='root',
    #                         password='root',
    #                         database='grammar_bot',
    #                         cursorclass=pymysql.cursors.DictCursor)
    connection = pymysql.connect(host='10.10.1.216',
                            user='root',
                            password='123456',
                            database='grammar_bot',
                            cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        
        sql = "SELECT * FROM user WHERE active = 1"
        cursor.execute(sql)
        result_user = cursor.fetchall()
        for i, dicc_user in enumerate(result_user):
            number_phone = dicc_user["number_phone"]
            id_user = dicc_user["id"]
            level = dicc_user["level"]
            status = dicc_user["status"]
            if(status=="REGISTERED"):
                print("ENVIO DE PLANTILLA PARA ACEPTAR RECIBIR MENSAJE")
            if(status=="ACCEPT_SEND"):
                print("ENVIO DE MENSJAES")
                

                sql = "SELECT count(id) as count FROM send_sentence WHERE id_user=%s AND id_sentence=%s"
                cursor.execute(sql,(id_user,level))
                result_count = cursor.fetchone()

                sql = "SELECT * from sentence where id= %s"
                cursor.execute(sql,(level))
                result_sentence = cursor.fetchall()
                for i, dicc_sentence in enumerate(result_sentence):
                    message = dicc_sentence["sentence"]
                    id_sentence = dicc_sentence["id"]
                    #print("ENVIAR SENTENCIAS")
                    if (int(result_count["count"])== int(0)):
                        sql = "INSERT INTO `send_sentence` (`id`, `id_user`, `id_sentence`,`fecha`, `status`) VALUES (NULL,%s , %s, CONCAT(CURRENT_DATE(),\" \",CURRENT_TIME()), %s);"
                        cursor.execute(sql, (id_user, id_sentence,"sent"))
                        connection.commit()
                    print(message)
                    sentence = message.split("|")
                    msg = '██▒▒▒▒▒▒▒▒▒▒\n *' + sentence[0] + '* 👌 '
                    for s in range(1,len(sentence)):
                        msg = msg + '\n👉 *' + sentence[s]
                    msg = msg + '\n_Choose the correct option *a*, *b* or *c*_ ✍'
                
                    message = msg
                    client = WhatsAppWrapper()
                    response = client.send_message(
                        message=message,
                        phone_number=number_phone,
                    )

    connection.close() 
    return  {
            "data": response,
            "status": "success",
        },200
        

   



@app.route("/send_template_message/", methods=["POST"])
def send_template_message():
    """_summary_: Send a message with a template to a phone number"""

    if "language_code" not in request.json:
        return jsonify({"error": "Missing language_code"}), 400

    if "phone_number" not in request.json:
        return jsonify({"error": "Missing phone_number"}), 400

    if "template_name" not in request.json:
        return jsonify({"error": "Missing template_name"}), 400

    client = WhatsAppWrapper()

    response = client.send_template_message(
        template_name=request.json["template_name"],
        language_code=request.json["language_code"],
        phone_number=request.json["phone_number"],
    )

    return  {
            "data": response,
            "status": "success",
        }, 200


@app.route("/send_message/", methods=["POST","GET"])
def send_message():

    if request.method == "GET":
        message=request.args.get('message')
        phone_number=request.args.get('phone_number')
        print(message)
        print(phone_number)

    else:
        if "message" not in request.json:
            return jsonify({"error": "Missing message"}), 400

        if "phone_number" not in request.json:
            return jsonify({"error": "Missing phone_number"}), 400
        
        message=request.json["message"]
        phone_number=request.json["phone_number"]
        
      



        sentence = message.split("|")
        msg = '██▒▒▒▒▒▒▒▒▒▒\n *' + sentence[0] + '* 👌 '
        for s in range(1,len(sentence)):
            msg = msg + '\n👉 *' + sentence[s]
        msg = msg + '\n_Choose the correct option *a*, *b* or *c*_ ✍'
       
       
        message = msg
        


    client = WhatsAppWrapper()

    response = client.send_message(
        message=message,
        phone_number=phone_number,
    )

    return {
            "data": response,
            "status": "success",
        }, 200


@app.route('/webhook/', methods=["POST", "GET"])
def verify():
   
    # webhook verification
    #print(HOOK_TOKEN)
    if request.method == "GET":
        if request.args.get('hub.verify_token') == HOOK_TOKEN:
            return request.args.get('hub.challenge')
        return "Authentication failed. Invalid Token."
    
    data_json = request.get_json()
    
    client = WhatsAppWrapper()
    response =  client.process_webhook_notification(data_json)
    return {"status": "success"}, 200 
