# Review History — 3+1d Retained-Positive

## 2026-05-02 — block-local self-review

### Cycle 1 (Route R3, chirality grading)
- **Strength:** the sublattice-parity replacement is structurally clean
  on retained-clean primitives. Cl(3) per-site uniqueness +
  CPT note + Z^3 bipartite structure together fully replace the
  Lawson-Michelsohn appeal.
- **Concern (handled):** the chirality grading no longer constrains d_t,
  but Cycle 2 picks up the d_t constraint from single-clock unitarity.
- **Disposition:** pass. No demotion needed.

### Cycle 2 (Route R4, ultrahyperbolic obstruction)
- **Strength:** "single-clock = exactly one time direction" is direct
  and dispenses with the Cauchy literature import.
- **Concern (open):** assumption 1 (single-clock unitarity) remains a
  framework axiom rather than a derived consequence. If a critic
  challenges this axiom, the theorem retreats to a deeper hypothesis
  about the Hilbert/locality/information surface, which is not yet
  retained-clean.
- **Disposition:** pass at the theorem level; assumption-level
  open item documented in CYCLE_02.

### Cycle 3 (Route R1, ABJ inconsistency)
- **Strength:** the cycle is honest about the residual import.
- **Concern (open):** R1 is genuinely not closed on retained-clean
  primitives; lattice Wess-Zumino / Fujikawa is not in the repo.
- **Disposition:** open / honest documentation of unclosed admission.
  Roadmap to closure included.

### Cycle 4 (Route R2, singlet completion)
- **Strength:** the (a)-(e) classification of allowed framework
  extensions is exhaustive on the retained-clean surface.
- **Concern (handled):** the argument relies on
  `native_gauge_closure_note`'s retained-bounded gauge closure, so
  Step 2 inherits a bounded-support classification rather than
  retained-positive.
- **Disposition:** pass with caveat. Bounded-support honestly noted.

### Cycle 5 (Synthesis)
- **Strength:** the rewritten theorem note is internally consistent;
  references retained-clean primitives explicitly; bounded scope
  narrowed from four admissions to one.
- **Concern:** the audit ledger entry will still come back as
  bounded_theorem rather than retained-positive, because of (i).
- **Disposition:** pass. Honest narrowing achieved.

## Aggregate disposition

**pass with bounded scope.** The campaign substantively narrowed the
bounded scope from four admissions to one. The remaining literature
import (ABJ inconsistency for chiral gauge theories in 3+1d) is a
named, well-understood QFT result with a documented internal-closure
roadmap. The theorem rewrite is honest, retained-clean primitives are
correctly used, and the runner still passes.

The campaign **did not** achieve full retained-positive closure on
the actual current surface. That requires upstream re-audit of
reflection positivity, microcausality, and a new lattice Wess-Zumino
theorem. Those are tractable next-loop targets but were out of scope
for this campaign.
