#!python
# coding: utf-8

# Imports
import XboxController
import audio
import json
import csv
import time
import graph_audio
import os
import stot
import settings
import gui
import concurrent.futures


# Controller Callback
def CallBackA(controlId, value):

    global back, select, pointer_ud, pointer_lr, swap, ignore, a_tables, a_graphs, a_images, a_notes, a_equations, a_text, a_settings

    # Tables (A)
    if controlId == 6 and value == 0:
        guisett("a","green")
        time.sleep(0.2)
        guisett("a","red")
        a_tables = True
        
    # Graphs (X)
    if controlId == 8 and value == 0:
        guisett("x","green")
        time.sleep(0.2)
        guisett("x","red")
        if a_graphs == False:
            a_graphs = True
        else:
            select = True

    # Equations (B)
    if controlId == 7 and value == 0:
        guisett("b","green")
        time.sleep(0.2)
        guisett("b","red")
        a_equations = True

    # Images (Y)
    if controlId == 9 and value == 0:
        guisett("y","green")
        time.sleep(0.2)
        guisett("y","red")
        a_images = True

    # Text (Lshoulder)
    if controlId == 10 and value == 0:
        guisett("lb","green")
        time.sleep(0.2)
        guisett("lb","red")
        if a_text == False:
            a_text = True
        else:
            select = True
    
    # Setings (Rshoulder)
    if controlId == 11 and value == 0:
        guisett("rb","green")
        time.sleep(0.2)
        guisett("rb","red")
        a_settings = True

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

    # Add Notes (XBOX)
    if controlId == 8 and value == 0:
        guisett("xbox","green")
        time.sleep(0.2)
        guisett("xbox","red")
        if a_notes == False:
            a_notes = True
        else:
            select = True

    # Right Joystick Push - Swap table columns and rows
    if controlId == 16 and value == 0:
        guisett("rt","green")
        time.sleep(0.2)
        guisett("rt","red")
        if swap == False:
            swap = True
            ignore = True
            pointer_ud[1] = 0
            audio.go("key", "access_009")
        else:
            swap = False
            ignore = True
            pointer_ud[1] = 0
            audio.go("key", "access_009")

    # Stop program (BACK)
    if controlId == 12 and value == 0:
        guisett("back","green")
        time.sleep(0.2)
        guisett("back","red")
        back = True

    return


def settings_(path):

    global a_settings

    # Access the settings menu
    with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(settings.begin, path)
    audio.go("key", "access_008")

    a_settings = False

    return


