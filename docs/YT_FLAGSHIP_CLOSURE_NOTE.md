# y_t Flagship Boundary Note

## Authority Notice

This note is a **supporting boundary note**, not the sole lane authority.

For current branch decisions, read it together with:

- [YT_ZERO_IMPORT_CLOSURE_NOTE.md](./YT_ZERO_IMPORT_CLOSURE_NOTE.md)
- [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md)
- [RENORMALIZED_YT_PAPER_NOTE.md](./RENORMALIZED_YT_PAPER_NOTE.md)

Its purpose is narrower: say exactly what remains bounded in the live `y_t`
lane after the recent cleanup and direct-extraction audit.

**Date:** 2026-04-15
**Status:** BOUNDED
**Current central value:** `y_t(v) ~= 0.918`, implying `m_t(pole) ~= 172.6 GeV`
at the current accepted conversion order

---

## Final reviewer answer

The current `y_t` lane is best described as:

- **zero external SM observables**
- **derived central value**
- **bounded by an inherited `~3%` systematic from the backward-Ward / QFP
  surrogate above `v`**

That is the honest final boundary on this branch today.

## What is exact

These parts of the `y_t` lane are not the live blocker:

1. `y_t / g_s = 1 / sqrt(6)` from the Cl(3) trace identity
2. `G_5` centrality in Cl(3), giving lattice-scale ratio protection
3. the derivation of the SM gauge group and matter content
4. the use of SM beta coefficients as consequences of that derived field content
5. the hierarchy / electroweak matching scale `v`

Those pieces explain why the lane is predictive at all.

## What is still bounded

One real bounded step remains.

### The bounded step

The low-energy `y_t(v)` value is obtained by transferring the lattice Ward
boundary condition through the backward-Ward route. That route uses the SM RGE
as the perturbative surrogate for the true lattice blocking flow over the full
`v -> M_Pl` interval.

The QFP insensitivity result bounds the error from this surrogate at about
`~3%`. That bound is real and propagates to the physical top mass.

### What the bound means

- the central value can still be very strong
- the lane is still zero-import
- but the exact numerical closure is not yet unbounded

The right read is:

- `y_t(v)`: derived central value, bounded at `~3%`
- `m_t(pole)`: derived central value, inherits the same bounded systematic

## Direct-lattice bypass audit

The obvious way to remove the bound would be to avoid the backward-Ward
surrogate entirely and measure `y_t(v)` directly on the lattice.

That route was checked in
[scripts/frontier_direct_yt_extraction.py](../scripts/frontier_direct_yt_extraction.py).

Current conclusion:

- direct response / vertex / susceptibility methods measure the Yukawa at the
  lattice scale, not at the low-energy endpoint `v`
- applying the Ward identity directly at `v` fails badly
- lattice-native step-scaling would in principle work, but it would require an
  absurdly large blocking range and is not feasible on accessible lattices

So the current branch does **not** have a practical direct-lattice bypass for
the backward-Ward route.

## Therefore

The current `y_t` lane is **not** blocked by a missing algebraic theorem.
It is blocked by a real but understood methodological systematic:

- the backward-Ward / QFP surrogate remains the minimal feasible bridge
- the resulting `~3%` systematic is the current irreducible bound on this branch

## Paper-safe claim

The honest branch-safe wording is:

> The framework derives the lattice-scale Yukawa-to-gauge ratio exactly and
> propagates it to low energy with zero external SM observables. The current
> low-energy `y_t` and `m_t` central values are strong and near observation, but
> they retain an inherited `~3%` bounded systematic because the backward-Ward
> continuation uses the SM RGE as the practical surrogate for the true lattice
> blocking flow above `v`.

## Cannot claim

Do not claim any of the following from this branch today:

- that the `y_t` lane is fully unbounded
- that the backward-Ward surrogate has been bypassed
- that direct lattice extraction already delivers `y_t(v)` on accessible lattices
- that the `~3%` QFP / backward-Ward systematic has disappeared

## Why this still matters

The bound is now as narrow as we know how to make it without a genuinely new
low-energy `y_t` route:

- no external SM observable is used as an input
- the central value remains close to observation
- the remaining uncertainty is explicit, localized, and method-specific

That is a much stronger posture than “`y_t` is still vague or open.”
