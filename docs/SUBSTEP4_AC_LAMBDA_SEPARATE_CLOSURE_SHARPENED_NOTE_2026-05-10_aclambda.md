# Substep-4 AC_λ Separate-Closure (Sharpened, Partial)

**Date:** 2026-05-10
**Type:** sharpened_bounded_theorem
**Claim type:** bounded_theorem (sharpened partial closure of AC_λ atom only)
**Scope:** Separate closure of the AC_λ atom of the substep-4 atomic
decomposition, leaving AC_φ and AC_φλ untouched. Source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.
**Authority role:** source-note proposal — the substep-4 surface status
remains `bounded_theorem`. This note narrows the substep-4 admitted
context further by separating AC_λ closure from the joint amplitude-
equipartition atom AC_φλ (= BAE), and shows that under retained meta
clarifications (PR #728 and PR #729) plus the runner-certified
Kawamoto-Smit block-diagonality (already cached on main), the AC_λ-
restricted sub-content of substep-4 admits a partial ratchet from
bounded-with-three-atoms to bounded-with-two-atoms.
**Loop:** physics-loop / substep4-aclambda-separate-20260510
**Primary runner:** [`scripts/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.py`](../scripts/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.py)
**Cache:** [`logs/runner-cache/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.txt`](../logs/runner-cache/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.txt)

## Authority disclaimer

This is a source-note proposal. The independent audit lane has full
authority to retag, narrow, or reject. The author does NOT propose a
positive_theorem promotion at this time; the result is sharpened bounded
because the AC_λ closure inherits the bounded tier of its load-bearing
upstream (Kawamoto-Smit forcing, currently `bounded_theorem` on main)
plus the meta-companion notes (currently `meta` source-note proposals
themselves). No new axioms are added. No PDG values are imported.

## Question

Per [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md),
the substep-4 admitted-context decomposes as

```
AC_narrow = AC_φ ∧ AC_λ ∧ AC_φλ
```

The 30-probe BAE campaign (PR #836) attacked the joint
amplitude-equipartition atom AC_φλ extensively and reached terminal
bounded-obstruction state. The AC_φ atom is now reframed as a bounded
structural no-go candidate within A_min under preserved-`C_3` framing
(rigorization 2026-05-09). The AC_λ atom was attacked only as a joint
"runner-certified bounded candidate via Kawamoto-Smit" (rigorization
addendum 2026-05-09) but has not been examined as an
**independently-closeable** atom separated from AC_φλ.

Recent retained meta clarifications change the question:

- [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
  (PR #728) records that `{smallest λ_k, middle λ_k, largest λ_k} ↔
  {electron, muon, tau}` is a labeling convention identical in nature
  to `{u, c, t}`, `{ν_1, ν_2, ν_3}`, etc., consuming zero retained-grade
  content.
- [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
  (PR #729) records that labeling and unit conventions are the same
  kind of bookkeeping operation, never derivation input.
- [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
  (PR #790) makes explicit that AC_φλ is now exclusively the BAE
  (amplitude-equipartition `|b|²/a² = 1/2`) condition, separated from
  any species-label / mass-ordering content.

Question: under these retained meta clarifications plus the runner-
certified Kawamoto-Smit block-diagonality, does AC_λ close
**separately** from AC_φλ at a stronger sub-tier?

## Answer

**SHARPENED partial closure.** Under {Kawamoto-Smit forcing
(`bounded_theorem` on main); the C_3-preserved interpretation note (PR
#728); the conventions-unification companion note (PR #729); the BAE
rename note (PR #790)}, the AC_λ atom **separates cleanly** from AC_φλ
into two sub-claims:

- **AC_λ.struct (block-diagonality):** `⟨χ̄_{c_α}(x) χ_{c_β}(y)⟩_Ω =
  δ_{αβ} S_α(x − y)` with no inter-corner mixing in the free measure
  on `H_{hw=1}`. **Status: runner-certified bounded candidate** via
  interval-certified Kawamoto-Smit (Reed-Simon I §VIII.5 simultaneous-
  diagonalization on commuting `(T_x, T_y, T_z)` with pairwise distinct
  joint eigenvalues `((-1,1,1), (1,-1,1), (1,1,-1))`). Inherits bounded
  tier from its Kawamoto-Smit upstream.

- **AC_λ.label (species-kind label):** the species-label is the
  *kind-of-label* used throughout particle physics for distinct fermion
  carriers (analogue: `{u, d, s, c, b, t}` are species labels on
  distinct quark carriers). **Status: labeling-convention bridge under
  retained meta**, identical in nature to standard particle-physics
  conventions per PR #728 and PR #729.

The conjunction `AC_λ.struct ∧ AC_λ.label` is logically equivalent to
the original AC_λ atom. With AC_λ.struct certified and AC_λ.label
recognized as a labeling convention (not a derivation step), the AC_λ
atom **does not require separate closure beyond Kawamoto-Smit** —
the substep-4 residual reduces to {AC_φ, AC_φλ}.

This is a **partial** ratchet, not a full positive_theorem promotion.
Substep-4 status remains `bounded_theorem` because:

1. AC_λ.struct inherits the bounded tier of its Kawamoto-Smit upstream.
2. The retained meta companion notes are themselves `meta` source-note
   proposals, audit-pending.
3. AC_φ remains a bounded structural no-go candidate within A_min.
4. AC_φλ (= BAE) remains terminally bounded per PR #836.

## Setup

### Premises (P_min for AC_λ separate closure)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| A2 | Z³ spatial substrate | framework axiom; [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| KS | Kawamoto-Smit phase form on Z³ APBC | upstream `bounded_theorem`: [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md) |
| BlockT3 | hw=1 BZ-corner triplet has M_3(C) algebra with distinct joint translation characters | upstream: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md), [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| C3pres | C_3[111] is the framework's preserved load-bearing symmetry; mass-ordering labels are conventions | retained meta source-note: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md) |
| ConvU | Labeling and unit conventions are the same kind of bookkeeping; never derivation input | retained meta source-note: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md) |
| BAErename | "A1-condition" = BAE = amplitude-equipartition `|b|²/a² = 1/2`; species-label content is separated from BAE | retained meta source-note: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md) |

### Forbidden imports

- NO PDG observed values (no `m_e`, `m_μ`, `m_τ` numerical inputs)
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms (zero new axiomatic content beyond A1+A2)
- NO HK + DHR appeal (Block 01 audit retired this)
- NO BAE-condition closure claim (AC_φλ remains terminally bounded
  per PR #836)
- NO physical-observable distinguishability claim on H_{hw=1} (AC_φ
  remains bounded structural no-go candidate)

## Decomposition of AC_λ

The original AC_λ atom (per substep-4 narrowing) reads:

> The triplet `{|c_α⟩}` carries a label-type that is the same kind as
> SM flavor — i.e., these three states transform under upstream
> dynamical evolution as three independent fermion species (free
> propagator block-diagonal in corner basis; no inter-corner mixing in
> the free measure).

This atom decomposes into two logically independent sub-claims:

### Sub-claim AC_λ.struct (block-diagonality)

> The free fermion 2-point function on `H_{hw=1}` factors as
> `⟨χ̄_{c_α}(x) χ_{c_β}(y)⟩_Ω = δ_{αβ} · S_α(x − y)` with NO
> off-diagonal corner mixing in the free measure.

This is a **mathematical structural claim** about the propagator on
Z³ APBC under Kawamoto-Smit phases.

### Sub-claim AC_λ.label (species-kind label)

> The label that distinguishes the three corner states under
> AC_λ.struct is **the same kind of label** as fermion species labels
> in particle physics — i.e., a label that distinguishes three
> independent fermion carriers, not a coincidence.

This is a **kind-of-label characterization**: not "which corner is
the electron" (that's labeling-convention; not even the question here)
but "what kind of label is the corner-distinguishing label" — species,
multiplicity, hidden-sector, internal-symmetry.

### Logical equivalence

The conjunction `AC_λ.struct ∧ AC_λ.label` is logically equivalent to
the original AC_λ atom. The two sub-claims are independent: AC_λ.struct
holds as a propagator structural fact whether or not AC_λ.label is
species-kind; AC_λ.label is a kind-of-label question whether or not the
propagator is block-diagonal.

## Derivation

### Step 1: AC_λ.struct certified by interval-certified Kawamoto-Smit

By the rigorization addendum (2026-05-09) recorded in the substep-4
narrowing note, AC_λ block-diagonality is **runner-certified bounded
candidate** via:

1. At every hw=1 BZ corner, `K(k) = Σ_μ i · η_μ · sin(k_μ) · γ_μ`
   vanishes because every `k_μ ∈ {0, π}` gives `sin(k_μ) = 0`. Verified
   in `mpmath.iv` interval arithmetic at 50-digit precision.

2. The Kawamoto-Smit kinetic operator `K` commutes with all three
   lattice translations `(T_x, T_y, T_z)` by translation-invariance of
   the staggered kinetic action.

3. The three hw=1 corners are simultaneous eigenvectors of
   `(T_x, T_y, T_z)` with **pairwise distinct** joint eigenvalue
   triples `((-1, 1, 1), (1, -1, 1), (1, 1, -1))`. By the
   simultaneous-diagonalization theorem for commuting operators with
   non-degenerate joint eigenspaces (Reed-Simon I §VIII.5), `K` is
   diagonal in the corner basis. Hence `⟨c_α | K | c_β⟩ = 0` for
   `α ≠ β`.

The argument is rigorous within A_min. The only standard-math machinery
is Reed-Simon's simultaneous-diagonalization theorem. The upstream
authority is the Kawamoto-Smit forcing theorem, which is currently
`bounded_theorem` on main.

**Conclusion of Step 1.** AC_λ.struct closes as a runner-certified
bounded candidate. Tier matches Kawamoto-Smit upstream.

### Step 2: AC_λ.label is a labeling-convention question, not derivation

The kind-of-label question — "is the corner-distinguishing label
species-kind, multiplicity-only, hidden-sector, or internal-symmetry-
unrelated?" — is answered structurally by the upstream content:

(a) **Species-kind requires distinct fermion carriers**: under
    AC_λ.struct, the three corners ARE three independent free-propagator
    blocks on `H_{hw=1}`. Each corner carries an independent fermion
    field operator on the Streater-Wightman §2.4 free-propagator
    decomposition.

(b) **Multiplicity-only ruled out**: under M_3(C) factor structure on
    hw=1 (per BlockT3 + no-proper-quotient), the three corners are NOT
    a degenerate multiplicity sector — they are the irreducible
    components of the M_3(C) factor decomposition.

(c) **Hidden-sector / internal-symmetry-unrelated ruled out within
    A_min**: any internal symmetry on the three corners must be
    consistent with the C_3[111] preserved cyclic action (per C3pres).
    No A_min-internal symmetry distinguishes the corners as anything
    other than three independent fermion-field carriers.

(d) **Convention-unification (per ConvU)**: the residual question
    "is this 'species' or 'something else with the same algebraic
    structure'?" is itself a labeling-convention question — asking
    whether to *call* a `M_3(C)`-irreducible 3-orbit of preserved-C_3-
    permuted free-propagator blocks "species" or "non-species". Per
    PR #729, this is bookkeeping at the same layer as
    `{u, c, t}`, `{ν_1, ν_2, ν_3}`. It does not consume retained
    content and it does not load PDG into a derivation step.

**Conclusion of Step 2.** AC_λ.label is structurally a labeling-
convention question once AC_λ.struct holds. The convention-unification
companion note (PR #729) places this in the same audit row as
particle-naming conventions throughout particle physics.

### Step 3: AC_λ closes as a bounded conjunction

By Steps 1-2:

- AC_λ.struct: runner-certified bounded candidate (inherits
  Kawamoto-Smit tier).
- AC_λ.label: labeling-convention bridge under C3pres + ConvU.

The conjunction AC_λ = AC_λ.struct ∧ AC_λ.label closes as a
**sharpened bounded** sub-result of substep-4: it is closed
structurally under retained meta + Kawamoto-Smit upstream, with no
admitted observation of its own beyond the inherited Kawamoto-Smit
admissions.

### Step 4: Independence from AC_φλ (= BAE)

AC_λ closure does NOT touch AC_φλ:

- AC_φλ is the amplitude-equipartition condition `|b|²/a² = 1/2` on
  the C_3-equivariant Hermitian circulant `H = aI + bC + b̄C²`. This
  is a **numerical constraint on the parameters `(a, b)`** of the
  C_3-invariant operator, not a label-kind or block-diagonality claim.
- Per the BAE rename note (PR #790), the BAE-condition is fully
  separated from any species-label / kind-of-label content. The
  30-probe campaign (PR #836) settled BAE as terminally bounded, with
  partial-falsification candidate (κ=1 vs empirical κ=2 on the tested
  retained-content packet).

AC_λ separate closure therefore changes **only** the AC_λ slot in the
substep-4 atomic decomposition. AC_φλ remains terminally bounded per
the 30-probe campaign synthesis. AC_φ remains a bounded structural
no-go candidate within A_min.

### Step 5: Independence from AC_φ

AC_λ closure does NOT touch AC_φ:

- AC_φ asks whether a physical observable distinguishes the three
  corner states by expectation value. The C_3[111] equal-expectation
  lemma rules this out for C_3-symmetric observables.
- AC_λ.struct says the **propagator is block-diagonal** in the corner
  basis. This is consistent with equal expectations for any single
  C_3-symmetric self-adjoint operator (the propagator block-
  diagonality is about off-diagonal vanishing; the equal expectation
  is about diagonal equality).
- The two atoms address different aspects of the corner triplet.
  AC_λ.struct addresses propagator factorization; AC_φ addresses
  diagonal expectation distinguishability. Both can hold
  simultaneously without contradiction.

## Theorem (AC_λ separate closure, sharpened bounded)

**Sharpened bounded theorem (substep-4 AC_λ separate closure).** On
A1+A2 + the stated upstream authorities + retained meta companion
notes (C3pres, ConvU, BAErename) + admissible standard math machinery:

```
The AC_λ atom of the substep-4 atomic decomposition decomposes as

  AC_λ = AC_λ.struct ∧ AC_λ.label

where:

  AC_λ.struct ≡ "free fermion propagator block-diagonal on hw=1
                 corner basis (no off-diagonal corner mixing in the
                 free measure)"
              ≡ runner-certified bounded candidate via
                interval-certified Kawamoto-Smit + Reed-Simon
                simultaneous-diagonalization

  AC_λ.label ≡ "the corner-distinguishing label is species-kind"
             ≡ labeling-convention bridge under retained meta
               (C3pres, ConvU)

The conjunction AC_λ closes as a sharpened bounded sub-result with
NO admitted observation of its own beyond inherited Kawamoto-Smit
upstream. The substep-4 surface status remains bounded_theorem,
sharpened to bounded by {AC_φ, AC_φλ} after AC_λ separate closure
(one fewer independent atom).
```

**Proof.** Steps 1-5 above. AC_λ.struct certified by interval-
certified Kawamoto-Smit (cached in `cl3_staggered_dirac_substep4_ac_phi_lambda_rigorize_2026_05_09.txt`). AC_λ.label characterized as
labeling-convention bridge per C3pres + ConvU + BAErename. Independence
from AC_φ and AC_φλ verified. ∎

## Partial substep-4 ratchet implications

The substep-4 note declared:

```
substep-4 status: bounded_theorem with admitted context AC_narrow
                  = AC_φ ∧ AC_λ ∧ AC_φλ
```

After AC_λ separate closure (this note):

```
substep-4 status: bounded_theorem with admitted context AC_narrow'
                  = AC_φ ∧ AC_φλ                           (one fewer atom)
                  ∧ Kawamoto-Smit bounded upstream         (inherited)
                  ∧ {C3pres, ConvU, BAErename} retained meta
                    (companion-note conditional)
```

The **partial ratchet** is precisely the AC_λ slot: from a separately-
admitted AC atom to an inherited bounded upstream + retained-meta
conditional. The substep-4 surface status does NOT promote (still
bounded). The reduction is in the **shape and count** of admitted-
context atoms, not in the surface tier.

This matches the audit-decision rule from the original substep-4
narrowing note: per-atom rigorization sharpens fates without promoting
status.

## Downstream effects

### P3 / Planck Orientation Principle (PR #874)

The Planck orientation principle bounded note (PR #874) states it
becomes positive_theorem **when** substep-4 ratchets from
bounded_theorem to positive_theorem. Specifically:

> "The full positive_theorem identification that ties the lattice
> action's η_t rule directly to the abstract exterior 1-form e^t
> requires the substep 4 staggered-Dirac realization gate to ratchet
> from bounded_theorem to positive_theorem ... Until that gate
> closes, this orientation principle is bounded_theorem."

Under AC_λ separate closure (this note), substep-4 is **still
bounded_theorem**. So P3's conditional does NOT weaken at the
surface-tier level.

However, P3's underlying admission **becomes more precisely
characterized**: the substep-4 admission carrying P3 is now bounded by
{AC_φ, AC_φλ, Kawamoto-Smit} rather than {AC_φ, AC_λ, AC_φλ} —
i.e., the admission inheritance is sharpened. P3 remains
bounded_theorem, but its conditional is more clearly tied to the two
remaining open atoms (AC_φ structural no-go candidate; AC_φλ = BAE
terminally bounded).

### L3a trace-surface (substep-4 conditional bounded)

The L3a trace-surface bounded obstruction note carries
substep-4-conditional partials. Under AC_λ separate closure, the L3a
substep-4 admission inheritance is sharpened the same way: from
"bounded by AC_φ ∧ AC_λ ∧ AC_φλ" to "bounded by AC_φ ∧ AC_φλ +
inherited Kawamoto-Smit". L3a's surface status does not change.

### Staggered-Dirac realization gate (PR #631-#635)

The parent open-gate `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03`
remains open at positive_theorem tier. Substep-4 still bounded; gate
still open. The gate's admission count is reduced by one atom via this
ratchet, but tier classification is unchanged.

## Comparison to prior work

| Prior closure attempt | Status | Comment |
|---|---|---|
| Block 04 (single-clause AC) | bounded with single-clause AC | Pre-narrowing |
| Substep-4 narrowing (PR #635) | bounded with 3-atom AC | Atomic decomposition |
| Rigorization 2026-05-09 | runner-certified bounded candidates | Per-atom interval-certified |
| 30-probe BAE campaign (PR #836) | AC_φλ terminally bounded | BAE attacked from 30 angles |
| **This note (AC_λ separate closure)** | **AC_λ atom subsumed by Kawamoto-Smit + retained meta** | **Substep-4 admission count reduced from 3 atoms to 2 atoms; tier unchanged** |

## What this narrowing closes

- **AC_λ atom separated** into AC_λ.struct (block-diagonality) and
  AC_λ.label (kind-of-label) sub-claims.
- **AC_λ.struct certified** as runner-certified bounded candidate via
  Kawamoto-Smit (already cached on main).
- **AC_λ.label characterized** as labeling-convention bridge under
  retained meta companion notes (PR #728, PR #729, PR #790).
- **AC_λ atom removed from substep-4 residual atomic stack** (now
  inherited bounded via Kawamoto-Smit upstream + retained-meta
  conditional rather than a separate AC atom).
- **Substep-4 admission count reduced** from `AC_φ ∧ AC_λ ∧ AC_φλ` to
  `AC_φ ∧ AC_φλ + Kawamoto-Smit upstream + retained-meta conditional`.
- **Independence verified** from AC_φ (different aspect: diagonal
  expectations vs off-diagonal vanishing) and from AC_φλ (different
  content: kind-of-label vs amplitude-equipartition).

## What this narrowing does NOT close

- The substep-4 surface status remains `bounded_theorem`.
- AC_φ remains a bounded structural no-go candidate within A_min.
- AC_φλ (= BAE) remains terminally bounded per the 30-probe campaign.
- Kawamoto-Smit upstream remains `bounded_theorem` (its own audit
  status unchanged).
- The retained meta companion notes (PR #728, PR #729, PR #790) remain
  `meta` source-note proposals, audit-pending themselves.
- No claim about specific SM mass values, CKM/PMNS angles, or any
  PDG observable.
- The parent staggered-Dirac realization gate remains open at
  positive_theorem tier.
- L3a trace-surface bounded obstruction status unchanged.
- P3 Planck Orientation Principle bounded status unchanged.

## Status

```yaml
actual_current_surface_status: bounded_theorem (sharpened; partial AC_λ separate closure)
proposed_claim_type: bounded_theorem
audit_review_points: |
  Conditional on:
   (a) independent audit confirmation that the AC_λ atomic
       decomposition (AC_λ.struct ∧ AC_λ.label) is logically
       equivalent to the original AC_λ atom;
   (b) independent audit confirmation that AC_λ.struct closes via
       interval-certified Kawamoto-Smit (already cached);
   (c) independent audit confirmation that AC_λ.label is correctly
       characterized as a labeling-convention bridge under the
       retained meta companion notes;
   (d) independent audit confirmation that AC_λ separate closure does
       not silently load BAE content (verified by Step 4 independence)
       or AC_φ content (verified by Step 5 independence);
   (e) independent audit confirmation that the partial-ratchet
       implication for substep-4 (admission count 3 → 2 atoms; tier
       unchanged) is correctly stated.
hypothetical_axiom_status: null
admitted_observation_status: |
  AC_λ.struct: runner-certified bounded candidate (inherits Kawamoto-
  Smit bounded upstream tier; no separate admission of its own).
  AC_λ.label: labeling-convention bridge under retained meta companion
  notes; consumes zero retained-grade content per ConvU (PR #729).
  Substep-4 admission residual after this narrowing: AC_φ + AC_φλ +
  inherited Kawamoto-Smit upstream + retained-meta conditional.
claim_type_reason: |
  Sharpened bounded sub-result: AC_λ atom of the substep-4 atomic
  decomposition closes structurally under {Kawamoto-Smit bounded
  upstream, C3pres + ConvU + BAErename retained meta}. The closure
  inherits the bounded tier of its load-bearing Kawamoto-Smit
  upstream; it is not promoted to positive_theorem here. The
  substep-4 surface status remains bounded_theorem; the change is in
  admission count (3 atoms → 2 atoms) and admission shape, not in
  surface tier.
independent_audit_required_before_any_effective_status_change: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The substep-4 admitted-context atom AC_λ is decomposed and closed under retained meta + cached Kawamoto-Smit upstream. No new obstruction introduced. |
| V2 | New derivation? | The AC_λ atomic sub-decomposition (struct ∧ label) and the independence verifications (from AC_φ and AC_φλ) are new structural content. The partial-ratchet implication for substep-4 admission count is new. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) sub-decomposition validity; (ii) AC_λ.struct via cached Kawamoto-Smit; (iii) AC_λ.label characterization under retained meta; (iv) independence from AC_φ and AC_φλ; (v) partial-ratchet implication. |
| V4 | Marginal content non-trivial? | Yes — separating AC_λ closure from AC_φλ (= BAE) is a non-trivial atomic refinement that changes the shape and count of substep-4 admissions. |
| V5 | One-step variant? | No — the sub-decomposition (AC_λ.struct ∧ AC_λ.label) and independence verifications are not relabels of the substep-4 narrowing; they sharpen the AC_λ slot specifically using retained meta + cached Kawamoto-Smit. |

**Source-note V1-V5 screen: pass for sharpened-bounded audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of the substep-4 narrowing. The AC_λ atomic
  sub-decomposition (struct ∧ label) is new structural content; the
  independence verifications are new audit-defensibility content.
- Identifies a partial ratchet: one atom of the substep-4
  admitted-context decomposition is removed via inheritance from
  cached upstream + retained meta.
- Sharpens the substep-4 admission count from 3 atoms to 2 atoms
  with explicit upstream inheritance — substep-4 narrowing kept the
  three atoms separate; this note shows AC_λ subsumes into upstream
  Kawamoto-Smit + retained meta.
- Is targeted at **AC_λ specifically**, not the joint AC_φλ atom (=
  BAE). The 30-probe BAE campaign exhausted that atom; this note does
  not retread BAE territory.

## Cross-references

- Parent atomic decomposition: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Kawamoto-Smit upstream: [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md)
- BZ corner forcing upstream: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- C_3-preserved interpretation: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- Conventions unification: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- BAE rename: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
- BAE 30-probe terminal synthesis: [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- Rigorization (cached Kawamoto-Smit certificate): [`scripts/cl3_staggered_dirac_substep4_ac_phi_lambda_rigorize_2026_05_09.py`](../scripts/cl3_staggered_dirac_substep4_ac_phi_lambda_rigorize_2026_05_09.py)
- Physical-lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- P3 Planck Orientation Principle (downstream consumer): [`PLANCK_ORIENTATION_PRINCIPLE_BOUNDED_NOTE_2026-05-10_planckP3.md`](PLANCK_ORIENTATION_PRINCIPLE_BOUNDED_NOTE_2026-05-10_planckP3.md)
- L3a trace-surface (downstream consumer): `L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md`
- MINIMAL_AXIOMS: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## Command

```bash
python3 scripts/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.py
```

Expected output: structural verification of the AC_λ sub-decomposition,
re-certification of AC_λ.struct via Kawamoto-Smit interval-certified
block-diagonality, AC_λ.label characterization under retained meta
companion notes, independence verification from AC_φ and AC_φλ, and
partial-ratchet implication for substep-4 admission count.

Cached: [`logs/runner-cache/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.txt`](../logs/runner-cache/cl3_substep4_ac_lambda_separate_closure_2026_05_10_aclambda.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: AC_λ.label is
  honest about being a labeling-convention bridge under retained
  meta, not a derivation step. AC_λ.struct is closed via
  Kawamoto-Smit derivation, not consistency-equality.
- `feedback_hostile_review_semantics.md`: this narrowing stress-tests
  the action-level semantics of the AC_λ atom — what is the
  *kind-of-label* claim vs the *block-diagonality* claim — not just
  algebra.
- `feedback_retained_tier_purity_and_package_wiring.md`: AC_λ.struct
  inherits the bounded tier of its Kawamoto-Smit upstream (cached on
  main as `bounded_theorem`). AC_λ.label is conditional on the
  retained meta companion notes' audit verdicts (currently `meta`
  source-note proposals). No automatic cross-tier promotion.
- `feedback_physics_loop_corollary_churn.md`: the AC_λ atomic
  sub-decomposition + independence verifications + partial-ratchet
  implication are substantive new structural content, not relabelling
  of the substep-4 narrowing or the BAE 30-probe campaign.
- `feedback_compute_speed_not_human_timelines.md`: closure paths and
  audit-pending tier dependencies are characterized in terms of WHAT
  upstream content would need to be retained, not how-long-it-takes.
- `feedback_review_loop_source_only_policy.md`: this delivery is the
  source-only triplet (source theorem note + paired runner + cached
  output); no output-packets, lane promotions, or working "Block"
  notes.
- `feedback_special_forces_seven_agent_pattern.md`: AC_λ specifically
  was identified as the un-attacked atom (AC_φλ exhausted by
  30-probe; AC_φ rigorized to bounded structural no-go); this single
  probe is the sharp narrow attack on the un-attacked atom.
