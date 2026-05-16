# Koide April 22 Second-Order `Q` Support Batch

**Date:** 2026-04-22
**Scope:** Charged-lepton Koide `Q = 2/3` support additions from the
second-order readout / reduced-carrier support packet.
**Status:** Support batch only. This note does **not** promote `Q` closure.

**Status authority and audit hygiene (2026-05-16):**
The audit lane has classified this row `audited_conditional`
(audit_date 2026-05-05, auditor codex-cli-gpt-5.5, auditor_confidence
high, load-bearing step class `F`). The verdict accepts that the
batch note is honest about being a support batch and explicitly does
not promote `Q` closure, but flags that the load-bearing
**compression step** — the claim that the remaining `Q` bridge
collapses to one explicit primitive ("why the physical charged-lepton
selector is source-free, `K = 0`, on the normalized second-order
reduced carrier") — depends on a physical-identification primitive
that the batch's runners do not derive from retained upstream
inputs. Audit verdict and effective status are set by the
independent audit lane only; nothing in the present edit promotes
status.

The audit-stated cheapest re-audit path (verbatim from the ledger
`notes_for_re_audit_if_any`):

> missing_bridge_theorem: provide a retained derivation that the
> physical charged-lepton selector is source-free, `K = 0`, on the
> normalized second-order reduced carrier.

Section 6 below adds the explicit audit-conditional perimeter, and
Section 7 records the candidate upstream supplier chain as
graph-bookkeeping dependency edges (no status promotion). The same
audit-named gap blocks the companion rows
`koide_q_reduced_observable_restriction_theorem_2026-04-22`,
`koide_q_normalized_second_order_effective_action_theorem_2026-04-22`,
and `koide_q_no_hidden_source_audit_2026-04-22`; the same supplier
chain is the audit-named missing bridge for all four rows.

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

## 6. Audit-conditional perimeter

The internal content of this batch — listed in "What this batch adds"
and "What this batch sharpens" above — is what the audit verdict
accepts as honest aggregation: an exact quotient/factorization on the
admitted `Γ_1 / T_1` carrier, an exact uniqueness statement for the
minimal scale-free `C_3`-invariant selector on that carrier, an exact
reduced two-block observable law `W_red(K) = log det(I + K)` on the
normalized block algebra, an exact Legendre-dual effective action on
that normalized carrier, and an algebraic hidden-source audit on the
same admitted carrier showing that any nonzero reduced source merely
re-parameterizes the selector family. Each of those sub-statements is
an internally consistent algebraic result on the admitted reduced
carrier and lives in its own sub-note with its own audit ledger row.

The audit-conditional perimeter (i.e. what stays open) is exactly the
**physical-identification primitive** named in "What this batch
sharpens":

1. derive from retained charged-lepton physics that the physical
   selector lives on the admitted second-order reduced carrier (this
   batch admits the carrier as input);
2. derive from retained charged-lepton physics that the physical
   selector is source-free, `K = 0`, on that carrier (this batch
   names the primitive but does not derive it);
3. derive the readout from `Y = I_2` through `kappa = 2` to the
   physical `Q = 2/3` from a retained Brannen / circulant identity
   on the charged-lepton selector (the batch documents the algebraic
   chain but does not anchor the physical identification).

Until at least (1) and (2) are supplied by retained upstream notes,
this row stays a **bounded support batch on the admitted reduced
carrier** rather than a physical-identification result. The
"Bottom line" above already states this honestly; this section makes
the audit-conditional perimeter explicit for the citation graph.

## 7. Candidate upstream supplier chain (graph-bookkeeping only)

The audit-stated repair target is a `missing_bridge_theorem`
(class F, identification of two symbols): a retained upstream
derivation that the physical charged-lepton selector is the source-free
(`K = 0`) point on the normalized second-order reduced carrier.

Four candidate supplier notes already exist on disk in this branch.
Their respective load-bearing inferences target the carrier-identification
and source-law halves of the audit-named bridge on the same admitted
normalized reduced carrier that the present batch sits on. They are
recorded here only as graph-bookkeeping dependency edges so the audit
citation graph can track them. Their current audit status does not
propagate retention to this row, and the current audit status of any
one supplier is independently determined by the audit lane.

1. `OBSERVABLE_PRINCIPLE_REAL_D_BLOCK_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10.md`
   — block-local uniqueness of the source-derivative content of the
   admissible scalar generator on an invertible real anti-Hermitian
   Dirac block. Targets the bridge between the generator
   `W = log|det(D + J)| - log|det D|` and any admissible scalar
   generator on a real-`D` block, which is the algebraic content
   underneath the reduced two-generator carrier when that block is
   admitted.

2. `KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md`
   — structural composition of the observable-principle theorems with
   physical-lattice-necessity §9 locality, the canonical
   trace-preserving local descent uniqueness, and the explicit
   `K = 0 ⇔ Y = I_2 ⇔ Q = 2/3` criterion. Targets the audit-named
   reduced-carrier identification half by forcing the framework's
   physical local scalar observables to read through the descent
   `E_loc`, which lands on the normalized `Y = I_2` baseline.

3. `KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md`
   — exact rank/kernel quotient of the linear second-order readout map
   `L : R^4 → Diag_3(R)`, `L(W) = P_{T_1} Γ_1 W Γ_1 P_{T_1}` on the
   retained `Γ_1 / T_1` grammar. Establishes that the readout map
   factors through the species-resolving diagonal carrier with a
   unique unreachable slot, supplying the algebraic skeleton of the
   reduced two-block carrier used in the batch.

4. `KOIDE_Q_MINIMAL_SCALE_FREE_SELECTOR_NOTE_2026-04-22.md`
   — exact uniqueness of the scale-free `C_3`-invariant selector
   ratio on the admitted second-order returned carrier (no nontrivial
   scale-free invariant at linear order; exactly one nontrivial ratio
   at quadratic order). Supplies the carrier-side uniqueness matching
   the source-side restriction used in the batch.

The combined load-bearing inference of this chain is:

> on the framework's accepted substrate, the physical local scalar
> observables read through the canonical descent `E_loc` to the
> diagonal carrier; the source-derivative content of any admissible
> scalar generator on a real-`D` block coincides with that of
> `W = log|det(D + J)| - log|det D|`; the readout map factors through
> the species-resolving diagonal target; and the normalized
> scale-free selector on the admitted carrier is unique. The
> reduced two-generator block carrier with baseline `D_red = I_2`
> and the source-free point `K = 0` is then the framework-forced
> reading rather than a free admitted choice.

That inference is the audit-named missing bridge for this row.

This section does not promote this row's `audit_status` or the
suppliers' status. Only the independent audit lane can do that. The
load-bearing physical-identification bridge in the auditor's
`verdict_rationale` remains open until at least one of the candidate
supplier chains is itself audited at retained-grade and the
composition is independently judged to close the bridge.

## 8. Boundaries

This note does **not**:

- modify the parent row's audit-ledger entry;
- promote the parent's `audit_status` from `audited_conditional`;
- derive the normalized second-order reduced carrier from retained
  upstream inputs;
- derive the source-free law `K = 0` from retained charged-lepton
  physics;
- close the physical `Q = 2/3` bridge;
- touch the separate `δ = 2/9` Brannen-phase bridge or the `v_0`
  scale lane.

## 9. Audit dependency repair links

This graph-bookkeeping section records explicit dependency links
named by the prior conditional audit so the audit citation graph can
track them. It does not promote this note or change the audited
claim scope.

- [observable_principle_real_d_block_uniqueness_narrow_theorem_note_2026-05-10](OBSERVABLE_PRINCIPLE_REAL_D_BLOCK_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10.md)
- `koide_q_op_locality_source_domain_closure_theorem_note_2026-04-29`
  (cycle-bearing context only; not a load-bearing upstream edge for
  this row until a one-way bridge lemma is extracted)
- [koide_q_readout_factorization_theorem_2026-04-22](KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md)
- [koide_q_minimal_scale_free_selector_note_2026-04-22](KOIDE_Q_MINIMAL_SCALE_FREE_SELECTOR_NOTE_2026-04-22.md)
- [koide_q_reduced_observable_restriction_theorem_2026-04-22](KOIDE_Q_REDUCED_OBSERVABLE_RESTRICTION_THEOREM_2026-04-22.md)
- [koide_q_normalized_second_order_effective_action_theorem_2026-04-22](KOIDE_Q_NORMALIZED_SECOND_ORDER_EFFECTIVE_ACTION_THEOREM_2026-04-22.md)
- [koide_q_no_hidden_source_audit_2026-04-22](KOIDE_Q_NO_HIDDEN_SOURCE_AUDIT_2026-04-22.md)
