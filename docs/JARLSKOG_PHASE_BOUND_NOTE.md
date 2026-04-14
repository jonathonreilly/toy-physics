# Jarlskog Phase Bound Note

**Date:** 2026-04-14  
**Status:** BOUNDED PARTIAL PREDICTION  
**Script:** `scripts/frontier_jarlskog_derived.py`

## Summary

The safe current flavor-companion statement on `main` is:

> the framework derives the discrete CP phase `delta = 2pi/3` from the `Z_3`
> structure, and with observed CKM mixing angles that phase gives
> `J = 3.145 x 10^-5`, within about `2.1%` of the PDG value `3.08 x 10^-5`.

This is bounded support for the CP-violation sector. It is **not** a closed
CKM theorem.

## Safe Claim Boundary

### Safe to say

- `delta = 2pi/3` is the derived part
- `J = 3.145 x 10^-5` from that phase plus observed mixing angles is a bounded
  partial prediction
- a zero-CKM-input `Z_3`/FN estimate exists at the correct order of magnitude,
  but is not precision closure

### Not safe to say

- that the full CKM matrix is derived
- that the Cabibbo angle is currently derived on the same main-branch surface
- that the flavor gate is closed

## Main Numerical Read

### Phase-only partial prediction

Using:

- derived phase `delta = 2pi/3`
- observed `s12`, `s23`, `s13`

the framework gives:

- `J = 3.145 x 10^-5`
- PDG reference: `3.08 x 10^-5`
- deviation: about `+2.1%`

This is the strongest current safe Jarlskog statement on `main`.

### Zero-CKM-input structural estimate

The same runner also records a `Z_3`/FN estimate with no CKM-angle imports:

- `J_Z3_FN = 1.303 x 10^-4`
- about `4.23x` the PDG value

That is a bounded structural estimate, not the publication-facing headline
number.

## Cabibbo Relation Status

The older combined Cabibbo/Jarlskog route note has been retired from the main
authority path.

Reason:

- the old note mixed a fitted Cabibbo relation with the bounded Jarlskog phase
  result
- it referenced a non-main-branch baryogenesis script
- its formula/presentation was not coherent enough to remain on the active
  publication surface

So the current package position is:

- **Jarlskog partial prediction:** active bounded companion
- **Cabibbo bounded companion:** still active on `main`, but through the
  cleaned Cabibbo / CKM magnitude authority surface rather than the old
  combined note

## Relationship To Other Flavor Notes

- quantitative CKM magnitude package:
  [CKM_MASS_BASIS_NNI_NOTE.md](CKM_MASS_BASIS_NNI_NOTE.md)
- current bounded Cabibbo authority:
  [CABIBBO_BOUND_NOTE.md](CABIBBO_BOUND_NOTE.md)
- historical combined Cabibbo/Jarlskog route note:
  [work_history/CABIBBO_JARLSKOG_ROUTE_NOTE_2026-04-12.md](work_history/CABIBBO_JARLSKOG_ROUTE_NOTE_2026-04-12.md)

## Publication Disposition

- keep this note as the current authority for the bounded Jarlskog row
- do not surface Cabibbo as an active bounded row until it has a coherent
  main-branch authority note and runner
