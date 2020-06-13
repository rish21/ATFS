#!python
# coding: utf-8

# Imports
import json
from gensim.summarization.summarizer import summarize 


def summ():

    with open('temp/access.JSON', 'r') as f:
        data = dict(json.load(f))

    text = data["page"][0]["description"]
    print(text)

    summ_p = summarize(text, ratio = 10) 
    summ_w = summarize(text, word_count = 50) 

    data["page"][0]["description"] = summ_w

    with open('temp/access.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return summ_w


if __name__ == '__main__':

    out = summ()
    print(out)
