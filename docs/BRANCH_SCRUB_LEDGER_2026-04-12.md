# Branch Scrub Ledger

**Date:** 2026-04-12  
**Purpose:** record which source branches have been scrubbed into
`codex/review-active`, what was captured, and whether the source branch is safe
to archive

## Branches

### `origin/claude/youthful-neumann`

Status:

- partially scrubbed into `codex/review-active`

Captured in this pass:

- `docs/EM_GRAVITY_COEXISTENCE_2X2_NOTE.md`
- `scripts/em_gravity_coexistence_2x2.py`
- `docs/DISPERSION_RUNNING_EXPONENT_NOTE.md`
- `scripts/frontier_dispersion_running_exponent.py`
- `docs/HAWKING_BOGOLIUBOV_QUENCH_NOTE.md`
- `scripts/frontier_hawking_bogoliubov_quench.py`
- `docs/DISTANCE_LAW_64_FROZEN_CONTROL_NOTE.md`
- `scripts/frontier_distance_law_64_frozen_control.py`
- `docs/DISTANCE_LAW_DEFINITIVE_NOTE.md`
- `scripts/frontier_distance_law_definitive.py`
- `docs/ACTION_NORMALIZATION_NOTE.md`
- `scripts/frontier_action_normalization.py`
- `docs/BEYOND_LATTICE_QCD_NOTE.md`
- `scripts/frontier_beyond_lattice_qcd.py`
- `docs/DIAMOND_NV_EXPERIMENT_CARD.md`
- `docs/DIAMOND_NV_LATTICE_CORRECTION_NOTE.md`
- `scripts/frontier_diamond_nv_lattice_correction.py`
- `docs/POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md`
- `scripts/frontier_poisson_exhaustive_uniqueness.py`
- `docs/INDEPENDENT_SPATIAL_METRIC_NOTE.md`
- `scripts/frontier_independent_spatial_metric.py`

Already captured before this pass:

- the overnight audit bundle and its narrowed hold notes

Not yet archive-ready:

- yes; do not archive or delete yet

Reason:

- the branch still contains many additional docs/scripts beyond the bounded
  overnight candidates, and those need one more uniqueness pass before the
  branch can be marked fully captured

### `origin/codex/review-final-20260411`

Status:

- superseded by `origin/codex/review-active`

Archive readiness:

- archive-ready once downstream references are switched to `review-active`

### `origin/codex/resonance-controls`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `docs/LENSING_H025_EXACT_EDGE_REFERENCE_NOTE.md`
- `scripts/lensing_adjoint_kernel_reduced_model.py`
- `scripts/infinite_lattice_green_kernel.py`
- `docs/SPECTRAL_DIMENSION_CDT_AUDIT_2026-04-11.md`
- `scripts/frontier_spectral_on_lattice_fluxnorm.py`
- `scripts/frontier_geometric_baseline_control.py`
- `scripts/frontier_phase_strip_control.py`
- `docs/WAVE_DIRECT_DM_H025_FAM3_SEED0_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_THREE_FAMILY_TRANSFER_NOTE.md`
- `docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`
- `docs/WAVE_STATIC_MATRIXFREE_MOVING_SOURCE_FIXED_BEAM_BOUNDARY_NOTE.md`
- `scripts/wave_static_direct_probe.py`

Archive readiness:

- archive-ready

Reason:

- the remaining branch diff after capture is older variants of files already
  preserved on `main` or `codex/review-active`, plus historical logs
- no additional branch-specific science paths remain stranded after the bounded
  historical slice above was imported

### `origin/codex/irregular-sign-closure`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NOTE_2026-04-11.md`
- `scripts/frontier_irregular_endogenous_sign_closure.py`

Archive readiness:

- archive-ready

Reason:

- relative to `origin/frontier/spot-checks`, this branch's unique payload is the
  single shell-packet irregular sign-closure note+runner pair above, and that
  pair is now preserved on the active review branch

### `origin/codex/wilson-temporal-robustness`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `docs/TWO_BODY_ATTRACTION_FROZEN_SOURCE_NOTE_2026-04-11.md`
- `scripts/frontier_two_body_attraction_frozen_source.py`

Archive readiness:

- archive-ready

Reason:

- the branch-specific payload beyond the already-captured Wilson temporal and
  robustness notes is the frozen-source control pair above, and that pair is
  now preserved on the active review branch

### `origin/codex/axiom-risk-ledger`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `docs/AXIOM_RISK_LEDGER.md`

