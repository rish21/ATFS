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
def CallBackA(controlId, value):

    global back, select, pointer_ud, pointer_lr, swap, a_window, a_gender, a_speakrate

    # Window (A)
    if controlId == 6 and value == 0:
        a_window = True
        
    # Gender (X)
    if controlId == 8 and value == 0:
        a_gender = True

    # Speaking Rate (B)
    if controlId == 7 and value == 0:
       a_speakrate = True

    # (Y)
    if controlId == 9 and value == 0:

    # DPad
    if controlId == 17:
        if value[1] == -1:
            #print("down")
            pointer_ud[0] = pointer_ud[1]
            pointer_ud[1] = pointer_ud[1] - 1
        elif value[1] == 1:
            #print("up")
            pointer_ud[0] = pointer_ud[1]
            pointer_ud[1] = pointer_ud[1] + 1
        elif value[0] == -1:
            #print("left")
            pointer_lr[0] = pointer_lr[1]
            pointer_lr[1] = pointer_lr[1] - 1
        elif value[0] == 1:
            #print("right")
            pointer_lr[0] = pointer_lr[1]
            pointer_lr[1] = pointer_lr[1] + 1

    # Stop program (BACK)
    if controlId == 12 and value == 0:
        print("BACK")
        back = True

    # (XBOX)
    if controlId == 8 and value == 0:

    return


def window():

    global pointer_ud, back, a_window
    sett = False

    while sett == False and back == False:
        try:
            audio.go("key", "access_028")
            w = int(stot.get())
            if w >= 1 and w <= 10:
                
                with open('temp/access.JSON', 'r') as f:
                    data_n = dict(json.load(f))
                with open('standard.JSON', 'r') as f:
                    data_s = dict(json.load(f))

                data_n["settings"][0]["window"] = w
                data_s["settings"][0]["window"] = w

                with open('temp/access.JSON', 'w') as n:
                    json.dump(data_n, n, indent=4, sort_keys=False)
                with open('standard.JSON', 'w') as n:
                    json.dump(data_s, n, indent=4, sort_keys=False)

                audio.go("key", "access_029")
                sett == True
                break
        except:
            audio.go("key", "access_030")

    audio.go("key", "access_026")
    a_window = False
    sett = False
    back = False

    return


def gender():

    global pointer_ud, back, a_gender
    sett = False

    while sett == False and back == False:
        try:
            audio.go("key", "access_032")
            g = str(stot.get())
            print(g)
            if g == "female" or g == "mail" or g == "male":
                
                with open('temp/access.JSON', 'r') as f:
                    data_n = dict(json.load(f))
                with open('standard.JSON', 'r') as f:
                    data_s = dict(json.load(f))

                data_n["settings"][0]["gender"] = g
                data_s["settings"][0]["gender"] = g

                with open('temp/access.JSON', 'w') as n:
                    json.dump(data_n, n, indent=4, sort_keys=False)
                with open('standard.JSON', 'w') as n:
                    json.dump(data_s, n, indent=4, sort_keys=False)

                audio.go("key", "access_029")
                sett == True
                break
        except:
            audio.go("key", "access_030")

    audio.go("key", "access_026")
    a_gender = False
    sett = False
    back = False

    return


def speakrate():

    global pointer_ud, back, a_speakrate
    sett = False

    while sett == False and back == False:
        try:
            audio.go("key", "access_034")
            sr = float(stot.get())
            if sr >= 0.25 and sr <= 4.0:
                
                with open('temp/access.JSON', 'r') as f:
                    data_n = dict(json.load(f))
                with open('standard.JSON', 'r') as f:
                    data_s = dict(json.load(f))

                data_n["settings"][0]["speaking_rate"] = sr
                data_s["settings"][0]["speaking_rate"] = sr

                with open('temp/access.JSON', 'w') as n:
                    json.dump(data_n, n, indent=4, sort_keys=False)
                with open('standard.JSON', 'w') as n:
                    json.dump(data_s, n, indent=4, sort_keys=False)

                audio.go("key", "access_029")
                sett == True
                break
        except:
            audio.go("key", "access_030")

    audio.go("key", "access_026")
    a_speakrate = False
    sett = False
    back = False

    return

    
def begin():

    global back, select, pointer_ud, pointer_lr, swap, a_window, a_gender, a_speakrate
    pointer_ud = [-1, -1]
    pointer_lr = [-1, -1]
    back = False
    swap = False
    a_window = False
    a_gender = False
    a_speakrate = False
    select = False

    xboxContA = XboxController.XboxController(
        controllerCallBack = CallBackA,
        joystickNo = 0,
        deadzone = 0.1,
        scale = 1,
        invertYAxis = False)

    xboxContA.start()

    audio.go("key", "access_026")

    audio.go("key", "access_027")
    audio.go("key", "access_031")
    audio.go("key", "access_033")

    while back == False:

        if a_window == True:
            window()

        if a_gender == True:
            gender()

        if a_speakrate == True:
            speakrate()

        pass

    xboxContA.stop()
    
    return back



if __name__ == '__main__':

    begin()