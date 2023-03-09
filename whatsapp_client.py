import os
import requests
import json
import pymysql.cursors
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv
import openai
import random
import datetime, time
import requests_async 



load_dotenv()

def call_gpt(preg):
    KEY_CHATGPT =  os.environ.get('KEY_CHATGPT')
    openai.api_key=KEY_CHATGPT
    try:
        completion = openai.Completion.create(engine="text-davinci-003",
                                            prompt=preg,
                                            max_tokens=2048)
        respuesta = completion.choices[0].text
        return respuesta
    except openai.error.Timeout as e:
        #Handle timeout error, e.g. retry or log
        print(f"OpenAI API request timed out: {e}")
        pass
    except openai.error.APIError as e:
    #Handle API error, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
    #Handle connection error, e.g. check network or log
        print(f"OpenAI API request failed to connect: {e}")
        pass
    except openai.error.InvalidRequestError as e:
    #Handle invalid request error, e.g. validate parameters or log
        print(f"OpenAI API request was invalid: {e}")
        pass
    except openai.error.AuthenticationError as e:
    #Handle authentication error, e.g. check credentials or log
        print(f"OpenAI API request was not authorized: {e}")
        pass
    except openai.error.PermissionError as e:
        #Handle permission error, e.g. check scope or log
        print(f"OpenAI API request was not permitted: {e}")
        pass
    except openai.error.RateLimitError as e:
        #Handle rate limit error, e.g. wait or log
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
def revisa_contrnido(contenido):
    API_URL = "https://api.openai.com/v1/moderations"
    KEY_CHATGPT = os.environ.get("KEY_CHATGPT")
    headers = {
        "Authorization": f"Bearer {KEY_CHATGPT}",
        "Content-Type": "application/json"
    }
    payload = json.dumps({"input": contenido})
    response = requests.request("POST", f"{API_URL}", headers=headers, data=payload)
    assert response.status_code == 200, "Error sending message"
    data_json  = json.loads(response.text) 
    hate =data_json['results'][0]['categories']['hate']
    threatening = data_json['results'][0]['categories']['hate/threatening']
    self_harm = data_json['results'][0]['categories']['self-harm']
    sexual = data_json['results'][0]['categories']['sexual']
    sexual_minors = data_json['results'][0]['categories']['sexual/minors']
    violence = data_json['results'][0]['categories']['violence']
    violence_graphic= data_json['results'][0]['categories']['violence/graphic']
    if (hate or threatening or self_harm or sexual or sexual_minors or violence or violence_graphic):
        return False
    else:
        return True
def envia_ultima_sentencia(curs,lev,number):
   
    sql = "SELECT sentence,correct_option, complete_sentence,traslate_sentence FROM sentence WHERE id=%s"
    curs.execute(sql,(lev))
    result_sentence= curs.fetchone()
    #correct_option = result_sentence["correct_option"].split("|")
    traslate_sentence = result_sentence["traslate_sentence"]
    sentence_actual = result_sentence["sentence"]
    message=sentence_actual
    sentence = message.split("|")
    msg = '*N' + sentence[0] + '* \n '
    for s in range(1,len(sentence)):
        msg = msg + '\n👉 *' + sentence[s]              
    message = msg + "\n"  
        
    client = WhatsAppWrapper()   
    client.send_message2(
        message=message,
        phone_number=number,
        trans =traslate_sentence
    )



def msgayuda():
    msg ="✨*Funciones*✨\n"
    msg = msg + "———————————\n"
    msg = msg + "☑️Traducir a Español\n"
    msg = msg + "      Ej: How are you🇪🇸\n"
    msg = msg + "☑️Traducir a Ingles\n"
    msg = msg + "      Ej:Buen trabajo🇺🇸\n"
    msg = msg + "☑️Ir a un nivel\n"  
    msg = msg + "      Ej: N5 (Va al nivel 5)\n"
    msg = msg + "☑️Ver Top 10: T\n"  
    msg = msg + "☑️Ver Funciones: F \n"
    

    # msg = msg + "Si tienes dudas o consultas las puedes hacer al WhatsApp: +56926249071"
    return msg

def almacena_respuestas(msg,type,idus,cur,con):
    msg = msg
    id_type_msg = type
    id_user = idus
    date_actual = datetime.datetime.now()
    mydate_time = date_actual.strftime("%Y-%m-%d %H:%M:00")
    mydate = date_actual.strftime("%Y-%m-%d")
    mytime = date_actual.strftime("%H:%M:%S")
    sql = "INSERT INTO `message_from_client` (`id`, `message`, `id_type_msg`, `id_user`, `fecha_time`, `fecha`, `time`) VALUES (NULL, '{var1}', {var2}, {var3}, '{var4}', '{var5}', '{var6}');".format(var1=str(msg),var2=id_type_msg,var3=id_user,var4=str(mydate_time),var5=str(mydate),var6=str(mytime))
    cur.execute(sql)
    con.commit()

