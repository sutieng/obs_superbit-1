import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
import numpy as np

# This is copying from afw/tests/testAmpInfoTable.py:
readout = [[12]]
gain_all = [[0.31]]

def addAmp(ampCatalog,i,rN,gain_s):
    #Record the new amp:
    record = ampCatalog.addNew()

    #This needs to be the full dimension of what your amp outputs,
    #including overscan, any dummy pixels etc etc.:
    width = 6665
    height = 4453

    os = 20 #pixels of overscan
    
    #This is the dimensions of the active region of your amp:
    bbox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(6576, 4384))
    
    #we only have one amp, no need to shift
    #bbox.shift(afwGeom.Extent2I(4088*i,0))
    
    gain = gain_s
    saturation = 20000
    readNoise = rN
    
    readoutCorner = afwTable.LL
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    
    #This defines the full output dimensions of your amp:

    rawBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(width,height))
    rawXYOffset = afwGeom.Extent2I(0, 0)
    rawDataBBox = afwGeom.Box2I(afwGeom.Point2I(45  , 35), afwGeom.Extent2I(6576,4384))
    rawHorizontalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(6634 , 0), afwGeom.Extent2I(os, height))
    rawVerticalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(0, 4432), afwGeom.Extent2I(width, os))
    rawPrescanBBox = afwGeom.Box2I(afwGeom.Point2I(12, 0), afwGeom.Extent2I(os, height))
    emptyBox = afwGeom.BoxI()

    ##Don't need to shift since we only have one amp
    #shiftp = afwGeom.Extent2I((width)*i,0)
    #rawBBox.shift(shiftp)
    #rawDataBBox.shift(shiftp)
    #rawHorizontalOverscanBBox.shift(shiftp)
    
    #Add the defined information to the amp record:
    record.setHasRawInfo(True) #Sets the first Flag=True
    record.setRawFlipX(False)  #Sets the second Flag=False
    record.setRawFlipY(False)  #Sets the third Flag=False
    record.setBBox(bbox)
    record.setName('left')
    record.setGain(gain)
    record.setSaturation(saturation)
    record.setReadNoise(readNoise)
    record.setReadoutCorner(readoutCorner)
    record.setLinearityCoeffs(linearityCoeffs)
    record.setLinearityType(linearityType)
    record.setRawBBox(rawBBox)
    record.setRawXYOffset(rawXYOffset)
    record.setRawDataBBox(rawDataBBox)
    record.setRawHorizontalOverscanBBox(rawHorizontalOverscanBBox)
    record.setRawVerticalOverscanBBox(rawVerticalOverscanBBox)
    record.setRawPrescanBBox(rawPrescanBBox)

def makeCcd(ccdId):
    '''
        Make a CCD out of a set of amps
        Remove the for loop if you only have one amp
        per CCD.
    '''
    schema = afwTable.AmpInfoTable.makeMinimalSchema()
    ampCatalog = afwTable.AmpInfoCatalog(schema)
    for i in range(1):
        addAmp(ampCatalog, i,readout[ccdId][i],gain_all[ccdId][i])
    return ampCatalog.writeFits('ccd%s_superbit.fits' %ccdId)

def main():
    '''
        Make a set of CCDs.
        Remove the for loop if you only have one CCD.
    '''
    for i in range(1):
        camera = makeCcd(i)

if __name__ == "__main__":
    main()
