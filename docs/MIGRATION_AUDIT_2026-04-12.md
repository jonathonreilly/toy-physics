# Migration Audit: claude/youthful-neumann to codex/review-active

**Date:** 2026-04-12
**Source branch:** `claude/youthful-neumann`
**Target branch:** `codex/review-active`

This audit documents all science artifacts migrated from the youthful-neumann
worktree and their classification under the promotion playbook.

## Files Copied (New to review-active)

These files were not previously on `codex/review-active` and were copied during
this migration:

Scripts:
- `scripts/frontier_nonlinear_born_gravity.py`
- `scripts/frontier_gravitational_entanglement.py`
- `scripts/frontier_wave_equation_gravity.py`
- `scripts/frontier_wilson_frozen_source_discriminator.py`
- `scripts/frontier_experimental_predictions.py`
- `scripts/continuum_convergence_h0625.py`
- `scripts/frontier_irregular_sign_low_screening_gate.py`

Docs:
- `docs/NONLINEAR_BORN_GRAVITY_NOTE.md`
- `docs/GRAVITATIONAL_ENTANGLEMENT_NOTE.md`
- `docs/WAVE_EQUATION_GRAVITY_NOTE.md`
- `docs/WILSON_FROZEN_SOURCE_DISCRIMINATOR_NOTE.md`
- `docs/EXPERIMENTAL_PREDICTIONS_NOTE.md`
- `docs/DISTANCE_LAW_64_BOUNDED_CONTINUATION_NOTE.md`
- `docs/IRREGULAR_SIGN_LOW_SCREENING_GATE_NOTE.md`

## Files Already Present (Verified Present)

These files already existed on `codex/review-active` from prior migrations:

Scripts:
- `scripts/frontier_distance_law_definitive.py`
- `scripts/frontier_emergent_product_law.py`
- `scripts/frontier_architecture_portability_sweep.py`
- `scripts/frontier_irregular_sign_core_packet_gate.py`
- `scripts/frontier_self_consistent_field_equation.py`
- `scripts/frontier_action_normalization.py`
- `scripts/frontier_beyond_lattice_qcd.py`
- `scripts/em_gravity_coexistence_2x2.py`
- `scripts/frontier_emergent_gr_signatures.py`
- `scripts/frontier_spatial_metric_derivation.py`
- `scripts/frontier_electromagnetism_probe.py`
- `scripts/frontier_second_quantized_prototype.py`
- `scripts/frontier_holographic_entropy.py`
- `scripts/frontier_hawking_analog.py`
- `scripts/frontier_hawking_bogoliubov_quench.py`
- `scripts/frontier_dimension_emergence.py`
- `scripts/frontier_cosmological_expansion.py`
- `scripts/frontier_dispersion_relation.py`
- `scripts/frontier_diamond_nv_lattice_correction.py`

Docs:
- `docs/DISTANCE_LAW_DEFINITIVE_NOTE.md`
- `docs/EMERGENT_PRODUCT_LAW_NOTE.md`
- `docs/ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md`
- `docs/IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md`
- `docs/SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`
- `docs/ACTION_NORMALIZATION_NOTE.md`
- `docs/BEYOND_LATTICE_QCD_NOTE.md`
- `docs/EM_GRAVITY_COEXISTENCE_2X2_NOTE.md`
- `docs/EMERGENT_GR_SIGNATURES_NOTE.md`
- `docs/SPATIAL_METRIC_DERIVATION_NOTE.md`
- `docs/ELECTROMAGNETISM_PROBE_NOTE.md`
- `docs/SECOND_QUANTIZED_PROTOTYPE_NOTE.md`
- `docs/HOLOGRAPHIC_ENTROPY_NOTE.md`
- `docs/HAWKING_ANALOG_NOTE.md`
- `docs/HAWKING_BOGOLIUBOV_QUENCH_NOTE.md`
- `docs/DIMENSION_EMERGENCE_NOTE.md`
- `docs/COSMOLOGICAL_EXPANSION_NOTE.md`
- `docs/DISPERSION_RELATION_NOTE.md`
- `docs/DIAMOND_NV_LATTICE_CORRECTION_NOTE.md`
- `docs/LATTICE_GAUGE_DISTINCTION_NOTE.md`
- `docs/DIAMOND_NV_EXPERIMENT_CARD.md`

## Classification

### A. Bounded Promotion Candidates (11 items)

Strong results with explicit claim boundaries. Safe for promotion to `main`
after one final review pass confirms the bounded read.

