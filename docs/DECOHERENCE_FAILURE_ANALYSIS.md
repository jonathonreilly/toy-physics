# Decoherence Failure Analysis

**Date:** 2026-04-01
**Experiments tested:** 14 decoherence architectures on uniform random DAGs, plus topology-pivot and growth follow-ons

## The problem

Detector-state purity Tr(ρ²) increases with graph size under every tested environment/record architecture. On random DAGs:
- N=8: purity ~0.60-0.74 (good decoherence)
- N=25: purity ~0.85-0.94 (weak decoherence)

This means the model's decoherence weakens as the system grows — the opposite
of physical decoherence.

That conclusion is now **scoped**:

- it remains true for the tested graph-local environment architectures on the
  original dense random-DAG lane
- but it is no longer the whole story once the graph family is changed into a
  **gap-controlled modular topology**

## What was tested

| # | Architecture | Env states | Purity trend | Why it fails |
|---|---|---|---|---|
| 1 | Node label (fine) | N_mass | ↑ | both slits reach all mass nodes |
| 2 | Node label (binary) | 2 | ↑ | too coarse to distinguish slits |
| 3 | Node label (y-bin) | 2-3 | ↑ | both slits hit both y-bins |
| 4 | Cumulative action (binned) | N_bins | ↑ | action per path converges |
| 5 | Evolving phase | N_bins | ↑ or =1 | phase wrapping or convergence |
| 6 | Scaled bins (N_bins∝N_mass) | varies | ↑ | amplitude concentrates |
| 7 | Multi-local tensor (D1) | d^M | ↑ | amplitude in few dominant states |
| 8 | Spatial trace (D4) | N_exit | ↑ | = node label (relabeling) |
| 9 | Graph growth (stochastic) | varies | ↓ weakly | CLT over growth realizations |
| 10 | Distributed edge records | ~500-2000 | ↑ | CLT concentrates records |
| 11 | Two-scale (G2+env) | varies | ↑ | macro averaging erases micro info |
| 12 | Directional angle records | 5 | ↑ | too coarse, same convergence |

## The common failure mode

Every architecture fails the same way: **amplitude concentration.**

On small graphs (N<200), the few paths from each slit diverge through different mass nodes/edges/angles → different env states → balanced amplitude across states → low purity → good decoherence.

On large graphs (N>400), path multiplicity grows exponentially. Both slits have many paths reaching every mass node from every direction. The amplitude-weighted distribution over env states converges to the same shape for both slits (central limit theorem). The partial trace removes almost nothing → high purity → weak decoherence.

This is independent of:
- how env states are defined (node, edge, angle, cumulative, tensor)
- how many env states there are (2, 5, 29, 336, 2000)
- whether the propagator uses flat or directional measure

## What a successful architecture needs

Based on the failure analysis, a successful decoherence mechanism must have at least one of these properties:

### Property 1: Env diversity that grows faster than path convergence

Path multiplicity grows as ~degree^depth. The env state diversity of all tested architectures grows polynomially (linear in mass nodes, quadratic in edges). The mismatch is exponential-vs-polynomial.

**Requirement:** env dimensionality must grow exponentially with graph depth, matching path multiplicity. Tensor product structures (D1) achieve this in principle but amplitude concentrates in few states.

### Property 2: Amplitude spreading that resists concentration

Even with enough env states, amplitude concentrates in few dominant ones. This is because the path-sum is linear: the amplitude at each env state is the sum of many path contributions, which converges by CLT.

**Requirement:** a mechanism that prevents amplitude from concentrating. This could be:
- a nonlinear combination rule (breaks CLT but may break Born rule)
- an irreversible information loss (like measurement collapse)
- an interaction that CREATES diversity rather than summing it away

### Property 3: Slit discrimination that doesn't rely on path separation

All tested architectures assume slits are distinguishable because their paths go through different mass regions. On large graphs, this assumption fails because both slits' paths cover the entire mass region.

