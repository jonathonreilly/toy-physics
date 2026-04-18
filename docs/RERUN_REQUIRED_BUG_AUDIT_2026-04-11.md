# Rerun-Required Bug Audit — 2026-04-11

This note tracks the validated bugs from the last-week review that require
either reruns or full experiment redesign before any further promotion.

Use this together with:

- [`docs/CODE_REVIEW_LAST_WEEK_2026-04-11.md`](CODE_REVIEW_LAST_WEEK_2026-04-11.md)
- [`docs/repo/RETEST_PLAYBOOK.md`](repo/RETEST_PLAYBOOK.md)
- [`docs/repo/LANE_STATUS_BOARD.md`](work_history/repo/LANE_STATUS_BOARD.md)

## A. Fix And Rerun On The Same Lane

This section mixes two classes of items:

- active rerun requirements
- bug patterns that are already corrected on retained `main` surfaces but still
  matter when older runner families are reopened

Do not read every entry below as an unresolved blocker on current `main`.

### 1. Periodic 2D staggered wraparound-weight bug

**Status on `main`: corrected on the live periodic weighted package; historical
periodic frontiers still need code audit before reuse**

Bug class:

- periodic adjacency is built with modulo indexing
- hopping weights are then computed from raw coordinate differences instead of
  minimum-image distances
- boundary-crossing neighbors are therefore misweighted

Validated affected runners included:

- [`scripts/frontier_born_rule_alpha.py`](../scripts/frontier_born_rule_alpha.py)
- [`scripts/frontier_self_consistency_test.py`](../scripts/frontier_self_consistency_test.py)
- [`scripts/frontier_eigenvalue_stats_and_anderson_phase.py`](../scripts/frontier_eigenvalue_stats_and_anderson_phase.py)
- [`scripts/frontier_holographic_probe.py`](../scripts/frontier_holographic_probe.py)
- [`scripts/frontier_boundary_law_robustness.py`](../scripts/frontier_boundary_law_robustness.py)
- [`scripts/frontier_staggered_geometry_superposition_retained.py`](../scripts/frontier_staggered_geometry_superposition_retained.py)
- [`scripts/frontier_bmv_entanglement.py`](../scripts/frontier_bmv_entanglement.py)
- [`scripts/frontier_branch_entanglement_robustness.py`](../scripts/frontier_branch_entanglement_robustness.py)

Corrected current-main reruns now exist for:

- [`scripts/frontier_self_consistency_test.py`](../scripts/frontier_self_consistency_test.py)
- [`scripts/frontier_eigenvalue_stats_and_anderson_phase.py`](../scripts/frontier_eigenvalue_stats_and_anderson_phase.py)
- [`scripts/frontier_born_rule_alpha.py`](../scripts/frontier_born_rule_alpha.py)
- [`scripts/frontier_holographic_probe.py`](../scripts/frontier_holographic_probe.py)
- [`scripts/frontier_boundary_law_robustness.py`](../scripts/frontier_boundary_law_robustness.py)
- [`scripts/frontier_staggered_geometry_superposition_retained.py`](../scripts/frontier_staggered_geometry_superposition_retained.py)
- [`scripts/frontier_bmv_entanglement.py`](../scripts/frontier_bmv_entanglement.py)
- [`scripts/frontier_branch_entanglement_robustness.py`](../scripts/frontier_branch_entanglement_robustness.py)

Shared fix surface:

- [`scripts/periodic_geometry.py`](../scripts/periodic_geometry.py)

Historical note:

- [`scripts/frontier_bmv_threebody.py`](../scripts/frontier_bmv_threebody.py)
  also moves under the minimum-image fix, but it remains a historical heuristic
  surface and not the canonical branch-entanglement classifier.

Revisit rule:

- any *other* periodic 2D result outside those corrected current-main notes
  should still be code-audited against `scripts/periodic_geometry.py` and rerun
  before reuse

### 2. Self-consistency random controls are not moment-matched

**Status on `main`: corrected on the retained structured-null rerun**

Affected runner:

- [`scripts/frontier_self_consistency_test.py`](../scripts/frontier_self_consistency_test.py)

Bug:

- positive/negative random controls use `abs(normal(mean, std))`
- this changes the effective mean and variance
- sign/correlation comparisons are confounded

Corrected current surface:

