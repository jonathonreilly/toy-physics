# Figure Plan

This is the current manuscript figure map. It is intentionally conservative:
only figures that strengthen the retained backbone or cleanly illustrate bounded
companions belong in the first public package.

Companion captions live in [FIGURE_CAPTIONS.md](./FIGURE_CAPTIONS.md).

## Core arXiv figure set

### Figure 1. Framework and derivation map

- purpose: one-page visual of the retained backbone
- content:
  - `Cl(3)` on `Z^3`
  - weak-field gravity through Poisson / Newton together with WEP / time dilation
  - exact native `SU(2)`
  - graph-first structural `SU(3)`
  - anomaly-forced `3+1`
  - one-generation closure
  - three-generation matter structure
- source: manuscript synthesis, not a numerical runner
- status: schematic needed

### Figure 2. Graph-first `SU(3)` closure

- purpose: show selector, weak axis, residual swap, and `3 ⊕ 1` split
- source note: [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
- source runner: [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py)
- status: data available, publication figure not yet drawn

### Figure 3. Anomaly-forced `3+1`

- purpose: show the closure chain from left-handed anomaly to single-clock `3+1`
- source note: [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md)
- source runner: [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py)
- status: summary figure needed

### Figure 4. Three-generation matter structure

- purpose: display exact orbit structure `8 = 1 + 1 + 3 + 3` and the physical-lattice interpretation
- source note: [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md)
- source runners:
  - [frontier_generation_fermi_point.py](../../../scripts/frontier_generation_fermi_point.py)
  - [frontier_generation_rooting_undefined.py](../../../scripts/frontier_generation_rooting_undefined.py)
  - [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py)
- status: concept figure needed; do not use old overclaiming hierarchy plots

### Extended Data candidate. Weak-field gravity corollaries plus exact `I_3 = 0` and CPT

- purpose: carry compact gravity corollaries and exact supporting theorems
  without stealing main-text space
- source notes:
  - [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md)
  - [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md)
  - [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md)
- source runners:
  - [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py)
  - [frontier_born_rule_derived.py](../../../scripts/frontier_born_rule_derived.py)
  - [frontier_cpt_exact.py](../../../scripts/frontier_cpt_exact.py)
- status: optional depending on venue length

### Extended Data candidate. Retained `S^3` compactification / topology closure

- purpose: show the cone-cap family, boundary-link structure, and the retained
  topology closure without bloating the main text
- source notes:
  - [S3_GENERAL_R_DERIVATION_NOTE.md](../../S3_GENERAL_R_DERIVATION_NOTE.md)
  - [S3_CAP_UNIQUENESS_NOTE.md](../../S3_CAP_UNIQUENESS_NOTE.md)
- source runners:
  - [frontier_s3_boundary_link_theorem.py](../../../scripts/frontier_s3_boundary_link_theorem.py)
  - [frontier_s3_cap_uniqueness.py](../../../scripts/frontier_s3_cap_uniqueness.py)
  - [frontier_s3_general_r.py](../../../scripts/frontier_s3_general_r.py)
- status: optional depending on venue length

## arXiv-only companion figures

### Figure A1. Bounded DM lane

- purpose: show what is exact, derived, and bounded in the DM relic chain
- source notes:
  - [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md)
  - [OMEGA_LAMBDA_DERIVATION_NOTE.md](../../OMEGA_LAMBDA_DERIVATION_NOTE.md)
- status: wait until DM language stabilizes

### Figure A2. Bounded renormalized `y_t` lane

- purpose: show exact UV theorem versus bounded low-energy bridge
- source notes:
  - [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](../../YT_ZERO_IMPORT_AUTHORITY_NOTE.md)
  - [YT_GAUGE_CROSSOVER_THEOREM.md](../../YT_GAUGE_CROSSOVER_THEOREM.md)
- status: wait until `y_t` language stabilizes

### Figure A3. Bounded CKM lane

- purpose: preserve route history without confusing it for the promoted CKM package
- source notes:
  - [CABIBBO_BOUND_NOTE.md](../../work_history/ckm/CABIBBO_BOUND_NOTE.md)
  - [CKM_MASS_BASIS_NNI_NOTE.md](../../work_history/ckm/CKM_MASS_BASIS_NNI_NOTE.md)
  - [JARLSKOG_PHASE_BOUND_NOTE.md](../../work_history/ckm/JARLSKOG_PHASE_BOUND_NOTE.md)
- status: optional history/comparison figure only; do not present as the live flavor authority
