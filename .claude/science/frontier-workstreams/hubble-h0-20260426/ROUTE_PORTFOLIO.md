# Hubble H_0 — Route Portfolio

**Date:** 2026-04-26
**Workstream:** `hubble-h0-20260426`
**Purpose:** independent routes toward Lane 5 closure, scored by likely
claim-state movement under the dramatic-step gate.

## Scoring rubric

Each route is scored on:

- **Tier**: A (≤1 session), B (1-4 sessions), C (program-scale)
- **Claim-state move**: retire-import / exact-support / no-go / blocker-isolation / novel-structure
- **Falsifier**: explicit, ambiguous, or none
- **Blockers**: open dependencies on other lanes

Dramatic-step gate: a route is admissible only if it can produce one of
{import retired, exact support added, no-go proven, major blocker isolated,
novel structure with falsifier} in a single major cycle.

## Routes

### R4 — Hubble Tension Structural Lock theorem

- **Tier:** A (single cycle)
- **Claim-state move:** novel-structure-with-falsifier; manuscript-surface theorem
- **Falsifier:** **explicit.** Predicts no late-time `H_0` drift across
  distance-ladder rungs once `(Omega_Lambda, Omega_m, Omega_r, H_0)` are
  fixed. A measured z-dependent inconsistency in `H_0` at late times falsifies
  the retained surface (or one of the supplied inputs).
- **Premise:** retained `w_Lambda = -1`, retained `Lambda = 3/R_Lambda^2`
  spectral-gap identity, flat FRW with constant late-time `Omega_*`. No new
  axioms.
- **Statement (informal):** on the retained surface, the late-time
  distance-redshift relation is a fixed function of
  `(Omega_Lambda, Omega_m, Omega_r, H_0)` only. Any genuine `H_0` tension
  between distance-ladder and CMB measurements must therefore arise from
  pre-recombination physics or systematic measurement error, not from
  late-time modification of dark energy or gravity.
- **Output:** theorem note + symbolic+numerical runner (sympy + numpy) +
  paired log; `WHAT_THIS_PAPER_DOES_NOT_CLAIM.md` weave proposed in HANDOFF.
- **Blockers:** none.
- **Score: HIGH.** Publication-grade structural commitment with a real
  falsifier; the lane file flags this as the Phase-1 fast move.

### R3 — Open-number reduction theorem

- **Tier:** A (single cycle)
- **Claim-state move:** exact-support; counts open numbers exactly
- **Falsifier:** none directly (parameter-count statement). The result is
  more structural than predictive.
- **Premise:** matter-bridge theorem (2026-04-22) + single-ratio inverse
  reconstruction theorem (2026-04-25). Combines two retained results.
- **Statement (informal):** on the retained `(Lambda = 3/R_Lambda^2,
  w_Lambda = -1, flat FRW)` surface, every late-time bounded cosmology
  observable
  `{H_0, H_inf, Omega_Lambda, Omega_m, q_0, z_*, z_mLambda, H(a), R_Lambda}`
  is an exact function of the pair `(H_0, L)`, where `L := Omega_Lambda =
  (H_inf/H_0)^2 = (c / (R_Lambda H_0))^2`. The bounded surface therefore has
  exactly two open structural numbers, not seven.
- **Output:** theorem note + symbolic verifier runner (sympy) + paired log.
- **Blockers:** none.
- **Score: MEDIUM-HIGH.** Adds rigorous open-number-count structural claim;
  lighter than R4 but useful framing for downstream review.

### R5 — eta retirement audit (Tier B)

- **Tier:** B (multi-cycle, dependency on DM lane)
- **Claim-state move:** import-retirement gate identification + structural
  audit; not retirement itself in single cycle
- **Falsifier:** indirect (depends on which selector/normalization closure
  lands).
- **Premise:** existing DM leptogenesis branches (`eta/eta_obs = 0.1888`
  exact one-flavor; `eta/eta_obs = 1.0` reduced-surface PMNS). No new axioms.
