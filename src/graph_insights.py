#!python
# coding: utf-8

# Imports
import numpy as np 
from scipy.optimize import curve_fit 
from scipy.signal import savgol_filter
from matplotlib import pyplot as plt 
import operator
import csv
import json
import os
import pylab

path = 'temp/csv/'

def smoothList(list):

    # Moving average filter
    strippedXs = False
    degree = 5

    if strippedXs == True:
        return Xs[0:-(len(list)-(len(list)-degree+1))]

    smoothed = [0]*(len(list)-degree+1)

    for i in range(len(smoothed)):
        smoothed[i] = sum(list[i:i+degree])/float(degree)

    return smoothed

def smoothListTriangle(list):

    # Averaging triangular filter
    strippedXs = False
    degree = 5
    weight = []
    window = len(list)
    smoothed = [0.0]*(len(list)-window)

    for x in range(1, 2*degree):
        weight.append(degree-abs(degree-x))

    w = np.array(weight)

    for i in range(len(smoothed)):
        smoothed[i] = sum(np.array(list[i:i+window])*w)/float(sum(w))

    return smoothed

def smoothListGaussian(list):

    # Gaussian filter
    strippedXs = False
    degree = 5
    window = degree*2-1
    weight = np.array([1.0]*window)
    weightGauss = []

    for i in range(window):
        i = i-degree+1
        frac = i/float(window)
        gauss = 1/(np.exp((4*(frac))**2))
        weightGauss.append(gauss)

    weight = np.array(weightGauss)*weight
    smoothed = [0.0]*(len(list)-window)

    for i in range(len(smoothed)):
        smoothed[i] = sum(np.array(list[i:i+window])*weight)/sum(weight)

    return smoothed


def ord1(x, a, b):
    # Linear
    return (a * x) + b

def ord2(x, a, b, c):
    # Quadratic
    return (a * (x**2)) + (b * x) + c

def ord3(x, a, b, c, d):
    # Cubic
    return (a * (x**3)) + (b * (x**2)) + (c * x) + d

def expo(x, a, b, c):
    # Exponential
    return a * np.exp(-b * x) + c

def loga(x, a, b):
    # Logarithm
  return a * np.log(x) + b

def sinfn(x, a, b):
    # Sine
    return a * np.sin(b * x) 

def cosfn(x, a, b): 
    # Cosine
    return a * np.cos(b * x) 

def tanfn(x, a, b): 
    # Tangent
    return a * np.tan(b * x) 


def r2ed(param, x, y):

    # Coefficient of determination
    res = y - ord1(x, param[0], param[1])
    ss_res = np.sum(res**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)

    return r_squared

def graph_values(data):

    # Strip graph values from audio
    vx = []
    vy = []

    for d in data:
        vx.append(d[0])
        vy.append(d[1])
        
    x = np.array(vx, dtype=np.float128)
    y = np.array(vy, dtype=np.float128)

    return x, y


def sg_filter(xx, yy, n):

    # Savitzky–Golay filter
    win_len = len(yy)
    win_len = int(win_len / 2)
    if (win_len % 2) == 0:
        win_len = win_len -1

    fx = savgol_filter(xx, win_len, 1)
    fy = savgol_filter(yy, win_len, 1)

    fx = np.around(fx,decimals=5)
    fy = np.around(fy,decimals=5)

    data = np.column_stack((xx, fy))

    np.savetxt(path + str(n) + '.csv', data, delimiter=' ', fmt='%f')

    return fx, fy


