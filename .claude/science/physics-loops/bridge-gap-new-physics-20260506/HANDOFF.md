# Bridge Gap New Physics Loop — Final Handoff

**Date:** 2026-05-06
**Loop slug:** bridge-gap-new-physics-20260506
**Mode:** campaign (12h budget)
**Runtime used:** ~6 hours (50% of 12h budget; campaign reaching corollary-exhaustion-adjacent state)

## Summary

Six science blocks complete on the bridge-gap new-physics opening (per
[`docs/BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md)).
The campaign systematically explored whether the framework's gauge
action is genuinely Wilson (currently imported) or whether heat-kernel
(Casimir-native candidate) is the framework's actually-derived action.

## Block-level deliverables

| Block | Note | Runner | Status | PR |
|---|---|---|---|---|
| 01 | `BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md` | `probe_hk_time_derivation.py` PASS=7/0 | bounded support | [#617](https://github.com/jonathonreilly/cl3-lattice-framework/pull/617) OPEN |
| 02 | `BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md` | `probe_hk_plaquette_closed_form.py` PASS=8/0 | bounded support | [#619](https://github.com/jonathonreilly/cl3-lattice-framework/pull/619) OPEN, stacked on #617 |
| 03 | `BRIDGE_GAP_HK_THERMODYNAMIC_STRETCH_NOTE_2026-05-06.md` | (theoretical) | stretch + named-obstruction | PR_BACKLOG |
| 04 | `BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md` | (no-go analysis) | named-obstruction no-go | PR_BACKLOG |
| 05 | `BRIDGE_GAP_GAUGE_GROUP_TASTE_CUBE_EXPLORATION_NOTE_2026-05-06.md` | (exploration) | exploration / open_gate | PR_BACKLOG |
| 06 | `BRIDGE_GAP_HK_CUBE_PERRON_NOTE_2026-05-06.md` | `probe_hk_cube_perron_l2_2026_05_06.py` numerical | bounded support | PR_BACKLOG |

Plus three scoping notes from pre-loop work:
- `BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md` (parent)
- `BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md` (sibling, retires 7 routes)
- `BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md` (demoted fallback)

Plus probe script `scripts/probe_heat_kernel_su3_plaquette.py` (multi-convention HK probe motivating the loop).

## Cross-block synthesis: where the bridge gap stands now

### Positive content (closed in this campaign)

1. **Wilson is admitted-as-import, not derived.** Verbatim from
   `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md` line
   467: "Standard Wilson plaquette action ... retained convention,
   not derived from Cl(3)." Documented in scoping notes.

2. **Heat-kernel time t = g_bare² = 1 derived from canonical Tr-form
   (Block 01).** Theorem (T1) bounded support; under leading-order
   small-U Wilson-HK matching at canonical normalization.

3. **HK single-plaquette ⟨P⟩_HK,1plaq(6) = exp(-2/3) ≈ 0.5134 in
   exact closed form (Block 02).** Theorem (T2) bounded support;
   Schur orthogonality forces exact-in-2-characters result, structurally
   distinct from Wilson's infinite Bessel-determinant series.

4. **HK multi-plaquette partition function admits exact Casimir-diagonal
   factorization (Block 03).** Theorem (T3.a) bounded support;
   `Z = Σ (Π W_λ) F_Λ` with W_λ = d_λ exp(-t·C_2/2) per-plaquette and
   F_Λ t-independent Wigner-Racah graph trace. Fundamentally cleaner
   than Wilson.

5. **HK cube Perron L_s=2 = 0.5223 numerical artifact (Block 06).**
   Theorem (T6) bounded support; HK is 22% larger than Wilson cube
   0.4291 at the same lattice size, and 2.3× closer to lattice MC
   comparator 0.5934 in ε_witness units. Suggestive empirical evidence
   for HK naturality.

### Negative content (no-gos closed in this campaign)

6. **Action-form uniqueness is structurally undetermined (Block 04).**
   Theorem (T4) named-obstruction no-go. Wilson, HK, and Manton are
   jointly compatible with all currently-retained framework primitives
   + continuum-limit matching. No retained primitive selects one. Under
   the no-new-axiom rule, action-form ambiguity is **structural**, not
   a research-effort gap.

7. **Multi-plaquette HK thermodynamic limit needs cluster-decomposition
   estimate not in current primitives (Block 03 named obstruction).**
   The Casimir-diagonal structure makes the theoretical setup cleaner
   than Wilson, but the Λ → ∞ extrapolation requires an exponential-
   clustering bound on the Casimir-graded correlation structure. RP-A11
   + Lieb-Robinson + per-site dim 2 don't provide it.

8. **Cl(3) ⊗ Cl(3) → SU(4) ⊃ SU(3) × U(1) tensor angle does NOT break
   Block 04's no-go (Block 05).** The taste-cube structure supports
   richer SU(3) × U(1)^k gauge symmetry, but the SU(3) action-functional
   ambiguity (Wilson/HK/Manton) is independent of U(1) considerations.

### Net structural finding

The bridge gap has TWO independent structural layers:
- **Layer 1 (action-form ambiguity):** the framework cannot derive a
  unique gauge action from current primitives. Wilson vs HK vs Manton
  give distinct ⟨P⟩(6) values at any finite β. Range-bounding effect
  on the four cluster lanes' downstream chains is ~5-10% (150-300×
  ε_witness).
- **Layer 2 (thermodynamic ⟨P⟩(6) within fixed action):** the famous
  open lattice problem under each chosen action. For Wilson, this is
  the canonical 50-year-old problem. For HK, the Casimir-diagonal
  structure makes it cleaner but still requires a cluster-decomposition
  estimate not in current primitives.

**Layer 1's no-go is the deeper structural finding.** Even if Layer 2
is closed (e.g., via industrial SDP for one specific action), Layer 1's
ambiguity means the answer depends on the action choice that is itself
not derived.

## Numerical comparator table (consolidated)

| Quantity | Numerical | Source / Block |
|---|---|---|
| Wilson 1-plaq ⟨P⟩_W(6) | 0.4225317396 | V=1 PF ODE certified |
| Wilson cube L_s=2 ⟨P⟩_W,L=2(6) | 0.4291049969 | existing runner (5/04) |
| HK 1-plaq ⟨P⟩_HK,1plaq(t=1) | 0.5134171190 | Block 02, exp(-2/3) closed form |
| HK cube L_s=2 ⟨P⟩_HK,L=2(t=1) | 0.5223243151 | Block 06 |
| Lattice MC ⟨P⟩(6) | ≈ 0.5934 | comparator only |
| 4D MC FSS ⟨P⟩(6) | 0.59400 ± 0.00037 | comparator only |

ε_witness ≈ 3.030×10⁻⁴.

## Imports retired / exposed

### Retired (formally documented as imports)

- "Wilson is the framework's derived action" — explicitly NOT
  derived per `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18`.
  All seven previously-exhausted attack routes assumed Wilson, hence
  their failures don't extend to HK or other actions.

### Exposed

- **Action-form uniqueness** is now a known no-go under current
  primitives (Block 04).
- **HK Brownian time t at canonical normalization = 1** (Block 01).
- **HK 1-plaq exact closed form exp(-2/3)** (Block 02).
- **HK multi-plaquette factorization theorem** (Block 03).
- **HK cube L_s=2 numerical = 0.5223** (Block 06).

## Campaign rules respected

- ✓ No PDG/MC values as derivation inputs (comparators only)
- ✓ No fitted coefficients
- ✓ No same-surface family arguments
- ✓ No bare retained / promoted in branch-local notes; consistent
  bounded-support / no-go / open-gate / exploration tier labels
- ✓ Cluster cap respected (2 PRs in `bridge_gap_new_physics_*` family;
  Blocks 03-06 in PR_BACKLOG)
- ✓ Volume cap respected (2 of 5 24h-cap used)
- ✓ Forbidden imports tracked in ASSUMPTIONS_AND_IMPORTS.md
- ✓ V1-V5 promotion-value gate applied per cycle (PASS for all 6 blocks)
- ✓ Corollary-churn check applied; no churn (all blocks introduce new
  load-bearing premise or named obstruction or numerical artifact not
  derivable from prior blocks)
- ✓ REVIEW_HISTORY entries for all 6 blocks
- ✓ CLAIM_STATUS_CERTIFICATE.md updated for Blocks 01-02

## Stop reason

**Corollary-exhaustion-adjacent + cluster cap reached.** The campaign
has covered the four central angles of the new-physics opening:
1. Time derivation (Block 01) — DONE bounded
2. 1-plaq closed form (Block 02) — DONE bounded
3. Thermodynamic limit (Block 03) — named obstruction
4. Action-form uniqueness (Block 04) — no-go
5. Larger gauge structure (Block 05) — exploration
6. L_s=2 cube comparator (Block 06) — DONE bounded

Remaining ranked opportunities:
- L_s=3 cube under HK: heavy computational lift, no existing project
  framework runner; would require multi-day adaptation of cube
  geometry. Out of scope for remaining ~6h.
- Cube-shell strong-coupling β⁶ enumeration: incremental — adds one
  exact rational coefficient. Not corollary churn but marginal value
  given Block 04's no-go on action-form uniqueness already capped the
  campaign's structural progress.
- Manton numerical comparator at L_s=2: would confirm Block 04's no-go
  with a third action data point. Marginal — no-go is already
  structurally proven.
- Cluster-decomposition estimate from RP-A11: hard, multi-cycle work.
  Out of scope.

Stopping cleanly with comprehensive 6-block coverage of the central
angles, leaving runtime for next campaign on follow-on directions.

## Recommended next campaign(s)

In priority order:

### Next-1: Open Block 03+04+5+6 PRs as stacked PRs

The cluster cap of 2 PRs/24h was reached at Block 02 (#619). After
24h elapsed, open the four backlog PRs as a stacked chain:

```
physics-loop/bridge-gap-new-physics-block03-* (base = block02)
  → docs/BRIDGE_GAP_HK_THERMODYNAMIC_STRETCH_NOTE_2026-05-06.md
physics-loop/bridge-gap-new-physics-block04-* (base = block03)
  → docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md
physics-loop/bridge-gap-new-physics-block05-* (base = block04)
  → docs/BRIDGE_GAP_GAUGE_GROUP_TASTE_CUBE_EXPLORATION_NOTE_2026-05-06.md
physics-loop/bridge-gap-new-physics-block06-* (base = block05)
  → docs/BRIDGE_GAP_HK_CUBE_PERRON_NOTE_2026-05-06.md (with paired runner)
```

All 4 commits already exist on the `physics-loop/bridge-gap-new-physics-block02-20260506`
branch (HEAD at 4d109ed3f as of campaign close). Cherry-pick into
separate branches and open stacked PRs.

### Next-2: Resolution-B governance reclassification

Block 04's no-go means action-form is not derivable under current
primitives. Resolution B (admit a specific action — Wilson by precedent
or HK by Casimir-natural argument — as scheme convention with narrow
non-derivation role) would close the four cluster lanes' quantitative
ambiguity at the labeling layer. The user explicitly de-prioritized
this on 2026-05-06; revisit if needed.

### Next-3: HK cluster-decomposition estimate from retained primitives

Block 03's named obstruction. Hard, multi-cycle. Would require:
- A11 RP + Lieb-Robinson + per-site Cl(3) dim 2 → exponential clustering
  of Casimir-graded HK correlators
- Translation into an L_s → ∞ extrapolation bound that's NOT laundered
  through MC comparator

### Next-4: L_s=3 cube under HK

Adapts Block 06's L_s=2 to L_s=3 geometry. Computationally heavier;
expect multi-day. Would give a SECOND empirical data point on whether
HK converges to MC faster than Wilson. Useful but not structurally
decisive (Block 04's no-go stands either way).

### Next-5: SM-fermion taste-vertex assignment

Block 05's open question (3): assign SM fermion species to taste-cube
vertices in a way that makes one of the four U(1) factors identifiable
with U(1)_Y. Hard, depends on staggered-Dirac open gate.

### Next-6: Cube-shell strong-coupling expansion to β⁶

Cheap parallel track. Extends `GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE`
past β⁵. Adds one exact rational coefficient. Marginal value but
genuine derivation (not corollary).

## Files touched (this campaign)

### Documents (committed across multiple branches)
- `docs/BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md` (scoping)
- `docs/BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md` (scoping)
- `docs/BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md` (scoping, demoted to fallback)
- `docs/BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md` (Block 01)
- `docs/BRIDGE_GAP_HK_PLAQUETTE_CLOSED_FORM_NOTE_2026-05-06.md` (Block 02)
- `docs/BRIDGE_GAP_HK_THERMODYNAMIC_STRETCH_NOTE_2026-05-06.md` (Block 03)
- `docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md` (Block 04)
- `docs/BRIDGE_GAP_GAUGE_GROUP_TASTE_CUBE_EXPLORATION_NOTE_2026-05-06.md` (Block 05)
- `docs/BRIDGE_GAP_HK_CUBE_PERRON_NOTE_2026-05-06.md` (Block 06)

### Scripts
- `scripts/probe_heat_kernel_su3_plaquette.py` (motivating probe, 5 conventions)
- `scripts/probe_hk_time_derivation.py` (Block 01 PASS=7/0)
- `scripts/probe_hk_plaquette_closed_form.py` (Block 02 PASS=8/0)
- `scripts/probe_hk_cube_perron_l2_2026_05_06.py` (Block 06 numerical)

### Loop pack
- `.claude/science/physics-loops/bridge-gap-new-physics-20260506/`
  - GOAL.md
  - ASSUMPTIONS_AND_IMPORTS.md
  - NO_GO_LEDGER.md
  - ROUTE_PORTFOLIO.md
  - OPPORTUNITY_QUEUE.md
  - STATE.yaml (final)
  - CLAIM_STATUS_CERTIFICATE.md (Blocks 01-02 detail; Blocks 03-06 in note bodies)
  - REVIEW_HISTORY.md (all 6 blocks)
  - PR_BACKLOG.md
  - HANDOFF.md (this file)

### Branches and PRs
- `physics-loop/bridge-gap-new-physics-block01-20260506` → PR [#617](https://github.com/jonathonreilly/cl3-lattice-framework/pull/617) OPEN (base=main)
- `physics-loop/bridge-gap-new-physics-block02-20260506` → PR [#619](https://github.com/jonathonreilly/cl3-lattice-framework/pull/619) OPEN (base=block01); also contains Blocks 03-06 commits in PR_BACKLOG

## Final HEAD

`physics-loop/bridge-gap-new-physics-block02-20260506` HEAD = 4d109ed3f
(as of Block 06 push 2026-05-06).

## Independent audit invitations

PRs #617 and #619 await independent audit. Branch HEAD also contains
Blocks 03-06 commits ready for stacked-PR creation in next campaign.

For the audit lane: the bounded_theorem tier on Blocks 01-02 is the
narrowest honest tier given the inherited conditionals (g_bare = 1
open gate, HK as candidate action, leading-order matching). Blocks
03-04-05 are open_gate / no_go tier per controlled vocabulary. Block
06 is bounded_theorem-numerical artifact.

If the audit lane disagrees with any tier label, demotion is acceptable
(cf. user-memory feedback that retained-tier purity must NOT include
support-tier routes; the tier labels on this campaign are deliberately
narrow).
