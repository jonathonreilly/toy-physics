# Rerun-Required Bug Audit — 2026-04-11

This note tracks the validated bugs from the last-week review that require
either reruns or full experiment redesign before any further promotion.

Use this together with:

- [`docs/CODE_REVIEW_LAST_WEEK_2026-04-11.md`](CODE_REVIEW_LAST_WEEK_2026-04-11.md)
- [`docs/repo/RETEST_PLAYBOOK.md`](repo/RETEST_PLAYBOOK.md)
- [`docs/repo/LANE_STATUS_BOARD.md`](repo/LANE_STATUS_BOARD.md)

## A. Fix And Rerun On The Same Lane

These lanes are still scientifically meaningful, but the current runner surface
is buggy enough that the affected claim needs a corrected rerun.

### 1. Periodic 2D staggered wraparound-weight bug

Bug class:

- periodic adjacency is built with modulo indexing
- hopping weights are then computed from raw coordinate differences instead of
  minimum-image distances
- boundary-crossing neighbors are therefore misweighted

Validated affected runners:

- [`scripts/frontier_born_rule_alpha.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_born_rule_alpha.py)
- [`scripts/frontier_self_consistency_test.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_self_consistency_test.py)
- [`scripts/frontier_eigenvalue_stats_and_anderson_phase.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_eigenvalue_stats_and_anderson_phase.py)

Likely same bug pattern also touches nearby periodic 2D frontier probes built
with the same helper structure. Before promoting any periodic 2D result from
the 2026-04-11 frontier batch, check whether it uses this pattern.

Required reruns after fix:

- self-consistency comparisons
- Anderson / eigenvalue phase map
- any periodic 2D derived follow-on note that depends on those surfaces

### 2. Self-consistency random controls are not moment-matched

Affected runner:

- [`scripts/frontier_self_consistency_test.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_self_consistency_test.py)

Bug:

- positive/negative random controls use `abs(normal(mean, std))`
- this changes the effective mean and variance
- sign/correlation comparisons are confounded

Required rerun:

- rerun the full self-consistency comparison after replacing the random controls
  with true moment-matched nulls

### 3. Two-field wave family robustness is not independent

Affected runner:

- [`scripts/frontier_two_field_wave.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_two_field_wave.py)

Bug:

- family checks inherit the already evolved field state

Required rerun:

- rerun `W6` from clean restarts per family

### 4. Retarded probe R9 cannot fail

Affected runner:

- [`scripts/frontier_two_field_retarded_probe.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_two_field_retarded_probe.py)

Bug:

- the scale-gap row increments the score unconditionally

Required rerun:

- only if you want R9 to count as a real gate
- fix scoring first, then rerun the retarded scale-gap surface

### 5. Decoherence distance sweep aliases torus separations

Affected runner:

- [`scripts/frontier_gravitational_decoherence_rate.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_gravitational_decoherence_rate.py)

Bug:

- `d = 6, 8` on a periodic `10x10` torus are not clean long-range separations

Required rerun:

- redo the `Gamma(d)` law on an open surface or a torus protocol with distinct
  minimum-image separations

### 6. Geometry-superposition added-edge DAG variant is broken

Affected runner:

- [`scripts/frontier_geometry_superposition.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_geometry_superposition.py)

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

Affected runner:

- [`scripts/frontier_two_body_mutual_attraction.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_two_body_mutual_attraction.py)

Reason:

- one wavefunction with two lobes, not a true two-body channel

Action:

- do not rerun this for evidence
- use the two-orbital / Wilson harness family instead

### 2. Periodic Wilson “Newton law” runner

Affected runner:

- [`scripts/frontier_wilson_newton_law.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_wilson_newton_law.py)

Reasons:

- periodic torus, not image-free
- “mass law” only rescales partner source strength

Action:

- do not rerun as a Newton test
- if the law lane continues, rerun only on the open Wilson surface with a
  physically meaningful source/inertial parameterization

### 3. Wilson law-fit scripts use post-selected survivor rows

Affected runners:

- [`scripts/frontier_wilson_two_body_laws.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_wilson_two_body_laws.py)
- [`scripts/frontier_wilson_partner_source_crossover.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_wilson_partner_source_crossover.py)

Reason:

- fits are made only on rows already labeled `ATTRACT` and `CLEAN`

Action:

- redesign the fit surface first if you want a blind law estimate

### 4. Born-rule alpha sweep

Affected runner:

- [`scripts/frontier_born_rule_alpha.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_born_rule_alpha.py)

Reasons:

- ad hoc Hartree stability score, not a measurement-theory test
- also hit by the periodic 2D wraparound-weight bug

Action:

- no rerun in the current form
- the lane needs a different question, not more alpha sweeps

### 5. Branch/BMV entanglement classification

Affected runners:

- [`scripts/frontier_bmv_entanglement.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_bmv_entanglement.py)
- [`scripts/frontier_bmv_threebody.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_bmv_threebody.py)
- [`scripts/frontier_branch_entanglement_robustness.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_branch_entanglement_robustness.py)

Reasons:

- 2-body script is a toy branch witness, not a full BMV result
- 3-body GHZ path is dead / impossible under the current classifier

Action:

- redesign the entanglement witness/classifier before any rerun if the goal is
  a stronger quantum-gravity claim

### 6. Entanglement area-law script

Affected runner:

- [`scripts/frontier_entanglement_area_law.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_entanglement_area_law.py)

Reason:

- it computes channel entropy, not subsystem entanglement entropy

Action:

- no rerun until the measured object is changed

### 7. Bekenstein-Hawking script

Affected runner:

- [`scripts/frontier_bekenstein_hawking.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_bekenstein_hawking.py)

Reason:

- it fits Dirac-sea entropy of the final Hamiltonian, not the evolved packet

Action:

- redesign before rerun if the claim is black-hole-like entropy

### 8. Axioms / potential 16-card controls

Affected runners:

- [`scripts/frontier_axioms_16card.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_axioms_16card.py)
- [`scripts/frontier_staggered_potential_16card.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_potential_16card.py)

Reasons:

- non-cubic C11 is tautological
- C13/C14 use flattened-index derivatives, not geometry
- one potential-card row is a self-subtraction tautology

Action:

- redesign those rows before any rerun if the card is meant to carry evidence

### 9. DAG compatibility lane

Affected runner:

- [`scripts/frontier_staggered_dag.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_dag.py)

Reason:

- current Hamiltonian uses both edge directions, so it is not a true DAG

Action:

- redesign the operator if the causal-DAG claim is important

## C. Docs Only, No Immediate Rerun

These do not require new numerical work right now; they need narrowed framing.

- [`docs/SESSION_SYNTHESIS_2026-04-11.md`](SESSION_SYNTHESIS_2026-04-11.md)
- [`docs/FINAL_STATE_2026-04-11.md`](FINAL_STATE_2026-04-11.md)
- [`scripts/frontier_boundary_law_robustness.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_boundary_law_robustness.py) header/banner

## D. Verified False Positive

Discarded after direct check:

- the claim that [`scripts/frontier_wilson_two_body_open.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_wilson_two_body_open.py)
  still used a torus-style circular center of mass. It does not.