def graphs(path):

    global pointer_ud, pointer_lr, back, a_graphs, select
    pointer_ud[1] = -1
    prev_point = pointer_ud[1]
    
    #audio.go("key", "access_010")
    
    # Select type
    while select == False and back == False:
        if pointer_lr[1] == 0 and pointer_lr[0] != pointer_lr[1]:
            audio.go("key", "access_011")
            time.sleep(0.5)
            pointer_lr[0] = pointer_lr[1]
        if pointer_lr[1] == 1 and pointer_lr[0] != pointer_lr[1]:
            audio.go("key", "access_012")
            time.sleep(0.2)
            pointer_lr[0] = pointer_lr[1]
        if pointer_lr[1] == 2 and pointer_lr[0] != pointer_lr[1]:
            audio.go("key", "access_013")
            time.sleep(0.2)
            pointer_lr[0] = pointer_lr[1]
        if pointer_lr[1] == -1 and pointer_lr[0] != -1:
            pointer_lr[1] = 2
        if pointer_lr[1] == 3:
            pointer_lr[1] = pointer_lr[1] - 3
        pass
    select = False
    audio.go("key", "access_014")

    
    # Graph Descriptions
    if pointer_lr[1] == 0:
        with open(path + '/access.JSON', 'r') as f:
            data = dict(json.load(f))

        no_items = len(data["page"][0]["graph_results"][0])

        voice = "There are " + str(no_items) + " graph descriptions, use the up and down directions on the Dpad to select each item"
        audio.go("raw", voice)

        while pointer_ud[1] >= -2 and pointer_ud[1] <= no_items and back == False:
            if pointer_ud[1] != prev_point and pointer_ud[1] != no_items and pointer_ud[1] > -1:
                temp = data["page"][0]["graph_results"][0][str(pointer_ud[1])]
                voice = "Graph " + str(pointer_ud[1]) + " seems to represent a " +  temp
                audio.go("raw", voice)
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == no_items:
                audio.go("key", "access_006")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
                audio.go("key", "access_007")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -2:
                audio.go("key", "access_007")
                pointer_ud[1] = -1
                prev_point = pointer_ud[1]
            pass


    # Full Graph Audio
    if pointer_lr[1] == 1:

        pointer_ud[1] = -1
        pointer_lr[1] = -1

        with open(path + '/access.JSON', 'r') as f:
            data = dict(json.load(f))

        no_files = len(data["page"][0]["graph_results"][0])
        
        voice = "There are " + str(no_files) + " graphs, use the up and down directions on the Dpad to select which graph audio to hear"
        audio.go("raw", voice)

        while pointer_ud[1] >= -2 and pointer_ud[1] <= no_files and back == False:
            if pointer_ud[1] != prev_point and pointer_ud[1] != no_files and pointer_ud[1] > -1:
                audio.play(path + "/audio/final0.wav")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == no_files:
                audio.go("key", "access_006")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
                audio.go("key", "access_007")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -2:
                audio.go("key", "access_007")
                pointer_ud[1] = -1
                prev_point = pointer_ud[1]
            pass

    
    # By point Graph Audio
    if pointer_lr[1] == 2:

        pointer_ud[1] = -1
        pointer_lr[1] = -1

        no_files = len(next(os.walk(path + "/csv"))[2])
        voice = "There are " + str(no_files) + " graphs, use the up and down directions on the Dpad to select which graph to access and press X"
        audio.go("raw", voice)

        while pointer_ud[1] >= -2 and pointer_ud[1] <= no_files and back == False and select == False:
            if pointer_ud[1] != prev_point and pointer_ud[1] != no_files and pointer_ud[1] > -1:
                voice = "Graph " + str(pointer_lr[1])
                audio.go("raw", voice)
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == no_files:
                audio.go("key", "access_006")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
                audio.go("key", "access_007")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -2:
                audio.go("key", "access_007")
                pointer_ud[1] = -1
                prev_point = pointer_ud[1]
            pass
        select = False
        p = pointer_ud

        with open(path + '/access.JSON', 'r') as f:
            data = dict(json.load(f))

        no_items = data["page"][0]["misc"][0][str(p)]
        voice = "There are " + str(no_items) + " data points, use the left and right directions on the Dpad to move from point to point."
        audio.go("raw", voice)

        while pointer_ud[1] >= -2 and pointer_ud[1] <= no_items and back == False:
            if pointer_ud[1] != prev_point and pointer_ud[1] != no_items and pointer_ud[1] > -1:
                graph_audio.get(1, pointer_ud[1])
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == no_items:
                audio.go("key", "access_006")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
                audio.go("key", "access_007")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -2:
                audio.go("key", "access_007")
                pointer_ud[1] = -1
                prev_point = pointer_ud[1]
            pass
        

    audio.go("key", "access_008")
    pointer_ud[1] = -1
    pointer_ud[0] = -1
    pointer_lr[1] = -1
    pointer_lr[0] = -1
    a_graphs = False
    back = False
    select = False

    return


