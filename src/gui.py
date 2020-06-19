#!/usr/bin/env python

# Import
import PySimpleGUI as sg
import time
import random
import json

def LEDIndicator(key=None, radius=30):

    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)


def SetLED(window, key, color):

    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)
    
    return


def run(debug):

    sg.theme('Dark')
    sg.list_of_look_and_feel_values()

    layout = [[sg.Text('LIVE DASHBOARD',
                size=(90,1),
                background_color='Green',
                auto_size_text=True,
                justification='center')],

            [sg.Text('Back'), LEDIndicator('_back_'),
            sg.Text('XBOX'), LEDIndicator('_xbox_'),
            sg.Text('Start'), LEDIndicator('_start_')],

            [sg.Text('A'), LEDIndicator('_a_'),
            sg.Text('B'), LEDIndicator('_b_'),
            sg.Text('X'), LEDIndicator('_x_'),
            sg.Text('Y'), LEDIndicator('_y_')],
            
            [sg.Text('Left Shoulder'), LEDIndicator('_lb_'),
            sg.Text('Right Shoulder'), LEDIndicator('_rb_')],

            [sg.Text('Left Thumb'), LEDIndicator('_lt_'),
            sg.Text('Right Thumb'), LEDIndicator('_rt_')],

            [sg.Text('DPad Up'), LEDIndicator('_du_'),
            sg.Text('DPad Down'), LEDIndicator('_dd_'),
            sg.Text('DPad Left'), LEDIndicator('_dl_'),
            sg.Text('DPad Right'), LEDIndicator('_dr_')],

            [sg.Text('SYSTEM LOC', size=(20,1)), sg.Text(key='-LOC-',
                size=(60,1),
                background_color='DarkBlue',
                auto_size_text=True,
                justification='center')],
            [sg.Text('AUDIO OUT', size=(20,1)), sg.Text(key='-SPEECH-',
                size=(60,1),
                background_color='DarkBlue',
                auto_size_text=True,
                justification='center')],
            [sg.Text('SPEECH INPUT', size=(20,1)), sg.Text(key='-MICROPHONE-',
                size=(60,1),
                background_color='DarkBlue',
                auto_size_text=True,
                justification='center')],

            [sg.Button('Exit')]]

    window = sg.Window('ATF-STEM DASHBOARD', layout, default_element_size=(12, 1), auto_size_text=False, finalize=True)

    i = 0
    while debug == True:
        event, value = window.read(timeout=400)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            debug = False
        if value is None:
            debug = False
        i += 1

        with open('gui.JSON', 'r') as f:
            data = dict(json.load(f))

        window['-LOC-'](data["loc"])
        window['-SPEECH-'](data["speech"])
        window['-MICROPHONE-'](data["microphone"])

        SetLED(window, '_a_', data["a"])
        SetLED(window, '_b_', data["b"])
        SetLED(window, '_x_', data["x"])
        SetLED(window, '_y_', data["y"])

        SetLED(window, '_lb_', data["lb"])
        SetLED(window, '_rb_', data["rb"])

        SetLED(window, '_back_', data["back"])
        SetLED(window, '_start_', data["start"])
        SetLED(window, '_xbox_', data["xbox"])

        SetLED(window, '_lt_', data["lt"])
        SetLED(window, '_rt_', data["rt"])

        SetLED(window, '_du_', data["du"])
        SetLED(window, '_dd_', data["dd"])
        SetLED(window, '_dl_', data["dl"])
        SetLED(window, '_dr_', data["dr"])
    
    window.close()

    return


if __name__ == '__main__':

    debug = True
    run(debug)