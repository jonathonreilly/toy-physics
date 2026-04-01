# Decoherence Failure Analysis

**Date:** 2026-04-01
**Experiments tested:** 12 architectures across ~25 experiments

## The problem

Detector-state purity Tr(ρ²) increases with graph size under every tested environment/record architecture. On random DAGs:
- N=8: purity ~0.60-0.74 (good decoherence)
- N=25: purity ~0.85-0.94 (weak decoherence)

This means the model's decoherence weakens as the system grows — the opposite of physical decoherence.

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

The non-uniform topology hypothesis was **confirmed**. Three graph families tested:

| Family | pur_min at N=25 | pur_min at N=40 | Verdict |
|---|---|---|---|
| Uniform random (baseline) | 0.944 | not tested | ceiling |
| Hierarchical (channel leak=0.05) | 0.950 | not tested | rebounds |
| **Modular two-channel (gap=4.0)** | **0.942** | **0.893** | **breaks ceiling** |
| Preferential attachment | 0.996 | not tested | fails |

The modular two-channel DAG with a y-gap between channels preserves slit-path
structural separation as N grows. At N=40:
- **pur_min = 0.893** (lowest ever measured at large N)
- **decoh = +0.107** (strongest CL bath decoherence ever measured)
- **S_norm = 0.457** (bath contrast still growing)
- No reversal — pur_min DECREASES at N=40 after brief N=25-30 plateau

The bottleneck was the **graph family**, not the bath design. The IF framework
and CL bath work correctly when given topology that preserves slit distinction.

## Honest assessment (updated)

On **uniform random DAGs**, all 14 architectures fail due to geometric
convergence (CLT). The decoherence-at-scale program is closed for this
graph family.

On **modular two-channel DAGs**, the CL bath achieves scaling decoherence:
pur_min stays bounded below 0.95 (and continues improving) at N=40.
The resolution is topological, not architectural.

Open questions:
- Does the modular topology have a physical interpretation? (channel
  separation ↔ spatial locality in emergent geometry?)
- Can the channel structure emerge dynamically from an evolving graph?
- What is the asymptotic pur_min as N→∞ on modular DAGs?
