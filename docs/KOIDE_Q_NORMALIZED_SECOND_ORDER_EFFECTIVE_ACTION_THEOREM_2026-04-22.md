# Koide Q From The Normalized Second-Order Effective Action

**Date:** 2026-04-22
**Status:** exact support / candidate value-law note on the second-order `Q`
route; not a closure theorem
**Purpose:** sharpen the last remaining value-law gap in the branch-local
`Q = 2/3` route without:

- primitive adoption,
- quartic-potential import,
- unreduced determinant weighting,
- hand-inserted target/seed data.

**Primary runner:** `scripts/frontier_koide_q_normalized_second_order_effective_action.py`

**Status authority and audit hygiene (2026-05-10):**
The audit lane has classified this row `audited_conditional`
(claim_type `open_gate`, audit_date 2026-05-05, auditor
codex-cli-gpt-5.5, auditor_confidence high). The verdict accepts the
runner's symbolic algebra — that `K = 0 -> Y = I_2 -> Q = 2/3` closes
on the admitted normalized second-order positive trace-2 carrier with
the exact reduced observable generator `W_red(K) = log det(I + K)` and
its Legendre dual `S_eff(Y) = Tr(Y) - log det(Y) - 2`. The verdict
flags that the load-bearing **physical** premise is the source-free
law `K = 0` on the normalized second-order charged-lepton carrier,
and the note explicitly says (Section 8) this remains open. With no
cited retained authority closing that bridge, retained-grade status
cannot propagate to the physical `Q` closure. Audit verdict and
effective status are set by the independent audit lane only; nothing
in this rigorization edit promotes status.

The audit-stated cheapest re-audit path (verbatim from the ledger
`notes_for_re_audit_if_any`):

> missing_bridge_theorem: prove from retained charged-lepton physics
> that the normalized second-order physical selector has zero external
> source `K = 0`.

---

## 1. What was still open

The branch-local stack before this note already established:

1. the exact second-order `Γ_1` return is the **first live**
   species-resolving local bosonic returned object on `T_1`;
2. its cyclic scalar sector reduces exactly to the two positive block powers

   ```text
   E_+    = r0^2 / 3,
   E_perp = (r1^2 + r2^2) / 6;
   ```

3. after quotienting by overall scale, there is only **one** nontrivial
   selector variable.

So the remaining issue was not:

- which carrier to use,
- or which invariant to read.

It was only:

> what exact native value law picks the physical point on that one-dimensional
> normalized positive carrier?

---

## 2. Normalize the first-live positive carrier

Because the `Q` selector is scale-free, the physical datum on the positive
second-order carrier is not `(E_+, E_perp)` itself but its projective class.

The canonical normalized representative is

```text
Y = 2 K_quad / Tr(K_quad),
K_quad = diag(E_+, E_perp),
```

so

```text
Y = diag(2 E_+ / (E_+ + E_perp), 2 E_perp / (E_+ + E_perp)),
Tr(Y) = 2.
```

This removes the overall scale exactly and introduces no new law.

Most importantly,

```text
Y = I_2   <=>   E_+ = E_perp.
```

So the `Q` bridge would close if the normalized physical carrier were forced to
the identity point of the positive trace-2 cone.

---

## 3. Exact reduced observable generator

The observable-principle authority already fixed the sole-axiom scalar source
generator:

```text
W[J] = log|det(D+J)| - log|det D|.
```

On the exact first-live second-order carrier, the independent positive scalar
slots are the two block variables. Additivity on independent blocks and the
same one-block normalization used in the observable-principle note give the
reduced generator

```text
W_red(K) = log det(I + K)
         = log(1 + K_+) + log(1 + K_perp)
```

for block source

```text
K = diag(K_+, K_perp),   K > -I.
```

This is the key strengthening over the earlier branch-local `log det` note:
the value law is no longer presented as "a plausible additive scalar on the
two-slot carrier." It is the exact reduced observable generator forced by the
same multiplicative-to-additive logic as the original authority theorem.

---

## 4. Exact effective action on the normalized carrier

Take the Legendre dual of the reduced source generator on the positive carrier.
For positive `Y = diag(y_1, y_2)`, define

```text
Phi(K;Y) = W_red(K) - Tr(KY).
```

The unique maximizer is

```text
K_* = Y^(-1) - I,
```

and substituting it back gives the exact effective action

```text
S_eff(Y) = Tr(Y) - log det(Y) - 2.
```

This is the same native observable-to-effective-action reduction already used
successfully on the DM lane, now applied to the first-live charged-lepton
second-order carrier.

