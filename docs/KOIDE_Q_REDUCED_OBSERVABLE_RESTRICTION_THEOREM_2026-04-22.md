# Koide Q Reduced Observable Restriction Theorem

**Date:** 2026-04-22
**Claim type:** bounded_theorem
**Status:** bounded algebraic support theorem on the second-order reduced-carrier route
for charged-lepton Koide `Q`; not a closure theorem
**Purpose:** remove the reviewer objection that

```text
W_red(K) = log det(I + K)
```

on the two-slot second-order carrier is only a plausible additive transplant.

**Primary runner:** `scripts/frontier_koide_q_reduced_observable_restriction_theorem.py`

**Status authority and audit hygiene (2026-05-10):**
The audit lane has classified this row `audited_conditional`
(claim_type `bounded_theorem`, audit_date 2026-05-05, auditor
codex-cli-gpt-5.5, auditor_confidence high). The verdict accepts the
runner's symbolic algebra — that on the assumed normalized
two-generator block carrier with `D_red = I_2` and reduced source
`K = diag(k_+, k_perp)`, the observable-principle restriction is
exactly `W_red(K) = log det(I_2 + K) = log(1 + k_+) + log(1 + k_perp)`,
its Legendre dual is `K_* = Y^(-1) - I` with effective action
`S_eff(Y) = Tr(Y) - log det(Y) - 2`, and the unreduced `1 ⊕ 2`
vector-slot determinant is a different object (the `(1, 2)` law).
The verdict flags that the theorem **imports** the normalized
second-order two-generator block carrier and `D_red = I_2` as admitted
structure, and the note explicitly states (Section 5) that the
physical identification of this reduced carrier remains open.
Therefore retained-grade status cannot propagate to the physical
`Q` closure. Audit verdict and effective status are set by the
independent audit lane only; nothing in this rigorization edit
promotes status.

The audit-stated cheapest re-audit path (verbatim from the ledger
`notes_for_re_audit_if_any`):

> missing_bridge_theorem: provide a retained theorem deriving the
> physical charged-lepton observable carrier/readout and
> `D_red = I_2` normalization from the upstream framework.

---

## 1. Exact reduced carrier

Once the first-live second-order charged-lepton sector has been reduced to the
positive two-slot carrier, the split-preserving projectors are exactly

```text
Π_+ + Π_perp = I_2,
Π_+ Π_perp = 0.
```

So the most general split-preserving source is

```text
K = k_+ Π_+ + k_perp Π_perp
  = diag(k_+, k_perp).
```

This is not an ansatz. It is the exact source family on the reduced block
algebra.

---

## 2. Exact restriction of the observable principle

Apply the original observable principle directly on this reduced carrier:

```text
W[J] = log|det(D+J)| - log|det D|.
```

With reduced baseline `D_red = I_2` and reduced source `K`, this gives

```text
W_red(K)
  = log det(I_2 + K)
  = log(1 + k_+) + log(1 + k_perp).
```

So the reduced source law is not "the right additive form by analogy."
It is the exact restriction of the original theorem to the exact reduced
carrier.

Pure-block restriction fixes the coefficients uniquely:

```text
W_red(k_+,0) = log(1+k_+),
W_red(0,k_perp) = log(1+k_perp),
```

leaving no residual coefficient freedom.

---

## 3. Exact dual reduction

The Legendre dual of the reduced source law is therefore exact as well. For
positive `Y = diag(y_1,y_2)`,

```text
K_* = Y^(-1) - I,
S_eff(Y) = Tr(Y) - log det(Y) - 2.
```

So the normalized effective-action theorem is not a separate imported layer. It
is the exact dual of the exact reduced observable generator.

---

## 4. Why this is not the unreduced determinant

On the unreduced `1 ⊕ 2` vector-slot carrier one would have

```text
log det = log(1+k_+) + 2 log(1+k_perp),
```

because the nontrivial doublet is counted twice as ordered vector slots.

The present theorem is different because it works on the **reduced block
algebra of invariant generators**, where there are exactly two independent
positive scalar blocks. That is why the exact restricted law is

```text
log(1+k_+) + log(1+k_perp),
```

not the unreduced `(1,2)` law.

---

## 5. Honest scope

### What this note claims

1. once the normalized second-order two-block carrier is admitted, the reduced
   source law on that carrier is exactly `W_red = log det(I+K)`;
