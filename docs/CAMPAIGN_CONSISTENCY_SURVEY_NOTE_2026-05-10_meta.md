# Campaign Consistency Survey — Cross-PR Review (2026-05-08 to 2026-05-10)

**Date:** 2026-05-10
**Type:** meta
**Claim type:** meta (survey-only; no theorem promotion, no retagging)
**Survey result:** no contradictions or silent admission introductions
detected in this cross-PR consistency survey; conditionalities are
explicitly tracked.
**Authority role:** records the cross-PR consistency state of the
2026-05-08 to 2026-05-10 campaign rounds (BAE 30-probe, foundational
meta clarifications, C-iso engineering, bridge-lane promotion, Lane 2
attack, substrate-to-carrier, G_Newton sharpening + closures, Planck-
from-structure synthesis). This note does not write audit verdicts and
does not promote or retag any source-note proposal.
**Companion to:**
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md),
[`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md),
[`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md),
[`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md),
[`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md),
[`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md),
[`PLANCK_FROM_STRUCTURE_PATH_OPENING_META_NOTE_2026-05-10.md`](PLANCK_FROM_STRUCTURE_PATH_OPENING_META_NOTE_2026-05-10.md).
**Primary runner:** [`scripts/frontier_campaign_consistency_survey_2026_05_10_meta.py`](../scripts/frontier_campaign_consistency_survey_2026_05_10_meta.py)
**Cache:** [`logs/runner-cache/frontier_campaign_consistency_survey_2026_05_10_meta.txt`](../logs/runner-cache/frontier_campaign_consistency_survey_2026_05_10_meta.txt)

## Authority disclaimer

This is a meta cross-PR consistency survey. It records observations
about the relationships among landed and open source-note proposals; it
does not write audit verdicts, promote claims, retag rows, or aggregate
admission counts. The audit lane retains full authority over each
referenced source-note proposal.

## Scope

This note surveys cross-PR consistency for the 2026-05-08 to 2026-05-10
campaign rounds, comprising approximately 50 source-note proposals
across:

- 30-probe BAE campaign (PRs #727-#840) and terminal synthesis (#836)
- Foundational meta clarifications: physical-lattice (#725), C_3-
  preserved (#728), conventions-unification (#729), BAE rename (#790)
- Bridge-lane promotion evaluation (#843)
- Lane 2 lattice-physical matching per-step bounded obstruction (Lane 2
  attack vectors, e.g. #865/#866/#867)
- C-iso engineering: ε_witness numerical convergence (#845), SU(3)
  NNLO/N5LO closed-form rationals (#857)
- Substrate-to-carrier round (PRs #874, #875, #876, #877; planckP1-P4)
- G_Newton sharpening + sub-closure proposals (#875 sharpening, plus
  three companion proposals gnewtonG1/G2/G3 closing admissions B(a),
  B(b), B(c) respectively)
- Planck-from-structure path-opening synthesis (#882)

The survey follows the review-loop source-only pattern. Inventory and
consistency findings are recorded; no audit-lane verdicts.

## Survey Result — No Contradictions Detected

The campaign's retained-grade claims, conditionality chains, and
admission inventory are mutually consistent. No silent new admission
introductions detected. Specifically:

1. **A1+A2 axioms unchanged across all rounds.** Every meta note and
   source-note proposal explicitly preserves
   `MINIMAL_AXIOMS_2026-05-03.md`'s two-axiom surface.
2. **No source-note proposal has been silently promoted to retained.**
   Every probe, sharpening, and synthesis explicitly carries an authority
   disclaimer: pipeline-derived `effective_status` is set only by the
   independent audit lane after review.
3. **Admission count is correctly maintained.** BAE + P remain the two
   bounded admissions outside the substrate-to-carrier path. P4
   (#875) explicitly names three additional G_Newton admissions
   (B(a)/B(b)/B(c)); these are recorded but not aggregated. The G1/G2/G3
   companion proposals advance closure of these named admissions and
   are themselves source-note proposals awaiting audit review.
4. **Conditionality chains are explicit and tracked.** No retained-grade
   claim depends on an open admission of another retained-grade claim.
5. **Probe 25 (F3 vs F1) and Probe 22 (spectrum-cone pivot) operate in
   the BAE / Koide-circulant domain, not the gravity / G_Newton domain.
   No conflict with G2 (Born-as-source) or P1 (substrate-to-carrier).**
   Cross-domain audit independence is preserved.

## Inventory — landed retained-grade claims surveyed

### Foundational axiom surface (unchanged)

The two retained mathematical axioms per
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md):

- **A1** Local algebra `Cl(3)`
- **A2** Spatial substrate `Z³`

Two open derivation gates (also unchanged):

- Staggered-Dirac realization gate (currently `bounded_theorem` per
  `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`,
  with substep-4 ratchet pending)
- `g_bare = 1` derivation gate (parent: `G_BARE_DERIVATION_NOTE.md`,
  audited_conditional)

### Foundational meta clarifications (landed on origin/main)

These four meta notes are all classified `claim_type: meta` and
explicitly do not promote downstream theorems:

| PR | Note | Claim |
|---|---|---|
| #725 | `PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08` | Physical Cl(3)/Z³ baseline is repo semantics, not a new admission |
| #728 | `C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08` | C_3[111] on hw=1 is preserved; mass-ordering labels are conventions |
| #729 | `CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08` | Labeling conventions and unit conventions are the same kind of bookkeeping |
| #790 | `BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09` | Rename "A1-condition" → BAE; resolves naming collision with framework axiom A1 |

### BAE 30-probe campaign terminal state (PR #836)

Per
[`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md):

