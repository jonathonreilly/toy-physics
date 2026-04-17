# Hypothesis: Critical Ratio Threshold for Off-Center Visibility

## Date
2026-03-30

## Statement
There exists a sharp critical ratio R_c = width / slit_sep below which off-center fringe visibility V(y≠0) is exactly zero, and the transition from zero to nonzero visibility is discontinuous (step function, not gradual onset).

## Prediction
- R_c lies between 1.0 and 2.5 based on the coarse sweep data.
- R_c is the SAME for all off-center positions y (i.e., it's a single universal threshold, not y-dependent).
- OR: R_c depends on y, with positions closer to center having a LOWER threshold (easier to reach from both slits). This would mean the threshold is really a function R_c(y).
- The transition is discontinuous: V jumps from exactly 0 to a finite value at R_c, with no gradual onset.

## Falsification Criteria
- If V transitions smoothly from 0 through small values (0.001, 0.01, etc.) rather than jumping, the threshold is not sharp — it's a gradual onset.
- If R_c varies chaotically with y rather than monotonically, the threshold is not a clean geometric property.

## Null Hypothesis
The "exact zeros" in the coarse sweep are an artifact of discrete grid spacing (integer coordinates). At finer parameter resolution, all visibility values would be nonzero.

## Relevant Prior Work
- `logs/2026-03-30-interference-offcenter-fringe-sweep.txt` — coarse data showing exact zeros and the approximate threshold.

## Proposed Experiments
1. Fine sweep width from 4 to 40 in steps of 2, slit_half from 1 to 12 in steps of 1.
2. For each geometry, measure V(y) at y=1,2,3,5.
3. Map the zero/nonzero boundary in (width, slit_sep) space.
4. Determine if the transition is discontinuous (V jumps from 0 to finite) or gradual.

## Status
PROPOSED
