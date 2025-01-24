from http.server import HTTPServer
from ProHub import ProHub
from ProjectHttpHandler import ProjectHttpHandler

class ProjectServer:
    __defHostName = 'localhost'
    __defPortNum = 8080
    def __init__(self, hostName=__defHostName, nPort=__defPortNum):
        self.hostName = hostName
        self.nPort = nPort
    def initGateway(self, sPort):
        self.ProHub = ProHub(sPort)
    def runServer(self):
        self.webServer = HTTPServer((self.hostName, self.nPort), ProjectHttpHandler)
        self.webServer.gateway = self.ProHub
        print('Server started at http://%s:%s' % (self.hostName, self.nPort))
        self.webServer.serve_forever()