# HANDOFF — axiom-first-foundations block01

**Last update:** 2026-04-29 (loop launch)
**Branch:** `physics-loop/axiom-first-foundations-block01-20260429`
**Based on:** `origin/main @ 37329240`
**Loop runtime budget:** 12 hours from launch
**Resume status:** loop pack scaffolded; preflight + grounding done; about
to begin Cycle 1 (Route R1: spin-statistics).

## Snapshot of the world at launch

- Audited current `A_min` is `Cl(3)` on `Z^3` + finite Grassmann /
  staggered-Dirac partition + canonical `g_bare = 1` normalization
  (`docs/MINIMAL_AXIOMS_2026-04-11.md`).
- The active review queue records no live repo-governance blockers
  (`docs/repo/ACTIVE_REVIEW_QUEUE.md` as of 2026-04-18). All open items
  are science-facing.
- Existing axiom-implication infrastructure includes the assumption /
  derivation ledger (`docs/ASSUMPTION_DERIVATION_LEDGER.md`), the axiom
  reduction note (2 axioms + 1 dimensional choice), the two single-axiom
  variants (Hilbert tensor product / conserved information flow), and the
  observable-principle-from-axiom note that uses CPT-evenness as an
  unproven premise.
- The `Cl_4(C)` carrier-axiom consequence map (`CL4C_CARRIER_AXIOM_CONSEQUENCE_MAP_NOTE_2026-04-28.md`)
  is the most recent axiom-frontier work; this loop does **not** extend
  `A_min` and does not adopt `Axiom*`. It only derives consequences of
  the existing `A_min`.

## Plan in flight

| Cycle | Route | Status |
|-------|-------|--------|
| 1 | R1: spin-statistics | not started |
| 2 | R2: reflection positivity | not started |
| 3 | R3: cluster decomposition / Lieb–Robinson | not started |
| stretch | R4: CPT theorem | not started |

## Proposed repo weaving (do **not** apply during the run)

When this block is reviewed and merged, propose:

- adding the four theorem notes to the program-wide derivation atlas
  (`docs/notes/DERIVATION_ATLAS.md`) under a new "Axiom-First Foundations"
  section.
- updating `docs/ASSUMPTION_DERIVATION_LEDGER.md` to flip the four
  retired imports from "implicit" to "derived" with citations.
- citing R1 from any DM/leptogenesis / Yukawa note that currently asserts
  Grassmann fermion antisymmetry as background.
- citing R2 from any note that invokes the Wick-rotation / transfer-matrix /
  Hilbert-reconstruction language without an explicit reflection-positivity
  argument on the canonical action.
- citing R3 from confinement and area-law lanes that use exponential
  clustering of correlators.
- citing R4 (if it closes) from `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
  to retire the CPT-even premise.

## Resume instructions for the next agent

1. Read this `HANDOFF.md`, then `STATE.yaml`, then `ARTIFACT_PLAN.md`.
2. Continue from `STATE.yaml -> next_exact_action`.
3. Do not enlarge `A_min` or import literature; this loop's scope is
   strictly consequences of the existing `A_min`.
4. Update this file at every checkpoint and before stopping.
