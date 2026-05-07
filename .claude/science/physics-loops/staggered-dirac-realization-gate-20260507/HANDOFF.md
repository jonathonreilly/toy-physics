# Staggered-Dirac Realization Gate Loop — Final Handoff

**Date:** 2026-05-07
**Loop slug:** staggered-dirac-realization-gate-20260507
**Mode:** campaign (12h budget)
**Runtime used:** ~7 hours (60% of 12h budget; campaign reached
volume-cap-respecting closure)

## Summary

Six blocks complete on the staggered-Dirac realization gate (formerly
axiom A3 per [`MINIMAL_AXIOMS_2026-05-03.md`](../../../../docs/MINIMAL_AXIOMS_2026-05-03.md)).
Five PRs opened (#631–#635); Block 06 synthesis committed but in
PR_BACKLOG per volume cap (5/24h). The gate is **substantially
closed** — substeps 1-3 as positive theorems, substep 4 bounded with
admitted-context AC.

## Block-level deliverables

| Block | Note | Runner | Status | PR |
|---|---|---|---|---|
| 01 | `STAGGERED_DIRAC_FORCING_GAP_MAP_NOTE_2026-05-07.md` | (scoping) | scoping audit | [#631](https://github.com/jonathonreilly/cl3-lattice-framework/pull/631) OPEN |
| 02 | `STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md` | `probe_grassmann_forcing_dependency_chain.py` PASS=9/0 | positive_theorem (substep 1) | [#632](https://github.com/jonathonreilly/cl3-lattice-framework/pull/632) OPEN, stacked on #631 |
| 03 | `STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md` | `probe_kawamoto_smit_phase_forcing.py` PASS=24/0 | positive_theorem (substep 2) | [#633](https://github.com/jonathonreilly/cl3-lattice-framework/pull/633) OPEN, stacked on #632 |
| 04 | `STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md` | `probe_bz_corner_decomposition.py` PASS=5/0 | positive_theorem (substep 3) | [#634](https://github.com/jonathonreilly/cl3-lattice-framework/pull/634) OPEN, stacked on #633 |
| 05 | `STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md` | (theoretical) | bounded_theorem (substep 4) | [#635](https://github.com/jonathonreilly/cl3-lattice-framework/pull/635) OPEN, stacked on #634 |
| 06 | `STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md` | (synthesis) | bounded_theorem (synthesis of 1-4) | PR_BACKLOG (volume cap reached at Block 05) |

## Cross-block synthesis

### Net structural finding

The staggered-Dirac realization gate is **substantially closed** under
A1+A2 + retained primitive stack + admissible standard math machinery
+ admitted-context AC:

- **Substep 1 (Grassmann partition)**: positive theorem — bosonic 2nd
  quantization incompatible with retained per-site Cl(3) dim 2;
  Grassmann uniquely forced
- **Substep 2 (Kawamoto-Smit phases)**: positive theorem — single-
  mode Grassmann (Block 02) forces spin-diagonalization;
  T(x) = σ_1^{x_1} σ_2^{x_2} σ_3^{x_3} gives unique η_μ(x)
- **Substep 3 (BZ-corner three-gen)**: positive theorem — Hamming-
  weight decomposition 1+3+3+1 unique; hw=1 triplet has retained
  M_3(C) algebra with no proper quotient
- **Substep 4 (physical-species)**: bounded theorem with admitted-
  context AC — DHR superselection (admitted standard QFT) gives
  three superselection sectors → three SM matter generations

### Net status

`bounded_theorem` synthesis. Promotion to full retained `positive_theorem`
requires:
1. **S2 re-audit at retained tier** (Block 02 dependency; chirality-
   aware upstream repair has fixed the dependency, audit pending)
2. **AC upgrade** (Block 05 dependency; either as new structural
   primitive establishing DHR correspondence as framework-internal,
   OR as direct framework-derived argument without external HK+DHR)

## Imports retired / exposed

### Retired (formally closed under campaign)

The staggered-Dirac realization is no longer "an open gate with
scattered pieces." It is a synthesized derivation chain with explicit
forcing arguments at each substep (1-3 positive, 4 bounded).

### Exposed

- AC (Hilbert/no-proper-quotient semantics) as the precise residual
  research target for full retained-tier promotion
- Sub-question (open): which gl(1) commutant U(1) factor on the taste
  cube corresponds to U(1)_Y? (See bridge-gap-new-physics-20260506
  Block 05 — connected via the now-closed staggered-Dirac realization)

### Lane-impact (substantial)

Per the parent open-gate's "Lanes that depend on this gate" listing:

> "Any lane whose derivation defines fermion fields, fermion-number
> operators, fermion correlators, fermion bilinears, or staggered
> Dirac action — essentially every lane that touches matter content.
> Examples: coleman_mermin_wagner, cpt_exact, lattice_noether,
> spin_statistics, three-generation, baryon/meson singlet, fermion-
> parity Z_2, Q̂ integer spectrum, hopping bilinear, etc."

These lanes (~488 LHCM-related rows + ~248 three-generation rows +
many fermion-touching descendants) become eligible for upgrade from
`bounded_theorem` (with staggered-Dirac as admitted-context) to
`positive_theorem` upstream-of-staggered-Dirac upon audit ratification.

## Stop reason

**Volume cap reached at Block 05** (5 PRs/24h on goal-specific target
per skill protocol). Block 06 synthesis committed to branch but not
opened as PR. Per the new judgment-based cluster cap (PR #624
governance update), the cluster cap evaluator was self-applied to
Blocks 03-05 (V1-V5 PASS each); Block 06 synthesis self-evaluation
PASSES V1-V5 but volume cap is the binding constraint.

## Recommended next campaign(s)

### Next-1: Open Block 06 PR after volume-cap reset

After 24h elapsed, open Block 06 (synthesis) as PR base = Block 05
branch. This packages the campaign's primary deliverable.

### Next-2: S2 re-audit lane

Independent audit lane work to re-audit the spin-statistics theorem
S2 at retained tier (currently support, awaiting re-audit after
2026-05-03 chirality repair). Closes Block 02's residual dependency
and unlocks substeps 1-2 from `conditional` to fully retained.

### Next-3: AC upgrade research

Either:
(a) New structural primitive establishing DHR superselection
    correspondence as framework-internal (currently HK+DHR are
    admitted standard machinery)
(b) Direct framework-derived argument for three-superselection-sector
    structure on H_phys without invoking external HK+DHR

This closes Block 05's residual admitted-context. Hard, multi-cycle
research.

### Next-4: g_bare = 1 normalization gate (formerly A4)

The other open gate from MINIMAL_AXIOMS_2026-05-03. Now that
staggered-Dirac is substantially closed, the g_bare = 1 derivation
chain has cleaner upstream foundations. Sister campaign target.

### Next-5: SM-fermion taste-vertex assignment

Bridge-gap-new-physics-20260506 Block 05's open question: which gl(1)
commutant U(1) factor on the taste cube corresponds to U(1)_Y?
Closing this would derive hypercharge from staggered-Dirac structure.

### Next-6: GUT embedding from graph-first surface

SU(5) GUT embedding (named open Nature-grade target per
AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02). Could leverage
the now-closed staggered-Dirac chain.

## Files touched (this campaign)

### Documents
- `docs/STAGGERED_DIRAC_FORCING_GAP_MAP_NOTE_2026-05-07.md` (Block 01)
- `docs/STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md` (Block 02)
- `docs/STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md` (Block 03)
- `docs/STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md` (Block 04)
- `docs/STAGGERED_DIRAC_PHYSICAL_SPECIES_BRIDGE_THEOREM_NOTE_2026-05-07.md` (Block 05)
- `docs/STAGGERED_DIRAC_REALIZATION_FORCING_THEOREM_NOTE_2026-05-07.md` (Block 06 synthesis)

### Scripts
- `scripts/probe_grassmann_forcing_dependency_chain.py` (Block 02 PASS=9/0)
- `scripts/probe_kawamoto_smit_phase_forcing.py` (Block 03 PASS=24/0)
- `scripts/probe_bz_corner_decomposition.py` (Block 04 PASS=5/0)

### Loop pack
- `.claude/science/physics-loops/staggered-dirac-realization-gate-20260507/`
  - GOAL.md, ASSUMPTIONS_AND_IMPORTS.md, NO_GO_LEDGER.md, ROUTE_PORTFOLIO.md
  - STATE.yaml (final)
  - HANDOFF.md (this file)
  - PR_BACKLOG.md (Block 06)

### Branches and PRs
- `physics-loop/staggered-dirac-realization-gate-block01-20260507` → PR [#631](https://github.com/jonathonreilly/cl3-lattice-framework/pull/631) OPEN
- `physics-loop/staggered-dirac-realization-gate-block02-20260507` → PR [#632](https://github.com/jonathonreilly/cl3-lattice-framework/pull/632) OPEN, stacked on #631
- `physics-loop/staggered-dirac-realization-gate-block03-20260507` → PR [#633](https://github.com/jonathonreilly/cl3-lattice-framework/pull/633) OPEN, stacked on #632
- `physics-loop/staggered-dirac-realization-gate-block04-20260507` → PR [#634](https://github.com/jonathonreilly/cl3-lattice-framework/pull/634) OPEN, stacked on #633
- `physics-loop/staggered-dirac-realization-gate-block05-20260507` → PR [#635](https://github.com/jonathonreilly/cl3-lattice-framework/pull/635) OPEN, stacked on #634
- `physics-loop/staggered-dirac-realization-gate-block06-20260507` → PR_BACKLOG (volume cap; ready for opening after 24h reset)

## Independent audit invitations

PRs #631-#635 await independent audit. Block 06 synthesis on the
block06 branch awaits PR opening after volume-cap reset (24h).

For the audit lane:
- Substeps 1-3 are POSITIVE theorems — eligible for retained tier
  upon audit ratification (Substep 1 conditional on S2 re-audit)
- Substep 4 is BOUNDED with admitted-context AC — bounded tier is
  honest given the AC dependency
- Block 06 synthesis is BOUNDED until S2 re-audit + AC upgrade close
