# Claude Frontier Retain Audit — 2026-04-11

**Purpose:** classify the late 2026-04-11 Claude frontier batch into:

- safe to retain on `main`
- frontier-only until further audit
- fix/rerun or redesign before reuse

This note is about the **recent Claude frontier wave**, not the whole repo.
Use it with:

- [CODE_REVIEW_LAST_WEEK_2026-04-11.md](CODE_REVIEW_LAST_WEEK_2026-04-11.md)
- [RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md](RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md)
- [PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md](PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md)
- [repo/LANE_STATUS_BOARD.md](repo/LANE_STATUS_BOARD.md)

## Retain To `main`

These items are useful, honestly framed, and coherent enough to become part of
the repo baseline.

### 1. Review / rerun control-plane hardening

Keep:

- [CODE_REVIEW_LAST_WEEK_2026-04-11.md](CODE_REVIEW_LAST_WEEK_2026-04-11.md)
- [RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md](RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md)

Why:

- they capture the real bugs from the last-week frontier surface
- they stop stale or invalid runners from being silently promoted

### 2. Wilson `mu^2` distance calibration

Keep:

- [WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md](WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md)
- [scripts/frontier_wilson_mu2_distance_sweep.py](../scripts/frontier_wilson_mu2_distance_sweep.py)

Why:

- this is the cleanest diagnosis of the steep Wilson distance exponent
- the current note is careful: it says the exponent is **screening-controlled**
  and becomes Newton-compatible as `mu^2` is reduced
- it does **not** overclaim full Newton closure

### 3. Wilson test-mass / continuum companion

Keep:

- [WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md](WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md)
- [scripts/frontier_wilson_two_body_open.py](scripts/frontier_wilson_two_body_open.py)
- [scripts/frontier_wilson_two_body_laws.py](scripts/frontier_wilson_two_body_laws.py)
- [scripts/frontier_test_mass_limit.py](scripts/frontier_test_mass_limit.py)
- [scripts/frontier_perturbative_mass_law.py](scripts/frontier_perturbative_mass_law.py)
- [scripts/frontier_continuum_limit.py](scripts/frontier_continuum_limit.py)
- [scripts/frontier_newton_systematic.py](scripts/frontier_newton_systematic.py)
- [WILSON_NORMALIZATION_RECONCILIATION_NOTE_2026-04-11.md](WILSON_NORMALIZATION_RECONCILIATION_NOTE_2026-04-11.md)

Why:

- this is the strongest bounded Newton-strengthening package on the Wilson lane
- the note keeps the result inside its actual closure surface:
  - exact test-mass source scaling
  - same-convention continuum fit converging to `-2`
  - no both-masses closure claim
- it also resolves the normalization-review concern by framing the batch as
  same-convention Wilson evidence, not a global cross-runner verdict

### 4. Memory `mu^2` / geometry diagnostic

Keep:

- [MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md](MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md)
- [scripts/frontier_memory_mu2_size_sweep.py](../scripts/frontier_memory_mu2_size_sweep.py)

Why:

- it corrects an important false simplification
- the honest result is that memory fragility is **not purely** a Yukawa-range
  effect; geometry scaling and boundary placement matter at least as much

### 5. Born-rule boundary marker

Keep:

- [BORN_RULE_ANALYSIS_2026-04-11.md](BORN_RULE_ANALYSIS_2026-04-11.md)

Why:

- it is a useful boundary statement, not a positive claim
- it correctly says the old alpha sweep was probing fixed-point smoothness, not
  measurement theory

### 6. Spectral / trajectory theory memo

Keep as a memo, not a theorem:

- [SPECTRAL_TRAJECTORY_THEOREM_2026-04-11.md](SPECTRAL_TRAJECTORY_THEOREM_2026-04-11.md)

Why:

- it is a coherent organizing document for the current scientific state
- it should be read as an interpretive framework built from the repo record,
  not as a proven theorem

### 7. Bounded staggered open-cubic trajectory companions

Keep:

- [STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md](STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md)
- [STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md](STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md)
- [STAGGERED_3D_SELF_GRAVITY_SIGN_NOTE_2026-04-11.md](STAGGERED_3D_SELF_GRAVITY_SIGN_NOTE_2026-04-11.md)
- [scripts/frontier_staggered_newton_reproduction.py](../scripts/frontier_staggered_newton_reproduction.py)
- [scripts/frontier_staggered_newton_blocking_sensitivity.py](../scripts/frontier_staggered_newton_blocking_sensitivity.py)
- [scripts/frontier_staggered_3d_self_gravity_sign.py](../scripts/frontier_staggered_3d_self_gravity_sign.py)