- [`scripts/frontier_self_consistency_test.py`](../scripts/frontier_self_consistency_test.py)
- [`docs/SELF_CONSISTENCY_STRUCTURED_NULL_NOTE_2026-04-11.md`](SELF_CONSISTENCY_STRUCTURED_NULL_NOTE_2026-04-11.md)

Revisit rule:

- do not reuse older iid-random-control summaries; use the structured-null note
  and corrected runner surface instead

### 3. Two-field wave family robustness is not independent

**Status on `main`: corrected and rerun; the wave note is now downgraded to a
bounded wave-field result**

Affected runner:

- [`scripts/frontier_two_field_wave.py`](../scripts/frontier_two_field_wave.py)

Bug:

- family checks inherit the already evolved field state

Corrected retained surface:

- [`scripts/frontier_two_field_wave.py`](../scripts/frontier_two_field_wave.py)
- [`docs/STAGGERED_TWO_FIELD_WAVE_NOTE.md`](STAGGERED_TWO_FIELD_WAVE_NOTE.md)

Rerun outcome on current `main`:

- `W6` now restarts each family from clean `Φ=0`, `dΦ/dt=0` initial data
- the corrected hard scores are `4/5`, `5/5`, `4/5` on random geometric,
  growing, and layered cycle
- the old retained `5/5` interpretation does not survive the clean-family rerun

Revisit rule:

- do not cite older retained `5/5` wave-coupling summaries; use the rerun-
  corrected wave note and current test matrix wording instead

### 4. Retarded probe R9 cannot fail

**Status on `main`: corrected and rerun; R9 is now diagnostic-only and not part
of the scored closure battery**

Affected runner:

- [`scripts/frontier_two_field_retarded_probe.py`](../scripts/frontier_two_field_retarded_probe.py)

Bug:

- the scale-gap row increments the score unconditionally

Corrected current surface:

- [`scripts/frontier_two_field_retarded_probe.py`](../scripts/frontier_two_field_retarded_probe.py)
- [`docs/TWO_FIELD_RETARDED_PROBE_NOTE_2026-04-10.md`](TWO_FIELD_RETARDED_PROBE_NOTE_2026-04-10.md)

Current mainline read:

- R9 is explicitly labeled as an unscored diagnostic row for force-gap,
  shell-radial, and spectral characterization
- the scored battery on current `main` is `R1`-`R8` only
- the retained takeaway is therefore about graph-native causal-memory viability
  and the surviving scored rows, not a closed scale-gap gate

Revisit rule:

- do not count R9 as a pass/fail closure row unless the lane is redesigned to
  make it a real scored gate
- for current `main`, cite the retarded-probe note and runner as a bounded
  rerun-corrected retarded-field companion with diagnostic-only scale-gap
  reporting

### 5. Decoherence distance sweep aliases torus separations

**Status on `main`: stale historical caution only; not a live rerun blocker**

Affected runner:

- historical frontier-only runner `frontier_gravitational_decoherence_rate.py`
  (not retained on `main`)

Bug:

- `d = 6, 8` on a periodic `10x10` torus are not clean long-range separations

Current mainline read:

- the live gravitational-decoherence companion on current `main` hangs off:
  - [`scripts/frontier_grav_decoherence_derived.py`](../scripts/frontier_grav_decoherence_derived.py)
  - [`docs/GRAV_DECOHERENCE_DERIVED_NOTE.md`](GRAV_DECOHERENCE_DERIVED_NOTE.md)
- that bounded companion is a derived BMV-class benchmark lane, not the old
  finite-torus distance sweep

Action if the historical torus sweep is reopened:

- redo the `Gamma(d)` law on an open surface or a torus protocol with distinct
  minimum-image separations

### 6. Geometry-superposition added-edge DAG variant

**Status on `main`: corrected and rerun; exploratory lane preserved with
narrower historical/path-sum framing**

Affected runner:

- [`scripts/frontier_geometry_superposition.py`](../scripts/frontier_geometry_superposition.py)

Bug:

- the added-edge DAG builder can break after the first failed draw, often
  returning essentially no added edges

Corrected current surface:

- [`scripts/frontier_geometry_superposition.py`](../scripts/frontier_geometry_superposition.py)
- [`docs/GEOMETRY_SUPERPOSITION_DAG_ENSEMBLE_NOTE_2026-04-11.md`](GEOMETRY_SUPERPOSITION_DAG_ENSEMBLE_NOTE_2026-04-11.md)

