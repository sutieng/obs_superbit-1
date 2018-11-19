import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
import numpy as np

# This is the readout noise and gain of our amps: 
readout = [[22.3,23.1],[23.0,22.1],[23.0,24.4]]
gain_all = [[0.53,0.54],[0.52,0.52],[0.59,0.59]]

def addAmp(ampCatalog,i,rN,gain_s):

    #Record the new amp:
    record = ampCatalog.addNew()

    #This needs to be the full dimension of what your amp outputs,
    #including overscan, any dummy pixels etc etc.:
    width = 4152
    height = 6220

    os = 10 #pixels of overscan

    #This is the dimensions of the active region of your amp:
    bbox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(4088, 6132))

    #If your CCD consists of more than one amp, you'll need to
    #some of them (i.e., the one on the right is shifted by X pixels)
    bbox.shift(afwGeom.Extent2I(4088*i,0))

    #Define the gain, saturation and readout noise:
    gain = gain_s
    saturation = 65535
    readNoise = rN

    #Which corner is the data read out from?
    readoutCorner = afwTable.LL if i == 0 else afwTable.LR

    #I don't worry about linearity; maybe I should...
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    
    #This defines the full output dimensions of your amp:
    rawBBox = afwGeom.Box2I(afwGeom.Point2I(0,0), afwGeom.Extent2I(width,height))
    rawXYOffset = afwGeom.Extent2I(0,0)

    #This defines the data region. Here, there are 64 pixels to the
    #left of the the left amp that don't take data. There are 44 pixels
    #on the top and bottom of the amps that don't take data.
    rawDataBBox = afwGeom.Box2I(afwGeom.Point2I(64 if i==0 else 0, 44), afwGeom.Extent2I(4088,6132))

    #Here, I define the overscan boxes. These are 10 pixels to the left of the left anmp
    #(1 pixel in) and 10 pixels to the right of the right amp. The overscan runs the
    #full top to bottom length of the detector.
    rawHorizontalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(1 if i==0 else width-os-1, 0), afwGeom.Extent2I(os, 6220))
    #rawVerticalOverscanBBox = afwGeom.Box2I(afwGeom.Point2I(50, 6132), afwGeom.Extent2I(0, 0))
    #rawPrescanBBox = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(0, 0))
    emptyBox = afwGeom.BoxI()

    #Shift the right amp to the right by the full width:
    shiftp = afwGeom.Extent2I((width)*i,0)
    rawBBox.shift(shiftp)
    rawDataBBox.shift(shiftp)
    rawHorizontalOverscanBBox.shift(shiftp)

    #Add the defined information to the amp record:
    record.setHasRawInfo(True) #Sets the first Flag=True
    record.setRawFlipX(False)  #Sets the second Flag=False
    record.setRawFlipY(False)  #Sets the third Flag=False
    record.setBBox(bbox)
    record.setName('left' if i == 0 else 'right')
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
    record.setRawVerticalOverscanBBox(emptyBox) #We don't have any Vertical OS
    record.setRawPrescanBBox(emptyBox) #...nor prescan.
    
def makeCcd(ccdId):
    '''
    Make a CCD out of a set of amps
    Remove the for loop if you only have one amp
    per CCD.
    '''
    schema = afwTable.AmpInfoTable.makeMinimalSchema()
    ampCatalog = afwTable.AmpInfoCatalog(schema)
    for i in range(2):
        addAmp(ampCatalog, i,readout[ccdId][i],gain_all[ccdId][i])
    return ampCatalog.writeFits('cc1%s_superbit.fits' %ccdId)
        
def main():
    '''
    Make a set of CCDs.
    Remove the for loop if you only have one CCD.
    '''
    for i in range(3):
        camera = makeCcd(i)
            
if __name__ == "__main__":
    main()