def images(path):

    global pointer_ud, back, a_images
    pointer_ud[1] = -1
    prev_point = pointer_ud[1]

    # Image descriptions
    with open(path + '/access.JSON', 'r') as f:
        data = dict(json.load(f))

    no_items = len(data["page"][0]["image_results"][0])

    voice = "There are " + str(no_items) + " image descriptions, use the up and down directions on the Dpad to select each item"
    audio.go("raw", voice)

    while pointer_ud[1] >= -2 and pointer_ud[1] <= no_items and back == False:
        if pointer_ud[1] != prev_point and pointer_ud[1] != no_items and pointer_ud[1] > -1:
            temp = data["page"][0]["image_results"][0][str(pointer_ud[1])]
            voice = "Image " + str(pointer_ud[1]) + " seems to represent a " +  temp
            audio.go("raw", voice)
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == no_items:
            audio.go("key", "access_006")
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
            audio.go("key", "access_007")
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == -2:
            audio.go("key", "access_007")
            pointer_ud[1] = -1
            prev_point = pointer_ud[1]
        pass

    audio.go("key", "access_008")
    a_images = False
    back = False

    return


def tables(path):

    global pointer_ud, back, a_tables, swap, ignore
    ignore = False
    pointer_ud[1] = 0
    prev_point = pointer_ud[1]
    c_heading = []
    r_heading = []

    # Tables
    table_path = path + "/csv/tables/tables-page-1-table-1.csv"

    with open(table_path, newline='') as csvfile:
        im = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = list(im)

    cols = len(data[0])
    rows = len(data)

    for n, r in enumerate(data[0]):
        c_heading.append(data[0][n])
        r_heading.append(data[n][0])

    voice = "There are " + str(cols) + " columns and " + str(rows) + " rows in this table. Please note that the columns are assumed to be the headings. Use the up and down directions on the Dpad to select each item. If you would like to swap the rows with columns, press down the right joystick."
    audio.go("raw", voice)

    while pointer_ud[1] >= -1 and pointer_ud[1] <= rows and back == False:
        if pointer_ud[1] != prev_point and pointer_ud[1] != rows and pointer_ud[1] > 0 and swap == False:
            voice = ""
            for n, r in enumerate(data[pointer_ud[1]]):
                temp = "The " + str(c_heading[n]) + " is " + str(data[pointer_ud[1]][n]) + ". "
                voice = voice + temp
            audio.go("raw", voice)
            prev_point = pointer_ud[1]
            ignore = False
        if pointer_ud[1] != prev_point and pointer_ud[1] != cols and pointer_ud[1] > 0 and swap == True:
            voice = ""
            for n, r in enumerate(data):
                temp = "The " + str(r_heading[n]) + " is " + str(data[n][pointer_ud[1]]) + ". "
                voice = voice + temp
            audio.go("raw", voice)
            prev_point = pointer_ud[1]
            ignore = False
        if pointer_ud[1] != prev_point and pointer_ud[1] == rows and swap == False:
            audio.go("key", "access_006")
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == cols and swap == True:
            audio.go("key", "access_006")
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == 0 and ignore == False:
            audio.go("key", "access_007")
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
            audio.go("key", "access_007")
            pointer_ud[1] = 0
            prev_point = pointer_ud[1]
        pass

    audio.go("key", "access_008")
    a_tables = False
    back = False

    return


