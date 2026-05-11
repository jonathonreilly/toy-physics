# Physical Cl(3) on Z^3 Baseline Interpretation Note

**Date:** 2026-05-08
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion.
**Authority role:** restores the framework baseline that `Cl(3)` on `Z^3`
is physical, not a regulator or optional extra axiom.
**Primary runner:** [`scripts/frontier_physical_lattice_foundational_interpretation.py`](../scripts/frontier_physical_lattice_foundational_interpretation.py)
**Cache:** [`logs/runner-cache/frontier_physical_lattice_foundational_interpretation.txt`](../logs/runner-cache/frontier_physical_lattice_foundational_interpretation.txt)

## Baseline

The repo baseline is the physical `Cl(3)` on `Z^3` framework:

- A1: the physical local algebra is `Cl(3)`;
- A2: the physical spatial substrate is the cubic lattice `Z^3`.

That language is already the framework surface in
`MINIMAL_AXIOMS_2026-05-03.md`. This note
does not add a third mathematical axiom. It records the review-rule
consequence that the lattice should not be reclassified as a regulator,
formal bookkeeping device, or optional new premise during review.

## What This Fixes

Recent review packets treated "the lattice is physical" as if it were a
new admission that still needed to be added to the framework. That is the
wrong repo language. The physical `Cl(3)` on `Z^3` reading is baseline
framework semantics.

Review-loop should therefore not count the physical-lattice reading itself
as a new axiom, new theory premise, or admitted-context input. If a branch
does that, vocabulary correction back to the baseline is an appropriate
review-loop fix.

## Boundary

This clarification does not by itself promote any downstream theorem,
close an audit row, or change an `effective_status`.

In particular, the following still require their own source theorem and
independent audit path when they are load-bearing:

- a species or generation identification beyond the baseline `Cl(3)` on
  `Z^3` semantics;
- a `C_3`-breaking selector;
- a fitted, measured, PDG, or otherwise empirical value used as a
  derivation input;
- a scale, readout, unit, phase, or normalization bridge not already
  derived on the retained stack;
- a parent theorem/status update that depends on new bounded child rows.

The audit lane still owns `claim_type`, `audit_status`, and
`effective_status` on claim rows. Review-loop may seed or repair source
surfaces, but it must not write audit verdicts.

## Relation To Physical-Lattice Necessity

[`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md)
remains narrowed to its algebraic two-invariant rigidity/no-go surface.
This note does not widen that theorem. The present note is a repo-language
and review-process clarification: do not lose the baseline physical
`Cl(3)` on `Z^3` semantics while reviewing later theorem packages.

## A3/AC Consequence

For A3/AC work, physical `Cl(3)` on `Z^3` should not be listed as one of
the missing admissions. It is already the framework baseline.

That does not mean an A3/AC closure follows automatically. If a package
needs a physical-species identification, a `C_3`-breaking mechanism, a
Koide/Brannen readout, or an empirical mass match to do derivational work,
those inputs remain separate and must be labelled honestly.

## Review-Loop Rule

When reviewing future branches:

1. Treat "physical `Cl(3)` on `Z^3`" as baseline repo semantics.
2. Do not call that baseline a new axiom or a new admitted premise.
3. Do not let that baseline silently promote downstream science.
4. Keep extra identifications, selectors, observations, and readout bridges
   explicit as bounded/open inputs unless they have their own retained-grade
   derivation and audit closure.

## Validation

Run:

```bash
python3 scripts/frontier_physical_lattice_foundational_interpretation.py
```

The runner checks that this note is a meta clarification, that it matches
the two-axiom physical `Cl(3)` on `Z^3` baseline, and that it does not
declare audit verdicts or downstream theorem promotion.
