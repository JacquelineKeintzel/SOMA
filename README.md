# SOMA

Mandatory arguments are:
- **"- -pathnames":**
Path to *pathnames.txt* file, which contains all other paths necessary for the package.

Optional arguments are:
- **"- -harmonic1"/"-h1":**
Harmonic analysis without knowledge of BPM synch. This is enough to obtain tunes.
- **"- -optics1"/"-p1":**
Phase analysis of harmonic1 output without BPM synch knowledge.
- **"- -plotasynch1"/"-pa1":**
Plotting of BPM synchronisation from phase1 output, before synch fix is applied.
- **"- -asynch"/"-aa":**
Analysis of BPM synchronisation from phase1 output.
- **"- -harmonic2"/"-h2":**
sdds conversion and harmonic analysis with knowledge of BPM synch.
- **"- -optics2"/"-p2":**
Phase analysis of harmonic2 output with knowledge of BPM synch.
- **"- -plotoptics22"/"-po2":**
Plots the optics repository after BPM synchronisation.
- **"- -plotasynch2"/"-pa2":**
Plotting of BPM synchronisation from phase2 output, after synch fix is applied.
- **"- -calib"/"-c":**
Calculates the BPM calibration for this measurement.
- **"- -optics3"/"-p3":**
Phase analysis of harmonic3 output with knowledge of BPM calibration.
- **"- -plotcalib1"/"-pc1":**
Plotting of BPM calibration from phase2 output, before calibration is applied.
- **"- -plotcalib2"/"-pc2":**
Plotting of BPM calibration from phase3 output, after calibration is applied.
- **"- -group_runs"/"-g":**
To be used when multiple runs for a single setting are available.
- **"- -all_at_once"/"-all":**
To be used when all files should run at once, e.g. for dispersion measurement with off-momentum files.
- **"- -debug"/"-db":**
Debug option. Only does analysis on 2 files, as opposed to all.
- **"- -omc3"/"-omc3":**
Using the OMC3 in python3 analysis package instead of Beta-Beat.src in python2.
