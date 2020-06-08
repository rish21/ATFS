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
            ttos.go(script[value])
            play("temp/ttos.mp3")
    elif det == "raw":
        ttos.go(value)
        play("temp/ttos.mp3")
    elif det == "nav":
        play("temp/nav.mp3")
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

    play("temp/ttos.mp3")