Why:

- they are honestly framed bounded companions on the **primary staggered
  architecture**
- the external-source open-cubic lane now shows a Newton-compatible
  trajectory-distance law with sensible blocking, not just with one tuned
  `2x2x2` readout
- the 3D self-gravity note adds a real trajectory-level staggered positive
  while also freezing the negative sign-closure result on the same centered
  surface

Retention boundary:

- these are **not** full Newton closure
- they are **not** both-masses closure
- they are **not** irregular-graph transfer
- they should move with their runner/note pairs, not as standalone control-plane
  prose

### 6B. Bounded staggered self-consistent two-body force companion

Keep:

- [STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md](STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md)
- [scripts/frontier_staggered_self_consistent_two_body.py](../scripts/frontier_staggered_self_consistent_two_body.py)

Why:

- this is a real primary-architecture positive beyond external-source forcing
- the exact partner-only force channel reruns cleanly with a near-Newton
  distance law on the calibrated open-cubic surface
- the note is already honest that the trajectory channel is still noisy and
  that this does not close both-masses or full staggered Newton

Retention boundary:

- force-led, not trajectory-closed
- calibrated open-cubic surface only
- not a retained both-masses law

### 6C. Bounded staggered weak-field source-mass companion

Keep:

- [STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md](STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md)
- [scripts/frontier_staggered_test_mass_companion.py](../scripts/frontier_staggered_test_mass_companion.py)

Why:

- this is the primary-architecture analogue of the retained Wilson weak-field
  test-mass/source-mass logic
- the note is explicit that the source is static and the test packet is
  normalized
- the audited weak-field surface gives exact source scaling in the force
  channel and near-linear source scaling in the blocked-envelope trajectory
  companion

Retention boundary:

- source-only, not both-masses
- static-source, not self-consistent two-body
- not a standalone distance-law closure

### 6D. Bounded irregular core-packet sign separator

Keep:

- [IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md](IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md)
- [scripts/frontier_irregular_sign_core_packet_gate.py](../scripts/frontier_irregular_sign_core_packet_gate.py)

Why:

- this is the first bounded same-surface irregular sign-separation result that
  survives both the screened and low-screening replay on the audited families
- it does not lean on cubic exact-force semantics; it is a same-surface matter
  response readout on the irregular graph families themselves
- it cleanly narrows the older blocker: the shell/off-center/transport-style
  failures were real, but they no longer justify saying no such irregular
  observable exists at all

Retention boundary:

- core-packet surface only
- audited families and operating window only
- not transport portability
- not packet-family universality
- not full off-lattice directional-gravity closure

### 8. Corrected periodic-2D rerun surface

Keep:

- [PERIODIC_2D_WRAPAROUND_FIX_NOTE_2026-04-11.md](PERIODIC_2D_WRAPAROUND_FIX_NOTE_2026-04-11.md)
- [SELF_CONSISTENCY_STRUCTURED_NULL_NOTE_2026-04-11.md](SELF_CONSISTENCY_STRUCTURED_NULL_NOTE_2026-04-11.md)
- [EIGENVALUE_ANDERSON_PHASE_NOTE_2026-04-11.md](EIGENVALUE_ANDERSON_PHASE_NOTE_2026-04-11.md)
- [scripts/frontier_self_consistency_test.py](../scripts/frontier_self_consistency_test.py)
- [scripts/frontier_eigenvalue_stats_and_anderson_phase.py](../scripts/frontier_eigenvalue_stats_and_anderson_phase.py)
- [scripts/frontier_born_rule_alpha.py](../scripts/frontier_born_rule_alpha.py)

Why:

- the validated minimum-image wraparound bug has now been fixed in these
  runners
- the corrected reruns preserve bounded fixed-surface self-consistency and the
  finite Anderson-vs-disorder window
- the Born-rule alpha lane is worth preserving only as a corrected negative /
  boundary-of-validity marker, not as a measurement-theory derivation

### 7B. Unscreened periodic Anderson companion

Keep:

- [ANDERSON_PHASE_MU2_0001_NOTE_2026-04-11.md](ANDERSON_PHASE_MU2_0001_NOTE_2026-04-11.md)
- [scripts/frontier_anderson_phase_unscreened_periodic.py](../scripts/frontier_anderson_phase_unscreened_periodic.py)

Why:

- the unscreened rerun reproduces the note cleanly
- it preserves the corrected periodic torus lane while clarifying that the
  disorder separation changes character under unscreening
- it remains careful about sign being a weak discriminator on this surface

### 9. Bounded Ollivier curvature proxy

Keep:

- [OLLIVIER_EINSTEIN_PROXY_NOTE_2026-04-11.md](OLLIVIER_EINSTEIN_PROXY_NOTE_2026-04-11.md)
- [scripts/frontier_ollivier_einstein.py](../scripts/frontier_ollivier_einstein.py)
- [scripts/frontier_ollivier_control.py](../scripts/frontier_ollivier_control.py)

Why:

- the note is now honest about what survives
- the retained claim is a bounded potential-weighted structured-curvature proxy
- the note explicitly rules out the stronger Einstein-equation overclaim

### 10. Wilson two-body hardening notes

Keep:

- [WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md](WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md)
- [TWO_BODY_MUTUAL_ATTRACTION_NOTE_2026-04-11.md](TWO_BODY_MUTUAL_ATTRACTION_NOTE_2026-04-11.md)

Why:

- they preserve the current honest state of the two-body lane
- they keep the clean open-surface mutual channel while explicitly recording
  the failed both-masses closure
- this prevents the later frontier Newton overclaim from becoming repo truth

## Frontier-Only For Now

These are not necessarily wrong, but they are not yet `main`-grade.

### 1. Full Newton-law headline

Do not retain as a repo truth yet:

- `scripts/frontier_wilson_unscreened.py`
- `scripts/frontier_wilson_newton_law.py`
- `scripts/frontier_newton_both_masses.py`

Reason:

- the distance-law side is now much stronger
- the mass-law side is still not closed on a valid both-masses runner
- the old periodic Wilson runner only tested source-strength scaling

Current honest baseline:

> the open Wilson distance exponent is strongly controlled by `mu^2` and
> becomes Newton-compatible as screening is reduced; full Newton closure is
> still pending a valid both-masses law on the same surface

### 2. BMV / branch-entanglement extensions

Keep bounded retained notes that are already honest, but do not promote the
stronger new frontier claims yet.

Reason:

- current branch/BMV runners still do not implement a full gravity-quantumness
  witness
- the corrected bounded 2-body and W-type 3-body notes are already enough for
  `main`

### 3. Graph selection, topological, CDT quantitative, Hartree N-body,
mirror Z2, error correction

Leave on frontier until separately audited.

Reason:

- others are plausible but still only represented by a fresh frontier script
  plus a claim-heavy session narrative

### 4. Screening-fix global narrative

Do not retain [SCREENING_FIX_RECHECK_LIST_2026-04-11.md](SCREENING_FIX_RECHECK_LIST_2026-04-11.md) to `main` as written.

Reason:

- it overstates the shared diagnosis
- `mu^2 = 0.22` was a major confound for some lanes, but not the universal root
  cause of everything involving Poisson coupling

## Fix / Rerun Or Redesign Before Reuse

Use [RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md](RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md) as the detailed source. The highest-priority items are:

### 1. Periodic 2D wraparound-weight bug

Affected examples:

- `scripts/frontier_self_consistency_test.py`
- `scripts/frontier_eigenvalue_stats_and_anderson_phase.py`
- `scripts/frontier_born_rule_alpha.py`

Impact:

- the bug is now fixed and rerun on these three headline scripts
- any additional periodic-2D follow-on claims outside the retained rerun notes
  should still be treated as untrusted until separately rerun

### 2. Self-consistency random controls

Affected:

- `scripts/frontier_self_consistency_test.py`

Impact:

- the corrected structured-null rerun is now the retained baseline
- older iid-random-control framings should not be reused

### 3. Invalid or redesign-only claim surfaces

Do not rerun in current form:

- `scripts/frontier_two_body_mutual_attraction.py`
- `scripts/frontier_wilson_newton_law.py`
- `scripts/frontier_entanglement_area_law.py`
- `scripts/frontier_bekenstein_hawking.py`

## Practical Reading Rule

If a recent Claude result is only present in:

- a new `frontier_*` runner
- a session summary
- and no honest retained note

then treat it as **frontier-only** until this audit is updated.
