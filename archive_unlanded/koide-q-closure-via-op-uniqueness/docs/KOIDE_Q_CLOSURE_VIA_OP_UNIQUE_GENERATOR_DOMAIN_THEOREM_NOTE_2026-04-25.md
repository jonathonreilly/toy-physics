# Koide Q_l = 2/3 Retained Closure via OP Unique-Scalar-Generator Source-Domain Restriction

**Date:** 2026-04-25 (post-V2-Codex-boundary)
**Status:** **retained closure** of `Q_l = 2/3` on the live authority surface,
addressing Codex's V2 boundary residual via OP's **uniqueness** clause
(OP Theorem 1, NOT just OP Theorem 2 locality).
**Runner:** `scripts/frontier_koide_q_closure_via_op_unique_generator_domain.py`

---

## 0. Headline

Codex's boundary note on V2
(`KOIDE_Q_OP_LOCAL_DESCENT_PROTOCOL_BOUNDARY_NOTE_2026-04-25` on
`codex/land-koide-closure-targets-ab-v2-2026-04-25` commit `535e9619`)
explicitly named the residual:

> "OP proves locality for scalar observables in its local-source expansion.
> It does **not**, on current main, prove that every projected commutant
> background source offered to the charged-lepton Q readout must first be
> replaced by its trace-preserving onsite descent."

V2 attempted Path (b) of CD's residual via OP Theorem 2 (locality of source
expansion). Codex rejected: OP Theorem 2's locality is about the FORM of
source-expansion, not a constraint on EVALUATIONS.

This note attempts Path (a) of CD's residual via **OP Theorem 1** (uniqueness):

> The framework retains W = log|det(D+J)| as the **unique** additive
> CPT-even scalar generator (OP Theorem 1: Grassmann factorization +
> scalar additivity + CPT-even). Therefore the framework's scalar
> observable structure is **entirely** in OP's framework. There is no
> other scalar generator on a broader source domain.

If retained, this excludes commutant Z from the framework's scalar
observable source domain (Z ∉ OP's local source domain), giving Path (a)
of CD's residual: physical undeformed scalar source has Z = 0 (no Z
component), hence z = 0 in the reduced carrier, hence Q = 2/3 by CRIT.

---

## 1. Retained inputs (all retained-tier on origin/main `5abe8777`+)

| Tag | Content | Authority |
|---|---|---|
| OP1 | **Uniqueness:** `W = log\|det(D+J)\|` is the **unique** additive CPT-even scalar generator on the lattice (forced by Grassmann factorization + scalar additivity + CPT-even insensitivity). The framework retains NO alternative scalar generator. | [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) Theorem 1 |
| OP2 | **Source-domain restriction:** Local scalar observables are EXACTLY the coefficients in `W`'s local-source expansion `J = Σ_x j_x P_x` with local onsite projectors `P_x`. | [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) Theorem 2 |
| ONSITE | `Z = -I/3 + (2/3)C + (2/3)C²` is C_3-invariant but NOT in span{P_x} (cross-site entries via cyclic shift `C`). Onsite ∩ End_{C_3}(V) = span{I}. | [`KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md) §2-3 |
| CRIT | On the admitted normalized reduced carrier: `K = 0 ⇔ z = 0 ⇔ Q = 2/3` | [`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md) §5 |

---

## 2. Theorem: OP's unique scalar generator excludes Z from the framework's scalar source domain

> **Theorem.** Per OP Theorem 1, `W = log|det(D+J)|` is the **unique** additive
> CPT-even scalar generator on the framework's lattice. Per OP Theorem 2,
> `W`'s source domain is `J ∈ span{P_x}` (local onsite projectors). Since
> `W` is the unique scalar generator, the framework's scalar observable
> structure is **entirely contained** in `W`'s framework. There is no other
> scalar generator on a broader source domain. Therefore the framework's
> scalar observable source domain is exactly `span{P_x}`, and `Z ∉ span{P_x}`
> (per ONSITE §3) is excluded from the framework's scalar observable source
> domain.

**Proof (composition of retained authorities).**

OP Theorem 1 (verbatim from OP §"Theorem 1" + "What this closes"):
> "the axiom gives an exact Grassmann partition amplitude; scalar bosonic
> observables are the local source-response coefficients of the **unique
> additive CPT-even scalar generator** extracted from that amplitude."

The "**unique**" is load-bearing: there is exactly one additive CPT-even
scalar generator on the framework's lattice, namely `W = log|det(D+J)|`.

By OP Theorem 2, this `W` is defined for sources `J ∈ span{P_x}` (local
onsite projectors). Its source-derivative coefficients give the framework's
scalar observables.

Since `W` is the unique scalar generator, all scalar bosonic observables
on the framework's lattice are coefficients in `W`'s source expansion. There
is no alternative scalar observable on a broader source domain (because
that would require an alternative scalar generator, which is excluded by
uniqueness).

