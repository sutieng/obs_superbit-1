import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
import numpy as np

# This is the readout noise and gain of our amps: 
readout = [[12,12,12,12]]
gain_all = [[0.53,0.54,0.54,0.54]]  ##not sure the value

def addAmp(ampCatalog,i,rN,gain_s):

    #Record the new amp:
    record = ampCatalog.addNew()

    #This needs to be the full dimension of what your amp outputs,
    #including overscan, any dummy pixels etc etc.:
    width = 3333
    height = 2227

    os = 20   #pixels of overscan

    #This is the dimensions of the active region of your amp:
    bbox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(3288, 2192))

    #If your CCD consists of more than one amp, you'll need to
    #some of them (i.e., the one on the right is shifted by X pixels)
    bbox.shift(afwGeom.Extent2I(3288 if (i==1 or i==3) else 0, 2192 if (i==2 or i==3) else 0))

    #Define the gain, saturation and readout noise:
    gain = gain_s
    saturation = 65535  ##not sure
    readNoise = rN

    #Which corner is the data read out from?
    readoutCorner = afwTable.LL if i == 0 else afwTable.LR

    #I don't worry about linearity; maybe I should...
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    
    #This defines the full output dimensions of your amp:
    ##for the top amp, there are only y=height-1 pixels, for the right amps, x=width-1 pixels
    rawBBox = afwGeom.Box2I(afwGeom.Point2I(0,0), afwGeom.Extent2I(width if (i==0 or i==2) else width-1,height if (i==0 or i==1) else height-1))
    rawXYOffset = afwGeom.Extent2I(0,0)

    #This defines the data region. Here, there are 45 pixels to the
    #left of the the left amps that don't take data. There are 35 pixels
    #on  bottom of the amps that don't take data.
    
    rawDataBBox = afwGeom.Box2I(afwGeom.Point2I(45 if (i==0 or i ==2) else 0, 35 if (i==0 or i ==1) else 0), afwGeom.Extent2I(3288,2192))
    # These are 20 pixels to the left of the left anmp
    #(12 pixel in) and 20 pixels (11pixels in) to the right of the right amp. The overscan runs the
    #full top to bottom length of the detector.
    #rawHorizontalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(1 if i==0 else width-os-1, 0), afwGeom.Extent2I(os, height))
    rawHorizontalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(12 if (i==0 or i==2) else width-os-12, 0), afwGeom.Extent2I(os, height if (i==0 or i==1) else height-1))
    # These are 20 pixels to the top of the top anmp
    #(1 pixel in) and 20 pixels (2pixels in) to the bottom of the bottom amp. The overscan runs the
    #full left to right length of the detector.
    rawVerticalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(0, 2 if (i==0 or i==1) else height-os-2), afwGeom.Extent2I(width if (i==0 or i==2) else width-1, os))
    ##no prescan
    rawPrescanBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(0, 0))
    emptyBox = afwGeom.BoxI()

    #Shift the right amp to the right by the full width:
    shiftp = afwGeom.Extent2I(width if (i==1 or i==3) else 0, height if (i==2 or i==3) else 0)
    rawBBox.shift(shiftp)
    rawDataBBox.shift(shiftp)
    rawHorizontalOverscanBBox.shift(shiftp)
    rawVerticalOverscanBBox.shift(shiftp)
    
    #Add the defined information to the amp record:
    record.setHasRawInfo(True) #Sets the first Flag=True
    record.setRawFlipX(False)  #Sets the second Flag=False
    record.setRawFlipY(False)  #Sets the third Flag=False
    record.setBBox(bbox)
    record.setName('left' if i == 0 else ("right" if i==1 else ("top left" if i==2 else "top right")))
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
    record.setRawPrescanBBox(emptyBox)

def makeCcd(ccdId):
    '''
    Make a CCD out of a set of amps
    Remove the for loop if you only have one amp
    per CCD.
    '''
    schema = afwTable.AmpInfoTable.makeMinimalSchema()
    ampCatalog = afwTable.AmpInfoCatalog(schema)
    for i in range(4):
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
