'''
The various parameters that control how each of the stack's
tasks operate are changed from their defaults via these
config files.

Each task can have its own config file, named after the name
of the task. For example, this is the config file for the
processCcd.py task.

To see a full list of configurable parameters associated with
a task (and their defaul values), call the task with 
`--show config` (without quotes), e.g.,
processCcd.py --show config

'''

#ISR:
#This is just an example of how to change a parameter.
#You don't have to write out the ISR image (but it
#can be useful to do so).

# Apply bias frame correction?
config.isr.doBias=True

# Apply dark frame correction?
config.isr.doDark=True

# Apply flat field correction?
config.isr.doFlat=False

# Apply fringe correction?
config.isr.doFringe=False

# Apply correction for CCD defects, e.g. hot pixels?
config.isr.doDefect=True

# Apply a distortion model based on camera geometry to the WCS?
config.isr.doAddDistortionModel=False

# Persist postISRCCD?
config.isr.doWrite=False

# Name of the bias data product
config.isr.biasDataProductName='bias'

# Name of the dark data product
config.isr.darkDataProductName='dark'

# Name of the flat data product
config.isr.flatDataProductName='flat'

# trim out non-data regions?
config.isr.assembleCcd.doTrim=True

# FITS headers to remove (in addition to DATASEC, BIASSEC, TRIMSEC and perhaps GAIN)
config.isr.assembleCcd.keysToRemove=[]