def best_fit(show, x, y):

    # Fit graph to all functions
    rsquared = []
    polythresh = 0.95

    try:
        param, param_cov = curve_fit(ord1, x, y)
        ord1_y = ord1(x, param[0], param[1])
        res = y - ord1_y
        ss_res = np.sum(res**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        rsquared.append(1 - (ss_res / ss_tot))
    except:
        ord1_y = y
        rsquared.append(0)
        pass

    try:
        param, param_cov = curve_fit(ord2, x, y)
        ord2_y = ord2(x, param[0], param[1], param[2])
        res = y - ord2_y
        ss_res = np.sum(res**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        rsquared.append(1 - (ss_res / ss_tot))
    except:
        ord2_y = y
        rsquared.append(0)
        pass

    try:
        param, param_cov = curve_fit(ord3, x, y)
        ord3_y = ord3(x, param[0], param[1], param[2], param[3])
        res = y - ord3_y
        ss_res = np.sum(res**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        rsquared.append(1 - (ss_res / ss_tot))
    except:
        ord3_y = y
        rsquared.append(0)
        pass
    
    try:
        param, param_cov = curve_fit(expo, x, y)
        expo_y = expo(x, param[0], param[1], param[2])
        res = y - expo_y
        ss_res = np.sum(res**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        rsquared.append(1 - (ss_res / ss_tot))
    except:
        expo_y = y
        rsquared.append(0)
        pass

    try:
        param, param_cov = curve_fit(loga, x, y)
        loga_y = loga(x, param[0], param[1])
        res = y - loga_y
        ss_res = np.sum(res**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        rsquared.append(1 - (ss_res / ss_tot))
    except:
        loga_y = y
        rsquared.append(0)
        pass

    try:
        param, param_cov = curve_fit(sinfn, x, y)
        sinfn_y = sinfn(x, param[0], param[1])
        res = y - sinfn_y
        ss_res = np.sum(res**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        rsquared.append(1 - (ss_res / ss_tot))
    except:
        sinfn_y = y
        rsquared.append(0)
        pass

    try:
        param, param_cov = curve_fit(cosfn, x, y)
        cosfn_y = cosfn(x, param[0], param[1])
        res = y - cosfn_y
        ss_res = np.sum(res**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        rsquared.append(1 - (ss_res / ss_tot))
    except:
        cosfn_y = y
        rsquared.append(0)
        pass

    try:
        param, param_cov = curve_fit(tanfn, x, y)
        tanfn_y = tanfn(x, param[0], param[1])
        res = y - tanfn_y
        ss_res = np.sum(res**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        rsquared.append(1 - (ss_res / ss_tot))
    except:
        tanfn_y = y
        rsquared.append(0)
        pass

    # Identify best fit
    i, max_val = max(enumerate(rsquared), key=operator.itemgetter(1))

    # Cubic adjustment
    if i == 2 and max_val >= polythresh:
        if rsquared[1] >= polythresh:
            if rsquared[0] >= polythresh:
                i = 0
            else:
                i = 1

    # Quadratic adjustment
    if i == 1 and max_val >= polythresh:
        if rsquared[0] >= polythresh:
            i = 0

    # Plot
    if show == True:
        plt.plot(x, ord1_y, '-', color ='C2', label ="Linear")
        plt.plot(x, ord2_y, '-', color ='C3', label ="Quadratic")
        plt.plot(x, ord3_y, '-', color ='C4', label ="Cubic")
        plt.plot(x, expo_y, '-', color ='C5', label ="Exponential")
        plt.plot(x, loga_y, '-', color ='C6', label ="Log")
        plt.plot(x, sinfn_y, '-', color ='C7', label ="Sine")
        plt.plot(x, cosfn_y, '-', color ='C8', label ="Cosine")
        plt.plot(x, tanfn_y, '-', color ='C9', label ="Tangent")
        plt.legend() 
        plt.show() 

    return i


def store_json(results):

    # Store model function in JSON
    store = ["Linear function","Quadratic function","Cubic function","Exponential function","Logarithmic function","Sine function","Cosine function","Tangent function"]

    with open('temp/access.JSON', 'r') as f:
        data = dict(json.load(f))

    for n, r in enumerate(results):
        data["page"][0]["graph_results"].append({n:""})
        data["page"][0]["graph_results"][n][n] = store[results[n]]

    with open('temp/access.JSON', 'w') as n:
        json.dump(data, n, indent=4, sort_keys=False)

    return


def get():

    print("pkg_GRAPH_INSIGHTS - Getting insights for graphs")

    # Try for all graphs extracted
    results = []
    no_files = next(os.walk("temp/csv"))[2]

    try:
        for n, f in enumerate(no_files):

            filePath = path + str(n) + '.csv'

            with open(filePath, newline='') as csvfile:
                im = csv.reader(csvfile, delimiter=' ', quotechar='|')
                data = list(im)

            valx, valy = graph_values(data)
            #plt.plot(valx, valy, 'o', color ='C0', label ="Raw Data", markersize=2) 

            
            x, y = sg_filter(valx, valy, n)
            #plt.plot(valx, y, 'o', color ='C1', label ="Savgol Filter", markersize=2) 
            """
            y = smoothList(valy)
            plt.plot(x[:len(y)], y, 'o', color ='C2', label ="Average Filter", markersize=2) 
            
            y = smoothListTriangle(valy)
            plt.plot(x[:len(y)], y, 'o', color ='C3', label ="Triangle Filter", markersize=2) 

            y = smoothListGaussian(valy)
            plt.plot(x[:len(y)], y, 'o', color ='C4', label ="Gaussian Filter", markersize=2)
            """
            #plt.legend() 
            #plt.show() 

            results.append(best_fit(False, valx, valy))
                    
        store_json(results)

    except:
        print("ERR - No result")


if __name__ == '__main__':

    get()