def almacena_envio_msg(msg,status,idus,cur,con):
    id_user = idus

    sql = "SELECT id FROM message_last_to_client WHERE id_user=%s "
    cur.execute(sql,(id_user))
    result_user= cur.fetchone()
    if(cur.rowcount==0):
        msg = msg
        status = status

        date_actual = datetime.datetime.now()
        mydate_time = date_actual.strftime("%Y-%m-%d %H:%M:00")
        mydate = date_actual.strftime("%Y-%m-%d")
        mytime = date_actual.strftime("%H:%M:%S")
        sql = "INSERT INTO `message_last_to_client` (`id`, `message`, `status`, `id_user`, `fecha_time`, `fecha`, `time`) VALUES (NULL, '{var1}','{var2}', {var3}, '{var4}', '{var5}', '{var6}');".format(var1=str(msg),var2=status,var3=id_user,var4=str(mydate_time),var5=str(mydate),var6=str(mytime))
        cur.execute(sql)
        con.commit()
        



class WhatsAppWrapper:
    API_URL = "https://graph.facebook.com/v15.0/"

    API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
    NUMBER_ID = os.environ.get("WHATSAPP_NUMBER_ID")

    ARCHIVO_JSON =  os.environ.get('ARCHIVO_JSON_GOOGLE')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= ARCHIVO_JSON

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json"
        }
        self.API_URL = self.API_URL + self.NUMBER_ID

  


    def send_template_message(self, template_name, phone_number):

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "es"
                }
            }
        })

        requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        # response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        
        # assert response.status_code == 200, "Error sending message"

        # return response.status_code
    

    def send_message2(self, message, phone_number,trans):

      
    
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": "██▒▒▒▒▒▒▒▒▒▒ "
                },
            
                "body": {
                    "text": message
                },
                "footer": {
                    "text": "\nChoose the correct option"
                },
                "action": {
                    "button": "Translate",
                    "sections": [
                        {
                            "title": " ",
                            "rows": [
                                {
                                    "id": "1",
                                    "title": " ",
                                    "description": trans
                                }
                            ]
                        }
                    ]
                }
            }
        })

        requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)

        # response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        
        # assert response.status_code == 200, "Error sending message"

        # return response.status_code
    


    async def send_message_image(self,  phone_number,url_image):
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "image",
            "image": {
                "link": url_image
            }
        })

       
        response = await requests_async.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        
        assert response.status_code == 200, "Error sending message"

        return response.status_code
    def send_message_video(self,  phone_number,body):
        payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {
            "preview_url": True,
            "body": body
            }
        })
        requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        # response =  requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        
        # assert response.status_code == 200, "Error sending message"

        # return response.status_code
    def send_message_reply(self,idmsg,phone_number, message ):

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "context": {
                "message_id": str(idmsg)
            },
            "type": "text",
            "text": {
                "preview_url": False,
                "body": str(message)
            }
        })
        requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        # response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        
        # assert response.status_code == 200, "Error sending message"

        # return response.status_code
    
   
    def send_message(self, message, phone_number):

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
        requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        # response =  requests_async.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        
        # assert  response.status_code == 200, "Error sending message"

        # return  response.status_code
    

    

    
    
    async def process_webhook_notification(self, data):
        response = []
        changes =   data['entry'][0]['changes'][0]['value']
        print(changes)
        connection = pymysql.connect(host='10.10.1.216',
        user='root',
        password='123456',
        database='grammar_bot',
        cursorclass=pymysql.cursors.DictCursor)
        
        print(changes)
        messages =   changes.get("messages")
        if messages:
            phone_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            from_name = data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']   
            idmsg = data['entry'][0]['changes'][0]['value']['messages'][0]['id']
            #print(messages)
            #print (phone_number + " - " + from_name )
            if (data['entry'][0]['changes'][0]['value']['messages'][0]['type']=="text"):
                #print (data_json['entry'][0]['changes'][0]['value']['messages'][0]['type'])
                respuesta_cliente =data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

                respuesta_cliente_normal =respuesta_cliente
                text = respuesta_cliente
                #print(respuesta_cliente_normal)
                respuesta_cliente = respuesta_cliente.lower()
                len_respuesta_cliente = len(respuesta_cliente)
                len_respuesta_cliente_normal = len(respuesta_cliente_normal)
                #print(len_respuesta_cliente_normal)
                phone_admin = 56926249071
                #print(str(len(respuesta_cliente)) + respuesta_cliente)
                #if(revisa_contrnido(respuesta_cliente)):
                #    print("Cliente responde :" + respuesta_cliente + " RESPUESTA VALIDA")
                #else:
                #    print("Cliente responde :" + respuesta_cliente + " RESPUESTA NO VALIDA")   
      
                with connection.cursor() as cursor:
                    sql = "SELECT id,level,modo, status,date_expired,pais,maxlevel FROM user WHERE number_phone=%s AND active = 1"
                    cursor.execute(sql,(phone_number))
                    result_user= cursor.fetchone()
                    client = WhatsAppWrapper()

                    if(cursor.rowcount==1):
                        id_user = result_user["id"]
                        level = result_user["level"] 
                        modo = result_user["modo"] 
                        status = result_user["status"]
                        date_expired  = result_user["date_expired"]
                        elpais  = result_user["pais"]
                        maxlevel  = result_user["maxlevel"]
                        date_actual = datetime.datetime.now()   
                        date_last_conexion = date_actual.strftime("%Y-%m-%d %H:%M:%S")
                        sql = "UPDATE user SET  date_last_conexion='{var1}'  WHERE id={var2}".format( var1=str(date_last_conexion), var2=str(id_user))   
                        cursor.execute(sql)
                        connection.commit()


                        opcion = ""
                        data_respuesta = ""
                        if (modo==4):
                            #pagar  mensaje_no_valido
                            if((len(text)>=4)):
                                if((text[0:5].lower()=="pagar")):
                                    data_respuesta = text[5:]  
                                    opcion ="pagar"
                                    #print("Pagar")
                                    #print(data_respuesta)
                                elif((text[0:17].lower()=="mensaje_no_valido")):
                                    opcion ="mensaje_no_valido"
                                    data_respuesta = text[17:]
                                    #print("mensaje_no_valido")
                                    #print(data_respuesta)
                                else:
                                    #NO HACE NADA
                                    pass
                                    #print("#NO HACE NADA")
                        else:
                            if ((len(text)== 1) and (modo==1 or modo==3)):
                                if((text.lower()=="f") ) and (modo==1 or modo==3):
                                    opcion="f"
                                    #print("F")
                                elif((text.lower()=="t" )and (modo==1 or modo==3)):
                                    opcion="t"
                                    #print("T")
                                else:
                                    #NO HACE NADA
                                    pass
                                    #print("#NO HACE NADA")

                            elif(len(text)==2):
                                if((text[0:1].lower()=="n" ) and (modo==1 or modo==3)):
                                    if (text[1:].replace(" ","").isnumeric()):
                                        data_respuesta = text[1:].replace(" ","")
                                        opcion="nivel"
                                    else:
                                        #NO HACE NADA
                                        opcion="nivel_no_numeric"
                                        pass
                                        #print("MALO NO ES NUMERICO")
                                else:
                                    #NO HACE NADA
                                    pass
                                    #print("#NO HACE NADA")
                            elif(len(text)==3):
                                if((text[0:1].lower()=="n" ) and (modo==1 or modo==3)):
                                    if (text[1:].replace(" ","").isnumeric()):
                                        data_respuesta = text[1:].replace(" ","")
                                        opcion="nivel"        
                                    else:
                                        #NO HACE NADA
                                        opcion="nivel_no_numeric"
                                        pass
                                        #print("MALO NO ES NUMERICO")
                                else:
                                    #NO HACE NADA
                                    pass
                                    #print("#NO HACE NADA")

                            elif(len(text)>=4):
                                if((text[0:1].lower()=="n") and (modo==1 or modo==3)):
                                    if (text[1:].replace(" ","").isnumeric()):
                                        
                                        data_respuesta = text[1:].replace(" ","")  
                                        if (int(data_respuesta)<=15805):
                                            opcion="nivel"
                                            #print("Es Numero")
                                        else:
                                            #NO HACE NADA
                                            opcion="no_permitido_mayor_15805"
                                            pass
                                            #print("#NO HACE NADA")
                                        
                                    else:
                                        if((text[-2]=='🇺') and (modo==1 or modo==3)):
                                            opcion="trad_ing"
                                            data_respuesta = text[:-2]
                                            #print("TRADUCCION A INGLES")
                                        elif((text[-2]=='🇪' ) and (modo==1 or modo==3)):
                                            opcion="trad_esp"
                                            data_respuesta = text[:-2]
                                            #print("TRADUCCION A ESPAÑOL")
                                        else:
                                            #NO HACE NADA
                                            pass
                                            #print("#NO HACE NADA")

                                elif((text[0:3].lower()=="bot") and (modo==2 or modo==3)):
                                    data_respuesta = text[4:]  
                                    opcion="usar_bot"
                                
                                elif((text[-2]=='🇺') and (modo==1 or modo==3)):
                                    opcion="trad_ing"
                                    data_respuesta = text[:-2]
                                    #print("TRADUCCION A INGLES")
                                
                                elif((text[-2]=='🇪') and (modo==1 or modo==3)):
                                    opcion="trad_esp"
                                    data_respuesta = text[:-2]    
                                    #print("TRADUCCION A ESPAÑOL")
                                else:
                                    #NO HACE NADA
                                    pass
                                    #print("#NO HACE NADA")
   


                        email= ""
                        pais= ""
                        if (status==1):
                            # TYPE 2
                            ingreso_data  = respuesta_cliente.split(",")
                            if (len(ingreso_data)==2):
                                nombre = ingreso_data[0]
                                pais= ingreso_data[1]
                            
                            elif(len(ingreso_data)>=3):
                                nombre = ingreso_data[0]
                                pais   = ingreso_data[1]
                                email  = ingreso_data[2]
                            else:
                                nombre= respuesta_cliente
                                
                            ahora = datetime.datetime.now()
                            manana = ahora + datetime.timedelta(days=1)
                            date_expired = manana.strftime("%Y-%m-%d %H:%M:%S")                            
                            date_actual = datetime.datetime.now()   
                            date_last_conexion = date_actual.strftime("%Y-%m-%d %H:%M:%S")
                            sql = "UPDATE user SET status=2, name='{var1}', pais='{var2}', email='{var3}', date_expired='{var4}', date_last_conexion='{var5}'  WHERE id={var6}".format(var1=str(nombre), var2=str(pais),var3=str(email), var4=str(date_expired), var5=str(date_last_conexion), var6=str(id_user))   
                            cursor.execute(sql)
                            connection.commit()
                            
                            client.send_message(        
                                message="El registro fue éxitoso, recuerda que desde este momento se activará tu periodo de prueba de un día. Si tienes dudas o consultas las puedes hacer al WhatsApp: +56926249071 o al e-mail: mygrammarbot@gmail.com",
                                phone_number=phone_number,
                            )
                            client.send_message(        
                                message="¡Vamos a empezar con los ejercicios interactivos de gramática! ¡Ponte cómodo y comencemos!💪¡Good luck!👋. ",
                                phone_number=phone_number,
                            )
                            
                            msg = msgayuda()
                            client.send_message(        
                                message=msg,
                                phone_number=phone_number,
                            )
                            #time.sleep(10)
                            envia_ultima_sentencia(cursor,level,phone_number)
                            almacena_respuestas(respuesta_cliente_normal,2,id_user,cursor,connection)
                        elif(status== 2 or status== 3 ):
                            date_actual = datetime.datetime.now()              
                            date_expired = datetime.datetime.strptime(str(date_expired), '%Y-%m-%d %H:%M:%S')
                            if (date_actual<=date_expired):
                                #USUARIO PERMITO PARA UTILIZAR EL SERVICIO DE MENSAJERIA
                                sql = "SELECT sentence,correct_option, complete_sentence,traslate_sentence FROM sentence WHERE id=%s"
                                cursor.execute(sql,(level))
                                result_sentence= cursor.fetchone()
                                correct_option = result_sentence["correct_option"].split("|")
                                # traslate_sentence = result_sentence["traslate_sentence"]
                                # sentence_actual = result_sentence["sentence"]

                                if(opcion =='mensaje_no_valido'):
                                    # TYPE 3
                                    data = data_respuesta.split("-")
                                    idmsg=data[1]
                                    phone=data[2]
                                    message=data[5]
                                    

                                    sql = "SELECT id,level,modo, status,date_expired,pais FROM user WHERE number_phone=%s AND active = 1"
                                    cursor.execute(sql,(phone))
                                    result_user= cursor.fetchone()
                                    

                                    if(cursor.rowcount==1):
                                        id_user2 = result_user["id"]
                                        status = result_user["status"]
                                        level = result_user["level"]
                                        
                                        client.send_message_reply(    
                                            idmsg=idmsg,
                                            phone_number=phone,  
                                            message=message
                                            
                                        )
                                        #print("mensaje_no_valido" + response)
                                     
                                        client.send_message(        
                                            message="MENSAJE RESPONDIDO",
                                            phone_number=phone_number
                                        )

                                        envia_ultima_sentencia(cursor,level,phone)
                                        almacena_respuestas(respuesta_cliente_normal,3,id_user,cursor,connection)

                                    else:
                                        client.send_message(        
                                            message="ERROR- USUARIO NO REGISTRADO",
                                            phone_number=phone_number
                                        )
                                elif(opcion =='pagar'):
                                    
                                    #print("PAGAR " + data_opcion_pagar) # TYPE 4
                                    data_respuesta = data_respuesta.replace("+","")
                                    data_respuesta = data_respuesta.replace(" ","")
                                    

                                    sql = "SELECT id,level,modo, status,date_expired,pais FROM user WHERE number_phone=%s AND active = 1"
                                    cursor.execute(sql,(data_respuesta))
                                    result_user= cursor.fetchone()
                                    

                                    if(cursor.rowcount==1):
                                        id_user2 = result_user["id"]
                                        status = result_user["status"]
                                        level = result_user["level"]
                                        
                                        date_actual = datetime.datetime.now()
                                        date_expired = date_actual + datetime.timedelta(days=30)
                                        date_expired = date_expired.strftime("%Y-%m-%d %H:%M:%S")  

                                        date_paid = date_actual.strftime("%Y-%m-%d %H:%M:%S")
                                        sql = "UPDATE user SET status=3, date_paid='{var1}' , date_expired='{var2}' WHERE id={var3}".format( var1=str(date_paid),  var2=str(date_expired), var3=str(id_user2))   
                                        cursor.execute(sql)
                                        connection.commit()

                                        client.send_message(        
                                            message="PAGO ACEPTADO",
                                            phone_number=phone_number
                                        )
                                        client.send_message(        
                                            message="Pago aceptado, puedes seguir disfrutando nuestro servicio",
                                            phone_number=data_respuesta
                                        )
                                        envia_ultima_sentencia(cursor,level,data_respuesta)
                                        almacena_respuestas(respuesta_cliente_normal,4,id_user,cursor,connection)

                                    else:
                                        client.send_message(        
                                            message="ERROR- USUARIO NO REGISTRADO",
                                            phone_number=phone_number
                                        )
                                elif((opcion =='nivel_no_numeric')) :
                                    #TYPE 5
                                    msg = "El nivel ingresado({var1}) no es un numero".format(var1=str(data_respuesta))
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_number
                                    )
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,5,id_user,cursor,connection)
                                elif((opcion =='no_permitido_mayor_15805')) :
                                    #TYPE 5
                                    msg = "El nivel ingresado({var1}) debe ser menor a 15805".format(var1=str(data_respuesta))
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_number
                                    )
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,5,id_user,cursor,connection)

                                elif((opcion =='nivel') ) :
                                   # TYPE 5
                                    if(int(data_respuesta)<=int(maxlevel)):
                                        sql = "UPDATE user SET level= %s  WHERE id=%s" 
                                        cursor.execute(sql, (data_respuesta,id_user))
                                        connection.commit()
                                        envia_ultima_sentencia(cursor,data_respuesta,phone_number)
                                    
                                    else:
                                        msg = "El nivel ingresado es N{var1}, no debe ser mayor a el maximo obtenido, su nivel maximo obtenido es {var2}".format(var1=str(data_respuesta),var2=str(level))
                                        client.send_message(        
                                            message=msg,
                                            phone_number=phone_number
                                        )

                                        envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,5,id_user,cursor,connection)

   

                                elif((opcion =='f' )) : 
                                    # TYPE 6            
                                    msg = msgayuda()  
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_number,
                                    )
                                    almacena_respuestas(respuesta_cliente_normal,6,id_user,cursor,connection) 
                                    envia_ultima_sentencia(cursor,level,phone_number)
         
                                elif((opcion =='t')) :
                                    # TYPE 8
                                    sql = "SELECT name_whatsapp FROM user ORDER BY level desc limit 10"
                                    cursor.execute(sql)
                                    result_sentence = cursor.fetchall()
                                    msg= " Top 10 🏆\n"
                                    for  i, dicc_sentence in enumerate(result_sentence):
                                        name_whatsapp = dicc_sentence["name_whatsapp"]
                                        msg= msg + "\n🏆 "+ str(int(i) +1 )  + ".-" +name_whatsapp
                                 
                                    
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_number,
                                    )
                                    
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,8,id_user,cursor,connection)
                                elif((opcion =='usar_bot') and (modo==2 or modo==3)) :
                                    pregunta = data_respuesta
                                    #print("OPCION CHATGPT Y USARIO PREGUNTA:" + pregunta) TYPE 9
         
                                    respuesta_bot = call_gpt(pregunta)
                                    
                                    client.send_message(        
                                    message=respuesta_bot,
                                    phone_number=phone_number,
                                    )
                                    if (modo==3):
                                        
                                        envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,9,id_user,cursor,connection)
                            
                                elif((opcion=="trad_ing")):
                                    #print("OPCION TRADUCCION AL INGLES")TYPE 10
                                    text_traducir = data_respuesta
                                    code_trans = "en"
                                    traductor = translate.Client()
                                    texto_traducido = traductor.translate(text_traducir,code_trans)                 
                                    client.send_message(        
                                        message=texto_traducido["translatedText"].replace("&#39;","'"),
                                        phone_number=phone_number,
                                    )
                                    sql = "INSERT INTO `message_traducido` (`id`, `code_lang`,  `message_original`, `message_traducido`,`fecha`,`id_user`) VALUES (NULL,%s ,%s,%s, CONCAT(CURRENT_DATE(),\" \",CURRENT_TIME()), %s);"
                                    cursor.execute(sql, (code_trans,text_traducir,texto_traducido["translatedText"].replace("&#39;","'"),id_user))
                                    connection.commit()
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,10,id_user,cursor,connection)
                            
                                elif( (opcion=="trad_esp")):
                                    #print("OPCION TRADUCCION AL ESPAÑOL")  TYPE 11                   
                                    text_traducir = data_respuesta
                                    code_trans = "es"
                                    traductor = translate.Client()
                                    texto_traducido = traductor.translate(text_traducir,code_trans)
                                    
                                    client.send_message(        
                                    message=texto_traducido["translatedText"].replace("&#39;","'"),
                                    phone_number=phone_number,
                                    )     
                                    sql = "INSERT INTO `message_traducido` (`id`, `code_lang`,  `message_original`, `message_traducido`,`fecha`,`id_user`) VALUES (NULL,%s ,%s,%s, CONCAT(CURRENT_DATE(),\" \",CURRENT_TIME()), %s);"
                                    cursor.execute(sql, (code_trans,text_traducir,texto_traducido["translatedText"].replace("&#39;","'"),id_user))
                                    connection.commit()
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,11,id_user,cursor,connection)

                                elif((respuesta_cliente==correct_option[0]  or respuesta_cliente==correct_option[1]) and (modo==1 or modo==3)):
                                    #print("OPCION SENTENCE RESPUESTA CORRECTA") TYPE 12
                                    random_number = random.randint(1,20)
                                    sql = "SELECT message FROM message_respuestas_correcto WHERE active= 1 and id=%s"
                                    cursor.execute(sql,(random_number))
                                    result_message1 = cursor.fetchone()
                                    message_correcto = result_message1["message"]
                                                                    
                                    client.send_message(        
                                        message=message_correcto,
                                        phone_number=phone_number,
                                    )

                                    if (int(level)%25==0):
                                        sql = "SELECT name_whatsapp FROM user ORDER BY level desc limit 10"
                                        cursor.execute(sql)
                                        result_sentence = cursor.fetchall()
                                        msg= " Top 10 🏆\n"
                                        for  i, dicc_sentence in enumerate(result_sentence):
                                            name_whatsapp = dicc_sentence["name_whatsapp"]
                                            msg= msg + "\n🏆 "+ str(int(i) +1 )  + ".-" +name_whatsapp
                              
                                        client.send_message(        
                                            message=msg,
                                            phone_number=phone_number,
                                        )

                                    if (int(level)== int(maxlevel)):   
                                        sql = "UPDATE user SET level= level +1, maxlevel= maxlevel +1   WHERE id=%s" 
                                        cursor.execute(sql, (id_user))
                                        connection.commit()
                                    else:
                                        sql = "UPDATE user SET level= level +1  WHERE id=%s" 
                                        cursor.execute(sql, (id_user))
                                        connection.commit()
                                    level_entero = int(level) + 1
                                    envia_ultima_sentencia(cursor,str(level_entero),phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,12,id_user,cursor,connection)
                                elif((respuesta_cliente =="a" or  respuesta_cliente=="b" or respuesta_cliente=="c"  or respuesta_cliente=="d" or respuesta_cliente=="e") and (modo==1 or modo==3) ):
                                    #print("OPCION SENTENCE RESPUESTA INCORRECTA") TYPE 13
                                    random_number = random.randint(1,20)
                                    sql = "SELECT * FROM message_respuestas_incorrecto WHERE active= 1 and id=%s"
                                    cursor.execute(sql,(random_number))
                                    result_message2 = cursor.fetchone()
                                    message_incorrecto = result_message2["message"]
                                    client.send_message(        
                                        message=message_incorrecto,
                                        phone_number=phone_number,
                                    )       
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,13,id_user,cursor,connection)
                  
                                elif ((modo==1 or modo==3) and (opcion !='usar_bot') ):
                                    #print("OPCION SENTENCE RESPUESTA NOVALIDA") TYPE 14
                                    msg = "MENSAJE_NO_VALIDO - "+str(idmsg) +"-" +phone_number + " - "+ from_name +" - " + respuesta_cliente          
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_admin,
                                    )
                                    client.send_message(        
                                        message="Lo siento, la opción elejida no es válida.",
                                        phone_number=phone_number,
                                    )
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,14,id_user,cursor,connection)
                                
                                else:
                                    #OTRA OPCION QUE NO ESTA DEFINIDA DENTRO DE LAS FUNCIONES TYPE 15
                                    #print("OTRA OPCION QUE NO ESTA DEFINIDA DENTRO DE LAS FUNCIONES ")
                                    #envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,15,id_user,cursor,connection)
                                    pass
                            else:
                                if (status== 2):
                                    #PERIDO GRATUITO EXPIRADO TYPE 16
                                    sql = "UPDATE user SET status= 4  WHERE id=%s" 
                                    cursor.execute(sql, (id_user))
                                    connection.commit()
                                    client.send_message(        
                                        message="¡Hola! 👋.. El periodo gratuito ha finalizado. Si desea continuar disfrutando de nuestro servicio, le sugerimos comunicarse por WhatsApp al: +56926249071 o pincha aquí  👉 https://api.whatsapp.com/send?phone=56926249071&text=Hola%20soy%20de%20"+ elpais +",%20quiero%20conocer%20el%20valor%20y%20las%20formas%20de%20pago%20para%20seguir%20utilizando%20MyGrammarBot .",
                                        phone_number=phone_number
                                    )
                                    almacena_respuestas(respuesta_cliente_normal,16,id_user,cursor,connection)
                                elif(status== 3):
                                    #PERIDO PAGADO EXPIRADO  TYPE 17
                                    client.send_message(        
                                        message="¡Hola! 👋.. El periodo de su succripcion a finalizado. Si desea continuar disfrutando de nuestro servicio, le sugerimos comunicarse por WhatsApp  al: +56926249071 o pincha aquí  👉 https://api.whatsapp.com/send?phone=56926249071&text=Hola%20soy%20de%20"+ elpais +",%20quiero%20conocer%20el%20valor%20y%20las%20formas%20de%20pago%20para%20seguir%20utilizando%20MyGrammarBot .",
                                        phone_number=phone_number
                                    )
                                    sql = "UPDATE user SET status= 5  WHERE id=%s" 
                                    cursor.execute(sql, (id_user))
                                    connection.commit()
                                    almacena_respuestas(respuesta_cliente_normal,17,id_user,cursor,connection)
                                else:
                                    pass
                        elif(status== 4 ):
                           #OTRO ESTADO 4  TYPE 18
                            client.send_message(        
                                    message="¡Hola! 👋.. El periodo gratuito ha finalizado. Si desea continuar disfrutando de nuestro servicio, le sugerimos comunicarse por WhatsApp al: +56926249071 o pincha aquí  👉 https://api.whatsapp.com/send?phone=56926249071&text=Hola%20soy%20de%20"+ elpais +",%20quiero%20conocer%20el%20valor%20y%20las%20formas%20de%20pago%20para%20seguir%20utilizando%20MyGrammarBot .",
                                    phone_number=phone_number
                                )
                            almacena_respuestas(respuesta_cliente_normal,18,id_user,cursor,connection)
                          
                        elif(status== 5 ):
                            #OTRO ESTADO 5  TYPE 19
                            client.send_message(        
                                        message="¡Hola! 👋.. El periodo de su succripcion a finalizado. Si desea continuar disfrutando de nuestro servicio, le sugerimos comunicarse por WhatsApp al: +56926249071 o pincha aquí  👉 https://api.whatsapp.com/send?phone=56926249071&text=Hola%20soy%20de%20"+ elpais +",%20quiero%20conocer%20el%20valor%20y%20las%20formas%20de%20pago%20para%20seguir%20utilizando%20MyGrammarBot .",
                                        phone_number=phone_number
                            )
                            almacena_respuestas(respuesta_cliente_normal,19,id_user,cursor,connection)

                    else:
                        #CUANDO NO ESTA REGISTRADO EL CLIENTE
                        sql = "SELECT id,level,modo, status,active FROM user WHERE number_phone=%s"
                        cursor.execute(sql,(phone_number))
                        result_user= cursor.fetchone()
                        if(cursor.rowcount==1):
                            pass
                            #print("USUARIO INACTIVO")

                        else:
                             # TYPE 1
                            id_user  = 1
                            almacena_respuestas(respuesta_cliente_normal,1,id_user,cursor,connection)
                            msg = "USUARIO INTENTANDO CHATIAR SIN ESTAR REGISTRADO - " + phone_number + " - " + from_name + " - " + respuesta_cliente
                            
                            client.send_message(    
                                    message=msg,
                                    phone_number=phone_admin
                                )
                            almacena_envio_msg(msg,"send",id_user,cursor,connection)
                        
                            client.send_message(        
                                message="👋Hola, soy tu asistente virtual, estoy aquí para ayudarte a practicar y mejorar tu inglés de forma fácil y divertida. Con MyGrammarBot🤖 podrás responder ejercicios💪 interactivos, practicar tu vocabulario y gramática.",
                                phone_number=phone_number
                            )


                            url_image= "https://app.idealsoft.cloud/grammarbot.png"
                            response =   await  client.send_message_image(
                              phone_number=phone_number,
                              url_image=url_image
                            )

                            client.send_message(        
                                message="✨ Modo Grammar: el usuario puede enviar repuestas para completar oraciones gramaticalmente correcta.",
                                phone_number=phone_number
                            )
    
                            client.send_message_video(  
                                phone_number=phone_number,
                                body ="✨Visita el siguiente link para ver el funcionamiento  del modo Grammar👉 https://www.youtube.com/watch?v=E-84QJFcpxQ"

                            )

                            client.send_message(        
                                message="✨Te invito a registrarte para poder acceder a nuestro servicio en forma gratuita por un día. ",
                                phone_number=phone_number
                            )
                           

                            # response = client.send_message(        
                            #     message="✨Registrarse es muy fácil, solo necesito algunos datos sobre ti. ¿Podrías proporcionarme tu nombre, el país y tu email. Ejemplo 👉: alexis,chile,alexis@gmail.com",
                            #     phone_number=phone_number
                            # )
                        
                            date_actual = datetime.datetime.now()   
                            date_last_conexion = date_actual.strftime("%Y-%m-%d %H:%M:%S")
                            date_created = date_actual.strftime("%Y-%m-%d %H:%M:%S")
                            sql = """INSERT INTO `user` (`id`, `name_whatsapp`, `name`, `email`, `number_phone`, `pais`, `level`, `status`, `maxlevel`, `modo` ,`date_expired`,`date_paid` ,`date_last_conexion`,`date_created`, `active`) 
                            VALUES (NULL,'{var1}', '{var1}',NULL,'{var2}', NULL, 1, 1, 1, 1, NULL, NULL, '{var3}','{var4}' , 1);
                            """.format(var1=str(from_name), var2=str(phone_number), var3=str(date_last_conexion) , var4=str(date_created))   
                            cursor.execute(sql)
                            connection.commit()
    

                connection.close()
        else:
            #print("NO SON MENSAJES DE CLIENTE...")
            # print("STATUS" +  str( data['entry'][0]['changes'][0]['value']['statuses'][0]['status']))
            # print("NUMBER" +  str( data['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']))

            if (data['entry'][0]['changes'][0]['value']['statuses'][0]['status']=="failed"):
                print("STATUS" +  str( data['entry'][0]['changes'][0]['value']['statuses'][0]['status']))
                print("NUMBER" +  str( data['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']))
                phone_number = data['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']
                with connection.cursor() as cursor:
                    sql = "SELECT id FROM user WHERE number_phone=%s"
                    cursor.execute(sql,(phone_number))
                    result_user= cursor.fetchone()
                    client = WhatsAppWrapper() 
                    client.send_template_message("pregunta_envio_mensajes", phone_number)

                    # if(cursor.rowcount==1):
                    #     id_user = result_user["id"]
                    #     sql = "SELECT message FROM message_last_to_client WHERE id_user=%s "
                    #     cursor.execute(sql,(id_user))
                    #     result_last_message= cursor.fetchone()
                    #     if(cursor.rowcount==1):
                    #         msg = result_last_message["message"]
                    #         pass
                    
                    connection.close()
         
          
        return  response
    
    
    
