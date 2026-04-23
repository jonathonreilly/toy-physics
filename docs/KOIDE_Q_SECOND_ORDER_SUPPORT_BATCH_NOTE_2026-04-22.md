# Koide April 22 Second-Order `Q` Support Batch

**Date:** 2026-04-22
**Scope:** Charged-lepton Koide `Q = 2/3` support additions from the
second-order readout / reduced-carrier support packet.
**Status:** Support batch only. This note does **not** promote `Q` closure.

## What this batch adds

This batch adds a coherent second-order support route on the charged-lepton
lane:

- an exact quotient/factorization theorem for the first-live second-order
  `Γ_1 / T_1` readout carrier;
- an exact uniqueness statement for the minimal scale-free `C_3`-invariant
  selector variable once that carrier is admitted;
- an exact reduced two-block observable law
  `W_red(K) = log det(I + K)` on the normalized block algebra;
- an exact Legendre-dual effective-action calculation on that normalized
  carrier;
- a no-hidden-source audit showing that any nonzero reduced source simply
  re-parameterizes the selector family;
- a dedicated stress-test harness consolidating the second-order route.

The practical scientific gain is a sharper statement of the remaining open
step on the `Q` lane.

## What this batch sharpens

This batch does **not** prove that charged-lepton `Q = 2/3` is axiom-native
retained.

What it does is compress the remaining `Q` bridge to one explicit primitive:

```text
why the physical charged-lepton selector is source-free (K = 0)
on the normalized second-order reduced carrier.
```

Equivalently, the remaining open work is now:

1. derive from retained charged-lepton physics why the physical selector lives
   on the admitted second-order reduced carrier and is source-free there, or
2. explicitly retain that source-free law as the final missing primitive.

That is materially sharper than the earlier “find the right extremal
functional” posture.

## What this batch does not close

- It does **not** prove that the physical selector must lie in the admitted
  first-live bosonic second-order class.
- It does **not** prove that the reduced two-block observable law is the
  physical charged-lepton observable law rather than the exact law on a chosen
  reduced carrier.
- It does **not** prove that `K = 0` is forced by retained charged-lepton
  physics.
- It does **not** affect the separate Brannen-phase bridge behind
  `δ = 2/9`.

## Main artifacts

### Notes

- `docs/KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md`
- `docs/KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md`
- `docs/KOIDE_Q_MINIMAL_SCALE_FREE_SELECTOR_NOTE_2026-04-22.md`
- `docs/KOIDE_Q_REDUCED_OBSERVABLE_RESTRICTION_THEOREM_2026-04-22.md`
- `docs/KOIDE_Q_NORMALIZED_SECOND_ORDER_EFFECTIVE_ACTION_THEOREM_2026-04-22.md`
- `docs/KOIDE_Q_NO_HIDDEN_SOURCE_AUDIT_2026-04-22.md`
- `docs/KOIDE_Q_SECOND_ORDER_REVIEWER_STRESS_TEST_NOTE_2026-04-22.md`

### Runners

- `scripts/frontier_koide_q_bridge_single_primitive.py`
- `scripts/frontier_koide_q_readout_factorization_theorem.py`
- `scripts/frontier_koide_q_minimal_scale_free_selector.py`
- `scripts/frontier_koide_q_reduced_observable_restriction_theorem.py`
- `scripts/frontier_koide_q_normalized_second_order_effective_action.py`
- `scripts/frontier_koide_q_no_hidden_source_audit.py`
- `scripts/frontier_koide_q_second_order_reviewer_stress_test.py`

## Bottom line

This batch should be read as a **second-order support expansion** of the Koide
support package.

It strengthens the `Q` lane by turning the remaining gap into one named
physical-identification problem, but it does not change the current package
status:

- `Q = 2/3` support is stronger, not closed;
- `δ = 2/9` support is stronger, not closed;
- `v_0` remains a separate support lane.
