import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
import numpy as np

# This is the readout noise and gain of our amps:
readout = [[12]]
gain_all = [[0.31]]

def addAmp(ampCatalog,i,rN,gain_s):
    
    #Record the new amp:
    record = ampCatalog.addNew()
    
    #This needs to be the full dimension of what your amp outputs,
    #including overscan, any dummy pixels etc etc.:
    width = 6665
    height = 4453
    
    os = 20   #pixels of overscan
    
    #This is the dimensions of the active region of your amp:
    bbox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(6576, 4384))
    
    #If your CCD consists of more than one amp, you'll need to
    #some of them (i.e., the one on the right is shifted by X pixels)
    bbox.shift(afwGeom.Extent2I(3288 if (i==1 or i==3) else 0, 2192 if (i==2 or i==3) else 0))
    
    #Define the gain, saturation and readout noise:
    gain = gain_s
    saturation = 20000
    readNoise = rN
    
    #Which corner is the data read out from?
    readoutCorner = afwTable.LL
    
    #I don't worry about linearity; maybe I should...
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    
    rawBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(width,height))
    rawXYOffset = afwGeom.Extent2I(0, 0)
    rawDataBBox = afwGeom.Box2I(afwGeom.Point2I(45  , 35), afwGeom.Extent2I(6576,4384))
    rawHorizontalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(6634 , 0), afwGeom.Extent2I(os, height))
    rawVerticalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(0, 4432), afwGeom.Extent2I(width, os))
    rawPrescanBBox = afwGeom.Box2I(afwGeom.Point2I(12, 0), afwGeom.Extent2I(os, height))
    emptyBox = afwGeom.BoxI()

    
    ##Don't need to shift since we only have one amp
    #shiftp = afwGeom.Extent2I(width if (i==1 or i==3) else 0, height if (i==2 or i==3) else 0)
    #rawBBox.shift(shiftp)
    #rawDataBBox.shift(shiftp)
    #rawHorizontalOverscanBBox.shift(shiftp)
    #rawVerticalOverscanBBox.shift(shiftp)
    
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

        note that the name used to be set to 'ccd0_superbit.fits' in
        ampCatalog.writeFits('ccd%s_superbit.fits' %ccdId) (ccdId=0)
        That causes problems since 'ccd0_superbit' never 
        appears in header of calib/data files, so not useful as identifier 

        Changed writeFits to 'superbitccd', which \does\ appear in header
        '''
    schema = afwTable.AmpInfoTable.makeMinimalSchema()
    ampCatalog = afwTable.AmpInfoCatalog(schema)
    for i in range(1):
        addAmp(ampCatalog,i,readout[ccdId][i],gain_all[ccdId][i])

    return ampCatalog.writeFits('superbitccd.fits')

def main():
    '''
        Make a set of CCDs.
        Remove the for loop if you only have one CCD.
        '''
    for i in range(1):
        camera = makeCcd(i)

if __name__ == "__main__":
    main()
