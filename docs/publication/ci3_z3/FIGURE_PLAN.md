# Figure Plan

This is the current manuscript figure map. It is intentionally conservative:
only figures that strengthen the retained backbone or cleanly illustrate bounded
companions belong in the first public package.

Companion captions live in [FIGURE_CAPTIONS.md](./FIGURE_CAPTIONS.md).

## Nature letter figure set

### Figure 1. Framework and derivation map

- purpose: one-page visual of the retained backbone
- content:
  - `Cl(3)` on `Z^3`
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
- source runner: [frontier_graph_first_su3_integration.py](/private/tmp/physics-publication-prep/scripts/frontier_graph_first_su3_integration.py)
- status: data available, publication figure not yet drawn

### Figure 3. Anomaly-forced `3+1`

- purpose: show the closure chain from left-handed anomaly to single-clock `3+1`
- source note: [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md)
- source runner: [frontier_anomaly_forces_time.py](/private/tmp/physics-publication-prep/scripts/frontier_anomaly_forces_time.py)
- status: summary figure needed

### Figure 4. Three-generation matter structure

- purpose: display exact orbit structure `8 = 1 + 1 + 3 + 3` and the physical-lattice interpretation
- source note: [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md)
- source runners:
  - [frontier_generation_fermi_point.py](/private/tmp/physics-publication-prep/scripts/frontier_generation_fermi_point.py)
  - [frontier_generation_rooting_undefined.py](/private/tmp/physics-publication-prep/scripts/frontier_generation_rooting_undefined.py)
  - [frontier_generation_axiom_boundary.py](/private/tmp/physics-publication-prep/scripts/frontier_generation_axiom_boundary.py)
- status: concept figure needed; do not use old overclaiming hierarchy plots

### Extended Data candidate. Exact `I_3 = 0` and CPT

- purpose: carry exact supporting theorems without stealing main-text space
- source notes:
  - [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md)
  - [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md)
- source runners:
  - [frontier_born_rule_derived.py](/private/tmp/physics-publication-prep/scripts/frontier_born_rule_derived.py)
  - [frontier_cpt_exact.py](/private/tmp/physics-publication-prep/scripts/frontier_cpt_exact.py)
- status: optional depending on venue length

## arXiv-only companion figures

### Figure A1. Bounded topology lane

- purpose: show the cap-map / cone-cap construction and clearly label the lane as bounded
- source notes:
  - `review-active` bounded `S^3` notes
- status: wait until the topology lane stabilizes

### Figure A2. Bounded DM lane

- purpose: show what is exact, derived, and bounded in the DM relic chain
- source notes:
  - `review-active` bounded DM notes
- status: wait until DM language stabilizes

### Figure A3. Bounded renormalized `y_t` lane

- purpose: show exact UV theorem versus bounded low-energy bridge
- source notes:
  - `review-active` bounded `y_t` notes
- status: wait until `y_t` language stabilizes

### Figure A4. Bounded CKM lane

- purpose: show route-pruning and the remaining Higgs `Z_3` obstruction
- source notes:
  - `review-active` bounded CKM notes
- status: hold until CKM work stops moving
