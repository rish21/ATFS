#!python
# coding: utf-8

# Imports
import tables
import items
import image_insights
import plotdigitizer
import graph_insights
import graph_audio
import OCR
import equations

import time

def run():

    start = time.time()

    # Set true if debugging information is required
    info = True

    # Step 1 - Extract tables from page
    tables.get(info)

    # Step 2 - Extract items (graphs and images)
    items.get()

    # Step 3 - Get insights for the images extracted
    image_insights.get()

    # Step 4 - Extract data points from graphs
    plotdigitizer.get()

    # Step 5 - Get insights for graph trends extracted
    graph_insights.get()

    # Step 5 - Synthesise audio files for graph
    graph_audio.get()

    # Step 6 - OCR text extraction
    OCR.get()

    # Step 7 - Extract equations
    equations.get()

    # Step 8 - Perform NLP Content analysis

    

    # Step 9 - Controls 


    # Storage


    print('It took', time.time()-start, 'seconds.')

    return


if __name__ == '__main__':

    run()