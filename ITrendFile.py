
from abc import ABC, abstractmethod

class ITrendFile(ABC):

    @abstractmethod
    def getSupportedVerion(self) -> int:
        pass

    @abstractmethod
    def getSignalsData(self):
        pass

    @abstractmethod
    def getIniData(self):
        pass

    @abstractmethod
    def getNamesData(self):
        pass
        
    @abstractmethod
    def getFileName(self):
        pass

    @abstractmethod
    def hasIniData(self):
        pass

    @abstractmethod
    def getDateTimeRange(self):
        pass

    @abstractmethod
    def getFormatVersion(self):
        pass




