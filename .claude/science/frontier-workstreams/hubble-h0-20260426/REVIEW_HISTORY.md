# Hubble H_0 — Review History

**Workstream:** `hubble-h0-20260426`

This file records the `review-loop` disposition for each major artifact
produced in the workstream.

## Cycle 0 — pack scaffold

- **Date:** 2026-04-26
- **Artifacts:** STATE.yaml, GOAL.md, ASSUMPTIONS_AND_IMPORTS.md,
  NO_GO_LEDGER.md, ROUTE_PORTFOLIO.md, ARTIFACT_PLAN.md,
  LITERATURE_BRIDGES.md, REVIEW_HISTORY.md, HANDOFF.md
- **Review:** internal grounding-phase audit only; pack content reflects the
  current Lane 5 file and retained cosmology theorem stack as of this
  branch's `origin/main` baseline.
- **Findings:** none requiring action; pack is stable for Cycle 1 entry.
- **Disposition:** pack scaffold accepted; Cycle 1 (R4) authorized.

## Cycle 1 — R4 Hubble Tension Structural Lock theorem

- **Date:** 2026-04-26
- **Artifacts:**
  - `docs/HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md`
  - `scripts/frontier_hubble_tension_structural_lock.py`
  - `logs/2026-04-26-hubble-tension-structural-lock.txt`
- **Review mode:** branch-local self-review against the standard reviewer
  criteria (CodeRunnerReviewer, PhysicsClaimReviewer,
  ImportSupportReviewer, NatureRetentionReviewer, RepoGovernanceReviewer,
  MethodologySkillReviewer). The full multi-agent `/review-loop` skill is
  reserved for the post-workstream integration step per skill delivery
  policy.
- **Findings:**
  1. **CodeRunnerReviewer (PASS).** All 5 runner checks pass: continuity
     ODE solved exactly for `w in {0, 1/3, -1}`; Friedmann reduction (★)
     verified symbolically; lock corollary `H_0_implied(a) = H_0` verified
     symbolically; numerical Lambda-CDM scan over `z in [0, 1]` gives
     constant `H_0_implied` to floating-point precision; modified-DE stress
     test produces zero spread at `delta = 0` and growing spread for
     `delta != 0` (operational falsifier).
     - Sub-finding: initial run had a 3.1e-3 km/s/Mpc deviation in the
       numerical sub-check at `a = 1` because the comparator triple
       `(Omega_m=0.315, Omega_Lambda=0.685)` did not include radiation.
       Fixed by deriving `Omega_Lambda` from flatness given fixed
       `(Omega_m, Omega_r)`. Shift is Omega_r ~ 9.2e-5, well inside the
       Planck quoted uncertainty.
  2. **PhysicsClaimReviewer (PASS after edit).** Theorem statement matches
     proof. Initial draft listed three premises, but the proof only used
     `(P1) w_Lambda = -1` and `(P2) flat FRW`; the spectral-gap identity
     was framework grounding, not load-bearing for `(★)`. **Edit applied:**
     §0 now lists two premises with the framework grounding moved to a
     clarifying paragraph; §2-§4 references updated to `(P1)`/`(P2)` only.
  3. **ImportSupportReviewer (PASS).** All imports identified in
     `ASSUMPTIONS_AND_IMPORTS.md`; the theorem itself imports only the
     retained `w_Lambda = -1` and FRW textbook structure. Comparators
     (Planck 2018, SH0ES 2022) flagged in `LITERATURE_BRIDGES.md` and used
     only as comparators in the runner.
  4. **NatureRetentionReviewer (PASS).** Theorem note explicitly scoped as
     "retained structural-identity theorem on `main`-compatible surface,
     landed branch-locally on `frontier/hubble-h0-20260426` for later
     review-and-integration". Falsifier explicit and operational. No
     hidden semantic bridge: the proof uses only declared premises.
  5. **RepoGovernanceReviewer (PASS).** Theorem note in `docs/` with
     date-suffix convention. Runner in `scripts/` with `frontier_*`
     prefix. Log in `logs/`. Workstream pack at
     `.claude/science/frontier-workstreams/hubble-h0-20260426/`. No
     repo-wide authority surface (LANE_REGISTRY, ACTIVE_REVIEW_QUEUE,
     INPUTS_AND_QUALIFIERS_NOTE, WHAT_THIS_PAPER_DOES_NOT_CLAIM,
     CLAIMS_TABLE) updated on this branch — proposed weaves recorded in
     `HANDOFF.md` per skill science-only delivery policy.
  6. **MethodologySkillReviewer (PASS).** Workflow followed: pack scaffold
     committed before science cycle; grounding done from authority
     surfaces; assumptions/imports audited; no-go ledger acknowledges
     adjacent Planck and DM lanes; route portfolio scored under the
     dramatic-step gate; selected route R4 produces a
     novel-structure-with-falsifier artifact (manuscript-grade); review
     findings recorded here; STATE.yaml will be checkpointed.
- **Disposition:** Cycle 1 accepted. Theorem note + runner + log committed
  to branch. Edit applied to tighten premise count from 3 to 2.
- **Next:** STATE.yaml checkpoint, branch push, then evaluate continuation.

## Cycle 2 — R3 Cosmology Open-Number Reduction theorem

