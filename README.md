# An LSST Obs package for SuperBIT

This obs package tells the LSST stack how to process data taken with SuperBIT. It describes:
- the basic properties of the detectors in `camera` (size, gain etc);
- the filesystem of the input and output data in `policy`;
- the configuration parameters that tell the stack's processing modules what to do in `config`;

and includes various python scripts in `python/lsst/obs/superbit/` which the stack uses to interact with the data.

To use this obs package, you first need to install the LSST stack on your system. Installation instructions are provided at:
https://pipelines.lsst.io/install/lsstsw.html

(Edit: Recently, the lsst-build installation that the above link points to has been failing on our systems, despite us following the same procedures as we did when installing previous versions of the stack. We've instead moved over to the `newinstall.sh` installation system described at https://pipelines.lsst.io/install/newinstall.html , which seems to work fine).

I prefer to install and run the stack within the Bourne-again shell (bash); when I first started using the LSST stack, I tried to run it under C-shell, but it failed. I could only get it to work using bash, and I've stuck with that ever since. I also recommend that you run the `lsstsw/bin/setup.sh` script each time you open a new shell by adding the command to your `.bashrc` file (the following instructions assume that you have done so, and that you're also using bash).

After the install script has finished running, you must clone this repository into the stack. I suggest you make a fork of this repository on Github, then clone it from there. From within the directory you called the install script from, execute the following:
```
cd lsstsw/stack/Linux64
```
or
```
cd lsst_stack/stack/current/Linux64/
```
(depending on how you installed the stack), then:
```
git clone git@github.com:YOUR-GITHUB-USER-AREA/obs_superbit.git
```

Next, you must tell the stack how to find `obs_superbit`. This is done using the eups versioning system (which is installed as part of the stack). At the (bash) command line execute:
```
eups declare obs_superbit v1 -r /full/path/to/lsstsw/stack/Linux64/obs_superbit
eups declare -t current obs_superbit v1
```
With the second command telling the stack to use version `v1` by default.

Once `obs_superbit` has been declared, it can be setup, which must be done in order to use it to process your data. Setting up is done using:
```
setup obs_superbit
```

Once setup, you can use `obs_superbit` to process your SuperBIT data with the LSST stack.

In summary, the following block of bash commands will:
- ingest raw data;
- create and ingest calibration frames;
- process the exposures, including source detection;
- coadd the exposures to create a deep coadd, and perform source detection on coadd.

Assuming all your raw data (both science and calibration files!) is contained within `./rawData`:
```
#!/bin/bash
mkdir -p DATA/CALIB
echo "lsst.obs.superbit.superbitMapper.SuperbitMapper" > DATA/_mapper

ingestImages.py DATA ./rawData/*.fits --mode=link --ignore-ingested

constructBias.py DATA --calib DATA/CALIB --output=Cals --id dataType=BIAS --cores=6 --clobber-config
```
Or, if you are running on a machine without a batch system for jobs, e.g. a laptop:
```
constructBias.py DATA --calib DATA/CALIB --output=Cals --id dataType=Bias --batch-type=None --cores=2 --clobber-config
ingestCalibs.py DATA --calib DATA/CALIB 'Cals/BIAS/*/NONE/*.fits' --validity 180

constructDark.py DATA --calib DATA/CALIB --output=Cals --id dataType=DARK --cores=6 --clobber-config
ingestCalibs.py DATA --calib DATA/CALIB 'Cals/DARK/*/NONE/*.fits' --validity 180

constructFlat.py DATA --calib DATA/CALIB --output=Cals --id dataType=FLAT filter=G --cores=6 --clobber-config
ingestCalibs.py DATA --calib DATA/CALIB 'Cals/FLAT/*/*/*.fits' --validity 180 --config clobber=True

singleFrameDriver.py DATA --rerun outSFD --calib DATA/CALIB --id filter=G --clobber-config --cores 6
makeDiscreteSkyMap.py DATA --rerun outSFD:outMDSM --id filter=G --clobber-config
coaddDriver.py DATA --id filter=G --cores 6 --rerun outMDSM:outCD --clobber-config
multiBandDriver.py DATA --id filter=L dateObs=2018-07-22 --cores 6 --rerun outCD:outMBD --clobber-config
```

Other filters can be processed via `filter=X` within the `--id` block.  
