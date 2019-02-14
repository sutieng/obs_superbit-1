from lsst.afw.geom import degrees, SpherePoint
from lsst.afw.coord import Observatory
from lsst.obs.base import MakeRawVisitInfo
import pdb

__all__ = ["MakeSuperbitRawVisitInfo"]

class MakeSuperbitRawVisitInfo(MakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of a SuperBIT image
    """
    #Hmm - bit tricky for a floaty observatory; let's hope it's not important
    #Having said that, if you have a record of the telescopes position
    #at the time of observation, you may be able to use that.
    #
    # Put in coordinates of CSBF as a placeholder, with an elevation of 30,000 m
    # hopefully that doesn't make limit of elev fail? --JEM
    observatory = Observatory(31.779524*degrees, 95.712369*degrees, 30000)  # long, lat, elev


    def setArgDict(self, md, argDict):
        """Set an argument dict for makeVisitInfo and pop associated metadata
        @param[in,out] md  metadata, as an lsst.daf.base.PropertyList or PropertySet
        @param[in,out] argdict  a dict of arguments
        """
        #I believe the names in capitals come from the header. You'll need
        #to change these to reflect your header keywords.
        startDate = self.popIsoDate(md, "DATE_OBS")
        argDict["exposureTime"] = self.popFloat(md, 'EXPTIME')
        argDict['darkTime'] = argDict['exposureTime']

        argDict["date"] = self.offsetDate(startDate, 0.5*argDict["exposureTime"])
        argDict["boresightAzAlt"] = SpherePoint(
            self.popAngle(md, "AZ"),
            self.popAngle(md, "EL"),
        )
        #argDict["boresightAirmass"] = self.popFloat(md, "AIRMASS")
        argDict["observatory"] = self.observatory
        
