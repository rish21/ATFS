#!python
# coding: utf-8

# Imports
import XboxController
import audio
import json
import time
import os
import stot


# Controller Callback
def CallBackS(controlId, value):

    global back, select, pointer_ud, pointer_lr, swap, s_window, s_gender, s_speakrate

    # Window (A)
    if controlId == 6 and value == 0:
        guisett("a","green")
        time.sleep(0.2)
        guisett("a","red")
        s_window = True
        
    # Gender (X)
    if controlId == 8 and value == 0:
        guisett("x","green")
        time.sleep(0.2)
        guisett("x","red")
        s_gender = True

    # Speaking Rate (B)
    if controlId == 7 and value == 0:
        guisett("b","green")
        time.sleep(0.2)
        guisett("b","red")
        s_speakrate = True

    # DPad
    if controlId == 17:
        if value[1] == -1:
            guisett("dd","green")
            time.sleep(0.2)
            guisett("dd","red")
            #print("down")
            pointer_ud[0] = pointer_ud[1]
            pointer_ud[1] = pointer_ud[1] - 1
        elif value[1] == 1:
            guisett("du","green")
            time.sleep(0.2)
            guisett("du","red")
            #print("up")
            pointer_ud[0] = pointer_ud[1]
            pointer_ud[1] = pointer_ud[1] + 1
        elif value[0] == -1:
            guisett("dl","green")
            time.sleep(0.2)
            guisett("dl","red")
            #print("left")
            pointer_lr[0] = pointer_lr[1]
            pointer_lr[1] = pointer_lr[1] - 1
        elif value[0] == 1:
            guisett("dr","green")
            time.sleep(0.2)
            guisett("dr","red")
            #print("right")
            pointer_lr[0] = pointer_lr[1]
            pointer_lr[1] = pointer_lr[1] + 1

    # Stop program (BACK)
    if controlId == 12 and value == 0:
        guisett("back","green")
        time.sleep(0.2)
        guisett("back","red")
        back = True

    return


def window(path):

    global pointer_ud, back, s_window
    sett = False

    # Set window size for graph audio 
    while sett == False and back == False:
        try:
            audio.go("key", "access_028")
            w = int(stot.get())
            if w >= 1 and w <= 10:
                
                with open(path + '/access.JSON', 'r') as f:
                    data_n = dict(json.load(f))
                with open('standard.JSON', 'r') as f:
                    data_s = dict(json.load(f))

                data_n["settings"][0]["window"] = w
                data_s["settings"][0]["window"] = w

                with open(path + '/access.JSON', 'w') as n:
                    json.dump(data_n, n, indent=4, sort_keys=False)
                with open('standard.JSON', 'w') as n:
                    json.dump(data_s, n, indent=4, sort_keys=False)

                audio.go("key", "access_029")
                sett == True
                break
        except:
            audio.go("key", "access_030")

    audio.go("key", "access_026")
    s_window = False
    sett = False
    back = False

    return


def gender(path):

    global pointer_ud, back, s_gender
    sett = False

    # Set gender for text to speech
    while sett == False and back == False:
        try:
            audio.go("key", "access_032")
            g = str(stot.get())
            print(g)
            if g == "female" or g == "mail" or g == "male":
                
                with open(path + '/access.JSON', 'r') as f:
                    data_n = dict(json.load(f))
                with open('standard.JSON', 'r') as f:
                    data_s = dict(json.load(f))

                data_n["settings"][0]["gender"] = g
                data_s["settings"][0]["gender"] = g

                with open(path + '/access.JSON', 'w') as n:
                    json.dump(data_n, n, indent=4, sort_keys=False)
                with open('standard.JSON', 'w') as n:
                    json.dump(data_s, n, indent=4, sort_keys=False)

                audio.go("key", "access_029")
                sett == True
                break
        except:
            audio.go("key", "access_030")

    audio.go("key", "access_026")
    s_gender = False
    sett = False
    back = False

    return


def speakrate(path):

    global pointer_ud, back, s_speakrate
    sett = False

    # Set speaking rate
    while sett == False and back == False:
        try:
            audio.go("key", "access_034")
            sr = float(stot.get())
            if sr >= 0.25 and sr <= 4.0:
                
                with open(path + '/access.JSON', 'r') as f:
                    data_n = dict(json.load(f))
                with open('standard.JSON', 'r') as f:
                    data_s = dict(json.load(f))

                data_n["settings"][0]["speaking_rate"] = sr
                data_s["settings"][0]["speaking_rate"] = sr

                with open(path + '/access.JSON', 'w') as n:
                    json.dump(data_n, n, indent=4, sort_keys=False)
                with open('standard.JSON', 'w') as n:
                    json.dump(data_s, n, indent=4, sort_keys=False)

                audio.go("key", "access_029")
                sett == True
                break
        except:
            audio.go("key", "access_030")

    audio.go("key", "access_026")
    s_speakrate = False
    sett = False
    back = False

    return


def guisett(key, val):

    # Set GUI LED/Text
    with open('gui.JSON', 'r') as f:
        data = dict(json.load(f))
    
    data[key] = val

    with open('gui.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return

    
def begin(path):

    # Declare and initialise 
    global back, select, pointer_ud, pointer_lr, swap, s_window, s_gender, s_speakrate
    pointer_ud = [-1, -1]
    pointer_lr = [-1, -1]
    back = False
    swap = False
    s_window = False
    s_gender = False
    s_speakrate = False
    select = False

    guisett("loc","settings")

    # Initialise new instance for new set of controls
    xboxContS = XboxController.XboxController(
        controllerCallBack = CallBackS,
        joystickNo = 0,
        deadzone = 0.1,
        scale = 1,
        invertYAxis = False)

    xboxContS.start()

    audio.go("key", "access_026")

    audio.go("key", "access_027")
    audio.go("key", "access_031")
    audio.go("key", "access_033")

    # Run
    while back == False:

        if s_window == True:
            window(path)

        if s_gender == True:
            gender(path)

        if s_speakrate == True:
            speakrate(path)

        pass

    xboxContS.stop()
    
    return back



if __name__ == '__main__':

    path = "temp/"
    begin(path)