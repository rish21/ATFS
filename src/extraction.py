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


def run():

    #audio.go("key", "extraction_001")
    startt = time.time()

    try:
        # Set true if debugging information is required
        info = False

        # Step 1 - Extract tables from page
        #tables.get(info)
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
        graph_insights.get()
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

        # Step 8 - Perform NLP analysis - summarisation
        nlp.summ()
        print('Summarisation - It took', time.time()-start, 'seconds.')
        start = time.time()

    except:
        #audio.go("key", "extraction_004")
        print("issue")
        return False
    
    print('Final - It took', time.time()-startt, 'seconds.')
    #audio.go("key", "extraction_003")

    return True


if __name__ == '__main__':

    run()