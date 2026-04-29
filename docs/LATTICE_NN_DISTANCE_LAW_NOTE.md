# NN Lattice Distance-Law Note

**Date:** 2026-04-03 (status line narrowed 2026-04-28 per audit-lane verdict)
**Status:** bounded conditional distance-law signal on the refinement path — live distance-law numbers reproduce in the runner, but the path is inherited from an upstream Born-clean NN branch whose note is not audit-clean; archived logs named by the source are absent from this worktree; the distance runner does not check Born or `k = 0`. Not a tier-ratifiable Born-safe refinement-path theorem.

This note freezes the nearest-neighbor lattice distance-law probe.
It answers a narrow question:

- on the raw NN refinement path inherited from the upstream Born-clean branch,
  does the barrier-harness distance
  signal remain meaningful?
- if simple `h`-dependent strength laws are used, does the distance-law
  magnitude improve, degrade, or stay flat?

Artifacts:

- [`scripts/lattice_nn_distance_law.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_distance_law.py)
- [`logs/2026-04-03-lattice-nn-distance-law.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-nn-distance-law.txt)
- upstream refinement note:
  [`docs/LATTICE_NN_CONTINUUM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_NN_CONTINUUM_NOTE.md)

## Scope

This is the **barrier harness only** from the raw nearest-neighbor family.

- it does **not** use the ordered-lattice no-barrier branch
- it does **not** mix in the ordered-lattice `1/b` branch
- it keeps the raw NN slit geometry used in the refinement study
- it reports signed centroid shift and `|delta|` separately

## Canonical sweep

The probe uses:

- `h = 1.0, 0.5, 0.25`
- `b = 3, 5, 7, 10, 13, 16, 19`
- two strength schedules:
  - fixed strength
  - `alpha = 1.5` with `strength = s0 / h^alpha`

## Retained read

### Fixed strength

The refined raw NN path keeps a clear far-field magnitude law:

| `h` | far-field sign | `|delta| ~ b^alpha` | `R^2` |
|---|---|---:|---:|
| `1.0` | negative | `-1.886` | `0.922` |
| `0.5` | positive for `b >= 7` | `-0.966` | `0.966` |
| `0.25` | positive for `b >= 7` | `-0.929` | `0.996` |

Saved raw rows:

| `h` | `b` | `delta` |
|---|---:|---:|
| `0.5` | `3` | `-0.0494` |
| `0.5` | `5` | `+0.0162` |
| `0.5` | `7` | `+0.1323` |
| `0.5` | `10` | `+0.1114` |
| `0.5` | `13` | `+0.0821` |
| `0.5` | `16` | `+0.0639` |
| `0.5` | `19` | `+0.0514` |
| `0.25` | `3` | `+0.0160` |
| `0.25` | `5` | `+0.0773` |
| `0.25` | `7` | `+0.0857` |
| `0.25` | `10` | `+0.0642` |
| `0.25` | `13` | `+0.0504` |
| `0.25` | `16` | `+0.0408` |
| `0.25` | `19` | `+0.0338` |

### `alpha = 1.5`

The alpha-scaled schedule keeps the signal but flattens the far-field decay:

| `h` | far-field sign | `|delta| ~ b^alpha` | `R^2` |
|---|---|---:|---:|
| `0.5` | positive for `b >= 7` | `-0.815` | `0.909` |
| `0.25` | positive for `b >= 7` | `-0.692` | `0.956` |

## Interpretation

The distance-law signal is **retained** on the Born-safe refinement path:

- coarse `h = 1.0` has a decaying magnitude law, but the far-field sign is
  negative rather than attractive
- refined `h = 0.5` and `h = 0.25` both retain a positive far-field signal
- the fixed-strength path has the cleanest far-field decay, close to `1/b`
- the alpha-scaled path does **not** improve the distance law; it mildly
  flattens the decay while keeping the far-field sign positive

So the correct narrow read is:

- the raw NN branch keeps a meaningful distance-law magnitude under refinement
- the sign is only clean in the far field, not across the whole `b` sweep
- simple alpha scaling is **degrading / flattening**, not rescuing, the magnitude law

## Safe conclusion

Use this wording:

- the nearest-neighbor lattice retains a meaningful **far-field** distance-law
  signal on the refinement path inherited from the upstream Born-clean NN note
- the signal is strongest in the raw fixed-strength window through `h = 0.25`
- simple alpha-scaled strength laws preserve the signal but slightly flatten the
  decay
- the near-field sign remains mixed, so the retained claim is about the
  far-field magnitude law rather than a clean signed attraction law everywhere

Do **not** overstate this as a full continuum theorem or as a universal
attraction law across all `b`.

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, leaf criticality):

> Issue: the source's live distance-law numbers reproduce, but the
> retained claim is explicitly on a refinement path inherited from
> an upstream Born-clean NN branch whose note is not audit-clean;
> the archived logs named by the source are also absent from this
> worktree, and the distance runner does not check Born or k=0.

## What this note does NOT claim

- A tier-ratifiable Born-safe refinement-path theorem.
- That the upstream Born-clean NN branch is audit-clean.
- That the runner checks Born or `k = 0` (it does not).
- That the cited archived logs are present in the worktree (they
  are absent).

## What would close this lane (Path A future work)

A retained Born-safe refinement-path result would require:

1. Independently audit-clean upstream NN branch refinement controls.
2. Archived logs registered in `logs/`.
3. A runner that checks Born and `k = 0` alongside the distance-law
   fit.
