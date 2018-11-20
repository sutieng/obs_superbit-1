import os

from lsst.daf.persistence import Policy
from lsst.obs.base import CameraMapper
import lsst.afw.image.utils as afwImageUtils
import lsst.afw.image as afwImage
from .makeSuperbitRawVisitInfo import MakeSuperbitRawVisitInfo

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
                'taiObs':str}
        for name in ("raw",
                     "postISRCCD",
                     "calexp",
                     "src",
                     "icSrc",
                     "srcMatch"):
            self.mappings[name].keyDict.update(keys)
         
        #Define the filters in the filter registry
        #I've just guessed these...
        afwImageUtils.defineFilter(name='R',  lambdaEff=635.9, alias=['R'])
        afwImageUtils.defineFilter(name='G',  lambdaEff=534.9, alias=['G'])
        afwImageUtils.defineFilter(name='B',  lambdaEff=446.6, alias=['B'])
        
        #Allocate the newly-defined filters
        self.filters = {}
        self.filters['R'] = afwImage.Filter('R').getCanonicalName()
        self.filters['G'] = afwImage.Filter('G').getCanonicalName()
        self.filters['B'] = afwImage.Filter('B').getCanonicalName()

        #I'm not sure whether this is necessary, but it seems like a
        #good idea...
        self.defaultFilterName = 'R'
