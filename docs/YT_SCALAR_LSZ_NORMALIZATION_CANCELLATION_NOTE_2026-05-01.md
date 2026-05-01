# Top-Yukawa Scalar LSZ Normalization Cancellation

**Date:** 2026-05-01  
**Status:** conditional support / scalar LSZ normalization cancellation  
**Runner:** `scripts/frontier_yt_scalar_lsz_normalization_cancellation.py`  
**Certificate:** `outputs/yt_scalar_lsz_normalization_cancellation_2026-05-01.json`

```yaml
actual_current_surface_status: conditional-support
conditional_surface_status: conditional-support for a future interacting scalar-channel LSZ theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The interacting scalar-channel kernel and pole-residue derivative remain open imports."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The projector-normalization obstruction showed that a finite ladder pole test is
not invariant if the scalar source is rescaled while the kernel is held fixed.
This note tests the constructive alternative: in a derived
Bethe-Salpeter/RPA scalar channel, source normalization, kernel normalization,
and LSZ residue must transform together.

## Runner Result

```text
python3 scripts/frontier_yt_scalar_lsz_normalization_cancellation.py
# SUMMARY: PASS=6 FAIL=0
```

The runner uses the free Wilson-staggered bubble as a controlled finite model
and imposes an RPA-like pole denominator only to test normalization covariance.

| Check | Result |
|---|---|
| free bubble derivative finite | `Z_inv_base=0.237218171767` |
| fixed-kernel source rescaling breaks pole | yes |
| covariant kernel rescaling restores pole | max residual `< 1e-10` |
| canonical LSZ `y` proxy source-scale invariant | relative spread `< 1e-12` |
| source propagator residue scales inversely | ratio `16` for `c=0.5` vs `c=2` |

## Consequence

Pure scalar-source normalization is not the final obstruction if the scalar
kernel and source projector are derived as one covariant object.  The canonical
LSZ proxy

```text
y_canonical ~ vertex_source / sqrt(Z_inverse)
```

is invariant under `O -> c O` when the denominator and residue transform
consistently.

This is still not retained closure.  The runner chooses a pole condition inside
the model; PR #230 still needs a theorem deriving the interacting
Wilson-staggered scalar-channel denominator, pole location, finite-volume/IR
limit, and inverse-propagator derivative.

## Non-Claims

- This note is not a retained `y_t` derivation.
- This note is not a production measurement.
- This note does not use observed top, Higgs, or Yukawa values.
- This note does not define `y_t` through an `H_unit` matrix element.
- This note does not set a contact kernel by fiat as proof.
