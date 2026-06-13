# Roller Compaction Deformation Analysis

Calculate roller bending deflection from powder and geometry parameters.

## Input Parameters

D = 8 mm (roller diameter)
L = 50 mm (roller length)
h = 150 um (target gap)
sigma_A = 200 g/m2 (areal density)
D50 = 15 um (particle size)
h0 = 356 um (feed thickness, from R0 approx 0.25)
E = 200 GPa (roller modulus, steel)
rho_s = 2250 kg/m3 (graphite true density)
sigma_y = 50 MPa (flake graphite effective yield)

## Method

Step 1: Target relative density
  R_target = sigma_A / (rho_s * h) = 0.2 / (2250 * 0.00015) = 0.593

Step 2: Initial relative density
  R0 approx 0.25  (flake graphite, hand-levelled)
  h0 = sigma_A / (rho_s * R0) = 0.2 / (2250 * 0.25) = 356 um

Step 3: Contact arc length
  Dh = h0 - h = 356 - 150 = 206 um
  S = sqrt(D * Dh) = sqrt(0.008 * 0.000206) = 1.28 mm

Step 4: Gap and density along the arc
  h(x) = h + x*x/D  (parabolic approximation)
  R(x) = sigma_A / (rho_s * h(x))
  At x=0 (center): h=150um, R=0.593 (densest)
  At x=S/2 (edges): h=356um, R=0.25 (entry)

Step 5: Pressure distribution (Helle-Fleck Stage I)
  p(R) = 1.5 * sigma_y * (R-R0)^2 / [R * (1-R0)]
  At R=0.593: p = 1.5*50e6*0.343^2/(0.593*0.75) = 19.8 MPa

Step 6: Total force
  F = L * integral(p(x), -S/2, S/2) = 987 N

Step 7: Bending deflection (simply-supported beam)
  I = pi * D^4 / 64 = 2.01e-10 m^4
  w = F / L = 19740 N/m
  delta = 5 * w * L^4 / (384 * E * I) = 40.0 um

Step 8: Deviation
  deviation = delta / h * 100 = 26.7 percent
  Grade: D (unacceptable)

## Key Results (sigma_y = 50 MPa)

  D=8mm   L=20mm:  delta=1.0um   dev=0.7%   Grade A
  D=8mm   L=30mm:  delta=5.2um   dev=3.5%   Grade B
  D=8mm   L=40mm:  delta=16.4um  dev=10.9%  Grade D
  D=8mm   L=50mm:  delta=40.0um  dev=26.7%  Grade D
  D=20mm  L=50mm:  delta=1.6um   dev=1.1%   Grade B
  D=30mm  L=50mm:  delta=0.4um   dev=0.3%   Grade A
  D=50mm L=200mm:  delta=0.2um   dev=0.1%   Grade A

## Grading Criteria

  A: under 1 percent -- negligible, excellent uniformity
  B: 1 to 5 percent -- marginal, slight non-uniformity
  C: 5 to 10 percent -- significant, needs attention
  D: over 10 percent -- unacceptable, redesign required

## Parameter Sensitivity

  sigma_y: linear effect on result -- MOST CRITICAL
  D: 4th-power effect -- double D makes delta divided by 16
  L: 4th-power effect -- double L makes delta times 16
  h0, R0: moderate effect through contact arc length

## Uncertainties

  sigma_y: Calibrate via Rocky DEM single-axis compaction test
  R0, h0: Measure directly or use conservative estimate
  D, L, h: From design drawing, accurate

## Model Assumptions

  1. Helle-Fleck Stage I compaction law (R under 0.9)
  2. Parabolic gap h(x)=h+xx/D
  3. Simply-supported beam for roller bending
  4. Quasi-static, no rate effects
  5. Uniform areal density across roller width

## Script Usage

  python roller_study.py           -- single-point calculation
  python roller_study.py --sweep   -- full parametric sweeps
  Edit top variables in roller_study.py to customize.

---
Script: roller_study.py  |  Requires: Python + NumPy
