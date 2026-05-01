# Top-Yukawa Scalar Ladder IR / Zero-Mode Obstruction

**Date:** 2026-05-01  
**Status:** exact negative boundary / scalar ladder IR zero-mode obstruction  
**Runner:** `scripts/frontier_yt_scalar_ladder_ir_zero_mode_obstruction.py`  
**Certificate:** `outputs/yt_scalar_ladder_ir_zero_mode_obstruction_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support for a future scalar-channel Bethe-Salpeter limiting theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The scalar ladder pole criterion depends on open IR/zero-mode and finite-volume limiting imports."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The scalar-channel ladder route is the highest-ranked analytic successor after
the projector-normalization obstruction.  This note asks whether the finite
Wilson-exchange ladder pole criterion is at least stable once the scalar source
is held fixed.

It is not.  The pole test remains load-bearingly dependent on the still-open
IR, finite-volume, and gauge zero-mode prescription.

## Runner Result

```text
python3 scripts/frontier_yt_scalar_ladder_ir_zero_mode_obstruction.py
# SUMMARY: PASS=7 FAIL=0
```

The runner uses the same finite scalar-channel ladder form as the prior scout,
but varies only the IR/zero-mode and finite-volume prescription after fixing the
source choice.

Key witnesses:

| Check | Witness |
|---|---:|
| fixed local source, `4^4`, `m=0.50`, `mu_IR^2=0.10`, zero mode included | `lambda_max = 1.02120376891` |
| same, zero mode removed | `lambda_max = 0.236938829531` |
| local source, zero mode included, `mu_IR^2=0.20`, `3^4` | `lambda_max = 1.32066531710` |
| same prescription, `5^4` | `lambda_max = 0.175318272179` |
| normalized point-split source, `3^4`, `mu_IR^2=0.20`, zero mode included | `lambda_max = 1.31898088871` |
| same, zero mode removed | `lambda_max = 0.0639786582793` |

Thus the same finite ladder kernel can pass or fail the scout pole test

```text
lambda_max >= 1
```

depending only on choices that the current PR #230 authority surface has not
derived.

## Consequence

This does not rule out the scalar Bethe-Salpeter route.  It narrows what the
route must prove before it can be load-bearing:

```text
gauge fixing / zero-mode treatment
+ finite-volume and IR limiting order
+ scalar source/projector normalization
+ eigenvalue crossing in that fixed limit
+ pole residue from d Gamma_phi^{-1} / d p^2
```

Without those pieces, a finite scalar ladder eigenvalue crossing is not a
physical top-Yukawa readout.

## Non-Claims

- This note is not a `y_t` derivation.
- This note is not a production measurement.
- This note is not a retained Bethe-Salpeter pole theorem.
- This note does not define `y_t` through an `H_unit` matrix element.
- This note does not use observed top, Higgs, or Yukawa values as selectors.
