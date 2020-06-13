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
import audio
import json

path = 'temp/csv/'

def graph_values(data):

    vx = []
    vy = []

    for d in data:
        vx.append(d[0])
        vy.append(d[1])
    
    x = np.array(vx, dtype=np.float128)
    y = np.array(vy, dtype=np.float128)

    return x, y


def graph_audio_values(x, y, fn):

    with open('temp/access.JSON', 'r') as f:
        data = dict(json.load(f))

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
            counter = counter + int(data["settings"][0]["window"])
        except:
            done = True
            pass
    
    store_json(len(valx), fn)

    return valx, valy, ragx, ragy


def store_json(insert, n):

    with open('temp/access.JSON', 'r') as f:
        data = dict(json.load(f))

        data["page"][0]["misc"].append({n:""})
        data["page"][0]["misc"][n][n] = insert

    with open('temp/access.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


def graph_audio_point(valx, valy, maxx, maxy, p, n):

    synth = chippy.Synthesizer(framerate=44100)
    loc = "temp/audio/"

    fp = 2000 * (float(valx[p]) / float(maxx))
    ap = 1 * (float(valy[p]) / float(maxy))
    sine_wave = synth.sine_pcm(length=1, frequency=fp, amplitude=ap)
    synth.save_wave(sine_wave, loc + "temp_s"  + str(n) + ".wav")

    audio.play( loc + "temp_s"  + str(n) + ".wav")

    return 


def graph_audio_full(valx, valy, maxx, maxy, n):

    synth = chippy.Synthesizer(framerate=44100)
    once = False
    loc = "temp/audio/"

    fp = 2000 * (float(valx[0]) / float(maxx))
    ap = 1 * (float(valy[0]) / float(maxy))
    sine_wave = synth.sine_pcm(length=1, frequency=fp, amplitude=ap)
    synth.save_wave(sine_wave, loc + "temp_p"  + str(n) + ".wav")

    for v in range(1, len(valx) - 1):

        fn = 2000 * (float(valx[v]) / float(maxx))
        an = 20 * (float(valy[v]) / float(maxy))
        sine_wave = synth.sine_pcm(length=0.1, frequency=fn, amplitude=an)
        synth.save_wave(sine_wave, loc + "temp_n" + str(n) + ".wav")

        if once == False:
            temp_prev = AudioSegment.from_wav(loc + "temp_p"  + str(n) + ".wav")
            temp_next = AudioSegment.from_wav(loc + "temp_n" + str(n) + ".wav")

            combined_sounds = temp_prev + temp_next
            combined_sounds.export(loc + "final"  + str(n) + ".wav", format="wav")
            once = True
        else:
            temp_prev = AudioSegment.from_wav(loc + "final"  + str(n) + ".wav")
            temp_next = AudioSegment.from_wav(loc + "temp_n" + str(n) + ".wav")

            combined_sounds = temp_prev + temp_next
            combined_sounds.export(loc + "final"  + str(n) + ".wav", format="wav")


def get(select, p):

    print("pkg_GRAPH_AUDIO - Synthesising audio for the graph data")

    no_files = next(os.walk(path))[2]

    #try:
    for n, f in enumerate(no_files):

        filePath = path + str(n) + '.csv'

        with open(filePath, newline='') as csvfile:
            im = csv.reader(csvfile, delimiter=' ', quotechar='|')
            data = list(im)

        valx, valy = graph_values(data)

        vx, vy, ragx, ragy = graph_audio_values(valx, valy, n)

        if select == 0:
            graph_audio_full(vx, vy, ragx, ragy, n)
        elif select == 1:
            graph_audio_point(vx, vy, ragx, ragy, p, n)

    #except:
    #    print("ERR - Invalid file")


if __name__ == '__main__': 

    p = 0
    get(0, p)
