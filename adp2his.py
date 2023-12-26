    

from ast import Index
import gc
from math import ceil, floor
from time import sleep
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
from ADPFile import ADPFile
import pandas as pd
from datetime import datetime, timedelta
import io 
import numpy as np
import h5py
import hdf5plugin
import multiprocessing
from numba import jit
import warnings


files = ['D:\\adp\\KA1#2023_06_20_00_00-2023_06_20_23_59.adp',]
destFile = 'D:\\adp\\KA1@PTU1#2023_06_20_00_00-2023_06_20_23_59.his'

#@jit(nopython=True)
#def parseLine(idx, val, time, name):
#    nLine = []
#    print(name)
#    i = 0
#    for r, row in enumerate(idx):
#        #try:
#        if len(nLine) < len(idx):
#            if floor(time[i]) == idx[r]:
#                nLine.append(val[i])
#                i += 1
#            elif floor(time[i]) > idx[r]:
#                nLine.append(val[i-1])
#            else:
#                while not floor(time[i]) > idx[r]:
#                    if floor(time[i+1]) >= idx[r+1] and len(nLine) < len(idx):
#                        nLine.append((val[i]))
#                    i += 1
#        #except:
#        #    pass

#    if len(idx)>len(nLine):
#        for i in range(len(idx)-len(nLine)):
#            nLine.append(nLine[len(nLine)-1])

#    return nLine, name


@jit(nopython=True)
def parseLine_alt(idx, val, time, name):
    nLine = []
    print(name)
    i = 0
    for r, row in enumerate(idx):
        if r==0:
            nLine.append(val[0])
        elif r==len(idx) - 1:
            nLine.append(val[len(val)-1])
        else:
            while row > time[i]:
                i+=1
                if i >= len(time):
                    continue
            nLine.append(val[i])

    return nLine, name
    

def parseLineWrapper(idx, line, namesDict):
    lineName = namesDict[line.iloc[0]['nodeid']]
    line['actualtime'] = (line['actualtime']/10**9)
    val_ = np.array(line['valdouble'], dtype=np.single)
    time_ = np.array(line['actualtime'], dtype=np.uint32)
    idx_ = np.array(idx.index.values, dtype=np.uint32)
    a, b = parseLine_alt(idx_, val_, time_, lineName)
    return a, b

if __name__ == '__main__':

    warnings.simplefilter(action='ignore')

    res = pd.DataFrame()

    for file in files:

        print(file)

        namesData = pd.DataFrame()
        adpFiles = []
        adp = ADPFile(file)
        namesData = pd.read_csv(io.StringIO(adp.getNamesData()))
        dataFrame = adp.getSignalsData().copy()
        fileName = adp.getFileName()
        del adp
        gc.collect()

        nodeids = dataFrame['nodeid'].copy()
        nodeids = nodeids.drop_duplicates()

        namesDict = {}
        for line in namesData.iloc:
            namesDict[line['nodeid']] = line['tagname']

        linesDFs = []
        for i, nid in enumerate(nodeids):
            lineDF = dataFrame.loc[dataFrame['nodeid'] == nid].copy()
            linesDFs.append(lineDF)

        baseDT = int((round(lineDF.iloc[0]['actualtime']/10**11)) * 100.0)
        maxDT = int((round(lineDF.iloc[len(lineDF)-1]['actualtime']/10**11)) * 100.0)
        print('BaseDT', baseDT, 'MaxDT', maxDT)

        res['actualtime'] = range(baseDT, maxDT)
        res.set_index('actualtime', inplace=True)

        for line in linesDFs:
            a,b = parseLineWrapper(res, line, namesDict)
            res[b] = a

    print('Write ADP')

    h5File = h5py.File(destFile, 'w')
    h5File.create_dataset('data/actualtime', data=res.index, dtype=np.uint64, **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))
    for key in res.keys():
        h5File.create_dataset('data/' + key, data=res[key], dtype=np.single, **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))
    h5File.close()

    print('Done!')
   