Archive readiness:

- archive-ready

Reason:

- the branch-specific payload is the reviewer-facing axiom risk note above, and
  that note is now preserved on the active review branch

### `origin/codex/next-session-tests`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `scripts/frontier_lorentzian_weakfield_geodesic_refine.py`
- `scripts/frontier_persistent_source_spectrum.py`

Archive readiness:

- archive-ready

Reason:

- the branch-specific payload is future-probe scaffolding for already-open
  lanes, and those scripts are now preserved on the active review branch

### `origin/codex/archive-automation-backup-20260411`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- no new science files needed capture; all branch payload already existed on
  `main` and `codex/review-active`

Archive readiness:

- archive-ready

Reason:

- the direct-`dM` docs, scripts, and logs on this helper branch are already
  preserved on the retained or active review surfaces
- no branch-specific science remains stranded here

### `origin/codex/archive-claude-distracted-napier-20260411`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `docs/K_OSCILLATION_PREDICTION_NOTE.md`
- `scripts/k_oscillation_prediction.py`
- `scripts/lensing_beta_sweep_fine.py`

Archive readiness:

- archive-ready

Reason:

- the branch-specific payload is the bounded lensing `k`-oscillation note and
  its support scripts above, and those artifacts are now preserved on the
  active review branch

### `origin/codex/local-lorentzian-beamsplitter`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `scripts/frontier_local_unitary_lorentzian.py`

Archive readiness:

- archive-ready

Reason:

- the branch-specific payload is the local-unitary Lorentzian beam-splitter
  harness above, and that script is now preserved on the active review branch

### `origin/codex/chiral-harness-tests`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `scripts/frontier_chiral_two_body_superposition.py`

Archive readiness:

- archive-ready

Reason:

- relative to `main` and the active review branch, the remaining unique payload
  on this branch is the narrow chiral two-body superposition diagnostic above,
  and that script is now preserved on review

### Single-artifact `claude/*` capture batch

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `origin/claude/4d-continuum` -> `scripts/four_d_continuum_gap_sweep.py`
- `origin/claude/adaptive-emergence` -> `scripts/adaptive_quantile_emergence.py`
- `origin/claude/assumption-ledger` -> `docs/ASSUMPTION_DERIVATION_LEDGER.md`
- `origin/claude/birth-death` -> `scripts/birth_death_emergence.py`
- `origin/claude/cross-family` -> `scripts/cross_family_robustness.py`
- `origin/claude/emergence-sustain` -> `scripts/emergence_sustain_and_4d.py`
- `origin/claude/fixed-position-alpha` -> `scripts/fixed_position_alpha.py`
- `origin/claude/geometric-growth` -> `scripts/geometric_growth_emergence.py`
- `origin/claude/intelligent-jepsen` -> no unique payload relative to review
- `origin/claude/literature` -> `docs/LITERATURE_POSITIONING_NOTE.md`
- `origin/claude/overnight-2` -> `scripts/overnight_batch_2.py`
- `origin/claude/overnight-3` -> `scripts/overnight_batch_3.py`
- `origin/claude/overnight-4` -> `scripts/overnight_batch_4.py`
- `origin/claude/overnight-deep` -> `scripts/overnight_deep_batch.py`
- `origin/claude/overnight-science` -> `scripts/overnight_batch.py`
- `origin/claude/overnight-verify` -> `scripts/overnight_verification.py`
- `origin/claude/slit-growth` -> `scripts/slit_guided_3d_growth.py`

Archive readiness:

- archive-ready

Reason:

- each branch in this batch either had exactly one unique artifact or no unique
  payload at all
- those artifacts are now preserved on the active review branch as historical
  emergence/continuum scaffolding or reviewer-facing context notes
- no additional branch-specific science remains stranded on these tips

### Small overlapping `claude/*` capture batch

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `origin/claude/continuum-bridge` -> `docs/CONTINUUM_BRIDGE_NOTE.md`
- `origin/claude/docs-update` -> superseded by the captured
  `docs/CONTINUUM_BRIDGE_NOTE.md`
- `origin/claude/review-fixes` -> `docs/CONTINUUM_BRIDGE_NOTE.md`,
  `docs/REVIEWER_SUMMARY.md`
- `origin/claude/reviewer-summary` -> superseded by the captured
  `docs/REVIEWER_SUMMARY.md`
- `origin/claude/predictions` -> `docs/PREDICTION_CARD.md`,
  `scripts/preferential_gravity_diagnosis.py`
