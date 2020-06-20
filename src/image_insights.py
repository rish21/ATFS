#!python
# coding: utf-8

# Imports
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import json

path = 'temp/blocks/images/'

def get():

    print("pkg_IMAGE_INSIGHTS - Getting insights for detected images")

    # Try for all images extracted
    results=[]
    no_files = next(os.walk(path))[2]

    for n, f in enumerate(no_files):
        
        # Upload the image to google search and grab the new URL
        filePath = path + str(n) + '.jpg'
        searchUrl = 'http://www.google.hr/searchbyimage/upload'
        multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers['Location']

        # Open this new URL in a headless browser so that we can access the results
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
        driver.get(fetchUrl)

        # Extract the information we need 
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.findAll('div', attrs={'class':'r5a77d'}):
            extract=a.find('a', href=True, attrs={'class':'fKDtNb'})
            results.append(extract.text) 
        
    # Store the results in the JSON access file
    store_json(results)

    return results


def store_json(results):

    # Store image descriptions in JSON
    with open('standard.JSON', 'r') as f:
        data = dict(json.load(f))

    for n, r in enumerate(results):
        data["page"][0]["image_results"].append({n:""})
        data["page"][0]["image_results"][n][n] = r 

    with open('temp/access.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


if __name__ == '__main__':

    get()