def notes(path):
    
    global a_notes, select, back
    pointer_ud[1] = -1
    pointer_lr[1] = -1
    prev_point = pointer_ud[1]

    audio.go("key", "access_015")

    # Select add or hear
    while select == False and back == False:
        if pointer_lr[1] == 0 and pointer_lr[0] != pointer_lr[1]:
            audio.go("key", "access_017")
            time.sleep(0.5)
            pointer_lr[0] = pointer_lr[1]
        if pointer_lr[1] == 1 and pointer_lr[0] != pointer_lr[1]:
            audio.go("key", "access_018")
            time.sleep(0.2)
            pointer_lr[0] = pointer_lr[1]
        if pointer_lr[1] == -1 and pointer_lr[0] != -1:
            pointer_lr[1] = 1
        if pointer_lr[1] == 2:
            pointer_lr[1] = pointer_lr[1] - 2
        pass
    select = False
    audio.go("key", "access_014")

    # Add a new note
    if pointer_lr[1] == 0:
        audio.go("key", "access_019")

        counter = 0

        with open(path + '/access.JSON', 'r') as f:
            data = dict(json.load(f))

        while back == False:
            if select == True:
                store = stot.get()
                data["page"][0]["notes"].append({counter:""})
                data["page"][0]["notes"][counter][counter] = store
                counter = counter + 1
                select = False
        select = False

    # Saved notes
    if pointer_lr[1] == 1:
        with open(path + '/access.JSON', 'r') as f:
            data = dict(json.load(f))

        no_items = len(data["page"][0]["notes"][0])

        voice = "There are " + str(no_items) + " notes, use the up and down directions on the Dpad to select which note to access"
        audio.go("raw", voice)

        while pointer_ud[1] >= -2 and pointer_ud[1] <= no_items and back == False:
            if pointer_ud[1] != prev_point and pointer_ud[1] != no_items and pointer_ud[1] > -1:
                voice = data["page"][0]["image_results"][0][str(pointer_ud[1])]
                audio.go("raw", voice)
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == no_items:
                audio.go("key", "access_006")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
                audio.go("key", "access_007")
                prev_point = pointer_ud[1]
            if pointer_ud[1] != prev_point and pointer_ud[1] == -2:
                audio.go("key", "access_007")
                pointer_ud[1] = -1
                prev_point = pointer_ud[1]
        pass

    audio.go("key", "access_008")
    a_notes = False
    back = False

    return


def equations(path):

    global pointer_ud, back, a_equations
    pointer_ud[1] = -1
    prev_point = pointer_ud[1]

    # Equations
    with open(path + '/access.JSON', 'r') as f:
        data = dict(json.load(f))

    no_items = len(data["page"][0]["equations"][0])

    voice = "There are " + str(no_items) + " equations, use the up and down directions on the Dpad to select which equation to hear"
    audio.go("raw", voice)

    while pointer_ud[1] >= -2 and pointer_ud[1] <= no_items and back == False:
        if pointer_ud[1] != prev_point and pointer_ud[1] != no_items and pointer_ud[1] > -1:
            temp = data["page"][0]["equations"][0][str(pointer_ud[1])]
            voice = "Equation " + str(pointer_ud[1]) + " states that " +  temp
            audio.go("equ", voice)
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == no_items:
            audio.go("key", "access_006")
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
            audio.go("key", "access_007")
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == -2:
            audio.go("key", "access_007")
            pointer_ud[1] = -1
            prev_point = pointer_ud[1]
        pass

    audio.go("key", "access_008")
    a_equations = False
    back = False

    return