- `origin/claude/evolving-network` -> `scripts/self_regulating_gap_3d.py`,
  `scripts/self_regulating_large_n.py`
- `origin/claude/nonlinear-pathsum` -> `scripts/dynamical_reweight_distance_law.py`,
  `scripts/nonlinear_phase_distance.py`

Archive readiness:

- archive-ready

Reason:

- the reviewer-doc overlap is now preserved in the latest available form on the
  active review branch
- the remaining scripts are historical diagnostic harnesses now preserved on
  review
- no additional branch-specific science remains stranded on these tips

### `origin/claude/control-reruns`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- no new capture needed; all branch payload files are already present on the
  active review branch

Archive readiness:

- archive-ready

Reason:

- the branch-specific control-rerun scripts are already preserved on
  `codex/review-active`
- no additional unique science remains stranded on the source branch tip

### `origin/claude/sleepy-cerf`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- no new capture needed; the bounded note+runner pairs already exist on
  `main` or the active review branch

Archive readiness:

- archive-ready

Reason:

- the branch-specific payload is already preserved on the retained or active
  review surfaces
- no additional unique science remains stranded on the source branch tip

### `origin/claude/hierarchical-alpha`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- no new capture needed; `scripts/hierarchical_alpha_study.py` is already on
  the active review branch

Archive readiness:

- archive-ready

Reason:

- the branch is a single-file alias of a script already preserved on review

### `origin/claude/smart-prune`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- no new capture needed; `scripts/smart_prune_emergence.py` is already on the
  active review branch

Archive readiness:

- archive-ready

Reason:

- the branch is a single-file alias of a script already preserved on review

### Historical medium `claude/*` research branches

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `origin/claude/gracious-pasteur` -> historical 3D/4D DAG notes, derivations,
  synthesis docs, and probe scripts already preserved on review
- `origin/claude/distracted-napier` -> historical moonshot/frontier notes,
  derivations, write-ups, and ordered-lattice probe scripts already preserved
  on review

Archive readiness:

- archive-ready

Reason:

- representative spot checks confirm the branch payload is already present on
  the active review branch
- these branches now function as historical provenance only; no additional
  branch-specific science remains stranded on the source tips

### `origin/claude/backreaction-frontier`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `docs/SOURCE_AWARE_MECHANISM_NOTE.md`
- `scripts/backreaction_cross_family.py`
- `scripts/backreaction_stability_map.py`
- `scripts/dense_prune_gravity_repair.py`
- `scripts/directional_b_overlap_onset_continuum_crowding_bridge.py`
- `scripts/directional_b_overlap_onset_midlayer_sampling_holdout.py`
- `scripts/directional_b_overlap_onset_occupancy_load_bridge.py`

Archive readiness:

- archive-ready

Reason:

- the unique branch payload is now preserved on the active review branch
- the remainder of the branch surface is already present on `main` or review as
  historical notes, logs, and scripts
- no additional branch-specific science remains stranded on the source tip

### `origin/claude/youthful-neumann`

Status:

- live working branch; protected from archive/delete

Archive readiness:

- not archive-ready

Reason:

- this branch is an active Claude working directory and should be treated as
  live source material, not as an archive candidate
- capture from it should happen incrementally into `codex/review-active`, but
  the branch itself should not be deleted or pruned while active work continues

### Single-artifact `frontier/*` historical-variant batch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/3d-convergence`
- `origin/frontier/chiral-closure-card`
- `origin/frontier/chiral-wider`
- `origin/frontier/cleanup`
- `origin/frontier/decoherence-suppression`
- `origin/frontier/honest-closure`
- `origin/frontier/local-unitary`
- `origin/frontier/session-writeup`

Archive readiness:

- archive-ready

Reason:

- spot checks confirm these branch tips only differ by historical variants of
  files already preserved on the active review branch
- no branch-specific science paths remain stranded on these source tips

### Two-file `frontier/*` exact-match batch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/chiral-validation`
- `origin/frontier/lorentzian-beamsplitter`

Archive readiness:

- archive-ready

Reason:

- both branch file pairs match the active review branch exactly
- no branch-specific science paths remain stranded on these source tips

### Mixed small `frontier/*` batch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/phase-metric`
- `origin/frontier/lorentzian-closure`

Archive readiness:

- archive-ready

Reason:

- `phase-metric` differs only by older reporting / logging text around files
  already preserved on review
