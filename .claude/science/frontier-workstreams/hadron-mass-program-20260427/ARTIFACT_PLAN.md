# Hadron Mass Program — Artifact Plan

**Workstream:** `hadron-mass-program-20260427`

## Cycle 1 — Route R2 (Lane 3 dependency audit + Lane 1 theorem plan)

**Artifact:**

`docs/HADRON_MASS_LANE1_THEOREM_PLAN_NOTE_2026-04-27.md`

Structure:
- §0 statement: Lane 1 closure roadmap with explicit Lane 3 dependencies
- §1 retained framework structure used
- §2 the five derivation targets (3A-3E) with closure pathways
- §3 Lane 3 dependency map (which Lane-3 retentions unblock which
  Lane-1 targets)
- §4 Lane-1-internal routes that can proceed in parallel (3E √σ
  promotion; possibly R7 Σ structural attempt)
- §5 Phase ordering: Phase 1 (3A m_π via GMOR + 3E √σ), Phase 2 (3B
  m_p ab initio), Phase 3 (spectroscopy + form factors)
- §6 cross-references to lane file, retained gauge-sector content,
  Lane 3 entry point
- §7 boundary statement

**No runner needed** for the planning artifact (consistent with the
hubble-h0 workstream's audit-grade artifacts).

**Acceptance criteria:**

- Theorem plan is sharp on: which retentions Lane 3 must produce;
  which closures Lane 1 can produce in parallel; which Lane-1
  closures depend on Lane 3.
- Cross-references are correct.
- No silent imports of hadron-mass observables or quark-mass values.

**Anti-pattern guard:**

- Plan must NOT claim a hadron mass numerically.
- Plan must NOT assume a specific Lane 3 timeline.
- Plan must NOT silently absorb chiral perturbation theory or
  lattice-QCD methodology — both are explicit admitted-convention
  bridges in `ASSUMPTIONS_AND_IMPORTS.md`.

## Cycle 2 (tentative) — Route R6 (Confinement / √σ EFT bridge audit)

If Cycle 1 lands cleanly, Cycle 2 produces:

`docs/HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_NOTE_2026-04-27.md`

Identifies the specific gap between bounded `sqrt(sigma) ≈ 465 MeV`
(5.6% above PDG 440 ± 20 MeV) and a retained sub-percent or retention-
budget claim. Lane-1-internal; does not depend on Lane 3.

## Cycle 3+ candidates

- **R7 scoping cycle:** can the staggered-Dirac partition on `Cl(3)/Z³`
  deliver retained `Sigma` (chiral condensate)? This could unblock
  3A `m_π` even before Lane 3 light-quark closure.
- **R1 first attempt:** if R6 audit identifies a clean retention path
  for √σ, attempt the actual promotion.
- **R8 no-go:** if direct work fails on R1/R7, prove a specific class
  no-go.

## Repo-wide weaving (NOT done in workstream — recorded in HANDOFF)

When this branch is later merged into the `main` review pipeline:

- Update `docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md`
  §4 scaffolding list with the Lane-1 theorem plan.
- Update `docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md` Lane 1 status
  line if the workstream advances to Phase 1 retention.
- Add new theorem notes to `docs/CANONICAL_HARNESS_INDEX.md` if any
  cycle produces a runner.

These weaves are NOT applied on this workstream branch per skill
science-only delivery policy.
