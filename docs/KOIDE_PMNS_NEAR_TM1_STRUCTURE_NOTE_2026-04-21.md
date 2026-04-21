# Koide Loop Iteration 11 — I5 Mechanism: Near-TM1 Structure

**Date:** 2026-04-21 (iter 11)
**Attack target:** Refine iter 5's single-rotation no-go; find dominant mass-basis rotation.
**Status:** **SOFT-TM1 STRUCTURE IDENTIFIED** (mass-basis near-rotation around ν_1 axis)
**Runner:** `scripts/frontier_koide_pmns_near_tm1_structure.py` (19/19 PASS)

---

## One-line finding

Iter 4 V_conj is **V_TBM right-multiplied** by a rotation that is ~97%
aligned with the ν_1 axis (= V_TBM col_1) at angle ~0.168 rad (closest
to Q/4 = 1/6, 0.9% off). This is a **soft-TM1 deformation** —
structurally cleaner than iter 5's flavor-basis analysis (0.058 vs 0.109
distance).

## Key numerical findings

1. **Right-mult decomposition** `R_right = V_TBM^T · V_conj` has:
   - Angle: 0.1682 rad = 9.636°
   - Axis: (-0.859, 0.480, 0.177)

2. **Axis near ν_1 (V_TBM col_1)**:
   - V_TBM col_1 = (2, -1, -1)/√6 = (0.816, -0.408, -0.408)
   - Overlap |axis · col_1| = **0.970** (with negative sign)
   - Suggests a "near-TM1" rotation (TM1 preserves col_1 exactly).

3. **Best single-rotation approximation (right-mult, mass basis)**:
   - R(-col_1, exact angle): dist 0.058 ← best
   - R(-col_1, Q/4): dist 0.058 (Q/4 = 1/6 angle approximation)
   - Baseline |V_conj - V_TBM|: 0.238

4. **Mass-basis vs flavor-basis comparison**:
   - Iter 5 best (flavor left-mult): dist 0.109 (axis (0,1,-1)/√2)
   - Iter 11 best (mass right-mult): **dist 0.058** (axis -col_1)
   - Mass-basis picture gives 76% gap reduction vs 54% for flavor.

5. **Angle candidate gaps** (to exact 0.1682):
   - δ·Q = 4/27 = 0.1481: 11.91% off
   - √Q·δ = 0.1814: 7.88% off
   - **Q/4 = 1/6 = 0.1667: 0.90% off** ← cleanest

## "Soft-TM1" interpretation

Strict TM1 would preserve V_TBM col_1 exactly: |V_{e1}|² = 2/3, rotation
angle in (col_2, col_3) plane only. Iter 4 V_conj is CLOSE but:

- **|V_{e1}|² = 0.684** (gap +0.018 from exact 2/3)
- **sin²θ_12 = 73/243 = 0.3004** (gap -0.018 from strict TM1 prediction 0.318)

So iter 4 conjecture is "soft-TM1" — approximately TM1 but deformed at
~6% level. The deformation direction is NOT fully along the (col_2, col_3)
plane (which would be strict TM1); it has a small col_1 component (3%
from perfect axis alignment).

## What this iteration contributes

**Iter 11 is mechanism NARROWING**, not closure:

- Iter 5 (flavor single-rot): ruled out simplest mechanism.
- Iter 11 (mass single-rot): identified **soft-TM1** as dominant structure.

The iter 4 V_conj mechanism is now characterized as:
> A rotation in mass basis ~97% aligned with the ν_1 eigenvector axis,
> by angle ~Q/4 ≈ 0.167 rad, with ~3% residual for axis alignment and
> ~1% for angle value.

## Open questions (iter 12+ targets)

- **Q/4 coefficient derivation**: Why 1/4 specifically? Not obviously
  forced by retained (Q, δ) axioms. Candidates: square-root structure
  relating to SELECTOR² = Q, √Q = SELECTOR/I normalization, etc.

- **Residual axis component (3%)**: The axis differs from -col_1 by
  ~3%. This suggests a subleading second-rotation component. Search for
  a clean (Q, δ)-decomposition of this residual.

- **Connection to CP phase**: Iter 8 identified Z₂ CP orientation as
  separate DOF. TM1 rotations are real (J_CP = 0). Adding CP-phase is
  a separate layer.

## Status update

| Gap | Iter 10 status | Iter 11 update |
|---|---|---|
| I1 (Q=2/3) | RETAINED-FORCED | (unchanged) |
| I2/P (δ=2/9) | RETAINED-FORCED | (unchanged) |
| I5 mechanism | composite (iter 5) | **soft-TM1 mass-basis rotation** (iter 11) |
| I5 CP sign | Z₂ orientation DOF (iter 8) | (unchanged) |

I5's mechanism space has been systematically narrowed:
- Iter 3: TBM is leading order.
- Iter 4: (Q, δ)-deformation fits NuFit 1σ.
- Iter 5: single flavor-rotation ruled out.
- Iter 8: CP-orientation is Z₂ DOF.
- Iter 11: mass-basis rotation ~97% aligned with ν_1 axis, angle ~Q/4.

Remaining open: exact axis alignment, exact angle coefficient,
CP-orientation selection.