- `lorentzian-closure` carried one branch-specific neighboring-window script;
  that `k=8` card was captured onto review as a historical exploratory variant
- no branch-specific science paths remain stranded on these source tips

### Follow-on small `frontier/*` batch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/synthesis-and-next`
- `origin/frontier/unitary-linear`

Archive readiness:

- archive-ready

Reason:

- `unitary-linear` matches the active review branch exactly
- `synthesis-and-next` differs only by an older overclaiming synthesis doc and
  one script already preserved on review
- no branch-specific science paths remain stranded on these source tips

### Narrow `frontier/*` Lorentzian diagnostic branch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/gravity-diagnosis`

Archive readiness:

- archive-ready

Reason:

- all three scripts are already preserved on review
- the remaining diffs are older, less-cautious Lorentzian/geodesic diagnostic
  wording rather than unique branch-specific science payload
- no branch-specific science paths remain stranded on this source tip

### Exact-match `frontier/*` architecture / chiral batch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/architecture-fork`
- `origin/frontier/chiral-3plus1d`
- `origin/frontier/chiral-higher-dim`

Archive readiness:

- archive-ready

Reason:

- all files in these three branches match the active review branch exactly
- no branch-specific science paths remain stranded on these source tips

### Historical-variant `frontier/*` dynamics / Lorentzian / unitarity batch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/final-fixes`
- `origin/frontier/lorentzian-validation`
- `origin/frontier/review-round7`
- `origin/frontier/unitarity-fix`
- `origin/frontier/spectral-on-lattice`

Archive readiness:

- archive-ready

Reason:

- `review-round7`, `unitarity-fix`, and `spectral-on-lattice` match the active
  review branch exactly on their tracked paths
- `final-fixes` and `lorentzian-validation` differ only by older,
  less-cautious or superseded Lorentzian / spectral framing, with no unique
  science payload left after the earlier review captures
- no branch-specific science paths remain stranded on these source tips

### Historical-variant `frontier/*` growth / dimensionality batch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/cleanup-experiments`
- `origin/frontier/moonshot-round3`

Archive readiness:

- archive-ready

Reason:

- the differing scripts on these branches are older, broader versions of
  growth / dispersion / dimensionality probes already preserved on review
- the active review branch contains the narrowed current forms of the same
  files
- no branch-specific science paths remain stranded on these source tips

### Historical-variant `frontier/*` review-fixes batch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/review-fixes-round6`

Archive readiness:

- archive-ready

Reason:

- the branch combines one exact-match retained two-body valley-linear harness
  with the same older growth / dispersion / dimensionality script variants
  already classified above
- no branch-specific science paths remain stranded on this source tip

### Large `frontier/*` exact-match and historical-variant batch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/resonance`
- `origin/frontier/unified-model`
- `origin/frontier/chiral-moonshots`
- `origin/frontier/critical-gaps`
- `origin/frontier/publication-blockers`
- `origin/frontier/final-two`
- `origin/frontier/final-push`

Archive readiness:

- archive-ready

Reason:

- `resonance`, `unified-model`, and `chiral-moonshots` match the active
  review branch exactly on their tracked paths
- `critical-gaps`, `publication-blockers`, `final-two`, and `final-push`
  differ only by older, less-cautious or superseded script framing on files
  already preserved on review
- no branch-specific science paths remain stranded on these source tips

### Historical-variant `frontier/*` chiral moonshots branch

Status:

- scrubbed into `codex/review-active`

Branches covered in this pass:

- `origin/frontier/final-moonshots`

Archive readiness:

- archive-ready

Reason:

- all tracked paths already exist on the active review branch
- the differing docs and sweep script are older, less-cautious chiral
  synthesis/decoherence variants rather than unique science payload
- no branch-specific science paths remain stranded on this source tip

## Codex First-Pass Triage

These statuses are mechanical only: whether the branch tip is already an
ancestor of `origin/main` or `origin/codex/review-active`. Non-ancestor status
means the branch still needs a uniqueness pass before archive.

### Already subsumed by `main`

- `origin/codex/main-distance-64`
- `origin/codex/main-newton-note`
- `origin/codex/main-open-cubic-validation`
- `origin/codex/main-post-validation`
- `origin/codex/strict-staggered-repro`

### Already subsumed by `review-active`

- `origin/codex/review-final-20260411`
- `origin/codex/main-open-cubic-validation`
- `origin/codex/main-post-validation`
- `origin/codex/strict-staggered-repro`

### Archive-ready now

