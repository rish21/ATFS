#!python
# coding: utf-8

# Imports
import tables
import blocks
import image_insights
import adj_plotdigitizer
import graph_insights
import graph_audio
import text
import equations
import time
import audio
import nlp
import os
import shutil
import glob
import json


def run():

    guisett("loc","extraction")

    #audio.go("key", "extraction_001")
    startt = time.time()

    with open('standard.JSON', 'r') as f:
        data = dict(json.load(f))

    with open('temp/access.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    try:
        # Set true if debugging information is required
        info = False

        # Step 1 - Extract tables from page
        tables.get(info)
        print('Tables - It took', time.time()-startt, 'seconds.')
        start = time.time()

        # Step 2 - Extract blocks
        blocks.get()
        print('Blocks - It took', time.time()-start, 'seconds.')
        start = time.time()

        # Step 3 - Get insights for the images extracted
        image_insights.get()
        print('Images - It took', time.time()-start, 'seconds.')
        start = time.time()

        # Step 4 - Extract data points from graphs
        adj_plotdigitizer.get()
        print('Graph - It took', time.time()-start, 'seconds.')
        start = time.time()

        #audio.go("key", "extraction_002")

        # Step 5 - Get insights for graph trends extracted
        graph_insights.get(info)
        print('Graph desc - It took', time.time()-start, 'seconds.')
        start = time.time()

        # Step 5 - Synthesise audio files for graph
        graph_audio.get(0, None)
        print('Graph audio - It took', time.time()-start, 'seconds.')
        start = time.time()

        # Step 6 - OCR text extraction
        text.get()
        print('Text - It took', time.time()-start, 'seconds.')
        start = time.time()

        # Step 7 - Extract equations
        equations.get()
        print('Equations - It took', time.time()-start, 'seconds.')
        start = time.time()

        # Step 8 - Perform NLP analysis - summarisation & content analysis
        nlp.get()
        print('NLP - It took', time.time()-start, 'seconds.')
        start = time.time()

        # Store all the extracted information
        path = store()

    except:
        #audio.go("key", "extraction_004")
        print("issue")
        return False
    
    print('Final - It took', time.time()-startt, 'seconds.')
    #audio.go("key", "extraction_003")

    return True, path


def store():

    # Number of documents stored
    path = "../library/"
    folder_no = len(next(os.walk(path))[1])
    path = path + str(folder_no)

    # Store extracted document to library
    os.mkdir(path)

    shutil.copy("temp/access.JSON", path)

    src = "temp/csv/"
    dst = path + "/csv/"
    os.mkdir(dst)
    
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)

    src = "temp/audio/"
    dst = path + "/audio/"
    os.mkdir(dst)
    
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
        else:
            shutil.copy2(s, d)

    return path


def guisett(key, val):

    with open('gui.JSON', 'r') as f:
        data = dict(json.load(f))
    
    data[key] = val

    with open('gui.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


if __name__ == '__main__':

    run()
    #store()
