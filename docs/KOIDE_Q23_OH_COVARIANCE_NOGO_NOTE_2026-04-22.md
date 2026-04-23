# Koide Q = 2/3 Sub-Route (a) No-Go: Retained Chart is Not O_h-Covariant

**Date:** 2026-04-22
**Status:** **NO-GO** on sub-route (a) of the spin-1 structural attack. Sharpens the remaining structural question.
**Primary runner:** `scripts/frontier_koide_q23_oh_covariance_nogo.py` (7/7 PASS)

---

## 0. Result

The retained affine Hermitian chart

```
H(m, δ, q_+) = H_base + m T_m + δ T_δ + q_+ T_q
```

is **NOT covariant** under the 48-element cubic point group `O_h ⊂ SO(3) × Z_2`. The joint covariance group (elements `g ∈ O_h` such that the chart's span is `g`-invariant) is only **`{+I, -I} = Z_2` = spatial parity**.

This falsifies sub-route (a) of the spin-1 structural claim (`koide-q23-spin1-structural-route`):

> "The retained chart inherits SO(3) isotropy from O_h ⊂ SO(3) × Z_2 cubic lattice symmetry."

Does not hold. The chart carries at most parity `Z_2` from the O_h side. Any SO(3) or spin-1 extension must come through a DIFFERENT structural mechanism.

## 1. Precise statement

**Theorem (O_h covariance no-go)**. Let `O_h` = signed permutations of `Z³` (48 elements). For `g ∈ O_h`, define the action `H ↦ g H g^T`. The covariance group of the retained chart is

```
CovG  :=  { g ∈ O_h : for every (m, δ, q_+) there exists (m', δ', q_+') 
                      with g·H(m,δ,q_+)·g^T = H(m',δ',q_+') }
```

Equivalently, `CovG` = subgroup of `g ∈ O_h` such that `g·B·g^T` lies in the real span of `{H_base, T_m, T_δ, T_q, I}` for each basis matrix `B`.

**Result**: `CovG = {+I, -I}`, explicitly:
- `g = +I = diag(+1,+1,+1)` (trivially; identity).
- `g = -I = diag(-1,-1,-1)` (spatial parity; since `(-I) M (-I)^T = M` for any `M`).

Out of 48 O_h elements, only these 2 preserve the chart's span. The remaining 46 map the chart out of its span.

## 2. Individual stabilizers (pointwise `g M g^T = M`)

| Matrix | `|Stab(M)|` |
|--------|-------------|
| `H_base` | 2 |
| `T_m` | 8 |
| `T_δ` | 2 |
| `T_q` | 12 |
| **Joint pointwise** | **2** |

`T_q` is circulant (symmetric with cyclic structure), so its stabilizer in O_h is larger (S_3 × Z_2 = 12 elements). `T_m` is a specific transposition matrix with 8-element stabilizer. But the JOINT pointwise stabilizer (elements preserving all four simultaneously) is only 2 = `{+I, -I}`.

This is significantly stronger than CovG analysis: it says even under relabeling of `(m, δ, q_+)`, the chart cannot exploit more than Z_2 from O_h.

## 3. Structural interpretation

### What this rules out (sub-route (a))

The previous note (`koide-q23-spin1-structural-route`) proposed three paths to close Q = 2/3 via spin-1:

- **(a) Lattice O_h cubic-point-group invariance of H_base** — NOW RULED OUT.
- (b) Body-diagonal Z_3 fixed-point ⇒ SO(3) isotropy extension.
- (c) SU(2)_L × generation forcing spin-1 on 3-gen factor.

(a) claimed that the retained H_base chart inherits O_h cubic symmetry from the Z³ lattice, and this propagates to SO(3) spin-1 by restriction. This note shows that's WRONG: the chart doesn't carry O_h symmetry at all — only parity Z_2.

The H_base entries `E1 = √(8/3)` and `E2 = √(8)/3` and `γ = 1/2` are NOT O_h-invariant coefficients. They're specific non-symmetric numbers that break the naive cubic symmetry.

### What remains (sub-routes (b) and (c))

**(b) Body-diagonal isotropy**: the Z_3 body-diagonal fixed locus has natural isotropy under SO(2) rotations around the body-diagonal axis. If the retained charged-lepton triplet lives at such a fixed point and the isotropy extends to SO(3) via some mechanism (e.g., zero-mode spectral-averaging), spin-1 could emerge.

**(c) SU(2)_L × generation**: the SM has SU(2)_L doublet × 3 generations = 6-dim LH fermion space. Projection onto the "generation" factor (mass-eigenstate space) could inherit spin-1 from the natural angular-momentum structure of the SM.

Neither (b) nor (c) is falsified by this no-go. They remain open as candidate closure routes.

## 4. Implication for the broader attack

The Q = 2/3 spin-1 structural attack is NOT dead. It is **sharpened**:

> **Q = 2/3 cannot close through O_h cubic invariance of the retained H_base chart. It must close through a mechanism that endows the 3-generation triplet with SO(3) spin-1 representation WITHOUT requiring O_h invariance of H_base.**

This is a substantive reformulation: the attack must go through a symmetry-breaking mechanism that nevertheless produces spin-1 structure at a different level of the theory (e.g., zero-mode action, effective potential, or SU(2)_L doublet embedding).

## 5. Why this is real progress

This is a NEGATIVE RESULT that:
- Eliminates one candidate derivation path definitively (sub-route (a)).
- Sharpens the remaining open question.
- Saves future work from exploring a dead end.

**Negative results of this kind are essential for the framework's scientific rigor**: the retained stack now has an EXPLICIT audit that sub-route (a) fails, computed over all 48 O_h elements with sympy-exact verification.

## 6. Relationship to the earlier six no-gos

This note adds a **seventh no-go** on the Q = 2/3 stack, distinct from the previous six:

| # | No-go | Target |
|---|-------|--------|
| 1 | Z_3-invariance alone | generic symmetry |
| 2 | Sectoral universality | species-independence |
| 3 | Color-sector correction | QCD structure |
| 4 | Anomaly-forced cross-species | anomaly mechanism |
| 5 | SU(2) gauge exchange mixing | electroweak structure |
| 6 | Observable-principle character symmetry | group-character methods |
| **7** | **O_h covariance of H_base chart (THIS NOTE)** | **cubic lattice invariance of chart** |

Sub-routes (b) and (c) of the spin-1 attack remain as the only untested structural paths.

## 7. Cross-references

- `docs/KOIDE_Q23_SPIN1_STRUCTURAL_ROUTE_NOTE_2026-04-22.md` — spin-1 route with three sub-routes.
- `docs/KOIDE_Q23_ANOMALY_STRUCTURAL_ATTACK_NOTE_2026-04-22.md` — parallel anomaly-identity attack (loop 12).
- `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` — six existing no-gos.
- `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md` — retained chart provenance.
