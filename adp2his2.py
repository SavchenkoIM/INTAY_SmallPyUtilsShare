    

import gc
from math import floor
from ADPFile import ADPFile
from ADPFile_UINT64 import ADPFile_UINT64
import pandas as pd
from datetime import datetime, timedelta
import io 
import numpy as np
import h5py
import hdf5plugin
from numba import jit
import warnings

dtStart = datetime(2023, 8, 10)
dtEnd = datetime(2023, 8, 21)

folder = 'D:\\hisadp\\'
#period = '2023_07_25_00_00-2023_07_25_23_59'

techs = ('KA1', 'OSO1', 'PTU1')

warnings.simplefilter(action='ignore')

@jit(nopython=True)
def parseLine(idx, val, time, name):
    nLine = []
    print(name, len(idx), len(val), type(val[0]), len(time))
    i = 0
    for r, row in enumerate(idx):
        #try:
            if len(nLine) < len(idx):
                if floor(time[i]) == idx[r]:
                    nLine.append(val[i])
                    i += 1
                elif floor(time[i]) > idx[r]:
                    nLine.append(val[i-1])
                else:
                    while not floor(time[i]) > idx[r]:
                        if r+1 >= len(idx) - 1 or i+1 >= len(val)-1:
                            break
                        if floor(time[i+1]) >= idx[r+1] and len(nLine) < len(idx):
                            nLine.append((val[i]))
                        i += 1
        #except:
        #    print('Error')
        #    pass

    if len(idx)>len(nLine):
        for i in range(len(idx)-len(nLine)):
            nLine.append(nLine[len(nLine)-1])

    return nLine, name

def parseLineWrapper(idx, line, namesDict):
    lineName = namesDict[line.iloc[0]['nodeid']]
    line['actualtime'] = (line['actualtime']/10**11) * 100.0
    if type(line['valdouble'][0]) == np.float32:
        val_ = np.array(line['valdouble'], dtype=np.single)
    else:
        val_ = np.array(line['valdouble'], dtype=np.uint64)
    time_ = np.array(line['actualtime'], dtype=np.uint32)
    idx_ = np.array(idx.index.values, dtype=np.uint32)
    a, b = parseLine(idx_, val_, time_, lineName)
    return a, b

for day in range((dtEnd-dtStart).days):
    _dtStart = dtStart + timedelta(days=day)
    period = _dtStart.strftime('%Y_%m_%d_00_00') + '-' + _dtStart.strftime('%Y_%m_%d_23_59')

    files = [folder+x+'#'+period+'.adp' for x in techs]

    destFile = folder+period+'.his'

    res = pd.DataFrame()

    for file in files:

        print(file)

        for valType in range(2):

            namesData = pd.DataFrame()
            adpFiles = []
            if valType == 0:
                adp = ADPFile(file)
            else:
                adp = ADPFile_UINT64(file)
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
                if (type(lineDF["valdouble"].iloc[0]) == np.float32 and valType == 0) or (type(lineDF["valdouble"].iloc[0]) == np.uint64 and valType == 1):
                    linesDFs.append(lineDF.reset_index())

            baseDT = int((round(lineDF.iloc[0]['actualtime']/10**11)) * 100.0)
            maxDT = int((round(lineDF.iloc[len(lineDF)-1]['actualtime']/10**11)) * 100.0)
            print('BaseDT', baseDT, 'MaxDT', maxDT)

            res['actualtime'] = range(baseDT, maxDT)
            res.set_index('actualtime', inplace=True)


            for line in linesDFs:
                a,b = parseLineWrapper(res, line, namesDict)
                res[b] = a
    

    print('Write HIS')

    h5File = h5py.File(destFile, 'w')
    h5File.create_dataset('data/actualtime', data=res.index, dtype=np.uint64, **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))
    for key in res.keys():
        if type(res[key].iloc[0]) == np.float32 or type(res[key].iloc[0]) == np.float64:
            h5File.create_dataset('data/' + key, data=res[key], dtype=np.single, **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))
        else:
            h5File.create_dataset('data/' + key, data=res[key], dtype=np.uint64, **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))
    h5File.close()

print('Done!')
   
