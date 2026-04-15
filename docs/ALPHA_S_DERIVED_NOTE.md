# `alpha_s(M_Z)` Zero-Import Authority On The Current `y_t` Package

**Date:** 2026-04-15
**Status:** bounded quantitative support on an open lane
**Primary runners:** `scripts/frontier_alpha_s_determination.py`,
`scripts/frontier_yt_2loop_chain.py`

## Authority Role

This note records the current strongest zero-input strong-coupling route used
inside the bounded renormalized `y_t` package.

Use it together with:

- [YT_ZERO_IMPORT_CLOSURE_NOTE.md](./YT_ZERO_IMPORT_CLOSURE_NOTE.md)
- [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md)
- [YT_EFT_BRIDGE_THEOREM.md](./YT_EFT_BRIDGE_THEOREM.md)
- [YT_VERTEX_POWER_DERIVATION.md](./YT_VERTEX_POWER_DERIVATION.md)

Do not read this file as permission to promote the entire `y_t` lane. The
package still keeps the low-energy transfer bounded.

## Safe Statement

The current zero-input route gives:

- `alpha_s(v) = alpha_bare / u_0^2 = 0.1033`
- one-decade low-energy transfer from `v` to `M_Z`
- `alpha_s(M_Z) = 0.1181`

That is the strongest current zero-input `alpha_s` number on `main`.

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

## Why The Package Still Keeps This Bounded

The operator-level `u_0^2` dressing is a closed subderivation, but the package
still treats the full low-energy `alpha_s` / `y_t` transfer stack as one open
bounded lane because:

1. the low-energy bridge is still packaged as bridge-conditioned rather than
   as one theorem-grade same-surface closure
2. the same transfer infrastructure also feeds the bounded top-mass lane
3. the package still distinguishes a zero-input route from an import-allowed
   companion route

So the number is strong and publication-relevant, but the package does not yet
promote it as a retained flagship theorem.

## Validation Snapshot

- current zero-input route:
  `alpha_s(M_Z) = 0.1181`
- comparison value:
  `0.1179`
- deviation:
  `+0.2%`

Primary reruns:

- `frontier_alpha_s_determination.py`
- `frontier_yt_2loop_chain.py`
