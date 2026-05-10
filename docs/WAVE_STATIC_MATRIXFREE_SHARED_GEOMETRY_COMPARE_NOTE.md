# Wave Static Matrix-Free Shared Geometry Compare

**Date:** 2026-04-08
**Status:** proposed_retained engine-equivalence probe

**Audit-conditional perimeter (2026-04-27):**
The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, `claim_type =
positive_theorem`, and load-bearing step class `C`. The audit
chain-closure explanation is exact: "The live runner reproduces the
two numerical comparison tables, but it does not define or pass a
drop-in-replacement acceptance criterion; its own printed verdict
says the matrix-free result is close but not yet proven identical."
The audit-stated repair target is exact: `runner_artifact_issue` —
"add an audited acceptance criterion for drop-in replacement, such
as field and propagated-response tolerances tied to solver
residuals, or prove both algorithms converge to the same finite-grid
Poisson solution with a runner pass/fail threshold." This
rigorization edit only sharpens the boundary of the conditional
perimeter; nothing here promotes audit status. The retained
conclusion is already narrowed to a "strong drop-in replacement on
the shared geometries tested" engine-equivalence probe and is not a
formal drop-in-replacement theorem; that scope is unaffected.

This probe compares the existing direct static solver against the
matrix-free static solver on one shared geometry and the same beam setup.

The test is intentionally narrow:

> Is the matrix-free static engine a drop-in replacement for the current
> direct discrete static comparator?

## What it compares

- exact discrete static field from the direct probe
- exact discrete static field from the matrix-free probe
- beam-side centroid shift through the same beam DAG

## Retained result

The retained runs use the shared frozen source at `z_phys = 3.0`
at two shared lattice spacings:

| H | realized `z_src` | `max |direct-mf|` | `rel field mismatch` | `rel(dS)` | `rel_MS` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0.35` | `3.15` | `1.203e-08` | `4.481e-06` | `2.825e-06` | `22.86%` |
| `0.25` | `3.00` | `2.327e-08` | `7.940e-06` | `1.863e-06` | `62.09%` |

At both tested `H` values, the direct and matrix-free solvers agree
extremely closely on the static field and on the propagated static
beam response:

- `H=0.35`
  - direct residual `= 1.997e-10`
  - matrix-free residual `= 2.292e-10`
  - matrix-free iterations `= 86`
  - `dS direct = +0.010863`
  - `dS mf = +0.010863`
- `H=0.25`
  - direct residual `= 1.992e-10`
  - matrix-free residual `= 1.830e-10`
  - matrix-free iterations `= 115`
  - `dS direct = +0.015456`
  - `dS mf = +0.015456`

The underlying exact-static comparator is still far from `dM` on these
shared geometries, but that is a comparator-science issue, not an
engine-equivalence issue.

So the retained conclusion here stays narrow:

> matrix-free is a strong drop-in replacement for the direct exact-static
> engine on the shared geometries tested.

## Honest read

This note does **not** rescue the exact-comparator lane by itself.
At both tested `H` values, `rel_MS` is still large (`22.86%` and
`62.09%`), so the static comparator can still disagree materially
with the retarded response even when the two static engines agree
with each other almost exactly.

The retained read is:

- matrix-free is a sound engineering path for the exact-static branch
- the remaining problem is the comparator science, not the solver engine

## Artifact chain

- [`scripts/wave_static_matrixfree_shared_geometry_compare.py`](../scripts/wave_static_matrixfree_shared_geometry_compare.py)
- [`scripts/wave_static_matrixfree_shared_geometry_compare_freeze.py`](../scripts/wave_static_matrixfree_shared_geometry_compare_freeze.py)
- [`logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare-h035.txt`](../logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare-h035.txt)
- [`logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare-h025.txt`](../logs/2026-04-08-wave-static-matrixfree-shared-geometry-compare-h025.txt)

## Cited authority chain (2026-05-10)

The active runner is
[`scripts/wave_static_matrixfree_shared_geometry_compare.py`](../scripts/wave_static_matrixfree_shared_geometry_compare.py)
(audit-lane runner cache: `status: ok`, elapsed ~60 s, exit 0,
unmodified runner SHA pinned by the cache). The frozen freeze
helper is
[`scripts/wave_static_matrixfree_shared_geometry_compare_freeze.py`](../scripts/wave_static_matrixfree_shared_geometry_compare_freeze.py).
The frozen outputs are the two H-pair logs cited above.

The runner reproduces both numerical comparison tables verbatim
(`H=0.35` and `H=0.25` rows of the retained-result table at the top
of this note) and the matched solver residuals
(`direct residual ~ 1.99e-10` and `matrix-free residual ~ 2.0e-10`
at both H values, with `dS direct == dS mf` to printed precision at
both H). The two-row engine-equivalence numbers are therefore
already verifiable from the runner cache.

What the runner does not yet do, and what the audit verdict's
repair target names exactly, is define an asserted pass/fail
acceptance criterion for "drop-in replacement". The runner's own
printed verdict ("close but not yet proven identical") is the
audit-conditional perimeter the verdict cites verbatim. The retained
narrow conclusion of this note ("matrix-free is a strong drop-in
replacement for the direct exact-static engine on the shared
geometries tested") is exactly that engine-equivalence probe scope
and is unaffected; the formal drop-in-replacement theorem (with
field/propagated-response tolerances tied to solver residuals or a
shared finite-grid Poisson convergence proof) is the named
follow-up runner workload. The downstream `rel_MS` mismatch
(`22.86%` and `62.09%`) between exact-static and `dM` is an
independent comparator-science issue and is not reopened by this
rigorization edit.
