# Staggered-Dirac AC Upgrade — Hostile-Review Record (Block 03)

**Date:** 2026-05-07
**Type:** hostile-review record
**Claim type:** review-record / tier correction
**Status:** branch-local hostile-review record on Block 02 of this
campaign (PR #642). External hostile-review agent applied 7 challenges
based on user-memory feedback rules; verdict: **FAIL at
positive_theorem tier**. Block 02 algebraic content is sound but two
real gaps require the substep-4 closure to remain `bounded_theorem`
with a NEW NARROWED AC (much smaller than prior DHR-based AC).
**Authority role:** branch-local hostile-review record. Audit verdict
and effective status are set only by the independent audit lane.
**Loop:** staggered-dirac-ac-upgrade-20260507 (Block 03)
**Branch:** physics-loop/staggered-dirac-ac-upgrade-block03-20260507

## Summary of hostile-review verdict

External hostile-review agent (dispatched 2026-05-07) examined Block 02
(`STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md`,
PR #642) under 7 challenges informed by user-memory feedback rules.
**Verdict: FAIL at positive_theorem tier.** Recommended status:
`bounded_theorem` with a **new narrowed AC** = "physical-species
reading of joint-translation-character-distinct hw=1 corners"
(much smaller than old DHR-based AC).

## The 7 challenges and verdicts

### Challenge 1 — Momentum eigenstates ≠ physical species

**Verdict: PARTIAL HIT, does not break algebraic content.**

The orthogonal-states statement (three corners as joint eigenstates of
T_x, T_y, T_z) is rock-solid via spectral theorem. But the SM concept
of "species" is mass-eigenstate distinguishability, not momentum-
character distinguishability. There is a **semantic gap** between
"three orthogonal eigenstates of (T_x, T_y, T_z) with distinct
characters" and "three physical generations." Block 02 closes the
algebraic statement; the species reading is asserted, not proven.

**Constructive note:** the narrow no-proper-quotient theorem
(`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02`)
explicitly disclaims the physical-species reading. Block 02 quietly
elides this disclaimer. The algebraic three-state content is fine;
the species-label is the over-claim.

### Challenge 2 — Is C_3[111] really in A(Λ)?

**Verdict: SHARP HIT — real precision gap.**

Block 02 Step 3 asserts "C_3[111] is in A(Λ)" without justification.
In Wightman/AQFT framings, lattice translations T_x, T_y, T_z are
implemented as **automorphisms of the algebra** (action of ℤ³ on the
net `O ↦ A(O)` by `α_a: A(O) → A(O+a)`), not necessarily as elements
of any specific local algebra. C_3[111] is a global lattice symmetry
(ℤ_3 cyclic permutation of coordinate axes) and is even less plausibly
an element of any local A(O) — it's a global automorphism, not a
finite-support polynomial in fields.

Block 02's Step 4 hinges on "C_3[111] ∈ A(Λ)" → "states connected by
A(Λ) elements are in same superselection sector." If C_3[111] is NOT
in A(Λ) but is a non-inner automorphism, the clean DHR rebuttal does
not directly apply to operators in the implementing unitary
representation of the symmetry group on H_phys.

**Constructive fix:** replace the claim with the weaker correct
statement that C_3[111] is implemented by a unitary on H_phys that is
the GNS image of a lattice automorphism. The single-sector conclusion
(via RS+CD) still goes through, but the wording must be corrected.

### Challenge 3 — "Three states in single H_phys" vs "three DHR sectors": GENUINELY DIFFERENT

**Verdict: HOLDS — distinct framings, not a relabel.**

Structurally:
- **DHR sectors:** `H = ⊕_α H_α`, local algebra preserves each H_α,
  sectors connected only by charged intertwiners outside A(O).
  Vacuum lives in one sector; other sectors are inequivalent reps of
  the local algebra.
- **Three states in H_phys:** single Hilbert space, single rep of
  the local algebra. C_3[111] (qua unitary) connects three orthogonal
  eigenstates within that single rep.

The reformulation is structurally distinct from DHR, and is the right
target. The question is whether it's correctly proved.

### Challenge 4 — Does RS+CD actually rule out DHR sectors on canonical surface?

**Verdict: HOLDS WITH CAVEAT.**

The RS argument correctly rules out DHR sectors as **subspaces of
H_phys**. It does NOT rule out the existence of **inequivalent
representations** of the local algebra (which is what DHR sectors
actually are technically — distinct reps, not distinct subspaces).
The standard DHR construction begins precisely by acknowledging that
the GNS rep around the vacuum is irreducible / single-sector, and
constructs additional reps via charged morphisms.

For Block 02's purposes (refuting Block 05's misframed claim that
H_phys decomposes into three sectors), the argument holds: all three
states live in the unique GNS sector. No precision break.

### Challenge 5 — Hidden imports?

**Verdict: ONE LIVE CONCERN, but appropriately scoped.**

Spectral theorem on H_phys is invoked load-bearing in Step 5. RS
gives `A(O)|Ω⟩` dense; spectral theorem requires H_phys to be Hilbert
space (true by RP-OS) and translations to be commuting bounded normal
operators (true). Spectral theorem usage is admissible standard math.

GNS reconstruction is via retained RP A11, not a new admission.

No theorem-grade smuggled imports.

### Challenge 6 — SM phenomenology cross-validation

**Verdict: CONSISTENCY-EQUALITY DRESSED AS SUPPORT.**

Block 02 Step 6 says "the framework's direct three-state reading
MATCHES SM phenomenology." This is empirical-fact comparison against
externally-provided SM picture. The framework has NO retained W-boson
or electroweak primitive at theorem grade. So Step 6 is comparing
against an SM fact that the framework does not derive.

Per `feedback_consistency_vs_derivation_below_w2.md`: "consistency
equality is not derivation."

**Constructive fix:** Step 6 should be marked explicitly as
consistency-equality / external-phenomenology cross-check, NOT as a
load-bearing component. The "SM phenomenology match" comparison-table
row should be removed or flagged as non-derivable from retained
primitives.

The formal Steps 1-5 do not depend on Step 6; the theorem itself is
not load-bearing on imported SM phenomenology. But the *promotion*
case (positive vs bounded) leans on Step 6 in places. This is a
documentation defect rather than a theorem break.

### Challenge 7 — Algebraically distinct vs physically distinct

**Verdict: SAME GAP AS CHALLENGE 1.**

The three states are algebraically distinct on H_hw=1 ≅ ℂ³. To upgrade
"algebraically distinct eigenstates of translations" to "physically
distinct species" requires either:
(i) A primitive that says "translation-character-distinct states ARE
    distinct physical species"
(ii) Additional structure (like a mass operator with distinct
     eigenvalues on each corner) that distinguishes the states by a
     physical observable beyond momentum

Neither is provided in Block 02. The narrow no-proper-quotient theorem
explicitly disclaims this; Block 02 quietly elides the disclaimer.

## Synthesis: where the gaps are precisely

| Block 02 claim | Status |
|---|---|
| Three orthogonal eigenstates of (T_x, T_y, T_z) on H_hw=1 | ✓ rock-solid algebraic theorem (positive) |
| Three states all in single H_phys (RS+CD) | ✓ correct (refutes Block 05's misframed DHR) |
| C_3[111] generates 3-cycle on hw=1 | ✓ correct (group theory) |
| C_3[111] **as element of A(Λ)** | ✗ HAND-WAVED (Challenge 2) — should be "implemented by unitary on H_phys" |
| Three states all in same superselection sector | ✓ correct via RS+CD (Challenge 4 caveat noted) |
| **Three states ARE the SM matter generations** | ✗ INTERPRETIVE GAP (Challenges 1, 7) — needs new narrow AC |
| SM phenomenology cross-validation as load-bearing support | ✗ CONSISTENCY-EQUALITY (Challenge 6) — should be flagged |

## Recommended corrections to Block 02

1. **Retitle:** drop "Physical Species" from theorem name. New title:
   *Three-State Single-Sector Direct Theorem* (algebraic content only).

2. **Algebraic content stays positive_theorem** — the three-state
   single-sector content from RP+RS+CD+M_3(C)+no-proper-quotient is
   sound and retained-grade.

3. **Species-identification becomes new narrow AC:**
   `AC_narrow = "physical-species reading of joint-translation-
   character-distinct hw=1 corners as SM matter generations"`
   This is MUCH narrower than the old DHR-based AC. It does not
   appeal to HK or DHR; it admits a single specific interpretive
   bridge from algebraic distinguishability to physical-species
   labeling.

4. **Fix Challenge 2 wording:** replace "C_3[111] ∈ A(Λ)" with
   "C_3[111] is implemented by a unitary on H_phys via GNS image of
   the lattice automorphism."

5. **Mark Step 6 explicitly:** SM-phenomenology cross-validation is
   external-phenomenology cross-check, NOT load-bearing. Remove the
   "SM phenomenology match" row from the comparison table OR flag it
   as non-derivable from retained primitives.

## Net result for synthesis

The synthesis (Block 06 of prior campaign, PR #637) tier:
- **Prior:** `bounded_theorem` with old AC (DHR-based, broad)
- **Updated:** `bounded_theorem` with NEW NARROW AC
  (species-identification reading, much narrower than DHR-based AC)

This is an **AC SHARPENING**, not an AC retirement. The synthesis
remains bounded support theorem, but the admitted-context is now
extremely narrow and well-defined. The narrow AC is a clean axiom-
addition target if/when the framework's primitive stack expands.

## Status

```yaml
actual_current_surface_status: hostile-review record + tier correction
target_claim_type: review-record / tier correction
conditional_surface_status: |
  Conditional on:
   (a) the external hostile-review agent's challenge analysis being
       correct;
   (b) Block 02 (PR #642) being interpretable as making the
       overclaims identified above;
   (c) the user-memory feedback rules being correctly applied.
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  This is a hostile-review record documenting that Block 02's
  positive_theorem claim was over-stated. The algebraic content is
  sound; the species-identification overclaim should be retired to a
  new narrow AC. The synthesis remains bounded with sharpened AC.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The Block 02 overclaim is corrected to bounded with narrow AC; honest tier classification |
| V2 | New derivation? | Hostile-review record. Not a new derivation; documents the correction. |
| V3 | Audit lane could complete? | Pieces of hostile review exist (V1-V5 self-eval was on Block 02); this PR explicitly records the external hostile review. |
| V4 | Marginal content non-trivial? | Yes — corrects an overclaim, sharpens the AC dramatically (DHR-based → species-identification narrow), keeps the audit graph honest. |
| V5 | One-step variant? | No — distinct content type (hostile-review record vs theorem note). |

**PASS V1-V5.** Cluster-cap evaluator (PR #3 in cluster) self-record:
the campaign's primary deliverable is now identified as the SHARPENED
bounded-tier framing rather than full positive_theorem upgrade.
This is the honest result.

## Honest assessment of the campaign

The AC upgrade campaign initially aimed to promote substep 4 from
bounded_theorem → positive_theorem (full retired AC). The hostile
review reveals this was over-ambitious: the algebraic content is
positive-grade, but the species-identification is interpretive and
needs a new (much narrower) AC.

**Net result:**
- Block 01 (DHR framing audit): ✓ correct, identifies real Block 05
  misframing
- Block 02 algebraic content: ✓ positive_theorem grade
- Block 02 species-identification claim: ✗ needs new narrow AC
- Synthesis tier: bounded_theorem with sharpened AC (much narrower
  than prior)

This is an **AC sharpening** rather than an AC retirement. The
synthesis remains bounded but the admitted-context has been reduced
from "DHR semantics on Hilbert/no-proper-quotient surface" (broad,
load-bearing on HK+DHR machinery) to "physical-species reading of
joint-translation-character-distinct hw=1 corners" (narrow, single-
clause interpretive bridge).

The narrow AC is a **clean axiom-addition target** — much more
tractable than the broad AC for future research toward full
positive_theorem retention.

## Cross-references

- Block 01 audit: [`STAGGERED_DIRAC_AC_DHR_FRAMING_AUDIT_NOTE_2026-05-07.md`](STAGGERED_DIRAC_AC_DHR_FRAMING_AUDIT_NOTE_2026-05-07.md) — PR #641 (correct, no changes needed)
- Block 02 reformulation (overclaimed at positive tier): [`STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md) — PR #642 (algebraic content sound; species claim needs narrow AC)
- Sister synthesis (bounded with sharpened AC): [`STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md) — PR #637
- Prior bounded substep 4 (with old DHR-based AC): [`STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md) — PR #635
- Narrow no-proper-quotient (correctly disclaims species-identification): [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)
- User-memory feedback rules: `feedback_consistency_vs_derivation_below_w2.md` and `feedback_hostile_review_semantics.md`
