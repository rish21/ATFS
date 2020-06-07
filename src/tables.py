#!python
# coding: utf-8

# Imports
from camelot_pro import check_usage
from camelot_pro import read_pdf
import csv

# API key for Camelot
api_key = '44DOdk4yMG7m7v9pFmEpm3dxCW2QUm568mA0RbyG'

def get(info):

    print("pkg_TABLES - Extracting tables")

    # Request for the tables from the page to be extracted and stored
    pro_tables = read_pdf('temp/1.jpg', flavor="CamelotPro", pro_kwargs={'api_key': api_key}) 
    pro_tables.export('temp/temp.csv', f='csv')

    # Print out request information
    if info == True:
        #pro_tables.JobStatus
        #pro_tables
        print(check_usage(api_key))

    return

if __name__ == '__main__':

    info = True

    get(info)