- **Date:** 2026-04-26
- **Artifacts:**
  - `docs/COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`
  - `scripts/frontier_cosmology_open_number_reduction.py`
  - `logs/2026-04-26-cosmology-open-number-reduction.txt`
- **Review mode:** same branch-local 6-criterion self-review as Cycle 1.
- **Findings:**
  1. **CodeRunnerReviewer (PASS after 2 fixes).**
     - Initial run had `R_Lambda` numerical sub-check FAIL because the
       expected range was set to ~14 Gpc (a misremembered Hubble-radius
       value). Correct value `R_Lambda = c/H_inf ≈ 5.4 Gpc` per the
       2026-04-22 matter-bridge note. Range corrected to 5000-5800 Mpc.
     - Initial theorem-note table had `1 + z_mLambda = ((1 - L - R)/L)^{1/3}`
       which is the inverse of the correct formula. The runner symbolic
       check matched the correct version `(L / (1 - L - R))^{1/3}`.
       Theorem note updated to match.
  2. **PhysicsClaimReviewer (PASS).** Theorem packages prior retained
     identities (matter-bridge 2026-04-22, single-ratio inverse
     reconstruction 2026-04-25, structural lock 2026-04-26) into one
     parameter-count statement. Statement matches proof. The "no fourth
     class of derivation" §3.2 is the program-bounding component.
  3. **ImportSupportReviewer (PASS).** No new imports beyond the retained
     surface and Cycle-1 theorem.
  4. **NatureRetentionReviewer (PASS, borderline).** The theorem is more
     a parameter-count statement than a strongly falsifiable prediction;
     §3.2 ("no fourth derivation class") provides the operational
     program-bounding content. Scoping language matches Cycle 1
     ("retained structural-identity theorem on `main`-compatible surface,
     landed branch-locally").
  5. **RepoGovernanceReviewer (PASS).** Same conventions as Cycle 1.
  6. **MethodologySkillReviewer (PASS).** Cycle 2 follows logically from
     Cycle 1, builds on retained items, adds a real claim
     (`|open numbers in S| = 2`), not pure prose.
- **Disposition:** Cycle 2 accepted. Theorem note + runner + log
  committed to branch.

## Cycle 3 — R7 Lane 5 Cosmic-History-Ratio Necessity No-Go

- **Date:** 2026-04-26
- **Artifacts:**
  - `docs/HUBBLE_LANE5_COSMIC_HISTORY_RATIO_NECESSITY_NO_GO_NOTE_2026-04-26.md`
  - (no runner — structural case-analysis on `A_min` and the retained
    cosmology stack)
- **Review mode:** branch-local 6-criterion self-review.
- **Findings:**
  1. **CodeRunnerReviewer (PASS).** No runner authored. The skill allows
     note-only artifacts for no-gos when the proof is structural. The
     case-analysis in §2 (dimensional argument) and §3 (cosmic-history
     enumeration) is verified by inspection.
  2. **PhysicsClaimReviewer (PASS after one strengthening edit).** The
     initial closure-pathway corollary said Lane 5 closure requires "at
     least one premise from `{(C1), (C2), (C3)}`". Strengthened to
     "`(C1)` AND one of `{(C2), (C3)}`" — neither alone is sufficient
     because `(C1)` fixes scale but not `L`, while `(C2)/(C3)` fix `L`
     but not the absolute time scale. §0 statement and §4 corollary
     both updated.
  3. **ImportSupportReviewer (PASS).** All cited identities are on the
     retained surface or landed Cycle-1/Cycle-2 branch-locally. No new
     external imports.
  4. **NatureRetentionReviewer (PASS).** Scoped as
     "retained no-go theorem on `main`-compatible surface, landed
     branch-locally". Falsifier explicit (existential — exhibit a
     counterexample). Boundary §9 explicitly notes the no-go does not
     claim any of `(C1)`, `(C2)`, `(C3)` is impossible.
  5. **RepoGovernanceReviewer (PASS).** Note placed in `docs/` with
     `*_NO_GO_NOTE_2026-04-26.md` suffix matching the 50+ existing
     no-go notes. No repo-wide authority weave; proposed weaves go to
     `HANDOFF.md`.
  6. **MethodologySkillReviewer (PASS).** Cycle 3 follows logically from
     Cycle 2 by formalizing the "no fourth class of derivation"
     program-bounding statement. Real claim-state movement (no-go
     proven, taxonomy established). Note-only is appropriate for
     axiomatic no-gos per the skill.
- **Disposition:** Cycle 3 accepted. No-go theorem committed to branch.

## Cycle 4+ — pending evaluation

With the closure-pathway taxonomy `{(C1), (C2), (C3)}` established,
strongest single-cycle candidates are now:

- **eta retirement gate audit** (advances `(C2)`): identify the minimal
  selector/normalization closure for the surviving DM leptogenesis
  branches.
- **Planck conditional-completion review** (advances `(C1)`
  understanding): audit the gravitational boundary/action carrier
  identification gate.
- **Direct cosmic-`L` proposal exploration** (would open `(C3)`): assess
  whether any framework-internal vacuum/topology argument could give
  `L = Omega_Lambda` without going through the matter cascade.

Loop continues per ScheduleWakeup.

