# One-Generation Matter Closure Note

**Date:** 2026-04-14
**Status:** proposed_retained
**Scripts:** `scripts/frontier_right_handed_sector.py`, `scripts/frontier_anomaly_forces_time.py`
**Authority role:** canonical main-branch note for the retained one-generation matter-closure row

## Safe statement

The framework closes one Standard Model generation in the **full framework**:

- the graph-first selected-axis surface fixes the left-handed gauge/matter sector
- anomaly-forced time supplies the chirality structure and single-clock `3+1` closure
- anomaly cancellation then fixes the right-handed singlet completion on the Standard Model branch

The retained full-framework one-generation closure is therefore:

- `u_R : (1,3)_{+4/3}`
- `d_R : (1,3)_{-2/3}`
- `e_R : (1,1)_{-2}`
- `nu_R : (1,1)_0`

## Canonical derivation stack

1. [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](./LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
   fixes the safe left-handed selected-axis charge surface.
2. [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)
   shows that anomaly cancellation requires the opposite-chirality completion
   and that the framework closes on exactly one temporal direction.
3. `frontier_right_handed_sector.py` verifies the concrete completion chain:
   no weak singlets on the purely spatial `C^8` surface, proper chirality only
   on the 4D `C^16` surface, and anomaly cancellation fixing the Standard Model
   right-handed branch.

## Boundary

This note is intentionally narrower than an overclaim:

- retained: full-framework one-generation closure
- not retained: a derivation of the right-handed sector from the spatial graph alone

The temporal/chirality step is load-bearing. That is part of the accepted
framework claim, not a defect.

## Validation

- [frontier_anomaly_forces_time.py](./../scripts/frontier_anomaly_forces_time.py)
- [frontier_right_handed_sector.py](./../scripts/frontier_right_handed_sector.py)

Current main-branch runner state:

- `frontier_right_handed_sector.py`: `PASS=61`, `FAIL=0`
