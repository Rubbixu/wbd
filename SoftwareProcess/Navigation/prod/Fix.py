'''
    CA02 by LZX0014

'''
import time as _time
import Angle as angle
from datetime import tzinfo, timedelta, datetime
from xml.dom.minidom import parse
from math import sqrt, tan,pi


STDOFFSET = timedelta(seconds=-_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds=-_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(tzinfo):

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return 0

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

localtime = LocalTimezone()

def LogTimeStamp():
    return datetime.now(localtime).replace(microsecond=0).isoformat(' ')

class fix():
    def __init__(self, logFile=None):
        functionName = "fix.__init__:  "
        if logFile == None:
            logFile = "log.txt"
        if not(isinstance(logFile,str)):
            raise ValueError(functionName+"Input should be a string")
        if logFile=='':
            raise ValueError(functionName+"Name length should be greater or equal to 1")
        try:
            with open(logFile, "a+") as openlog:
                openlog.write("LOG:\t" + LogTimeStamp() + "\t" + "Start of log\n")
        except IOError:
            raise ValueError (functionName+"This file can not be created or appended")
        self.logFile = logFile            
             
        
    def setSightingFile(self, sightingFile=None):
        functionName = "fix.setSightingFile:  "
        if not(isinstance(sightingFile,str)):
            raise ValueError(functionName+"Input is not a xml file")
        if not(sightingFile[-4:] == ".xml"):
            raise ValueError(functionName+"Input is not a xml file")
        if sightingFile[0:-4] == "":
            raise ValueError(functionName+"Name length should be greater or equal to 1")
        try:
            open(sightingFile,"r")
        except IOError:
            raise ValueError (functionName+"This file can not opened")        
        self.sightingFile = sightingFile
        with open(self.logFile, "a+") as openlog:
            openlog.write("LOG:\t" + LogTimeStamp() + "\t" +\
                "Start of sighting file:\t" + self.sightingFile+"\n")
        return self.sightingFile
    
    
    def _getText(self,sighting,tagName):
        elementNodelist = sighting.getElementsByTagName(tagName)
        textNodelist = elementNodelist[0].childNodes
        data = textNodelist[0].data
        return data
        
    def getBody(self,sighting):
        try:
            bodyText = self._getText(sighting,"body")
        except IndexError:
            raise ValueError('fix.getSightings:  "body" is missing in the sighting')
        bodyString = str(bodyText)
        return bodyString 
    
    def getDate(self,sighting):
        try:
            dateText = self._getText(sighting,"date")
        except IndexError:
            raise ValueError('fix.getSightings:  "date" is missing in the sighting')
        dateString = str(dateText)
        return self.validateDate(dateString) 
    
    def validateDate(self,dateString):
        try:
            date = datetime.strptime(dateString,'%Y-%m-%d').date()
            return date
        except ValueError:
            raise ValueError('fix.getSightings:  Wrong date format')
        
    def getTime(self,sighting):
        try:
            timeText = self._getText(sighting,"time")
        except IndexError:
            raise ValueError('fix.getSightings:  "time" is missing in the sighting')
        timeString = str(timeText)
        return self.validateTime(timeString)
    
    def validateTime(self,timeString):
        try:
            time = datetime.strptime(timeString,'%X').time()
            return time
        except ValueError:
            raise ValueError('fix.getSightings:  Wrong time format') 
    
    def getObservedAltitude(self,sighting):
        try:
            angleText = self._getText(sighting,"observation")
        except IndexError:
            raise ValueError('fix.getSightings:  "observation" is missing in the sighting')
        angleString = str(angleText)
        return self.validateObservation(angleString)
        
    def validateObservation(self,angleString):
        functionName = "fix.getSightings:  "
        parts = angleString.partition ('d')
        if (not(parts[1] == 'd')):
            raise ValueError(functionName+'wrong observation format, d is missing')
        try:
            integpart = int(parts[0])
        except ValueError:
            raise ValueError(functionName+'wrong observation format, X should be a integer')
        if not(0<=integpart<90):
            raise ValueError(functionName+'wrong observation format, X should be in [0,90)')
        try:
            floatpart = float(parts[2])
        except ValueError:
            raise ValueError(functionName+'wrong observation format, y should be float or integer')
        if not(0.0<=floatpart<60.0):
            raise ValueError(functionName+'wrong observation format, y should be in [0.0,60.0)')
        if (not(floatpart == round(floatpart, 1))):
            raise ValueError(functionName+'wrong observation format, y should only have one digit')
        observedAltitude = angle.Angle()
        observedAltitude.setDegreesAndMinutes(angleString)
        return observedAltitude

    def getHeight(self,sighting):
        functionName = "fix.getSightings:  "
        try:
            heightText = self._getText(sighting,"height")
        except Exception:
            return 0.0
        try:
            height = float(heightText)
        except ValueError:
            raise ValueError(functionName+"Height should be numeric")
        if height>= 0:
            return height
        else:
            raise ValueError(functionName+"Height should be greater than 0")
    
    def getTemperature(self,sighting):
        functionName = "fix.getSightings:  "
        try:
            temperatureText = self._getText(sighting,"temperature")
        except IndexError:
            return 72
        try:
            temperature = int(temperatureText)
        except ValueError:
            raise ValueError(functionName+"Height should be integer")
        if -20<=temperature<=120:
            return temperature
        else:
            raise ValueError(functionName+"Temperature should be in [-20,120]")
            
    def getPressure(self,sighting):
        functionName = "fix.getSightings:  "
        try:
            pressureText = self._getText(sighting,"pressure")
        except IndexError:
            return 1010
        try:
            pressure = int(pressureText)
        except ValueError:
            raise ValueError(functionName+"Pressure should be integer")
        if 100<=pressure<=1100:
            return pressure
        else:
            raise ValueError(functionName+"Pressure should be in [100,1100]")        
    
    def isHorizonNatural(self,sighting):
        functionName = "fix.getSightings:  "
        try:
            horizonText = self._getText(sighting,"horizon")
        except IndexError:
            return True
        horizonString = str(horizonText)
        if horizonString.lower() == "natural":
            return True
        elif horizonString.lower() == "artificial":
            return False
        else:
            raise ValueError(functionName+"Horizon category can not be identified")   
    
    def calculateDip(self,isHorizonNatural,height):
        if isHorizonNatural:
            dip = (-0.97*sqrt(height))/60
        else:
            dip = 0
        return dip
    
    def calculateRefraction(self,observedAltitude,pressure,temperature):        
        functionName = "fix.getSightings:  "
        minimumAngle = angle.Angle()
        minimumAngle.setDegreesAndMinutes("0d0.1")
        if observedAltitude.compare(minimumAngle) == -1:
            raise ValueError(functionName+"Observation should be greater or equal to 0d0.1")
        else:           
            temperatureInC = (temperature - 32)*5/9
            observedAltitudeInRadian = observedAltitude.getDegrees()/180*pi           
            refraction = (-0.00452*pressure)/(273+temperatureInC)/tan(observedAltitudeInRadian)
        return refraction
    
    def getAdjustedAltitude(self,sighting):
        observedAltitude = self.getObservedAltitude(sighting)
        height = self.getHeight(sighting)
        temperature = self.getTemperature(sighting)
        pressure = self.getPressure(sighting)
        isHorizonNatural = self.isHorizonNatural(sighting) 
        dip = self.calculateDip(isHorizonNatural, height)
        refraction = self.calculateRefraction(observedAltitude, pressure, temperature)
        adjustedAltitudeDegree = observedAltitude.getDegrees() + dip + refraction
        adjustedAltitude = angle.Angle()
        adjustedAltitude.setDegrees(adjustedAltitudeDegree)
        return adjustedAltitude.getString()        
    
    def writeEndOfSightingFile(self,logFile,sightingFile):
        with open(logFile,"a+") as openlog:
            openlog.write("LOG:\t" + LogTimeStamp() + "\t" +\
            "End of sighting file:\t" + sightingFile+"\n") 
    
    def getSightings(self):
        functionName = "fix.getSightings:  "
        try:
            domtree = parse(self.sightingFile)
        except Exception:
            self.writeEndOfSightingFile(self.logFile, self.sightingFile)
            raise ValueError(functionName+"No sighting files has bee set")
        sightings = domtree.getElementsByTagName("sighting")
        sightingList =[]
        for sighting in sightings:
            try:
                body = self.getBody(sighting)
                date = self.getDate(sighting)
                time = self.getTime(sighting)
                adjustedaltitude = self.getAdjustedAltitude(sighting)
                combinedDatetime = datetime.combine(date,time)
                sightingList.append((body,date,time,adjustedaltitude,combinedDatetime))
            except ValueError:
                self.writeEndOfSightingFile(self.logFile, self.sightingFile)
                raise
        sightingList.sort(key=lambda s:(s[4],s[0]))
        for sighting in sightingList:
            with open(self.logFile,"a+") as openlog:
                    openlog.write("LOG:\t" + LogTimeStamp() + "\t" + sighting[0] +\
            "\t" + sighting[1].isoformat() + "\t" + sighting[2].isoformat() + "t" + sighting[3] + "\n") 
        self.writeEndOfSightingFile(self.logFile, self.sightingFile)
        approximateLatitude = "0d0.0"
        approximateLongtitude = "0d0.0"
        return (approximateLatitude, approximateLongtitude)