**Requirement:** slit discrimination based on something other than spatial path separation. Candidates:
- phase relationships (not just phase magnitude)
- temporal ordering (which slit's amplitude arrives first)
- correlation structure (how amplitude is distributed, not just where)

## Additional architectures tested (2026-04-01, post-summary)

| # | Architecture | Key property | Result |
|---|---|---|---|
| 13 | AFC (amplitude field coherence) | Complex wavefield overlap K at mass region | |K| drops 0.999→0.91, but purity Δ < 0.006 |
| 14 | CL bath (Caldeira-Leggett y-bin) | Exponential D=exp(-λ²S), spatial bins | Correct direction N=12→18, same reversal at N=25 |

### Architecture 13: AFC
K = Σ_m ψ_A*(m) ψ_B(m) / sqrt(N_A N_B). Uses phase structure, not just magnitudes.
K decreases with N (0.999→0.91) — the phase contrast IS present.
But purity decoherence is only ~0.006 because a single scalar K cannot achieve
the mixing that multi-dimensional environments produce. The single-K structure
limits how mixed the density matrix can become.

### Architecture 14: Caldeira-Leggett bath
S_norm = Σ_bins |ψ_A(y_b) - ψ_B(y_b)|² / (N_A + N_B) INCREASES with N:
N=12: 0.097, N=18: 0.113, N=25: 0.219. Correct direction.
At λ=10, D≈0, bath achieves near-maximal decoherence.
Decoh grows N=12→18 (+0.006→+0.049). FIRST approach with correct scaling direction.

BUT: N=25 reverses (+0.014). Root cause: pur_min (purity of maximally decohered
state) jumps from 0.9506 (N=18) to 0.9860 (N=25). The two single-slit patterns
at detectors are MORE SIMILAR at N=25 — geometric convergence hits the
DETECTOR DISTRIBUTIONS, not just the bath.

## What has NOT been tested

1. **Nonlinear path combination** (breaks CLT but may break Born)
2. **Measurement-like collapse** at mass nodes (irreversible information loss)
3. **Temporal/causal ordering** of slit interactions with mass
4. **Entanglement with CA dynamics** (pattern oscillation as environment)
5. ~~**Non-uniform graph topology**~~ → TESTED, see below

## Topology pivot result (2026-04-01)

The non-uniform-topology hypothesis was **confirmed**.

### 1. Modular topology breaks the old ceiling picture

Three graph families were tested in the first pivot:

| Family | pur_min at N=25 | pur_min at N=40 | Verdict |
|---|---|---|---|
| Uniform random (baseline) | 0.986 | not tested in the original pivot log | ceiling |
| Hierarchical (channel leak) | rebounds | not retained | rebounds |
| **Modular two-channel** | **0.942** | **0.893** | **breaks ceiling** |
| Preferential attachment | ~1.0 | not retained | fails |

The modular two-channel DAG with a y-gap between channels preserves
slit-path structural separation as N grows. In the later asymptotic pass:

- **pur_min stays near `0.93 ± 0.02` through the tested `N=100` lane**
- **both-slits-open detector contrast remains high** in the current large-`N`
  scan
- **CL bath contrast stays finite**
- the old sharp reversal picture does not return on the retained modular lane

So the bottleneck was the **graph family**, not the IF / CL machinery.

### 2. The joint gravity+decoherence phase diagram is broad, not narrow

The later 24-seed modular sweep changed the earlier small-sample read.
Once gravity and decoherence were measured on the **same graph instances**
with enough seeds, the result was not a narrow sweet spot but a broad
unification window.

Current retained read:

- the refined phase diagram now uses actual traced purity `pur_cl`
  together with paired per-seed gravity significance
- tested gaps `0.0..5.0` keep positive gravity and `pur_cl < 0.96`
  on the audited sweep
- larger imposed gaps generally give **stronger gravity and stronger
  decoherence** until connectivity eventually breaks
- crosslink probability is subleading across the tested `0.0..0.10` range
- `gap=0` now behaves as the true uniform-style baseline in the
  modular generator

So the emerging statement is stronger than “modular helps.” It is:

- **hard topological separation is a control parameter**
- more imposed gap means stronger branch preservation, stronger decoherence,
  and stronger gravity on the tested family

### 3. Dynamic emergence is still open

Simple local growth rules do **not** yet generate the good channel structure.
The failed family is now broader and cleaner:

- locality bias gives temporary clustering but recoheres by larger `N`
- reinforcement / repulsion also fail at larger `N`
- pre-barrier source-amplitude feedback fails because the source is y-symmetric
  before the slit/barrier structure exists
- post-barrier slit-conditioned connection growth also fails because on
  sufficiently connected graphs both slits already reach almost every
  post-barrier node, so the local asymmetry signal collapses toward `0.5`
- first-pass distinguishability-based node placement creates real gaps, but at
  the wrong size or location: too small does not help, too large disconnects
  the graph
- global node pruning can improve the dense-random baseline at intermediate
  `N`, and the newer 3D self-regulating lanes sharpen that result:
  fixed-threshold pruning helps through `N=50`, while adaptive-quantile
  pruning extends the useful window through `N=60`. But the ceiling still
  returns by `N=80`, and deletion-only dynamics still drive the graph toward
  disconnection or low valid-seed coverage. The current implementation
  therefore remains a nonlocal post-hoc surrogate rather than a retained local
  endogenous dynamics law

So the open emergence question is now sharper:

- **can node placement or node removal create persistent hard gaps at the right
  size and midpoint location as a local law, rather than a global pruning
  surrogate?**
- the remaining open growth lane is no longer another connection-bias rule
  but a rule for where nodes exist at all
- simple deletion-only pruning of a connected graph is now a bounded partial
  positive, but still a closed asymptotic lane

## Honest assessment (updated)

On the original **uniform-random / dense-connected** lanes, the tested
graph-local environment architectures still fail by geometric convergence.
That diagnostic remains real.

But the sharper repo-facing result is now this:

- the IF / CL route is retained on a broader **gap-controlled modular family**
- the joint gravity+decoherence window is broad inside that family
- stronger imposed gap lowers the current decoherence floor and strengthens
  gravity until connectivity breaks

So the resolution is **topological first**, not “find a cleverer bath.”

Open questions:

- Does the modular channel structure have a clean physical interpretation?
  (channel separation ↔ branch-preserving spatial locality?)
- Can a self-regulating node-placement or node-removal rule generate the
  channel structure dynamically instead of imposing it by hand?
- Can adaptive quantile pruning be stabilized with connectivity-aware or
  birth/death updates, or is deletion-only dynamics fundamentally too weak?
- If node non-permanence matters, does it have to create a real hard gap
  rather than merely thin the graph?
- Does `pur_min ~ 0.93 ± 0.02` represent a true floor, or a slower large-`N`
  drift that still needs more seeds to resolve?
- How much of the large-`N` interference story survives once the detector
  contrast proxy is replaced by a true single-vs-double-slit visibility metric?
