# Claude Main Promotion Playbook

**Date:** 2026-04-12  
**Purpose:** single instruction set for getting the remaining review artifacts
onto `main` without reintroducing claim drift

## Working Rules

1. Work only from the consolidated review checkout, not from an old Claude or
   frontier worktree.
2. Treat `main` as the retained baseline and the review branch as the only
   place where non-`main` science is finalized.
3. Promote only bounded note+runner pairs.
4. Never promote a branch narrative. Promote specific artifacts.
5. Do not restate:
   - full Newton closure
   - architecture-independent full Newton closure
   - Einstein-equation derivation
   - unconditional factor-of-2 light bending
   - gravity+EM coexistence in one Hamiltonian
   unless the missing control listed below is explicitly closed.

## Current Branch Targets

- `main`: retained baseline
- review branch: `origin/codex/review-active`

## Source of Truth

Use these two files first:

- `docs/REVIEW_WORKTREE_INBOX_2026-04-11.md`
- `docs/REMAINING_NON_MAIN_HOLDS_2026-04-11.md`

If a claim is not reflected there, do not promote it.

## What Is Already On `main`

Do not reopen or duplicate these:

- bounded staggered weak-field source-mass companion
- bounded `64^3` path-sum distance continuation
- bounded Wilson test-mass / continuum companion
- bounded irregular core-packet sign separator
- bounded emergent cross-field product-law companion
- bounded architecture-portability companion
- bounded Newton-family notes already retained

Check `docs/REVIEW_WORKTREE_INBOX_2026-04-11.md` before touching anything.

## Remaining Lanes And Exact Gates

### 1. Overnight Claude bundle

Files:

- `docs/OVERNIGHT_CLAUDE_AUDIT_2026-04-12.md`
- `docs/EMERGENT_GR_SIGNATURES_NOTE.md`
- `docs/ELECTROMAGNETISM_PROBE_NOTE.md`
- `docs/EM_GRAVITY_COEXISTENCE_CONTROL_NOTE_2026-04-12.md`
- `docs/SPATIAL_METRIC_DERIVATION_NOTE.md`
- `docs/SECOND_QUANTIZED_PROTOTYPE_NOTE.md`
- `docs/HOLOGRAPHIC_ENTROPY_NOTE.md`
- `docs/HAWKING_ANALOG_NOTE.md`
- `docs/DIMENSION_EMERGENCE_NOTE.md`
- `docs/COSMOLOGICAL_EXPANSION_NOTE.md`
- `docs/LATTICE_GAUGE_DISTINCTION_NOTE.md`
- `docs/SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`
- the paired scripts in `scripts/`

Promotion rule:

- do not promote any overnight artifact directly from the Claude branch
- first land it on the review branch
- then write a new bounded audit note if and only if the blocker is actually
  closed

Sub-gates:

- GR signatures:
  - keep as consistency checks unless the spatial-metric step is derived
    independently of reusing the same `1-f` factor twice
- electromagnetism:
  - no coexistence claim without the 2x2 factorial mixed-residual control
- second-quantized / holographic:
  - no many-body or Hawking claim without a real Gaussian-state in/out or
    quench-style vacuum calculation
- dimension / cosmology:
  - keep as bounded proxy studies unless the specific proxy issues are fixed
- dispersion:
  - no retention until the anomalous-scaling ambiguity is replaced by a cleaner
    observable
- Poisson preference:
  - keep as preference among tested operators unless uniqueness is actually
    established
- lattice-gauge distinction:
  - reviewer memo only, not retained science

### 2. Wilson mutual-attraction side lane

Files:

- `docs/TWO_BODY_ATTRACTION_RETAINED_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_TEMPORAL_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/WILSON_SIDE_LANE_PROMOTION_REVIEW_2026-04-11.md`
- `docs/WILSON_BOTH_MASSES_ACCEL_NOTE_2026-04-11.md`
- `docs/WILSON_CAUSAL_DISCRIMINATOR_NOTE_2026-04-11.md`
- paired scripts

Gate:

- same open 3D Wilson surface
- causal discriminator must separate dynamic shared backreaction from frozen or
  lagged/static explanations
- temporal robustness alone is not enough

Do not promote if:

- `FROZEN_SOURCE` still explains the lane within tolerance

### 2a. Distance-law close path

Current best retained artifact:

- `docs/DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md`
- `scripts/distance_law_3d_64_closure.py`

Gate:

- do **not** treat `96^3` as the primary next fix
- first add a matched frozen/static-source control on the same `64^3` surface
- write the control outcome into a review-safe bounded note
- only then use `96^3` as a secondary widening / stability check

Do not promote if:

- the `64^3` lane still lacks same-surface frozen/static-source separation
- the only improvement is a larger-box continuation with no causal/static null

### 3. Exact two-particle product-law toy

Files:

- `docs/EXACT_TWO_PARTICLE_PRODUCT_LAW_FRONTIER_NOTE_2026-04-11.md`
- `scripts/exact_two_particle_product_law.py`

Gate:

