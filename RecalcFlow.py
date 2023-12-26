

from math import sqrt
from ADPFile import ADPFile
import io
import pandas as pd
from datetime import datetime, timedelta
import sys
import h5py
import hdf5plugin

inName = 'D:/adp/adpFile.adp'
outName = inName[:-4] + '_MOD.adp'

paramsToRecalc = [
                     {'AP':'root_KA1.PARAM_MON.KA1_AP_GasBefPZK_F1.PV_ARCHIVE', 'AT': 'root_KA1.PARAM_MON.KA1_AT_GasBefPZK_F1.PV_ARCHIVE',
                          'ADP': 'root_KA1.PARAM_MON.KA1_ADP_GasMain_F1.PV_ARCHIVE', 'AFV': 'root_KA1.PARAM_MON.KA1_AFV_nGasMain_F1.PV_ARCHIVE',
                          'COEFFS': {'C': 0.60206, 'Kp': 1, 'Kh': 1, 'E': 1.0208, 'Ksu': 1.00033, 'epsilon': 0.98593, 'd': 0.232113}},
                     {'AP':'root_KA1.PARAM_MON.KA1_AP_GasBefPZK_F1.PV_ARCHIVE', 'AT': 'root_KA1.PARAM_MON.KA1_AT_GasBefPZK_F1.PV_ARCHIVE',
                          'ADP': 'root_KA1.PARAM_MON.KA1_ADP_GasByp_F1.PV_ARCHIVE', 'AFV': 'root_KA1.PARAM_MON.KA1_AFV_nGasByp_F1.PV_ARCHIVE',
                          'COEFFS': {'C': 0.60446, 'Kp': 1.000045, 'Kh': 1.0045, 'E': 1.13734, 'Ksu': 1.00033, 'epsilon': 0.98886, 'd': 0.142856}},
                     {'AP':'root_KA1.PARAM_MON.KA1_AP_GasBefPZK_F2.PV_ARCHIVE', 'AT': 'root_KA1.PARAM_MON.KA1_AT_GasBefPZK_F2.PV_ARCHIVE',
                          'ADP': 'root_KA1.PARAM_MON.KA1_ADP_GasMain_F2.PV_ARCHIVE', 'AFV': 'root_KA1.PARAM_MON.KA1_AFV_nGasMain_F2.PV_ARCHIVE',
                          'COEFFS': {'C': 0.60206, 'Kp': 1, 'Kh': 1, 'E': 1.0208, 'Ksu': 1.00033, 'epsilon': 0.98593, 'd': 0.232113}},
                     {'AP':'root_KA1.PARAM_MON.KA1_AP_GasBefPZK_F2.PV_ARCHIVE', 'AT': 'root_KA1.PARAM_MON.KA1_AT_GasBefPZK_F2.PV_ARCHIVE',
                          'ADP': 'root_KA1.PARAM_MON.KA1_ADP_GasByp_F2.PV_ARCHIVE', 'AFV': 'root_KA1.PARAM_MON.KA1_AFV_nGasByp_F2.PV_ARCHIVE',
                          'COEFFS': {'C': 0.60446, 'Kp': 1.000045, 'Kh': 1.0045, 'E': 1.13734, 'Ksu': 1.00033, 'epsilon': 0.98886, 'd': 0.142856}}
                 ]
aggFlows = [ 
             {'AFV': 'root_KA1.PARAM_MON.KA1_AFV_Gas_F1.PV_ARCHIVE', 'AFV_1': 'root_KA1.PARAM_MON.KA1_AFV_nGasMain_F1.PV_ARCHIVE',
              'AFV_2': 'root_KA1.PARAM_MON.KA1_AFV_nGasByp_F1.PV_ARCHIVE'},
             {'AFV': 'root_KA1.PARAM_MON.KA1_AFV_Gas_F2.PV_ARCHIVE', 'AFV_1': 'root_KA1.PARAM_MON.KA1_AFV_nGasMain_F2.PV_ARCHIVE',
              'AFV_2': 'root_KA1.PARAM_MON.KA1_AFV_nGasByp_F2.PV_ARCHIVE'},
             {'AFV': 'root_KA1.PARAM_MON.KA1_AFV_Gas.PV_ARCHIVE', 'AFV_1': 'root_KA1.PARAM_MON.KA1_AFV_Gas_F1.PV_ARCHIVE',
              'AFV_2': 'root_KA1.PARAM_MON.KA1_AFV_Gas_F2.PV_ARCHIVE'}
           ]

