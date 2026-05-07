# Staggered-Dirac Realization Synthesis — AC Sharpening (Block 04)

**Date:** 2026-05-07
**Type:** synthesis tier-update note
**Claim type:** AC sharpening proposal (NOT full upgrade — see Block 03 hostile review)
**Status:** branch-local proposal to update the staggered-Dirac
realization synthesis (Block 06 of staggered-dirac-realization-gate-
20260507 campaign, PR #637) tier from `bounded_theorem` (with old broad
DHR-based AC) to `bounded_theorem` (with NEW NARROW AC). This is an
**AC SHARPENING**, NOT an AC retirement. Triggered by Blocks 01-03 of
this AC upgrade campaign.
**Authority role:** branch-local source-note proposal for synthesis-
tier AC sharpening. Audit verdict and effective status are set only
by the independent audit lane.
**Loop:** staggered-dirac-ac-upgrade-20260507 (Block 04)
**Branch:** physics-loop/staggered-dirac-ac-upgrade-block04-20260507

## Important context: hostile review changed the conclusion

This Block 04 note was originally drafted (pre-hostile-review) as a
full positive_theorem upgrade proposal. **Block 03 hostile review
(PR #644) changed the tier outcome:**

- **Original draft target:** synthesis bounded → positive_theorem
  retained (full AC retirement)
- **Post-hostile-review:** synthesis bounded → bounded with **NEW
  NARROW AC** (AC sharpening, not retirement)

The hostile review identified two real gaps in Block 02's
positive_theorem claim that prevent full upgrade:
1. C_3[111] ∈ A(Λ) hand-waved (Challenge 2)
2. Species-identification needs new narrow AC (Challenges 1, 6, 7)

The algebraic content of Block 02 holds at positive_theorem grade,
but the species-identification (the load-bearing step for substep 4
closure) requires a new narrow AC. Hence the synthesis cannot fully
upgrade — only the AC sharpens.

## Statement (revised post-hostile-review)

**Synthesis AC sharpening proposal.** The staggered-Dirac realization
synthesis (`STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md`,
prior Block 06 in PR #637) is updated from:

- **Prior tier:** `bounded_theorem` (synthesis), with broad AC =
  "DHR superselection semantics on Hilbert/no-proper-quotient surface"
  (load-bearing on HK + DHR external machinery)
- **Updated tier:** `bounded_theorem` (synthesis), with **NEW NARROW
  AC** = "physical-species reading of joint-translation-character-
  distinct hw=1 corners as SM matter generations"
  (single-clause interpretive bridge, no HK/DHR machinery)

The AC is **sharpened** (narrowed) but not retired. Full retirement
to positive_theorem would require closing the new narrow AC.

## What changed

| Aspect | Prior (Block 06 / PR #637) | Updated (post-this campaign) |
|---|---|---|
| Synthesis tier | bounded_theorem (synthesis) | bounded_theorem (synthesis) — UNCHANGED |
| Substep 4 closure path | DHR superselection | Direct three-state in single H_phys (algebraic content) + species-identification AC |
| AC scope | Broad — DHR semantics + HK machinery | Narrow — single-clause species-identification bridge |
| HK + DHR dependency | Load-bearing standard machinery | Retired (refuted by RS+CD per Block 01) |
| C_3[111] precision wording | (no claim) | Hand-waved in Block 02; needs fix per Block 03 |

## Updated A_min (post-AC-sharpening)

```
A_min(staggered-Dirac realization, post-AC-sharpening) = {
  // RETAINED (unchanged):
  A1, A2,
  Cl(3) per-site uniqueness (chirality-aware),
  Per-site Hilbert dim 2,
  Spin-statistics S2 (re-audit pending),
  Fermion parity Z_2 grading,
  Three-generation observable theorem M_3(C) on hw=1,
  Three-generation no-proper-quotient,
  S_3 taste-cube decomposition,
  Site-phase cube-shift intertwiner,
  Physical-lattice necessity,
  Reflection positivity A11,
  Reeh-Schlieder cyclicity,                    // ← NEW load-bearing for substep 4
  Cluster decomposition,                        // ← NEW load-bearing for substep 4
  Microcausality / Lieb-Robinson,
  Lattice Noether,
  Single-clock evolution,
  No-rooting irreducibility,
  Spectral 1+1+3+3 corner structure,
  Standard math machinery (admissible)

  // RETIRED (no longer load-bearing):
  ✗ HK (Haag-Kastler axiomatic local QFT framework) — was admitted
    standard machinery; per Block 01 audit, RS+CD rule out DHR
    sectors so HK appeal is unnecessary
  ✗ DHR superselection theory — was admitted standard machinery;
    same reason as HK retirement

  // SHARPENED AC (replaces broad DHR-based AC):
  AC_narrow: physical-species reading of joint-translation-character-
             distinct hw=1 corners as SM matter generations
             (single-clause interpretive bridge, NO HK/DHR machinery)
}
```

## Synthesis upgrade roadmap

For full retired-tier promotion of the synthesis to `positive_theorem
retained`, two residuals remain:

### Residual 1: S2 re-audit (audit-lane work)

Spin-statistics theorem S2 (Block 02 of prior campaign dependency) is
currently support tier, awaiting re-audit at retained tier after the
2026-05-03 Cl(3) per-site uniqueness chirality-aware repair. This is
audit-lane work, not science.

### Residual 2: AC_narrow closure (research target)

The narrow AC ("physical-species reading of joint-translation-
character-distinct hw=1 corners as SM matter generations") would
close via either:

(a) **Mass operator forcing:** show that the framework's retained
    primitives FORCE a mass operator on H_phys whose distinct
    eigenvalues correspond exactly to the three corners, providing
    a physically-distinguishing observable beyond translation
    eigenvalues. This would upgrade species-identification from
    interpretive to derived.

(b) **Direct species-identification primitive:** show that the
    framework's retained Lattice Noether + RP A11 + spin-statistics
    structure identifies "translation-character-distinct orthogonal
    eigenstates with M_3(C) algebra" with "physically distinct
    species sectors of the matter field" as a direct theorem.

(c) **Yukawa coupling mechanism:** derive that the C_3[111]-
    transitive structure on hw=1 admits a Yukawa-like coupling that
    breaks the C_3 symmetry into three mass eigenstates. This would
    require additional gauge-Higgs structure not yet retained.

None of (a)-(c) is currently available; all are research targets.
The narrow AC is a clean axiom-addition target if/when the framework's
primitive stack expands.

## Updated audit-graph effect (revised)

Per the prior synthesis: ~488 LHCM-related rows + ~248 three-generation
rows + many fermion-touching descendants are admitted-context-conditional
on the staggered-Dirac realization gate. With the AC sharpening:

- These rows REMAIN admitted-context-conditional (gate not fully
  closed at positive)
- BUT the admitted-context is now MUCH NARROWER (single-clause species
  bridge, not DHR machinery)
- Future research closing AC_narrow would propagate through these
  rows automatically

This is incremental progress on the audit-graph health, not full
retirement.

## What this closes

- The synthesis admitted-context is sharpened from broad (DHR-based)
  to narrow (species-identification single-clause bridge)
- HK + DHR dependencies retired from the synthesis A_min
- Adds Reeh-Schlieder + cluster decomposition as new load-bearing
  retained primitives for substep 4 closure
- Identifies AC_narrow closure paths for future research

## What this does NOT close

- The synthesis tier (still bounded_theorem)
- AC_narrow itself (research target)
- S2 re-audit (audit-lane work)
- Full positive_theorem promotion (requires both Residuals)

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | Synthesis AC is sharpened from broad DHR-based to narrow species-identification |
| V2 | New derivation? | Documents the AC sharpening consequence of Blocks 01-03. Includes paths for closing AC_narrow. |
| V3 | Audit lane could complete? | Audit lane could synthesize the AC sharpening once Blocks 01-03 are reviewed; this Block 04 documents it cleanly. |
| V4 | Marginal content non-trivial? | Yes — synthesis AC narrowed dramatically (broad DHR → single-clause species). |
| V5 | One-step variant? | No — synthesis tier-update meta-note distinct from substep theorems. |

**PASS V1-V5.**

## Honest campaign assessment

This AC upgrade campaign delivered:

1. **Block 01:** identified Block 05's DHR framing as misapplied (real audit finding)
2. **Block 02:** reformulated substep 4 with direct three-state derivation (algebraic content sound, species-identification overclaimed)
3. **Block 03:** hostile-review found two real gaps in Block 02 positive claim
4. **Block 04 (this note):** honest tier classification — synthesis AC sharpening, not retirement

**Net delivery: AC sharpening from broad DHR-based to narrow species-identification.** This is an INCREMENTAL improvement, not the full upgrade originally targeted, but it's a substantive sharpening that makes the residual gap much more tractable for future research.

The campaign respected user-memory feedback rules:
- Hostile-review challenged SEMANTICS not just algebra (Block 03 found real gaps)
- Consistency-equality vs derivation distinction enforced (SM-phenomenology cross-validation flagged as not load-bearing)
- No-new-axiom rule (no extension of axiom stack)
- Retained-tier purity (no support-tier routes load-bearing for retained equalities)

## Cross-references

- Block 01 audit: [`STAGGERED_DIRAC_AC_DHR_FRAMING_AUDIT_NOTE_2026-05-07.md`](STAGGERED_DIRAC_AC_DHR_FRAMING_AUDIT_NOTE_2026-05-07.md) — PR #641
- Block 02 reformulation (algebraic positive, species AC needed): [`STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md) — PR #642
- Block 03 hostile-review record: [`STAGGERED_DIRAC_AC_HOSTILE_REVIEW_RECORD_NOTE_2026-05-07.md`](STAGGERED_DIRAC_AC_HOSTILE_REVIEW_RECORD_NOTE_2026-05-07.md) — PR #644
- Synthesis being updated (still bounded): [`STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md) — PR #637
- Prior bounded substep 4 (DHR-framed, superseded by Block 02): [`STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md) — PR #635
