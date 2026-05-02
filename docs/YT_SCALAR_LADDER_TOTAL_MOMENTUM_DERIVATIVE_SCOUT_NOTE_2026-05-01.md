# Top-Yukawa Scalar Ladder Total-Momentum Derivative Scout

**Date:** 2026-05-01
**Status:** bounded-support / scalar ladder total-momentum derivative scout
**Runner:** `scripts/frontier_yt_scalar_ladder_total_momentum_derivative_scout.py`
**Certificate:** `outputs/yt_scalar_ladder_total_momentum_derivative_scout_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support / scalar ladder total-momentum derivative scout
conditional_surface_status: conditional-support if the finite-volume, IR, zero-mode, projector, and pole-derivative limits are derived
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The derivative is finite in a scout, but no retained limiting theorem or production pole derivative is supplied."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Scout

The previous eigen-derivative gate showed that a scalar ladder pole witness
needs more than:

```text
lambda_max(pole) = 1
```

It needs the total-momentum derivative:

```text
d lambda_max / d p^2
```

This runner computes a finite Wilson-exchange ladder scout by shifting the
fermion bubble denominators with total scalar momentum `p/2` and `-p/2`,
then finite-differencing the largest ladder eigenvalue.

Validation:

```text
python3 scripts/frontier_yt_scalar_ladder_total_momentum_derivative_scout.py
# SUMMARY: PASS=9 FAIL=0
```

## Result

The derivative is finite across the scanned finite surfaces.  It is negative
throughout this scan, but its magnitude varies strongly with mass, volume,
IR regulator, zero-mode treatment, and scalar projector.  The output reports
an absolute derivative spread of about `3903.98` across 108 scan points, and
27 points have `lambda_max(p=0) >= 1`.

This is useful constructive support for the scalar-LSZ route: the missing
quantity is computable once the correct finite-volume, IR, zero-mode, and
projector prescription is fixed.  It is not closure.  The scout does not prove
that the derivative has a controlled continuum/IR limit, does not derive the
canonical Higgs normalization, and does not supply production pole data.

## Claim Boundary

This block does not set `kappa_s = 1`, `c2 = 1`, or `Z_match = 1`.  It does not
use `H_unit`, `yt_ward_identity`, alpha/plaquette/u0, observed top/Yukawa
values, or reduced cold pilots as proof selectors.  PR #230 remains open until
the scalar pole derivative is derived or measured with controlled matching.
