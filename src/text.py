#!python
# coding: utf-8

# Imports
import cv2
import sys
import re
import pdb
import time
import json
import csv
import pytesseract
#from pylanguagetool import api

path = 'temp/scanned'

def tess_detect(img):

    # '-l eng'  for using the English language
    # '--oem 1' for using LSTM OCR Engine
    config = ('-l eng --oem 1 --psm 3')

    start = time.time()

    text = pytesseract.image_to_string(img, config=config)
    
    #print('It took', time.time()-start, 'seconds.')

    return text

def boxes_char(img):
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    #cv2.imshow('letters', img)
    cv2.imwrite('temp/letters.jpg', img)
    cv2.waitKey(0)


def boxes_words(img):

    d = pytesseract.image_to_data(img, output_type='dict')

    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #cv2.imshow('words', img)
    cv2.imwrite('temp/words.jpg', img)
    cv2.waitKey(0)


def correct(text):

    correct = api.check(text, api_url='https://languagetool.org/api/v2/', lang='en-GB')

    while len(correct.get('matches')) < 0:
        wrn = correct.get('warnings')
        err = correct.get('matches')[0]['message']
        conf = correct.get('language').get('correctectedLanguage').get('confidence')

        chg = correct.get('matches')[0]['replacements'][0]['value']
        offset = correct.get('matches')[0]['context']['offset']
        length = correct.get('matches')[0]['context']['length']

        if correct.get('matches')[0]['replacements'][0]['value'] == "":
            p1 = text[:offset+1]
            p2 = text[offset+length:]
            text = p1 + chg + p2
        else:
            p1 = text[:offset]
            p2 = text[offset+length:]
            text = p1 + chg + p2

        correct = api.check(text, api_url='https://languagetool.org/api/v2/', lang='en-GB')

    return correct


def store_json(store, check, data):

    with open('temp/access.JSON', 'r') as f:
        data = dict(json.load(f))
        
    store = re.split('\n\n', store)

    for A,  c in enumerate(store):
        if check == True and c == data:
            pass
        elif c == "" and c == " ":
            pass
        else:
            data["page"][0]["sections"].append({"full_text": "","nlp":[],"sentences": []})
            c = re.sub('\n', ' ', c)
            data["page"][0]["sections"][A]["full_text"] = c
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', c)

            for B, s in enumerate(sentences):
                data["page"][0]["sections"][A]["sentences"].append({"text": "","highlighted": ""})
                data["page"][0]["sections"][A]["sentences"][B]["text"] = s

    with open('temp/access.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


def check_table():

    line = ""
    check = False

    try:
        with open('temp/scanned-page-1-table-1.csv', newline='') as csvfile:
            im = csv.reader(csvfile, delimiter=' ', quotechar='|')
            tables = list(im)

        for A,  rows in enumerate(tables):
            for B, cols in enumerate(rows):
                q = re.sub('"', '', cols)
                c = re.sub(',', ' ', q)
                line = line + c
            line = line + " "

        check = True
    except:
        pass

    return check, line

def get():

    print("pkg_OCR - Extracting text from page")

    global img
    img = cv2.imread(path + '.jpg', cv2.IMREAD_COLOR)

    text = tess_detect(img)
    #boxes_char(img)
    #boxes_words(img)
    check, data = check_table()
    #store = correct(text)
    store_json(text, check, data)

    return


if __name__ == '__main__':

    get()

