import lsst.afw.cameraGeom.cameraConfig

#Set the plate scale in arcsec/mm:
#Not strictly necessary.
#config.plateScale=206.67

#This defines the native coordinate system:
#FocalPlane is (x,y) in mm (rather than radians or pixels, for example).
config.transformDict.nativeSys='FocalPlane'

#For some reason, it must have "FieldAngle" transform defined:
config.transformDict.transforms={}
config.transformDict.transforms['FieldAngle']=lsst.afw.geom.transformConfig.TransformConfig()

# coeffs = [0,1] is the default. This is only necessary if you want to convert
#between positions on the focal plane.
config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.retarget(target=lsst.afw.geom.transformRegistry['radial'])
config.transformDict.transforms['FieldAngle'].transform['inverted'].transform.coeffs=[0.0, 1.0]
config.transformDict.transforms['FieldAngle'].transform.name='inverted'

#Define a list of detectors:
#If you have more than one detector, just repeat what is here for
#detector[0], but for detector[1], detector[2]...
config.detectorList={}
config.detectorList[0]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()

#All non-commented lines ARE REQUIRED for CameraMapper:
# y0 of pixel bounding box
config.detectorList[0].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[0].bbox_y1=4383

# x1 of pixel bounding box
config.detectorList[0].bbox_x1=6575

# x0 of pixel bounding box
config.detectorList[0].bbox_x0=0

# Name of detector slot
config.detectorList[0].name='superbitccd'

# Pixel size in mm
config.detectorList[0].pixelSize_x=0.005
config.detectorList[0].pixelSize_x=0.0055
config.detectorList[0].pixelSize_y=0.0055

# Name of native coordinate system
config.detectorList[0].transformDict.nativeSys='Pixels'

# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_x=3287.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_y=2191

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[0].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_x=0.

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_y=0.

config.detectorList[0].yawDeg=0.0
config.detectorList[0].rollDeg=0.0
config.detectorList[0].pitchDeg=0.0

# Serial string associated with this specific detector
config.detectorList[0].serial='KAI-29050'

# ID of detector slot
config.detectorList[0].id=0
