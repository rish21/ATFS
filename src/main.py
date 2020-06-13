#!python
# coding: utf-8

# Imports
import XboxController
import audio
import scanner
import extraction
import access
import concurrent.futures


# Controller Callback
def CallBackM(controlId, value):

    # Scan new document
    if controlId == 6 and value == 0:
        global ext_flag      
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(scanner.run,)
            ext_flag = future.result()
        audio.go("key", "main_008")
        if ext_flag == True:
            audio.go("key", "main_003")
        else:
            audio.go("key", "main_010")
        
    # Run extraction if a document has been scanned
    if controlId == 8 and value == 0 and ext_flag == True:
        audio.go("key", "main_005")
        global load_flag
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(extraction.run,)
            load_flag = future.result()
        audio.go("key", "main_008")
        if load_flag == True:
            audio.go("key", "main_009")
        else:
            audio.go("key", "main_011")
    elif controlId == 8 and value == 0 and ext_flag == False:
        audio.go("key", "main_006")

    # Load current document
    if controlId == 7 and value == 0 and load_flag == True:
        print("ok")
    elif controlId == 7 and value == 0 and ext_flag == False:
        audio.go("key", "main_007")

    # Load old document Y
    if controlId == 9 and value == 0:
        print("access")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(access.begin,)
        print("main")

    # Stop program
    if controlId == 12 and value == 0:
        global end
        end = True
        #audio.go("key", "main_004")
        print("Program Stopping")

    return


if __name__ == '__main__':

    #audio.go("key", "main_001")

    global end, ext_flag, load_flag
    end = False
    ext_flag = False
    load_flag = False

    xboxContM = XboxController.XboxController(
        controllerCallBack = CallBackM,
        joystickNo = 0,
        deadzone = 0.1,
        scale = 1,
        invertYAxis = False)

    xboxContM.start()

    #audio.go("key", "main_002")

    while end == False:
        pass

    xboxContM.stop()
