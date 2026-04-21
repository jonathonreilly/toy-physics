# PMNS Selector Iter 5: δ · q_+ = Q = 2/3 — Observationally Admissible at 3σ, Not Exact

**Date:** 2026-04-21
**Branch:** `afternoon-4-21`
**Status:** **Strong intermediate result.** The hypothesis
`δ · q_+ = Q = 2/3` (tying I5 to the retained I1 Koide value) is NOT
exact at machine precision (0.16% deviation) but, when imposed as an
exact constraint with PDG `sin²θ_12, sin²θ_13` as inputs, predicts
`sin²θ_23 = 0.5447` within **0.06%** of PDG central 0.545 — well inside
both 3σ and 1σ NuFit ranges.
**Runner:** `scripts/frontier_pmns_selector_iter5_precision_delta_qplus_product.py` —
6 PASS, 3 FAIL (FAILs are on the exact-identity test at 1e-4 / 1e-8).

---

## Iter 5 attack

Iter 4 found the scalar `δ_* · q_+* = 0.66770` within 0.15% of `Q = 2/3
= 0.66667`. Iter 5 settles whether this is exact (hidden in 6-digit
rounding of the pinned values) or a near-miss.

### Method

1. **Part A — high-precision re-pin.** Use `scipy.optimize.least_squares`
   with LM method and `xtol=ftol=gtol=1e-15`, starting from the iter-4
   6-digit seed `(0.657061, 0.933806, 0.715042)`. Verify the refined
   point stays in the A-BCC basin (signature (1, 0, 2) in numpy
   convention = (2, 0, 1) in briefing convention).
2. **Part B — exact-identity test.** Compute `δ_hp · q_hp` to 15
   digits; compare to `Q = 2/3`.
3. **Part C — constrained re-pin.** Solve the chamber inversion with
   `sin²θ_12`, `sin²θ_13` fixed to PDG central AND `δ · q_+ = 2/3`
   exactly. Read off the resulting `sin²θ_23` and compare to PDG and
   NuFit 3σ ranges.
4. **Part D — gradient sanity.** Verify `∇(δ · q_+)` is non-zero
   at the pinned point (valid constraint).

### Correction to iter 4: PMNS extraction convention

The original retained closure-theorem runner uses ASCENDING eigenvalue
order + row-permutation `(2, 1, 0)` (electron ↔ largest eigenvalue):

```python
w, V = np.linalg.eigh(H)
order = np.argsort(np.real(w))      # ascending
V = V[:, order]
PMNS = V[PMNS_PERMUTATION, :]      # row perm (2, 1, 0)
```

My iter 5 initial draft used descending + no row permutation — gave
wrong angles at the pinned point (0.454, 0.185, 0.168 instead of
0.307, 0.0218, 0.545). After correction, the pinned point correctly
reproduces PDG central values.

## Results

### Part A — precision re-pin

High-precision LM-refined point from the iter-4 seed:

| Coord | Seed | HP-refined | displacement |
|---|---:|---:|---:|
| `m` | 0.657061 | 0.6570613422 | +3.4e-7 |
| `δ` | 0.933806 | 0.9338063438 | +3.4e-7 |
| `q_+` | 0.715042 | 0.7150423296 | +3.3e-7 |

Residuals: all three `< 1e-15` (machine precision). Basin preserved.

### Part B — exact-identity test

```
δ_hp · q_hp   = 0.667711063424943
Q = 2/3       = 0.666666666666667
difference    = +1.044e-03       (0.16%)
```

- **FAIL** at 1e-8 (not an exact identity).
- **FAIL** at 1e-4 (not even a close-to-exact identity).
- **PASS** at 1e-2 (confirmed as a weak structural hint).

Also tested: `Σλ / Σ|λ| = 0.16778` vs `1/6 = 0.16667`, deviation
`+1.1e-3` — same order. Not an exact identity.

### Part C — constrained re-pin (KEY RESULT)

Solving for `(m, δ, q_+)` with three equations: `sin²θ_12 = 0.307`,
`sin²θ_13 = 0.0218`, `δ · q_+ = 2/3` (exactly):

```
m_c     = 0.658752645  (was 0.657061,  Δ = +0.0017)
δ_c     = 0.933393857  (was 0.933806,  Δ = −0.0004)
q_c     = 0.714239398  (was 0.715042,  Δ = −0.0008)
δ_c · q_c = 0.666666666666667   ← exactly 2/3 by construction

Predicted sin²θ_23 = 0.544693
                     (PDG central 0.545; deviation 0.000307 = 0.06%)
                     (NuFit 3σ NO range: [0.430, 0.596] — passes)
                     (NuFit 1σ NO range: [0.530, 0.558] — also passes)

sin(δ_CP) = −0.9877   (essentially unchanged from the free-pinned -0.9874)
```