- **Statement:** identify the minimal selector/normalization closure required
  to promote one of the surviving DM leptogenesis branches to retained, which
  would retire `eta` from the bounded `Omega_b` cascade.
- **Output:** retirement-audit note + an explicit closure-gate statement;
  cross-references to live DM lane work; runner only if numerically novel.
- **Blockers:** depends on DM/leptogenesis lane work outside this branch.
- **Score: MEDIUM.** Real movement but not a single-cycle retirement.

### R6 — `R_Lambda` direct route (Tier C, blocked)

- **Tier:** C (program-scale)
- **Claim-state move:** retained absolute-scale anchor; would close `H_inf`
  and reduce Lane 5 to deriving `L`
- **Falsifier:** if achieved, predicts numerical `R_Lambda`, hence numerical
  `H_inf`, hence numerical `H_0` once `L` is fixed.
- **Blockers:** **Planck lane.** The 2026-04-24 conditional packet leaves the
  primitive boundary count's identification as the gravitational
  boundary/action carrier as the explicit open premise; the area-law
  shortcuts are closed. No path to `R_Lambda` in single cycle.
- **Score: BLOCKED.** Out of scope for this workstream until the Planck lane
  promotes an absolute-scale identification.

### R7 — minimal-axiom cosmology no-go

- **Tier:** B
- **Claim-state move:** no-go (program-bounding negative)
- **Falsifier:** if a future retained derivation of `L` lands, the no-go is
  falsified — useful program-bounding statement.
- **Premise:** the `MINIMAL_AXIOMS_2026-04-11.md` accepted axiom stack plus
  the matter-bridge and inverse reconstruction theorems.
- **Statement:** prove that `L` cannot be derived without an additional
  scale-axiom (i.e., an absolute lattice spacing or a separate dimensionless
  ratio) on the minimal accepted axiom stack. The proof would isolate the
  gap that the cosmology lane needs an additional structural premise to
  close.
- **Output:** no-go theorem note + minimal-stack derivation map.
- **Blockers:** depends on a careful canonical formulation of "the minimal
  accepted axiom stack" — borderline of methodology.
- **Score: MEDIUM.** Real claim-state move (program-bounding), but harder to
  make rigorous in one session than R4 or R3.

### R8 — Inverse certificate consistency runner

- **Tier:** A
- **Claim-state move:** support-tier (turns the inverse reconstruction
  theorem into an executable consistency tool for downstream cycles)
- **Falsifier:** none directly; runner is a verifier.
- **Premise:** retained `COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md`.
- **Statement:** code the four inverse reconstruction formulas as a runner
  that takes any candidate late-time data packet and outputs all four
  reconstructed `L` values plus their pairwise differences, with PASS/FAIL
  tolerance.
- **Output:** runner + paired log against Planck 2018 data packet.
- **Blockers:** none.
- **Score: LOW-MEDIUM.** Useful tool but pure support; better as
  cycle-2/cycle-3 work after a structural theorem cycle.

## Selection — Cycle 1

**Selected route: R4 — Hubble Tension Structural Lock theorem.**

Rationale:
1. Single-session achievable (Tier A).
2. Real falsifier (no late-time `H_0` drift), making it a publication-grade
   structural claim, not pure prose.
3. Lane file Phase-1 priority; ground for downstream Lane 5 work.
4. No blockers, no dependencies on other open lanes.
5. Output is a manuscript-surface clarification that adds load-bearing
   prediction content (no late-time tension resolution permitted).

If R4 lands cleanly with review-loop disposition, **Cycle 2 candidate is
R3** (open-number reduction theorem) since it formalizes what R4 implicitly
uses.

## Rejected for this workstream

- R6 (`R_Lambda` direct): blocked by Planck lane.
- Any route that imports a value of `H_0`, `Omega_Lambda`, or `Omega_m` from
  Planck 2018 or distance-ladder data as a derivation input: violates the
  workstream's import-retirement priority. Such values are comparators only.
- Pure prose passes that restate the matter-bridge or inverse reconstruction
  theorems without adding new structural claim or falsifier: fail dramatic-
  step gate per skill.
