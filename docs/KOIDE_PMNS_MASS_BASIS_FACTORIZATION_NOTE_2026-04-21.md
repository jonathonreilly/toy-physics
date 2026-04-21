# Koide Loop Iteration 15 — I5 Mechanism: Mass-Basis 2-Rotation Factorization

**Date:** 2026-04-21 (iter 15)
**Attack target:** Continue I5 mechanism search with correct basis awareness (post-iter-12 revision).
**Status:** **PRIMARY ROTATION IDENTIFIED as R_{ν_1}(−θ_13)** (clean); residual still open.
**Runner:** `scripts/frontier_koide_pmns_mass_basis_factorization.py` (12/12 PASS)

---

## One-line finding

The mass-basis rotation R_right = V_TBM^T · V_conj factors as
**R_right = R_{ν_1}(α) · R_transverse(β, ψ)** where the primary rotation
**α = −0.1446 rad ≈ −δ·Q = −θ_13** (2.5% gap — clean identification),
with a residual ~4.9° correction having no clean (Q, δ) form.

## Factorization result

```
R_right (mass basis, angle 0.168 rad) decomposes as:

  R_right = R_{ν_1}(α) · R_{(0, cos ψ, sin ψ)}(β)

  α = -0.14455 rad = -8.282°   ≈ -δ·Q = -θ_13   (2.5% gap)
  β =  0.08604 rad =  4.930°   ≈ π/36  (1.4%)  (coincidence?)
  ψ =  0.42590 rad = 24.402°   ≈ π/8 (7.8%) or arctan(1/2) (8.9%)
```

Residual after factoring out R_{ν_1}(−δQ) exactly:
- angle = 0.0861 rad (= 4.93°)
- axis = (0.042, 0.909, 0.414) — primarily **ν_2** (91%), with **41% ν_3**

The residual is NOT a pure ν_2 rotation — it has substantial ν_3
contamination.

## What this contributes

**Clean identification of primary component**:
- The dominant mass-basis rotation IS the iter 4 θ_13 = δ·Q, expressed
  as a TM1 rotation (preserving ν_1 up to a 5° secondary rotation).
- This gives a cleaner structural reading than iter 11's (withdrawn)
  "near-TM1" claim or iter 12's bare 86% nu_1 overlap.

**Non-clean residual**:
- The 5° residual rotation has no match to (Q, δ) expressions within 10%.
- Closest coincidences: β ≈ π/36 (1.4%), ψ ≈ π/8 (7.8%) — but
  these don't obviously connect to retained axioms.
- This is the remaining open part of I5 mechanism derivation.

## Comparison to prior iterations

| Iter | Mechanism claim | Status |
|---|---|---|
| 5 | Single flavor-rotation | Ruled out (dist 0.11) |
| 8 | Z_2 CP-orientation identified | Valid |
| 11 | "Near-TM1" 97% (WITHDRAWN) | Basis error |
| 12 | True nu_1 overlap = 86% | Correct |
| **15** | **R_{ν_1}(−θ_13) · R_transverse(β, ψ)** | **Factored, 1 clean + 2 open** |

## Structural interpretation

In the standard PMNS parametrization V = R_23(θ_23) · R_13(θ_13) · R_12(θ_12),
the R_13 rotation is by θ_13 in the (e, τ) flavor plane, which in
mass basis corresponds to a rotation involving ν_1 and ν_3.

The finding α = −θ_13 in mass basis around ν_1 (= rotation in (ν_2, ν_3)
plane) is NOT the direct mass-basis dual of the flavor R_13. But it's
the "effective" TM1 rotation component that aligns with the known
θ_13 ~ δ·Q identification from iter 4.

The residual (β, ψ) rotation likely encodes the mixing between the
(ν_2, ν_3) rotation and the residual θ_23 deviation from π/4. Its
exact analytic form requires further work.

## Status update

| Gap | Pre-iter-15 | Post-iter-15 |
|---|---|---|
| I1, I2/P | RETAINED-FORCED | (unchanged) |
| I5 angles | observationally robust | (unchanged) |
| **I5 mechanism primary** | open (iter 12 revert) | **α = -θ_13 identified** |
| **I5 mechanism residual** | open | open (5° rotation, unclean β, ψ) |

Net progress: one out of three deformation components identified
cleanly. Two remain.

## Iter 16+ targets

1. **Derive residual β, ψ from retained Cl(3) structure**: the residual
   rotation is primarily in (ν_2, ν_3) plane, consistent with a
   "μ-τ breaking" interpretation. Can its exact coefficients be forced?

2. **Chirality-forced CP orientation** (Attack B1 follow-up): still open.

3. **Quark-sector parallel**: Cabibbo ≈ 2/9 rad with 2.4% gap — investigate.

4. **Or: publication draft** if user wishes to close with current state.
