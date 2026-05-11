# 3D 1/L^2 Tail Statistics Note

**Date:** 2026-04-04  
**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem

**Review repair perimeter (2026-05-03 generated-audit context):**
Generated-audit context identified this chain-closure blocker: "The note states the width-8
statistics and the width-6 comparison, but the restricted packet
contains no runner output and no cited width-6 comparator authority.
The improvement claim therefore depends on premises not closed by
the provided inputs." The repair target being addressed is:
"provide the runner output/log as audit evidence and cite the exact
width-6 comparator note/status, or include the reproducible fit
calculation in the note." This rigorization edit only sharpens the
boundary of the repair perimeter; nothing here promotes audit
status. The runner cache file
[`logs/runner-cache/lattice_3d_l2_tail_stats.txt`](../logs/runner-cache/lattice_3d_l2_tail_stats.txt)
(the canonical SHA-pinned cache path under
[`scripts/runner_cache.py`](../scripts/runner_cache.py)) records the
current default-budget behavior; the runner still times out at the
120 s default ceiling, so the completed frozen reference log
[`logs/2026-04-04-lattice-3d-l2-tail-stats.txt`](../logs/2026-04-04-lattice-3d-l2-tail-stats.txt)
remains the completed stdout artifact for the row read by this note.
The width-6 comparator
defaults are the
[`scripts/lattice_3d_inverse_square_kernel.py`](../scripts/lattice_3d_inverse_square_kernel.py)
module-top constants `PHYS_L = 12.0`, `PHYS_W = 6.0` against which
this note's `lattice_3d_l2_tail_stats.py` patches `PHYS_W = 8.0` (see
the `patched_branch` context manager in the runner). See "Cited
authority chain (2026-05-10)" below for the full provenance map.

## Purpose

This note freezes a narrow follow-up on the exploratory 3D `1/L^2`
propagator fork. The question is not whether the branch is promoted; it is
whether widening the `h = 0.25` lattice improves the post-peak tail fit
without losing the same-family barrier sanity checks.

Artifact chain:

- [`scripts/lattice_3d_l2_tail_stats.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_tail_stats.py)
- [`scripts/lattice_3d_inverse_square_kernel.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_inverse_square_kernel.py)
- [`logs/2026-04-04-lattice-3d-l2-tail-stats.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-lattice-3d-l2-tail-stats.txt)

## Result

The wider `h = 0.25` probe at `width = 8` stayed review-clean on the same
barrier geometry:

- Born: `3.75e-15`
- `k=0`: `0.000000`
- `dTV`: `0.358`
- barrier read: `ATTRACTIVE`

The no-barrier rows remained attractive across the post-peak sample:

| `z` | centroid | `P_near` | bias | read |
|---|---:|---:|---:|---|
| 4 | `+0.049373` | `+0.004422` | `+0.795766` | attractive |
| 5 | `+0.046445` | `+0.003459` | `+0.765371` | attractive |
| 6 | `+0.040248` | `+0.001309` | `+0.719169` | attractive |
| 7 | `+0.035067` | `+0.000651` | `+0.668926` | attractive |
| 8 | `+0.030697` | `+0.000357` | `+0.627323` | attractive |

Tail fit on the post-peak segment:

- `peak@z = 4`
- `n_tail = 5`
- exponent `b^(-0.70)`
- `R^2 = 0.955`

## Comparison

This is a real improvement over the earlier `h = 0.25`, width-6 readout that
had fewer post-peak points and a weaker tail fit (`b^(-0.53)` in the retained
summary). The wider lattice gives:

- more post-peak support points
- a steeper tail
- slightly better `R^2`

The right review-safe wording is still narrow:

- the wider lattice **improves the post-peak tail fit**
- it does **not** by itself prove an asymptotic `-2` law
- it remains a propagator-fork probe, not a promoted branch theorem

## Cited authority chain (2026-05-10)

The generated-audit context cited at top flagged that the
restricted audit packet "contains no runner output and no cited
width-6 comparator authority." The cited-authority chain on this
row is:

| Cited authority | File / log | Role |
|---|---|---|
| Active runner | [`scripts/lattice_3d_l2_tail_stats.py`](../scripts/lattice_3d_l2_tail_stats.py) | computes the width-8 row and the post-peak tail fit; patches `PHYS_W = 8.0` over the inverse-square kernel default `PHYS_W = 6.0` via the `patched_branch` context manager |
| Width-6 comparator (parent module) | [`scripts/lattice_3d_inverse_square_kernel.py`](../scripts/lattice_3d_inverse_square_kernel.py) | module-top constants `PHYS_L = 12.0`, `PHYS_W = 6.0`, `PHYS_CONNECTIVITY = 3.0`, `MASS_Z_VALUES = [2.0..7.0]`; provides the `build_family`, `barrier_metrics`, `no_barrier_distance`, and `fit_power` helpers used here |
| Frozen runner output | [`logs/2026-04-04-lattice-3d-l2-tail-stats.txt`](../logs/2026-04-04-lattice-3d-l2-tail-stats.txt) | preserves the exact width-8 Born=3.75e-15, k0=+0.000000, dTV=0.358 barrier row, the five no-barrier centroid rows for `z=4..8`, and the `tail fit: peak@z=4 n_tail=5 exponent=b^(-0.70) R^2=0.955` line cited in the Result table |
| Audit-lane runner cache | [`logs/runner-cache/lattice_3d_l2_tail_stats.txt`](../logs/runner-cache/lattice_3d_l2_tail_stats.txt) (canonical path under `scripts/runner_cache.py`) | SHA-pinned cache for the current runner source; currently records `status: timeout` at the 120 s default ceiling, so it is diagnostic freshness evidence rather than completed stdout. The completed row evidence remains the frozen log above; a future sliced runner or longer declared timeout is needed for an `ok` audit cache. |
| Cache contract | [`scripts/runner_cache.py`](../scripts/runner_cache.py) | declares the cache header format and `runner_sha256` pinning that lets the audit lane verify the cache is fresh against the current runner source |

The width-6 baseline cited in the Comparison section is the
inverse-square kernel default configuration: same family, same
barrier geometry, same action, `h = 0.25`, but `PHYS_W = 6.0` rather
than the patched `PHYS_W = 8.0` of this note. The narrower
post-peak window of the width-6 default produces fewer tail rows
and the weaker `b^(-0.53)` retained summary fit cited in the
Comparison section. This rigorization edit registers that
provenance explicitly so the audit-graph one-hop edges to the
inverse-square kernel module and to the frozen runner output are
visible in the source note.

This rigorization edit only sharpens the conditional perimeter and
registers the cited authority chain; it does not set audit status,
hand-author audit JSON, or claim a stronger asymptotic law beyond
the bounded post-peak improvement already in scope.
