#!python
# coding: utf-8

# Imports
import XboxController
import audio
import scanner
import extraction
import access
import concurrent.futures

import gui
import time
import os
import json
from multiprocessing import Process


# Controller Callback
def CallBackM(controlId, value):

    global back, select, m_scan, m_extract, m_access, m_access_old, pointer_ud, pointer_lr

    # Scan new document (A)
    if controlId == 6 and value == 0:
        guisett("a","green")
        time.sleep(0.2)
        guisett("a","red")
        m_scan = True
        
    # Run extraction if a document has been scanned (X)
    if controlId == 8 and value == 0:
        guisett("x","green")
        time.sleep(0.2)
        guisett("x","red")
        m_extract = True

    # Access current scanned document (B)
    if controlId == 7 and value == 0:
        guisett("b","green")
        time.sleep(0.2)
        guisett("b","red")
        m_access = True

    # Access old scanned documents (Y)
    if controlId == 9 and value == 0:
        guisett("y","green")
        time.sleep(0.2)
        guisett("y","red")
        if m_access_old == False:
            m_access_old = True
        else:
            select = True

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


def scan(xboxContM):

    global m_scan, ext_flag

    #os.system("gnome-terminal -- python scanner.py")
    
    # Run document scanning
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(scanner.run,)
        ext_flag = future.result()
    
    if ext_flag == True:
        # Scan successful 
        audio.go("key", "main_003")
    else:
        # Scan unsuccessful
        audio.go("key", "main_010")

    m_scan = False

    return


def extract():

    global m_extract, load_flag

    ext_flag = os.path.isfile('temp/scanned.jpg')
    if ext_flag == True:
        # Scan successful 
        audio.go("key", "main_003")
    else:
        # Scan unsuccessful
        audio.go("key", "main_010")

    if ext_flag == True:
        # Extract information from document 
        audio.go("key", "main_005")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(extraction.run,)
            load_flag, path = future.result()
        if load_flag == True:
            # Successful extraction
            audio.go("key", "main_009")
        else:
            # Unsuccessful extraction
            audio.go("key", "main_011")
    else:
        # Document not scanned
        audio.go("key", "main_006")

    m_extract = False

    return


def access_n(path):

    global m_access, ext_flag, load_flag

    if ext_flag == True and load_flag == True:
        # Access document just scanned
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(access.begin, path)
    else:
        # Document not scaned or ectracted
        audio.go("key", "main_007")

    audio.go("key", "main_008")
    m_access = False

    return


def access_o():

    global m_access_old, ext_flag, load_flag, pointer_ud, back, select
    pointer_ud[1] = -1
    prev_point = pointer_ud[1]
    ext_flag = True

    while back == False:
        if ext_flag == True and load_flag == True:
            
            # Number of stored documents
            folders = next(os.walk("../library/"))[1]
            no_folders = len(folders)

            voice = "There are " + str(no_folders) + " stored documents, please use the up and down directions on the Dpad to find and select which document to access and press Y to select"
            audio.go("raw", voice)
            
            # Select which document to access
            while pointer_ud[1] >= -2 and pointer_ud[1] <= no_folders and select == False and back == False:
                if pointer_ud[1] != prev_point and pointer_ud[1] != no_folders and pointer_ud[1] > -1:
                    with open('../library/' + str(folders[pointer_ud[1]]) + '/access.JSON', 'r') as f:
                        data = dict(json.load(f))
                    topic = data["page"][0]["topic"]
                    voice = "This is document " + str(folders[pointer_ud[1]]) + ", and it is about " +  topic
                    audio.go("raw", voice)
                    path = '../library/' + str(folders[pointer_ud[1]])
                    prev_point = pointer_ud[1]
                if pointer_ud[1] != prev_point and pointer_ud[1] == no_folders:
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
            
            if back == False:
                # Access document
                audio.go("key", "access_014")
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(access.begin, path)
                    back = True
        else:
            # Document not scanned or extracted
            audio.go("key", "main_007")
            break

    audio.go("key", "main_008")
    m_access_old = False
    select = False
    back = False

    return


def guisett(key, val):

    with open('gui.JSON', 'r') as f:
        data = dict(json.load(f))
    
    data[key] = val

    with open('gui.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return

    
if __name__ == '__main__':

    audio.go("key", "main_001")
    
    # Declare and initialise 
    global back, select, path, ext_flag, load_flag, path, pointer_ud, pointer_lr, m_scan, m_extract, m_access, m_access_old
    pointer_ud = [-1, -1]
    pointer_lr = [-1, -1]
    back = False
    m_scan = False
    m_extract = False
    m_access = False
    m_access_old = False
    ext_flag = False
    load_flag = False
    select = False
    path = ""

    # GUI
    p = Process(target=gui.run, args=(True,))
    p.start()
    guisett("loc","main")
    guisett("speech", "")
    guisett("microphone", "")

    xboxContM = XboxController.XboxController(
        controllerCallBack = CallBackM,
        joystickNo = 0,
        deadzone = 0.1,
        scale = 1,
        invertYAxis = False)

    xboxContM.start()

    audio.go("key", "main_002")

    # System begins operation
    while back == False:

        if m_scan == True:
            scan(xboxContM)

        if m_extract == True:
            extract()

        if m_access == True:
            access_n(path)

        if m_access_old == True:
            access_o()

        pass

    # System shuts down
    audio.go("key", "main_004")
    p.terminate()
    xboxContM.stop()