| # | Name | Script | Note | Summary |
|---|------|--------|------|---------|
| 1 | distance_law_definitive | `frontier_distance_law_definitive.py` | `DISTANCE_LAW_DEFINITIVE_NOTE.md` | alpha=-1.001+/-0.004 on 96^3; bounded to ordered-cubic/Dirichlet |
| 2 | emergent_product_law | `frontier_emergent_product_law.py` | `EMERGENT_PRODUCT_LAW_NOTE.md` | M1*M2 from self-consistent Poisson; bounded family result |
| 3 | architecture_portability_sweep | `frontier_architecture_portability_sweep.py` | `ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md` | 4/4 architectures pass; bounded portability |
| 4 | irregular_sign_core_packet_gate | `frontier_irregular_sign_core_packet_gate.py` | `IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md` | 100%/93% both screenings; bounded same-surface separator |
| 5 | self_consistent_field_equation | `frontier_self_consistent_field_equation.py` | `SELF_CONSISTENCY_FORCES_POISSON_NOTE.md` | only Poisson gives attractive; bounded operator-family result |
| 6 | action_normalization | `frontier_action_normalization.py` | `ACTION_NORMALIZATION_NOTE.md` | c=1 from Eddington; reviewer-facing normalization memo |
| 7 | nonlinear_born_gravity | `frontier_nonlinear_born_gravity.py` | `NONLINEAR_BORN_GRAVITY_NOTE.md` | I3=0 iff attractive, perfect correlation; bounded Born-rule probe |
| 8 | gravitational_entanglement | `frontier_gravitational_entanglement.py` | `GRAVITATIONAL_ENTANGLEMENT_NOTE.md` | MI=2.3, LGT cannot reproduce; bounded entanglement discriminator |
| 9 | wave_equation_gravity | `frontier_wave_equation_gravity.py` | `WAVE_EQUATION_GRAVITY_NOTE.md` | box(f)=rho, grav waves at c=1.05; bounded wave-equation probe |
| 10 | beyond_lattice_qcd | `frontier_beyond_lattice_qcd.py` | `BEYOND_LATTICE_QCD_NOTE.md` | inseparability + structural Born; bounded differentiation memo |
| 11 | em_gravity_coexistence_2x2 | `em_gravity_coexistence_2x2.py` | `EM_GRAVITY_COEXISTENCE_2X2_NOTE.md` | R_GE=0, 7/7 pass; bounded kinematic coexistence |

### B. Explicit Holds with Blockers (9 items)

Each has a named blocker preventing promotion.

| # | Name | Script | Note | Blocker |
|---|------|--------|------|---------|
| 12 | emergent_gr_signatures | `frontier_emergent_gr_signatures.py` | `EMERGENT_GR_SIGNATURES_NOTE.md` | consistency check; spatial metric gate not closed per user call |
| 13 | spatial_metric_derivation | `frontier_spatial_metric_derivation.py` | `SPATIAL_METRIC_DERIVATION_NOTE.md` | Born rule squaring; user says not independent enough; (1-f) prefactor prescribed |
| 14 | electromagnetism_probe | `frontier_electromagnetism_probe.py` | `ELECTROMAGNETISM_PROBE_NOTE.md` | needs 2x2 factorial (done but staggered eps issue) |
| 15 | second_quantized_prototype | `frontier_second_quantized_prototype.py` | `SECOND_QUANTIZED_PROTOTYPE_NOTE.md` | prototype-scale, Paper 2 foundation |
| 16 | holographic_entropy | `frontier_holographic_entropy.py` | `HOLOGRAPHIC_ENTROPY_NOTE.md` | prototype-scale, Paper 2 foundation |
| 17 | hawking_analog | `frontier_hawking_analog.py` | `HAWKING_ANALOG_NOTE.md` | falsified single-particle; Paper 2 foundation |
| 18 | hawking_bogoliubov_quench | `frontier_hawking_bogoliubov_quench.py` | `HAWKING_BOGOLIUBOV_QUENCH_NOTE.md` | Gaussian-state, Paper 2 foundation |
| 19 | dimension_emergence | `frontier_dimension_emergence.py` | `DIMENSION_EMERGENCE_NOTE.md` | bounded proxy only |
| 20 | cosmological_expansion | `frontier_cosmological_expansion.py` | `COSMOLOGICAL_EXPANSION_NOTE.md` | bounded proxy only |

### C. Archive-Ready (4 items)

Negative results or closed lanes. Retained for completeness, not for promotion.

| # | Name | Script | Note | Reason |
|---|------|--------|------|--------|
| 21 | wilson_frozen_source_discriminator | `frontier_wilson_frozen_source_discriminator.py` | `WILSON_FROZEN_SOURCE_DISCRIMINATOR_NOTE.md` | negative result, lane closed |
| 22 | dispersion_relation | `frontier_dispersion_relation.py` | `DISPERSION_RELATION_NOTE.md` | honest negative, anomalous scaling |
| 23 | experimental_predictions | `frontier_experimental_predictions.py` | `EXPERIMENTAL_PREDICTIONS_NOTE.md` | Planck-scale undetectable |
| 24 | diamond_nv_lattice_correction | `frontier_diamond_nv_lattice_correction.py` | `DIAMOND_NV_LATTICE_CORRECTION_NOTE.md` | tests retardation not discreteness |

### D. Reviewer Memos (2 items, not science)

| # | Name | File | Type |
|---|------|------|------|
| 25 | LATTICE_GAUGE_DISTINCTION_NOTE | `docs/LATTICE_GAUGE_DISTINCTION_NOTE.md` | reviewer memo only |
| 26 | DIAMOND_NV_EXPERIMENT_CARD | `docs/DIAMOND_NV_EXPERIMENT_CARD.md` | lab protocol, not science |

### E. Companion Files (migrated alongside primary artifacts)

| File | Companion to |
|------|-------------|
| `docs/DISTANCE_LAW_64_BOUNDED_CONTINUATION_NOTE.md` | distance_law_definitive (#1) |
| `scripts/continuum_convergence_h0625.py` | distance_law_definitive (#1) |
| `scripts/frontier_irregular_sign_low_screening_gate.py` | irregular_sign_core_packet_gate (#4) |
| `docs/IRREGULAR_SIGN_LOW_SCREENING_GATE_NOTE.md` | irregular_sign_core_packet_gate (#4) |

## Promotion Rules

- Do NOT promote directly to `main` from this migration
- Do NOT restate full Newton closure, unconditional spatial-metric derivation,
  or global Poisson uniqueness
- Bounded candidates require one final review pass before any `main` merge
- Hold items require the named blocker to be resolved before promotion
- Archive-ready items stay on review-active for reference only

## Source Branch Status

After this migration, `claude/youthful-neumann` has no unique science artifacts
that are not also on `codex/review-active`. The branch can be considered
fully migrated for science content.
