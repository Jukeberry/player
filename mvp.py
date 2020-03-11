

#!/usr/bin/env python
import pygame
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import paho.mqtt.client as mqtt
import datetime
import json
import time

def song(i):
    switcher={
        96675065265: "music/ParanoidAndroid.mp3",
        664003290249: "music/Creep.mp3",
        649586696873: "music/HighAndDry.mp3",
        711986787821: "music/BonfireHeart.mp3"
    }
    return switcher.get(i,"INVALID");

selectedDevice = False
reader = SimpleMFRC522()
mqttClient = mqtt.Client("jukeberry")
mqttClient.connect("192.168.0.12", 1883)
try:
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)
    while(True):
        id, text = reader.read()
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%zZ")
        print("id:" + str(id))
        print("text:" + text)
        
        
        play = song(id)
        print(play)
        if(selectedDevice):
            print("playing in raspi")
            pygame.mixer.music.load(play)
            pygame.mixer.music.play()
        else:
            message = {"id": str(id), "text": text, "sentAt": now }
            mqttClient.publish("card/presented", json.dumps(message))
        
        time.sleep(1);
        
    
finally:
    GPIO.cleanup()


