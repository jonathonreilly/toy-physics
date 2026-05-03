# CLAIM STATUS CERTIFICATE — Block 01 (H2 reformulation)

**Date:** 2026-05-02
**Block:** 01
**Branch:** `physics-loop/vev-v-singlet-derivation-block01-20260502`
**Slug:** `vev-v-singlet-derivation-20260502`
**Primary artifact:** `docs/EW_VEV_V_SINGLET_DERIVATION_THEOREM_NOTE_2026-05-02.md`
**Primary runner:** `scripts/frontier_ew_vev_v_singlet_derivation.py`

## Status fields

```yaml
actual_current_surface_status: exact-support
target_claim_type: positive_theorem
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  H2 reformulation provides a route to the (A_2/A_4)^(1/4) = (7/8)^(1/4)
  selector factor that retires bridges B1, B2, B3 (scalar additivity,
  CPT-even phase blindness, continuity) of the parent
  OBSERVABLE_PRINCIPLE_FROM_AXIOM 5-bridge audit. The new derivation is
  a positive theorem on retained framework primitives (A6, A7, A8, A9,
  A10) plus admitted C1 (textbook-standard EFT identification of v² with
  the curvature of f_vac at origin) plus the still-admitted B5 (separate
  hierarchy-baseline lane). The runner DERIVES (does not hard-code) the
  (7/8) and (7/8)^(1/4) values from direct Matsubara-mode sums.
audit_required_before_effective_retained: true
bare_retained_allowed: false
proposal_allowed: false
proposal_allowed_reason: |
  Honest tier on this branch is exact-support theorem with two admissions
  remaining (C1 textbook-standard, B5 separate-lane). Independent audit
  ratification is required before any effective-retained promotion. C1's
  classification (definition vs bridge of comparable weight to B1+B2+B3)
  is the load-bearing audit question; we cannot self-certify retained
  status.
```

## 7-criterion retained-proposal certificate

| # | Criterion | Pass? | Notes |
|---|---|---|---|
| 1 | `proposal_allowed: true` | **NO** | Set to false because C1 audit classification is the open question; this is exact-support, not retained-grade proposal |
| 2 | No open imports | **PARTIAL** | C1 (textbook EFT identification) and B5 (hierarchy baseline) remain admitted; this is the honest reduction from the parent's 5 admissions |
| 3 | No load-bearing observed/fitted/admitted unit conventions | **YES** | The (7/8) ratio is derived from rational arithmetic on Matsubara modes; no observed/fitted values used; admitted-context comparators (v_meas, framework (7/8)^(1/4) value) are explicitly out-of-scope |
| 4 | Every dep retained | **YES** | A6, A7, A8, A9, A10 are all retained framework primitives or direct corollaries (HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE, HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE) |
| 5 | Runner checks dep classes | **YES** | The runner verifies the V-invariance argument (Lemma H2.1), the orbit-closure structure (A8), the rational ratio (A9), and the selector-dependence of the result |
| 6 | Review-loop disposition `pass` | **PENDING** | Self-review PASS recorded in `REVIEW_HISTORY.md`; formal review-loop invocation deferred to the audit lane |
| 7 | PR body says independent audit required | **YES** | PR body explicitly states `proposal_allowed: false`, `audit_required_before_effective_retained: true` |

**Result:** Criterion 1 is intentionally NO (exact-support claim, not retained-grade proposal). Criterion 2 is partial (2 admissions remaining, down from 5). Criteria 3, 4, 5, 7 are YES; Criterion 6 is pending. **Honest tier: exact-support theorem.**

This is NOT proposing retained-grade promotion. It is proposing an
exact-support theorem that retires 3 of the parent's 5 bridges, with
independent audit ratification required before any retained-grade
classification.

## Promotion Value Gate (V1-V5)

Recorded in `REVIEW_HISTORY.md` §1. Disposition: **PASS** — all V1-V5
answered positively.

## Cluster-cap / volume-cap

- Volume cap: 1 of 5 used.
- Cluster cap: new family `vev-v-singlet-derivation-*`; 1 of 2 used.
- Corollary-churn: first cycle of campaign; not applicable.

