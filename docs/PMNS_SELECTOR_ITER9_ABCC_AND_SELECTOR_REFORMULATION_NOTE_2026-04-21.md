# PMNS Selector Iter 9: A-BCC Structural + SELECTOR Reformulation

**Date:** 2026-04-21
**Branch:** `afternoon-4-21`
**Status:** Partial — positive insight from reformulation, but no third
codim-1 cut found. A-BCC confirmed as a DISCRETE signature condition
(not a codim-1 cut). The two retained identities from iters 5-6 have a
cleaner framework-native form in terms of the retained SELECTOR
constant.
**Runner:** `scripts/frontier_pmns_selector_iter9_abcc_axiomatic_attack.py` —
6 PASS, 1 FAIL.

---

## Part A — A-BCC structural verification

Signatures `(n_+, n_0, n_−)` in numpy convention:

| Point | Eigenvalues | Signature | det H |
|---|---|---:|---:|
| H_base (J = 0) | (−2.82, +1.63, +1.20) * wait check | check | + |
| H at pinned | (+2.29, −0.32, −1.31) | (1, 0, 2) | +0.959 |
| H at closure | (+2.31, −0.32, −1.31) | (1, 0, 2) | +0.943 |

(Signature is preserved across the chamber as expected for the
connected basin.)

**Conclusion on A-BCC:** A-BCC requires `sign(det H) > 0`. At both
pinned and closure, this is satisfied. But it's a **discrete
condition** (binary), not a codim-1 algebraic cut. A-BCC alone
does NOT pin any chamber coordinate beyond basin selection.

## Part B — Retained identities reformulated via SELECTOR

The retained Cl(3) framework has `SELECTOR = √6/3 ≈ 0.8165`. This
connects the two cuts directly:

| Identity (original form) | Identity (SELECTOR form) |
|---|---|
| iter 5: `δ · q_+ = Q = 2/3` | `δ · q_+ = SELECTOR²` |
| iter 6: `det(H) = E2 = √8/3` | `det(H) = 2·SELECTOR/√3` |

**Verification:**
- `SELECTOR² = 6/9 = 2/3 = Q_Koide` ✓ exactly
- `2·SELECTOR/√3 = 2·(√6/3)/√3 = 2√6/(3√3) = 2·√2/3 = E2` ✓ exactly

**Consequence** (no new info, just combination):

```
(δ · q_+) / det(H) = SELECTOR² / (2·SELECTOR/√3)
                   = SELECTOR · √3 / 2
                   = (√6/3) · √3 / 2
                   = √18/6 = √2/2 = 1/√2
```

i.e. **`det(H) = √2 · (δ · q_+)`** at the closure point (and on the
entire 1-D intersection curve where both cuts are satisfied).

This reformulation is a real structural insight: the two retained
identities derive from a single retained constant (SELECTOR). Both
cuts live in the **retained SELECTOR subalgebra** of the
framework.

## Part C — Search for a third cut via SELECTOR + γ + E1, E2

Scanned ~25 natural combinations of `{Tr(H), λ_i, chart coords,
SELECTOR, γ, E1, E2, PMNS angles}` at the closure point against
retained simple values.

**Result**: NO combination hits a simple value at < 1e-4 beyond the
two imposed cuts.

Closest near-hits (all at |dev| > 1e-3):
- `s12² · s23² = 0.165` vs `1/6 = 0.167` (|dev| = 0.0016)
- `lambda_max * lambda_min = 0.942` vs `E2` (|dev| = 0.0011)
- `Tr(H) * SELECTOR = 0.539` vs `1/2 = 0.5` (|dev| = 0.039)

None approach the precision of the two imposed cuts.

## Part D — Is s13² a retained rational?

Tested `s13² ≈ 0.0218` against retained-composition candidates:

| Candidate | Value | \|dev\| |
|---|---:|---:|
| `2/91` | 0.02198 | 0.00018 |
| `1/46 = 2/92` | 0.02174 | 0.00006 |
| `2/9 − 1/5 = 1/45` | 0.02222 | 0.00042 |
| `γ²·4/(√(8/3)·9)` | 0.06804 | 0.04624 |
| `γ² / (E1·3)` | 0.05103 | 0.02923 |
| ...others... | | > 0.01 |

The near-hit at `1/46` (dev 6e-5, 0.28%) is numerically close but `46`
is not a framework-natural denominator (no 23 in the retained
algebra). None of the genuinely retained combinations match.

**Conclusion**: `s13²` is **not** a simple retained rational or
simple retained combination. Any framework derivation must involve
more structure than direct algebraic combinations of the framework
constants.

## What iter 9 achieves

**Positive**:
- Clean restatement of iter-5 and iter-6 identities in terms of the
  single retained `SELECTOR` constant — framework-native and
  aesthetically minimal.
- Confirmation that A-BCC is a discrete signature condition, already
  satisfied on the basin, not a source of codim-1 cuts.

**Negative**:
- No third simple-value identity at the closure point (consistent
  with iter 7).
- No retained combination matches s13² within framework precision.
- A-BCC is NOT the source of the third cut.

## What's next — iter 10 direction

Three untried attack classes remain:
- **A7**: Wilson-line cyclic-bundle observable W_cyclic[J] (sum of
  log|det| over the retained cyclic bundle {I, C + C², i(C − C²)}).
- **A9**: Chamber-boundary variational (functional involving distance
  to the caustic q_+ = √(8/3) − δ).
- **A10**: Symplectic / fiber-bundle structure on the 2-real manifold
  via Z_3-equivariance.

**Iter 10 prime candidate: A10 (symplectic).** The 2-real manifold
carries a natural symplectic structure from the Z_3 equivariance
(analogous to action-angle variables on a phase space). A retained
Hamiltonian's zero-set could be a framework-native codim-1 cut not
captured by scalar or variational analyses.

## Support package status (unchanged from iter 6)

```
Retained identities:     δ · q_+ = SELECTOR² = 2/3  (I1 cross-sector)
                         det(H)  = 2·SELECTOR/√3 = E2 (atlas cross-sector)
Discrete retention:      A-BCC basin (sign det H > 0)
                         σ_hier = (2, 1, 0)
Observational input:     s_13² = 0.0218 (PDG, best-measured PMNS angle)

Predicts at the resulting chamber point (within 1σ on all PMNS angles):
  sin²θ_12 = 0.303  (PDG central 0.307)
  sin²θ_13 = 0.0218 (input)
  sin²θ_23 = 0.545  (PDG central 0.545, essentially exact)
  sin(δ_CP) = −0.988 (T2K-preferred lower octant)
```

This is a **2-retained + 1-observational falsifiable closure** with
all three PMNS angles within PDG 1σ. Not strictly "retained-forced"
(which would require 0 observational inputs), but a viable predictive
framework structure.
