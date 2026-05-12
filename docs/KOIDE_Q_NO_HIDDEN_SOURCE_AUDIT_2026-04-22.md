# Koide Q No-Hidden-Source Audit

**Date:** 2026-04-22
**Status:** exact support audit on the second-order `Q` route; not a closure
theorem
**Purpose:** sharpen two review risks at once:

1. show that no earlier/admissible carrier closes `Q` cleanly, and
2. show that any nonzero reduced source on the normalized second-order carrier
   would merely re-encode an arbitrary selector choice.

**Primary runner:** `scripts/frontier_koide_q_no_hidden_source_audit.py`

**Status authority and audit hygiene (2026-05-10):**
The audit lane has classified this row `audited_conditional` (audit_date
2026-05-05, auditor codex-cli-gpt-5.5, auditor_confidence high). The
verdict accepts the symbolic algebra performed by the runner — that
`K = 0 ⇔ y = 1 ⇔ Y = I_2` on the asserted normalized carrier
`Y = diag(y, 2-y)` with `K = Y^(-1) - I` — but flags that the packet
does not derive (a) the normalized second-order carrier itself, (b) the
exact dual equation `K = Y^(-1) - I`, or (c) the readout from `Y = I_2`
to the physical `Q = 2/3` route from retained upstream inputs. Audit
verdict and effective status are set by the independent audit lane
only; nothing in this rigorization edit promotes status. The note's
Section 4 "Bottom line" already states this honestly; the present
edit makes the audit-conditional perimeter explicit at the top of the
note.

The audit-stated cheapest re-audit path (verbatim from the ledger
`notes_for_re_audit_if_any`):

> missing_dependency_edge: provide retained upstream support for the
> normalized second-order carrier, the exact dual equation, and the
> `Y = I_2 -> kappa = 2 -> Q = 2/3` readout, then re-audit the scoped
> closure.

---

## 1. Earlier carrier audit

The branch-local route remains consistent with the earlier no-gos:

- the raw chiral bridge `Y = P_R Γ_1 P_L` has zero bosonic
  `log|det|` response on a scalar baseline;
- the unreduced determinant carrier still lands on the `(1,2)` leaf and gives
  `kappa = 1`, not `2`.

So the present route is not hiding a contradiction. It really does live on a
later carrier.

---

## 2. Hidden-source audit on the normalized carrier

On the normalized positive carrier,

```text
Y = diag(y, 2-y),   0 < y < 2,
```

the exact dual equation is

```text
K = Y^(-1) - I.
```

So every normalized point determines a unique reduced source

```text
K(y) = diag(1/y - 1, 1/(2-y) - 1).
```

The crucial consequence is:

```text
K = 0   <=>   y = 1   <=>   Y = I_2.
```

So there is exactly one datum-free point.

If one also imposes the normalized trace condition `Tr(Y)=2`, then the
admissible nonzero sources form a **one-parameter family**. That family is
exactly the same one free parameter as the selector variable itself.

In other words:

> a hidden nonzero source does not explain the selector value; it merely
> re-parameterizes an arbitrary chosen point on the selector family.

That is why `K = 0` is load-bearing. It is not a convenience choice. It is the
only source choice that does not smuggle in the value being derived.

---

## 3. Review consequence

The clean reviewer statement is:

```text
source-free on the normalized second-order carrier
```

means exactly:

- no added target matrix,
- no nonzero selector source,
- no hidden one-parameter datum equal in content to the unknown `Q` value.

Then the exact dual equation gives

```text
Y = I_2,
```

which is exactly

```text
E_+ = E_perp
-> kappa = 2
-> Q = 2/3.
```

---

## 4. Bottom line

The second-order route survives the hidden-source audit:

> any nonzero reduced source is just the selector value written in source
> coordinates, while the source-free point `K = 0` is the unique datum-free
> closure point of the normalized carrier.

That sharply narrows the remaining primitive. What it does **not** yet prove is
that retained charged-lepton physics forces the physical lane to be source-free
on that carrier.

## 5. Audit-conditional perimeter

This note's contribution is the **algebraic** narrowing inside the
admitted normalized second-order carrier `Y = diag(y, 2-y)` with
reduced source `K = Y^(-1) - I`: it shows the family of nonzero
sources is a one-parameter selector reparameterization, and that
`K = 0` is the unique datum-free point. That algebraic step is what
the audit verdict accepts as internally consistent.

The audit-conditional perimeter (i.e. what stays open) is exactly:

1. derive the normalized second-order positive trace-2 carrier
   `Y = diag(y, 2-y)` from retained upstream charged-lepton physics
   (the carrier is admitted as input here);
2. derive the exact dual equation `K = Y^(-1) - I` from a retained
   reduced observable generator (this note imports it from the
   companion reduced-observable note, which is itself
   `audited_conditional` on the same gap);
3. derive the readout from `Y = I_2` through `kappa = 2` to the
   physical `Q = 2/3` from a retained Brannen / circulant identity
   on the charged-lepton selector.

Until at least (1) and (2) are supplied by retained upstream notes,
this row remains a bounded algebraic hidden-source audit on the
admitted normalized carrier rather than a physical-identification
result. The runner's verdict line in `logs/runner-cache/` already
states this scope explicitly:

> This narrows the remaining primitive; it does not itself prove the
> physical charged-lepton lane must be source-free there.

## 6. Boundaries

This note does **not**:

- modify the parent row's audit-ledger entry;
- promote the parent's `audit_status` from `audited_conditional`;
- derive the normalized second-order carrier from retained upstream
  inputs;
- derive the exact dual equation from a retained observable generator;
- close the physical `Q = 2/3` bridge.

These are the same audit-named open dependencies that block the
reduced observable restriction note and the normalized second-order
effective action note in the same `Q` cluster (see audit ledger rows
`koide_q_reduced_observable_restriction_theorem_2026-04-22` and
`koide_q_normalized_second_order_effective_action_theorem_2026-04-22`).

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_q_reduced_observable_restriction_theorem_2026-04-22](KOIDE_Q_REDUCED_OBSERVABLE_RESTRICTION_THEOREM_2026-04-22.md)
- [koide_q_normalized_second_order_effective_action_theorem_2026-04-22](KOIDE_Q_NORMALIZED_SECOND_ORDER_EFFECTIVE_ACTION_THEOREM_2026-04-22.md)
