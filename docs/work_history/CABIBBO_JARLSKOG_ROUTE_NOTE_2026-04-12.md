# Cabibbo Angle and Jarlskog Route Note

**Status:** historical route note only. The current main-branch authority
surface is split:

- Cabibbo bounded companion:
  [../CABIBBO_BOUND_NOTE.md](ckm/CABIBBO_BOUND_NOTE.md)
- Jarlskog bounded companion:
  [../JARLSKOG_PHASE_BOUND_NOTE.md](ckm/JARLSKOG_PHASE_BOUND_NOTE.md)

# Cabibbo Angle and Jarlskog Invariant -- Derived vs Fitted

**Date:** 2026-04-12  
**Status:** Honest reframing after codex review. Separates what is derived from what is input.  
**Script:** `scripts/frontier_baryogenesis.py` (tests 1-2)

**Current publication disposition:** historical route note; superseded on the
main authority path.

---

## The Results

### Cabibbo Angle

  sin(theta_C) = sqrt(epsilon), with epsilon identified as the FN parameter

  **Predicted: sin(theta_C) = 0.2236**  
  **Observed:  sin(theta_C) = 0.2243 (PDG 2024)**  
  **Ratio: 0.997 (0.3% match)**

### Jarlskog Invariant

  J = c_12 s_12 c_23 s_23 c_13^2 s_13 sin(delta), with delta = 2pi/3

  **Predicted: J = 3.145 x 10^-5**  
  **Observed:  J = 3.08 x 10^-5 (PDG 2024)**  
  **Ratio: 1.021 (2.1% match)**

---

## Honest Decomposition: What Is Derived vs What Is Input

### Derived from Z_3

- **The CP phase delta = 2pi/3.** This is a genuine output of the Z_3
  symmetry of the 3-colorable lattice. The same Z_3 that gives 3 color
  charges and 3 generations also fixes the CP-violating phase to one of
  the cube roots of unity. This is the strongest part of the prediction.

- **The Jarlskog invariant's 2.1% match** comes primarily from this
  derived phase. The factor sin(2pi/3) = sqrt(3)/2 enters the Jarlskog
  formula directly, and this value IS derived from the lattice symmetry.

### Input (not derived)

- **The Froggatt-Nielsen expansion parameter epsilon = 1/3.** The Cabibbo
  angle match (0.3%) comes from the formula sin(theta_C) = sqrt(epsilon)
  with epsilon = 1/3. The identification of epsilon with 1/3 is an INPUT:
  it is chosen to match the observed Cabibbo angle. The 0.3% "prediction"
  is therefore partly circular -- it is a 0.3% residual from a fit, not
  a zero-parameter prediction.

- **The FN mechanism itself.** The Froggatt-Nielsen texture ansatz (mass
  matrix entries scaling as epsilon^|q_i - q_j|) is assumed, not derived
  from the lattice dynamics.

- **The other CKM angles (theta_23, theta_13).** These enter the Jarlskog
  formula but are taken from observation, not independently predicted.
  The Jarlskog match therefore tests the phase prediction, not a complete
  CKM prediction.

---

## Corrected Claim Strength

| Quantity | What is tested | What is derived | What is input |
|---|---|---|---|
| sin(theta_C) = 0.2236 | FN formula + epsilon value | nothing -- this is the defining equation for epsilon | epsilon = 1/3 (fitted) |
| J = 3.145 x 10^-5 | CP phase in Jarlskog formula | delta = 2pi/3 from Z_3 | epsilon = 1/3, theta_23, theta_13 from data |

The honest summary:

- The **Jarlskog invariant** is a genuine partial prediction: the CP phase
  delta = 2pi/3 is derived from Z_3, and the resulting J is within 2.1%
  of observation. The other mixing angles entering J are taken from data.

- The **Cabibbo angle** match is NOT a zero-parameter prediction. It is
  the statement that epsilon = 1/3 fits the Cabibbo angle to 0.3%. The
  value epsilon = 1/3 is motivated by the Z_3 structure but is not derived
  from it in a unique way.

---

## Relationship to CKM Charge Selection

These numbers come from the baryogenesis script (`frontier_baryogenesis.py`),
NOT from the CKM charge-selection script (`frontier_ckm_dynamical_selection.py`).

The charge-selection script is a separate calculation that attempts to
narrow Froggatt-Nielsen charge assignments using S_3 symmetry. It does not
quantitatively reproduce the CKM matrix (its V_us = 0.111 vs observed
0.224). See `docs/CKM_CHARGE_SELECTION_HONEST_NOTE.md` for the honest
status of that lane.

The two calculations should not be conflated:
- **Baryogenesis script:** uses Z_3 phase delta = 2pi/3 and fitted epsilon
  to get Cabibbo/Jarlskog numbers
- **CKM charge-selection script:** uses Z_3 charges and S_3 symmetry to
  select FN charge patterns, but does not reproduce quantitative CKM

---

## Caveats

1. The FN parameter epsilon = 1/3 needs a derivation from the lattice
   structure to upgrade the Cabibbo match from "fit" to "prediction."
2. The other CKM angles (theta_23, theta_13) have not been independently
   predicted -- they are taken from PDG data when computing J.
3. The O(1) coefficients in the FN texture are assumed to be exactly 1.
   Realistic O(1) variation would change the predicted values.

## Scripts

- `scripts/frontier_baryogenesis.py` (contains the calculation, tests 1-2)
- `logs/2026-04-12-frontier_baryogenesis.txt`