2. its Legendre-dual effective action is then exact on that same carrier;
3. the note removes coefficient ambiguity inside that reduced-carrier route.

### What this note does not claim

1. it does not prove that the physical charged-lepton observable principle must
   live on this reduced two-generator block algebra rather than on the
   unreduced vector-slot carrier or another readout;
2. it does not by itself close the physical/source-law bridge behind
   `Q = 2/3`;
3. it does not touch the separate `δ = 2/9` bridge.

## 6. Bottom line

The strongest exact statement is:

> the reduced two-slot source law `W_red = log det(I+K)` is the exact
> restriction of the original observable principle to the normalized
> second-order block algebra, and its dual effective action is therefore exact
> on that carrier as well.

That is a genuine support theorem for the second-order `Q` route. The
remaining open step is still the physical identification of this reduced
carrier and source law.

## 7. Audit-conditional perimeter

The internal algebra of this note (Sections 1–4) is what the audit
verdict accepts as internally consistent on the admitted reduced
carrier:

| Internal algebra step | Audit-accepted as internal consistency |
|---|---|
| Split-preserving source family `K = diag(k_+, k_perp)` (Section 1) | yes |
| `W_red(K) = log det(I_2 + K)` from `W[J] = log\|det(D + J)\| - log\|det D\|` (Section 2) | yes |
| Pure-block restriction fixes coefficients uniquely (Section 2) | yes |
| Legendre dual `K_* = Y^(-1) - I`, `S_eff(Y) = Tr(Y) - log det(Y) - 2` (Section 3) | yes |
| Contrast with unreduced `(1, 2)` vector-slot determinant (Section 4) | yes |

The audit-conditional perimeter (i.e. what stays open) is the
**physical identification** of the reduced carrier and baseline
already named in Section 5:

1. derive that the physical charged-lepton observable principle must
   live on the **reduced two-generator block algebra** (rather than
   on the unreduced vector-slot carrier or another readout) from
   retained upstream inputs;
2. derive the reduced baseline `D_red = I_2` from retained upstream
   inputs;
3. derive the source family `K = diag(k_+, k_perp)` from retained
   upstream inputs (it is admitted here as the most general
   split-preserving source on the assumed reduced algebra).

Until at least (1) and (2) are supplied, this row remains a bounded
algebraic restriction theorem on the admitted reduced carrier rather
than a physical-identification result. The runner's verdict line in
`logs/runner-cache/` already states this scope explicitly:

> `W_red = log det(I+K)` is not a post-hoc transplant. It is the
> exact restriction of the observable principle to the normalized
> two-generator second-order block algebra. This is support for the
> admitted second-order route. It does not by itself prove that this
> reduced carrier is the physical charged-lepton observable carrier.

## 8. Path A future work (audit-stated repair target)

To move this row's `audit_status` from `audited_conditional` toward
retained-grade, the audit verdict's repair list requires:

1. a retained upstream theorem that the physical charged-lepton
   observable carrier on the second-order surface is the reduced
   two-generator block algebra (not the unreduced `1 ⊕ 2` vector-slot
   carrier);
2. a retained upstream theorem that the reduced baseline is
   `D_red = I_2` (rather than another normalization);
3. either provided independently or as a corollary of (1) and (2).

This same upstream gap also blocks promotion of the companion notes
`KOIDE_Q_NO_HIDDEN_SOURCE_AUDIT_2026-04-22.md` and
`KOIDE_Q_NORMALIZED_SECOND_ORDER_EFFECTIVE_ACTION_THEOREM_2026-04-22.md`,
which use the same admitted reduced carrier.

### 8.1 Candidate upstream supplier notes (graph-bookkeeping only)

The audit-stated repair target is a `missing_bridge_theorem` (class A,
short algebraic bridge): a retained upstream theorem deriving the
physical charged-lepton observable carrier/readout and the
`D_red = I_2` normalization from retained upstream framework inputs.

Four candidate supplier notes already exist on disk in this branch;
their respective load-bearing inferences target the two halves of the
audit-named bridge (carrier identification and baseline normalization)
on the admitted normalized reduced carrier used in this note. They are
recorded here only as graph-bookkeeping dependency edges so the audit
citation graph can track them. Their current audit status does not
propagate retention to this row:

