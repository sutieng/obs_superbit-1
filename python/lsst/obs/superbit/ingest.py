from lsst.pipe.tasks.ingestCalibs import CalibsParseTask
from lsst.pipe.tasks.ingest import ParseTask
from astropy.time import Time
import re

class SuperbitCalibsParseTask(CalibsParseTask):

    def _translateFromCalibId(self, field, md):
        # data = md.get("CALIB_ID") --- this kw doesn't exist (JEM)
        data = md.get("OBS_TYPE")
        match = re.search(".*%s=(\S+)" % field, data)
        return match.groups()[0]
    
    def translate_ccd(self, md):
        return self._translateFromCalibId("ccd", md)

    def translate_filter(self, md):
        return self._translateFromCalibId("filter", md)

    def translate_calibDate(self, md):
        return self._translateFromCalibId("calibDate", md)

class SuperbitParseTask(ParseTask):
    
    def translateDate(self, md):
        '''
        Superbit doesn't really need this - we could have
        just used DATE_OBS - but I wanted to give an example
        of a translation.
        '''
        
        date = md.get("DATE")
        start = date[11:]
        date = date.strip()[:10]

        return date