## Imports retired

| Bridge in parent (B1-B5) | Retirement status under H2 |
|---|---|
| B1 (scalar additivity) | RETIRED — replaced by extensivity of f_vac (intensive thermodynamic free energy) |
| B2 (CPT-even phase blindness) | RETIRED — staggered det D is real-positive on real masses; no phase admission |
| B3 (continuity) | RETIRED — replaced by analyticity of Z[J] in J (finite-dim Grassmann, polynomial in J) |
| B4 (normalization) | NOT RETIRED — remains as standard thermodynamic normalization (no functional-equation framework-specific role) |
| B5 (hierarchy baseline) | NOT RETIRED — out of scope; depends on plaquette/α_LM separate lane |

**Net:** 3 framework-specific bridges retired; 2 admissions remain (one
textbook-standard EFT identification C1, one out-of-scope separate-lane B5).
The reduction in framework-specific load-bearing admissions is from 4
(B1+B2+B3+B4) to 1 (B4 alone, with B4 demoted to standard thermodynamic
convention rather than functional-equation premise).

## Imports newly exposed

| Admission | Class | Notes |
|---|---|---|
| C1: v² = -∂²f_vac/∂m²\|_0 for V-singlet source m | textbook-standard EFT | Coleman-Weinberg 1973; Peskin-Schroeder Ch. 11. Audit classification load-bearing question. |
| C2: vacuum at m=0 is V-singlet on finite minimal block | provable (Lemma H2.3) | Standard finite-volume argument; no SSB on finite V-symmetric block |

C2 is provable in the artifact, so not a true admission. C1 is a textbook
EFT identification that audit may classify as a "bridge" or as a
"definition"; we record this as Risk R1.

## Honest classification

This PR is a coherent **exact-support theorem** that retires 3 framework-specific
bridges of the parent OBSERVABLE_PRINCIPLE_FROM_AXIOM 5-bridge audit, on the
retained framework's minimal Klein-four block primitives, with one
textbook-standard EFT admission (C1) and one out-of-scope separate-lane
admission (B5).

It is NOT a retained-grade proposal. It is NOT a closure of the v lane
(B5 hierarchy baseline remains open). It is NOT a closure of the cluster
obstruction (the cluster covers different lanes; this PR is independent).

It IS a strict reduction in framework-specific admissions for the
(A_2/A_4)^(1/4) = (7/8)^(1/4) factor, modulo audit's classification of C1.

## Repo-weaving recommendation (for later integration, NOT executed in this PR)

For the later review/integration process (NOT executed on the science branch
per skill non-negotiable on repo authority surfaces):

- Add a sister-theorem row in `docs/publication/ci3_z3/DERIVATION_ATLAS.md`
  mirroring the existing OBSERVABLE_PRINCIPLE_FROM_AXIOM row pattern, with
  status "exact support" and admissions C1 + B5.
- If audit ratifies C1 as definition-class: amend status to retained-companion-grade.
- If audit pushes back on C1: H2 stays at exact-support tier, recorded as a
  parallel route to the parent W route, with a methodological note about
  the trade-off (3 functional-equation bridges vs 1 EFT identification).
- Update `docs/MINIMAL_AXIOMS_2026-04-11.md` consequences list to reference
  the H2 sister theorem.
- Add `frontier_ew_vev_v_singlet_derivation.py` to `docs/CANONICAL_HARNESS_INDEX.md`.

These are recorded in `HANDOFF.md` and not woven on the science branch.

## Stop conditions checked

- Runtime exhaustion: no (campaign just started)
- Volume cap: no (1 of 5 used)
- Cluster cap: no (1 of 2 used; new cluster)
- Corollary exhaustion: no (first cycle, novel content)
- Value-gate exhaustion: no (V1-V5 PASS)
- Tooling: no (all needed tools available)

## Next action

Commit theorem note + runner + loop-pack state. Push branch. Open PR with
title `[physics-loop] vev-v-singlet-derivation block01: f_vac reformulation
retires B1+B2+B3 (exact support)`. After PR is open, pivot to block 02
(H1 Route 2 cheap probe).
