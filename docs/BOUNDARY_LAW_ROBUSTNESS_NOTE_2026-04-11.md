# Boundary-Law Robustness Addendum

**Date:** 2026-04-11
**Status:** bounded finite-run numerical robustness diagnostic on a
pre-registered parameter envelope (not a boundary-law theorem, not a holography
proof)

Primary artifact:
- `/Users/jonreilly/Projects/Physics/scripts/frontier_boundary_law_robustness.py`

Companion retained note:
- [`HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md`](HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md)

## Claim scope (read this first)

This addendum is a **bounded finite-run numerical robustness diagnostic** on
the pre-registered parameter envelope below. It is *not*:

- a clean bounded theorem-level boundary-law result,
- a parameter-independent area-law statement,
- a holography proof,
- evidence that the linear `S` versus `|boundary|` fit holds outside the
  pre-registered envelope.

The conclusion depends on (a) finite selected observables, (b) fixed model
parameters, (c) selected sizes/seeds/couplings/partitions, and (d) the `R^2`
linear-fit readout. None of these are forced by retained inputs and the
addendum should not be cited as if they were.

The auditor verdict requires that the retained statement be limited to "the
exact fixed-run numerical observation that this script/parameter grid reports
high `R^2` boundary-size linearity for the audited BFS-ball sweep and the
stated small partition check; it should not be cited as a general boundary-law
theorem or holography proof". This addendum is now scoped accordingly.

## Pre-registered parameter envelope

The diagnostic is run exactly once on this fixed surface and is not claimed
outside it.

Model parameters (fixed, not swept):
- `MASS = 0.30`
- `MU2 = 0.22`
- `DT = 0.12`
- `N_STEPS = 30`
- `SIGMA = 1.5`
- `JITTER = 0.05`

Counted BFS-ball sweep (pre-registered):
- sides: `{6, 8, 10, 12, 14}`
- couplings: `G in {0, 5, 10, 20}`
- seeds: `{42, 43, 44, 45, 46}`
- total counted BFS-ball fits: `100 = 5 sides x 4 couplings x 5 seeds`

Partition cross-check (pre-registered, smaller and separate):
- single side: `10`
- single coupling: `G = 10`
- partitions: `{BFS-ball, rectangular, random}`

The grid above is what the runner sweeps. The diagnostic does not assert
anything about other lattice geometries (non-2D, non-periodic, non-square),
other Hamiltonians, other entanglement carriers, or other readouts.

## What Was Rerun

Rerun command:

```bash
source /tmp/physics_venv/bin/activate && python scripts/frontier_boundary_law_robustness.py
```

## Exact Rerun Numbers

This note reflects the current-main minimum-image rerun on the periodic surface.

### Counted BFS-ball surface (full 100-config grid)

- total configs: `100`
- `R^2 > 0.95`: `100/100`
- `R^2 > 0.99`: `78/100`
- `R^2` range: `0.974518` to `1.000000`
- `R^2` mean +/- std: `0.994607 +/- 0.007004`

### Three-or-more-radii subgrid (audit-relevant subset)

The `side = 6` rows in the BFS-ball sweep have only two available radii at
`R = 1, 2`, so `R^2 = 1.0` is automatic by two-point linear regression. These
`20/100` configurations carry no diagnostic information about boundary-law
linearity. Excluding them isolates the configurations that actually probe a
linear-versus-nonlinear distinction.

- counted configs with `>= 3` BFS radii: `80/100` (sides `8, 10, 12, 14` x
  `G in {0, 5, 10, 20}` x `5` seeds)
- `R^2 > 0.95` on the 3+-radii subgrid: `80/80`
- `R^2 > 0.99` on the 3+-radii subgrid: `58/80`
- `R^2` range on the 3+-radii subgrid: `0.974518` to `0.999971`
- `R^2` mean +/- std on the 3+-radii subgrid: `0.993258 +/- 0.007227`

### Partition cross-check (`side = 10`, `G = 10`)

- BFS-ball: `R^2` mean +/- std `0.995138 +/- 0.001668`
- rectangular: `R^2` mean +/- std `0.994513 +/- 0.002123`
- random: `R^2` mean +/- std `0.995500 +/- 0.002903`

## Caveats and audit-flagged limitations

The auditor flagged the following limitations explicitly. They remain.

- **Two-point fits are automatic.** `20/100` BFS counted fits come from
  `side = 6`, where only `2` radii are available. Those are two-point fits, so
  `R^2 = 1.0` there is automatic and should be reported separately, as above.
- **Counted-grid scope only.** The `100/100 R^2 > 0.95` figure applies only to
  the BFS-ball sweep. The partition-family generalization evidence is smaller
  (one size, one coupling, three partition geometries, five seeds) and
  separate.
- **Selection-of-observables risk.** The diagnostic is the linear fit of the
  Dirac-sea entanglement entropy `S` versus the counted boundary-edge size
  `|boundary|`. Other readouts (e.g., volume fits, RT-style minimal surfaces,
  Schmidt-rank scaling) are not part of this addendum.
- **Fixed parameters.** `MASS`, `MU2`, `DT`, `N_STEPS`, `SIGMA`, and `JITTER`
  are fixed values, not swept axes. The diagnostic does not bound the fit
  quality outside these fixed parameters.
- **Fixed grid.** The pre-registered envelope above is the full sweep set.
  This addendum makes no claim outside that envelope.
- **Minimum-image periodic geometry only.** This is the corrected
  minimum-image periodic rerun; older pre-fix torus numbers should not be
  reused.
- **Bounded, not theorem-level.** This is a finite-run numerical robustness
  addendum for the bounded many-body-style boundary-law probe in the
  companion holographic note. It is not, by itself, a holography proof and is
  not a parameter-independent boundary-law theorem.

## Strongest honest claim

> On the pre-registered parameter envelope above (2D periodic staggered
> lattice with small positional jitter, fixed `MASS`, `MU2`, `DT`, `N_STEPS`,
> `SIGMA`, and `JITTER`), the Dirac-sea entanglement entropy is highly linear
> in counted BFS-ball boundary size: every counted fit on the `5 sides x 4
> couplings x 5 seeds = 100`-configuration BFS-ball grid satisfies
> `R^2 > 0.95`, and the `80`-configuration `>= 3`-radii subgrid (which
> excludes the automatic two-point `side = 6` rows) also satisfies
> `R^2 > 0.95` in `80/80` configurations. The complementary partition
> cross-check at `side = 10, G = 10` reports `R^2 > 0.95` on `BFS-ball`,
> `rectangular`, and `random` partition geometries.

This is a bounded finite-run diagnostic on the stated envelope. It is not a
boundary-law theorem and it is not parameter-independent.

## What is out of scope

- Parameter-independence of the boundary-law structure (size, seed, coupling,
  partition).
- A clean bounded theorem-level statement that the linear fit holds for all
  parameters in some retained-grade family.
- A holography or AdS/CFT closure.
- Any continuum limit or thermodynamic extrapolation.
- Replacing or amending the broader Widom-class no-go in
  [`AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md`](AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md).
- Identifying the area-law coefficient with the Planck packet `1/4`. See
  [`AREA_LAW_COEFFICIENT_GAP_NOTE.md`](AREA_LAW_COEFFICIENT_GAP_NOTE.md) for
  the canonical gap analysis.

The auditor-recommended path to lift this to theorem status (analytic closure
or substantially broader independent partition and size checks under the
parameter sweep) is not attempted in this addendum.
