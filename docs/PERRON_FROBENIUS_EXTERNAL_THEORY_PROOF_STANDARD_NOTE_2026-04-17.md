# Perron-Frobenius External-Theory Proof Standard

**Date:** 2026-04-17  
**Status:** exact science-only proof-standard boundary for atlas and external PF theory use  
**Script:** `scripts/frontier_perron_frobenius_external_theory_proof_standard_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

How should atlas rows and published mathematics be used on this PF lane if the
work has to survive a hard technical review?

## Answer

They must be used only in the following theorem-safe way:

1. **Atlas rows are index objects, not proof objects.**  
   An atlas entry can point to an exact theorem already present in the repo,
   but the row itself is never the proof.

2. **Published mathematics is a hypothesis template, not a plug-in closure.**  
   An external theorem can guide the mathematical form of the next attack only
   when the repo has already identified the corresponding object type and the
   relevant hypotheses that would need to be matched.

3. **No conclusion may be imported at wider scope than the hypotheses matched
   in-repo.**  
   If the repo has Wilson-side positivity, that supports Wilson-side use.
   It does not automatically support a global cross-sector descendant claim.

4. **Every PF claim should be typed.**  
   On this branch a statement should be one of:
   - exact in-repo theorem,
   - exact current-stack boundary / no-go,
   - external mathematical template for a future theorem search,
   - conjectural target.

That is the only hard-review-safe way to use atlas and outside theory here.

## Current application on this branch

The branch is already close to that standard, but the standard itself needs to
be explicit.

### Atlas use

The atlas is being used correctly when it does one of these:

- locates the exact theorem row for a Wilson transfer object,
- locates the exact theorem row for a PMNS support/intertwiner law,
- locates the exact theorem row for a PMNS last-mile current boundary,
- locates the exact theorem row for a plaquette underdetermination boundary.

That is citation/index use, not proof import.

### External theory use

The current outside references are useful only at these exact scopes:

- [Luescher 1977](https://doi.org/10.1007/BF01614090): step-1 template for
  positive transfer-matrix realization on the Wilson side.
- [Stinespring 1955](https://doi.org/10.1090/S0002-9939-1955-0069403-4):
  step-2 template for descendant / compression / intertwiner form.
- [Evans-Hoegh-Krohn 1978](https://doi.org/10.1112/jlms/s2-17.2.345):
  step-3 template for PF-type spectral compatibility of positive maps once the
  descendant laws are actually in hand.

None of those papers currently upgrades the repo to:

- a global parent/intertwiner theorem,
- a Wilson-to-PMNS descendant theorem,
- or a common-state PF selector.

## Theorem 1: hard-review-safe use rule for atlas and external PF theory

On the current PF lane, atlas and published mathematics may be used only under
the following rule.

### Atlas rule

An atlas citation is valid only as a pointer to a theorem already present in
the repo. It cannot substitute for reproducing the exact object and exact
conclusion actually used.

### External-theory rule

An external theorem is valid only as a template unless the repo has already
matched all load-bearing hypotheses on its own exact objects.

For this branch, the load-bearing hypotheses include things like:

- positivity / strict positivity,
- self-adjointness or positive-map structure,
- actual parent operator existence,
- actual descendant / compression / intertwiner law,
- the precise codomain on which the theorem is being invoked.

Therefore:

- Luescher cannot be cited as if it already proves the repo’s global parent
  theorem.
- Stinespring cannot be cited as if it already gives the missing
  Wilson-to-PMNS descendant law.
- Evans-Hoegh-Krohn cannot be cited as if it already gives common-state
  compatibility before the descendant theorem exists.

## Corollary 1: the atlas is admissible as navigation, not as authority by itself

The atlas is essential for locating exact rows and keeping the lane organized.
But every live claim must still be grounded in the underlying theorem note and,
when needed, the local verifier script.

## Corollary 2: external theory currently supports work order, not closure

At the present branch state, the outside mathematics legitimately supports:

- what kind of object step 1 should produce,
- what kind of law step 2 should produce,
- what kind of compatibility theorem step 3 would eventually need.

It does **not** legitimately support:

- positive global PF closure,
- implied PMNS provenance from Wilson,
- or implied plaquette framework-point evaluation.

## Corollary 3: every hard-review PF paragraph should separate four strata

Any serious writeup from this lane should separate:

1. exact theorem already proved in the repo,
2. exact boundary/no-go already proved in the repo,
3. mathematically motivated next target,
4. outside theorem used only as template.

If those strata are mixed, the review risk is real and justified.

## What this closes

- one explicit proof-standard rule for using atlas and outside PF theory
- one exact statement that outside math is currently supporting work order, not
  closure
- one exact hard-review hygiene rule for every future PF note on this branch

## What this does not close

- any new PF theorem by itself
- the missing Wilson-to-PMNS descendant law
- the missing plaquette operator evaluator
- the global selector

## Command

```bash
python3 scripts/frontier_perron_frobenius_external_theory_proof_standard_2026_04_17.py
```
