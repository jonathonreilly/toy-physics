# IF Decoherence Program: Closing Note

**Date:** 2026-04-01
**Status:** Closed for uniform random DAGs. Topology pivot next.

## Retained framework

The **Influence Functional (IF)** is the retained decoherence framework.
It is validated: hermiticity (3.6e-16), baseline (alpha=0 -> purity 1.0),
partial equivalence with slot-resolved bitstring env (Delta=0.033).
The IF kernel structure K = prod_encounters cos(alpha * Delta_obs) is
algebraically clean and physically motivated.

## What the experiments showed

14 architectures tested. Two reached correct scaling direction briefly:

| Architecture | Mechanism | Best result | Failure mode |
|---|---|---|---|
| AFC (amplitude field coherence) | scalar K from phase overlap | |K| drops 0.999->0.91 | single scalar can't mix enough |
| CL bath (Caldeira-Leggett y-bins) | D = exp(-lambda^2 * S) | decoh grows N=12->18 | pur_min reversal at N=25 |

All others (node labels, action bins, evolving phase, edge records,
directional angles, tensor envs, neighborhood fingerprints) fail the
same way: CLT concentration of amplitude-weighted distributions.

## The geometric ceiling

On uniform random DAGs, both single-slit detector distributions converge:

```
pur_min (maximally decohered purity):
  N=12: 0.9899
  N=18: 0.9506  <-- brief dip (best decoherence window)
  N=25: 0.9860  <-- rebounds toward 1
```

Root cause: path multiplicity grows exponentially with depth.
By N=25, both slits have paths reaching every detector node from
every direction with similar amplitude-weighted statistics.
The CLT guarantees this convergence for ALL fixed-dimensional
observables on these graphs.

This is a property of the **graph family**, not the bath design.
No kernel, observable, or coupling strength can escape it on
uniform random DAGs.

## What is NOT ruled out

The IF framework itself is fine. The bottleneck is the geometry.
Three escape routes remain:

1. **Non-uniform graph topology** — hierarchical, modular, or
   scale-free families where slit paths remain structurally
   separated as N grows. (Next step.)

2. **Irreversible collapse** — measurement-like projection at
   mass nodes, breaking linearity of the path sum.

3. **Nonlinear propagator** — breaks CLT but likely breaks
   Born rule too.

## Decision

Test topology first (option 1). Keep the propagator, IF kernel,
and CL bath machinery fixed. Change only the graph generator.
Primary metric: does pur_min stay bounded away from 1 as N grows?
