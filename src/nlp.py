#!python
# coding: utf-8

# Imports
import os
import json
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from gensim.summarization.summarizer import summarize 


def content_analysis():

    with open('temp/access.JSON', 'r') as f:
        data = dict(json.load(f))

    text = data["page"][0]["description"]

    # Setup enviroment and instantiate client
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/home/rishmanju/fyp/Documents/static-forest-277817-d4e340a3e881.json'
    client = language_v1.LanguageServiceClient()

    # Configuration settings (text type, language and request)
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text, "type": type_, "language": language}

    # Request content classification
    response = client.classify_text(document)

    # Store topic
    try:
        topic = response.categories[0].name
        topic = topic.replace('/', ' ')
        data["page"][0]["topic"] = topic

        with open('temp/access.JSON', 'w') as n:
            json.dump(data, n, indent=4, sort_keys=False)
    except:
        print("No response")
        pass

    return response.categories[0]


def summ():

    # Get GENSIM TextRank summary
    with open('temp/access.JSON', 'r') as f:
        data = dict(json.load(f))

    text = data["page"][0]["description"]

    summ_w = summarize(text, word_count = 50) 

    data["page"][0]["description"] = summ_w

    with open('temp/access.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


def get():

    content_analysis()
    summ()

    return


if __name__ == '__main__':

    get()