1. `OBSERVABLE_PRINCIPLE_REAL_D_BLOCK_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10.md`
   — block-local uniqueness of the source-derivative content of the
   admissible scalar generator on an invertible real anti-Hermitian
   Dirac block, anchored on the retained
   `CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md`
   structural fact. Targets the audit-named bridge between the
   generator `W = log|det(D+J)| - log|det D|` and any admissible
   scalar generator on a real-D block, including the reduced
   two-generator carrier here once that block is admitted.
2. `KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md`
   — structural composition of OP Theorems 1+2 with
   physical-lattice-necessity §9 (locality is structural content of
   the framework, not a parameterization choice), the canonical
   trace-preserving local descent uniqueness, and the
   `K = 0 ⇔ Y = I_2 ⇔ Q = 2/3` criterion. Targets the audit-named
   reduced-carrier identification half by forcing the framework's
   physical local scalar observables to read through the descent
   `E_loc`, which lands on the normalized `Y = I_2` baseline.
3. `KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md`
   — exact rank/kernel quotient of the linear second-order readout
   map `L : R^4 → Diag_3(R)`, `L(W) = P_{T_1} Γ_1 W Γ_1 P_{T_1}` on
   the retained `Γ_1 / T_1` grammar. Establishes that the readout
   map factors through the species-resolving diagonal carrier with a
   unique unreachable slot, supplying the algebraic skeleton of the
   two-generator block reduction used in this note's Sections 1–2.
4. `KOIDE_Q_MINIMAL_SCALE_FREE_SELECTOR_NOTE_2026-04-22.md`
   — exact uniqueness of the scale-free `C_3`-invariant selector
   ratio on the admitted second-order returned carrier (no nontrivial
   scale-free invariant at linear order; exactly one nontrivial
   ratio at quadratic order). Supplies the carrier-side uniqueness
   matching the source-side restriction proved in this note.

The audit-status of these candidate suppliers as currently recorded in
`docs/audit/data/audit_ledger.json` is independently determined. Two
of the four (`OBSERVABLE_PRINCIPLE_REAL_D_BLOCK_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10.md`
and the underlying `CPT_EXACT_REAL_ANTI_HERMITIAN_D_NARROW_THEOREM_NOTE_2026-05-10.md`)
are already at `retained_bounded` effective status. The remaining two
suppliers are at lower status and contribute to the bridge only
conditionally on their independent audit retention.

The combined load-bearing inference of the supplier chain is:

> on the framework's accepted substrate, the physical local scalar
> observables must read through the canonical descent `E_loc` to the
> diagonal carrier; the source-derivative content of any admissible
> scalar generator on a real-D block coincides with that of
> `W = log|det(D+J)| - log|det D|` up to overall scale; the readout
> map `L` factors through the species-resolving diagonal target; and
> the normalized scale-free selector on the admitted carrier is
> already unique. The reduced two-generator block carrier with
> baseline `D_red = I_2` is therefore the framework-forced reading,
> rather than a free admitted choice.

That inference is the audit-named missing bridge for this row.

This subsection does not promote this row's `audit_status` or the
suppliers' status. Only the independent audit lane can do that. The
load-bearing physical-identification bridge in the auditor's
`verdict_rationale` remains open until at least one of the candidate
supplier chains is itself audited at retained-grade and the
composition is independently judged to close the bridge.

## 9. Boundaries

This note does **not**:

- modify the parent row's audit-ledger entry;
- promote the parent's `audit_status` from `audited_conditional`;
- derive the reduced two-generator block algebra from retained upstream
  inputs;
- derive the reduced baseline `D_red = I_2` from retained upstream
  inputs;
- close the physical `Q = 2/3` bridge;
- touch the separate `delta = 2/9` Brannen-phase bridge.

## 10. Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [observable_principle_real_d_block_uniqueness_narrow_theorem_note_2026-05-10](OBSERVABLE_PRINCIPLE_REAL_D_BLOCK_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10.md)
- `koide_q_op_locality_source_domain_closure_theorem_note_2026-04-29`
  (cycle-bearing context only; not a load-bearing upstream edge for this
  row until a one-way bridge lemma is extracted)
- [koide_q_readout_factorization_theorem_2026-04-22](KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md)
- [koide_q_minimal_scale_free_selector_note_2026-04-22](KOIDE_Q_MINIMAL_SCALE_FREE_SELECTOR_NOTE_2026-04-22.md)
