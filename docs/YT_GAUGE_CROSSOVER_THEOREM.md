# Gauge Crossover Theorem: Import-Allowed Companion For `y_t`

**Date:** 2026-04-15
**Status:** bounded companion theorem
**Primary runner:** `scripts/frontier_yt_gauge_crossover_theorem.py`

## Authority Role

This note is the numerically stronger import-allowed companion to the current
zero-input `y_t` package.

It is not the primary zero-input authority. Use it together with:

- [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](./YT_ZERO_IMPORT_AUTHORITY_NOTE.md)
- [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md)

## Safe Statement

The current one-shot lattice-to-`MSbar` crossover companion gives:

- `m_t = 171.0 GeV`
- residual about `-1.1%` against the comparison value

This is the strongest current import-allowed top-mass route on `main`.

## Why This Stays Bounded

The route is not zero-input. It still depends on:

- perturbative scheme conversion from the lattice-side coupling to `MSbar`
- imported matching coefficients in that crossover
- perturbative running below the crossover surface

So the current package keeps it as a bounded companion rather than as a
retained theorem.

## What The Theorem Establishes

The current note supports three narrower claims:

1. a one-shot crossover map from the lattice-side gauge surface to the
   low-energy `MSbar` companion route
2. preservation of the protected Yukawa/gauge ratio on the physical-taste
   companion route
3. a numerically stronger top-mass companion than the current zero-input route

## Validation Snapshot

`frontier_yt_gauge_crossover_theorem.py` is the current supporting runner.

Current package headline:

- `m_t = 171.0 GeV`
- perturbative matching band remains explicit
