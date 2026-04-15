# y_t Gate: Bounded Zero-Import Authority

**Date:** 2026-04-15
**Status:** BOUNDED authority surface (zero external observables)
**Primary runner:** `scripts/frontier_yt_2loop_chain.py`
**Supporting runners:** `scripts/frontier_yt_boundary_consistency.py`,
`scripts/frontier_yt_eft_bridge.py`,
`scripts/frontier_alpha_s_determination.py`

## Authority role

This is the canonical bounded authority note for the zero-import
renormalized `y_t` lane on `main`.

Use this note together with:

- [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md)
- [YT_EFT_BRIDGE_THEOREM.md](./YT_EFT_BRIDGE_THEOREM.md)
- [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md)
- [YT_GAUGE_CROSSOVER_THEOREM.md](./YT_GAUGE_CROSSOVER_THEOREM.md)

Do not treat older closure or route-history notes as competing authority.

## Current strongest bounded quantitative route

| Observable | Framework result | Comparator | Deviation |
|---|---|---|---|
| `v` | `246.3 GeV` | `246.22 GeV` | `+0.03%` |
| `\alpha_s(M_Z)` | `0.1181` | `0.1179` | `+0.2%` |
| `m_t` (zero-import 2-loop route) | `169.4 GeV` | `172.69 GeV` | `-1.9%` |

These are the current strongest bounded zero-input numbers on the open
renormalized `y_t` gate. They are publication-relevant, but they are not yet
promoted into the retained flagship core.

## Safe claim

The current package can safely say:

- the electroweak hierarchy theorem fixes `v` without electroweak input
- the coupling-map / vertex-power stack gives a strong bounded zero-input
  route to `\alpha_s(M_Z)`
- the zero-import 2-loop chain gives a strong bounded route to
  `m_t = 169.4 GeV`
- the import-allowed crossover companion gives a numerically stronger but
  explicitly imported route near `171.0 GeV`

The package cannot yet say that the renormalized `y_t` lane is closed.

## Canonical chain

```
Cl(3) on Z^3
  |-> g_bare = 1                              [framework normalization]
  |-> <P> = 0.5934                            [computed plaquette]
  |-> u_0 = <P>^(1/4) = 0.8776               [mean-field link]
  |
  |-> hierarchy theorem:
  |     alpha_LM = alpha_bare/u_0
  |     v = 246.3 GeV
  |
  |-> coupling-map / vertex route:
  |     alpha_s(v) = alpha_bare/u_0^2 = 0.1033
  |     alpha_s(M_Z) = 0.1181
  |
  |-> boundary + bridge stack:
        y_t(M_Pl) = g_lattice/sqrt(6) = 0.436
        v is the physical crossover endpoint
        backward Ward transfer selects y_t(v) = 0.973
        m_t = y_t(v) * v/sqrt(2) = 169.4 GeV
```

## Why the lane stays bounded

The current blocker is no longer a vague “matching-band” objection. It is
narrower and more specific:

1. the package still treats the low-energy bridge as bridge-conditioned rather
   than as one theorem-grade same-surface closure
2. the zero-import route still uses perturbative SM EFT running as the current
   transfer infrastructure below the lattice theory
3. the package still carries two bounded quantitative readings:
   the zero-import 2-loop route and the import-allowed crossover companion

So the lane is materially stronger, but it is still a live gate.

## Current bounded readings

### A. Zero-import bounded route

- authority:
  [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md),
  [YT_EFT_BRIDGE_THEOREM.md](./YT_EFT_BRIDGE_THEOREM.md),
  [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md)
- runner:
  `scripts/frontier_yt_2loop_chain.py`
- headline:
  `\alpha_s(M_Z) = 0.1181`, `m_t = 169.4 GeV`

### B. Import-allowed bounded companion

- authority:
  [YT_GAUGE_CROSSOVER_THEOREM.md](./YT_GAUGE_CROSSOVER_THEOREM.md)
- runner:
  `scripts/frontier_yt_gauge_crossover_theorem.py`
- headline:
  `m_t = 171.0 GeV`

This companion is useful because it is numerically stronger. It is not the
zero-input authority.

## Historical routes not to use as primary authority

Do not route reviewers through:

- old `184 GeV` Planck-boundary narratives
- earlier 1-loop zero-import route notes
- older closure packets that mix bounded subresults with stronger claims than
  the current package accepts

Those can remain in repo history, but they are not the current authority
surface.

## Honest remaining work

To unfreeze this lane from the bounded portfolio into a promoted theorem-grade
surface, the package still needs:

- one single same-surface low-energy bridge authority that the package is
  willing to treat as fully internal rather than bridge-conditioned
- a final canonical quantitative route with no parallel authority ambiguity
- final package wording that no longer needs to distinguish zero-import and
  import-allowed bounded companions as separate live readings
