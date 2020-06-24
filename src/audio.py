#!python
# coding: utf-8

# Imports
import pygame
import json
import ttos


def go(det, value):

    # Get speech from script 
    if det == "key":
        with open('script.JSON', 'r') as f:
            script = dict(json.load(f))
            guisett("speech", script)
            ttos.go(script[value], False)
            play("temp/audio/ttos.wav")
    elif det == "raw":
        # RAW speech
        guisett("speech", value)
        ttos.go(value, False)
        play("temp/audio/ttos.wav")
    elif det == "equ":
        # Equations with SSML
        ttos.go(value, True)
        play("temp/audio/ttos.wav")
    elif det == "nav":
        # Navigational audio
        play("temp/audio/nav.wav")
    else: 
        print("ERR - Invalid call")

    return


def play(file):
    
    print("pkg_AUDIO - Playing audio")

    # Play audio
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

    return


def guisett(key, val):

    # Set GUI LED/Text
    with open('gui.JSON', 'r') as f:
        data = dict(json.load(f))
    
    data[key] = val

    with open('gui.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


if __name__ == '__main__':

    play("temp/audio/ttos.wav")

