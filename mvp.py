

#!/usr/bin/env python
import pygame
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def song(i):
    switcher={
        96675065265: "music/ParanoidAndroid.mp3",
        664003290249: "music/Creep.mp3",
        649586696873: "music/HighAndDry.mp3",
        711986787821: "music/BonfireHeart.mp3"
    }
    return switcher.get(i,"INVALID");

reader = SimpleMFRC522()
try:
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)
    while(True):
        id, text = reader.read()
        print("id:" + str(id))
        print("text:" + text)
        
        play = song(id)
        print(play)
        pygame.mixer.music.load(play)
        pygame.mixer.music.play()
    
    
    
    
finally:
    GPIO.cleanup()