if len(sys.argv) > 1:
    print('Name from command line args:', sys.argv[1])
    inName = sys.argv[1]
    outName = inName[:-4] + '_MOD.adp'

print(inName, '->', outName)
inFile = ADPFile(inName)

namesData = pd.read_csv(io.StringIO(inFile.getNamesData()))
signalsData = inFile.getSignalsData()
timeRaw = signalsData['actualtime']
signalsData['actualtime'] = pd.to_datetime(signalsData['actualtime'], unit='ns')

def findClosestPoint(refTime: datetime, currPtr: int, df: pd.DataFrame):
    
    ctr = currPtr
    prevDev = abs(df.iloc[ctr]['actualtime'] - refTime).total_seconds()

    while True:
        dev = abs(df.iloc[ctr]['actualtime'] - refTime).total_seconds()
        if prevDev < dev:
            return ctr-1, prevDev
        if ctr == len(df) - 1:
            return ctr, dev
        ctr += 1
        prevDev = dev

namesDict = {}
for line in namesData.iloc:
    namesDict[line['tagname']] = line['nodeid']

print('\n\nStart calculating flows')
for item in paramsToRecalc:

    print('====', item['AFV'], '====')

    AFV_mask = signalsData['nodeid'] == namesDict[item['AFV']]
    AF_ptr = min([i for i,x in enumerate(AFV_mask) if x])
    print('AF data pointer:', AF_ptr)

    AFV_Array = signalsData[signalsData['nodeid'] == namesDict[item['AFV']]]
    AP_Array = signalsData[signalsData['nodeid'] == namesDict[item['AP']]]
    ADP_Array = signalsData[signalsData['nodeid'] == namesDict[item['ADP']]]
    AT_Array = signalsData[signalsData['nodeid'] == namesDict[item['AT']]]

    AP_ctr = 0
    ADP_ctr = 0
    AT_ctr = 0

    for i in range(len(AFV_Array)):
        AF_time = AFV_Array.iloc[i]['actualtime']

        ADP_ctr, dev = findClosestPoint(AF_time, ADP_ctr, ADP_Array)
        if dev >= 1:
            print('Warning: ADP time deviation =', dev, 'seconds')
        AT_ctr, dev = findClosestPoint(AF_time, AT_ctr, AT_Array)
        if dev >= 1:
            print('Warning: AT time deviation =', dev, 'seconds')
        AP_ctr, dev = findClosestPoint(AF_time, AP_ctr, AP_Array)
        if dev >= 1:
            print('Warning: AP time deviation =', dev, 'seconds')

        #==================================BEGIN========================================
        c = item['COEFFS']

        DP = ADP_Array.iloc[ADP_ctr]['valdouble']
        P = AP_Array.iloc[AP_ctr]['valdouble']
        P /= 1000.0
        T = AT_Array.iloc[AT_ctr]['valdouble']
        pi = 3.1415926535898

        #===================================END_VARS====================================

        if DP < 0.01:
            DP= 0 
        _DP = DP * 1000.0 # Перевод в Па (для формулы СУ используются Па)
        _P = P + 0.101325 # Давление должно быть абсолютным
        _T = T

        # 1. Неисправность
        QCSF = False #DP_CSF or P_CSF or T_CSF
	        
        if T < -100:
           QCSF = True 

        # 2. Расчет плотности природного газа
        if not QCSF : 
            ro =( _P*1000*16.04 / (8.314*(_T + 273.15))) 
	        
        if ro < 0.0000001:
            QCSF = True 
		    # _P - в кПа
		    # _T - в К(кельвинах)
		    #16.04 - M – молярная масса природного газа
		    #8,314 - R – газовая постоянная 8,314 Дж/(моль·К),		

        # 3. Расчет расхода
        if not QCSF:
            if ro < 0.00001 : 
                Qvh = 0.0 
                Qmh = 0.0
                if P > 0.1 and DP > 0.1: # Т.е. если расход через диафрагму есть, а плотность среды отрицательная
                    QCSF = True
					        
            else:
                try:
                    alpha = c['Ksu'] * c['Ksu'] * c['C'] * c['E'] * c['Kh'] * c['Kp']  
                    _Qv = (pi / 4.0) * alpha * c['epsilon'] * (c['d'] * c['d']) * sqrt(2.0 * _DP / ro)
                    _Qm = (pi / 4.0) * alpha * c['epsilon'] * (c['d'] * c['d']) * sqrt(2.0 * _DP * ro)
                    if (0.0 <= _Qv and _Qv <= 100000.0) and (0.0 <= _Qm and _Qm <= 100000.0):
                        Qvh = _Qv * 3600.0 
                        Qmh = _Qm * 3600.0 / 1000.0 
                    else:
                        Qvh = 0.0 
                        Qmh = 0.0
                        QCSF = True
                except:
                    print(_DP, ro, _Qv)
                    raise

            
        # 4. Перевод расхода среды к нормальным условиями 0С и 101,325 кПа
        if not QCSF:
	        # Объемный расход в НУ, нм3/c	
            Qnu = _Qv*273.15*_P*1000/((273.15+_T)*101.325)	
	        # Объемный расход в НУ, нм3/ч
            Qnuh = Qnu*3600
		
	        # Объемный расход в стандартных условиях, ст.м3/c	
            Qsu = _Qv*(273.15+20.0)*_P*1000/((273.15+_T)*101.325)		
	        # Объемный расход в стандартных условиях, ст.м3/ч
            Qsuh = Qsu*3600			
        else:
            Qsuh = 0
            print('Warning: QCSF!')
        #==================================END==========================================

        signalsData.at[AF_ptr + i, 'valdouble'] = Qsuh

        if i % 10000 == 0:
            print(round((i*100.0)/len(AFV_Array)), '% (', 'Old:', AFV_Array.iloc[i]['valdouble'], ' new:', Qsuh ,')')

