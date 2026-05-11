# Claim Status Certificate — Cycle 2: P1 Cluster-Decomposition Narrowing

**Date:** 2026-05-10
**Loop:** v-scale-planck-convention
**Cycle:** 02 — cluster-decomp-p1
**Block:** physics-loop/v-scale-g1-cluster-decomp-20260510
**Note:** [`docs/OBSERVABLE_GENERATOR_ADDITIVITY_FROM_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-05-10.md`](../../../../docs/OBSERVABLE_GENERATOR_ADDITIVITY_FROM_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-05-10.md)
**Runner:** [`scripts/frontier_observable_generator_additivity_from_cluster_decomposition.py`](../../../../scripts/frontier_observable_generator_additivity_from_cluster_decomposition.py)
**Runner result:** THEOREM PASS=12 FAIL=0

## Block Type

Bounded-support / narrowing note on the parent
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](../../../../docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
audit row's remaining P1 admission. The note documents that, on the
finite-Grassmann surface `Z[J] = det(D + J)` of the staggered Cl(3)
hopping operator over a finite block of `Z^3`, the three statements

- (A1) `W[J_A (+) J_B] = W[J_A] + W[J_B]` on partitions with no cut
  bond (i.e. P1 as physical-principle admission),
- (A2) `W = log|det(D + J)|` up to additive constant,
- (A3) `W` is the cumulant generating functional of the finite-Grassmann
  moment sequence (mixed kernels vanish across cuts),

are mathematically equivalent up to an additive constant fixed by the
zero-source baseline.

The equivalence is real mathematical content. It does **not** retire
P1 as an admission: it shows that P1 is the same selection as the
canonical cumulant-generator definition (A3) in finite Grassmann field
theory.

## Status

```yaml
actual_current_surface_status: bounded support
target_claim_type: bounded_theorem
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  The equivalence (A1) <=> (A2) <=> (A3) is proved from finite Grassmann
  calculus + Z^3 lattice locality of the staggered Dirac hopping
  operator + Cauchy continuity at J=0 + finite-block polynomial
  analyticity. No new axiom is introduced. However, the equivalence
  does NOT eliminate the definitional selection between additive-class
  generators (cumulant generator) and non-additive functionals of Z[J]:
  it documents that the three forms of the selection are the same
  selection in different language. Hence the parent observable-principle
  row's `audited_conditional` verdict is not flipped by this note.
proposal_allowed: false
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Recommended status (no parent-row flip proposed)

```yaml
# observable_principle_from_axiom_note (parent) — UNCHANGED
effective_status: audited_conditional   # unchanged by this note

# observable_generator_additivity_from_cluster_decomposition_theorem_note_2026-05-10 (new)
proposed_target_status: bounded_theorem (intended)
proposal_allowed: false
proposal_allowed_reason: |
  Equivalence theorem, not closure. The remaining definitional selection
  between additive-class (cumulant generator) and non-additive
  functionals on Z[J] is documented as canonical in finite Grassmann
  field theory but is not eliminated. The parent row's conditional
  shape persists.
```

## Promotion Value Gate (V1-V5)

These answers are required IN WRITING before any PR. Failing any single
question forbids opening the PR as a retained-promotion attempt; in this
case V3 fails the retained-promotion bar, so this PR is opened as a
**bounded-support note**, NOT as a retained-promotion proposal.

### V1 — Verdict-identified obstruction quoted from parent row

Quoted from
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](../../../../docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
§"What remains admitted: P1 (scalar additivity) only":

> P1 — that `W` must satisfy `W[J_1 (+) J_2] = W[J_1] + W[J_2]` on
> independent subsystems — remains an admitted physical-principle
> premise. It is the criterion that selects the additive class of
> generators when defining "physical scalar bosonic observable
> generator". **It cannot be derived from the staggered axiom alone
> without an additional classification axiom about which functionals
> on `Z[J]` are admissible scalar observable generators.**

And from
[`OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md`](../../../../docs/OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md)
§0 verdict-rationale:

> the note proves the `log|det(D+J)|` source-response result only
> after adding scalar additivity, CPT-even phase blindness, continuity,
> and normalization assumptions, and its electroweak-scale consequence
> imports the current hierarchy baseline rather than deriving that
> normalization here.

This note targets the **scalar-additivity** part of the verdict only.

### V2 — New derivation content

A three-way equivalence proof, with companion runner exhibiting it on
small staggered blocks at machine precision:

> Under finite Grassmann calculus on Cl(3) ⊗ Z^3 with the staggered
> hopping operator `D` block-diagonal under no-cut-bond partition
> `D = D_A (+) D_B`, the three statements (A1) scalar-additivity, (A2)
> `W = log|Z|` up to normalization, and (A3) `W` is the cumulant
> generating functional (mixed kernels vanish across cuts) are
> mathematically equivalent.

The equivalence is established in four theorems:

- T1: `Z[J_A (+) J_B] = Z_A[J_A] * Z_B[J_B]` (block multiplicativity)
- T2: (A1) <=> (A2) under continuity (Cauchy functional equation)
- T3: (A2) <=> (A3) (cumulant generating functional Taylor expansion +
  connected-truncated property from block diagonality)
- T4: (A3) <=> (A1) (substituting connected-truncated kernels recovers
  block additivity)

The companion runner verifies T1, T2, T3, T3'' (split-cumulant vanish),
T4, and a cut-bond counterfactual on L=2 and L=4 staggered blocks; all
12 tests pass at relative-error 1e-9 or better (PASS=12 FAIL=0).

### V3 — Could audit lane already complete this from standard math?

**Honest answer: YES, in part.** Standard math machinery (block-diagonal
determinant multiplicativity, Cauchy functional equation, real-analytic
Taylor expansion of `log|det(D + jI)|`) suffices for the equivalence
proof. The parent observable-principle note already shows (A1) =>
(A2) under continuity in §"Theorem 1: additivity forces `log|Z|`" and
P2/P3/P4 derivations.

What this note adds beyond the parent and beyond standard math:

- An explicit (A3) formulation: `W` is the cumulant generating
  functional, with kernels `K_n` connected-truncated across no-cut-bond
  partitions. This was not previously written down as a load-bearing
  equivalent of P1.
- The link to the retained-bounded gauge-sector authority
  [`GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md`](../../../../docs/GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md)
  which already uses `W = log Z` and `C_n = d^n W / dJ^n` as the
  canonical cumulant-generator definition.
- The honest framing that P1 is mathematically equivalent to (A3) and
  therefore cannot be retired by a cluster-decomposition argument alone:
  the cumulant-generator definition is itself a selection.

**This is therefore a bounded-support note** — it documents the
equivalence structure but does NOT retire P1, so the audit lane has not
already done this work (the equivalence had not been written down as
load-bearing) AND the audit lane is not asked to flip the parent verdict.

V3 failing the retained-promotion bar is the **correct** outcome of an
honest stretch attempt: the cluster-decomposition attack does not retire
P1, it narrows it, and the certificate records that openly.

### V4 — Marginal content non-trivial?

**Yes.** The (A1) <=> (A3) equivalence is the load-bearing content. It
is not "real shifts don't change imaginary parts" or "(1/sqrt(N)) * I
has matrix elements 1/sqrt(N)". The connected-truncated property
(T3'') is a structural theorem from block-diagonality, not a definition
restated. The runner exhibits the cumulant kernels vanish numerically
where the equivalence theorem says they must, and the cut-bond
counterfactual at L=4 confirms the no-cut-bond hypothesis is load-
bearing (rel_err goes from ~10^-16 to ~10^11 between no-cut-bond and
cut-bond partitions on the same block).

### V5 — One-step variant of a landed cycle?

**No.** Closest prior cycle in the audit-backlog campaign is cycle 8
([`OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md`](../../../../docs/OBSERVABLE_PRINCIPLE_AUDIT_NOTE_2026-05-02.md)),
which is a metadata / status-correction packet identifying the 4+1
bridge assumptions of the parent row. The structural distinction is:
cycle 8 enumerates the admissions and recommends honest demotion; this
note does not enumerate admissions but proves an algebraic equivalence
between P1 and the canonical cumulant-generator definition in finite
Grassmann field theory.

The parent row's 2026-05-09 update derives P2, P3, P4 as runner-local
algebraic consequences from
[`CPT_EXACT_NOTE.md`](../../../../docs/CPT_EXACT_NOTE.md) content +
finite-block regularity. This note targets the **remaining** P1
admission left open by that update, and approaches it from a different
direction (cluster-decomposition equivalence) than the P2/P3/P4
derivations (CPT-content + polynomial-structure). The 2026-05-09 update
explicitly says P1 cannot be retired from the staggered axiom alone;
this note documents that it CAN be reformulated equivalently as a
canonical cumulant-generator definition, which the audit lane may find
useful when evaluating the parent row's `audited_conditional` shape.

### V1-V5 gate summary

| V# | Status |
|----|--------|
| V1 | Quoted from parent row's "What remains admitted: P1" section + 2026-05-02 audit verdict rationale. |
| V2 | Three-way equivalence (A1) <=> (A2) <=> (A3) on the finite-Grassmann surface, with companion runner PASS=12 FAIL=0. |
| V3 | Standard math can do most of it; the new framing of (A3) as a load-bearing equivalent of P1 was not written down as such before. **Does NOT meet retained-promotion bar.** |
| V4 | Non-trivial: the connected-truncated property + cut-bond counterfactual are structural, not definitional. |
| V5 | Not a one-step variant; targets P1 (left open by 2026-05-09 P2/P3/P4 update) from a different direction. |

V3 fails the retained-promotion bar, so the PR is opened as a **bounded
support note** (not a retained-promotion proposal). The note's
`Type:` field is `bounded_theorem` (intended); the parent row's audit
verdict is NOT proposed for flip.

## Audit-graph effect

- Parent row
  [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](../../../../docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):
  status **unchanged** (`audited_conditional`).
- New note: candidate `bounded_theorem` (intended), awaiting independent
  audit.
- Existing retained gauge-sector authorities
  ([`GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md`](../../../../docs/GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md)
  +
  [`GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md`](../../../../docs/GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md))
  are cited as precedent for the cumulant-generator framework being
  usable on the framework surface; no status change is proposed for
  these either.

## What this closes

- Documents the structural equivalence (A1) <=> (A2) <=> (A3) on the
  finite-Grassmann surface.
- Identifies that the "physical-principle classification axiom" that
  the parent row's P1 admission requires is mathematically equivalent
  to the canonical cumulant-generator definition shared with retained
  gauge-sector content.
- Records the remaining wall: the definitional selection between
  additive-class (cumulant generator) and non-additive functionals of
  `Z[J]` is not eliminated by cluster decomposition alone; it would
  need a retained-grade theorem from `A_min` primitives selecting
  "physical scalar observable = cumulant generator", which is not
  provided here.

## What this does NOT close

- The parent row's `audited_conditional` shape is not flipped.
- The definitional selection step remains.
- No promotion attempt on the parent or on any cited authority.