Current mainline read:

- the added-edge geometry now samples valid forward skip edges explicitly
- the rerun remains a bounded exploratory/path-sum geometry-superposition
  signal, not a staggered retained result
- current rerun summary:
  - raw coherent-vs-incoherent contrast: `3.93%`
  - normalized phase-only contrast: `3.93%`
  - centroid shift: `0.0574`
  - width change: `0.0211`
  - pairwise detector-phase differences up to `0.323 rad` (`18.5°`)

Revisit rule:

- do not promote this lane as a staggered headline result
- if reopened later, treat it as a path-sum exploratory control rather than a
  live retained architecture lane

## B. Redesign Before Any Rerun

These are not “run it again” bugs. The measurement itself is invalid or the
claim does not match the computed object.

### 1. Original two-body mutual-attraction runner

**Status on `main`: retired as evidence; preserved only as a historical
exploratory predecessor to the open-Wilson two-orbital lane**

Affected runner:

- historical frontier-only runner `frontier_two_body_mutual_attraction.py`
  (not retained on `main`)

Reason:

- one wavefunction with two lobes, not a true two-body channel

Action:

- do not rerun this for evidence
- use the retained open-Wilson family instead:
  - [`scripts/frontier_wilson_two_body_open.py`](../scripts/frontier_wilson_two_body_open.py)
  - [`scripts/frontier_wilson_two_body_laws.py`](../scripts/frontier_wilson_two_body_laws.py)
  - [`scripts/frontier_test_mass_limit.py`](../scripts/frontier_test_mass_limit.py)

### 2. Periodic Wilson “Newton law” runner

**Status on `main`: historical-only caution; not part of the live Wilson
evidence chain**

Affected runner:

- historical frontier-only runner `frontier_wilson_newton_law.py`
  (not retained on `main`)

Reasons:

- periodic torus, not image-free
- “mass law” only rescales partner source strength

Action:

- do not rerun as a Newton test
- do not treat it as a missing rerun blocker for the current `main` package;
  the live Wilson weak-field lane already hangs off the open-surface runners
  and notes
- if the law lane continues, rerun only on the open Wilson surface with a
  physically meaningful source/inertial parameterization:
  - [`scripts/frontier_wilson_mu2_distance_sweep.py`](../scripts/frontier_wilson_mu2_distance_sweep.py)
  - [`scripts/frontier_test_mass_limit.py`](../scripts/frontier_test_mass_limit.py)
  - [`scripts/frontier_continuum_limit.py`](../scripts/frontier_continuum_limit.py)

### 3. Wilson law-fit scripts use post-selected survivor rows

**Status on `main`: bounded post-selected law-characterization surface; not a
blind law-estimate blocker for the current Wilson reopen lane**

Affected runners:

- [`scripts/frontier_wilson_two_body_laws.py`](../scripts/frontier_wilson_two_body_laws.py)
- historical frontier-only runner `frontier_wilson_partner_source_crossover.py`
  (not retained on `main`)

Reason:

- fits are made only on rows already labeled `ATTRACT` and `CLEAN`

Current mainline read:

- [`scripts/frontier_wilson_two_body_laws.py`](../scripts/frontier_wilson_two_body_laws.py)
  now presents itself explicitly as a post-selected characterization surface
- the companion Wilson notes say the same thing: these fits are bounded
  calibrations on the clean attractive subset of the audited open surface
- the live Wilson package therefore keeps the narrow calibration claim without
  pretending to be a blind law estimate

Revisit rule:

- do not cite these fits as an unbiased all-row law inference
- redesign the fit surface first if the goal is a blind law estimate or a
  stronger Newton-law closure argument

### 4. Born-rule alpha sweep

**Status on `main`: corrected negative / boundary-of-validity marker; not a
live rerun blocker in its current form**

Affected runner:

- [`scripts/frontier_born_rule_alpha.py`](../scripts/frontier_born_rule_alpha.py)

Reasons:

- ad hoc Hartree stability score, not a measurement-theory test
- also hit by the periodic 2D wraparound-weight bug

Current mainline read:

- the corrected minimum-image surface still does **not** make `alpha=2`
  uniquely selected
- the runner is now framed explicitly as a generalized-density Hartree
  fixed-point smoothness diagnostic, not a Born-rule derivation
