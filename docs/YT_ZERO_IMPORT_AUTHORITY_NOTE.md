# y_t Lane: Zero-Import Authority

**Date:** 2026-04-15
**Status:** DERIVED with explicit systematic authority surface (zero external observables)
**Primary runners:** `scripts/frontier_yt_color_projection_correction.py`,
`scripts/frontier_yt_explicit_systematic_budget.py`
**Supporting runners:** `scripts/frontier_yt_exact_interacting_bridge_transport.py`,
`scripts/frontier_yt_microscopic_schur_class_admissibility.py`,
`scripts/frontier_yt_boundary_consistency.py`,
`scripts/frontier_yt_eft_bridge.py`,
`scripts/frontier_yt_2loop_chain.py` (historical support route)

## Authority role

This is the canonical authority note for the zero-import
renormalized `y_t` lane on `main`.

Use this note together with:

- [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md)
- [YT_EFT_BRIDGE_THEOREM.md](./YT_EFT_BRIDGE_THEOREM.md)
- [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md)
- [YT_GAUGE_CROSSOVER_THEOREM.md](./YT_GAUGE_CROSSOVER_THEOREM.md)
- [YT_FLAGSHIP_BOUNDARY_NOTE.md](./YT_FLAGSHIP_BOUNDARY_NOTE.md)

Do not treat older closure or route-history notes as competing authority.

**2026-04-15 authority correction:** the older zero-import 2-loop route
(`y_t(v) = 0.973`, `m_t = 169.4 GeV`) remains useful route history, but it is
not the final quantitative posture of the current package. The current live
boundary is narrower:

- the accepted central route is `y_t(v) = 0.9176`
- the lane is now best read as `DERIVED with explicit systematic`
- the current package-native bridge budget is narrower than the older fallback:
  `1.2147511%` conservative and `0.75500635%` support-tight around the local
  selector, under the forced-UV transport hypotheses
- there is no practical direct-lattice bypass on accessible lattices

## Current strongest package read

| Observable | Framework result | Comparator | Deviation |
|---|---|---|---|
| `y_t(v)` | `0.9176` | `~0.917` | `+0.06%` |
| `m_t(pole)` 2-loop | `172.57 GeV` | `172.69 GeV` | `-0.07%` |
| `m_t(pole)` 3-loop | `173.10 GeV` | `172.69 GeV` | `+0.24%` |

These are the current strongest zero-SM-import central values on the
renormalized `y_t` lane.

## Safe claim

The current package can safely say:

- the lattice-scale Yukawa-to-gauge ratio is exact
- the low-energy `y_t` endpoint is a zero-import derived central value
- the current `m_t` central values are very near observation
- the lane now carries an explicit residual bridge systematic from the
  package-native forced-UV transport law: `1.2147511%` conservative,
  `0.75500635%` support-tight on the current package support stack

The package cannot yet say that the renormalized `y_t` lane is unbounded.

## Why the lane stays systematic-limited

One real systematic-limited step remains:

1. the low-energy endpoint still uses the backward-Ward bridge
2. that bridge uses the SM RGE as the perturbative surrogate for the true
   lattice blocking flow over `v -> M_Pl`
3. the current package bridge stack narrows the live endpoint budget to
   `1.2147511%` conservative (`0.75500635%` support-tight), closes the broad
   scanned constructive family at the intrinsic UV-centered class level, but
   does not yet remove the surrogate transport law or prove the exact
   microscopic bridge beyond the proxy family

So the lane is materially stronger than before. On the current package it is now a
derived quantitative lane with explicit systematic, not an unbounded one.
