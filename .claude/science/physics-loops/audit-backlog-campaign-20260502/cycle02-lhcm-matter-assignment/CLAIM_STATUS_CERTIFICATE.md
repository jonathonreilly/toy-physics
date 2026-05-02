# Claim Status Certificate — Cycle 2: LHCM Matter Assignment

**Date:** 2026-05-02
**Block:** physics-loop/lhcm-matter-assignment-block02-20260502
**Note:** `docs/LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`
**Runner:** `scripts/frontier_lhcm_matter_assignment.py`
**Runner result:** PASS=64 FAIL=0

## Status Vocabulary

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
conditional_surface_status: closes LHCM repair item (1) modulo SM-definition labels
hypothetical_axiom_status: null
admitted_observation_status: SM-definition labels (color-charged ≡ quark, color-singlet ≡ lepton)
proposal_allowed: false
proposal_allowed_reason: |
  Item (2) U(1)_Y normalization remains open in LHCM verdict, blocking
  full LHCM retention. This block closes item (1) only.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Seven Retained-Proposal Certificate Criteria — Honest Assessment

| # | Criterion | Pass? | Notes |
|---|---|---|---|
| 1 | `proposal_allowed: true` | **NO** | This certificate sets `proposal_allowed: false`. |
| 2 | No open imports for the claimed target | N/A given (1) | LHCM repair item (2) remains open. |
| 3 | No observed values, fitted selectors, admitted unit conventions, or literature values are load-bearing proof inputs | **YES** | Derivation rests on graph_first_su3_integration_note (retained) + SU(3) representation theory (standard math). SM-definition labels "quark"/"lepton" are admitted **for naming only** and do not enter the structural derivation. |
| 4 | Every dependency is retained, retained corollary, or explicitly allowed exact support | **PARTIAL** | The retained primitive is graph_first_su3_integration_note. HYPERCHARGE_IDENTIFICATION (audited_renaming) is cited only as a comparator, not as a load-bearing proof input. |
| 5 | Runner or proof artifact checks dependency classes, not only numerical output | **YES** | Runner (PASS=64/0) verifies note structure, citation classes, su(3) commutator algebra closure, fundamental rep trace identities, dimension counts, and explicit non-closure mark. |
| 6 | Review-loop disposition is `pass` | **PENDING** | Branch-local self-review = pass. |
| 7 | PR body explicitly says independent audit is still required | **YES** | Documented. |

**Result:** Criteria 1, 2, 4, 6 fail or are partial. The block is NOT
eligible for `proposed_retained`. The narrowest honest tier is
**exact algebraic identity / support theorem on retained graph-first surface**.

## What This Block Closes

- **LHCM repair item (1) "matter assignment"** modulo SM-definition labels:
  - The Sym²(3) sub-decomposition of the 4-point base is the **unique
    non-trivial irreducible representation of SU(3) on a 3-dim space**;
    structurally, this carries the SU(3) fundamental representation.
  - The Anti²(1) sub-decomposition is the **unique trivial (singlet)
    representation of SU(3) on a 1-dim space**; this is forced because SU(3)
    is its own commutator subgroup (perfect group), so all 1-dim characters
    are trivial.
  - The LH-doublet sector decomposes as `(2,3) ⊕ (2,1)` under SU(2)×SU(3),
    with (2,3) carrying 6 states (3 colors × 2 isospin) = SM Q_L count, and
    (2,1) carrying 2 states (1 singlet × 2 isospin) = SM L_L count.
  - SM-definition convention `color-charged ≡ quark, color-singlet ≡ lepton`
    forces the matter assignment Sym²(3) ↔ Q_L, Anti²(1) ↔ L_L.

The structural content of item (1) is now **derived from
graph_first_su3_integration_note (retained)** rather than admitted.

## What This Block Does NOT Close

- **LHCM repair item (2) "U(1)_Y normalization"**. The lepton-doublet
  eigenvalue −1 (normalization of the unique traceless U(1) direction) is
  still admitted convention. Closing this requires deriving the SM photon
  `Q = T_3 + Y/2` from graph-first surface — a deeper Nature-grade target.
- LHCM cannot be promoted to retained by this block alone; item (2) gates the
  full retention.
- The SM-definition convention (naming `color-charged ≡ quark`) remains
  admitted; this is a definitional choice in SM, not a derivation.

## Authorities Cited

| Authority | Surface status | Role in this note |
|---|---|---|
| `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` | retained | structural source of gl(3)⊕gl(1) commutant on Sym²/Anti² decomposition |
| `GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md` | retained | canonical axis selection |
| `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` | audited_conditional | parent of repair item (1) |
| `HYPERCHARGE_IDENTIFICATION_NOTE.md` | audited_renaming | cross-reference for SWAP-decomposition algebra (NOT load-bearing) |
| `RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md` | exact-support (cycle 1, PR #254) | sister support theorem closing (R-A,B,C) |
| Standard SU(3) representation theory (Gell-Mann matrices, fundamental rep) | admitted convention | structural representation theory |

## Forbidden Imports — Verified Absent

- No PDG observed quark/lepton charges or masses
- No literature SU(3) representation tables (only as audit comparators)
- No fitted selectors
- The SM-definition labels "quark" and "lepton" are admitted naming
  conventions, not load-bearing proof inputs

## Independent Audit Required

The note's status as `exact algebraic identity / support theorem` requires
fresh-context audit verification of:
1. su(3) commutator algebra closure via Gell-Mann generators on Sym²
2. SU(3) trivial action on Anti² (perfect-group → 1-dim characters trivial)
3. The dimension counting `(2,3) ⊕ (2,1) = 6+2 = 8` matches SM LH-doublet count

The PR body explicitly states this block does NOT promote LHCM,
HYPERCHARGE_IDENTIFICATION, or any upstream theorem to retained.

## Audit-Graph Effect

After this PR lands and the audit ledger regenerates:
- LHCM repair item (1) "matter assignment" becomes a derived consequence on
  the retained graph-first surface, with only SM-definition labels admitted.
- LHCM remains `audited_conditional`. Only item (2) "U(1)_Y normalization"
  remains open.
- Combined with PR #254 (R-A,B,C) and PR #253 (LH SU(2)²×Y), 4 of LHCM's
  5 named repair items are now derived as exact identities or representation
  theorems. Only U(1)_Y normalization (item 2) gates LHCM full retention.
- 488 transitive descendants under LHCM continue to await item (2).
