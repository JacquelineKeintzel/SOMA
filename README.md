# SOMA
SuperKEKB Optics Measurement Analysis package, based on pyLHC (Betabeat.src and OMC3).


# 1 Prerequisites

- Python2 and Beta-Beat.src, see also:  https://github.com/pylhc/Beta-Beat.src.
- Python3 and OMC3, see also: https://github.com/pylhc/omc3
- SAD (Strategic Accelerator Design), see also: https://github.com/KatsOide/SAD


# 2 SOMA

This code is used to analyse SuperKEKB Turn-by-Turn Optics measurements as follows:

1) Edit *parameters.txt* to define input, output, model, lattice and which code should be used for the analysis. Lines starting with "#" are ignored. Additionall an example file containing the correct paths at KEK (*parameters_atKEK.txt*) is given.

2) Run *run\_SOMA.py* from the command line. The following options are available:

Mandatory arguments are:
- **"- -pathnames":**
Path to *pathnames.txt* file, which contains all other paths necessary for the package.

Optional arguments are:
- **"- -harmonic1"/"-h1":**
Harmonic analysis without knowledge of BPM synch. This is enough to obtain tunes.
- **"- -plotsdds1"/"-ps1":**
Plotting of raw sdds files, before synchronization.
- **"- -plotfreq1"/"-pf1":**
Plotting of frequency spectrum before synchronization.
- **"- -optics1"/"-o1":**
Phase analysis of harmonic1 output without BPM synch knowledge.
- **"- -plotasynch1"/"-pa1":**
Plotting of BPM synchronisation from phase1 output, before synch fix is applied.
- **"- -asynch"/"-aa":**
Analysis of BPM synchronisation from phase1 output.
- **"- -harmonic2"/"-h2":**
sdds conversion and harmonic analysis with knowledge of BPM synch.
- **"- -plotsdds1"/"-ps2":**
Plotting of synchronized sdds files.
- **"- -optics2"/"-o2":**
Phase analysis of harmonic2 output with knowledge of BPM synch.
- **"- -plotoptics22"/"-po2":**
Plots the optics after BPM synchronisation.
- **"- -plotasynch2"/"-pa2":**
Plotting of BPM synchronisation from phase2 output, after synch fix is applied.
- **"- -plotcalib1"/"-pc1":**
Plotting of BPM calibration from phase2 output, before calibration is applied.
- **"- -calib"/"-c":**
Estimates the BPM calibration (beta from phase vs amplitude) for this measurement.
- **"- -optics3"/"-o3":**
Phase analysis of harmonic3 output with knowledge of BPM calibration.
- **"- -plotoptics22"/"-po3":**
Plots the optics after BPM calibration.
- **"- -plotcalib2"/"-pc2":**
Plotting of BPM calibration from phase3 output, after calibration is applied.
- **"- -all_at_once"/"-all":**
To be used when all files should run at once, e.g. for dispersion measurement with off-momentum files.
- **"- --omc3"/"-omc3":**
Use OMC3/python3 instead of BetaBeat.src/python2.


Concerning the optional arguments, the following commands depend, expressed by " <- " on each other:
    -h1 <- -p1 <- -aa <- -h2 <- -p2 <- -c <- -p3 .

Plotting of the recorded orbit data, the frequency output, BPM synchronization colormap (i.e. total phase advance error with respect to the model), BPM calibration estimate and the optics can be called and depend on previous analysis, e.g:
    -h1 <- -pf1
    -o2 <- -po2
    -o2 <- -c


# 3 Get data from SKEKB server 

These scripts can only be run at SKEKB cluster with required access right. Connection requires the following: 

- *VPN connection* : To requested at https://ccportal.kek.jp/accounts/login/?next=/application/
- *KEK computing account* : To be requested "For general users" at https://acc-physics.kek.jp/SAD/links/account_eng/

With these permissions one can access the following servers:
- *afsad1* : ssh user@afsad1.kek.jp
- *alsad1* : ssh user@alsad1.kek.jp


SAD can be run using */SAD/bin/gs -env skekb* from the command line.


Measurement files are stored in the following repository and should be copied to the personal folder:
- In alsad1: */nfs/sadstorage-ldata/SuperKEKB/KCG/SAD/BM/TBT/data/2024/02/06*
- In afsad1: */ldata/SuperKEKB/KCG/SAD/BM/TBT/data/2024/02/06*


Chromaticity files are stored in the following repository and should be copied to the personal folder:
*/ldata/SuperKEKB/KCG/LER/SXP/2024/02/*


To get the SAD lattice which is used at a specific measurement acquisition time run *extract\_sadlattice.sad* from the command line. Please note that the ring (HER or LER) and the measurement file for which the lattice should be extracted must be changed lines 2, 7 and 13. 
WARNING: This only works on afsad1!


To extract beam current in a specific time interval, run the following command:
*/usr/local/bin/kblogrdc -t 20210222190000-20210222194300d1 -r BMLDCCT:CURRENT, MHDCCT:CURRENT -f 'kaleida' BM/DCCT > cur_2021_02_22_19_40_00.txt*


This code allows to extract measurements obtained from Closed Orbit Distortion (COD) and converts them to a twiss-file.

Run *run\_convertCODtoTwiss.py* from the command line. The following options are available:

- **"- -beta":**
SAD timestamp of COD measurements for beta;
e.g. /nfs/sadnas1a/ldata/SuperKEKB/KCG/HER/MeasOpt/2019/11/BETA_RAW_2019_11_21_17:58:18
- **"- -disp":**
SAD timestamp of COD measurements for dispersion; 
e.g. /nfs/sadnas1a/ldata/SuperKEKB/KCG/HER/MeasOpt/2019/11/DISP_2019_11_12_12:40:54
- **"- -coup":**
SAD timestamp of COD measurements for coupling; 
e.g. /nfs/sadnas1a/ldata/SuperKEKB/KCG/HER/MeasOpt/2019/11/XYC_2019_11_29_15:41:16
- **"- -ring":**
RingID, either HER or LER
- **"- -output":**
Define output directory
- **"- -model":**
Path to twiss file "twiss_elements.dat" containing all BPMs.