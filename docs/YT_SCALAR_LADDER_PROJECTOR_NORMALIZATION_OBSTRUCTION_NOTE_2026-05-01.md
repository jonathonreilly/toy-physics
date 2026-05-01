# Top-Yukawa Scalar Ladder Projector-Normalization Obstruction

**Date:** 2026-05-01  
**Status:** exact negative boundary / projector-normalization obstruction  
**Runner:** `scripts/frontier_yt_scalar_ladder_projector_normalization_obstruction.py`  
**Certificate:** `outputs/yt_scalar_ladder_projector_normalization_obstruction_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support for a future scalar projector and LSZ theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The scalar projector/source normalization is not fixed by the current retained surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The scalar-channel input audit found an exact formula-level equality:

```text
F_scalar_ps(k) = F_gauge(k) = sum_mu cos^2(k_mu/2).
```

This note tests whether that equality is enough to fix the scalar-channel
ladder pole criterion.  It is not.  The pole test is sensitive to the scalar
source/projector normalization.

## Runner Result

```text
python3 scripts/frontier_yt_scalar_ladder_projector_normalization_obstruction.py
# SUMMARY: PASS=6 FAIL=0
```

The runner evaluates the same finite `4^4` Wilson-exchange ladder kernel at
`m=0.50`, `mu_IR^2=0.20`, varying only the scalar projector:

| Projector | `lambda_max` |
|---|---:|
| local scalar source | `0.609481173204` |
| raw point-split scalar | `6.795902611879` |
| zero-momentum-normalized point-split scalar | `0.424743913242` |
| uniform source scale `2` | `2.437924692817` |
| uniform source scale `0.5` | `0.152370293301` |

Two exact checks expose the obstruction:

```text
lambda_max[c O] / lambda_max[O] = c^2
lambda_max[F_ps] / lambda_max[F_ps/4] = 16
```

Thus the same kernel can pass or fail the scout pole criterion
`lambda_max >= 1` depending only on scalar source normalization.

## Consequence

The equality of scalar and gauge kinematic factors is useful exact support, but
it is not a physical readout.  A closure route still needs:

```text
scalar projector from the Cl(3)/Z^3 Wilson-staggered substrate
+ source normalization independent of H_unit matrix-element authority
+ scalar LSZ residue from the interacting two-point function
+ eigenvalue/pole test rerun with that fixed projector
```

Without that theorem, the scalar-channel ladder route remains open and cannot
certify `y_t`.

## Non-Claims

- This note is not a `y_t` derivation.
- This note is not a production measurement.
- This note does not use `alpha_LM` or plaquette normalization.
- This note does not define `y_t` through an `H_unit` matrix element.
