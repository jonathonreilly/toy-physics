# `alpha_s(M_Z)` Retained Same-Surface-Derived Authority

**Date:** 2026-04-15
**Status:** retained quantitative lane on `main`
**Primary derivation runner:** `scripts/frontier_yt_zero_import_chain.py`
**Current package carrier:** `scripts/frontier_complete_prediction_chain.py`
**Historical support runner:** `scripts/frontier_alpha_s_determination.py`

## Authority Role

This note records the standalone strong-coupling lane used on the current
`main` package surface.

The current package treats `alpha_s(M_Z)` as its own retained quantitative
lane, not merely as a hidden subcomponent of a larger synthesis memo.

## Safe Statement

The current retained lane gives:

- `alpha_s(v) = alpha_bare / u_0^2 = 0.1033`
- `alpha_LM^2 = alpha_bare * alpha_s(v)` as an exact retained
  coupling-chain identity
- one-decade low-energy transfer from `v` to `M_Z` on the retained running
  bridge
- `alpha_s(M_Z) = 0.1181`

That is the current retained same-surface-derived `alpha_s` result on `main`.

## Canonical Chain

```
Cl(3) on Z^3
  |-> g_bare = 1
  |-> <P> = 0.5934  (same-surface evaluated; see plaquette self-consistency)
  |-> u_0 = <P>^(1/4)
  |
  |-> hierarchy theorem:
  |     alpha_LM = alpha_bare / u_0
  |     v = 246.282818290129 GeV
  |
  |-> vertex-power theorem:
        alpha_s(v) = alpha_bare / u_0^2 = 0.1033
        alpha_LM^2 = alpha_bare * alpha_s(v)
  |
  |-> low-energy transfer:
        alpha_s(M_Z) = 0.1181
```

## Package Role

This is a retained standalone quantitative lane, not a theorem-core row.
Its quantitative anchor is the canonical same-surface plaquette evaluation in
[PLAQUETTE_SELF_CONSISTENCY_NOTE.md](PLAQUETTE_SELF_CONSISTENCY_NOTE.md).

The framework-side quantity is `alpha_s(v)`. The quoted `alpha_s(M_Z)` row is
the same lane after the retained one-decade running bridge below `v`.

It remains distinct from:

- the retained hierarchy / `v` lane
- the EW normalization lane
- the Yukawa / top lane
- the Higgs / vacuum lane

## Validation Snapshot

- current zero-input route:
  `alpha_s(M_Z) = 0.1181`
- comparison value:
  `0.1179`
- deviation:
  `+0.2%`

Primary reruns on the current package surface:

- `frontier_yt_zero_import_chain.py`
- `frontier_complete_prediction_chain.py`

Historical support, not canonical authority:

- `frontier_alpha_s_determination.py`
