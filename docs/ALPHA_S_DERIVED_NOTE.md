# `alpha_s(M_Z)` Promoted Zero-Import Authority

**Date:** 2026-04-15
**Status:** promoted quantitative lane on `main`
**Primary runners:** `scripts/frontier_yt_zero_import_chain.py`,
`scripts/frontier_alpha_s_determination.py`

## Authority Role

This note records the standalone strong-coupling lane used on the current
`main` package surface.

The current package treats `alpha_s(M_Z)` as its own promoted quantitative
lane, not merely as a hidden subcomponent of a larger synthesis memo.

## Safe Statement

The current zero-input lane gives:

- `alpha_s(v) = alpha_bare / u_0^2 = 0.1033`
- one-decade low-energy transfer from `v` to `M_Z`
- `alpha_s(M_Z) = 0.1181`

That is the current promoted zero-input `alpha_s` result on `main`.

## Canonical Chain

```
Cl(3) on Z^3
  |-> g_bare = 1
  |-> <P> = 0.5934
  |-> u_0 = <P>^(1/4)
  |
  |-> hierarchy theorem:
  |     alpha_LM = alpha_bare / u_0
  |     v = 245.080424447914 GeV
  |
  |-> vertex-power theorem:
        alpha_s(v) = alpha_bare / u_0^2 = 0.1033
  |
  |-> low-energy transfer:
        alpha_s(M_Z) = 0.1181
```

## Package Role

This is a promoted quantitative lane, not a retained theorem-core row.

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
- `frontier_alpha_s_determination.py`
