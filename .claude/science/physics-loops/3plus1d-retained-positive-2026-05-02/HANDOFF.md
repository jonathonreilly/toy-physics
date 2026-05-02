# Handoff — 3+1d Retained-Positive Loop

**Loop slug:** `3plus1d-retained-positive-2026-05-02`
**Branch:** `claude/3plus1d-retained-positive-2026-05-02`
**Date:** 2026-05-02

## What was done

Drove `anomaly_forces_time_theorem` (PR #337's bounded version with
four admissions) toward retained-positive closure. Outcome: bounded
scope sharply narrowed from four admissions to one.

Per-admission outcome:

1. **ABJ inconsistency** — still requires literature import
   (Adler 1969 / Bell-Jackiw 1969). Roadmap to internal closure
   sketched (lattice Wess-Zumino / Fujikawa, requires upstream
   retained-clean reflection positivity / microcausality).
2. **Singlet completion uniqueness** — re-classified as Cl(3)/Z^3 +
   retained gauge structure fact, conditional on
   `native_gauge_closure_note`'s retained-bounded gauge closure.
3. **Clifford-volume chirality** — re-classified as sublattice
   parity ε(x) = (-1)^{x_1+x_2+x_3} on Z^3, supported by retained-clean
   `CPT_EXACT_NOTE` and `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29`.
4. **Ultrahyperbolic Cauchy obstruction** — shown dispensable; theorem's
   own hypothesis 1 (single-clock unitarity) directly forces d_t = 1.

## Final claim_type for the row

`bounded_theorem` with **narrowed scope**: only one external bridge
premise (i) remains. Three of the prior four admissions are now
discharged on retained-clean / Cl(3)/Z^3 structural primitives.

## Strongest unconditional statement now holding

> **Within the framework's retained-clean Cl(3)/Z^3 structure plus
> single-clock unitary one-parameter group hypothesis, and modulo the
> standard Adler-Bell-Jackiw inconsistency implication for chiral
> gauge theories with the framework's specific gauge content,
> spacetime signature is forced to be (3,1).**

The narrowing makes the bounded scope precise: only *one* well-named
literature import (ABJ inconsistency) is needed; the chirality
grading, the singlet completion uniqueness, and the d_t=1 conclusion
are now all framework-internal.

## Honest open items

- **(R1, residual)** ABJ inconsistency for chiral gauge theories in
  3+1d remains a literature import. Closing requires:
  - Elevate `axiom_first_reflection_positivity_theorem_note_2026-04-29`
    (currently `unaudited`) to retained-clean.
  - Elevate `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01`
    (currently `unaudited`) to retained-clean.
  - Write a new lattice Wess-Zumino consistency / Fujikawa-on-Z^3
    theorem.
  - Combine the above to derive "nonzero anomaly traces ⇒ gauge
    invariance broken on the framework's Hilbert physical-state
    surface".

- **(R2, conditional residual)** Singlet completion uniqueness is
  conditional on `native_gauge_closure_note`'s retained-bounded
  "no other gauge factor" closure. If that bounded closure is later
  sharpened to retained-positive, Step 2 of the theorem closes
  retained-positive.

## What this branch contains

- `docs/ANOMALY_FORCES_TIME_THEOREM.md` — rewritten with the
  three discharged admissions; references the retained-clean
  primitives explicitly; documents the residual (i).
- `.claude/science/physics-loops/3plus1d-retained-positive-2026-05-02/`
  - `GOAL.md`, `STATE.yaml`, `ASSUMPTIONS_AND_IMPORTS.md`,
    `ROUTE_PORTFOLIO.md`, `CLAIM_STATUS_CERTIFICATE.md`,
    `REVIEW_HISTORY.md`
  - `CYCLE_01_CHIRALITY_GRADING.md` (Route R3 — chirality grading
    via sublattice parity ε(x))
  - `CYCLE_02_ULTRAHYPERBOLIC.md` (Route R4)
  - `CYCLE_03_ABJ.md` (Route R1)
  - `CYCLE_04_SINGLET.md` (Route R2)
  - `CYCLE_05_SYNTHESIS.md`
  - `HANDOFF.md` (this file)
- Audit pipeline outputs auto-regenerated.

## Next exact action

Open a review PR against `main`. The PR should be reviewed by the
audit lane to:
1. ratify (or reject) the narrowing of admissions (ii)-(iv);
2. update `claim_scope` in the audit ledger entry to reflect the
   narrowed bounded scope;
3. refresh `audit_status` based on the new note.

If the audit lane accepts the narrowing, the row's `verdict_rationale`
should change from "four admissions" to "one admission (ABJ)" and
the upstream lift path should be referenced.

## Proposed repo-wide weaving (NOT done in this branch)

After audit ratification:
- Update `docs/publication/ci3_z3/CLAIMS_TABLE.md` to reflect the
  narrowed bounded scope.
- Consider opening a separate audit-loop campaign to elevate
  `axiom_first_reflection_positivity_theorem_note_2026-04-29` and
  `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01`
  from `unaudited` to retained-clean. That would unlock R1 closure.
