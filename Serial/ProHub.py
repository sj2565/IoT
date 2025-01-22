from serial import Serial
from StringTok import StringTok
import time
import psycopg2
import pandas.io.sql as psql

class ProHub:
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
        try:
            t = float(self.sOutput.toString())  # 온도센서 정보 출력
            print('Temperature = ' +str(t))
            self.tTemp += (t,)        
            return True 
        except:
            print('센서값을 가져오지 못했습니다.')
            return False         
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
    def autoData(self, nCount, nDelay):
        i = 0
        while True:
            bResult = self.addTemp(), self.addEcho()
            if bResult: i = i+1
            if i >= nCount: break
            time.sleep(nDelay/1000.)
    def getData(self, nCount, nDelay):
        self.clearData()
        self.autoData(nCount, nDelay) 
        self.insertDb()     
        self.clearData()        
    # db 부분
    def clearDb(self):
        self.connectDb()
        self.cur.execute('TRUNCATE mysensor')
        self.conn.commit()
        self.closeDb()
    def clearData(self):
        self.tTemp = ()
        self.tEcho = ()
    def connectDb(self):
        self.conn = psycopg2.connect(host='localhost', dbname='prosensor', user='postgres', password='2565', port='5432')
        self.cur = self.conn.cursor()    
    def closeDb(self):
        self.cur.close()
        self.conn.close()
    def countDb(self):
        self.connectDb()
        self.cur.execute('SELECT COUNT(*) FROM mysensor')
        self.conn.commit()
        nCount =  self.cur.fetchone()[0]
        self.closeDb()
        return nCount
    def insertDb(self):
        if len(self.tTemp and self.tEcho) <= 0: return
        self.connectDb()
        dbCount = self.countDb()
        for (t, d) in zip(self.tTemp, self.tEcho):
            self.connectDb()
            dbCount = dbCount + 1
            self.cur.execute('INSERT INTO mysensor (id, temperature, distance) VALUES (%d, %f, %f)' %(dbCount, t, d))
        self.conn.commit()
        self.closeDb()
        self.clearData()                
    def loadDb(self):      
        self.connectDb()
        self.db = psql.read_sql('SELECT temperature, distance FROM mysensor', self.conn) 
        self.closeDb()
        print('저장된 데이터 개수 : ', len(self.db));
    # 서버 부분    
    def makeHtmlTableDb(self):
        self.loadDb()
        html = '<table style="width:50%; border: 1px solid black; text-align: center;"><tr><th>Temp</th><th>Echo</th></tr>'
        for (t, d) in zip(self.db.temperature, self.db.distance):
            html += '<tr><td>%f</td><td>%f</td></tr>' % (t, d)       
        html += '</table>'
        return html        