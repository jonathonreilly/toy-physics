# Top-Yukawa Joint Feynman-Hellmann / Scalar-LSZ Resource Projection

**Date:** 2026-05-01
**Status:** bounded-support / joint FH-LSZ production resource projection
**Runner:** `scripts/frontier_yt_fh_lsz_joint_resource_projection.py`
**Certificate:** `outputs/yt_fh_lsz_joint_resource_projection_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support / joint FH-LSZ production resource projection
conditional_surface_status: production-planning support for future joint dE/ds plus scalar-LSZ measurement
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Projected compute cost and harness readiness do not derive kappa_s or provide production measurements."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Projection

The joint physical-response route is executable after the harness extensions,
but it is not a foreground closure route.

Using the existing production resource projection as the baseline:

```text
direct three-volume mass-scaled projection: 228.48 single-worker hours
```

and a modest scalar-LSZ plan:

```text
base mass points: 3
source shifts: 3
scalar-LSZ momenta: 4
scalar-LSZ noise vectors/configuration: 16
```

the fermion solve budget is approximately:

```text
solve factor vs three-mass direct route: 15.8889
joint mass-scaled projection: 3630.28 single-worker hours
joint mass-scaled projection: 151.26 single-worker days
```

Validation:

```text
python3 scripts/frontier_yt_fh_lsz_joint_resource_projection.py
# SUMMARY: PASS=7 FAIL=0
```

## Result

The exact next action is no longer additional reduced-scope harness plumbing.
It is one of:

- choose a scalar-LSZ momentum/noise budget from a pilot variance study;
- launch the joint production harness on saved gauge ensembles;
- fit correlated `dE_top/ds` and `Gamma_ss(q)` on the same ensemble stream;
- derive the scalar pole and `dGamma_ss/dp^2` in the controlled
  finite-volume/IR limit;
- convert `dE_top/ds` to physical `dE_top/dh` only after deriving `kappa_s`.

## Claim Boundary

This projection is not production evidence and not a scalar LSZ theorem.  It
does not set `kappa_s = 1`, `c2 = 1`, or `Z_match = 1`, and it does not use
`H_unit`, `yt_ward_identity`, observed top mass, or observed `y_t`.
