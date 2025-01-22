from serial import Serial
from StringTok import StringTok
import time
import matplotlib.pyplot as plt
import psycopg2

class SensorHub:
    __nPortDefRate = 115200 #private member
    def __init__(self, sPort, nPortRate = __nPortDefRate): #public member
        self.ard = Serial(sPort, nPortRate)
        self.sInput = StringTok()
        self.sOutput = StringTok()
        self.tVolt = ()
        self.tVoltTime = ()
        self.startTime = time.time()
        self.bEpoch = True
    def __del__(self):
        if self.ard.isOpen(): self.ard.close()
    def addVolt(self):
        self.clearOutput()
        self.printSerial('volt get')
        if self.bEpoch: vt = time.time()
        else: vt = time.time() - self.startTime    
        while True:
            if self.isAvailable(): break
        self.appendSerial()
        try:
            v = float(self.sOutput.toString())
            print('V = ' + str(v))
            self.tVolt += (v,)
            self.tVoltTime += (vt, )
            return True 
        except:
            print('Comm error!')
            return False      
    def appendSerial(self):
        self.sOutput.appendSerial(self.ard)
    def clearDb(self):
        self.connectDb()
        self.cur.execute('TRUNCATE myvolt')
        self.conn.commit()
        self.closeDb()          
    def clearOutput(self):
        self.sOutput.empty()
    def clearVolt(self):
        self.tVolt = ()
        self.tVoltTIme = ()
    def connectDb(self):
        self.conn = psycopg2.connect(host='localhost', dbname='mydb', user='postgres', password='2565', port='5432')
        self.cur = self.conn.cursor()
    def closeDb(self):
        self.cur.close()
        self.conn.close()
    def countDbVolt(self):
        self.connectDb()
        self.cur.execute('SELECT COUNT(*) FROM myvolt')
        self.conn.commit()
        nCount =  self.cur.fetchone()[0]
        self.closeDb()
        return nCount
    def insertDbVolt(self):
        if len(self.tVolt) <= 0: return
        dbCount = self.countDbVolt()
        self.connectDb()
        for (v, vt) in zip(self.tVolt, self.tVoltTime):
            dbCount = dbCount + 1
            self.cur.execute('INSERT INTO myvolt (id, time, volt) VALUES (%d, %f, %f)' %(dbCount, vt, v))
        self.conn.commit()    
        self.closeDb()
        self.clearVolt()     
    def isAvailable(self):
        return self.ard.inWaiting() > 0
    def loadDbVolt(self):
        self.connectDb()
        self.cur.execute('SELECT time, volt FROM myvolt')
        self.conn.commit()
        dbInfo = self.cur.fetchall()
        self.closeDb()
        for i in range(len(dbInfo)):
            voltTime = dbInfo[i][0]
            volt = dbInfo[i][1]
            self.tVoltTime += (voltTime,)
            self.tVolt += (volt,)
        # print(self.tVoltTime)
        # print(self.tVolt)
    def plotVolt(self):
        plt.plot(self.tVoltTime, self.tVolt)
        plt.xlabel('Measure Time (sec)')
        plt.ylabel('Volt')
        plt.show()
    def printOutput(self):
        print(self.sOutput.toString())
    def printSerial(self, sCmd):
        self.sInput.setString(sCmd)
        self.sInput.printlnSerial(self.ard)
    def sampleVolt(self, nCount, nDelay):
        i = 0
        while True:
            bResult = self.addVolt()
            if bResult: i = i+1
            if i >= nCount: break
            time.sleep(nDelay/1000.)   