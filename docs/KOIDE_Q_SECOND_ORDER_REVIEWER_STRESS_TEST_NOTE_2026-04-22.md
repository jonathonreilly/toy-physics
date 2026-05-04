# Koide Q Second-Order Stress Test

**Date:** 2026-04-22
**Status:** science-only support packet for the second-order `Q` route; not a
closure theorem
**Primary runner:** `scripts/frontier_koide_q_second_order_reviewer_stress_test.py`

---

## Purpose

This note is the dedicated stress test for the **second-order** `Q` support
route, not for the older Frobenius-only support chain.

It checks four objection classes:

1. **carrier identification and factorization**
2. **exact reduced-observable restriction**
3. **zero-source response and no hidden source**
4. **no earlier close / exact Koide consequence on the admitted carrier**

The runner is meant to answer the question:

> if one accepts the retained `Γ_1 / T_1` grammar, does the new
> second-order route still hide a soft step?

Current answer on this branch-local packet: the core objections are executable
and clean.

---

## Load-bearing facts checked

- the first-live second-order readout map has rank `3` and kernel equal to the
  unreachable slot only;
- within the admitted first-live second-order class, the quotient/factorization
  statements are exact;
- the reduced source law is exactly `W_red = log det(I+K)`;
- the dual equation is exactly `K = Y^{-1} - I`, so zero source is the exact
  no-added-source response point;
- nonzero source simply re-encodes an arbitrary selector choice;
- the raw chiral bridge and the unreduced determinant carrier still fail in the
  expected ways;
- the admitted second-order route still lands at `Q = 2/3`.

---

## Bottom line

This is the dedicated executable objection pack for the current second-order
`Q` support route. It is useful support infrastructure, but it does not by
itself discharge the remaining physical/source-law bridge.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [observable_principle_from_axiom_note](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [hierarchy_bosonic_bilinear_selector_note](HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
- [charged_lepton_mass_hierarchy_review_note_2026-04-17](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