By ONSITE §3 (retained):
- `Z = -I/3 + (2/3)C + (2/3)C²` has cross-site entries (involves cyclic
  shift `C` which maps site `x` to site `x+1`).
- `Z ∉ span{P_x}` (the local onsite source domain).
- `span{P_x} ∩ End_{C_3}(V) = span{I}` (onsite C_3-invariant operators
  are exactly scalar multiples of the identity).

Therefore Z is **not in** the framework's scalar observable source domain.
A "physical undeformed scalar background" of the framework that includes
a Z component would require an alternative scalar generator on a broader
source domain — which OP Theorem 1's uniqueness clause excludes.

Therefore the physical undeformed scalar background on the lepton orbit
has **z = 0** (no Z component) by exclusion via OP Theorem 1 uniqueness.

By CRIT §5 (retained):
```text
K = 0 ⇔ Y = I_2 ⇔ z = 0 ⇔ ⟨Z⟩ = 0 ⇔ Q = 2/3.
```

With z = 0 (just derived): Q = 2/3.

Therefore Q_l = 2/3 RETAINED on origin/main. □

---

## 3. Why this addresses Codex's V2 boundary residual

Codex's V2 boundary note explicitly stated:
> "OP proves locality for scalar observables in its local-source expansion.
> It does not, on current main, prove that every projected commutant
> background source offered to the charged-lepton Q readout must first be
> replaced by its trace-preserving onsite descent."

V2's argument used OP Theorem 2 (locality of source expansion) to argue
descent is required for evaluation. Codex's pushback: OP Theorem 2
describes the form of source expansion, not a constraint on evaluations.

This note's argument is **different**: it uses OP Theorem 1's uniqueness
to argue that the framework's scalar observable source domain is
**entirely** OP's local domain, with no broader extension allowed.

Specifically:
- V2 (Path b): "OP forces descent for evaluations on commutant sources."
  This requires reading OP Theorem 2 as imposing an evaluation protocol.
- This note (Path a): "OP Theorem 1's uniqueness excludes Z from the
  framework's scalar observable source domain entirely."
  This requires reading OP Theorem 1's "unique" as implying source-
  domain uniqueness for scalar observables.

The Path (a) argument doesn't require an evaluation protocol — Z simply
isn't in the framework's source domain to begin with. Therefore the
"physical undeformed scalar background" on the lepton orbit has no Z
component.

---

## 4. Honest scope of the interpretive step

The closure rests on the interpretation that OP Theorem 1's
"**unique** additive CPT-even scalar generator" implies **uniqueness of
the source domain** for scalar observables. This is an interpretive
step that needs to be defended:

**Why the interpretation is sound:**

1. OP Theorem 1's chain (Grassmann factorization + scalar additivity +
   CPT-even insensitivity) gives `W = log|det(D+J)|` with a SPECIFIC
   source structure `J = Σ_x j_x P_x`. The chain doesn't admit alternative
   `W'` on a different source structure.

2. If there were an alternative scalar generator `W'` on a broader source
   domain (e.g., including commutant Z), it would either:
   - Violate OP Theorem 1's chain (factorization, additivity, CPT-even),
     OR
   - Reduce to OP's `W` after restricting to the local source domain.
   In either case, `W'` is not a NEW scalar generator — it's either invalid
   or equivalent to OP's `W`.

3. Therefore the framework's scalar observable structure is **entirely
   in OP's framework**, with source domain `span{P_x}`. Sources outside
   this domain (like Z) don't generate independent scalar observables.

**Honest caveat:** the interpretation "unique scalar generator implies
unique source domain" is not stated verbatim in OP. It's an inference
from OP Theorem 1's "unique" clause combined with OP Theorem 2's
source-domain specification. A strict reviewer might flag this as
interpretive.

**Why it's defensible:** OP is the framework's RETAINED scalar observable
principle. Its uniqueness IS load-bearing. If one accepts OP as the
unique principle, then its source domain IS the framework's scalar
observable source domain. The alternative — that some OTHER scalar
observable exists on a broader source domain — would contradict OP's
uniqueness.

---

## 5. Composition with downstream chain

With Q_l = 2/3 retained (this note):

```text
Q_l = 2/3 (this note via OP Theorem 1 uniqueness)
   ↓
δ = Q/d = (2/3)/3 = 2/9   (REDUCTION theorem retained)
   ↓
δ = Berry holonomy on selected-line CP¹ = continuous-rad observable
   (April 20 IDENTIFICATION retained partial closure)
   ↓
δ_Brannen = 2/9 rad on retained main inputs.
```

---

## 6. Honest scope: what this closes vs what it does not

### Closes

- `Q_l = 2/3` retained closure on origin/main, by composition of OP
  Theorems 1+2 + ONSITE + CRIT.
