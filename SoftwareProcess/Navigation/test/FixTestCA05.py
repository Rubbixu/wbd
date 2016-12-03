import unittest
import uuid
import os
import Navigation.prod.Fix as F

class TestFix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.className = "Fix."
        cls.logStartString = "Log file:"
        cls.starSightingString = "Sighting file:"
        cls.starSightingErrorString = "Sighting errors:"
        cls.ariesFileString = "Aries file:"
        cls.starFileString = "Star file:"
        cls.DEFAULT_LOG_FILE = "log.txt"
        cls.ariesFileName = "CA03_Valid_Aries.txt"
        cls.starFileName = "CA03_Valid_Stars.txt"
        cls.testToFileMap = [
            ["validStarSightingFile", "CA02_200_ValidStarSightingFile.xml"],
            ["validAriesFile", "CA03_Valid_Aries.txt"],           
            ["validStarFile", "CA03_Valid_Stars.txt"], 
            ["genericValidStarSightingFile", "CA02_300_GenericValidStarSightingFile.xml"], 
            ["genericValidSightingFileWithMixedIndentation", "CA02_300_ValidWithMixedIndentation.xml"],
            ["validOneStarSighting", "CA02_300_ValidOneStarSighting.xml"],
            ["validMultipleStarSighting", "CA02_300_ValidMultipleStarSighting.xml"],
            ["validMultipleStarSightingSameDateTime", "CA02_300_ValidMultipleStarSightingSameDateTime.xml"],
            ["validWithNoSightings", "CA02_300_ValidWithNoSightings.xml"],
            ["validWithExtraneousTags", "CA02_300_ValidWithExtraneousTags.xml"],
            ["validOneStarNaturalHorizon","CA02_300_ValidOneStarNaturalHorizon.xml"],
            ["validOneStarArtificialHorizon", "CA02_300_ValidOneStarArtificialHorizon.xml"],
            ["validOneStarWithDefaultValues", "CA02_300_ValidOneStarWithDefaultValues.xml"],
            ["invalidWithMissingMandatoryTags","CA02_300_InvalidWithMissingMandatoryTags.xml"],
            ["invalidBodyTag","CA02_300_InvalidBody.xml"],
            ["invalidDateTag","CA02_300_InvalidDate.xml"],
            ["invalidTimeTag","CA02_300_InvalidTime.xml"],
            ["invalidObservationTag","CA02_300_InvalidObservation.xml"],
            ["invalidHeightTag","CA02_300_InvalidHeight.xml"],
            ["invalidTemperatureTag", "CA02_300_InvalidTemperature.xml"],
            ["invalidPressureTag","CA02_300_InvalidPressure.xml"],
            ["invalidHorizonTag","CA02_300_InvalidHorizon.xml"],
            ["validLatLon", "CA03_300_ValidStarLatLon.xml"],
            ["validLatLonInterpolated", "CA03_300_ValidStarLatLonInterpolationRequired.xml"]
            ]      
    def setUp(self):
        if(os.path.isfile(self.DEFAULT_LOG_FILE)):
            os.remove(self.DEFAULT_LOG_FILE) 
        # generate random log file name
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
        self.deleteNamedLogFlag = False
    
    def tearDown(self):
        if(self.deleteNamedLogFlag):
            try:
                if(os.path.isfile(self.RANDOM_LOG_FILE)):
                    os.remove(self.RANDOM_LOG_FILE)  
            except:
                pass
    
#     def test200_100ShouldReturn0ForDefault(self):
#         theFix = F.Fix()
#         lagitude = theFix.validatelagitude()
#         self.assertEqual(lagitude, 0, "not work on default")
        
#     def test200_100ShouldForValid(self):
#         theFix = F.Fix()
#         lagitude = theFix.validatelagitude("S19d0.0")
#         self.assertEqual(lagitude, "S19d0.0", "not work on default")
# 
#     def test200_910ShouldNotForInvalid(self):
#         theFix = F.Fix()
#         expectedDiag = self.className + "getSightings:"
#         with self.assertRaises(ValueError) as context:
#             theFix.validatelagitude("G1d0.0") 
#         self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)], 
#                           "fail to detect wrong altitude input")  
#     
#     def test300_110ShouldCalculateCorrectedAltitude(self):
#         theFix = F.Fix()
#         x = theFix.adjustPosition("318d9.9","74d35.3" ,"-60d53.8" , "S53d38.4","35d8.1")
#         self.assertEquals(x,2159)
        
#     def test400_110ShouldReturnCorrectArcMinute(self):
#         theFix = F.Fix()
#         x = theFix.calculateArcMinute("35d58.5")
#         self.assertEquals(x,2159)
    def test100_110ShouldCalculateCorrectPosition(self):
        theFix = F.Fix(self.RANDOM_LOG_FILE)    
        theFix.setSightingFile("CA05_100_ValidStarSightingFile.xml")
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        x = theFix.getSightings()
        self.assertEquals(x,("S13d28.0","101d42.2"))
        