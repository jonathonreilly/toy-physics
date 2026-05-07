# Staggered-Dirac AC Upgrade Loop — Final Handoff

**Date:** 2026-05-07
**Loop slug:** staggered-dirac-ac-upgrade-20260507
**Mode:** campaign (12h budget)
**Runtime used:** ~5 hours
**Stop reason:** clean stopping state — all four planned blocks complete, hostile review identified honest tier outcome (AC sharpening, not full retirement), no productive remaining angle without venturing into research targets

## Summary

Four blocks complete on the staggered-Dirac realization synthesis AC
upgrade. Four PRs OPEN (#641, #642, #644, #645). Campaign delivered
**AC SHARPENING** from broad DHR-based dependency to narrow species-
identification single-clause bridge — an incremental but substantive
improvement.

## Block-level deliverables

| Block | Note | Verdict | PR |
|---|---|---|---|
| 01 | `STAGGERED_DIRAC_AC_DHR_FRAMING_AUDIT_NOTE_2026-05-07.md` | DHR framing audit; Block 05 of prior campaign was misframed | [#641](https://github.com/jonathonreilly/cl3-lattice-framework/pull/641) OPEN |
| 02 | `STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md` | Direct three-state theorem (algebraic content positive; species claim overclaimed per Block 03) | [#642](https://github.com/jonathonreilly/cl3-lattice-framework/pull/642) OPEN, stacked on #641 |
| 03 | `STAGGERED_DIRAC_AC_HOSTILE_REVIEW_RECORD_NOTE_2026-05-07.md` | Hostile-review record; FAIL at positive_theorem tier; recommend bounded with new narrow AC | [#644](https://github.com/jonathonreilly/cl3-lattice-framework/pull/644) OPEN, stacked on #642 |
| 04 | `STAGGERED_DIRAC_REALIZATION_SYNTHESIS_UPGRADE_NOTE_2026-05-07.md` | Synthesis AC sharpening (bounded → bounded with narrow AC) | [#645](https://github.com/jonathonreilly/cl3-lattice-framework/pull/645) OPEN, stacked on #644 |

## Net delivery: AC SHARPENING (not retirement)

| Aspect | Prior synthesis (Block 06, PR #637) | Updated (post-this campaign) |
|---|---|---|
| Synthesis tier | bounded_theorem | bounded_theorem (UNCHANGED) |
| AC scope | Broad — DHR semantics + HK machinery | Narrow — single-clause species-identification bridge |
| HK + DHR dependency | Load-bearing standard machinery | RETIRED |
| RS + cluster decomposition | (not load-bearing) | NEW LOAD-BEARING |
| Substep 4 closure path | DHR superselection (admitted standard QFT) | Direct three-state in single H_phys (algebraic positive) + species AC (narrow) |
| Tractability of AC closure | Difficult — broad DHR machinery dependency | Cleaner — single-clause bridge with three named research paths |

## Research insight delivered

The DHR framing in Block 05 of the prior campaign was structurally
incompatible with the framework's retained Reeh-Schlieder + cluster
decomposition theorems (which together imply unique vacuum, no DHR
superselection sectors on canonical surface). Block 01 of this
campaign identified this. Block 02 reformulated substep 4 as direct
three-state in single H_phys.

**However, hostile review (Block 03) found two real gaps in Block 02:**

1. **Challenge 2 (precision):** "C_3[111] ∈ A(Λ)" hand-waved.
   C_3[111] is a global lattice automorphism, not a finite-support
   polynomial. Constructive fix: replace with "implemented by a
   unitary on H_phys via GNS image of the lattice automorphism."
2. **Challenges 1, 6, 7 (interpretive):** "Three momentum eigenstates =
   three SM species" is a SEMANTIC identification not derivable from
   retained primitives. Step 6 SM-phenomenology cross-validation is
   consistency-equality, not derivation. Needs a new narrow AC.

Block 04 honestly classifies the result as AC SHARPENING (not
retirement).

## Three candidate paths for full AC_narrow closure (research targets)

Future campaigns could attempt:
1. **Mass operator forcing** — derive a mass operator with distinct
   eigenvalues on three corners from retained primitives
2. **Direct species-identification primitive** — extend Lattice
   Noether + RP A11 + spin-statistics to bridge algebraic-distinctness
   to physical-species labeling
3. **Yukawa coupling mechanism** — derive C_3[111]-symmetry-breaking
   Yukawa coupling structure giving three mass eigenstates

None currently available; all are research targets.

## Imports retired / exposed

### Retired
- HK + DHR (no longer load-bearing for substep 4 closure under
  reformulation)

### Newly load-bearing
- Reeh-Schlieder cyclicity (substep 4)
- Cluster decomposition (substep 4)

### Identified as new narrow AC
- "Physical-species reading of joint-translation-character-distinct
  hw=1 corners as SM matter generations"

## Recommended next campaign(s)

### Next-1: Open Block 06 (synthesis Block 06 of prior campaign) update note
The synthesis note `STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md`
(PR #637) should be updated in-place to reflect the AC sharpening from
Block 04 of this campaign. This is a follow-up commit on PR #637 or
a new PR.

### Next-2: AC_narrow closure research
Pursue one of the three candidate paths (mass operator, species-
identification primitive, Yukawa coupling). Each is a multi-cycle
research target.

### Next-3: g_bare = 1 normalization gate (formerly axiom A4)
The other open gate from MINIMAL_AXIOMS_2026-05-03. Now has cleaner
upstream foundations (staggered-Dirac realization substantially
closed, synthesis AC sharpened).

### Next-4: SM-fermion taste-vertex assignment for hypercharge
Identify which gl(1) commutant U(1) factor on the taste cube
corresponds to U(1)_Y. Bridge-gap-new-physics-20260506 Block 05
question; now potentially attackable from cleaner staggered-Dirac
foundation.

## Stop reason

**Clean stopping state.** All four planned blocks complete; hostile
review identified the honest tier outcome (AC sharpening, not full
retirement); the three paths for closing AC_narrow are research
targets requiring substantive new structural work. Pushing further
in this campaign without making one of those research bets would risk
corollary churn.

The campaign respected user-memory feedback rules:
- Hostile-review challenged SEMANTICS (Block 03 found real gaps)
- Consistency-equality vs derivation enforced (SM-phenomenology
  cross-validation correctly flagged)
- No-new-axiom rule
- Retained-tier purity

## Files touched (this campaign)

### Documents
- `docs/STAGGERED_DIRAC_AC_DHR_FRAMING_AUDIT_NOTE_2026-05-07.md` (Block 01)
- `docs/STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md` (Block 02)
- `docs/STAGGERED_DIRAC_AC_HOSTILE_REVIEW_RECORD_NOTE_2026-05-07.md` (Block 03)
- `docs/STAGGERED_DIRAC_REALIZATION_SYNTHESIS_UPGRADE_NOTE_2026-05-07.md` (Block 04)

### Scripts
- `scripts/probe_three_states_direct_derivation.py` (Block 02 PASS=15/0)

### Loop pack
- `.claude/science/physics-loops/staggered-dirac-ac-upgrade-20260507/`
  - GOAL.md, ASSUMPTIONS_AND_IMPORTS.md, STATE.yaml, HANDOFF.md (this file)

### Branches and PRs
- `physics-loop/staggered-dirac-ac-upgrade-block01-20260507` → PR [#641](https://github.com/jonathonreilly/cl3-lattice-framework/pull/641) OPEN
- `physics-loop/staggered-dirac-ac-upgrade-block02-20260507` → PR [#642](https://github.com/jonathonreilly/cl3-lattice-framework/pull/642) OPEN, stacked on #641
- `physics-loop/staggered-dirac-ac-upgrade-block03-20260507` → PR [#644](https://github.com/jonathonreilly/cl3-lattice-framework/pull/644) OPEN, stacked on #642
- `physics-loop/staggered-dirac-ac-upgrade-block04-20260507` → PR [#645](https://github.com/jonathonreilly/cl3-lattice-framework/pull/645) OPEN, stacked on #644

## Independent audit invitations

PRs #641-#645 await independent audit. The campaign is honest about
its actual delivery (AC sharpening, not retirement). The audit lane
should:

1. **Ratify Block 01:** correct identification of DHR misframing
2. **Audit Block 02:** narrow to algebraic content (drop "Physical
   Species" from title); fix Challenge 2 wording; mark Step 6 as
   external cross-check
3. **Ratify Block 03:** hostile-review verdict
4. **Update PR #637 (synthesis):** apply Block 04 AC sharpening
   in-place
5. **Reclassify Block 05 of prior campaign (PR #635):** superseded
   by Block 02 reformulation; deprecate or retire upon audit
   ratification
