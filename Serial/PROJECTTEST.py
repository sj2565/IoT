from serial import Serial
from StringTok import StringTok
import time
import psycopg2
import pandas.io.sql as psql

class PROJECTTEST:
    __nPortDefRate = 115200 
    def __init__(self, sPort, nPortRate = __nPortDefRate): 
        self.ard = Serial(sPort, nPortRate)
        self.sInput = StringTok()
        self.sOutput = StringTok()
        self.tTemp = ()
        self.tEcho = ()
    def __del__(self):
        if self.ard.isOpen(): self.ard.close()       
    def addTemp(self):
        self.clearOutput()
        self.printSerial('temp get')
        while True:
            if self.isAvailable():
                break
        self.appendSerial()
        print(self.sOutput.toString())  # 온도센서 정보 출력        
    def addEcho(self):
        self.clearOutput()
        self.printSerial('echo get')
        while True:
            if self.isAvailable():
                break
        self.appendSerial()
        try:
            d = float(self.sOutput.toString())  # 초음파센서 정보 출력
            print('Distance = ' +str(d))
            self.tEcho += (d,)        
            return True 
        except:
            print('센서값을 가져오지 못했습니다.')
            return False               
    def appendSerial(self):
        self.sOutput.appendSerial(self.ard)    
    def clearOutput(self):
        self.sOutput.empty()
    def isAvailable(self):
        return self.ard.inWaiting() > 0
    def printOutput(self):
        print(self.sOutput.toString())
    def printSerial(self, sCmd):
        self.sInput.setString(sCmd)
        self.sInput.printlnSerial(self.ard)
    def autoData(self, nCount):
        i = 0
        while True:
            bResult = self.addTemp(), self.addEcho()
            if bResult: i = i+1
            if i >= nCount: break
            