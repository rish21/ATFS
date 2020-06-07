#!python
# coding: utf-8

# Imports
import XboxController
import audio
import scanner
import extraction

# Controller Callback
def CallBack(controlId, value):

    if controlId == 13 and value == 0:
        #scanner.run()
        global cont
        cont = True
        audio.go("key", "main_003")

    if controlId == 14 and value == 0:
        global end
        end = True
        print("Program Stopping")

    if controlId == 6 and value == 0 and cont == True:
        extraction.run()

    if controlId == 9 and value == 0:
        print("ok")

    return


if __name__ == '__main__':

    audio.go("key", "main_001")

    global end, cont
    end = False
    cont = False

    xboxCont = XboxController.XboxController(
        controllerCallBack = CallBack,
        joystickNo = 0,
        deadzone = 0.1,
        scale = 1,
        invertYAxis = False)

    xboxCont.start()

    audio.go("key", "main_002")

    while end == False:
        pass

    xboxCont.stop()