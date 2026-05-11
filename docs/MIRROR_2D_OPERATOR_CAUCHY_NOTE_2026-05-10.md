# 2D Mirror Operator-Cauchy Layer-Count No-Go

**Date:** 2026-05-10
**Claim type:** no_go (bounded numerical no-go for the current
`gen_2d_mirror` layer-count operator-Cauchy gate)
**Status:** source-note proposal only; independent audit controls any
downstream effective status.
**Status authority:** independent audit lane only.
**Primary runner:** [`scripts/mirror_2d_operator_cauchy.py`](../scripts/mirror_2d_operator_cauchy.py)
**Primary runner cache:** [`logs/runner-cache/mirror_2d_operator_cauchy.txt`](../logs/runner-cache/mirror_2d_operator_cauchy.txt)

## Claim Scope

This note tests one concrete question:

```text
Does the existing gen_2d_mirror harness pass the operator-Cauchy gate
when layer count N is treated as the refinement axis?
```

For the current harness and the tested grid

```text
N in {25, 40, 60, 80, 100, 150, 200},
```

the answer is no. The seed-mean five-observable vector fails the joint
operator-Cauchy gate, zero of five components pass the component gate,
and four of five components are non-monotone in `N`.

This is a bounded no-go for using the current layer-count axis as the
operator-Cauchy continuum bridge. It is not a no-go against redesigned
2D mirror families with a fixed physical domain and a true spacing
parameter.

## Harness Under Test

The runner calls the existing `measure_family(..., family="mirror", ...)`
path from `scripts/mirror_2d_validation.py`. Its mirror harness is
parameterized by:

- `nl`: layer count along the propagation axis;
- `npl_half = 12`: mirrored per-layer half-density;
- `yr = 10.0`: fixed transverse half-extent;
- `cr = 2.5`: fixed connect radius;
- `bl = nl // 3`: chokepoint layer;
- `grav_layer = 2 * nl // 3`: mass-source layer used by the measurement
  routine.

The test varies only `nl`. It leaves `npl_half`, `yr`, and `cr` fixed.
With the harness's unit inter-layer spacing convention, increasing `nl`
therefore lengthens the physical box and moves the chokepoint and
gravity-layer indices. It does not refine a fixed physical geometry.

## Observable Basis

For each `N`, the runner averages over eight deterministic seeds and the
`k`-band `{3.0, 5.0, 7.0}`. It records the five observables already used
by the mirror validation path:

| Symbol | Meaning |
| --- | --- |
| `MI` | slit-detector mutual information |
| `decoh` | `1 - pur_min` branch decoherence |
| `dTV` | total variation between branch outcome distributions |
| `gravity` | signed Born-weighted detector centroid shift |
| `born` | corrected three-slit Sorkin `|I_3| / P` floor |

The vector `vec(N)` is the seed-mean five-tuple. The joint Cauchy test
fits consecutive increments

```text
||vec(N_i) - vec(N_{i+1})||_2 ~ C N^r
```

against `sqrt(N_i N_{i+1})`. The review gate is

```text
r < -0.4 and R^2 >= 0.85.
```

## Runner Result

Seed-mean table from the runner. The first four columns are stable at the
shown precision; `born` stays at floating-point floor scale and can vary
at the last digits across BLAS/runtime scheduling.

| N | MI | decoh | dTV | gravity | born |
| --- | ---: | ---: | ---: | ---: | ---: |
| 25 | 5.02e-01 | 3.03e-01 | 6.00e-01 | +2.71 | floor |
| 40 | 5.37e-01 | 3.01e-01 | 6.22e-01 | +3.89 | floor |
| 60 | 7.56e-01 | 4.42e-01 | 8.57e-01 | +2.57 | floor |
| 80 | 5.65e-01 | 3.46e-01 | 6.74e-01 | +3.41 | floor |
| 100 | 3.46e-01 | 2.87e-01 | 5.46e-01 | +1.86 | floor |
| 150 | 4.90e-01 | 3.33e-01 | 6.25e-01 | +3.27 | floor |
| 200 | 3.08e-01 | 2.40e-01 | 4.72e-01 | +3.80 | floor |

Joint increments:

| Pair | `||vec(N_i) - vec(N_{i+1})||_2` |
| --- | ---: |
| 25 -> 40 | 1.176 |
| 40 -> 60 | 1.366 |
| 60 -> 80 | 0.884 |
| 80 -> 100 | 1.566 |
| 100 -> 150 | 1.415 |
| 150 -> 200 | 0.587 |

The joint fit is:

```text
r = -0.249
C = 3.27
R^2 = 0.173
```

The gate `r < -0.4 and R^2 >= 0.85` fails.

Per-component gates also fail:

| Observable | r | R^2 | Gate |
| --- | ---: | ---: | --- |
| `MI` | +0.686 | 0.355 | FAIL |
| `decoh` | +1.556 | 0.349 | FAIL |
| `dTV` | +0.626 | 0.200 | FAIL |
| `gravity` | -0.286 | 0.190 | FAIL |
| `born` | floor-scale | low | FAIL |

Four components, `MI`, `decoh`, `dTV`, and `gravity`, are non-monotone in
`N`. The `born` row stays at the linear-propagator precision floor.

## Guards

- Born floor: max `|I_3| / P` stays below `1e-14`, so the linear
  propagator is not broken by the sweep.
- Seed coverage: every `N` has at least 5 surviving seeds out of 8, so no
  row is a single-seed artifact.
- The runner exits nonzero if the Born guard fails, data coverage collapses,
  the joint Cauchy gate passes, any component Cauchy gate passes, or fewer
  than four components are non-monotone. A passing process is therefore a
  direct check of this no-go boundary.

## Structural Reading

The bounded numerical failure matches the harness structure. `N` is not a
spacing parameter for a fixed physical domain. Increasing `N` changes the
box length, moves the chokepoint from layer `nl // 3`, and moves the mass
source from layer `2 * nl // 3`. The vector sequence samples a family of
geometries rather than a fixed geometry at finer spacing.

That is the no-go: the current `gen_2d_mirror` layer-count axis does not
provide the same kind of operator-Cauchy bridge that a true `h -> 0`
spacing-refinement lane provides.

## Explicit Non-Claims

- This does not say the 2D mirror harness is useless.
- This does not rule out a redesigned mirror harness with fixed physical
  length `L`, spacing `h = L/N`, scaled density, and fixed physical
  chokepoint/source positions.
- This does not promote or change the audit status of
  `MIRROR_2D_GRAVITY_LAW_NOTE.md`; that note is relational context only.
- This does not claim a universal theorem about every construction that
  could be called a 2D mirror.

## Independent Audit Handoff

Audit status is set only by the independent audit lane. This source note
proposes one bounded `no_go` row with zero ledger dependencies:

```text
claim_type: no_go
declared_one_hop_deps: []
audit_status: unaudited
```
