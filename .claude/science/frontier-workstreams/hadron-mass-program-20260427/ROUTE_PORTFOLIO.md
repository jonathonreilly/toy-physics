# Hadron Mass Program — Route Portfolio

**Date:** 2026-04-27
**Workstream:** `hadron-mass-program-20260427`
**Purpose:** independent routes toward Lane 1 closure, scored by likely
claim-state movement under the dramatic-step gate.

## Scoring rubric

Each route scored on:

- **Tier:** A (≤1 session), B (1-4 sessions), C (program-scale)
- **Claim-state move:** retire-import / exact-support / no-go /
  blocker-isolation / novel-structure
- **Falsifier:** explicit, ambiguous, or none
- **Blockers:** open dependencies on other lanes

## Routes

### R1 — `sqrt(sigma)` retained promotion (3E)

- **Tier:** B (likely 2-3 cycles)
- **Claim-state move:** import-narrowed (bounded → retained); novel-
  structure if a clean retention budget emerges.
- **Falsifier:** explicit. A retained √σ predicts the lattice string
  tension to within an explicit retention budget.
- **Premise:** retained `T = 0` confinement + retained `alpha_s(M_Z)` +
  EFT bridge with screening corrections (currently bounded).
- **Blockers:** none. Runs in parallel to Lane 3.
- **Score: HIGH.** Single Lane-1-internal route that does not depend
  on Lane 3. The lane file flags this as "incremental tightening of
  existing bounded content".

### R2 — Lane 3 dependency audit + Lane 1 theorem plan

- **Tier:** A (single cycle)
- **Claim-state move:** blocker-isolation; produces the lane file's
  "first parallel-worker target" — a sharp pion/proton mass theorem
  plan.
- **Falsifier:** none directly (planning artifact); the plan's
  individual theorems will have their own falsifiers.
- **Premise:** retained gauge sector + Lane 3 lane status + lattice-
  QCD admitted-convention bridge.
- **Blockers:** none. Single cycle. The plan itself is Lane-1-internal;
  the theorems it sketches depend on Lane 3.
- **Score: HIGH.** Cleanest single-cycle entry; the lane file's
  explicit "first parallel-worker target".

### R3 — Pion mass via GMOR (3A)

- **Tier:** B (2-3 cycles, conditional on Lane 3)
- **Claim-state move:** retain `m_pi` numerically.
- **Falsifier:** explicit (predicts numerical `m_pi`).
- **Premise:** GMOR identity `m_pi^2 f_pi^2 = (m_u + m_d) Sigma`;
  needs:
  - `m_u + m_d` retained (Lane 3)
  - `Sigma` retained (Lane-1-internal possible: structural derivation
    from staggered-Dirac partition; see R7)
  - `f_pi` retained (Lane-1-internal possible: chiral SB pattern)
- **Blockers:** Lane 3 light-quark mass closure.
- **Score: HIGH** but blocked.

### R4 — Proton mass ab initio (3B)

- **Tier:** C (program-scale, conditional on Lane 3 + lattice-QCD
  setup)
- **Claim-state move:** retain `m_p` numerically — highest-visibility
  hadron observable.
- **Falsifier:** explicit (predicts numerical `m_p`).
- **Premise:** standard lattice-QCD methodology adapted to framework
  substrate; all quark masses retained; alpha_s running.
- **Blockers:** Lane 3 full closure; lattice-QCD computational
  infrastructure.
- **Score: HIGH** but heavily blocked.

### R5 — Hadron-mass theorem-plan synthesis

- **Tier:** A (single cycle)
- **Claim-state move:** novel-structure (synthesis); produces a
  unified Lane 1 closure roadmap integrating R1-R4 plus the Lane 3
  dependency.
- **Falsifier:** none directly (synthesis artifact).
- **Note:** overlaps with R2; could be merged. R2 is more focused
  ("Lane 3 dependency audit + theorem plan"); R5 is broader synthesis.
- **Score: MEDIUM-HIGH.** Useful payload for the post-workstream
  review pipeline; lighter than R2 if R2 lands first.

### R6 — Confinement / `sqrt(sigma)` EFT bridge audit

- **Tier:** B (1-2 cycles)
- **Claim-state move:** blocker-isolation on R1; identifies what
  specifically bridges bounded √σ to retained.
- **Falsifier:** indirect (depends on the closure attempt).
- **Premise:** existing bounded √σ derivation + EFT bridge analysis.
- **Blockers:** none.
- **Score: MEDIUM.** Useful precursor to R1; can run in single
  cycle. Could be done as Cycle 2 if Cycle 1 is R2.

### R7 — Chiral condensate `Sigma` structural attempt

- **Tier:** B-C (conditional on whether a clean structural path exists)
- **Claim-state move:** retain `Sigma` (chiral condensate); unblocks
  R3 even before Lane 3 closure of light quark masses.
- **Falsifier:** explicit (predicts numerical Σ).
- **Premise:** retained graph-first SU(3) + retained finite local
  Grassmann/staggered-Dirac partition + chiral SB pattern analysis.
- **Blockers:** none structurally; the question is whether the
  framework's substrate delivers Σ retained.
- **Score: HIGH if a clean path exists; LOW if not.** Worth a
  scoping cycle (R7-scoping) before committing to a full attempt.

### R8 — Hadron-mass route no-go

- **Tier:** B
- **Claim-state move:** no-go (program-bounding negative).
- **Falsifier:** existential — exhibit a counterexample, the no-go
  falls.
- **Premise:** structural analysis of what the minimal axiom stack
  alone delivers for hadron masses.
- **Score: MEDIUM.** Useful only if direct work fails; better
  saved for late cycles.

## Selection — Cycle 1

**Selected route: R2 — Lane 3 dependency audit + Lane 1 theorem plan.**

Rationale:
1. Single-session achievable (Tier A).
2. The lane file's explicit "first parallel-worker target".
3. Real claim-state movement (blocker-isolation + theorem-plan
   synthesis).
4. No blockers; no Lane-3 dependency to close before this cycle can
   proceed.
5. Output is a structural plan that subsequent cycles (R1, R6, R7)
   can build on.

If R2 lands cleanly, **Cycle 2 candidates are R6** (confinement / √σ
EFT bridge audit) — Lane-1-internal, runs parallel to Lane 3.

## Rejected for this workstream (or deferred)

- Direct attempt at R3 (3A m_pi via GMOR) before Lane 3 lands light-
  quark masses or R7 lands `Sigma` — would import quark-mass values
  silently.
- Direct attempt at R4 (3B m_p ab initio) — heavily blocked.
- Pure prose / restating the lane file content without adding
  structural claim — fails dramatic-step gate.
