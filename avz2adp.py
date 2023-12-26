


fileName = 'D:\\gas_trends.avz'
fileNameDest = fileName.replace('.avz','.adp')

from datetime import datetime
import zipfile
import json
import pandas as pd
import os
import h5py
import hdf5plugin

class trendData:
    def __init__(self):
        self.AxisMin = 0
        self.AxisMax = 0
        self.Description = ''
        self.Tag = ''
        self.Units = ''
        self.LineColor = ''
        self.IndexAxis = ''

trendDatas = []

avzFile = zipfile.ZipFile(fileName)

for zi in avzFile.filelist:
    if zi.filename == '00.json':
        mainJson = json.load(avzFile.open(zi, 'r'))
        for line in range(int(mainJson['LinesCount'])):
            td = trendData()
            td.AxisMin = mainJson['AxisMin'][line+1]
            td.AxisMax = mainJson['AxisMax'][line+1]
            td.Description = mainJson['Description'][line]
            td.Tag = mainJson['Tag'][line]
            td.Units = mainJson['Units'][line]
            td.LineColor = mainJson['LineColor'][line]
            td.IndexAxis = mainJson['IndexAxis'][line]
            trendDatas.append(td)
    break

# Trends.ini

iniData = '[TRENDS]\n'
iniData += '\n'
iniData += 'DEVICE_1=Устройство;\n'
iniData += 'Group_1_1=' + os.path.split(fileName)[1] + ';\n'
iniData += 'Subgroup_1_1_1=' + os.path.split(fileName)[1] + ';\n'
for i, td in enumerate(trendDatas):
    iniData += 'Trend_1_1_1_' + str(i+1) + '=KIP=id' + str(td.IndexAxis) + ';TAG=' + td.Tag + ';COMMENT=' +\
    td.Description + ';UNIT=' + td.Units + ';FORMAT=2;HLM=' + str(td.AxisMax) + ';LLM=' + str(td.AxisMin) + '#\n'

# names.csv
namesData = 'nodeid,tagname\n'
for td in trendDatas:
    namesData += str(td.IndexAxis) + ',' + td.Tag + '\n'

valsList = []
timesList = []
idsList = []

for td in trendDatas:
    trend = json.load(avzFile.open(str(td.IndexAxis)+'.json'))
    for line in range(len(trend['col_1'])):
        idsList.append(int(td.IndexAxis))
        timesList.append(float(trend['col_2'][line])*10**6)
        if int(trend['col_1'][line]) == 192:
            valsList.append(float(trend['col_0'][line]))
        else:
            valsList.append(None)

# Write adp file
h5File = h5py.File(fileNameDest, 'w')
h5File.create_dataset('/names.csv', data = namesData)
h5File.create_dataset('/Trends.ini', data = iniData)
hd5ItemTime =  timesList
mintime = datetime.fromtimestamp(min(timesList)/10**9).strftime("%Y/%m/%d %H:%M:%S")
maxtime = datetime.fromtimestamp(max(timesList)/10**9).strftime("%Y/%m/%d %H:%M:%S")
h5File.attrs.create('minDateTime', mintime)
h5File.attrs.create('maxDateTime', maxtime)
h5File.attrs.create('formatVersion', 1)
hd5ItemId = idsList
hd5ItemVal = valsList

h5File.create_dataset('data/actualtime', data=hd5ItemTime, **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))
h5File.create_dataset('data/nodeid', data=hd5ItemId, **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))
h5File.create_dataset('data/valdouble', data=hd5ItemVal, **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))

h5File.close()

