# CDS Intensity Models

## Introduction

This Python code contains utilities used to calibrate various intensity models to CDS spreads.

## Usage

Intensity models are implemented by subclassing the `CreditDefaultSwap` class, implemented in `CDS.py`.

Calibration procedures are implemented in the `Calibration.py` script, and analysis of calibration results is contained in the script `ParameterStabilityAnalysis.py`.  

Copulas are implemented in the `Copula.py` script, and default times are simulated in the `CopulaSimulation.py` script.    

Graphs are created by running the `GeneratePlots.py` script.  


### Implemented Intensity Models

* Homogenous Poisson (HP)
* Inhomogenous Poisson (IHP)
* Gamma-OU (G-OU)
* Inverse Gamma-OU (IG-OU)
* Cox-Ingersoll-Ross (CIR)

### Implemented Copulas

* Gaussian copulas
* Students *t* copulas
* Clayton copulas

### Implemented Credit Derivatives

* Credit Default Swaps
* *k*-th-to-default Basket Swaps
* *k*-th-to-*l*-th CDO Tranches



