import os

from lsst.daf.persistence import Policy
from lsst.obs.base import CameraMapper
import lsst.afw.image.utils as afwImageUtils
import lsst.afw.image as afwImage
from .makeSuperbitRawVisitInfo import MakeSuperbitRawVisitInfo
import pdb

class SuperbitMapper(CameraMapper):
    """
    The mapper class (which inherits CameraMapper) does a number
    of things. It tells the stack which policy file to use, provides
    a list of filters, tells the stack how to generate ID numbers
    for sources and allows certain default functions to be overridden
    by your own functions.
    """
    
    #packageName is used a few times throughout within the class
    packageName = 'obs_superbit'

    #MakeSuperBitRawVisitInfo grabs information from the header.
    #Take a look at makeSuperbitRawVisitInfo in this same directory.
    MakeRawVisitInfoClass = MakeSuperbitRawVisitInfo

    def __init__(self, inputPolicy=None, **kwargs):

        #Tell the mapper the location of the policy file, which
        #informs the stack where to read/write and the format of
        #files.
        policyFile = Policy.defaultPolicyFile(self.packageName, "SuperbitMapper.yaml", "policy")
        policy = Policy(policyFile)

        #Instantiate the parent class (CameraMapper) with the policy file:
        super(SuperbitMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)

        #Ensure each dataset type of interest knows about the full range
        #of keys available from the registry. This means a minimal set of
        #--id's need to be specified, and the stack will find the rest.
        keys = {'visit':int,
                'filter':str,
                'dataType':str,
                'expTime':float,
                'dateObs':str,
                'taiObs':str
                    }
        for name in ("raw",
                     "postISRCCD",
                     "calexp",
                     "src",
                     "icSrc",
                     "srcMatch"):
            self.mappings[name].keyDict.update(keys)
         
        #Define the filters in the filter registry
        #obtained from https://sites.physics.utoronto.ca/bit/documentation/camera_lenses/palestine-filter-list
        afwImageUtils.defineFilter(name='Open', lambdaEff=500, alias=['O'])
        afwImageUtils.defineFilter(name='Luminance', lambdaEff=500, alias=['L'])
        afwImageUtils.defineFilter(name='IR', lambdaEff=800, alias=['IR'])
        afwImageUtils.defineFilter(name='Red', lambdaEff=650, alias=['R'])
        afwImageUtils.defineFilter(name='Green',lambdaEff=550, alias=['G'])
        afwImageUtils.defineFilter(name='Blue', lambdaEff=450, alias=['B'])
        afwImageUtils.defineFilter(name='UV', lambdaEff=375, alias=['UV'])
        
        #Allocate the newly-defined filters
        #Is this ok?
        self.filters = {}
        
        self.filters['O'] = afwImage.Filter('O').getCanonicalName()
        self.filters['L'] = afwImage.Filter('L').getCanonicalName()
        self.filters['IR'] = afwImage.Filter('IR').getCanonicalName()
        self.filters['R'] = afwImage.Filter('R').getCanonicalName()
        self.filters['G'] = afwImage.Filter('G').getCanonicalName()
        self.filters['B'] = afwImage.Filter('B').getCanonicalName()
        self.filters['UV'] = afwImage.Filter('UV').getCanonicalName()

        #I'm not sure whether this is necessary, but it seems like a
        #good idea...
        self.defaultFilterName = 'O'
        
    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit identifier for a CCD exposure.
        @param dataId (dict) Data identifier with visit and CCD
        
        We uniquely identify an exposure via its visit ID (i.e., r******) and its ccd (UT number).
        We allow for up to 2**24 = 16,777,216 visits, and up to 2**6 = 64 UTs
        The first 34 (right to left) bits give the object ID (overkill).
        The next 6 give the UT.
        The next 24 give the visit number.
        If you want to add a filter code (up to 2**3 = 8 filters, say):
        return visit*64*8 + filt*64 + ccd
        Then add 3 to the 30 in bypass_ccdExposureId_bits
        """
        
        pathId = self._transformId(dataId)
        visit = pathId['visit']
        ccd = pathId['ccd']
        visit = int(visit)
        if ccd in 'superbitccd': 
            ccd = int(1)

        return visit*64 + ccd

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        return 24+6
    
    def _extractDetectorName(self, dataId):
        """ orginally was %(ccd)d but failed"""
        #ccdInstance="%(ccd)s" % dataId
        #if ccdInstance in 'superbitccd': 
        #    ccdInstance = int(1)

        return ("%(ccd)s" % dataId)

