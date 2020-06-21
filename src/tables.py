#!python
# coding: utf-8

# Imports
from camelot_pro import check_usage
from camelot_pro import read_pdf
import csv
import json

# API key for Camelot
with open('standard.JSON', 'r') as f:
        data = dict(json.load(f))

api_key = data["keys"][0]["camelot"]

def get(info):

    print("pkg_TABLES - Extracting tables")

    # Request for the tables from the page to be extracted and stored
    pro_tables = read_pdf('temp/scanned.jpg', flavor="CamelotPro", pro_kwargs={'api_key': api_key}) 
    pro_tables.export('temp/csv/tables/tables.csv', f='csv')

    # Print out request information
    if info == True:
        #pro_tables.JobStatus
        #pro_tables
        print(check_usage(api_key))

    return

if __name__ == '__main__':

    info = True

    get(info)