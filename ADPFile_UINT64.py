
import h5py
import hdf5plugin
import pandas as pd

from ITrendFile import ITrendFile

class ADPFile_UINT64(ITrendFile):
    def __init__(self, h5FileName: str):
        self.fileName = h5FileName
        try:
            self.h5File = h5py.File(h5FileName, 'r+')

            if 'formatVersion' in self.h5File.attrs.keys():
                self.version = self.h5File.attrs['formatVersion']
            else:
                self.version = 0;

            self.iniIncluded = 'Trends.ini' in self.h5File.keys()
            self.iniData = ''
            if self.iniIncluded:
                self.iniData = self.readStringDataSet('Trends.ini')
            self.namesData = self.readStringDataSet("names.csv")
            self.dict_ = {'actualtime': self.h5File['data_uint64/actualtime'], 'valdouble': self.h5File['data_uint64/valuint'], 'nodeid': self.h5File['data_uint64/nodeid']}
            self.data = pd.DataFrame(self.dict_)
            #self.data['actualtime'] = pd.to_datetime(self.data['actualtime'], unit='ns')

            if self.version == 1:
                self.minDateTime = self.h5File.attrs['minDateTime']
                self.maxDateTime = self.h5File.attrs['maxDateTime']
            elif self.version == 2:
                self.minDateTime = self.h5File.attrs['minDateTime'][0]
                self.maxDateTime = self.h5File.attrs['maxDateTime'][0]
            else:
                self.minDateTime = 'N/A'
                self.maxDateTime = 'N/A'

            self.bad = False
        except:
            raise
            self.bad = True
        finally:
            pass
            #self.h5File.close()

        del self.h5File

    def getSupportedVerion(self):
        return 2

    def readStringDataSet(self, dsName:str) -> str:
        try:
            return self.h5File[dsName][()].decode('utf-8')
        except:
            return self.h5File[dsName][0].decode('utf-8')

    def getSignalsData(self):
        return self.data

    def getIniData(self):
        return self.iniData

    def getNamesData(self):
        return self.namesData
        
    def getFileName(self):
        return self.fileName

    def hasIniData(self):
        return self.iniIncluded

    def getDateTimeRange(self):
        return self.minDateTime, self.maxDateTime

    def getFormatVersion(self):
        return self.version




