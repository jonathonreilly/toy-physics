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

**Status on `main`: corrected on the retained trio; still a live bug pattern
for nearby periodic-2D surfaces**

Bug class:

- periodic adjacency is built with modulo indexing
- hopping weights are then computed from raw coordinate differences instead of
  minimum-image distances
- boundary-crossing neighbors are therefore misweighted

Validated affected runners:

- [`scripts/frontier_born_rule_alpha.py`](../scripts/frontier_born_rule_alpha.py)
- [`scripts/frontier_self_consistency_test.py`](../scripts/frontier_self_consistency_test.py)
- [`scripts/frontier_eigenvalue_stats_and_anderson_phase.py`](../scripts/frontier_eigenvalue_stats_and_anderson_phase.py)

Likely same bug pattern also touches nearby periodic 2D frontier probes built
with the same helper structure. Before promoting any periodic 2D result from
the 2026-04-11 frontier batch, check whether it uses this pattern.

Corrected retained reruns now exist on `main` for:

- [`scripts/frontier_self_consistency_test.py`](../scripts/frontier_self_consistency_test.py)
- [`scripts/frontier_eigenvalue_stats_and_anderson_phase.py`](../scripts/frontier_eigenvalue_stats_and_anderson_phase.py)
- [`scripts/frontier_born_rule_alpha.py`](../scripts/frontier_born_rule_alpha.py)

Revisit rule:

- any *other* periodic 2D result outside those corrected retained notes should
  still be rerun or code-audited before reuse

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

Affected runner:

- [`scripts/frontier_two_field_retarded_probe.py`](../scripts/frontier_two_field_retarded_probe.py)

Bug:

- the scale-gap row increments the score unconditionally

Required rerun:

- only if you want R9 to count as a real gate
- fix scoring first, then rerun the retarded scale-gap surface

### 5. Decoherence distance sweep aliases torus separations

Affected runner:

- [`scripts/frontier_gravitational_decoherence_rate.py`](../scripts/frontier_gravitational_decoherence_rate.py)

Bug:

- `d = 6, 8` on a periodic `10x10` torus are not clean long-range separations

Required rerun:

- redo the `Gamma(d)` law on an open surface or a torus protocol with distinct
  minimum-image separations

### 6. Geometry-superposition added-edge DAG variant is broken

Affected runner:

- [`scripts/frontier_geometry_superposition.py`](../scripts/frontier_geometry_superposition.py)

Bug:

- the added-edge DAG builder can break after the first failed draw, often
  returning essentially no added edges

Required rerun:

- if the added-edge comparison still matters, fix the loop and rerun the
  perturbation-family comparison

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

Affected runner:

- historical frontier-only runner `frontier_wilson_newton_law.py`
  (not retained on `main`)

Reasons:

- periodic torus, not image-free
- “mass law” only rescales partner source strength

Action:

- do not rerun as a Newton test
- if the law lane continues, rerun only on the open Wilson surface with a
  physically meaningful source/inertial parameterization:
  - [`scripts/frontier_wilson_mu2_distance_sweep.py`](../scripts/frontier_wilson_mu2_distance_sweep.py)
  - [`scripts/frontier_test_mass_limit.py`](../scripts/frontier_test_mass_limit.py)
  - [`scripts/frontier_continuum_limit.py`](../scripts/frontier_continuum_limit.py)

### 3. Wilson law-fit scripts use post-selected survivor rows

Affected runners:

- [`scripts/frontier_wilson_two_body_laws.py`](../scripts/frontier_wilson_two_body_laws.py)
- historical frontier-only runner `frontier_wilson_partner_source_crossover.py`
  (not retained on `main`)

Reason:

- fits are made only on rows already labeled `ATTRACT` and `CLEAN`

Action:

- redesign the fit surface first if you want a blind law estimate

### 4. Born-rule alpha sweep

Affected runner:

- [`scripts/frontier_born_rule_alpha.py`](../scripts/frontier_born_rule_alpha.py)

Reasons:

- ad hoc Hartree stability score, not a measurement-theory test
- also hit by the periodic 2D wraparound-weight bug

Action:

- no rerun in the current form
- the lane needs a different question, not more alpha sweeps

### 5. Branch/BMV entanglement classification

Affected runners:

- [`scripts/frontier_bmv_entanglement.py`](../scripts/frontier_bmv_entanglement.py)
- [`scripts/frontier_bmv_threebody.py`](../scripts/frontier_bmv_threebody.py)
- [`scripts/frontier_branch_entanglement_robustness.py`](../scripts/frontier_branch_entanglement_robustness.py)

Reasons:

- 2-body script is a toy branch witness, not a full BMV result
- 3-body GHZ path is dead / impossible under the current classifier

Action:

- redesign the entanglement witness/classifier before any rerun if the goal is
  a stronger quantum-gravity claim

### 6. Entanglement area-law script

Affected runner:

- [`scripts/frontier_entanglement_area_law.py`](../scripts/frontier_entanglement_area_law.py)

Reason:

- it computes channel entropy, not subsystem entanglement entropy

Action:

- no rerun until the measured object is changed

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

- [`docs/SESSION_SYNTHESIS_2026-04-11.md`](SESSION_SYNTHESIS_2026-04-11.md)
- [`docs/FINAL_STATE_2026-04-11.md`](FINAL_STATE_2026-04-11.md)
- [`scripts/frontier_boundary_law_robustness.py`](../scripts/frontier_boundary_law_robustness.py) header/banner

## D. Verified False Positive

Discarded after direct check:

- the claim that [`scripts/frontier_wilson_two_body_open.py`](../scripts/frontier_wilson_two_body_open.py)
  still used a torus-style circular center of mass. It does not.
