

#!/usr/bin/env python
##import pygame
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import paho.mqtt.client as mqtt
import datetime
import json
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Booting Jukeberry")

rfidBased = True

def stop(pin):
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%zZ")
    message = {"sentAt": now }
    print (message)
    mqttClient.publish("stop/pushed", json.dumps(message))
    
def play(id, text):
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%zZ")
    message = {"id": str(id), "text": text, "sentAt": now }
    mqttClient.publish("card/presented", json.dumps(message))

def keyboardRead():
    i=1
    switcher=[
        (649586696873, "Bodysnatchers"),
        (252470762881, "Creep"),
        (735250948581, "High and Dry")
    ]
    for item in switcher:
        print(str(i) + ": " + str(item))
        i = i+1
    text = input('Select option:')
    if text.isnumeric() and int(text) >=1 and int(text) <=3:
        return switcher[int(text)-1]
    else:
        print("Invalid Option")
        return keyboardRead()

mqttTransport = "websockets"
mqttHost = "mr1nljqp0y1g2d.messaging.solace.cloud"
mqttPort = 21128
mqttUser = "solace-cloud-client"
mqttPassword = "7ide7v7illr1fs4bsio3ls26f0"

mqttClient = mqtt.Client("jukeberry", transport=mqttTransport)
mqttClient.username_pw_set(username="solace-cloud-client",password="7ide7v7illr1fs4bsio3ls26f0")
mqttClient.connect(mqttHost, mqttPort)

print("Connected to: " + mqttHost)

GPIO.add_event_detect(11, GPIO.FALLING, callback=stop, bouncetime=300)
print("Stop button registered") 

if rfidBased:
    reader = SimpleMFRC522()
    print("Enabling RFID Reader")
else:
    print("Enabling Keyboard RFID Reader emulation")

try:
    while(True):
        if rfidBased:
            id, text = reader.read()
        else:
            id, text = keyboardRead()
        
        print("Read ID:" + str(id))
        print("Card Song:" + str(text))
        
        play(id, text)
                
        if rfidBased:
            time.sleep(1);
except KeyboardInterrupt:         
    GPIO.cleanup()
    raise
finally:
    GPIO.cleanup()