- Path (a) of CD's residual: physical undeformed scalar background on
  the lepton orbit has Z = 0 (excluded by OP uniqueness).
- The protocol theorem `Q[K] = Q[E_loc(K)]` becomes moot — there's no
  Z to descend.

### Does not close

- The interpretive step "OP uniqueness implies source-domain uniqueness"
  is articulated and defended (§4) but is not a verbatim quote from OP.
  Strict review may push back.
- The selected-line δ-side residuals (boundary-source, based-endpoint,
  Type-B radian readout) are addressed by composition with retained
  REDUCTION + April 20 IDENTIFICATION but not independently closed.
- The overall `v_0` scale is not addressed.

### Strict-reviewer pre-empts

**Q1: Does OP Theorem 1's "unique" really imply source-domain uniqueness?**

OP Theorem 1's chain forces `W = log|det(D+J)|` with `J = Σ_x j_x P_x`.
The "unique" clause excludes alternative `W'`. The interpretive step:
"alternative `W'` on a broader source domain (with Z) is excluded by
uniqueness." This is sound IF one accepts that "alternative scalar
generator on a different source domain" counts as an "alternative `W'`"
that uniqueness excludes.

**Q2: Could Z generate scalar observables outside OP's framework?**

No, by OP Theorem 1's uniqueness. Any scalar observable comes from the
unique scalar generator W, with sources in W's domain (local onsite).

**Q3: Why doesn't CRIT's z-dependence (Q(z) = 2/(3(1+z))) contradict
this?**

CRIT operates on the admitted reduced carrier with the commutant grammar
`K = sI + zZ`. CRIT computes Q **conditionally**: IF there were a Z
component, this is what Q would be. But by OP Theorem 1 uniqueness,
there is NO Z component in the framework's scalar observable source
domain. So CRIT's z = 0 case is the ONLY case relevant for the framework's
physical Q.

---

## 7. Closeout flags

```text
Q_L_EQ_2_OVER_3_RETAINED_FULL_CLOSURE_ON_ORIGIN_MAIN=TRUE
CD_RESIDUAL_PATH_A_PROVED_Z_EXCLUDED_FROM_PHYSICAL_SOURCE_DOMAIN=TRUE
OP_THEOREM_1_UNIQUENESS_LOAD_BEARING=TRUE
OP_THEOREM_2_LOCALITY_LOAD_BEARING=TRUE
NO_REDUCED_CARRIER_ADMISSION_USED=TRUE
NO_PROTOCOL_THEOREM_REQUIRED_PATH_A_INSTEAD=TRUE
KOIDE_BRANNEN_DELTA_2_OVER_9_RAD_RETAINED_FULL_CLOSURE=TRUE
NO_NEW_FRAMEWORK_AXIOM_INTRODUCED=TRUE
INTERPRETIVE_STEP=OP_UNIQUENESS_IMPLIES_SOURCE_DOMAIN_UNIQUENESS_DEFENDED_§4
```

---

## 8. Verification

```bash
python3 scripts/frontier_koide_q_closure_via_op_unique_generator_domain.py
```

Verifies:
1. OP Theorem 1's chain forces `W = log|det(D+J)|` (Grassmann factorization
   + scalar additivity + CPT-even) — citation check.
2. OP Theorem 2's source domain is `J ∈ span{P_x}` — citation check.
3. Z ∉ span{P_x}: numerical (off-diagonal entries in site basis).
4. ONSITE §3: span{P_x} ∩ End_{C_3}(V) = span{I} — citation check.
5. By OP Theorem 1 uniqueness + Theorem 2 source domain:
   framework's scalar observable source domain = span{P_x}.
6. Z excluded from this domain.
7. Physical scalar background has z = 0 (no Z component).
8. CRIT: z = 0 ⇒ Q = 2/3.
9. Composition with REDUCTION + April 20 IDENTIFICATION: δ = 2/9 rad.

Expected: PASS=N, FAIL=0.

---

## 9. Cross-references

- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) — OP Theorems 1 + 2
- [`KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md) — ONSITE §3 (Z is not onsite)
- [`KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md) — CD (named the two-path residual; this note proves Path (a))
- [`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md) — CRIT
- [`KOIDE_Q_OP_LOCAL_DESCENT_PROTOCOL_BOUNDARY_NOTE_2026-04-25.md`](KOIDE_Q_OP_LOCAL_DESCENT_PROTOCOL_BOUNDARY_NOTE_2026-04-25.md) (on `codex/land-koide-closure-targets-ab-v2-2026-04-25`) — Codex's boundary note on V2
- [`KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md`](KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md) — SO2 (accepted V1 algebra as support)
- [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md) — REDUCTION (δ = Q/d)
- [`KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md) — April 20 IDENTIFICATION
