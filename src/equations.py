#!python
# coding: utf-8

# Imports
from mathpix.mathpix import MathPix
import os
import json

# Credentials
idd = 'rmanjunatha2198_gmail_com_79187c'
key = '859985511757a53ddc2b'

path = 'temp/blocks/'

def process(filePath):

    store = ""

    try:
        mathpix = MathPix(app_id=idd, app_key=key)
        ocr = mathpix.process_image(image_path=filePath)
        store = str(ocr.latex)
    except:
        pass

    return store


def store_json(results):

    with open('temp/access.JSON', 'r') as f:
        data = dict(json.load(f))

    for n, r in enumerate(results):
        data["page"][0]["equations"].append({n:""})
        data["page"][0]["equations"][n][n] = results[n]

    with open('temp/access.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


def get():

    print("pkg_Equations - Extracting equations images")

    results = []
    no_files = next(os.walk(path))[2]

    try:
        for n, f in enumerate(no_files):

            filePath = path + str(n) + '.jpg'
            
            check = process(filePath)
            if check:
                results.append(check)
        
        store_json(results)
    except:
        print("ERR - Invalid file")

    return


if __name__ == '__main__':

    get()
