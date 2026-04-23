# DM Split-2 Upper-Face Dense-Grid Dominance Support

**Date:** 2026-04-21
**Status:** strong carrier-side support on the residual split-2 neighborhoods; not interval-certified closure.
**Runner:** `scripts/frontier_dm_split2_dense_grid_lipschitz_dominance_support_2026_04_21.py`

---

## Review-surface target

The live carrier-side blocker on the DM flagship lane is narrower than the
older broad-box search. The active residual neighborhoods are the two
explicit split-2 upper-face boxes isolated by
`DM_NEUTRINO_SOURCE_SURFACE_CARRIER_SIDE_CONCLUSION_NOTE_2026-04-18.md`.

The strict remaining theorem target is still:

> interval-certified exact-carrier dominance/completeness on the residual
> split-2 selector branch.

This note does **not** claim that full target. What it adds is a much stronger
review-grade support packet on the exact two neighborhoods currently carrying
the residual pressure.

## Target neighborhoods

Two explicit 3-real boxes in `(m, delta, s)` where `s = q_+ - q_floor(delta)`:

| Box | m bounds | delta bounds | s bounds | Peak near |
|---|---|---|---|---|
| **CAP_BOX** | `[-0.145, -0.140]` | `[1.1835, 1.1935]` | `[0.0145, 0.0245]` | `(-0.14, 1.188513, 0.019504)` |
| **ENDPOINT_BOX** | `[-0.145, -0.140]` | `[1.1839, 1.1890]` | `[0.0, 0.005]` | `(-0.14, 1.188956, 0)` |

## Existing support before this note

`frontier_dm_neutrino_source_surface_split2_upper_face_local_neighborhoods_candidate.py`
already tested `11 x 31 x 31 = 10,571` samples per box and found:

- `CAP_BOX`: `max eta_best = 0.884523189582`
- `ENDPOINT_BOX`: `max eta_best = 0.883977578548`
- no sampled point reaches transport closure `eta_best >= 1`

That was useful evidence, but it was still only a sampled candidate result.

## New support packet

This note adds three strengthening steps:

1. `51 x 51 x 51 = 132,651` samples per box, giving a much denser audit of
   each neighborhood.
2. An empirical finite-difference Lipschitz estimate for `eta_best(m, delta, s)`
   over the scanned grid.
3. A seeded constrained optimization search to look for rivals hiding between
   grid cells.

The key point is not that this becomes a rigorous interval theorem. It does
not. The point is that the observed margin to transport closure is much larger
than the empirical interpolation error on these boxes.

## Results

| Box | Feasible (`Lambda_+ <= Lambda_+*`) | Grid max eta | Seed-opt max eta | Empirical-Lipschitz upper bound | Margin to 1.0 |
|---|---:|---:|---:|---:|---:|
| CAP_BOX | 40,193 | 0.884524 | 0.884530 | 0.884553 | **0.115447** |
| ENDPOINT_BOX | 80,855 | 0.883985 | 0.883987 | 0.884005 | **0.115995** |

So on both explicit neighborhoods:

- dense-grid sampling stays well below `eta = 1`
- seeded optimization does not find a rival above the grid maxima
- the empirical Lipschitz correction is about `2 x 10^-5`
- the residual margin to `eta = 1` is about `1.15 x 10^-1`

That is a separation of roughly four orders of magnitude.

## Runner summary

The accompanying runner passes `9/9` checks:

| Test | Result |
|---|---|
| CAP_BOX dense-grid max eta < 1 with margin > 0.1 | PASS |
| CAP_BOX seeded optimization consistent with grid | PASS |
| CAP_BOX empirical-Lipschitz upper bound < 1 | PASS |
| ENDPOINT_BOX dense-grid max eta < 1 with margin > 0.1 | PASS |
| ENDPOINT_BOX seeded optimization consistent with grid | PASS |
| ENDPOINT_BOX empirical-Lipschitz upper bound < 1 | PASS |
| Both boxes contain feasible lower-repair points | PASS |
| Dense grid is substantially stronger than the earlier sample audit | PASS |
| No rival with `eta_best >= 1` was found by seeded optimization | PASS |

## Honest verdict

What this note establishes:

- the residual split-2 carrier pressure is still localized to the same two
  explicit upper-face neighborhoods
- on those neighborhoods, the best currently tested values remain well below
  transport closure
- the dense-grid plus empirical-Lipschitz plus seeded-search packet is strong
  support for local dominance on the current exact carrier data

What it does **not** establish:

- a theorem-grade interval certificate on the exact carrier
- a rigorous analytic Lipschitz bound
- a certified ODE/transport enclosure
- full exact-carrier dominance/completeness on the residual split-2 branch

So the package-surface status should now read:

> the residual split-2 carrier blocker is materially narrowed by dense-grid
> and empirical-Lipschitz support, but the strict interval-certified
> exact-carrier dominance/completeness item remains open.

## Remaining gap

To close the residual carrier-side blocker outright, the branch still needs a
true rigorous enclosure of the exact carrier pipeline on these neighborhoods:

- rigorous analytic or interval bounds on the Hermitian spectral data
- certified bounds on the transport/ODE layer
- a full interval proof that `eta_best < 1` on the relevant feasible set

Until then this note should be read as the strongest current carrier-side
support packet, not as the final dominance theorem.
