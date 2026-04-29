# y_t Lane: Zero-Import Authority

**Date:** 2026-04-17
**Status:** DERIVED quantitative authority surface (zero external observables)
**Primary runners:** `scripts/frontier_yt_ward_identity_derivation.py`,
`scripts/frontier_yt_color_projection_correction.py`
**Supporting runners:** `scripts/frontier_yt_explicit_systematic_budget.py`,
`scripts/frontier_yt_exact_interacting_bridge_transport.py`,
`scripts/frontier_yt_boundary_consistency.py`,
`scripts/frontier_direct_yt_extraction.py`

## Authority role

This is the canonical authority note for the zero-import renormalized `y_t`
lane on `main`.

Use this note together with:

- [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](./YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- `YT_FLAGSHIP_BOUNDARY_NOTE.md`
- [YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md](./YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md)

Do not treat older backward-Ward / route-history notes as competing authority.

## Current strongest package read

| Observable | Framework result | Comparator | Deviation |
|---|---|---|---|
| `y_t(v)` | `0.9176` | `~0.917` | `+0.06%` |
| `m_t(pole)` 2-loop | `172.57 GeV` | `172.69 GeV` | `-0.07%` |
| `m_t(pole)` 3-loop | `173.10 GeV` | `172.69 GeV` | `+0.24%` |

These are the current strongest zero-external-observable central values on the
renormalized `y_t` lane.

## Safe claim

The current package can safely say:

- the lattice-scale Yukawa-to-gauge ratio is exact on the canonical surface:
  `y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)`
- the physical low-energy Yukawa is the Ward value times the derived
  color-projection factor `sqrt(8/9)`
- the low-energy `y_t` endpoint and the current `m_t` values are derived
  central values with zero external SM observables on the framework side
- the current precision caveat on the primary path is a standard-method
  residual budget, dominated by lattice-to-continuum 1-loop matching at the
  Planck interface plus standard SM RGE truncation, of order `~1.95%`
- the older Schur-coarse-bridge budget
  `1.2147511%` conservative / `0.75500635%` support-tight remains valid as an
  independent bridge-path cross-check, not as the load-bearing package
  qualifier on the primary lane

The package still cannot say that the renormalized `y_t` lane is a fully
framework-internal retained theorem from `M_Pl` to `v`.

## Why the lane is no longer carried by a framework-native explicit systematic

The live primary path is now:

1. exact lattice-scale Ward theorem on the retained theory
2. derived color projection `sqrt(8/9)`
3. standard lattice-to-continuum matching at the `M_Pl` interface
4. standard SM RGE running from `M_Pl` to `v`
5. standard pole-mass conversion

The remaining quantitative limitation is therefore not a framework-native
bridge systematic. It is the ordinary residual one would quote on any lattice
gauge-theory route that matches a lattice boundary condition onto the
continuum:

- sub-permille input precision on `g_s(M_Pl)` from the same-surface plaquette
  chain
- standard SM RGE truncation at the few-per-mille level
- standard lattice 1-loop matching at the `M_Pl` interface, which dominates
  the current budget

That leaves the lane as a **derived quantitative lane** rather than a
retained theorem-grade UV-to-IR closure.

## What the Schur-bridge stack becomes

The Schur-coarse-bridge program is not retracted. It remains useful and
nontrivial:

- it gives an independent route from the lattice Ward boundary toward the same
  low-energy endpoint
- its higher-order and nonlocal tails remain a real quantified bridge-path
  budget
- agreement of that bridge path with the Ward-primary path is a meaningful
  cross-check on the framework

But those bridge tails are no longer the package's load-bearing reason to mark
the primary YT lane as explicit-systematic.

## Honest boundary

The current package does **not** claim:

- a fully framework-internal continuum-limit theorem on this specific
  composite-Higgs Wilson-staggered surface
- a theorem-grade elimination of all UV-to-IR transport residuals
- a practical direct-lattice bypass that measures `y_t(v)` on accessible
  lattices

So the right read is:

> the exact lattice-scale Yukawa/gauge normalization is retained, the
> renormalized low-energy `y_t` / `m_t` lane is derived with zero external SM
> observables on the framework side, the current primary precision caveat is a
> standard-method residual budget of order `~1.95%`, and the older Schur
> bridge survives as an independent cross-check with its own tighter but
> route-specific budget.
