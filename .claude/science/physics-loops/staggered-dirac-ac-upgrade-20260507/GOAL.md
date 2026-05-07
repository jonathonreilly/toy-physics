# Staggered-Dirac AC Upgrade Research (12h Campaign Goal)

**Slug:** staggered-dirac-ac-upgrade-20260507
**Started:** 2026-05-07
**Runtime budget:** 12h unattended
**Mode:** campaign
**Worktree:** `/Users/jonreilly/Projects/Physics/.claude/worktrees/lucid-shamir-41757b`

## High-level goal

Close the substep-4 admitted-context AC (Hilbert/no-proper-quotient
semantics) of the staggered-Dirac realization synthesis, promoting
the synthesis from bounded_theorem to retained positive_theorem.

The prior campaign (staggered-dirac-realization-gate-20260507) closed
substeps 1-3 as positive theorems; substep 4 (Block 05, PR #635)
relied on:
- HK (Haag-Kastler axiomatic local QFT)
- DHR superselection theory
- AC: Hilbert/no-proper-quotient semantics admitted-context

## Strategic insight from grounding read (preflight)

**Block 05's DHR framing may have been over-complicated.**

Reeh-Schlieder theorem (retained per `AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01`)
states that A(O)|Ω⟩ is dense in H_phys for any open region O —
implying H_phys has a UNIQUE vacuum, NO DHR superselection sectors
on the canonical surface (cluster decomposition explicitly says
"no superselection sectors on the canonical surface").

The three matter generations cannot be "DHR sectors" — they must be
**three quantum-mechanically distinct STATES** within one H_phys,
separated by the retained translation characters
(diag(−1,+1,+1), diag(+1,−1,+1), diag(+1,+1,−1)) and connected by
C_3[111] cyclic generator within the M_3(C) algebra.

This is structurally simpler and may close substep 4 WITHOUT
admitted-context AC.

## Block plan

### Block 01: DHR-axioms-vs-retained-primitives map (~60-90m)
- Audit DHR's three classical assumptions:
  1. Local algebra net structure A(O)
  2. Translation covariance
  3. Existence of distinct superselection sectors via charged
     intertwiners
- Compare against retained primitives (RP A11, Lieb-Robinson, Lattice
  Noether, Reeh-Schlieder, cluster decomposition)
- **Key finding to verify:** Reeh-Schlieder + cluster → unique
  vacuum on H_phys → NO DHR sectors retained on canonical surface
- **Implication:** Block 05's DHR appeal is misframed. The three
  matter generations are three states within one H_phys, not three
  separate sectors. AC is unnecessary if the bridge is reformulated.

### Block 02: Direct three-state derivation (Route B from prior HANDOFF)
**Target: substep-4 closure WITHOUT admitted-context AC**

- Retained: RP A11 OS reconstruction → H_phys (single Hilbert space)
- Retained: hw=1 has M_3(C) algebra (translations + C_3[111])
- Retained: Distinct translation characters separate three corners
- Retained: No proper exact quotient of M_3(C)
- **Conclusion (target):** the three corners are three orthogonal
  eigenstates of T_x, T_y, T_z with distinct joint characters — they
  are three quantum-mechanically distinct STATES in H_phys, identified
  as three matter generations.
- This is observable separation + spectral distinctness, NOT DHR
  superselection. NO HK+DHR appeal. NO AC.

### Block 03: Reformulated substep-4 theorem
Write a revised substep-4 theorem replacing Block 05's DHR framing
with the direct three-state derivation. **Status target:**
positive_theorem (no AC dependency).

### Block 04: Hostile review of Block 02/03
Apply user-memory feedback rules:
- Consistency-equality vs derivation: are the three states
  GENUINELY physically distinct, or just three labels on a 3-dim
  Hilbert subspace? What makes them "generations" vs "internal
  symmetry levels"?
- Retained-tier purity: does the derivation use only retained
  primitives + admissible standard math?
- Hostile-review must challenge SEMANTICS not just algebra: the
  "physical species" reading is a SEMANTIC claim — does the
  framework's primitive stack actually pin it as physical species
  vs algebraic flavor states?

### Block 05: Synthesis update
If Blocks 02-04 succeed: package as positive_theorem update to
substep-4. Promote staggered-Dirac synthesis (Block 06 of prior
campaign, PR #637) from bounded_theorem to positive_theorem
retained.

If Blocks 02-04 don't fully close: produce sharp obstruction note
identifying the precise remaining gap as a clean axiom-addition
target (different from AC).

### Block 06+: Cross-validation + memory updates

## Hard constraints (forbidden imports)

- NO PDG observed values
- NO lattice MC empirical measurements as derivation inputs
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms (no-new-axiom rule)

## Cross-references

- Prior campaign (staggered-Dirac gate): PRs #631-#635, #637
- Prior synthesis: `docs/STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md`
- Prior substep 4: `docs/STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md`
- Reeh-Schlieder: `docs/AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`
- Cluster decomposition: `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
- RP A11: `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
- Lieb-Robinson: `docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`
- Lattice Noether: `docs/AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`
- Three-generation observable: `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- No-proper-quotient: `docs/THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`
- Generation axiom boundary (admitted-context source): `docs/GENERATION_AXIOM_BOUNDARY_NOTE.md`
