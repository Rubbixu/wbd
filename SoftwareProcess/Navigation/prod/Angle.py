import math
class Angle():
    def __init__(self):
        self.angle = 0       
        #set to 0 degrees 0 minutes
    
    def setDegrees(self, degrees=None):
        if degrees is None:
            self.angle = 0.0
        else:
            if (not(isinstance(degrees,(int,float)))):
                raise ValueError('Angle.setDegrees:  The input should be a integer or float')
            self.angle = float(degrees)
            while self.angle < 0:
                self.angle = self.angle + 360
            while self.angle >360:
                self.angle = self.angle - 360         
        return self.angle
     
         
    def setDegreesAndMinutes(self, degrees):
        if (not(isinstance(degrees,str))):
            raise ValueError('Angle.setDegreesAndMinutes:  The input should be a string with a format of "xdy.y"')
        parts = degrees.partition ('d')
        if (not(parts[1]=='d')):
            raise ValueError('Angle.setDegreesAndMinutes:  No d in the input')
        try:
            integpart = int(parts[0])
        except ValueError:
            raise ValueError ('Angle.setDegreesAndMinutes:  degrees must be integer')
        try:
            floatpart = float(parts[2])
        except ValueError:
            raise ValueError ('Angle.setDegreesAndMinutes:  minutes must be integer or float')
        if (floatpart < 0):
            raise ValueError('Angle.setDegreesAndMinutes:  minutes must be positive')
        floatpartcheck = round(floatpart,1)
        if (not(floatpart == floatpartcheck)):
            raise ValueError('Angle.setDegreesAndMinutes:  minutes must only have one decimal place')
        if (integpart < 0):
            self.angle = integpart - floatpartcheck/60
        else:
            self.angle = integpart + floatpartcheck/60
        while self.angle < 0:
            self.angle = self.angle + 360
        while self.angle >360:
            self.angle = self.angle - 360         
        return self.angle       
            
        
        
    
        
    def add(self, angle):
        if (not(isinstance(angle,Angle))):
            raise ValueError('Angle.add:  The input should be an angle')
        self.angle = self.angle + angle.angle
        while self.angle > 360:
            self.angle = self.angle - 360
        return self.angle
        
    def subtract(self, angle):
        if (not(isinstance(angle,Angle))):
            raise ValueError('Angle.subtract:  The input should be an angle')
        self.angle = self.angle - angle.angle
        while self.angle < 0:
            self.angle = self.angle + 360
        return self.angle
    
    def compare(self, angle):
        if (not(isinstance(angle,Angle))):
            raise ValueError('Angle.compare:  The input should be an angle')
        if self.angle == angle.angle:
            return 0
        else:
            if self.angle > angle.angle:
                return 1
            else:
                return -1 
        
    
    def getString(self):
        Integpart = int(math.floor(self.angle))
        Floatpart = round((self.angle - Integpart)*60,1)
        self.string = str(Integpart) + 'd' + str(Floatpart) 
        return self.string
    
    
    def getDegrees(self):
        return round(self.angle,1)