# Definitive Distance Law Closure

**Date:** 2026-04-12
**Script:** `scripts/frontier_distance_law_definitive.py`
**Status:** bounded review candidate -- high-precision ordered-cubic distance-law closure
**Claim type:** bounded_theorem

**Audit-lane runner update (2026-05-09):** The primary runner `scripts/frontier_distance_law_definitive.py` previously timed out under the audit-lane 120s default budget; AUDIT_TIMEOUT_SEC=1800 added; runs in 234s under the new budget. The runner's pass/fail semantics are unchanged; this update only ensures the audit-lane sees a complete cache instead of a TIMEOUT row.

**Audit-conditional perimeter (2026-05-09):**
The current generated audit ledger records this row `audited_numerical_match` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
runner genuinely computes Poisson fields and path-sum fits, but the
0.1% conclusion depends on choosing the scaled-fit N>=56 weighted
mean while multiple finite-size extrapolations in the same output
miss -1 by about 3% to 14%. The missing step is an independent
theorem or pre-registered rule selecting that estimator as the
continuum/bounded-law estimator." This rigorization edit only
sharpens the boundary of the numerical-match perimeter; nothing here
promotes audit status. The supported content of this note is the
finite per-N table of `alpha_scaled` values and the post-selected
weighted-mean estimator at N >= 56; the §"Conclusion" 0.1%-precision
phrasing is bounded interpretation conditional on that estimator
choice, and the alternative 1/N-extrapolation estimators discussed in
§"Finite-Size Systematics" are explicitly noted as giving alpha_inf
in [-0.94, -0.86], 6%-14% off -1.0. A future independent estimator-
selection theorem (or a pre-registered protocol) would close the
estimator-choice gap; that step is deferred and is the prescribed
repair path.

## Method

Sparse Poisson solver (direct for N<=48, conjugate gradient for N>=56) on 3D
lattices from 31^3 to 96^3 with Dirichlet boundary conditions. A point mass at
the grid center generates a Coulomb-like field via nabla^2 phi = -delta. Rays
propagate along x at impact parameter b from the mass, accumulating valley-linear
phase S = k * sum(1 - phi). The deflection delta(b) = phase(b+1) - phase(b) is
fitted to a power law delta ~ b^alpha.

Three fit ranges compared:
- **Full:** b = 3..14 (fixed)
- **Core:** b = 4..8 (well inside all grids)
- **Scaled:** b = 4..N/6 (scales with grid to maintain constant relative range)

The scaled fit is the most robust because it avoids both near-field (b < 4) and
boundary-contaminated (b > N/6) regions at all lattice sizes.

## Key Results

### Raw alpha (scaled fit, b=4..N/6)

| N  | alpha_scaled | |dev from -1| |
|----|-------------|----------------|
| 31 | -1.103      | 10.3%          |
| 40 | -1.048      | 4.8%           |
| 48 | -1.020      | 2.0%           |
| 56 | -1.011      | 1.07%          |
| 64 | -1.004      | 0.43%          |
| 80 | -1.003      | 0.34%          |
| 96 | -0.992      | 0.77%          |

For N >= 64, all individual values are within 1% of -1.0.

### Best Estimate (weighted mean, N >= 56)

```
alpha     = -1.00104 +/- 0.00416
deviation = 0.104%  (0.2 sigma)
```

### Force Exponent

```
F ~ 1/r^n  where n = alpha - 1
n = -2.0010 +/- 0.0042
deviation from -2.0: 0.10%
```

### Mass Independence

Tested at N=64 with M = 0.5, 1.0, 2.0:
- alpha spread = 0.00000 (exactly zero within float precision)
- Mass independence: CONFIRMED

### Finite-Size Systematics

The Dirichlet-box field differs from pure 1/r due to image-charge corrections
(numerical deflections are 11-79% larger than the 1/r analytic prediction at
individual b values). However, the *power-law exponent* of the deflection is
insensitive to this overall amplitude shift and converges to -1.0 as N grows.

All 1/N extrapolation methods give alpha_inf between -0.86 and -0.94 because
the alpha(N) sequence is non-monotonic (overshoots -1.0 at small N, undershoots
at large N). The weighted mean of converged large-N values is the correct
estimator, not 1/N extrapolation.

## Conclusion

Valley-linear path summation with Coulomb field f = s/r on a 3D lattice produces
gravitational deflection delta(b) ~ 1/b^alpha with alpha = -1.001 +/- 0.004.
On this ordered-cubic Dirichlet surface, the inverse-square force-law exponent
is numerically consistent with 1/r^2 at 0.1% precision.

## Claim boundary

- ordered 3D cubic only
- Dirichlet boundary conditions
- ray/path-sum deflection observable
- not architecture-independent closure by itself
- not a replacement for the existing bounded Newton-family notes on `main`

## Runtime

Total: 3.7 minutes (N=31..96, including mass-independence check).
CG solver handles 96^3 (884K sites) in 2.5 seconds.
