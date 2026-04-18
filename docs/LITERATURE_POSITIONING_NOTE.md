# Literature Positioning Note

**Status:** reviewer-facing comparison note  
**Date:** 2026-04-01

## Purpose

This repo has a lot of internal mechanism analysis. A fair external criticism is that the project can feel more internally complete than externally situated. This note is here to make the neighboring mathematical terrain explicit.

## What this project is closest to

The project is best understood as:

- **toy mechanism science**
- in the broad family of **discrete / emergent / digital physics**
- with stronger-than-average emphasis on:
  - explicit numerical pressure tests
  - mechanism ablations
  - adversarial self-audit

It is **not** currently best described as a mature discrete quantum-gravity program in the same sense as causal set theory, CDT, or loop quantum gravity.

## Nearest neighboring literatures

### 1. Digital / cellular-automaton physics

Closest in spirit:

- Zuse / Fredkin style digital physics
- cellular-automaton ontologies
- Wolfram-style discrete substrate programs

Why the comparison matters:

- same basic ambition: recover physics-like structure from discrete local rules
- same main reviewer vulnerability: importing too much of the desired physics into the effective rules

What is different here:

- unusually explicit cheat list / self-audit
- heavier emphasis on mechanism diagnostics and failure analysis

### 2. Causal-set / quantum-measure style approaches

Closest mathematically on the interference side:

- path sums on causal structures
- Sorkin-style quantum measure / higher-order interference questions

Why the comparison matters:

- the fixed-DAG Sorkin diagnostic and pairwise path-sum language live near this literature
- future decoherence / influence-functional work should probably be framed with this comparison in mind

What is missing relative to that literature:

- a mature dynamics law
- a stronger continuum / asymptotic bridge
- tighter formal measure-theoretic framing

### 3. Regge / discrete-geometry / CDT style approaches

Closest on the geometry side:

- discrete approximations to geometry and propagation
- questions about continuum recovery and scale dependence

Why the comparison matters:

- reviewer criticism about the Laplacian field / Poisson-like behavior lands in this neighborhood
- the project needs a clearer continuum/asymptotic story if it wants to speak more directly to this audience

What is different here:

- this repo is not summing over triangulated geometries
- it is testing path selection and record formation on generated DAG substrates

### 4. Open quantum systems / collision models

Closest on the current decoherence frontier:

- repeated-interaction models
- fresh-ancilla collision models
- influence-functional / reduced-kernel formulations

Why the comparison matters:

- this is now probably the most important external literature for the non-unitary side
- several failed record architectures were really failed env-bookkeeping schemes, not yet failed open-system formulations

This is the literature the repo should probably engage next most directly.

### 5. Discrete propagator / lattice regularization / paper-scope framing

Closest on the current valley-linear and `1/L^(d-1)` lanes:

- discrete propagator comparisons on a fixed lattice family
- finite-volume / finite-resolution scaling
- same-harness action-law forks where only the action changes

Why the comparison matters:

- the valley-linear result is a bounded action fork, not a universal law
- the ordered-lattice kernel branch is a propagator fork, not a theorem
- the reviewer should read both as replayable comparison studies, not as
  finished fundamental-physics derivations

What is missing relative to that literature:

- a derivation from the axioms that uniquely selects the action law
- a fully closed asymptotic / continuum bridge
- universality across graph families without new companion-harness wording

This is the literature context for
[`PAPER_SCOPE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/PAPER_SCOPE_NOTE.md).

## What this note is not claiming

This note is **not** claiming equivalence to those frameworks.

It is only saying:

- these are the nearest mathematical conversations
- future writeups should name them explicitly
- doing so will make the project feel less insular and more review-ready

## New results that sharpen the positioning (2026-04-01 session)

### Dimensional progression
Mass scaling exponent increases with spatial dimension: threshold (2D)
→ alpha~0.58 converged (3D) → positive but parameter-sensitive (4D).
This connects to CDT / Regge literature on how discrete models recover
dimensional behavior. The 3D continuum limit is the strongest bridge.

### Cross-family robustness
Gravity + decoherence work on 4 of 5 tested 3D graph families
(modular, hierarchical, uniform, not preferential-attachment).
Addresses the "one-family artifact" critique. The hub-concentration
exception is informative: gravity needs distributed path diversity.

### Falsification criteria
The current package keeps explicit falsification-style boundaries in the live
prediction and scoping surfaces rather than the old evaluation card. The `k=0`
control (gravity vanishes without phase) still connects to the
quantum-measure distinction between physical interference and trivial
amplitude bias.

### Distance law as structural result
b-independence derived and closed across 9+ avenues. Connects to
CDT/Regge question: what discrete structures recover continuum force
laws? Answer: linear path-sum on random DAGs does not.

## Most useful next citations / comparisons to add later

If this becomes a paper or formal note, the most useful comparison targets are likely:

- Sorkin / quantum measure / higher-order interference
- open-system collision models / repeated interactions
- influence functionals and reduced dynamics
- causal-set dynamics / sequential growth
- CDT / discrete continuum-limit methodology

## Practical writing guidance

When describing the project externally:

- call it a **discrete event-network computational model**
- compare it first to **digital / emergent mechanism programs**
- use **quantum-measure** language for fixed-DAG interference results
- use **collision-model / influence-functional** language for the decoherence frontier
- use **lattice regularization / finite-volume scaling** language for the ordered-lattice action forks
- avoid presenting it as if it already competes directly with mature quantum-gravity programs on derivation or continuum control
