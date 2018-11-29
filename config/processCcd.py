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
config.isr.doWrite = True
config.isr.doBias = True
config.isr.doDark=True
config.isr.doFlat=True