- 30 probes total; all with `claim_type` recorded per probe (`bounded_theorem`,
  `no_go`, or partial-falsification candidate).
- 2 positive candidate results awaiting audit:
  - Probe 19: `m_τ = M_Pl × (7/8)^(1/4) × u_0 × α_LM^18` (PDG match 0.017%)
  - Probe 24 Step 1: `φ_dimensionless = 2/9` from Z_3-character
- 1 partial-falsification candidate awaiting audit:
  - Probe 29: framework predicts κ=1, empirical κ=2 (factor-2 in κ
    on charged-lepton SPECTRAL-RELATION lane only)
- 3 structural-impossibility claims (Probes 14, 17, 25+27+28)
- 2 admissions remaining: BAE (`|b|²/a² = 1/2` multiplicity-counting),
  P (radian-bridge primitive)

### Substrate-to-carrier round (PRs #874-877; on agent branches awaiting audit)

| PR | Probe | Source note (proposed claim type) |
|---|---|---|
| #874 | P3 | `PLANCK_ORIENTATION_PRINCIPLE_BOUNDED_NOTE_2026-05-10_planckP3` (`bounded_theorem`) — landed on main |
| #875 | P4 | `G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4` (`bounded_theorem`) — agent branch |
| #876 | P2 | `PLANCK_HIDDEN_CHARACTER_DELTA_ZERO` (`positive_theorem`) — agent branch |
| #877 | P1 | `SUBSTRATE_TO_CARRIER_RP_BOUNDED` (`bounded_theorem`) — agent branch |

### G_Newton sharpening + companion sub-closures (on agent branches)

| Branch | Probe | Source note (proposed claim type) |
|---|---|---|
| `claude/skeleton-selection-bounded-2026-05-10-gnewtonG1` | G1 | `G_NEWTON_SKELETON_SELECTION_BOUNDED_NOTE_2026-05-10_gnewtonG1` (`bounded_theorem` closing admission B(a)) |
| `agent/g-newton-born-as-source-2026-05-10-gnewtonG2` | G2 | `G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2` (`positive_theorem` closing admission B(b)) |
| `agent/g-newton-weak-field-response-2026-05-10-gnewtonG3` | G3 | `G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3` (`bounded_theorem` closing admission B(c)) |

