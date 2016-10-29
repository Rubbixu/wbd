import unittest
import Navigation.prod.Fix as Fix
import Navigation.prod.Angle as Angle
from xml.dom.minidom import parse

class FixTest(unittest.TestCase):
    

    def tearDown(self):
        pass

# --------------------------------------------------
# ---Acceptance Test
# 100 constructor
# Happy path
    def test100_010_ShouldCreateInstanceOfFix(self):
        self.assertIsInstance(Fix.fix(), Fix.fix)

# Sad path     
    def test100_910_ShouldRaiseExceptionForIntegerInput(self):
        expectedString = "fix.__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.fix(20)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
         
    def test100_920_ShouldRaiseExceptionForReadOnlyFile(self):
        expectedString = "fix.__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.fix("ValidFile.txt")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test100_930_ShouldRaiseExceptionForZeroLengthString(self):
        expectedString = "fix.__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.fix("")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

# 200 setSightingFile
# Happy path
    def test200_010_ShouldReturnSightingFile(self):
        myFix = Fix.fix()
        self.assertEquals(myFix.setSightingFile("test200.xml"), "test200.xml")

# Sad path
    def test200_910_ShouldRaiseExceptionForInputIsNone(self):
        expectedString = "fix.setSightingFile:"
        myFix = Fix.fix()
        with self.assertRaises(ValueError) as context:
            myFix.setSightingFile()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
     
    def test200_920_ShouldRaiseExceptionForWrongFileExtention(self):
        expectedString = "fix.setSightingFile:"
        myFix = Fix.fix()
        with self.assertRaises(ValueError) as context:
            myFix.setSightingFile("abc")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
         
    def test200_930_ShouldRaiseExceptionForWrongFileExtention(self):
        expectedString = "fix.setSightingFile:"
        myFix = Fix.fix()
        with self.assertRaises(ValueError) as context:
            myFix.setSightingFile(".xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

    def test200_940_ShouldRaiseExceptionForCantOpenTheFile(self):
        expectedString = "fix.setSightingFile:"
        myFix = Fix.fix()
        with self.assertRaises(ValueError) as context:
            myFix.setSightingFile("test200_940.xml")
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

# 500 getSighting
# Happy path    
    def test500_010ShouldGetSightings(self):
        myFix = Fix.fix()
        myFix.setSightingFile("test500_010.xml")
        self.assertEquals(myFix.getSightings(), ("0d0.0", "0d0.0"))
    
    def test500_020ShouldGetSightingsByChoronicalOrder(self):
        myFix = Fix.fix()
        myFix.setSightingFile("test500_020.xml")
        self.assertEquals(myFix.getSightings(), ("0d0.0", "0d0.0"))   
         
# Sad path    
    def test500_910ShouldRaiseExceptionWhenBodyIsMissing(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        myFix.setSightingFile("test500_910.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getSightings()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test500_920ShouldRaiseExceptionWhenFixTagIsNotOne(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        myFix.setSightingFile("test500_920.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getSightings()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test500_930ShouldRaiseExceptionWhenPressureIsOutOfBoundry(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        myFix.setSightingFile("test500_930.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getSightings()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test500_940ShouldRaiseExceptionWhenObservationIsBelow0d01(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        myFix.setSightingFile("test500_940.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getSightings()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])        
# --------------------------------------------------
# ---Unit Tests
# 300 GetValueSeries
# Happy path        
    def test300_010ShouldGetText(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix._getText(sighting, "body"), unicode('Aldebaran'))    
        
    def test300_020ShouldGetBody(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix.getBody(sighting), 'Aldebaran')
    
    def test300_030ShouldGetDate(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix.getDate(sighting).isoformat(), '2016-03-01')
    
    def test300_040ShouldGetTime(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix.getTime(sighting).isoformat(), '23:40:01')
    
    def test300_050ShouldGetObservation(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix.getObservedAltitude(sighting).getString(), '15d4.9')
    
    def test300_060ShouldGetHeightWhenItExist(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix.getHeight(sighting), 6.0)
        
    def test300_070ShouldGetTemperatureWhenDataIsMissing(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix.getTemperature(sighting), 72)
    
    def test300_080ShouldGetPressureWhenTagIsMissing(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix.getPressure(sighting), 1010)
    
    def test300_090ShouldGetHorizonCaseInsensitive(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix.isHorizonNatural(sighting), False)

# Sad path    
    def test300_910ShouldRaiseExceptionForNoBodyInFile(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        sighting = parse("test300sadPath.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getBody(sighting)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_920ShouldRaiseExceptionForWrongDateFormat(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        sighting = parse("test300sadPath.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getDate(sighting)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_930ShouldRaiseExceptionForWrongTimeFormat(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        sighting = parse("test300sadPath.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getTime(sighting)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_940ShouldRaiseExceptionForWrongObservationFormat(self):    
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        sighting = parse("test300sadPath.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getObservedAltitude(sighting)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_950ShouldRaiseExceptionForNoneNumericHeight(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        sighting = parse("test300sadPath.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getHeight(sighting)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_960ShouldRaiseExceptionForNoneIntegerTemperature(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        sighting = parse("test300sadPath.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getTemperature(sighting)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    def test300_970ShouldRaiseExceptionForPressureOutOfBoundry(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        sighting = parse("test300sadPath.xml")
        with self.assertRaises(ValueError) as context:
            myFix.getPressure(sighting)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test300_980ShouldRaiseExceptionWhenHorizonCanNotBeIdentified(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        sighting = parse("test300sadPath.xml")
        with self.assertRaises(ValueError) as context:
            myFix.isHorizonNatural(sighting)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

# 400 CalculateValueSeries
# Happy path    
    def test400_010ShouldCalculateDip(self):
        myFix = Fix.fix()
        self.assertAlmostEquals(myFix.calculateDip(True, 6.0), -0.0396, 6)
    
    def test400_020ShouldCalculateRefraction(self):
        myFix = Fix.fix()
        testAngle = Angle.Angle()
        testAngle.setDegreesAndMinutes("45d0.0")
        self.assertAlmostEquals(myFix.calculateRefraction(testAngle, 1010, 50), -0.0161314, 6)
    
    def test400_030ShouldGetAdujustedAltitude(self):
        myFix = Fix.fix()
        sighting = parse("test300happyPath.xml")
        self.assertEquals(myFix.getAdjustedAltitude(sighting), "15d1.5")

# Sad path    
    def test400_910ShouldRaiseExceptionWhenObservedAltitudeIsOutOfBoundry(self):
        expectedString = "fix.getSightings:"
        myFix = Fix.fix()
        testAngle = Angle.Angle()
        testAngle.setDegreesAndMinutes("0d0.0")
        with self.assertRaises(ValueError) as context:
            myFix.calculateRefraction(testAngle, 1010, 50)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
    
    
