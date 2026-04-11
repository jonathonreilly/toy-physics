# Action Uniqueness Audit

**Date:** 2026-04-11
**Scope:** commit `a3888a33286e489be306c13d3610eaddadc0c628` and `scripts/action_uniqueness_investigation.py`

## Verdict

**Bounded family-law keep, not a theorem.**

The script argues for a uniqueness result:

- valley-linear is “forced by the axioms”
- the weak-field action is “uniquely determined”
- the action law is presented as a theorem, not a family result

That is stronger than what the retained repo evidence supports. The older retained note already narrows the claim to a bounded fixed-family universality class on one ordered-lattice family. On that family, multiple weak-field-linear valley actions behave equivalently in the Newtonian regime. That is a bounded family law, not a universal uniqueness theorem.

## Retainable Core

The part that is retainable for `main` is the narrow statement:

- on the tested 3D ordered-lattice family
- with nearest-neighbor propagation
- in the weak-field regime
- weak-field-linear phase valleys give Newtonian-like `F ∝ M` behavior

The script’s Part A and Part C are useful as support for that bounded family statement:

- `S = L(1-f)`, `S = L exp(-f)`, and `S = L/(1+f)` all collapse to the same weak-field linear behavior
- the continuum integral gives the expected `1/b^alpha` scaling for the chosen family, with `alpha = 1` giving the Newtonian case

That is a valid bounded result.

## Why It Is Not Yet A Main Theorem

This remains frontier-only because the script and note do not establish the stronger claims across architectures.

### Assumptions

The result depends on all of the following:

- 3D ordered dense lattice
- `h = 0.5`, `W = 8`, `L = 12`
- Coulomb-style field `f = s/r`
- nearest-neighbor propagation
- the tested action family `S = L * g(f)`
- weak-field expansion around `f = 0`

### Model Dependence

The claim is family-dependent, not universal:

- the script tests a finite set of action forms, not all admissible actions
- the current evidence shows equivalence among weak-field-linear valleys on this family
- it does not show that valley-linear is unique on arbitrary graphs, kernels, or dimensions
- it does not establish an architecture-independent theorem

### Promotion Blockers

The stronger uniqueness language is still blocked by:

- lack of architecture-independence
- lack of proof across non-ordered or irregular graph families
- the existence of other weak-field-linear valley actions with the same retained Newtonian behavior on this family

## Promotion Guidance

Promote only as a bounded family-law note if the wording stays at the family
level:

- “weak-field-linear phase valleys are Newtonian on the tested ordered-lattice family”
- “multiple weak-field-linear valleys are equivalent on this family in the Newtonian regime”

Do **not** promote the stronger wording:

- “valley-linear is uniquely forced by the axioms”
- “the action is uniquely determined on arbitrary graphs”

That phrasing is not supported by the retained note chain or by the current script evidence.
