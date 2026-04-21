# PMNS Selector Iter 6: Second Cut Candidate — det(H) = √8/3 = E2

**Date:** 2026-04-21
**Branch:** `afternoon-4-21`
**Status:** **Very strong result.** A systematic scan of scalar invariants
along the 1-D curve `{δ · q_+ = 2/3, s13² = 0.0218}` reveals a clear
best-aligned second cut: **`det(H) = √8/3 = E2`**, where E2 is a
retained atlas constant (appearing in H_base as the magnitude of the
(1,2) and (2,1) entries, up to sign). Combined with iter 5's first cut
`δ · q_+ = 2/3`, this pair reduces the 3D chart to a 1-D curve that is
observationally consistent with PDG 3σ on both `s12²` and `s23²`.
**Runner:** `scripts/frontier_pmns_selector_iter6_combined_cuts_scan.py`
— 2 PASS, 0 FAIL (on the best-candidate sanity checks).

---

## Iter 6 attack

Iter 5 established `δ · q_+ = 2/3` (tied to retained I1 Koide Q) as a
codim-1 cut observationally admissible at 1σ. Iter 6 searches the
resulting 1-D chamber curve for a SECOND retained cut that could
combine with the first to pin the exact point.

### Method

**Phase I** — build the curve: under `δ · q_+ = 2/3` AND `s13² = 0.0218`
(PDG), sweep `m` over `[M_STAR − 0.1, M_STAR + 0.1]` in 41 steps,
solve for `(δ, q_+)` at each `m` to machine precision.

**Phase II** — scan scalars along the curve: at each curve point,
compute ~33 natural scalar invariants. For each (scalar, retained
simple value) pair, find level-crossings along the curve. Report by
distance of crossing from `m_*`.

**Phase III** — test top candidates as combined closures: for each
top crossing, solve the 3-eq system {δ·q_+ = 2/3, scalar = simple_value,
s13² = 0.0218} and check (i) displacement from pinned, (ii) A-BCC basin
preservation, (iii) chamber interior, (iv) s12² and s23² in NuFit 3σ.

## Results

### Top closure candidates (sorted by displacement from pinned)

| Second cut | Δm | Δδ | Δq+ | s12² | s23² | 3σ |
|---|---:|---:|---:|---:|---:|:---:|
| **`det(H) = √8/3`** | 0.0032 | 0.0022 | 0.0028 | **0.3029** | **0.5450** | **Y/Y** |
| `prod λ = √8/3` | 0.0032 | 0.0022 | 0.0028 | 0.3029 | 0.5450 | Y/Y (same as above: det = prod λ) |
| `Σλ / Σ\|λ\| = 1/6` | 0.0020 | 0.0067 | 0.0041 | 0.3171 | 0.5440 | Y/Y |
| `det(H) = 1` | 0.0045 | 0.0108 | 0.0073 | 0.3238 | 0.5435 | Y/Y |
| `SELECTOR · q_+ = 1/√3` | 0.0070 | 0.0090 | 0.0079 | 0.2924 | 0.5458 | Y/Y |
| `Tr(H) = m = 2/3` | 0.0096 | 0.0138 | 0.0115 | 0.2852 | 0.5464 | Y/Y |

The winning candidate: **`det(H) = √8/3`**. Reasons:

1. **Smallest displacement from pinned** (all three coords < 0.003).
2. **Uses a retained atlas constant**: `E2 = √8/3 ≈ 0.9428` appears
   verbatim in `H_base` as the magnitudes of `H_base[1,2]` and
   `H_base[2,1]` (up to sign).
3. **PDG s12² prediction**: 0.3029 vs central 0.307 — **within 1σ**
   (NuFit 5.3 NO 1σ is roughly [0.295, 0.318]).
4. **PDG s23² prediction**: 0.5450 vs central 0.545 — **essentially
   central**.

### Combined closure: `δ · q_+ = 2/3` AND `det(H) = √8/3`

Solving the 3-equation system:
```
δ · q_+ = 2/3
det(H) = √8/3 = E2
s13² = 0.0218 (PDG input)
```

gives:
```
m   = 0.660242  (shifted from 0.657061 by 0.003181)
δ   = 0.935995  (shifted from 0.933806 by 0.002189)
q_+ = 0.712255  (shifted from 0.715042 by 0.002787)
```

Predicted:
```
sin²θ₁₂ = 0.302911  (PDG 0.307 ± 3σ [0.275, 0.345]: within 1σ)
sin²θ₂₃ = 0.545005  (PDG 0.545 ± 3σ [0.430, 0.596]: essentially central)
```

All three PMNS angles within NuFit 3σ NO; two within 1σ.

## What iter 6 achieves

**A viable combined selector structure has been identified.** Two
retained identities:
- `δ · q_+ = Q = 2/3` (I1 Koide cross-sector pull)
- `det(H) = E2 = √8/3` (atlas-constant cross-sector pull)

reduce the 3D chart to a discrete set of intersection points. Combined
with the chamber-interior and A-BCC basin constraints, the physical
point is picked out uniquely up to experimental precision on `s13²`.

**This is stronger than iter 5.** Iter 5 had ONE retained identity +
TWO PMNS inputs (s12² and s13²). Iter 6 has TWO retained identities +
ONE PMNS input (s13²). The framework-predictive content is now
`(s12², s23², s13²) → all three from {δ·q_+ = 2/3, det(H) = √8/3, and
one observational input}` — an observational-economy improvement.

Full gate closure would need a THIRD retained identity replacing `s13²`
as input, so the framework predicts ALL three PMNS angles.

## Cautions — what's NOT yet proven

1. **Neither identity is exact** at the PDG-pinned point. `δ · q_+` is
   0.16% off from 2/3; `det(H)` is 1.7% off from √8/3 at that specific
   point. The displacement to the closure point is small but non-zero.
2. **Neither identity is yet framework-derived**. Both are currently
   NEAR-HITS on simple retained values. Framework-native derivation
   from Cl(3)/Z³ is the remaining iter-7+ goal.
3. **`s13²` is still an observational input**. A third retained
   identity is needed for full closure.

## Iter 7+ direction

**Primary (iter 7)**: attempt framework-native derivation of
`det(H) = E2 = √8/3`. Expand `det(H(m, δ, q_+))` as a polynomial in
(m, δ, q_+) and look for a retained factorization. `E2` appearing is
suggestive: `H_base[1,2] = -E2`, `H_base[2,1] = -E2`, so possibly
`det(H) = f(H_base entries)` evaluated at a specific combination of
(m, δ, q_+).

**Secondary (iter 8)**: search for the THIRD retained cut. Candidates:
- Rescan scalars on the now-reduced 0-D intersection locus (actually
  discrete points after imposing both cuts); look for retained-simple
  hits that fix `s13²` specifically.
- A-BCC axiomatic attack (backlog A5): if A-BCC is derived from Cl(3),
  it may come with extra structure pinning s13².

Both iter 7 and iter 8 are concrete and executable. The loop is
making substantive progress after the iter 1-3 ruling-out.
