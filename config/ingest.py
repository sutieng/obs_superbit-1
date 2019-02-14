from lsst.obs.superbit.ingest import SuperbitParseTask
config.parse.retarget(SuperbitParseTask)


config.parse.translation = {'dataType':'OBSTYPE',
                            'expTime':'EXPTIME',
                            'filter':'FILTER',
                            'visit':'FRAMEID',
                            'ccd' : 'DETNAME'} 

config.parse.translators = {'dateObs':'translateDate',
                            'taiObs':'translateDate',
                                }

config.register.visit = ['visit','ccd', 'filter', 'dateObs','taiObs']

config.register.unique = ['visit','ccd','filter']

config.register.columns = {'visit':'int',
                           'filter':'text',
                           'dataType':'text',
                           'expTime':'double',
                           'dateObs':'text',
                           'taiObs':'text',
                            'ccd' : 'text'}