- remove the baked-in bilinear factor from the ansatz
- add frozen/static-source control
- replay on the primary staggered/open-cubic surface

Do not promote if:

- the `M1*M2` structure is still explicit in the Hamiltonian

### 4. Irregular transport / portability beyond core-packet

Files:

- `docs/IRREGULAR_ENDOGENOUS_SIGN_*`
- paired scripts

Gate:

- do not rerun the retained core-packet gate
- use a portability-grade transport or invariant observable on the same
  irregular surface

Do not promote if:

- `cut2` still fails
- portability across graph growth still fails

### 4a. Gravity + EM coexistence

Files:

- `docs/EM_GRAVITY_COEXISTENCE_CONTROL_NOTE_2026-04-12.md`

Gate:

- build a smallest 2x2 factorial on one fixed ordered 3D surface
- recommended surface:
  - `h=0.5`
  - `W=8`
  - `L=12`
  - same point packet
  - same final-layer detector
  - same source plane
- runner target:
  - `scripts/em_gravity_coexistence_2x2.py`

Required cells:

- `H0`: no gravity, no EM
- `Hg`: gravity only
- `Hem`: EM only
- `Hg+Hem`: both on

Required readouts on the same evolved packet:

- `Δg`: gravity centroid shift, using the retained gravity harness readout
- `Δem`: EM odd response, using the retained electrostatics signed-centroid or
  antisymmetry readout

Decision statistic:

```text
R_GE[readout] = readout(Hg+Hem) - readout(Hg) - readout(Hem) + readout(H0)
```

Pass signature:

- `R_GE[Δg] ≈ 0`
- `R_GE[Δem] ≈ 0`
- EM same-point `+/-` cancellation remains exactly zero
- the combined cell preserves both single-sector readouts

Do not promote if:

- one sector changes materially when the other is turned on
- the mixed residual is stably nonzero
- the joint cell only works after renormalizing back into one single-sector lane

### 5. Staggered two-body closure family

Files:

- `docs/STAGGERED_*TWO_BODY*`
- paired scripts

Gate:

- stop centroid and shell-flux variants
- only reopen with a genuinely different conserved-current or new geometry

Do not promote if:

- partner-force is positive but trajectory-side closure is still negative

## Promotion Procedure

For any candidate:

1. Verify the runner compiles and, if cheap enough, runs.
2. Write or update a bounded audit note first.
3. Explicitly state:
   - exact surface/family
   - what is supported
   - what is not supported
   - the missing closure that still remains
4. Update:
   - `docs/REVIEW_WORKTREE_INBOX_2026-04-11.md`
   - `docs/REMAINING_NON_MAIN_HOLDS_2026-04-11.md`
5. Only after that, promote to `main` and update:
   - `docs/CANONICAL_HARNESS_INDEX.md`
   - `docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`
   - `docs/PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md`
   - `docs/repo/LANE_STATUS_BOARD.md`

## Language Rules

Use:

- `bounded-retained`
- `review hold`
- `consistency check`
- `proxy`
- `preferred among tested operators`
- `compatible with`

Avoid unless explicitly closed:

- `derived uniquely`
- `unconditional`
- `proved`
- `architecture-independent Newton closure`
- `Einstein equation`
- `coexist in one Hamiltonian`

## Immediate Next Priorities

1. distance-law close path stronger than the current `64^3` bounded continuation
2. gravity+EM 2x2 factorial coexistence control
3. effective-Hamiltonian / transfer-matrix dispersion discriminator
4. Gaussian-state quench / in-out vacuum prototype for the Hawking lane

For the dispersion lane specifically:

- do not do another single global `R^2` fit
- use the running-exponent fingerprint of the principal transfer-matrix branch
- extract:
  - `Ω(k) = -Im log λ0(k) / h`
  - `α_eff(k) = d log|Ω(k) - Ω(0)| / d log k`
- retain:
  - `α_lo` on a low-`k` window
  - `α_hi` on a pre-aliasing high-`k` window
  - `k_*` if a crossover exists
- classification target:
  - Schrödinger: `α_lo ≈ 2`, `α_hi ≈ 2`
  - linear: `α_lo ≈ 1`, `α_hi ≈ 1`
  - KG: `α_lo ≈ 2`, `α_hi ≈ 1`, finite `k_*`

For the Hawking lane specifically:

- first build:
  - `scripts/frontier_hawking_bogoliubov_quench.py`
  - `docs/HAWKING_BOGOLIUBOV_QUENCH_NOTE.md`
- use a finite quadratic bosonic chain with a sudden quench in onsite mass
  and/or nearest-neighbor coupling
- define `H_in` and `H_out`, diagonalize both, and report exact Bogoliubov
  coefficients `β_k` and occupations `n_k = |β_k|^2`
- required null:
  - `H_out = H_in` must give `β_k = 0` mode-by-mode
- do not describe this first step as a horizon or Hawking claim
- the purpose is to leave overlap-proxy territory and establish a real
  Gaussian-state in/out calculation first

## Bottom Line

Claude should work the review branch top-down, promote only bounded artifacts,
and treat every remaining lane as blocked until its named control is closed.
