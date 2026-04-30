# DM Leptogenesis Projection Theorem

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-15
**Branch:** `codex/dm-main-refresh`
**Script:** `scripts/frontier_dm_leptogenesis_projection_theorem.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Result

The physical denominator in the coherent leptogenesis kernel is now fixed
theorem-grade on this branch:

- `Y_+(H) = H^(1/2)` on the intrinsic positive right-orbit representative
- `Y_mass = Y_+ U_M`
- `Y_mass^dag Y_mass = U_M^dag H U_M = K_mass`

Therefore

- `physical denominator = (Y_mass^dag Y_mass)00 = (K_mass)00 = K00`

This is a positive theorem, not a benchmark substitution.

## Comparison to older runners

- the older reduced runner still worked on the reduced texture benchmark
  where `(Y^dag Y)11 = y0^2`
- the exact-source diagnostic already identified the missing issue as the
  thermal / projection map from the exact heavy-basis tensor to `epsilon_1`
- the refreshed exact-kernel runner already inserted `/K00` explicitly

So the denominator/projection identity is now hardened. The remaining closure
question moves to the washout / thermal side.
