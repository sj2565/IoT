from SensorHub import SensorHub
import pandas.io.sql as psql

class SensorGateway(SensorHub):
    def loadDfVolt(self):      # pandas 사용
        self.connectDb()
        self.dfVolt = psql.read_sql('SELECT time, volt FROM myvolt', self.conn) 
        self.closeDb()
        print('# of volt = ', len(self.dfVolt));
    def makeHtmlTableVolt(self):
        self.loadDfVolt()
        html = '<table style="width:50%; border: 1px solid black; text-align: center;"><tr><th>Time</th><th>Volt</th></tr>'
        for (t, v) in zip(self.dfVolt.time, self.dfVolt.volt):
            html += '<tr><td>%f</td><td>%f</td></tr>' % (t, v)       
        html += '</table>'
        return html
    def measureVolt(self, nCount, nDelay):
        self.clearVolt()
        self.sampleVolt(nCount, nDelay) 
        self.insertDbVolt()     
        self.clearVolt()
    def plotVolt(self):
        self.clearVolt()
        self.loadDbVolt()
        SensorHub.plotVolt(self)
        self.clearVolt()
    def statVolt(self):
        self.minVolt = self.dfVolt.min()[1]
        self.maxVolt = self.dfVolt.max()[1]
        self.meanVolt = self.dfVolt.mean()[1]
        self.stdVolt = self.dfVolt.std()[1]
        print('min of V = ', self.minVolt)
        print('max of V = ', self.maxVolt)
        print('mean of V = ', self.meanVolt)
        print('standard of V = ', self.stdVolt)