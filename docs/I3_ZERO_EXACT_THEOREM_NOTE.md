# `I_3 = 0` Exact Theorem

**Date:** 2026-04-12
**Status:** exact theorem note for the proposed_retained Hilbert-surface interference result
**Runner:** `scripts/frontier_born_rule_derived.py` (historical filename)

## Claim

The retained exact statement is:

> given linear amplitude composition and quadratic probability
> `P = |A|^2`, the Sorkin third-order interference parameter `I_3`
> vanishes identically.

This is an exact no-third-order-interference theorem. It is **not** a
standalone derivation of the Born rule from nothing.

## What is proved

- amplitudes add linearly across disjoint paths
- probabilities of the accepted Hilbert form are quadratic
- inclusion-exclusion then cancels all terms of degree higher than two
- therefore `I_3 = 0` exactly

The result is algebraic and does not depend on a special lattice size or on a
specific `Cl(3)` representation.

## What is not proved

This lane does not independently derive `P = |A|^2` without already working on
the Hilbert probability surface. The paper-safe statement is therefore:

> on the Hilbert surface of the framework, interference is exactly pairwise and
> the Sorkin parameter `I_3` vanishes identically.

## Manuscript use

Safe main-text wording:

> The framework carries an exact `I_3 = 0` theorem: once amplitudes compose
> linearly and probabilities are quadratic on the Hilbert surface, all
> third-order interference cancels identically.

Explicitly unsafe wording:

> The Born rule is fully derived from the lattice axioms alone.
