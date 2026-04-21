# Koide Loop Iteration 21 — Q = 3·δ Retained Identity & Sum Rule Conservation

**Date:** 2026-04-21 (iter 21)
**Attack target:** Explain Sum Rule 2 via retained arithmetic identity.
**Status:** **Q = 3·δ retained identity + SR2 conservation law** (theorem-grade)
**Runner:** `scripts/frontier_koide_Q_eq_3delta_identity.py` (16/16 PASS)

---

## Headline

Iter 1 and iter 2 closures jointly imply a clean arithmetic identity:

```
Q = p · δ   (with p = 3 the Z_3 orbifold order)

i.e.,  2/3 = 3 · (2/9)  ✓
```

This elevates Sum Rule 2 from "numerical coincidence" to **conservation
law** under iter 4 deformation, anchored at TBM limit by Q = 3·δ.

## The identity

Iter 1 (APS η closure): **δ = 2/p²** (for p = 3 Z_p orbifold).
Iter 2 (AM-GM closure): **Q = 2/d** (for d = 3 generations).
Z_3 structure: **p = d = 3** (generations emerge from Z_3 isotypes).

Ratio:
```
Q / δ  =  (2/d) / (2/p²)  =  p²/d  =  p   (when p = d)
```

So **Q = p · δ = 3·δ**. Exact retained arithmetic.

## Implications for Sum Rule 2

### At TBM limit

With TBM: sin²(θ_12) = 1/3, sin²(θ_13) = 0:
```
SR2 LHS = Q · (1/3) + 0 = Q/3 = δ
```
Trivially satisfied by Q = 3·δ.

### Under iter 4 deformation (conservation law)

Deformation:
- Δ sin²(θ_12) = −δ²·Q  (decrease)
- Δ sin²(θ_13) = (δQ)²  = δ²·Q²  (increase, leading order)

Change in Sum Rule 2 LHS:
```
Δ SR2 = Q · Δsin²(θ_12) + Δsin²(θ_13)
      = Q · (−δ²·Q) + δ²·Q²
      = −δ²·Q² + δ²·Q²
      = 0
```

**Sum Rule 2 LHS is CONSERVED** under iter 4 deformation at leading
order. The correction is O((δQ)⁴).

## Structural interpretation

The iter 4 deformation (from TBM to NuFit-fitting values) is a
**1-parameter trajectory** in angle space along which Sum Rule 2 is
invariant:

```
{(sin²θ_12, sin²θ_13, θ_23) | Q · sin²θ_12 + sin²θ_13 = δ}
```

This is a 2-parameter surface (modulo θ_23 independence). Adding Sum
Rule 1 (θ_13 = 2(θ_23 − π/4)) reduces to 1-parameter. That 1 parameter
is θ_13 itself, with all other angles tied to it via SR1 and SR2.

So iter 4's three formulas reduce to **1 free parameter** (θ_13 = δQ)
plus two structural constraints (SR1, SR2).

## Why this matters

Before iter 21: iter 4 was 3 numerical formulas with 2 retained
parameters. Post iter 13: all NuFit data within 1σ. Post iter 18: two
elegant sum rules. Post iter 21: **SR2 is a conservation law anchored
at Q = 3·δ**, turning iter 4 from "numerical fit" into a
"structural identity + 1-parameter deformation".

The NuFit-fit quality is no longer surprising:
- TBM limit is forced by S_3 (iter 3).
- Q = 3·δ is forced by retained iter 1/2 closures.
- Sum Rule 2 is automatic at TBM (from Q = 3·δ).
- iter 4 deformation preserves SR2 (conservation law).
- All three NuFit angles tied to a single θ_13 via SR1, SR2.

The only genuinely free parameter is "how much θ_13 gets activated".
At iter 4's value θ_13 = δQ = 4/27, this is tied to the retained
(Q, δ) values. Deriving why **θ_13 = δ·Q exactly** (not something else)
remains iter 22+ target.

## Status update

| Gap | Pre-iter-21 | Post-iter-21 |
|---|---|---|
| I1, I2/P | RETAINED-FORCED | (unchanged) |
| **Q = 3·δ identity** | (implicit) | **EXPLICIT retained-forced** |
| Sum Rule 2 status | pattern fit | **CONSERVATION LAW** |
| iter 4 parameter count | 3 coefficients | **1 free parameter (θ_13)** |
| θ_13 = δ·Q derivation | open | still open (iter 22+) |

## Iter 22+ targets

The remaining open question for I5 mechanism is now:
**Why is θ_13 activated to the specific value δ·Q?**

Since SR1 and SR2 reduce iter 4 to 1 free parameter, and SR2 is a
conservation law anchored at Q = 3·δ (retained), the derivation of
θ_13 = δ·Q is the single remaining piece.

Candidates:
- Cl(3) bivector rotation by angle δ·√Q (iter 16's leading-order angle).
- Charged-lepton Yukawa structure with specific (Q, δ)-dependent mixing.
- Retained CP orientation (iter 8) forcing a specific θ_13 activation.

## Synthesis: I5 structural progression

| Iter | I5 status |
|---|---|
| 3 | V_TBM forced (leading order) |
| 4 | 3 angles fit NuFit 1σ (conjecture) |
| 13 | 4/6 NuFit releases within 1σ (robust) |
| 17 | e-row axis direction forced by TBM |
| 18 | 2 elegant sum rules (SR1, SR2) |
| 19 | SR2 operator form <e|M_SR2|e> = δ |
| **21** | **Q = 3·δ retained identity; SR2 conservation law** |

Iter 21 represents the **cleanest structural understanding of I5 to
date**: iter 4 is 1 free parameter (θ_13) plus retained (Q = 3·δ)
anchoring.
