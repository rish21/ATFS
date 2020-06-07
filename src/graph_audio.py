#!python
# coding: utf-8

# Imports
import csv
import chippy
import io
from pydub import AudioSegment
from scipy.signal import savgol_filter
import numpy as np 
import os


def graph_values(data):

    vx = []
    vy = []

    for d in data:
        vx.append(d[0])
        vy.append(d[1])
    
    x = np.array(vx, dtype=np.float128)
    y = np.array(vy, dtype=np.float128)

    return x, y


def sg_filter(x, y):

    win_len = len(y)
    win_len = int(win_len / 3)
    if (win_len % 2) == 0:
        win_len = win_len -1

    fx = savgol_filter(x, win_len, 2)
    fy = savgol_filter(y, win_len, 2)

    return fx, fy


def graph_audio_values(x, y):

    valx, valy = [], []

    maxx = x[0]
    maxy = y[1]
    minx = x[0]
    miny = y[1]

    for n, d in enumerate(x):
        if x[n] > maxx:
            maxx = x[n]
        if y[n] > maxy:
            maxy = y[n]
        if x[n] < minx:
            minx = x[n]
        if y[n] < miny:
            miny = y[n]

    ragx = maxx - minx
    ragy = maxy - miny

    counter = 0
    done = False
    while done == False:
        try:
            valx.append(x[counter])
            valy.append(y[counter])
            counter = counter + 2
        except:
            done = True
            pass
    
    return valx, valy, ragx, ragy


def graph_audio(valx, valy, maxx, maxy):

    synth = chippy.Synthesizer(framerate=44100)
    once = False
    loc = "temp/audio/"

    fp = 2000 * (float(valx[0]) / float(maxx))
    ap = 1 * (float(valy[0]) / float(maxy))
    sine_wave = synth.sine_pcm(length=1, frequency=fp, amplitude=ap)
    synth.save_wave(sine_wave, loc + "temp_p.wav")

    for v in range(1, len(valx) - 1):

        fn = 2000 * (float(valx[v]) / float(maxx))
        an = 20 * (float(valy[v]) / float(maxy))
        sine_wave = synth.sine_pcm(length=0.1, frequency=fn, amplitude=an)
        synth.save_wave(sine_wave, loc + "temp_n.wav")

        if once == False:
            temp_prev = AudioSegment.from_wav(loc + "temp_p.wav")
            temp_next = AudioSegment.from_wav(loc + "temp_n.wav")

            combined_sounds = temp_prev + temp_next
            combined_sounds.export(loc + "final.wav", format="wav")
            once = True
        else:
            temp_prev = AudioSegment.from_wav(loc + "final.wav")
            temp_next = AudioSegment.from_wav(loc + "temp_n.wav")

            combined_sounds = temp_prev + temp_next
            combined_sounds.export(loc + "final.wav", format="wav")


def get():

    print("pkg_GRAPH_AUDIO - Synthesising audio for the graph data")

    path = 'temp/csv/'
    no_files = next(os.walk("temp/csv"))[2]

    try:
        for n, f in enumerate(no_files):

            filePath = path + str(n) + '.csv'

            with open(filePath, newline='') as csvfile:
                im = csv.reader(csvfile, delimiter=' ', quotechar='|')
                data = list(im)

            valx, valy = graph_values(data)

            x, y = sg_filter(valx, valy)

            valx, valy, ragx, ragy = graph_audio_values(x, y)

            graph_audio(valx, valy, ragx, ragy)

    except:
        print("ERR - Invalid file")


if __name__ == '__main__': 

    get()
