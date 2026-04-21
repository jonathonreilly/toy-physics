# Koide Loop Iteration 17 — I5: e-Row Structural Uniqueness

**Date:** 2026-04-21 (iter 17)
**Attack target:** Explain WHY iter 16's complex-multiplication uses V_TBM's e-row.
**Status:** **"Why e-row?" sub-question ANSWERED** (forced by TBM property)
**Runner:** `scripts/frontier_koide_pmns_e_row_uniqueness.py` (14/14 PASS)

---

## One-line finding

The V_TBM e-row selection in iter 16's complex-multiplication identity
is **structurally UNIQUE**: it is the only row with V[e, 3] = 0
(inherited from TBM's θ_13 = 0 property), giving it a pure 2D structure
in the (ν_1, ν_2) plane.

## The structural uniqueness

V_TBM rows in mass basis (from iter 3):

| Row | Components | Norm in (ν_1, ν_2) plane |
|---|---|---|
| e | (√(2/3), √(1/3), **0**) | 1 (unit — pure 2D) |
| μ | (−√(1/6), √(1/3), √(1/2)) | 1/2 |
| τ | (+√(1/6), −√(1/3), √(1/2)) | 1/2 |

Only the e-row has V[e, 3] = 0, because TBM has θ_13 = 0 (the "reactor
angle is zero at TBM"). The other rows have V[·, 3] = ±√(1/2) from the
θ_23 = π/4 (maximal μ-τ mixing) structure.

## Why this matters for iter 16

Iter 16 identified:

```
axis_x + i · axis_y = z_e · w
  where z_e = V_TBM[e, 1] + i · V_TBM[e, 2] = exp(i · θ_12_TBM)
        w   = −δt_23 + i · t_13
```

The complex number z_e = e^{i·θ_12_TBM} is a **unit complex** (|z_e|² = 1)
precisely because the e-row is 2D-pure.

**Without V[e, 3] = 0**, the e-row couldn't be treated as a 2D complex
number. With it, the iter 16 identity has a clean geometric meaning:
**rotate the deformation vector w by angle θ_12_TBM in the (ν_1, ν_2)
plane**.

## Chain of forcing

1. **S_3 cubic symmetry** on Z³ (retained) → V_TBM is forced (iter 3).
2. **TBM property θ_13 = 0** → V_TBM[e, 3] = 0 (iter 17).
3. **V[e, 3] = 0** → (V[e,1], V[e,2]) is 2D unit complex z_e (iter 17).
4. **Deformation axis geometry** → axis_x + i·axis_y = z_e · w (iter 16).

The chain 1 → 2 → 3 → 4 is all retained-forced. Only the DEFORMATION
VECTOR w = (−δt_23, t_13) contains iter 4's conjecture — specifically,
the values t_13 = δ·Q and δt_23 = δ·Q/2 remain iter 4 conjectures
requiring separate derivation.

## What's still open

The **angle magnitudes** in iter 4:
- t_13 = δ · Q (why this specific product?)
- δt_23 = δ · Q / 2 (why half?)
- sin² θ_12 = 1/3 − δ² · Q (why coefficient −1?)

These were identified in iter 4 via numerical fit; they match NuFit to
1σ since 2020 (iter 13). But their derivation from retained Cl(3)/Z³
mechanism remains the iter 18+ target.

Iter 17 closes the "axis DIRECTION structural uniqueness" question.
The "angle MAGNITUDES" question is separate.

## Status update

| Gap | Pre-iter-17 | Post-iter-17 |
|---|---|---|
| I1, I2/P | RETAINED-FORCED | (unchanged) |
| I5 angles | observationally robust | (unchanged) |
| I5 mechanism primary | α = −θ_13 (iter 15), complex-mult structure (iter 16) | **e-row uniqueness proven** (iter 17) |
| I5 mechanism magnitudes | open | (unchanged) |

## Iter 18+ targets

1. **Derive t_13 = δ·Q** from retained Cl(3)/Z³ mechanism.
2. **Derive δt_23 = δ·Q/2** (the half-factor).
3. **Derive sin² θ_12 = 1/3 − δ²·Q** (the solar angle correction).
4. **Quark-sector parallel** or **publication-draft consolidation**.

## Synthesis of structural picture

After iter 17, the I5 mechanism has TWO clean structural identifications:

1. **Mass-basis TM1 rotation**: primary component α = −θ_13 around ν_1 (iter 15).
2. **Complex-multiplication axis**: direction determined by V_TBM e-row
   structure, itself forced by TBM θ_13 = 0 (iter 16 + 17).

What's NOT yet structural:
- Specific angle magnitudes (t_13 = δ·Q, etc.) — iter 4 conjecture.
- δ_CP sign (Z_2 orientation DOF from iter 8).

So I5 has **one piece retained-forced** (the axis direction structural
uniqueness, iter 17), and **several pieces conjectural**. This is
measurable progress over iter 15's mechanism-search state.
