# Session Summary: Topology Pivot
**Date:** 2026-04-01
**Status:** Architecture result locked. Dynamic emergence open.

## The architecture story

On discrete causal DAGs with path-sum propagation:

1. **Gravity works** via the corrected propagator (1/L^p attenuation,
   directional measure, spent-delay action). This is a pure phase effect.

2. **Decoherence requires topology.** On uniform random DAGs, all 14
   tested environment architectures fail due to geometric convergence
   (CLT erases slit distinction by N~25). On modular two-channel DAGs,
   the CL bath achieves stable decoherence through N=100.

3. **Both gravity and decoherence work on the same graph family**
   (modular DAG with channel separation). Gravity actually improves
   on modular DAGs because channel structure reduces phase cancellation.

## Locked results

### Decoherence on modular DAG (12 seeds, N=12..100)
```
pur_min = 0.93 +/- 0.02 for N >= 25
(Uniform DAG baseline: 0.986 at N=25)
Interference preserved (visibility > 0.99)
S_norm stays in 0.2-0.5 range
```

### Gravity on modular DAG (8 seeds, k-band [3,5,7])
```
N=25: delta = +3.20 (2.6 SE) — clear deflection toward mass
N=40: delta = +2.50 (2.6 SE) — gravity persists
```

### IF program closure (14 architectures on uniform random DAGs)
All fail the same way: CLT concentration. Diagnosed in detail
at docs/DECOHERENCE_FAILURE_ANALYSIS.md.

## What we learned about emergence

Simple local growth rules (locality bias, reinforcement, repulsive
placement, amplitude feedback) do NOT produce persistent channel
separation. The reasons are clear:

- **Probabilistic barriers** (soft locality) are not enough — CLT
  still operates on the amplitude distribution
- **Amplitude feedback** carries source information, not slit
  information — source is y-symmetric so feedback is too
- **Topological barriers** (no nodes in gap) are needed — this is
  what the imposed modular gap provides

The deep question: does the topology need to "know about" the
quantum state to create channels? If yes, this is measurement
back-reaction.

## Open questions (prioritized)

1. **Dynamic channel emergence via post-barrier feedback**
   The amplitude feedback test used pre-barrier source amplitude.
   A different approach: grow the graph layer by layer, and after
   the barrier layer, use per-slit amplitude to guide growth.
   This couples topology evolution to measurement outcomes.

2. **Asymptotic floor vs drift**
   pur_min at 0.93 could be a true floor or slow drift.
   Need O(100) seeds at each N to resolve.

3. **Continuum interpretation**
   Channel separation = discrete analogue of spatial locality /
   branch-preserving geometry. Formalize this connection.

4. **3D gravity on modular DAGs**
   The 3D gravity test (three_d_gravity.py) should be adapted
   to modular DAGs to check whether the deflection result
   generalizes to higher dimensions.

## Files delivered this session

### New scripts
- `scripts/topology_families.py` — three DAG generators (hierarchical, modular, preferential)
- `scripts/topology_pivot_test.py` — four-family comparison
- `scripts/topology_pivot_extended.py` — crosslink sweep
- `scripts/topology_plateau_confirm.py` — N=40 + gap sweep
- `scripts/topology_large_n.py` — N=60 with interference check
- `scripts/topology_large_n_smooth.py` — 8-seed smoothed scaling
- `scripts/topology_asymptotics.py` — 12-seed N=100 with power law fit
- `scripts/dynamic_channel_emergence.py` — three local growth rules
- `scripts/amplitude_feedback_growth.py` — quantum-topology coupling
- `scripts/gravity_on_modular_dag.py` — gravity test on modular DAGs

### Updated scripts
- `scripts/caldeira_leggett_bath.py` — N=25 in purity sweep

### Documentation
- `docs/IF_PROGRAM_CLOSING_NOTE.md` — canonical closure
- `docs/DECOHERENCE_FAILURE_ANALYSIS.md` — updated with topology pivot
- `docs/SESSION_SUMMARY_2026-04-01_TOPOLOGY.md` — this file

### Log artifacts
- `logs/2026-04-01-topology-pivot.txt`
- `logs/2026-04-01-topology-scaling-law.txt`
- `logs/2026-04-01-dynamic-emergence.txt`
