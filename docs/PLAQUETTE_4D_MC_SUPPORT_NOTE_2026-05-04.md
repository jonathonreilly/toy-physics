# Plaquette 3+1D Wilson MC Support Note

**Date:** 2026-05-04
**Type:** bounded_theorem
**Claim scope:** deterministic seeded finite-volume Monte Carlo support for
the full `3 spatial + 1 derived time` periodic `SU(3)` Wilson plaquette
surface at `beta = 6`; this is support for the surface identification, not
an analytic `P(6)` closure and not a retained-status proposal.
**Status authority:** independent audit lane only. This source note is a
bounded support surface and does not supply an audit verdict.
**Primary runner:** `scripts/frontier_su3_4d_mc_support_2026_05_04.py`

## Question

The current plaquette authority surface,
[`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md),
keeps the canonical plaquette value bounded: `<P>(beta=6, SU(3), 4D)` is a
same-surface observable, while the exact analytic insertion at `beta = 6`
remains open.

PR #528 contained a useful diagnostic hidden inside broader promotion prose:
the earlier small spatial APBC block is not the full `3+1D` Wilson plaquette
surface. Does a direct finite-volume run on the full periodic four-dimensional
Wilson surface land in the canonical plaquette region?

## Answer

Yes, as bounded numerical support. A deterministic small-volume Metropolis run
on the full periodic `Ls = Lt = 2` and `Ls = Lt = 3` Wilson surfaces gives a
plaquette in the expected `0.59` region by `L = 3`.

This does **not** promote the plaquette note, does **not** establish an
analytic closed form, and does **not** replace the independent audit lane.
The result is useful because it separates the full `3+1D` Wilson surface from
the spatial-only minimal-block reading that produced much lower diagnostic
values.

## Setup

The runner uses:

- gauge group `SU(3)`;
- Wilson action at `beta = 6`;
- periodic boundary conditions in all four directions;
- a cold start and fixed pseudo-random seed `42`;
- small Metropolis updates generated from the Gell-Mann basis;
- finite volumes `Ls = Lt = 2` and `Ls = Lt = 3`.

The canonical comparator `0.5934` is used only as a bounded context value from
the current plaquette note and standard Wilson-lattice practice. It is not
used as a fitted target and it is not treated here as an audit-ratified
theorem.

## Runner Result

Command:

```bash
python3 scripts/frontier_su3_4d_mc_support_2026_05_04.py
```

Expected deterministic summary on the current environment:

```text
result Ls=2, Lt=2: P = 0.6257 +/- 0.0035
result Ls=3, Lt=3: P = 0.5970 +/- 0.0013
SUMMARY: PASS=4 FAIL=0
```

The assertions are intentionally broad:

- `L=2` remains in the expected small-volume beta=6 band;
- `L=3` lies in the canonical plaquette region;
- the `L=3` value is close to the `0.5934` comparator but is not a
  thermodynamic-limit proof;
- the full `3+1D` surface is numerically separated from a spatial-only
  minimal-block interpretation.

## What This Supports

This note supports a narrow correction to the plaquette bridge discussion:

> direct finite-volume computation on the accepted full `3+1D` Wilson surface
> is already in the canonical plaquette region at `L=3`; the lower
> spatial-only minimal-block values should not be read as the complete
> `3+1D` plaquette value.

This is consistent with the accepted Wilson-surface combinatorics in
[`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md).

## What Remains Open

The retained-grade questions remain exactly where the current repo leaves
them:

- analytic identification of `P(6)`;
- a rigorous thermodynamic-limit extrapolation with controlled
  autocorrelation and finite-size systematics;
- any downstream publication-status or parent-chain update.

The existing no-go/boundary notes remain in force:

- [`GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md)
  says the current exact stack does not determine the explicit
  nonperturbative framework point;
- [`GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)
  rules out the constant-lift shortcut.

## Import And Support Inventory

- **Computed input:** the two finite-volume MC values printed by the runner.
- **Admitted computational method:** standard finite-volume Metropolis
  lattice-gauge sampling on the Wilson action.
- **Comparator only:** `0.5934` as the canonical `SU(3)` Wilson
  plaquette-context value. This note does not derive or ratify it.
- **No new axiom:** no new gauge axiom, anisotropy axiom, fitted parameter, or
  downstream theory language is introduced.