These branches are already represented by `main` or `codex/review-active` and
do not need further science capture before archive:

- `origin/codex/review-final-20260411`
- `origin/codex/main-open-cubic-validation`
- `origin/codex/main-post-validation`
- `origin/codex/strict-staggered-repro`
- `origin/codex/main-distance-64`
- `origin/codex/main-newton-note`
- `origin/codex/irregular-sign-closure`
- `origin/codex/staggered-direct-com`
- `origin/codex/wilson-temporal-robustness`
- `origin/codex/wilson-temporal-window-lane`
- `origin/codex/main-revisit-sweep`
- `origin/codex/source-weight-spectral`
- `origin/codex/archive-main-retain-audit-20260411`
- `origin/codex/archive-main-wilson-bounded-20260411`
- `origin/codex/archive-automation-backup-20260411`
- `origin/codex/archive-claude-distracted-napier-20260411`
- `origin/codex/axiom-risk-ledger`
- `origin/codex/chiral-harness-tests`
- `origin/codex/local-lorentzian-beamsplitter`
- `origin/codex/next-session-tests`
- `origin/claude/4d-continuum`
- `origin/claude/adaptive-emergence`
- `origin/claude/assumption-ledger`
- `origin/claude/birth-death`
- `origin/claude/cross-family`
- `origin/claude/emergence-sustain`
- `origin/claude/fixed-position-alpha`
- `origin/claude/geometric-growth`
- `origin/claude/intelligent-jepsen`
- `origin/claude/literature`
- `origin/claude/overnight-2`
- `origin/claude/overnight-3`
- `origin/claude/overnight-4`
- `origin/claude/overnight-deep`
- `origin/claude/overnight-science`
- `origin/claude/overnight-verify`
- `origin/claude/slit-growth`
- `origin/claude/continuum-bridge`
- `origin/claude/control-reruns`
- `origin/claude/docs-update`
- `origin/claude/review-fixes`
- `origin/claude/reviewer-summary`
- `origin/claude/predictions`
- `origin/claude/evolving-network`
- `origin/claude/nonlinear-pathsum`
- `origin/claude/hierarchical-alpha`
- `origin/claude/smart-prune`
- `origin/claude/sleepy-cerf`
- `origin/claude/gracious-pasteur`
- `origin/claude/distracted-napier`
- `origin/claude/backreaction-frontier`
- `origin/frontier/3d-convergence`
- `origin/frontier/chiral-closure-card`
- `origin/frontier/chiral-wider`
- `origin/frontier/cleanup`
- `origin/frontier/decoherence-suppression`
- `origin/frontier/honest-closure`
- `origin/frontier/local-unitary`
- `origin/frontier/session-writeup`
- `origin/frontier/chiral-validation`
- `origin/frontier/lorentzian-beamsplitter`
- `origin/frontier/phase-metric`
- `origin/frontier/lorentzian-closure`
- `origin/frontier/synthesis-and-next`
- `origin/frontier/unitary-linear`
- `origin/frontier/gravity-diagnosis`
- `origin/frontier/architecture-fork`
- `origin/frontier/chiral-3plus1d`
- `origin/frontier/chiral-higher-dim`
- `origin/frontier/final-fixes`
- `origin/frontier/lorentzian-validation`
- `origin/frontier/review-round7`
- `origin/frontier/unitarity-fix`
- `origin/frontier/spectral-on-lattice`
- `origin/frontier/cleanup-experiments`
- `origin/frontier/moonshot-round3`
- `origin/frontier/review-fixes-round6`
- `origin/frontier/resonance`
- `origin/frontier/unified-model`
- `origin/frontier/chiral-moonshots`
- `origin/frontier/critical-gaps`
- `origin/frontier/publication-blockers`
- `origin/frontier/final-two`
- `origin/frontier/final-push`
- `origin/frontier/final-moonshots`

### Likely archive-ready after one short verification pass

These appear to be promotion/integration helper branches rather than unique
science branches, but they still need a quick final diff audit before delete:


### Still need uniqueness review before archive

- none remaining in `codex/*`
- `origin/claude/youthful-neumann` remains live and protected; capture from it
  should continue incrementally into `codex/review-active`, but it is not an
  archive candidate while active work continues
- `origin/frontier/spot-checks` has now had its review-missing text artifacts
  imported to `codex/review-active`, but it is still not archive-ready until
  the already-present diff surface is lane-classified
- next scrub stage is the remaining `spot-checks` uniqueness pass and any
  residual helper / automation refs after that
