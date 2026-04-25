# Staggered Graph Observables Backreaction Stress Note

**Date:** 2026-04-24  
**Script:** `scripts/frontier_staggered_graph_observables_backreaction_stress.py`  
**Status:** source-sector positive / gauge-current obstruction on stress graphs

## Question

The graph-observables backlog had one natural P2 after the larger portability
stress run:

> add a backreaction version only after the retained observables are stable on
> the current portability families.

This note freezes that backreaction version on the larger stress graphs.  It
does not modify the canonical staggered card or the baseline portability
harnesses.

## Harness

The graph families are inherited from
`frontier_staggered_graph_portability_stress.py`:

- bipartite random-geometric stress, `n = 81`
- bipartite growing stress, `n = 82`
- bipartite chorded-grid stress, `n = 144`
- layered bipartite DAG stress, `n = 66`

The imposed depth potential is replaced by the retained graph-native
resistance-Yukawa source sector:

```text
Phi = K rho,
K_ij = exp(-1.50 R_eff(i,j)) / (R_eff(i,j) + 0.10),
```

where `R_eff` is the weighted effective-resistance distance on the graph.

The retained rows are source-sector rows:

- zero-source exactness
- norm preservation
- endogenous force sign
- source-response linearity
- two-body field additivity
- achromatic force
- robustness over probe momenta
- native gauge/current when cycles exist

Centroid/depth shift and shell bias are reported as secondary diagnostics only.

## Exact Results

| Family | n | Edges | Cycle | Rows | Source force | Source R2 | Two-body | Achrom CV | Robust | Gauge | Depth shift | Shell bias |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| random-geometric stress | 81 | 178 | yes | `7/8` | `+9.875e-01` | `0.9960` | `1.90e-16` | `3.92e-02` | `3/3` | `6.262e-10` FAIL | `+1.596e-01` | `-3.491e-01` |
| growing stress | 82 | 191 | yes | `8/8` | `+8.891e-01` | `0.9949` | `1.37e-16` | `4.95e-02` | `3/3` | `1.293e-02` PASS | `+3.415e-01` | `-3.333e-01` |
| chorded-grid stress | 144 | 407 | yes | `7/8` | `+1.170e+00` | `0.9981` | `1.35e-16` | `3.11e-02` | `3/3` | `3.497e-10` FAIL | `+1.750e-01` | `-3.900e-01` |
| layered DAG stress | 66 | 65 | no | `8/8` | `+1.856e+00` | `0.9997` | `1.43e-16` | `1.62e-02` | `3/3` | `N/A` | `+3.925e-02` | `-5.567e-01` |

## Readout

All non-gauge source-sector rows pass on all four stress families:

- zero-source exactness is machine-clean
- norm stays machine-clean
- the endogenous force is TOWARD in every family
- source-response linearity stays above `R2 = 0.9949`
- two-body field additivity is at machine precision
- achromatic force stays below the `0.05` CV threshold
- robustness is `3/3` on every family

The obstruction is specific:

> once the resistance-Yukawa field is active, native gauge/current fails on two
> of the three cycle-bearing stress families.

This is not a force-observable failure.  It is a current-compatibility failure
under the active endogenous source sector.

## Interpretation

This advances the graph-observables backlog but does not close it completely.

Positive result:

- the force/source half of the observable split transfers cleanly to the
  backreaction stress setting
- the layered DAG holdout remains clean with gauge correctly marked `N/A`

Negative result:

- current/gauge is not automatically compatible with the resistance-Yukawa
  source field on larger cycle-rich graphs
- future backreaction cards should not promote force/current jointly unless
  the gauge row is tested under the active source field, not only on the free
  transport Hamiltonian

## Boundary

Retain this as a partial closure:

- **closed:** backreacted source-sector force rows on the stress families
- **open:** gauge/current compatibility under active endogenous source fields

The next honest target is not another force retune.  It is either a
source-field construction that preserves native current response on
cycle-bearing stress graphs, or a sharper theorem separating force rows from
gauge/current rows in backreacted graph-native cards.

## Successor Update

[`STAGGERED_BACKREACTION_ACTIVE_GAUGE_EDGE_SELECTION_NOTE_2026-04-24.md`](./STAGGERED_BACKREACTION_ACTIVE_GAUGE_EDGE_SELECTION_NOTE_2026-04-24.md)
shows that the active-field gauge failure above is an edge-selection artifact
of the inherited DFS cycle edge.  With a source-proximal non-bridge flux edge,
the active-field gauge row passes `3/3` on the cycle-bearing stress graphs.
Keep the table above as the frozen negative control for arbitrary cycle-edge
selection, not as the final active-field gauge verdict.