- the canonical current-main interpretation lives in:
  - [`docs/BORN_RULE_ANALYSIS_2026-04-11.md`](BORN_RULE_ANALYSIS_2026-04-11.md)
  - [`docs/PERIODIC_2D_WRAPAROUND_FIX_NOTE_2026-04-11.md`](PERIODIC_2D_WRAPAROUND_FIX_NOTE_2026-04-11.md)

Revisit rule:

- do not promote this lane as a measurement-theory or Born-rule-selection result
- no rerun in the current form; the lane needs a different question, not more
  alpha sweeps

### 5. Branch/BMV entanglement classification

**Status on `main`: bounded branch-mediated entanglement package on an
externally imposed two-branch protocol preserved; no longer presented
as a full BMV / gravity-quantumness closure**

Affected runners:

- [`scripts/frontier_bmv_entanglement.py`](../scripts/frontier_bmv_entanglement.py)
- [`scripts/frontier_bmv_threebody.py`](../scripts/frontier_bmv_threebody.py)
- [`scripts/frontier_branch_entanglement_robustness.py`](../scripts/frontier_branch_entanglement_robustness.py)

Reasons:

- 2-body script is a branch-entanglement witness on an externally imposed
  two-branch protocol, not a full BMV result
- 3-body GHZ path is theorem-impossible under the fixed two-branch ansatz, so
  the zero-GHZ row is now treated only as a sanity check, not an empirical
  exclusion result

Action:

- keep the current bounded branch-mediated witness package only for the narrow
  `delta_S > 0` / W-type claims on the externally imposed two-branch protocol
- do not treat the `0/25 GHZ` line as a live rerun blocker on current `main`;
  the current blocker is only for any future attempt to promote this surface
  beyond the bounded two-branch witness framing
- redesign the entanglement witness/classifier before any rerun if the goal is
  a stronger quantum-gravity claim

### 6. Entanglement area-law script

**Status on `main`: retired as evidence; preserved only as a historical
boundary-transfer entropy diagnostic**

Affected runner:

- [`scripts/frontier_entanglement_area_law.py`](../scripts/frontier_entanglement_area_law.py)

Reason:

- it computes channel entropy, not subsystem entanglement entropy

Action:

- do not use this script as live boundary-law evidence
- if boundary-law support is needed on current `main`, use the bounded
  Dirac-sea package instead:
  - [`scripts/frontier_holographic_probe.py`](../scripts/frontier_holographic_probe.py)
  - [`scripts/frontier_boundary_law_robustness.py`](../scripts/frontier_boundary_law_robustness.py)

### 7. Bekenstein-Hawking script

Affected runner:

- [`scripts/frontier_bekenstein_hawking.py`](../scripts/frontier_bekenstein_hawking.py)

Reason:

- it fits Dirac-sea entropy of the final Hamiltonian, not the evolved packet

Action:

- redesign before rerun if the claim is black-hole-like entropy

### 8. Axioms / potential 16-card controls

Affected runners:

- [`scripts/frontier_axioms_16card.py`](../scripts/frontier_axioms_16card.py)
- [`scripts/frontier_staggered_potential_16card.py`](../scripts/frontier_staggered_potential_16card.py)

Reasons:

- non-cubic C11 is tautological
- C13/C14 use flattened-index derivatives, not geometry
- one potential-card row is a self-subtraction tautology

Action:

- redesign those rows before any rerun if the card is meant to carry evidence

### 9. DAG compatibility lane

**Status on `main`: narrowed to a bounded layered-geometry control; no longer
safe to cite as a genuinely directed causal-DAG result**

Affected runner:

- [`scripts/frontier_staggered_dag.py`](../scripts/frontier_staggered_dag.py)

Reason:

- current Hamiltonian uses both edge directions, so it is not a true DAG

Current mainline read:

- the runner and note are now framed as a layered DAG-derived control with
  symmetrized Hermitian transport

Action:

- redesign the operator if the causal-DAG claim is important

## C. Docs Only, No Immediate Rerun

These do not require new numerical work right now; they need narrowed framing.

- [`scripts/frontier_boundary_law_robustness.py`](../scripts/frontier_boundary_law_robustness.py) header/banner

## D. Verified False Positive

Discarded after direct check:

- the claim that [`scripts/frontier_wilson_two_body_open.py`](../scripts/frontier_wilson_two_body_open.py)
  still used a torus-style circular center of mass. It does not.
