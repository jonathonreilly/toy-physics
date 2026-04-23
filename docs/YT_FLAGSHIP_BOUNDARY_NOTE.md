# y_t Flagship Boundary Note

## Authority Notice

This note is a **supporting boundary note**, not the sole lane authority.

For current package decisions, read it together with:

- [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](./YT_ZERO_IMPORT_AUTHORITY_NOTE.md)
- [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](./YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md](./YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md)

Its purpose is narrower: state the honest current claim boundary of the live
`y_t` lane after the Ward theorem promotion and the YT-lane authority update.

**Date:** 2026-04-17
**Status:** DERIVED quantitative lane
**Current central values:** `y_t(v) = 0.9176`, canonical
`m_t(pole) = 173.10 GeV` (3-loop), with retained `172.57 GeV` (2-loop)
support

---

## Final reviewer answer

The current `y_t` lane is best described as:

- **zero external SM observables on the framework side**
- **exact retained lattice-scale Ward theorem**
- **derived low-energy central values**
- **standard-method residual budget on the primary path, currently of order
  `~1.95%`**

That is the honest current boundary on the package.

## What is exact

These parts of the `y_t` lane are no longer the remaining blocker:

1. the canonical-surface Ward theorem
   `y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)`
2. the same-surface `alpha_s` / `g_s(M_Pl)` input from the plaquette chain
3. the color-singlet projection factor `sqrt(8/9)` that turns the Ward value
   into the physical low-energy Yukawa route
4. the hierarchy / electroweak matching scale `v`
5. the direct framework-side Higgs/top numerical readout once the accepted
   low-energy Yukawa is supplied

Those pieces explain why the lane is predictive at all.

## What remains limited

The remaining limitation is no longer a framework-native exact-bridge
systematic on the primary path.

The live primary route is:

- exact Ward theorem at the lattice scale
- derived color projection
- standard lattice-to-continuum matching at the `M_Pl` interface
- standard SM running from `M_Pl` to `v`
- standard pole-mass conversion

So the current caveat is the ordinary precision caveat of that route:

- sub-permille same-surface input uncertainty on `g_s(M_Pl)`
- standard SM RGE truncation
- standard lattice 1-loop matching at the UV interface, which dominates

On the current package, this gives a primary residual budget of order
`~1.95%`. That is not being claimed as a framework-internal theorem; it is the
standard-method budget carried by the current live route.

## What happens to the bridge stack

The Schur-coarse-bridge program remains real and useful, but its role changes.

It is now an **independent cross-check path**:

- its higher-order and nonlocal tails remain quantified
- its endpoint budget
  `1.2147511%` conservative / `0.75500635%` support-tight remains valid
- agreement of that bridge path with the Ward-primary path is a meaningful
  consistency check

But that bridge budget is no longer the package's load-bearing reason to mark
the primary YT lane as explicit-systematic.

## Direct-lattice bypass audit

The direct-lattice bypass audit still matters, but its role is narrower.

Current conclusion:

- direct response / vertex / susceptibility methods measure the Yukawa at the
  lattice scale, not directly at `v`
- applying the Ward identity directly at `v` fails
- lattice-native step-scaling would require an infeasible blocking range on
  accessible lattices

So the current package still does **not** have a practical direct-lattice
measurement of `y_t(v)`. The accepted route remains one that passes through a
continuum matching/running layer.

## Paper-safe claim

The honest paper-safe wording is:

> The framework derives the lattice-scale Yukawa-to-gauge ratio exactly on the
> canonical surface and propagates it to low energy with zero external SM
> observables on the framework side. The current `y_t` and `m_t` central
> values are strong and near observation. The remaining precision caveat on
> the primary route is carried as standard lattice-to-continuum matching plus
> standard SM running residuals, not as a framework-native explicit bridge
> systematic. The older Schur bridge survives as an independent cross-check
> with its own tighter route-specific residual budget.

## Cannot claim

Do not claim any of the following from the current package:

- that the `y_t` lane is fully retained from `M_Pl` to `v`
- that a framework-internal continuum-limit theorem on this exact composite
  surface has been proved
- that direct lattice extraction already delivers `y_t(v)` on accessible
  lattices
- that the Schur bridge is worthless or obsolete rather than a real
  cross-check

## Why this still matters

The YT lane is materially stronger than the old bounded or
explicit-systematic read:

- no external SM observable is used as an input on the framework side
- the lattice-scale Yukawa/gauge normalization is exact and retained
- the low-energy route is explicit, numerically successful, and packaged on
  one authority surface
- the remaining precision caveat is now standard-method rather than a
  framework-native bridge qualifier

That is the right current flagship boundary.