No external entropy principle is imported.

---

## 5. Direct source-free candidate on the normalized cone

The exact dual relation is

```text
K_* = Y^(-1) - I.
```

With zero external selector source,

```text
K = 0,
```

the dual relation gives immediately

```text
Y = I_2.
```

that gives the desired candidate closure point:

```text
Y = I_2   <=>   E_+ = E_perp.
```

The effective-action minimum is still true, but it is now only a consistency
check. On the normalized trace slice `Tr(Y) = 2`, write `Y = diag(y, 2-y)`.
Then

```text
S_eff(Y) = - log(y (2-y)),
```

which has the unique interior stationary point `y = 1` with positive second
derivative there. So the source-free point `Y = I_2` is also the unique
minimum of the exact effective action on the normalized cone.

This step is fully **seed-free** once `K = 0` is admitted. The load-bearing
review question is whether retained charged-lepton physics forces that
source-free law on this normalized carrier.

---

## 6. Exact Koide consequence

Because `Y = I_2` is exactly `E_+ = E_perp`, we obtain

```text
r0^2 / 3 = (r1^2 + r2^2) / 6
<=> 2 r0^2 = r1^2 + r2^2
<=> a^2 = 2 |b|^2
<=> kappa = 2.
```

Then the exact Brannen/circulant identity gives

```text
Q = (1 + 2/kappa) / 3 = 2/3.
```

So on this branch-local route the candidate value-law chain is:

```text
observable principle
-> first-live second-order bosonic returned carrier
-> exact reduced block source generator log det(I+K)
-> exact Legendre-dual effective action
-> exact zero-source equation K = 0
-> Y = I_2
-> E_+ = E_perp
-> kappa = 2
-> Q = 2/3.
```

---

## 7. Why this is stronger than the earlier branch-local extremum note

The earlier branch-local close candidate already showed that

```text
log det K_quad
```

on the fixed-power slice gives `E_+ = E_perp`.

What this note adds is a stronger derivation layer *inside the admitted
second-order reduced carrier*:

- the physical carrier is normalized because `Q` is scale-free;
- the reduced block generator is the exact `log det(I+K)` observable generator;
- the value law is the exact Legendre-dual effective action on that carrier;
- the exact zero-source dual equation already fixes the physical point.

So the value law is no longer just "an attractive stationary principle." It is
the exact effective-action law attached to the admitted first-live carrier
itself, and its source-free equation lands on the Koide point.

---

## 8. Honest scope

### What this note claims

1. the branch-local `Q` route now has a native effective-action derivation on
   the normalized second-order carrier;
2. that derivation is seed-free and does not import a target point;
3. it isolates the remaining open primitive sharply as the physical
   source-free law `K = 0` on that carrier.

### What this note does not claim

1. it does not address the separate `delta = 2/9` bridge;
2. it does not rewrite review/public authority surfaces;
3. it does not erase the earlier no-go on the **unreduced** determinant carrier;
4. it does not prove from retained charged-lepton physics that the physical
   selector is source-free on this carrier.

---

## 9. Bottom line

The strongest science-only statement I can now defend is:

> on the normalized first-live second-order bosonic carrier, the exact
> Legendre-dual effective action has source-free point `Y = I_2`, i.e.
> `E_+ = E_perp`, hence `Q = 2/3`.

If review accepts the already-sharpened identification

```text
physical selector = scalar on the exact first-live second-order returned
carrier,
```

then the remaining open step is exactly why the physical charged-lepton lane is
source-free there. This note narrows that primitive sharply; it does not by
itself discharge it.

## 10. Audit-conditional perimeter

The internal algebra of this note (Sections 2–6) is what the audit
verdict accepts as internally consistent on the admitted normalized
second-order carrier:

| Internal algebra step | Audit-accepted as internal consistency |
|---|---|
| Trace normalization `Tr(Y) = 2` (Section 2) | yes |
| Reduced observable generator `W_red(K) = log det(I + K)` (Section 3) | yes |
| Legendre dual `S_eff(Y) = Tr(Y) - log det(Y) - 2` (Section 4) | yes |
| Dual relation `K = Y^(-1) - I` (Section 5) | yes |
| `K = 0 -> Y = I_2 -> kappa = 2 -> Q = 2/3` (Sections 5–6) | yes (algebraic) |

The audit-conditional perimeter (i.e. what stays open) is the single
**physical** bridge already named in Section 8:

> derive from retained charged-lepton physics that the physical
> selector lives on the admitted normalized second-order reduced
> carrier and is source-free there.

