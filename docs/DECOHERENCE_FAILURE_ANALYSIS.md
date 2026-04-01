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

## What has NOT been tested

1. **Continuous bath variable** (infinite-dim env, no binning)
2. **Nonlinear path combination** (breaks CLT but may break Born)
3. **Measurement-like collapse** at mass nodes (irreversible information loss)
4. **Temporal/causal ordering** of slit interactions with mass
5. **Entanglement with CA dynamics** (pattern oscillation as environment)

## Honest assessment

The decoherence scaling problem is not a parameter-tuning issue. It is a structural property of linear path-sum propagation on growing graphs. The CLT guarantees that any finite-dimensional environment register will see amplitude concentration on large graphs.

The resolution likely requires either:
- abandoning finite-dimensional env (continuous bath)
- abandoning linear path combination (nonlinear propagator)
- introducing genuine measurement/collapse at mass interactions
- coupling to a separate dynamical system (CA oscillation as bath)

Each of these would be a significant architectural change, not a variant of the current approach.
