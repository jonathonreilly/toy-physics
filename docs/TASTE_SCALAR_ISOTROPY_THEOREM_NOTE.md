# Taste-Scalar Coleman-Weinberg Isotropy Theorem

**Date:** 2026-04-16
**Status:** exact support theorem with bounded downstream scalar-spectrum consequences
**Primary runner:** `scripts/frontier_taste_scalar_isotropy.py`

## Authority Role

This note records one exact theorem on the retained `Cl(3)/Z^3` taste block:
the one-loop fermion Coleman-Weinberg Hessian is isotropic at an axis-aligned
electroweak minimum.

That exact theorem is useful downstream for:

- Higgs / taste-scalar near-degeneracy arguments
- scalar degree-of-freedom counting on the taste block
- bounded electroweak-transition diagnostics
- redirecting `y_b` and `2 -> 1+1` splitting work away from scalar-CW-only
  explanations

The theorem itself is exact. The scalar-mass splitting and thermal-transition
consequences below are still bounded because they additionally use a one-loop
gauge-only split model and a scalar-only thermal-cubic estimate.

## Exact Theorem

Let

`H(phi) = sum_i phi_i S_i`

on `C^8 = (C^2)^{otimes 3}`, where `S_i` are the commuting taste-shift
involutions acting as `sigma_x` on tensor factor `i`. Let the fermion
Coleman-Weinberg potential be any smooth sum of the form

`V_f(phi) = sum_s f(lambda_s(phi)^2)`

where `lambda_s(phi)` are the eigenvalues of `H(phi)`. Then at any axis-aligned
electroweak minimum `phi = (v, 0, 0)` the Hessian is isotropic:

`d^2 V_f / d phi_i d phi_j = delta_ij * C(v)`.

Equivalently, the one-loop fermion Coleman-Weinberg contribution cannot split
the Higgs-direction curvature from the two orthogonal taste-direction
curvatures on this retained taste block.

## Proof Sketch

1. The shift operators satisfy
   `S_i^2 = I`, `S_i = S_i^dagger`, and `[S_i, S_j] = 0`.
2. In the simultaneous eigenbasis `|s_1, s_2, s_3>` with `s_i in {0,1}`,
   `S_i |s> = (-1)^{s_i} |s>`, so
   `lambda_s(phi) = sum_i phi_i (-1)^{s_i}`.
3. At `phi = (v,0,0)`, all eigenvalues satisfy `|lambda_s| = v`, so any smooth
   `f(lambda_s^2)` evaluates to the same common factor `f(v^2)`.
4. The Hessian therefore reduces to the binary orthogonality sum
   `sum_s (-1)^{s_i} (-1)^{s_j}`.
5. That sum is `8` for `i = j` and `0` for `i != j`, so the Hessian is
   proportional to `delta_ij`.

No fits or observed Higgs-sector imports enter the theorem itself.

## Exact Consequences

### 1. No fermion-CW Higgs/taste splitting

The fermion Coleman-Weinberg sector gives the same local quadratic curvature in
all three taste-block directions at the retained axis-aligned minimum. Any
Higgs/taste mass splitting must therefore come from outside the fermion-CW
piece.

### 2. Exact taste-block scalar count

On the retained taste block there is one Higgs direction and two orthogonal
taste directions. The theorem therefore supports a `1 + 2` physical real-scalar
count on that block before Goldstone accounting, not an unconstrained
eight-mode scalar multiplicity.

## Bounded Downstream Package

The following consequences use the exact theorem plus additional bounded
assumptions on the current package surface.

### B1. Gauge-only leading split

Using the retained Higgs/taste reading in which `W` and `Z` couple to the
electroweak direction `phi_1` but not to the orthogonal taste directions
`phi_2, phi_3`, the leading one-loop gauge Coleman-Weinberg contribution shifts
only the Higgs-direction curvature:

`m_H^2 = m_0^2 + CW_f(common) + delta_gauge`

`m_taste^2 = m_0^2 + CW_f(common)`

so

`m_taste^2 = m_H^2 - delta_gauge`.

This gauge-only split is a bounded support model, not an exact theorem.

### B2. Near-degenerate taste-scalar pair

Using the current live package values

- `v = 246.282818290129 GeV`
- `g_2(v) = 0.648031`
- `g' = sqrt(3/5) g_1(v) = 0.359704`
- canonical `m_H = 125.10 GeV`

the standard one-loop gauge contribution gives

- `delta_gauge = 47.13 GeV^2`
- `m_taste = 124.91 GeV`

for a near-degenerate pair of taste scalars about `0.19 GeV` below the Higgs.

This is a bounded companion prediction, not a promoted primary quantitative
lane.

### B3. Scalar-only thermal-cubic estimate

If one uses the exact `1 + 2` scalar count together with the same gauge-only
split in the textbook finite-temperature cubic estimate, the current package
gives

- `v_c / T_c = 0.3079`

on that scalar-only estimate. This bounded readout disfavors an
electroweak-transition baryogenesis route on the same restricted surface.

This is not a full nonperturbative finite-temperature electroweak closure.

### B4. Redirected downstream work

Because the fermion-CW block is isotropic:

- `y_b` cannot be explained by scalar-CW splitting alone on this surface
- the `2 -> 1+1` taste/generation split cannot be attributed to scalar-CW
  anisotropy alone on this surface

Those lanes must look instead to gauge/Dirac/Jordan-Wigner or other retained
taste-breaking structure.

## What This Note Does Not Claim

- a theorem-grade derivation of the full Higgs/taste spectrum beyond the exact
  fermion-CW isotropy statement
- a theorem-grade derivation that gauge corrections vanish identically in the
  orthogonal taste directions
- a nonperturbative finite-temperature electroweak-transition closure
- an observed experimental identification of the near-degenerate taste-scalar
  pair
- a theorem-grade derivation of `y_b` or the `2 -> 1+1` split

## Atlas / Reuse Value

This note contributes one reusable proof mechanism to the atlas:

- exact taste-block Coleman-Weinberg isotropy on the retained `Cl(3)/Z^3`
  surface

That tool can be reused anywhere the package needs to know whether a proposed
scalar/taste splitting can arise from the fermion Coleman-Weinberg block alone.

## Validation

Primary rerun:

- `scripts/frontier_taste_scalar_isotropy.py`
  current summary: `THEOREM PASS=30`, `BOUNDED PASS=6`, `FAIL=0`
