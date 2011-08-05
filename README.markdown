# CDS Intensity Models

---

## Introduction

This Python code contains utilities used to calibrate various intensity models to CDS spreads.

## Usage

Graphs are created by running the `Graphs/GeneratePlots.py` script.  

Intensity models are implemented by subclassing the `CreditDefaultSwap` class, implemented in `CDS.py`.

Calibration procedures are implemented in the `Calibration.py` script, and analysis of calibration results is contained in the script `ParameterStabilityAnalysis.py`.  

## Implemented Intensity Models

* Homogenous Poisson (HP)
* Inhomogenous Poisson (IHP)
* Gamma-OU (G-OU)
* Inverse Gamma-OU (IG-OU)
* Cox-Ingersoll-Ross (CIR)