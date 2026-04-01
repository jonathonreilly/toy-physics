# Session Summary: Topology Pivot
**Date:** 2026-04-01
**Status:** Architecture result locked. Connection-feedback emergence closed; node-placement emergence open.

## The architecture story

On discrete causal DAGs with path-sum propagation:

1. **Gravity works** via the corrected propagator (1/L^p attenuation,
   directional measure, spent-delay action). This is a pure phase effect.

2. **Decoherence is topology-controlled.** On dense random / graph-local
   lanes, the tested environment architectures converge too much as graphs
   densify. On modular gap-controlled DAGs, the CL bath achieves stable
   decoherence through N=100.

3. **Both gravity and decoherence work on the same graph family**
   (gap-controlled modular DAGs). With wider seed counts, the joint window is
   broad: every tested gap `0.0..5.0` passes the current joint criteria, and
   larger gaps strengthen both effects until connectivity breaks.

## Locked results

### Decoherence on modular DAG (12-seed asymptotic lane, N=12..100)
```
pur_min = 0.93 +/- 0.02 for N >= 25
Interference preserved (visibility > 0.99)
S_norm stays in 0.2-0.5 range
```

### Joint gravity + decoherence window (24 seeds)
```
All tested gaps 0.0..5.0 pass current joint criteria
Larger gap => stronger gravity and stronger decoherence
N=40, gap=5.0: gravity +3.47, pur_min 0.889, decoh +0.110
Crosslink probability is subleading across 0.0..0.10
```

### Gravity on modular DAG
```
N=25: delta = +3.20 (2.6 SE) — clear deflection toward mass
N=40: delta = +2.50 (2.6 SE) — gravity persists
```

### Uniform-random qualification
The earlier one-point `pur_min = 0.986` ceiling claim at `N=25` was too
strong for the later 24-seed read. What remains retained is not a single
ceiling value, but the broader diagnosis that graph-local architectures on
dense connected families still converge too much and underperform the larger-gap
modular lane.

## What we learned about emergence

Simple local or feedback-style growth rules do **not** produce persistent
channel separation. Seven approaches were tested in total. The reasons are now
clearer:

- **Probabilistic barriers** (soft locality) are not enough — CLT
  still operates on the amplitude distribution
- **Amplitude feedback** carries source information, not slit
  information — source is y-symmetric so feedback is too
- **Post-barrier slit-conditioned connection feedback** also fails —
  on sufficiently connected graphs the slit asymmetry per node collapses
  toward `0.5`
- **Distinguishability-based placement** can create real gaps, but the first
  tested rules make them too small, too large, or in the wrong place
- **Topological barriers** (no nodes in gap) are needed — this is
  what the imposed modular gap provides

The sharpened question is no longer “which connection bias works?”
It is whether graph dynamics can create or maintain **regions with no nodes at
the right size and location**.

## Open questions (prioritized)

1. **Node-placement / node-removal growth**
   Connection feedback is now a closed lane. The next live emergence test is a
   rule that changes where nodes appear, disappear, or persist, so that a hard
   gap can form dynamically at the observed good scale instead of overshooting
   into disconnection.

2. **Boundary-condition interpretation**
   If no self-regulating placement/removal rule appears cleanly, the remaining
   serious alternative is that the gap should be treated as part of the
   effective boundary condition of the emergent geometry.

3. **Asymptotic floor vs drift**
   pur_min at 0.93 could be a true floor or slow drift.
   Need O(100) seeds at each N to resolve.

4. **Continuum interpretation**
   Channel separation = discrete analogue of spatial locality /
   branch-preserving geometry. Formalize this connection.

5. **3D gravity on modular DAGs**
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
- `scripts/slit_conditioned_growth.py` — post-barrier slit-conditioned connection feedback
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
