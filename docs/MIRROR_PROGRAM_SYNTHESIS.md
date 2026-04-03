# Mirror Symmetry Program: Complete Synthesis

**Date:** 2026-04-03
**Branches:** claude/distracted-napier (gap-physics + spectral program), main (structured growth)
**Status:** Unified architecture achieved. Born-clean. Audit-verified.

## The Problem

Linear path-sum propagation on random causal DAGs produces single-slit
detector distributions that converge as graph depth N grows (CLT ceiling).
This makes decoherence decay as ~1/N, limiting the model to N < 50 for
meaningful physics. Nine emergence approaches and 14 bath architectures
all failed to break this ceiling.

## The Solution: Z₂ Mirror Symmetry

Exact y → -y symmetry in the graph edge structure forces the transfer
matrix product to maintain rank-2 (one singular value per symmetry
sector). Slit A and slit B map to different sectors and cannot converge.

### Key results (audit-verified)

**Ceiling theorem** (distracted-napier):
Transfer matrix product T_N...T_1 is rank-1 on random DAGs. Second
singular value < 1e-30. Lindeberg condition passes. This is a spectral
no-go for all downstream mechanisms.

**Z₂ decoherence exponent** (distracted-napier):
Mirror purity exponent: -0.09 (nearly FLAT through N=80).
MI exponent: -0.31 (R²=0.89, cleanest scaling law in the project).
Compare random: purity -0.34, MI -1.06.

**Mass scaling F∝M** (distracted-napier):
2D mirror: alpha=0.84 (matches standard DAG 0.82). Confirmed at N=40.

**Born compliance** (distracted-napier, audit-verified):
All mirror generators with LINEAR propagator: |I₃|/P < 3e-15.
Verified by mirror_born_audit.py using propagate_LINEAR with NO
normalization. 6 generator/N combinations tested.

**MI audit** (distracted-napier, committed script):
mirror_mutual_information.py tests 4 families at N=15-80:
  2D mirror N=80: MI=0.773 bits (vs 0.131 random) — 6x more info
  3D mirror N=80: MI=0.484 bits (vs 0.099 random) — 5x more info

**Exact 2D mirror validation** (main, committed script):
mirror_2d_validation.py tests the exact 2D mirror family against a matched
random chokepoint baseline on the same linear propagator.
  N=60: MI=0.756 bits, dTV=0.857, 1-pur_min=0.442, gravity=+2.569,
  Born=1.08e-15 — strongest retained row in the exact 2D chain.
  Mass/distance follow-up remains weak, so no clean gravity law is promoted.

**Structured mirror growth** (main, linear propagator):
npl=30, N=30: 14% decoherence, gravity +3.05 (21.1 SE), Born=8e-17.
The GROWN geometry (not imposed) gives all four phenomena.

### Architecture comparison

| Architecture | Born | Gravity SE | Decoh% | MI bits (N=80) | Grown? |
|-------------|------|-----------|--------|---------------|--------|
| Random DAG | perfect | 1-5 | 2-5% | 0.10 | yes |
| Imposed modular gap | perfect | 3-7 | 5-10% | ~0.15 | no |
| Z₂ mirror (imposed) | perfect | 4-7 | 20-40% | 0.48-0.77 | no |
| exact 2D mirror | perfect | 2-4 | 30-44% | 0.35-0.76 | no |
| Z₂ mirror (grown) | 8e-17 | **21.1** | **14-19%** | (not yet measured) | **yes** |

## How we got here

### Phase 1: Gap characterization (20 experiments)
Established that the gap is a topological boundary condition about node
absence. Path-count asymmetry is the correct observable but non-local.
|y|-removal gives best Born-compliant joint coexistence.

### Phase 2: Ceiling theorem
Proved the transfer matrix product converges to rank-1. Quaternion
amplitudes don't help (magnitudes still sum like reals). Dynamical
topology creates functional channels but can't beat the CLT.

### Phase 3: Z₂ mirror breakthrough
Mirror symmetry forces rank-2 product. Decoherence exponent -0.27
(4x slower than random). F∝M preserved (alpha=0.84). Gravity grows
with N on mirror DAGs (unique property).

### Phase 4: Audit and unification
Born audit confirmed all mirror generators are Born-clean with linear
propagator. MI audit committed as reproducible script; the new exact 2D
validation adds a second artifact-backed mirror MI chain. Other thread
found structured mirror growth with linear propagator: 21.1 SE gravity
+ 14% decoherence + Born=8e-17.

## Z₂ breaking robustness

The symmetry is FRAGILE: 10% edge dropout loses 50% of decoherence.
The Z₂ must be exact in the edge structure, not approximate or
statistical. Physical interpretation: spatial parity must be a
fundamental feature of the event space geometry.

## Open questions

1. **Distance law on mirror DAGs:** Near-field peak confirmed, far-field
   1/b² not yet observed (graphs too small). Needs y_range > 20.

2. **Scaling on grown mirror:** The structured growth result is at N=25-30.
   Does it scale to N=60-100? Does the exponent match imposed mirror?

3. **MI on grown mirror:** Not yet measured. Expected to be high based
   on the decoherence signal.

4. **Physical interpretation of Z₂:** The model's axioms don't specify
   spatial parity. Is Z₂ a constraint on the event space or an emergent
   feature of the growth dynamics?

## Scripts (audit-grade, committed)

| Script | What it verifies |
|--------|-----------------|
| mirror_born_audit.py | Born < 3e-15 on ALL mirror generators (LINEAR) |
| mirror_mutual_information.py | MI on 4 families, N=15-80 |
| mirror_2d_validation.py | Exact 2D mirror Born + MI + gravity + decoherence |
| ceiling_formal_proof.py | Rank-1 theorem, Lyapunov spectrum |
| mirror_symmetric_dag.py | Z₂ decoherence scaling |
| mirror_chokepoint_joint.py | Born + gravity + decoherence joint |
| mirror_scaled_joint.py | Scaling to N=100 |
| approximate_mirror.py | Exact vs statistical symmetry |
| z2z2_explicit_mirror.py | Z₂×Z₂ decoherence + gravity |
| mirror_gravity_quantitative.py | Mass scaling on 3D mirror |
| mirror_gravity_controlled.py | Controlled mass placement |
