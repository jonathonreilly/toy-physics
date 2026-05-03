# HANDOFF — VEV V-Singlet Derivation Campaign

**Date:** 2026-05-02
**Slug:** `vev-v-singlet-derivation-20260502`
**Resume surface:** `STATE.yaml`

This handoff is updated at every checkpoint and is the canonical resume
surface for any agent picking up this campaign.

## Current state

| Field | Value |
|---|---|
| Mode | campaign |
| Runtime budget | 12h |
| Cycles completed | 0 |
| PRs opened | 0 |
| Active block | 01 |
| Active route | H2-A (f_vac V-singlet curvature reformulation) |
| Active residual | retire B1+B2+B3 of `OBSERVABLE_PRINCIPLE_FROM_AXIOM` 5-bridge audit |
| Active branch | `physics-loop/vev-v-singlet-derivation-block01-20260502` (from origin/main 1ef30c861) |
| Worktree | `/Users/jonreilly/Projects/Physics/.claude/worktrees/nostalgic-cori-c7fb1f` |

## Next exact action

Cycle 1: Write the umbrella theorem note's Lemma H2.1 (V-invariance of f_vac
on the minimal Klein-four block). Source: HIERARCHY_MATSUBARA_DECOMPOSITION
gives the closed-form `\|det(D+m)\| = ∏_ω [m² + u_0²(3+sin²ω)]^4`. Klein-four
acts on temporal phases. Show: action of V on `ω` permutes Matsubara modes
without changing the determinant.

## Proposed repo weaving (deferred to later review)

Once the science branches close as PRs and audit ratifies, the following
weaving would be appropriate (record only — DO NOT execute on science
branches):

- update `docs/CANONICAL_HARNESS_INDEX.md` to add `frontier_ew_vev_v_singlet_derivation.py`
- update `docs/lanes/` lane manifests for the EW v lane
- update `docs/repo/LANE_REGISTRY.yaml` for the EW v row
- update `docs/work_history/repo/LANE_STATUS_BOARD.md` for the v lane row
- update `docs/publication/ci3_z3/DERIVATION_ATLAS.md` to add a sister-theorem
  row mirroring the existing OBSERVABLE_PRINCIPLE_FROM_AXIOM row pattern
- update `docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md` if applicable
- update `docs/MINIMAL_AXIOMS_2026-04-11.md` consequence list

## Future-direction notes (not in this campaign)

- **H1 Route 3 (bootstrap closure):** ~6-month project requiring SDP
  infrastructure not in repo. Recommended for a separate campaign. Key
  references: Anderson-Kruczenski 2017, Kazakov-Zheng 2022, Lin et al 2023.
- **Lattice → physical matching Nature-grade target:** the cluster
  obstruction `LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02`
  is shared across cycles 5/9/11/17. H2 is INDEPENDENT of this; resolution
  of the cluster would close several other lanes simultaneously.
- **B5 hierarchy baseline retention:** depends on the plaquette/α_LM chain.
  Out of scope for this campaign.

## Stop history

(none yet)

## Risk log

- Risk R1: audit may rule that admission C1 ("v² is the m²-curvature of
  f_vac at origin") has comparable load-bearing weight to B1+B2+B3 combined.
  Mitigation: H2 note must explicitly justify C1 as a *definition* (closer
  to standard EFT language) rather than as a *bridge*, and show that B1+B2+B3
  do not appear in the H2 derivation.
- Risk R2: H1 Routes 1+2 likely produce only stretch-attempt / no-go output.
  Mitigation: that is honest output per skill; track as no-go in ledger.
- Risk R3: time pressure could push toward corollary-churn. Mitigation:
  explicit corollary-churn check before each new cycle after cycle 5.