print('\n\nStart calculating aggregate flows')
for item in aggFlows:
    print('====', item['AFV'], '====')

    AFV_mask = signalsData['nodeid'] == namesDict[item['AFV']]
    AF_ptr = min([i for i,x in enumerate(AFV_mask) if x])
    print('AF data pointer:', AF_ptr)

    AFV_Array = signalsData[signalsData['nodeid'] == namesDict[item['AFV']]]
    AF1_Array = signalsData[signalsData['nodeid'] == namesDict[item['AFV_1']]]
    AF2_Array = signalsData[signalsData['nodeid'] == namesDict[item['AFV_2']]]

    AF1_ctr = 0
    AF2_ctr = 0

    for i in range(len(AFV_Array)):
        AF_time = AFV_Array.iloc[i]['actualtime']

        AF1_ctr, dev = findClosestPoint(AF_time, AF1_ctr, AF1_Array)
        if dev >= 1:
            print('Warning: AF1 time deviation =', dev, 'seconds')
        AF2_ctr, dev = findClosestPoint(AF_time, AF2_ctr, AF2_Array)
        if dev >= 1:
            print('Warning: AF2 time deviation =', dev, 'seconds')

        signalsData.at[AF_ptr + i, 'valdouble'] = AF1_Array.iloc[AF1_ctr]['valdouble'] + AF2_Array.iloc[AF2_ctr]['valdouble']

        if i % 10000 == 0:
            print(round((i*100.0)/len(AFV_Array)), '% (', 'Old:', AFV_Array.iloc[i]['valdouble'], ' new:', AF1_Array.iloc[AF1_ctr]['valdouble'] + AF2_Array.iloc[AF2_ctr]['valdouble'] ,')')

print('\n\nWriting ADP file')

h5File = h5py.File(outName, 'w')

h5File.create_dataset('/names.csv', data = inFile.getNamesData())
h5File.create_dataset('/Trends.ini', data = inFile.getIniData())

h5File.attrs.create('minDateTime', inFile.getDateTimeRange()[0])
h5File.attrs.create('maxDateTime', inFile.getDateTimeRange()[1])
h5File.attrs.create('formatVersion', 1)
h5File.attrs.create('formatVersionMinor', 2)

h5File.create_dataset('data/actualtime', data=timeRaw, **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))
h5File.create_dataset('data/nodeid', data=signalsData['nodeid'],  **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))
h5File.create_dataset('data/valdouble', data=signalsData['valdouble'], **hdf5plugin.Blosc(cname='zstd', clevel=9, shuffle=hdf5plugin.Blosc.SHUFFLE))

h5File.close()

print('Done!')