The reduced observable restriction theorem
(`KOIDE_Q_REDUCED_OBSERVABLE_RESTRICTION_THEOREM_2026-04-22.md`) is
the upstream supplier of `W_red` on the same admitted carrier; it is
itself `audited_conditional` on the same physical-identification gap
(see audit ledger row
`koide_q_reduced_observable_restriction_theorem_2026-04-22`). So
upstream support for `W_red` is also `audited_conditional`, not
retained.

Within this audit-conditional perimeter, the runner's reproduced
verdict line is:

> on the exact first-live second-order carrier, the source-free
> normalized effective-action route lands at `Y = I_2`. That is
> exactly `E_+ = E_perp`, hence `kappa = 2` and `Q = 2/3`. This
> validates the internal algebra of the admitted second-order route.
> It does not by itself prove the physical source-free law.

That is exactly the `claim_type = open_gate` framing recorded in the
audit ledger.

## 11. Path A future work (audit-stated repair targets)

To move this row's `audit_status` from `audited_conditional` toward
retained-grade, the audit verdict's repair list requires **either**:

1. a retained upstream theorem that the physical charged-lepton
   selector lives on the normalized second-order positive trace-2
   reduced carrier `Y` (the carrier-identification half), **and**
2. a retained upstream theorem that the physical charged-lepton
   source on that reduced carrier is `K = 0` (the source-free half);

**or** an alternative carrier whose retained derivation directly
forces `E_+ = E_perp` without invoking the
admitted-carrier-plus-`K = 0` route used here.

Until at least one such retained upstream chain is supplied, the row
remains a bounded internal-algebra `open_gate` note on the admitted
carrier rather than a `Q = 2/3` closure.

### 11.1 Candidate upstream supplier notes (graph-bookkeeping only)

A subsequent campaign has filed three candidate upstream supplier
notes that together target the audit-stated source-free half (item 2
above) on the admitted normalized reduced carrier. They are recorded
here only as graph-bookkeeping edges so the audit citation graph can
track them; their current audit status does not propagate retention
to this row:

1. `KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md`
   — proves uniqueness of the trace-preserving local descent
   `E_loc : A -> D^C3` on the `C3`-commutant source algebra
   `A = span{I, Z}`, and shows that this descent annihilates the
   reduced traceless `Z` coordinate modulo a common scalar shift.
2. `KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`
   — establishes the criterion equivalence
   `K = 0 <=> Y = I_2 <=> z = 0 <=> Q = 2/3`
   on the admitted normalized reduced carrier used in this note.
3. `KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md`
   — composes the canonical-descent uniqueness with the observable
   principle's source-domain restriction
   (`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`) and the structural
   locality content of `PHYSICAL_LATTICE_NECESSITY_NOTE.md` §9 to
   target the source-free half on the admitted carrier.

The audit-status of these candidate suppliers as currently recorded
in `docs/audit/data/audit_ledger.json` is independently determined.
Two of the three suppliers (the canonical-descent theorem and the
OP-locality closure note) reduce the load-bearing inference to:

> the framework's physical local scalar observables on a background
> in the projected `C3`-commutant must be read after canonical local
> descent `E_loc`, which kills the reduced traceless `Z` coordinate
> and hence picks out `K = 0` on the admitted normalized reduced
> carrier.

That inference is the audit-named missing bridge for this row's
source-free half. The third supplier (`CRIT`) closes the bridge
between `K = 0` and `Q = 2/3` on the admitted carrier, which is
itself reproduced internally by this note's Sections 5–6 (see
table in Section 10).

This subsection does not promote this row's `audit_status` or the
suppliers' status. Only the independent audit lane can do that. The
load-bearing physical bridge in the auditor's verdict_rationale
remains open until at least one of the candidate supplier chains is
itself audited at retained-grade.

## 12. Boundaries

This note does **not**:

- modify the parent row's audit-ledger entry;
- promote the parent's `audit_status` from `audited_conditional`;
- derive the normalized second-order reduced carrier from retained
  upstream inputs;
- derive the source-free law `K = 0` from retained charged-lepton
  physics;
- close the separate `delta = 2/9` Brannen-phase bridge;
- claim a Nature-grade closure of `Q = 2/3` on the charged-lepton
  lane.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_q_reduced_observable_restriction_theorem_2026-04-22](KOIDE_Q_REDUCED_OBSERVABLE_RESTRICTION_THEOREM_2026-04-22.md)
- [koide_q_source_domain_canonical_descent_theorem_note_2026-04-25](KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md)
- [koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md)
- [koide_q_op_locality_source_domain_closure_theorem_note_2026-04-29](KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md)