### Planck-from-structure path-opening synthesis (on agent branch)

[`PLANCK_FROM_STRUCTURE_PATH_OPENING_META_NOTE_2026-05-10.md`](PLANCK_FROM_STRUCTURE_PATH_OPENING_META_NOTE_2026-05-10.md)
(PR #882, `agent/planck-from-structure-path-opening-2026-05-10`) — meta
synthesis recording the conditional path on which the conventional scale
anchor row reaches zero. **This synthesis was committed at 09:49:07 EDT,
BEFORE G1/G2/G3 (09:50:17 / 09:51:15 / 09:52:10).** The synthesis correctly
states: "Each admission has a separate companion-probe path identified
(referred to in the task framing as Probes G1, G2, G3); those probes'
results may not be on main yet at synthesis time." This is consistent —
the synthesis did not silently incorporate G1/G2/G3 results.

### Bridge-lane promotion + Lane 2 (PR #843, Lane 2 attack #865/#866/#867)

[`BRIDGE_LANES_PROMOTION_PROPOSAL_NOTE_2026-05-10_lanes.md`](BRIDGE_LANES_PROMOTION_PROPOSAL_NOTE_2026-05-10_lanes.md)
evaluates `retained_bounded` promotion potential for three bridge-
dependent lanes (α_s direct Wilson loop, Higgs mass from axiom, gauge-
scalar bridge). Lane 2 attack notes (e.g. `LATTICE_PHYSICAL_MATCHING_*`)
identify the per-step accounting (S1-S7) of the matching theorem and
classify each step retained / retained_bounded / open — verdict:
**STRUCTURAL OBSTRUCTION** at S4 (mean-field readout) and S7 (+12% gap-
closure). Consistent with prior 2026-05-02 cluster obstruction note.

### C-iso engineering (PRs #845, #857; landed on origin/main)

- C-iso ε_witness closure (#845): combined Weyl-truth + lattice estimator,
  2.6×10⁻⁴ at ξ=4.
- SU(3) NNLO/N5LO closed-form rationals (#857): exact rationals replace
  numerical c_3 across orders.
- Survey read: **C-iso truncation eliminated as the dominant systematic** on
  the gauge-side bridge. Engineering frontier remains tightening the
  stat+vol floor.

## Cross-consistency checks performed

### Check 1: A1+A2 axioms preserved across rounds — PASS

Every meta note (PRs #725, #728, #729, #790, #836, #882, #843), every
30-probe BAE source-note, every substrate-to-carrier source-note, every
G_Newton companion source-note, and every Lane 2 source-note explicitly
states "A1+A2 unchanged" or its equivalent. No round adds a third
mathematical axiom.

### Check 2: No silent retained-tier promotion — PASS

Every source-note proposal in the campaign carries an Authority
Disclaimer that pipeline-derived `effective_status` is generated only
after independent audit lane review. Cross-checked the synthesis #882
explicitly states: "Pipeline-derived `effective_status` is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. This note does not promote any source theorem note."

### Check 3: Admission count consistency — PASS

- Per #836 terminal synthesis: 2 admissions (BAE + P) on the BAE / Koide
  track.
- Per #875 (planckP4) and confirmed by #882 synthesis: G_Newton has 3
  named admissions (B(a) skeleton, B(b) Born, B(c) valley-linear),
  recorded but not aggregated into the BAE+P count. The synthesis
  explicitly tracks "2 (BAE, P) + 3 (G_Newton: skeleton, Born, valley-
  linear)" as separate inventories.
- Companion source-notes G1, G2, G3 propose closures of B(a), B(b), B(c)
  respectively. These do not silently reduce the count — they remain
  source-note proposals awaiting audit verdicts. If audit-lane ratifies
  G1+G2+G3, the G_Newton 3-admission row drops; the campaign synthesis
  has not pre-counted that drop.
- Substrate-to-carrier round (P1+P2+P3) and Lane 2 attack notes do NOT
  introduce any new named admissions. Each is a closure proposal on
  retained content.

### Check 4: Probe 25 (F3 structural rejection) vs G2 (Born-as-source) — PASS

Probe 25 operates on `Herm_circ(3)` for the BAE / Koide-circulant
spectrum. F3 vs F1 selection refers to canonical functional choice on
the Brannen-Rivero (a, |b|)-plane. G2 operates in the gravity domain on
the position-density Born map `ρ_grav(x) := ⟨x|ρ̂|x⟩`. **No domain
overlap.** Cross-domain claims do not collide.

### Check 5: Probe 22 (spectrum-cone pivot illusory) vs P1 (RP-induced selection) — PASS

Probe 22 says: spectrum-level cone localization on `Herm_circ(3)` is
arithmetically identical to parameter-level BAE; the pivot does not
escape the parameter-level obstruction. P1 says: among 17 rank-four
equivariant projector classes on the substrate primitive cell, RP
Cauchy-Schwarz selects `P_A` uniquely as the carrier. **Different
sectors (Herm_circ(3) vs primitive cell), different question (BAE
closure vs carrier identification), different retained content used.**
Both can be true simultaneously; they reference distinct reductions.

### Check 6: Probe 19 m_τ Wilson chain uses M_Pl as anchor — bounded as expected

Probe 19 (#799) derives `m_τ = M_Pl × (7/8)^(1/4) × u_0 × α_LM^18`. This
uses M_Pl as anchor; it does not break Probe 19's audit-honest framing
because (a) the campaign synthesis #836 records this as positive
candidate result awaiting audit verdict, NOT retained, and (b) the
Planck-from-structure synthesis #882 explicitly says "the conditional
path to zero conventional anchors" — meaning M_Pl as anchor is
currently a retained "conventional scale anchor" that ONLY becomes
structural under the audit ratification of P1+P2+P3 + substep-4
closure. The conditionality is correctly tracked.

### Check 7: G2 Born-as-source uses physical-lattice baseline — PASS

G2's load-bearing inputs include the retained physical-lattice baseline
(per `PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`).
This is `claim_type: meta` — repo-semantics clarification, not a
theorem promotion. The chain G2 → meta-baseline is allowed: meta-
clarifications are upstream ground-truth on what the baseline IS, not a
load-bearing positive theorem with its own admissions.

### Check 8: G3 valley-linear uses retained Hamiltonian flow — PASS

G3 invokes the retained Hamiltonian flow from RP transfer matrix +
spectrum condition. This chain is consistent with the retained
audit-ledger entries; no new admission introduced. G3 also forces (c)
under retained content, structurally replacing the prior empirical
F~M=1 pinning. The synthesis #882 explicitly listed B(c) as needing
a "structural target" — G3 provides that, in source-note form, awaiting
audit-lane ratification.

### Check 9: synthesis #882 timing vs G1/G2/G3 commit order — PASS

#882 was committed at 09:49:07 EDT, before G1 (09:50:17), G2 (09:51:15),
G3 (09:52:10). The synthesis correctly states the G_Newton three-
admission frontier without claiming closures from G1/G2/G3. After
audit ratification of any/all of G1/G2/G3, the synthesis's
"Conditional on G_Newton's three named admissions closing" subsection
will need re-statement — but the synthesis is internally consistent at
its commit time.

### Check 10: BAE rename does not silently retag claim_type — PASS

PR #790 (BAE rename) explicitly states the rename "does not modify any
retained theorem on main" and "does not reclassify the BAE admission's
`claim_type` or `effective_status`." Audit-ledger row keys remain at
their current `koide_a1_*` (file immutability); new rows use
`koide_bae_*`. No silent retagging.

### Check 11: PR #836 terminal synthesis F3 finding consistency — PASS

#836 reports F3 (κ=1) is the canonical κ-predictor under retained
dynamics, NOT F1 (κ=2 = BAE). This is consistent with:
- Probe 25 (#820): F1 structurally rejected by tested dynamics
- Probe 27 (#824): F3 sector-independent on Brannen ansatz
- Probe 28 (#827): F3 preserved by all C_3-covariant interactions

The F3 claim is internally consistent across all three probes. The
empirical κ=2 vs framework κ=1 disagreement is the precisely-localized
partial-falsification candidate (Probe 29, #825), recorded but not
adjudicated.

## Conditionality chains (explicitly catalogued)

The campaign maintains the following explicit conditionality chains.
Each is correctly stated as "X is positive_theorem PROVIDED Y is
closed":

1. **Substrate-to-carrier closures** (P1, P2, P3) are positive_theorem
   PROVIDED substep-4 staggered-Dirac realization gate closes (currently
   `bounded_theorem`). Per #882: "Until substep 4 ratchets from
   `bounded_theorem` to `positive_theorem`, the substrate-to-carrier
   chain inherits its bounded label."

2. **Conventional scale anchor row → 0** PROVIDED P1+P2+P3 audit-
   ratified AND substep-4 closure. Per #882: "(conditional)" label is
   load-bearing.

3. **G_Newton 3-admission frontier → 0** PROVIDED G1+G2+G3 audit-
   ratified. Currently each G_i is a source-note proposal awaiting
   audit. The synthesis #882 explicitly identifies these as "those
   probes' results may not be on main yet at synthesis time."

4. **Probe 19 m_τ Wilson chain → retained** PROVIDED audit-lane review
   of #799 closes positively AND the M_Pl-as-anchor input itself moves
   from "conventional scale anchor" to "structural" (which depends on
   #2 above).

5. **All quantitative results in the y_t / EW / Higgs lanes → retained
   positive_theorem** PROVIDED both the staggered-Dirac realization
   gate AND the `g_bare = 1` derivation gate close (per
   `MINIMAL_AXIOMS_2026-05-03.md` Section "Lanes that depend on both
   gates").

6. **Lane 2 (Higgs mass from axiom) STRUCTURAL OBSTRUCTION** at S4 +
   S7 stands; per #843 + #865/866/867: same Nature-grade non-
   perturbative residual as 2026-05-02 cluster obstruction.

7. **C-iso engineering → eliminated as dominant systematic** under
   #845 + #857 (NLO closed-form rationals + ε_witness 2.6e-4 at ξ=4).
   Stat+vol floor remains the dominant remaining bottleneck.

## Inconsistencies found — NONE

This survey detects **zero contradictions** among landed retained-grade
claims. Specifically:

- No two claims at retained tier are mutually inconsistent.
- No retained claim depends on an open admission of another retained
  claim.
- No silent admission introduction across the campaign.
- No silent retagging of `claim_type` or `effective_status`.
- No silent promotion of source-note proposals to retained.

## Items the audit lane retains authority on

This consistency survey does NOT adjudicate any of:

1. Whether P1, P2, P3 (substrate-to-carrier proposals) ratify clean.
2. Whether G1, G2, G3 (G_Newton companion proposals) ratify clean.
3. Whether Probe 19 m_τ Wilson chain ratifies as positive candidate.
4. Whether Probe 24 Step 1 φ_dimensionless = 2/9 ratifies as positive
   character-algebra candidate.
5. Whether Probe 29 partial-falsification candidate stands or is
   resolved by additional probes.
6. Whether the synthesis-level "path-opening" framing of #882 is
   admissible.
7. Whether the Lane 2 STRUCTURAL OBSTRUCTION verdict is retained.
8. Whether the bridge-lane promotion targets (PR #843) cross the
   `retained_bounded` line.

The audit lane has authority on each item.

## What this note does NOT do

1. Promote any source-note proposal.
2. Retag any `claim_type` or `effective_status`.
3. Aggregate admission counts into a composite number.
4. Adjudicate Probe 29 partial-falsification.
5. Adjudicate the path-opening synthesis (#882).
6. Modify any retained theorem on main.
7. Add a new mathematical axiom (A1+A2 still suffice).
8. Resolve the strategic options identified by #836 (accept partial
   falsification / build new physics outside C_3 rep theory / pivot
   to other bridge work).

## Cross-references

### Foundational

- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### BAE 30-probe campaign

- [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md) (PR #790)
- [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md) (PR #836)
- [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md) (PR #751)

### Substrate-to-carrier round

- [`PLANCK_ORIENTATION_PRINCIPLE_BOUNDED_NOTE_2026-05-10_planckP3.md`](PLANCK_ORIENTATION_PRINCIPLE_BOUNDED_NOTE_2026-05-10_planckP3.md) (PR #874, P3, on origin/main)
- `G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md` (PR #875, P4, on agent branch)
- `PLANCK_HIDDEN_CHARACTER_DELTA_ZERO_BOUNDED_NOTE_2026-05-10_planckP2.md` (PR #876, P2, on agent branch)
- `SUBSTRATE_TO_CARRIER_RP_BOUNDED_NOTE_2026-05-10_planckP1.md` (PR #877, P1, on agent branch)

### G_Newton companion sub-closures

- `G_NEWTON_SKELETON_SELECTION_BOUNDED_NOTE_2026-05-10_gnewtonG1.md` (G1, agent branch)
- `G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md` (G2, agent branch)
- `G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md` (G3, agent branch)

### Synthesis

- [`PLANCK_FROM_STRUCTURE_PATH_OPENING_META_NOTE_2026-05-10.md`](PLANCK_FROM_STRUCTURE_PATH_OPENING_META_NOTE_2026-05-10.md) (PR #882, on agent branch)

### Bridge-lane / C-iso

- `BRIDGE_LANES_PROMOTION_PROPOSAL_NOTE_2026-05-10_lanes.md` (PR #843)
- `LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md` (Lane 2 prior cluster)

## Validation

```bash
python3 scripts/frontier_campaign_consistency_survey_2026_05_10_meta.py
```

The runner is a review-hygiene check, not a physics proof. It verifies:

1. This survey note is classified as `meta` and does not declare pipeline
   status.
2. The two foundational axioms (A1+A2) are preserved.
3. The four foundational meta clarifications (PRs #725, #728, #729, #790)
   are cross-referenced.
4. The 30-probe BAE campaign terminal state (PR #836) admission inventory
   is referenced (BAE + P).
5. The G_Newton three named admissions (B(a), B(b), B(c)) are recorded
   without aggregation.
6. The synthesis #882 timing relative to G1/G2/G3 is noted.
7. The conditionality chains are enumerated.
8. No new axiom, no theorem promotion, no admission reclassification.
9. The survey result is no contradictions detected.
10. The 11 cross-consistency checks are listed.

## Review-loop rule

Going forward:

1. This survey is a snapshot of the cross-PR state as of 2026-05-10.
   Subsequent audit-lane verdicts on P1/P2/P3, G1/G2/G3, Probe 19,
   Probe 24, and Probe 29 may move individual rows; this survey does
   not pre-empt those verdicts.
2. If any retained-grade claim is later shown to depend on an open
   admission of another retained-grade claim, the chain becomes a
   silent admission introduction and should be flagged for repair. As
   of 2026-05-10, no such silent introduction is detected.
3. Cross-domain audit independence (BAE/Koide vs gravity/G_Newton vs
   substrate-to-carrier vs Lane 2) is preserved by current PR set;
   future PRs that mix these domains should be audited for cross-
   domain consistency before retained promotion.
