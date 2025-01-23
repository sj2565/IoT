from http.server import HTTPServer
from SensorGateway import SensorGateway
from SensorHttpHandler import SensorHttpHandler

class SensorServer:
    __defHostName = 'localhost'
    __defPortNum = 8080
    def __init__(self, hostName=__defHostName, nPort=__defPortNum):
        self.hostName = hostName
        self.nPort = nPort
    def initGateway(self, sPort):
        self.sensorGateway = SensorGateway(sPort)
    def runServer(self):
        self.webServer = HTTPServer((self.hostName, self.nPort), SensorHttpHandler)
        self.webServer.gateway = self.sensorGateway
        print('Server started at http://%s:%s' % (self.hostName, self.nPort))
        self.webServer.serve_forever()