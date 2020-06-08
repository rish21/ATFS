#!python
# coding: utf-8

# Imports
import tables
import blocks
import image_insights
import plotdigitizer
import graph_insights
import graph_audio
import text
import equations
import time
import audio


def run():

    audio.go("key", "extraction_001")
    start = time.time()

    try:
        # Set true if debugging information is required
        #info = True

        # Step 1 - Extract tables from page
        #tables.get(info)

        # Step 2 - Extract blocks
        blocks.get()

        # Step 3 - Get insights for the images extracted
        image_insights.get()

        # Step 4 - Extract data points from graphs
        plotdigitizer.get()

        audio.go("key", "extraction_002")

        # Step 5 - Get insights for graph trends extracted
        graph_insights.get()

        # Step 5 - Synthesise audio files for graph
        graph_audio.get()

        # Step 6 - OCR text extraction
        text.get()

        # Step 7 - Extract equations
        equations.get()

        # Step 8 - Perform NLP Content analysis

    except:
        audio.go("key", "extraction_004")
        return False
    
    print('It took', time.time()-start, 'seconds.')
    audio.go("key", "extraction_003")

    return True


if __name__ == '__main__':

    run()