def text(path):

    global pointer_ud, back, a_text, select
    pointer_ud[1] = -1
    prev_point = pointer_ud[1]

    # Text 
    with open(path + '/access.JSON', 'r') as f:
        data = dict(json.load(f))

    no_items = len(data["page"][0]["text"])

    voice = "There are " + str(no_items) + " pieces of text, use the up and down directions on the Dpad to select which section to hear"
    audio.go("raw", voice)

    while pointer_ud[1] >= -2 and pointer_ud[1] <= no_items and back == False:
        if pointer_ud[1] != prev_point and pointer_ud[1] != no_items and pointer_ud[1] > -1:
            rem = int(pointer_ud[1])

            voice = "Text piece " + str(pointer_ud[1] + 1) + ", please use the left and right directions to select between sentences and full pieces"
            audio.go("raw", voice)

            # Select 
            while select == False and back == False:
                if pointer_lr[1] == 0 and pointer_lr[0] != pointer_lr[1]:
                    audio.go("key", "access_021")
                    time.sleep(0.2)
                    pointer_lr[0] = pointer_lr[1]
                if pointer_lr[1] == 1 and pointer_lr[0] != pointer_lr[1]:
                    audio.go("key", "access_022")
                    time.sleep(0.2)
                    pointer_lr[0] = pointer_lr[1]
                if pointer_lr[1] == -1 and pointer_lr[0] != -1:
                    pointer_lr[1] = 1
                if pointer_lr[1] == 2:
                    pointer_lr[1] = pointer_lr[1] - 2
                pass
            select = False
            
            # Full text
            if pointer_lr[0] == 0:
                voice = data["page"][0]["text"][pointer_ud[1]]["full_text"]
                audio.go("raw", voice)

            # Sentences and Highlight
            if pointer_lr[1] == 1:
                pointer_ud[1] = -1
                prev_point = pointer_ud[1]

                no = len(data["page"][0]["text"][rem]["sentences"])

                voice = "There are " + str(no) + " sentences, use the up and down directions on the Dpad to select which sentence to hear"
                audio.go("raw", voice)

                while pointer_ud[1] >= -2 and pointer_ud[1] <= no and back == False:
                    if pointer_ud[1] != prev_point and pointer_ud[1] != no and pointer_ud[1] > -1:
                        voice = data["page"][0]["text"][rem]["sentences"][pointer_ud[1]]["text"]
                        audio.go("raw", voice)

                        if data["page"][0]["text"][rem]["sentences"][pointer_ud[1]]["highlighted"] == 1:
                            audio.go("key", "access_024")
                        else:
                            audio.go("key", "access_023")
                            while back == False:
                                if select == True:
                                    data["page"][0]["text"][rem]["sentences"][pointer_ud[1]]["highlighted"] = 1
                                    with open(path + '/access.JSON', 'w') as n:
                                        json.dump(data, n, indent=4, sort_keys=False)
                                    audio.go("key", "access_025")
                                    back = True
                        select = False
                        back = False
                        prev_point = pointer_ud[1]
                    if pointer_ud[1] != prev_point and pointer_ud[1] == no:
                        audio.go("key", "access_006")
                        prev_point = pointer_ud[1]
                    if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
                        audio.go("key", "access_007")
                        prev_point = pointer_ud[1]
                    if pointer_ud[1] != prev_point and pointer_ud[1] == -2:
                        audio.go("key", "access_007")
                        pointer_ud[1] = -1
                        prev_point = pointer_ud[1]
                    pass
                select = False
            
            pointer_lr[1] = -1
            pointer_ud[1] = rem
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == no_items:
            audio.go("key", "access_006")
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == -1:
            audio.go("key", "access_007")
            prev_point = pointer_ud[1]
        if pointer_ud[1] != prev_point and pointer_ud[1] == -2:
            audio.go("key", "access_007")
            pointer_ud[1] = -1
            prev_point = pointer_ud[1]
        pass

    audio.go("key", "access_008")
    a_text = False
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

    global back, select, pointer_ud, pointer_lr, swap, a_graphs, a_images, a_tables, a_notes, a_equations, a_text, a_settings
    pointer_ud = [-1, -1]
    pointer_lr = [-1, -1]
    back = False
    swap = False
    a_graphs = False
    a_images = False
    a_tables = False
    a_notes = False
    a_equations = False
    a_text = False
    a_settings = False
    select = False

    guisett("loc","access")

    # Initialise new instance for new set of controls
    xboxContA = XboxController.XboxController(
        controllerCallBack = CallBackA,
        joystickNo = 0,
        deadzone = 0.1,
        scale = 1,
        invertYAxis = False)

    xboxContA.start()

    audio.go("key", "access_008")

    audio.go("key", "access_008")
    audio.go("key", "access_001")
    audio.go("key", "access_002")
    audio.go("key", "access_003")
    audio.go("key", "access_004")
    audio.go("key", "access_035")

    # Run
    while back == False:

        if a_graphs == True:
            graphs(path)

        if a_images == True:
            images(path)

        if a_tables == True:
            tables(path)
        
        if a_notes == True:
            notes(path)
        
        if a_equations == True:
            equations(path)

        if a_text == True:
            text(path)

        if a_settings == True:
            settings_(path)

        pass

    xboxContA.stop()
    
    return back


if __name__ == '__main__':

    path = "../library/0"

    begin(path)