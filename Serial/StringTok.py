#/*-------------------------------------------------------------------
#StringTok.py: String with Token Operation for Serial
#Copyright (c) 2016-Forever ACE Lab, Korea.
#All Rights Reserved.  Personal and non-commercial purpose only.
#-------------------------------------------------------------------*/
class StringTok:
    # Static Variables
    __sDelimit = ' +-*/<>=()&|!,;:@#$%^\t\r\n[]{}'
    __sWhite = ' \t\r\n'
    __eol = '\n' # End of line
    # Contructor & Destructor
    def __init__(self, s=''):
        self.setString(s)
    def __del__(self):
        pass
    # String
    def getAt(self, nPos):
        return self.__str[nPos]
    def getAtPosTok(self):
        return self.getAt(self.getPosTok())
    def getLine(self):
        nPos = self.find(StringTok.__eol)
        if nPos < 0: return ''
        else: return self.substring(0, nPos)
    def getPosTok(self):
        return self.__nPosTok
    def getToken(self):
        nInput = self.length()
        s = ''
        while StringTok.isWhite(self.getAtPosTok()):
            self.incPosTok()
            if self.getPosTok() >= nInput: return StringTok(s)
        s = self.getAtPosTok()
        self.incPosTok()
        if StringTok.isDelimit(s[0]): return StringTok(s)
        while self.getPosTok() < nInput:
            if StringTok.isDelimit(self.getAtPosTok()): return StringTok(s)
            s += self.getAtPosTok()
            self.incPosTok()
        return StringTok(s)
    def setPosTok(self, nPos):
        self.__nPosTok = int(nPos)
    def setString(self, s):
        self.__str = str(s)
        self.initPosTok()
    def appendString(self, s):
        self.__str += str(s)
    def cutLine(self):
        nPos = self.find(StringTok.__eol)
        if nPos < 0: return ''
        sLine = self.substring(0, nPos)
        if nPos + 1 < self.length(): self.setString(self.substringToEnd(nPos + 1))
        else: empty()
        return sLine
    def cutToken(self):
        sToken = self.getToken();
        if self.getPosTok() < self.length(): self.setString(self.substringToEnd(self.getPosTok()))
        else: self.empty();
        return sToken;
    def empty(self):
        self.setString('')
    def find(self, s):
        return self.__str.find(s)
    def hasLine(self):
        return self.find(StringTok.__eol) >= 0
    def incPosTok(self):
        self.__nPosTok += 1
    def initPosTok(self):
        self.setPosTok(0)
    def isEmpty(self):
        return self.length() == 0
    def length(self):
        return len(self.__str)
    def substring(self, nFrom, nTo):
        return self.__str[nFrom:nTo]
    def substringToEnd(self, nFrom):
        return self.__str[nFrom:]
    def toFloat(self):
        return float(self.__str)
    def toInt(self):
        return int(self.__str)
    def toString(self):
        return self.__str
    def isDelimit(ch):
        return ch in StringTok.__sDelimit
    def isWhite(ch):
        return ch in StringTok.__sWhite
    # Serial
    def inputSerial(self, serial):
        self.setString(StringTok.getSerialInput(serial))
    def appendSerial(self, serial):
        self.appendString(StringTok.getSerialInput(serial))
    def printSerial(self, serial):
        serial.write(self.toString().encode())
    def printlnSerial(self, serial):
        serial.write((self.toString() + StringTok.__eol).encode())
    def getSerialInput(serial):
        nByte = serial.inWaiting()
        if nByte > 0: return serial.read(nByte).decode()
        else: return ''
#/*-------------------------------------------------------------------
#Revision Records
#---------------------------------------------------------------------
#C(2020-05-25)
#R():
#-------------------------------------------------------------------*/