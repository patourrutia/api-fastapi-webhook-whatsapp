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
def call_gpt2(preg):
    KEY_CHATGPT =  os.environ.get('KEY_CHATGPT')
    openai.api_key=KEY_CHATGPT

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    # model="gpt-3.5-turbo-0301",
    
    messages=[
        {"role": "system", "content": "You are a kind helpful assistant."},
        {"role": "user", "content": preg},
        # {"role": "system", "content": preg}
     ]
    )
    # print (completion.choices[0].message["content"])
    return completion.choices[0].message["content"]

def call_gpt(preg):
    KEY_CHATGPT =  os.environ.get('KEY_CHATGPT')
    openai.api_key=KEY_CHATGPT
    try:
        completion = openai.Completion.create(engine="text-davinci-003",
                                            prompt=preg,
                                            max_tokens=2048)
        # completion = openai.Completion.create(engine="gpt-3.5-turbo-0301",
        #                                     prompt=preg,
        #                                     max_tokens=2048)
        
        
        # completion = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages = preg,
        #     temperature = 0.8
        # )
        # respuesta = completion.choices[0]['message']['content']
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
   
    # sql = "SELECT sentence,correct_option, complete_sentence,traslate_sentence FROM sentence WHERE id=%s"
    # curs.execute(sql,(lev))
    # result_sentence= curs.fetchone()
    # #correct_option = result_sentence["correct_option"].split("|")
    # traslate_sentence = result_sentence["traslate_sentence"]
    # sentence_actual = result_sentence["sentence"]
    # message=sentence_actual
    # sentence = message.split("|")
    # msg = '*N' + sentence[0] + '* \n '
    # for s in range(1,len(sentence)):
    #     msg = msg + '\n👉 *' + sentence[s]              
    # message = msg + "\n"  
        
    # client = WhatsAppWrapper()   
    # client.send_message2(
    #     message=message,
    #     phone_number=number,
    #     trans =traslate_sentence[0:70]
    # )
    sql = "SELECT sentence,correct_option, complete_sentence,traslate_sentence FROM sentence WHERE id=%s"
    curs.execute(sql,(lev))
    result_sentence= curs.fetchone()
    #correct_option = result_sentence["correct_option"].split("|")
    traslate_sentence = result_sentence["traslate_sentence"]
    sentence_actual = result_sentence["sentence"]
    message=sentence_actual
    sentence = message.split("|")


    msg = '\n_🇪🇸N' + traslate_sentence[0:70] + '_ \n\n'
    msg = msg + '*🇺🇸N' + sentence[0].replace("...","_______") + '*  \n'
    for s in range(1,len(sentence)):
        msg = msg + '\n    👉 *' + sentence[s]              
    msg = msg + "\n\n"  
    message = msg + "_☘️Elije la opcion correcta_" 

        
    client = WhatsAppWrapper()   
    client.send_message(
        message=message,
        phone_number=number
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
    msg = msg + "☑️Ver Top 20: T\n"  
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
                    "text": "\nElije la opcion correcta"
                },
                "action": {
                    "button": "Ver_Traduccion_Español",
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
            "preview_url": False,
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
        connection = pymysql.connect(host='10.10.1.216',
        user='root',
        password='123456',
        database='grammar_bot',
        cursorclass=pymysql.cursors.DictCursor)
        
        
        messages =   changes.get("messages")
        if messages:
            #print("FROM CLIENTE")
            #print("FROM CLIENTE")
            #print(changes)
            phone_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            from_name = data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']   
            idmsg = data['entry'][0]['changes'][0]['value']['messages'][0]['id']
            # print(messages)
            #print (phone_number + " - " + from_name )
            if (data['entry'][0]['changes'][0]['value']['messages'][0]['type']=="text"):
                #print (data_json['entry'][0]['changes'][0]['value']['messages'][0]['type'])
                respuesta_cliente =data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

                respuesta_cliente_normal =respuesta_cliente
                text = respuesta_cliente
                # print(respuesta_cliente_normal)
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

                        if (phone_number =="56926249071"):
                            sql = "SELECT id, message FROM message_last_to_client WHERE id_user=%s"
                            cursor.execute(sql,(id_user))
                            result_msg_no_enviados = cursor.fetchall()
                            for  i, dicc_msg in enumerate(result_msg_no_enviados):
                                last_message = dicc_msg["message"]
                                id_last = dicc_msg["id"]
                                client.send_message(        
                                    message=last_message,
                                    phone_number=phone_number
                                )
                                sql = "DELETE FROM message_last_to_client WHERE id={var1}".format(var1=id_last)   

                                cursor.execute(sql)
                                connection.commit() 


                        opcion = ""
                        data_respuesta = ""
                        
                        if (phone_number =="56952244429"):
                            if((text[0:4].lower()=="foto")):
                                # mod = int(text[4:5])
                                # data_respuesta = text[5:]  
                                opcion ="foto"
                            elif((text[0:4].lower()==".")):
                                # mod = int(text[4:5])
                                # data_respuesta = text[5:]  
                                opcion ="nada"

                        if (modo==4):
                            #pagar  mensaje_no_valido
                            if((len(text)>=4)):
                                if((text[0:5].lower()=="pagar")):
                                    mod = int(text[5:7] )
                                    data_respuesta = text[7:] 
                                    opcion ="pagar"
                                elif((text[0:9].lower()=="envia_top")):
                                    # mod = int(text[5:7] )
                                    data_respuesta = text[9:] 
                                    opcion ="envia_top"
                                    #print("Pagar")
                                    #print(data_respuesta)
                                elif((text[0:17].lower()=="mensaje_no_valido")):
                                    opcion ="mensaje_no_valido"
                                    data_respuesta = text[17:]
                                    #print("mensaje_no_valido")
                                    #print(data_respuesta)
                                elif((text[0:4].lower()=="modo")):
                                    mod = int(text[4:5])
                                    data_respuesta = text[5:]  
                                    opcion ="modo"
                                # elif((text[0:4].lower()=="foto")):
                                #     # mod = int(text[4:5])
                                #     # data_respuesta = text[5:]  
                                #     opcion ="foto"
                         
            
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
                            manana = ahora + datetime.timedelta(days=7)
                            date_expired = manana.strftime("%Y-%m-%d %H:%M:%S")                            
                            date_actual = datetime.datetime.now()   
                            date_last_conexion = date_actual.strftime("%Y-%m-%d %H:%M:%S")
                            sql = "UPDATE user SET status=2, name='{var1}', pais='{var2}', email='{var3}', date_expired='{var4}', date_last_conexion='{var5}'  WHERE id={var6}".format(var1=str(nombre), var2=str(pais),var3=str(email), var4=str(date_expired), var5=str(date_last_conexion), var6=str(id_user))   
                            cursor.execute(sql)
                            connection.commit()
                            
                            # client.send_message(        
                            #     message="✅¡Registro exitoso! Desde de ahora, podrás disfrutar de nuestro servicio gratuito por tres días.",
                            #     phone_number=phone_number,
                            # )
                            # msg = msgayuda()
                            # client.send_message(        
                            #     message="✅ ¡Es hora de comenzar con los ejercicios interactivos de gramática! ¡Siéntete cómodo y prepárate para mejorar tus habilidades en inglés! 💪 ¡Buena suerte! 👋 ",
                            #     phone_number=phone_number,
                            # )
                            client.send_message(        
                                message="✅ ¡Registro exitoso! desde de ahora, disfruta de nuestro servicio gratuito por 7 días. ¡Es momento de comenzar con los ejercicios interactivos de gramática! 💪 ¡Buena suerte! 👋",
                                phone_number=phone_number,
                            )
                            
                           
                            # client.send_message(        
                            #     message=msg,
                            #     phone_number=phone_number,
                            # )

                            msgADNMIN ="✅ PHONE: " + str(phone_number) + " NAME: " +from_name + "  USUARIO NUMERO: " + str(id_user) +" A COMENENZADO A USAR MYGRAMMARBOT"
                            client.send_message(        
                                message=msgADNMIN,
                                phone_number=phone_admin,
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
                                            message="✅ MENSAJE RESPONDIDO",
                                            phone_number=phone_number
                                        )

                                        envia_ultima_sentencia(cursor,level,phone)
                                        almacena_respuestas(respuesta_cliente_normal,3,id_user,cursor,connection)

                                    else:
                                        client.send_message(        
                                            message="❌ ERROR- USUARIO NO REGISTRADO",
                                            phone_number=phone_number
                                        )
                                elif((opcion =='envia_top') ) :
                                    data_respuesta = data_respuesta.replace("+","")
                                    data_respuesta = data_respuesta.replace(" ","")
                                    phone_number = data_respuesta
                                    msg = msgayuda()  
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_number,
                                    )

                                    sql = "SELECT name_whatsapp FROM user ORDER BY maxlevel desc limit 20"
                                    cursor.execute(sql)
                                    result_sentence = cursor.fetchall()
                                    msg= " Top 20 🏆\n"
                                    for  i, dicc_sentence in enumerate(result_sentence):
                                        name_whatsapp = dicc_sentence["name_whatsapp"]
                                        if (int(i) == 0):
                                                medalla ="🥇"
                                        elif(int(i) == 1):
                                            medalla ="🥈"
                                        elif(int(i) == 2):
                                            medalla ="🥉"
                                        else:
                                            medalla ="🏅"
                                        msg= msg + "\n"+ medalla + " "+  str(int(i) +1 )  + ".-" +name_whatsapp
                                 


                                    # sql = "SELECT id, name_whatsapp FROM user ORDER BY maxlevel desc"
                                    # cursor.execute(sql)
                                    # result_sentence = cursor.fetchall()
                                    # p = 0
                                    # for  i, dicc_sentence in enumerate(result_sentence):
                                    #     p+=1
                                    #     if (str(id_user) == str(dicc_sentence["id"])):
                                    #         position = p
                                    #         break
                                    # msg= msg + "\n\n 🏅Tu posicion es " + str(position)
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_number,
                                    )

                                elif(opcion =='modo'):
                                    
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
                                    
                                      
                                        sql = "UPDATE user SET  modo='{var1}' WHERE id={var2}".format(var1=mod, var2=str(id_user2))   
                                        cursor.execute(sql)
                                        connection.commit()

                                        client.send_message(        
                                            message="✅ CAMBIO MODO ACEPTADO",
                                            phone_number=phone_number
                                        )
                                        if (mod == 1):
                                            modito = "GRAMMAR"
                                        elif (mod == 2):
                                            modito = "CHATGPT"
                                        elif( mod == 3):
                                            modito = "GRAMMAR Y CHATGPT"

                                        client.send_message(        
                                            message="✅ El cambio de modo se ha realizado exitosamente. Ahora estás en el modo: " +modito,
                                            phone_number=data_respuesta
                                        )
                                        envia_ultima_sentencia(cursor,level,data_respuesta)
                                        almacena_respuestas(respuesta_cliente_normal,7,id_user,cursor,connection)

                                    else:
                                        client.send_message(        
                                            message="❌ ERROR- USUARIO NO REGISTRADO",
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
                                        day_supcrypcion = mod * 31

                                      
                                        date_expired = date_actual + datetime.timedelta(days=day_supcrypcion)
                                        date_expired_clien = date_actual + datetime.timedelta(days=day_supcrypcion)


                                        date_expired = date_expired.strftime("%Y-%m-%d %H:%M:%S")  

                                        date_expired_clien_str = date_expired_clien.strftime("%d-%m-%Y ") 

                                        date_paid = date_actual.strftime("%Y-%m-%d %H:%M:%S")
                                        sql = "UPDATE user SET status=3, date_paid='{var1}' , date_expired='{var2}' WHERE id={var3}".format( var1=str(date_paid),  var2=str(date_expired), var3=str(id_user2))   
                                        cursor.execute(sql)
                                        connection.commit()

                                        client.send_message(        
                                            message="💳 👍 PAGO ACEPTADO",
                                            phone_number=phone_number
                                        )
                                        client.send_message(        
                                            message="💳 👍¡Pago aceptado! Ahora puedes seguir disfrutando de nuestro servicio hasta el " + date_expired_clien_str,
                                            phone_number=data_respuesta
                                        )
                                        envia_ultima_sentencia(cursor,level,data_respuesta)
                                        almacena_respuestas(respuesta_cliente_normal,4,id_user,cursor,connection)

                                    else:
                                        client.send_message(        
                                            message="❌ ERROR- USUARIO NO REGISTRADO",
                                            phone_number=phone_number
                                        )
                                elif((opcion =='nada')) :
                                    pass
                                elif((opcion =='foto')) :
                                    #TYPE 5
                                    # print("Foto")
               
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    # msg = "\n\n\n\n\n\n\n\n"
                                    # client.send_message(        
                                    #     message=msg,
                                    #     phone_number=phone_number
                                    # )

                                    
                                elif((opcion =='nivel_no_numeric')) :
                                    #TYPE 5
                                    msg = "❌ El nivel ingresado({var1}) no es un numero".format(var1=str(data_respuesta))
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_number
                                    )
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,5,id_user,cursor,connection)
                                elif((opcion =='no_permitido_mayor_15805')) :
                                    #TYPE 5
                                    msg = "❌ El nivel ingresado ({var1}) debe ser inferior a 15805.".format(var1=str(data_respuesta))
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
                                        msg = "❌ El nivel ingresado es N{var1}, no debe ser mayor que el nivel máximo obtenido, que es N{var2}.".format(var1=str(data_respuesta),var2=str(maxlevel))
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

                                    
                                        
                                      

                                    sql = "SELECT name_whatsapp FROM user ORDER BY maxlevel desc limit 20"
                                    cursor.execute(sql)
                                    result_sentence = cursor.fetchall()
                                    msg= " Top 20 🏆\n"
                                    for  i, dicc_sentence in enumerate(result_sentence):
                                        name_whatsapp = dicc_sentence["name_whatsapp"]
                                        if (int(i) == 0):
                                                medalla ="🥇"
                                        elif(int(i) == 1):
                                            medalla ="🥈"
                                        elif(int(i) == 2):
                                            medalla ="🥉"
                                        else:
                                            medalla ="🏅"
                                        msg= msg + "\n"+ medalla + " "+  str(int(i) +1 )  + ".-" +name_whatsapp
                                 


                                    sql = "SELECT id, name_whatsapp FROM user ORDER BY maxlevel desc"
                                    cursor.execute(sql)
                                    result_sentence = cursor.fetchall()
                                    p = 0
                                    for  i, dicc_sentence in enumerate(result_sentence):
                                        p+=1
                                        if (str(id_user) == str(dicc_sentence["id"])):
                                            position = p
                                            break
                                    msg= msg + "\n\n 🏅Tu posicion es " + str(position)
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_number,
                                    )
                                    
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,8,id_user,cursor,connection)
                                elif((opcion =='usar_bot') and (modo==2 or modo==3)) :
                                    pregunta = data_respuesta
                                    #print("OPCION CHATGPT Y USARIO PREGUNTA:" + pregunta) TYPE 9
                                    # print(pregunta)
                                    respuesta_bot = call_gpt2(pregunta)
                                    
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
                                    message_correcto = "👍 " + result_message1["message"]
                                                                    
                                    client.send_message(        
                                        message=message_correcto,
                                        phone_number=phone_number,
                                    )

                                    if (int(level)%30==0 or int(level)==10):
                                        msg = msgayuda()  
                                        client.send_message(        
                                            message=msg,
                                            phone_number=phone_number,
                                        )

                                        sql = "SELECT name_whatsapp FROM user ORDER BY maxlevel desc limit 20"
                                        cursor.execute(sql)
                                        result_sentence = cursor.fetchall()
                                        msg= " Top 20 🏆\n"
                                        for  i, dicc_sentence in enumerate(result_sentence):
                                            name_whatsapp = dicc_sentence["name_whatsapp"]
                                            if (int(i) == 0):
                                                medalla ="🥇"
                                            elif(int(i) == 1):
                                                medalla ="🥈"
                                            elif(int(i) == 2):
                                                medalla ="🥉"
                                            else:
                                                medalla ="🏅"
                                            msg= msg + "\n"+ medalla + " "+  str(int(i) +1 )  + ".-" +name_whatsapp
                                        
                                        sql = "SELECT id, name_whatsapp FROM user ORDER BY maxlevel desc"
                                        cursor.execute(sql)
                                        result_sentence = cursor.fetchall()
                                        p = 0
                                        for  i, dicc_sentence in enumerate(result_sentence):
                                            p+=1
                                            if (str(id_user) == str(dicc_sentence["id"])):
                                                position = p
                                                break
                                        msg= msg + "\n\n Tu posicion es " + str(position)

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
                                    message_incorrecto = "❌ " + result_message2["message"]
                                    client.send_message(        
                                        message=message_incorrecto,
                                        phone_number=phone_number,
                                    )       
                                    envia_ultima_sentencia(cursor,level,phone_number)
                                    almacena_respuestas(respuesta_cliente_normal,13,id_user,cursor,connection)
                  
                                elif ((modo==1 or modo==3) and (opcion !='usar_bot') ):
                                    #print("OPCION SENTENCE RESPUESTA NOVALIDA") TYPE 14
                                    msg = "❌ "+ "MENSAJE_NO_VALIDO - "+str(idmsg) +"-" +phone_number + " - "+ from_name +" - " + respuesta_cliente          
                                    client.send_message(        
                                        message=msg,
                                        phone_number=phone_admin,
                                    )
                                    client.send_message(        
                                        message="❌ Lo siento, la opción elejida no es válida.",
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
                                        message="❌ "+ "¡Hola! 👋 Lamentablemente, el período de prueba gratuita ha terminado. Si deseas seguir disfrutando de nuestro servicio, te recomendamos que te pongas en contacto con nosotros a través de WhatsApp al siguiente número: +56926249071 o haga clic en el siguiente enlace para obtener más información sobre nuestros planes de suscripción. 👉 https://api.whatsapp.com/send?phone=56926249071&text=Hola!%20¿Cuál%20es%20el%20precio%20mensual%20de%20la%20suscripción%20para%20seguir%20utilizando%20MyGrammarBot?",
                                        phone_number=phone_number
                                    )
                                    almacena_respuestas(respuesta_cliente_normal,16,id_user,cursor,connection)
                                    msg = "❌❌"+ "USUARIO INTENTANDO ACCEDER CON PERIDO PRUEBA CADUCADA - " + phone_number + " - " + from_name + " - " + respuesta_cliente
                                    client.send_message(    
                                            message=msg,
                                            phone_number=phone_admin
                                    )
                                elif(status== 3):
                                    #PERIDO PAGADO EXPIRADO  TYPE 17
                                    client.send_message(        
                                        message="❌ " +"¡Hola! 👋 Lamentablemente, su suscripción ha finalizado terminado. Si deseas seguir disfrutando de nuestro servicio, te recomendamos que te pongas en contacto con nosotros a través de WhatsApp al siguiente número: +56926249071.",
                                        phone_number=phone_number
                                    )
                                    sql = "UPDATE user SET status= 5  WHERE id=%s" 
                                    cursor.execute(sql, (id_user))
                                    connection.commit()
                                    almacena_respuestas(respuesta_cliente_normal,17,id_user,cursor,connection)
                                    msg = "❌❌❌ " +"USUARIO INTENTANDO ACCEDER CON SUCCRIPCION CADUCADA - " + phone_number + " - " + from_name + " - " + respuesta_cliente
                                    client.send_message(    
                                            message=msg,
                                            phone_number=phone_admin
                                    )

                                else:
                                    pass
                        elif(status== 4 ):
                           #OTRO ESTADO 4  TYPE 18
                            client.send_message(        
                                    message="¡Hola! 👋 Lamentablemente, el período de prueba gratuita ha terminado. Si deseas seguir disfrutando de nuestro servicio, te recomendamos que te pongas en contacto con nosotros a través de WhatsApp al siguiente número: +56926249071 o haga clic en el siguiente enlace para obtener más información sobre nuestros planes de suscripción. 👉 https://api.whatsapp.com/send?phone=56926249071&text=Hola!%20¿Cuál%20es%20el%20precio%20mensual%20de%20la%20suscripción%20para%20seguir%20utilizando%20MyGrammarBot?",
                                    phone_number=phone_number
                                )
                            almacena_respuestas(respuesta_cliente_normal,18,id_user,cursor,connection)
                            msg = "❌❌ "+ "USUARIO INTENTANDO ACCEDER CON PERIDO PRUEBA CADUCADA - " + phone_number + " - " + from_name + " - " + respuesta_cliente
                            client.send_message(    
                                    message=msg,
                                    phone_number=phone_admin
                                )
                          
                        elif(status== 5 ):
                            #OTRO ESTADO 5  TYPE 19
                            client.send_message(        
                                        message="❌❌❌ "+ "¡Hola! 👋 Lamentablemente, su suscripción ha finalizado terminado. Si deseas seguir disfrutando de nuestro servicio, te recomendamos que te pongas en contacto con nosotros a través de WhatsApp al siguiente número: +56926249071 ",
                                        phone_number=phone_number
                            )
                            msg = "USUARIO INTENTANDO ACCEDER CON SUCCRIPCION CADUCADA - " + phone_number + " - " + from_name + " - " + respuesta_cliente
                            client.send_message(    
                                    message=msg,
                                    phone_number=phone_admin
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
                            # url_image= "https://app.idealsoft.cloud/grammarbot.jpg"
                            # response =   await  client.send_message_image(
                            #   phone_number=phone_number,
                            #   url_image=url_image
                            # )
                            #print("imagen enviada" +  str(response))
                            almacena_respuestas(respuesta_cliente_normal,1,id_user,cursor,connection)
                            
                            
                            
                           
                            # msg = "USUARIO INTENTANDO ACCEDER SIN ESTAR REGISTRADO - " + phone_number + " - " + from_name + " - " + respuesta_cliente
                            # client.send_message(    
                            #         message=msg,
                            #         phone_number=phone_admin
                            #     )
                            #almacena_envio_msg(msg,"send",id_user,cursor,connection)
                        
                            # client.send_message(        
                            #     message="👋¡Bienvenido/a! Soy tu asistente virtual y mi objetivo es ayudarte a mejorar tu inglés de manera sencilla y entretenida. Con MyGrammarBot🤖, tendrás la oportunidad de practicar gramática y enriquecer tu vocabulario en inglés.",
                            #     phone_number=phone_number
                            # )


                          

                            # client.send_message(        
                            #     message="✨ Modo Grammar: el usuario puede enviar respuestas para completar oraciones gramaticalmente correctas.",
                            #     phone_number=phone_number
                            # )
    
                            # client.send_message_video(  
                            #     phone_number=phone_number,
                            #     body ="✨Visita el siguiente enlace para ver cómo funciona el Modo Grammar👉 https://www.youtube.com/watch?v=E-84QJFcpxQ"

                            # )

                            # client.send_message(        
                            #     message="✨¿Te gustaría probar nuestro servicio de forma gratuita y recibir ejercicios interactivos a través de WhatsApp❓ Si es así, por favor, ¿podrías proporcionarnos tu nombre❓",
                            #     phone_number=phone_number
                            # )

                            client.send_message(        
                                message="✨ Hola👋, soy GrammarBot, diseñado para ayudarte a mejorar tu gramática y enriquecer tu vocabulario en inglés a través de WhatsApp. Solo dime tu nombre para comenzar.",
                                phone_number=phone_number
                            )
                           

                        
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
            #print("FROM FACEBOOK")
            #print("FROM FACEBOOK")
            #print(changes)
            if (data['entry'][0]['changes'][0]['value']['statuses'][0]['status']=="failed"):
                #print("STATUS" +  str( data['entry'][0]['changes'][0]['value']['statuses'][0]['status']))
                #print("NUMBER" +  str( data['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']))
                phone_number = data['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']
                client = WhatsAppWrapper() 
                client.send_template_message("pregunta_envio_mensajes", phone_number)
           
         
          
        return  response
    
    
    
