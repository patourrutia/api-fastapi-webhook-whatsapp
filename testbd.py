#import pymysql.cursors
# import random
# import os
# import json
# #import requests
# random_number = random.randint(1,20)
# from dotenv import load_dotenv
# load_dotenv()
import datetime ,time
import os

message = "don't"

message =   message.replace("'","\\'")
print(message)

date_actual = datetime.datetime.now()
#$print(date_actual)


date_expired ="2023-02-23 16:33:48"
date_expired = datetime.datetime.strptime(date_expired, '%Y-%m-%d %H:%M:%S')
# if (date_actual>date_expired):
#     print("FECHA ACTUAL MAYOR")
# else:
#     print("FECHA ACTUAL MENOR")





# msg = "msg"
# id_type_msg = 1
# id_user = 2
# date_actual = datetime.datetime.now()
# mydate_time = date_actual.strftime("%Y-%m-%d %H:%M:00")
# mydate = date_actual.strftime("%Y-%m-%d")
# mytime = date_actual.strftime("%H:%M:%S")
# sql = "INSERT INTO `respuesta_message` (`id`, `message`, `id_type_msg`, `id_user`, `fecha_time`, `fecha`, `time`) VALUES (NULL, '{var1}', {var2}, {var3}, '{var4}', '{var5}', '{var6}');".format(var1=str(msg),var2=id_type_msg,var3=id_user,var4=str(mydate_time),var5=str(mydate),var6=str(mytime))
# print(sql)


# def revisa_contrnido(contenido):
#     API_URL = "https://api.openai.com/v1/moderations"
#     KEY_CHATGPT = os.environ.get("KEY_CHATGPT")
#     headers = {
#         "Authorization": f"Bearer {KEY_CHATGPT}",
#         "Content-Type": "application/json"
#     }
#     payload = json.dumps({"input": contenido})
#     response = requests.request("POST", f"{API_URL}", headers=headers, data=payload)
#     assert response.status_code == 200, "Error sending message"
#     data_json  = json.loads(response.text) 
#     hate =data_json['results'][0]['categories']['hate']
#     threatening = data_json['results'][0]['categories']['hate/threatening']
#     self_harm = data_json['results'][0]['categories']['self-harm']
#     sexual = data_json['results'][0]['categories']['sexual']
#     sexual_minors = data_json['results'][0]['categories']['sexual/minors']
#     violence = data_json['results'][0]['categories']['violence']
#     violence_graphic= data_json['results'][0]['categories']['violence/graphic']
#     if (hate or threatening or self_harm or sexual or sexual_minors or violence or violence_graphic):
#         return True
#     else:
#         return False


# contenido="putas"
# request = revisa_contrnido(contenido)
# print(request)

#print(random_number)


# import datetime
# ahora = datetime.datetime.now()
# print(ahora)
# manana = ahora + datetime.timedelta(days=1)
# manana = manana.strftime("%Y-%m-%d %H:%M:%S")
# print(manana)
# zona_horaria = timezone(hours=-3)
# print(zona_horaria)
# print(time.tzname(-3))

# respuesta_cliente="hol"
# ingreso_data  = respuesta_cliente.split(",")
# print(len(ingreso_data))
# email= ""
# pais= ""

# if (len(ingreso_data)==2):
#     nombre = ingreso_data[0]
#     pais= ingreso_data[1]
  
# elif(len(ingreso_data)>=3):
#     nombre = ingreso_data[0]
#     pais   = ingreso_data[1]
#     email  = ingreso_data[2]
# else:
#     nombre= respuesta_cliente

    # msg = msg + "———————————\n"
    # msg = msg + "☑️Traducir a Español\n"
    # msg = msg + "       Ej: How are you🇪🇸\n"
    # msg = msg + "☑️Traducir a Ingles\n"
    # msg = msg + "      Ej:Buen trabajo🇺🇸\n"
    # msg = msg + "☑️Ir a un nivel\n"  
    # msg = msg + "      Ej: N5 (Va al nivel 5)\n" N15000
    # msg = msg + "☑️Ver Top 10: T\n"  
    # msg = msg + "☑️Ver Funciones: F \n"


# text =" Nhola como estas🇪🇸"
# modo = 3
# opcion=""

# if (modo==4):
#     #pagar  mensaje_no_valido
#     if((len(text)>=4)):
#         if((text[0:5].lower()=="pagar")):
#             data_respuesta = text[5:]  
#             opcion ="pagar"
#             #print("Pagar")
#             #print(data_respuesta)
#         elif((text[0:17].lower()=="mensaje_no_valido")):
#             opcion ="mensaje_no_valido"
#             data_respuesta = text[17:]
#             #print("mensaje_no_valido")
#             #print(data_respuesta)
#         else:
#             #NO HACE NADA
#             pass
#             #print("#NO HACE NADA")
# else:
#     if ((len(text)== 1) and (modo==1 or modo==3)):
#         if((text=="F") ) and (modo==1 or modo==3):
#             opcion="F"
#             #print("F")
#         elif((text=="T" )and (modo==1 or modo==3)):
#             opcion="T"
#             #print("T")
#         else:
#             #NO HACE NADA
#             pass
#             #print("#NO HACE NADA")

