#!python
# coding: utf-8

# Imports
import pygame
import json
import ttos

def go(det, value):

    if det == "key":
        with open('script.JSON', 'r') as f:
            script = dict(json.load(f))
            ttos.go(script[value], False)
            play("temp/audio/ttos.wav")
    elif det == "raw":
        ttos.go(value, False)
        play("temp/audio/ttos.wav")
    elif det == "equ":
        ttos.go(value, True)
        play("temp/audio/ttos.wav")
    elif det == "nav":
        play("temp/audio/nav.wav")
    else: 
        print("ERR - Invalid call")

    return

# Play audio file to speakers
def play(file):
    
    print("pkg_AUDIO - Playing audio")

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

    return

if __name__ == '__main__':

    play("temp/audio/ttos.wav")

