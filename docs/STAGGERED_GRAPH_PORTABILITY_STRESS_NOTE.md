# Staggered Graph Portability Stress Note

**Status:** retained stress checkpoint

This note freezes the first larger-size / more irregular stress run for the
staggered / Kahler-Dirac portability probe.

## Question

Does the retained staggered force battery survive when the graphs are larger,
less regular, and more cycle-rich than the baseline portability families?

## Harness

- Script: [`frontier_staggered_graph_portability_stress.py`](../scripts/frontier_staggered_graph_portability_stress.py)
- Battery: Born/linearity, norm, force sign, `F∝M`, achromatic force,
  equivalence, robustness, gauge if cycles exist

## Stress Run

| Family | n | |E| | cycle | Born/linearity | norm | force | F∝M | achrom CV | equiv CV | robust | gauge |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| bipartite random geometric stress | 81 | 178 | yes | `6.49e-16` | `0.00e+00` | `+3.412e-03` TOWARD | `1.000` | `1.271e-16` | `1.078e-16` | `3/3` | `6.184e-04` PASS |
| bipartite growing stress | 82 | 191 | yes | `7.71e-16` | `1.11e-16` | `+3.275e-03` TOWARD | `1.000` | `2.369e-16` | `1.589e-16` | `3/3` | `1.869e-03` PASS |
| bipartite chorded grid stress | 144 | 407 | yes | `8.87e-16` | `0.00e+00` | `+3.707e-03` TOWARD | `1.000` | `0.000e+00` | `1.719e-16` | `3/3` | `1.175e-04` PASS |
| layered bipartite DAG stress | 66 | 65 | no | `4.38e-16` | `4.44e-16` | `+4.429e-03` TOWARD | `1.000` | `2.477e-16` | `1.175e-16` | `3/3` | `N/A` |

## Readout

- The retained staggered force battery survives the larger, more irregular
  bipartite families.
- The cycle-bearing stress families still show native gauge response.
- The acyclic layered family stays acyclic, and gauge is correctly skipped.
- No retained-row failure appeared in this stress run.

## Caveat

This is a stress checkpoint, not a new canonical card. It strengthens the
portability claim, but it does not replace the canonical force-based staggered
card or the full-suite baseline.