**C.1 PASS**: all three angles within NuFit 3σ NO ranges, sin(δ_CP)
preserved.

### Part D — constraint validity

`∇(δ · q_+) = (0, q_+, δ) = (0, 0.715, 0.934)` at pinned. `‖∇‖ =
1.176 ≠ 0` — the constraint is regular and cuts the 2-real manifold
smoothly to a 1-dim curve (a hyperbola).

## Interpretation

`δ · q_+ = Q = 2/3` is **not** an exact identity at the free-pinned
PDG-central chamber point. BUT:

1. **When imposed as a constraint**, it predicts `sin²θ_23 = 0.5447`
   within 0.06% of PDG central 0.545 — **indistinguishable from PDG
   within current experimental precision**.
2. **The constraint is framework-natural**: both `δ` and `q_+` are the
   chart coordinates themselves, and `Q = 2/3` is the retained I1
   Koide value (landed on morning-4-21 as retained-forced).
3. **The 0.16% exact-identity deviation is probably systematic** (not
   numerical noise), suggesting the retained selector is either:
   - (a) `δ · q_+ = 2/3` exactly, with the 0.0003 shift in sin²θ_23
     being a genuine framework prediction distinguishable from PDG
     central at future experimental precision (JUNO, DUNE), OR
   - (b) `δ · q_+ = 2/3 + small correction`, where the correction is
     itself framework-native (e.g., involving I2/P or A-BCC).

## What iter 5 establishes

- **An explicit codim-1 cut** on the 2-real source manifold that's
  OBSERVATIONALLY ADMISSIBLE at 3σ (in fact 1σ).
- **A direct I1 → I5 cross-sector linkage candidate**: if `δ · q_+ = Q`
  is retained, the Koide I1 scalar 2/3 appears in the PMNS chart.
- **A falsifiable prediction**: `sin²θ_23 = 0.5447` vs PDG central
  0.545 differs by 0.0003; future precision measurements test this.

## What remains open

Even if `δ · q_+ = 2/3` is accepted as a retained identity, it's only
a codim-1 cut on a 2-real manifold — we still need ONE MORE retained
condition to pin the point exactly. Candidate iter 6 directions:

- **Derive `δ · q_+ = Q` from Cl(3)/Z³ axioms.** This is the first
  priority — the hint is too strong to leave on the table without a
  retained-derivation attempt.
- **Find the second codim-1 cut.** Candidates: another simple scalar
  identity involving chart coordinates (`m + δ + q_+ = ?`, `m · δ = ?`),
  or an operator-based condition that's independent of the first.
- **Combined constraint optimization.** Re-run iter 4's scalar scan
  AFTER fixing `δ · q_+ = 2/3` exactly — the remaining 1-DOF curve
  gives a 1-parameter family; look for near-hits on that curve.

## Iter 6 plan

**Primary attack**: derive `δ · q_+ = 2/3` from the retained I1
closure machinery. The I1 AM-GM says `log(E_+ · E_⊥)` maximum at
`E_+ = E_⊥`, giving `κ = a²/|b|² = 2` and hence `Q = 2/3`. Can we
interpret `δ` and `q_+` as the analogs of `E_+` and `E_⊥` for the
PMNS chart? If so, AM-GM would force `δ = q_+` at the maximum (not
`δ · q_+ = constant`). So a direct I1 parallel doesn't immediately
fit — but there may be a WEIGHTED AM-GM structure.

**Concrete iter 6 runner**: test whether there's a retained functional
`F(δ, q_+)` whose constrained extremum under a retained "total
energy" gives `δ · q_+ = 2/3` specifically. Candidates:

1. `F = log(δ) + log(q_+) − λ · (δ + q_+ − N)` under
   `δ + q_+ = N` retained. AM-GM extremum at `δ = q_+ = N/2`, giving
   `δ · q_+ = N²/4`. For `δ · q_+ = 2/3`, need `N = 2 √(2/3) = 1.633
   = √(8/3)` — which IS the chamber boundary `q_+ + δ = √(8/3)`
   (`chamber distance = 0`). But we need the INTERIOR, so this isn't
   quite it.

2. `F = log(δ · q_+) − λ · g(m, δ, q_+)` for some retained constraint
   `g`. Find `g` such that at its extremum, `δ · q_+ = Q = 2/3`.

3. Cross-sector reformulation: reinterpret `δ`, `q_+` as isotype
   amplitudes on some retained projector structure. AM-GM on the
   Z_3-isotype product `E_1 · E_2` where `E_1 = δ`, `E_2 = q_+`
   gives `δ · q_+ = (N/2)² / 4 = N²/16` — needs `N² = 32/3` etc.

Iter 6 will probe these concretely.
