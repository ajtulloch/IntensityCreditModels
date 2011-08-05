CDS Calibration
===============

This Python code contains utilities used to calibrate various intensity models to CDS spreads.

Supported
---------

* Homogenous Poisson
* Inhomogenous Poisson
* Gamma-OU
* Inverse Gamma-OU
* Cox-Ingersoll-Ross (CIR)

Usage
-----

Graphs are created by running the `Graphs/GeneratePlots.py` script.  

Intensity models are implemented by subclassing the `CreditDefaultSwap` class, implemented in `CDS.py`.

Calibration procedures are implemented in the `PoissonCalibration.py` script, and analysis of calibration results is done in `ParameterStabilityAnalysis.py` script.  