#     elif(len(text)==2):
#         if((text[0:1]=="N" ) and (modo==1 or modo==3)):
#             if (text[1:].replace(" ","").isnumeric()):
#                 opcion="NIVEL"
#                 data_respuesta = text[1:].replace(" ","")  
#                 #print("ESTA BIEN")
#             else:
#                 #NO HACE NADA
#                 pass
#                 #print("MALO NO ES NUMERICO")
#         else:
#             #NO HACE NADA
#             pass
#             #print("#NO HACE NADA")
#     elif(len(text)==3):
#         if((text[0:1]=="N" ) and (modo==1 or modo==3)):
#             if (text[1:].replace(" ","").isnumeric()):
#                 opcion="NIVEL"
#                 data_respuesta = text[1:].replace(" ","")  
#                 #print("ESTA BIEN")
#             else:
#                 #NO HACE NADA
#                 pass
#                 #print("MALO NO ES NUMERICO")
#         else:
#             #NO HACE NADA
#             pass
#             #print("#NO HACE NADA")

#     elif(len(text)>=4):
#         if((text[0:1]=="N") and (modo==1 or modo==3)):
#             if (text[1:].replace(" ","").isnumeric()):
                
#                 data_respuesta = text[1:].replace(" ","")  
#                 if (int(data_respuesta)<=15805):
#                     opcion="NIVEL"
#                     #print("Es Numero")
#                 else:
#                     #NO HACE NADA
#                     pass
#                     #print("#NO HACE NADA")
                
#             else:
#                 if((text[-2]=='🇺') and (modo==1 or modo==3)):
#                     opcion="TRAD_ING"
#                     data_respuesta = text[:-2]
#                     #print("TRADUCCION A INGLES")
#                 elif((text[-2]=='🇪' ) and (modo==1 or modo==3)):
#                     opcion="TRAD_ESP"
#                     data_respuesta = text[:-2]
#                     #print("TRADUCCION A ESPAÑOL")
#                 else:
#                     #NO HACE NADA
#                     pass
#                     #print("#NO HACE NADA")

#         elif((text[0:3].lower()=="bot") and (modo==2 or modo==3)):
#             data_respuesta = text[4:]  
#             opcion="usar_bot"
        
#         elif((text[-2]=='🇺') and (modo==1 or modo==3)):
#             opcion="trad_ing"
#             data_respuesta = text[:-2]
#             #print("TRADUCCION A INGLES")
        
#         elif((text[-2]=='🇪') and (modo==1 or modo==3)):
#             opcion="trad_esp"
#             data_respuesta = text[:-2]    
#             #print("TRADUCCION A ESPAÑOL")
#         else:
#             #NO HACE NADA
#             pass
#             #print("#NO HACE NADA")
   
       
# print(opcion)

            
    









# text="registrameholamundo boT"

#print(text[-3:])
#boT
#print(text[:-3])
#registrameholamundo

# print(text[0:10])
# print(text[-1:])
#print(text[-2])
#print(text[3:])
#istrameholamundo boT



# connection = pymysql.connect(host='localhost',
#                     user='root',
#                     password='root',
#                     database='grammar_bot',
#                     cursorclass=pymysql.cursors.DictCursor)

# with connection.cursor() as cursor:
#     # phone_number = 56944188037
#     # phone_number = 56952244429
#     # sql = "SELECT id,level FROM user WHERE number_phone=%s"
#     # cursor.execute(sql,(phone_number))
#     # result_user= cursor.fetchone()
#     # id_user = result_user["id"]
#     # level = result_user["level"] 
#     # sql = "SELECT id, id_sentence FROM send_sentence WHERE id_user= %s ORDER BY  id desc LIMIT 1"
#     # cursor.execute(sql,(id_user))
#     # result_send_sentence= cursor.fetchone()
#     # print(cursor.rowcount)
#     #id_sentence = result_send_sentence["id_sentence"]
#     #id_send_sentence= result_send_sentence["id"]
#     #print(id_sentence)

#     random_number = random.randint(1,20)
#     sql = "SELECT message FROM message_respuestas_correcto WHERE active= 1 and id=%s"
#     cursor.execute(sql,(random_number))
#     result_message = cursor.fetchone()

#     print(result_message["message"])

#     random_number = random.randint(1,20)

#     sql = "SELECT * FROM message_respuestas_incorrecto WHERE active= 1 and id=%s"
#     cursor.execute(sql,(random_number))
#     result_message2 = cursor.fetchone()

#     print(result_message2["message"])
# connection.close()