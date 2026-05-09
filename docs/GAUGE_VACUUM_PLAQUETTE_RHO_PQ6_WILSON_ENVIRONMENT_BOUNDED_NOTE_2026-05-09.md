# Gauge-Vacuum Plaquette Rho(p,q)(6) Wilson Environment Bounded Note

**Date:** 2026-05-09
**Claim type:** bounded_theorem
**Status:** bounded support theorem, unaudited.
**Primary runner:** `scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py`

## Claim

For the single-link SU(3) Wilson boundary class function at `beta = 6`,

```text
c_(p,q)(6) = integral_SU(3) chi_(p,q)(U) exp((6/3) Re tr U) dU,
rho_(p,q)(6) = c_(p,q)(6) / (d_(p,q) c_(0,0)(6)),
```

the runner computes the normalized coefficients on the finite box
`0 <= p,q <= 4` by two independent methods:

- a Schur-Weyl Bessel-determinant sum, and
- direct Weyl integration on the SU(3) Cartan torus with Vandermonde squared.

The two evaluations agree to `4.136e-15` absolute and `7.952e-14`
relative error on that finite box.

Selected representative values are:

```text
rho_(0,0)(6) = 1.000000000000e+00
rho_(1,0)(6) = rho_(0,1)(6) = 4.225317396500e-01
rho_(1,1)(6) = 1.622597994799e-01
rho_(2,0)(6) = rho_(0,2)(6) = 1.359617273634e-01
rho_(2,1)(6) = rho_(1,2)(6) = 4.828805556745e-02
rho_(3,0)(6) = rho_(0,3)(6) = 3.505738045167e-02
rho_(2,2)(6) = 1.350507888830e-02
```

The same finite calculation verifies conjugation symmetry
`rho_(p,q)(6) = rho_(q,p)(6)`, positivity on the computed box, and diagonal
action of the finite operator `R_6^env chi_(p,q) = rho_(p,q)(6) chi_(p,q)`
when these computed coefficients are used.

## Scope

This is a bounded finite-coefficient result for the canonical normalized
single-link Wilson boundary class function. It replaces the prior arbitrary
witness sequence on the computed finite box.

It does not close:

- an all-weight formula for `rho_(p,q)(6)`;
- the full unmarked spatial Wilson tensor-transfer/Perron problem;
- analytic closure of canonical `P(6)`;
- retained status for the parent residual-environment identification notes.

Those parent gates remain audit-lane questions. This note only supplies a
runner-backed bounded coefficient table that future repair or audit work may
use.

## Audit Consequence

```yaml
claim_id: gauge_vacuum_plaquette_rho_pq6_wilson_environment_bounded_note_2026-05-09
note_path: docs/GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md
runner_path: scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps: []
audit_authority: independent audit lane only
```

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=7 SUPPORT=3 FAIL=0
```
