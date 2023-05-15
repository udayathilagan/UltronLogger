import os
import json
import logging

import paho.mqtt.client as mqtt

logging.basicConfig(filename='UltronLogger_app_app.log', filemode='a', format='%(asctime)s- %(name)s.%(funcName)s - %(levelname)s - %(message)s')

def Get_Mqtt_Data():
    global Mqtt_Server
    global Mqtt_Port
    global Mqtt_Sub_topic
    global Mqtt_Passcode
    try:        
        fl = open('Mqtt_Config.json',)
        mqtt_data = json.load(fl)
        fl.close()
        Mqtt_Server=mqtt_data["Host_Name"]
        Mqtt_Port=mqtt_data["Port"]
        Mqtt_Sub_topic=mqtt_data["Sub_Topic"]
        Mqtt_Passcode=mqtt_data["Passcode"]
        logging.warning(f"\nMqtt Host_Name : {Mqtt_Server}\nMqtt Port : {Mqtt_Port}\nMqtt Subscribe topic: {Mqtt_Sub_topic}\n")
    except Exception as e:
        logging.error(e)
    


def on_connect(client, userdata, flags, rc):
    print("Result from connect: {}".format( mqtt.connack_string(rc) ) )
    client.subscribe(Mqtt_Sub_topic)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")
    
    
            
def on_message(client, userdata, msg):
    dec=msg.payload.decode("utf-8")
    k='{{"TOPIC":"{}","MSG":"{}"}}'.format(msg.topic,dec)
    logging.warning(k)
    print(k)
        

if __name__ == "__main__":
    try :
            
        Current_version="0.1.0"
        program='''
            Program name        : UltronLogger
            Author              : udayathilagan
            Date created        : 06/08/2021
            Date last modified  : 06/08/2021
            Python Version      : 3.9.6
            Program Version     : {}        
            Email address       : udayathilagan@gmail.com'''.format(Current_version)  
            
        logging.warning(program)
        Get_Mqtt_Data()
        client = mqtt.Client()
        client = mqtt.Client(protocol=mqtt.MQTTv311)
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.connect(host=Mqtt_Server, port=Mqtt_Port)
        client.loop_forever()
    except Exception as e:
        logging.error(e)