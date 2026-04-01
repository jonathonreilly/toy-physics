# Assumption / Derivation Ledger

**Status:** reviewer-facing framing document  
**Date:** 2026-04-01

## Purpose

This project is strongest when it is explicit about which ingredients are:

- **assumed**
- **motivated but not derived**
- **numerically retained**
- **still open**

This ledger is meant to make that separation harder to blur in future writeups.

## Current ledger

| ingredient | current status | what is actually true now |
|---|---|---|
| Discrete event-network ontology | **assumed** | The primitive substrate is still a graph/event picture motivated by the axioms, not derived from a deeper theory. |
| Persistent patterns / matter-like sources | **assumed + explored** | Persistent CA-style patterns are designed and then studied systematically. The repo has real retention studies here, but not a derivation of the rule family from deeper dynamics. |
| Delay-field / relaxation law | **assumed + numerically retained** | The field law is chosen and then pressure-tested. Its consequences are real within the toy, but the law is not derived from graph growth or from a deeper dynamical principle yet. |
| Complex amplitudes | **assumed** | The project still assumes complex-valued path amplitudes. This is explicitly not derived from the event-network ontology yet. |
| Action-proportional phase | **assumed + comparatively tested** | The phase depends on a chosen action-like quantity. Competing action choices have been compared, but the retained form is still selected rather than derived. |
| Geometry-only attenuation `1/L^p` | **selected + numerically retained** | This is the current retained unitary core because it fixes the gravity sign while preserving Born/interference. It is not yet a unique derivation from the axioms. |
| Directional path measure `exp(-0.8θ²)` | **provisional retained effective law** | This is the current lead unitary improvement. It passes the current tested unitary guards, but it is still an empirically retained path-measure correction rather than a derived theorem. |
| Born / pairwise interference package | **numerically retained** | Within the current linear path-sum architecture, Born-style behavior and vanishing fixed-DAG Sorkin residual are strongly retained. This is a meaningful internal result, but not a foundational derivation of Born rule. |
| Gravity sign and phase-valley mechanism | **numerically retained + partly derived** | Wrong-sign antigravity from the older attenuation was identified and removed. The phase-valley picture and weak-coupling `k²` scaling are now analytically motivated inside the current toy. |
| Gravity distance law / `b`-dependence | **negative structural result inside the current linear architecture** | Attraction is retained across the higher-dimensional modular lanes, but fixed-mass 4D sweeps, propagator-power sweeps, fixed-mass locality shells, a bounded local saturation nonlinearity, and an induced/effective-distance readout all still give a flat/topological law rather than `1/b`. The remaining open lane is no longer a simple rescue tweak; it is analytic explanation or a deeper architecture change. |
| 3D transfer of the unitary package | **retained effective extension with caveats** | 3D now has a real higher-dimensional gravity/decoherence/Born story rather than only a smoke test, but the strict interference clause still depends on which visibility metric is used. |
| 4D transfer of the unitary/non-unitary package | **partly retained on the current modular family** | Dense modular 4D now supports strong large-`N` CL-bath decoherence and clean chokepoint Born-rule checks. A shared-worktree gravity harness also reaches near-Newtonian mass scaling under optimized parameters. The remaining caveats are strict visibility and generality across families/settings. |
| Decoherence as durable-record formation | **partly retained effective story** | The record-formation framing is now numerically supported on the gap-controlled modular family: the retained IF / CL route yields stable decoherence there. What is still open is dynamic emergence of the topology that makes those records effective. |
| Decoherence influence-functional route | **retained on one topology family, not yet generic law** | The IF / CL reduced-description route is no longer merely promising: it works on modular gap-controlled DAGs and supports the current non-unitary architecture. What is still missing is transfer beyond that family and a more endogenous derivation of the good topology. |
| Genuine evolving-network dynamics | **open** | The repo still does not have a fully satisfying dynamics-first implementation of Axiom 1. Failed feedback-based growth rules and the later asymptotic pruning failure sharpen the next step: the open lane is now hard-gap node placement / node-removal dynamics, not soft pruning of already connected graphs. |
| Continuum / asymptotic bridge | **partly closed** | 3D mass exponent converges to alpha~0.58 (spread 0.083) — proper continuum limit. 4D does NOT converge (spread > 0.3). Compact bridge note (CONTINUUM_BRIDGE_NOTE.md) separates what survives scaling from what doesn't. |
| Cross-family robustness | **retained on 4 of 5 families** | Gravity + decoherence work on modular, hierarchical, uniform, and hierarchical-leaky 3D DAGs. Only preferential attachment (hub_boost >= 2) fails gravity. No longer a single-family story. |
| Emergence dynamics | **bounded partial positive** | Adaptive quantile pruning creates emergent gap from uniform DAGs, improving decoherence by 5pp at N=30 and sustaining through N=60. Does not survive at N=80. Can also sustain an imposed gap through N=60. Asymptotic stability remains open. |
| Distance law closure | **structural negative, fully diagnosed** | b-independence confirmed across 9+ avenues (propagator power, density, locality shells, lattice, causal field, nonlinear phase, edge reweight, source-projected). Root cause derived: Laplacian field's graph-wide extent. Edge reweighting gives trivial 1/b (k=0 control proves it's amplitude routing, not gravity). |
| Prediction/falsification criteria | **documented** | PREDICTION_CARD.md lists 5 confirmed predictions, 5 falsification criteria, 4 distinguishing signatures. k=0 diagnostic is the key tool separating real from trivial gravity effects. |

## What this means

The honest current status is:

- the project has a **retained toy unitary architecture**
- it has a **retained non-unitary framework on one good topology family**
- but it does **not** yet derive its own core mathematics from a deeper evolving-network dynamics

So the best current claim is still:

- **toy mechanism science with increasingly disciplined retained structure**

not:

- **a finished derivation of gravity or quantum theory from first principles**

## Immediate use in writing

When writing papers, notes, or README summaries:

- call the directional path measure a **retained effective law** or **provisional unitary architecture**
- call the decoherence story a **retained topology-dependent reduced law with open emergence**
- call the delay/action/amplitude machinery **assumed or selected ingredients**, not derivations
- reserve stronger “derived” language for:
  - fixed-DAG pairwise interference
  - internal scaling diagnostics
  - bounded mechanism translations that truly come out of the tested model
