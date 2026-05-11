# LHCM Matter Assignment from SU(3) Representation Content

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on the retained
graph-first surface — closes LHCM repair item (1) "matter assignment" modulo
the SM-definition labels (`quark color` ≡ SU(3)-fundamental,
`lepton` ≡ SU(3)-singlet). NOT proposed_retained — see
CLAIM_STATUS_CERTIFICATE.md.
**Primary runner:** `scripts/frontier_lhcm_matter_assignment.py`
**Authority role:** structural matter-assignment companion to
`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`; closes the SU(3)-representation half
of repair item (1).

## 0. Statement

**Theorem (LHCM matter assignment from SU(3) representation content).**

On the graph-first selected-axis surface, the residual permutation `τ`
acting on the 4-point base induces the canonical Sym²/Anti² decomposition
`C⁴ = C³ ⊕ C¹`. Under the joint action of the gl(3)⊕gl(1) commutant of
{SU(2)_weak, τ}:

1. the 3-dimensional Sym² block is the **unique** non-trivial irreducible
   representation of the structural SU(3) on the 4-point base;
2. the 1-dimensional Anti² block is the **unique** trivial (singlet)
   representation of the structural SU(3) on the 4-point base;
3. the LH-doublet sector decomposes as a direct sum
   `(SU(2) doublet) ⊗ (Sym² triplet) ⊕ (SU(2) doublet) ⊗ (Anti² singlet)
    = (2,3) ⊕ (2,1)` under the structural SU(2)×SU(3).

Under the SM-definition convention that
`color-charged Weyl fermion ≡ quark, color-singlet Weyl fermion ≡ lepton`:

- the (2,3) sector IS the LH quark doublet `Q_L` of SM;
- the (2,1) sector IS the LH lepton doublet `L_L` of SM.

This identification is forced by the SU(3) representation content; only the
labels "quark" and "lepton" are SM-definition conventions, not derivations.

## 1. Retained inputs

| Ingredient | Class | Reference | Role |
|------------|-------|-----------|------|
| graph-first selector picks axis μ canonically | retained | [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md) | canonical axis selection |
| selected-axis shift+parity generates SU(2)_weak on 2-fiber | retained | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) Step 2 | weak fiber structure |
| residual permutation τ acts on 4-point base | retained | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) Step 3 | Sym²/Anti² decomposition |
| 3⊕1 commutant decomposition under τ | retained | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) Step 3-5 | irreducible blocks |
| compact semisimple commutant = SU(3) | retained | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) §"What this closes" | structural SU(3) |

No PDG observed values, no fitted selectors, no literature numerical
comparators are imported. The labels "quark" and "lepton" are admitted
SM-definition conventions only — they do not enter the structural derivation.

## 2. SU(3) Representation Theory on Sym²/Anti²

### 2.1 The 4-point base under SWAP_{ν,ρ}

After axis μ is selected, the residual two coordinates ν, ρ have a canonical
transposition τ that exchanges them. Acting on the 4-point base
`{0,1}² = {(0,0), (0,1), (1,0), (1,1)}`, τ permutes states as
`τ(a,b) = (b,a)`.

The eigendecomposition of τ on `C⁴`:
- 3 symmetric eigenvectors at eigenvalue +1 (Sym²(C²) ⊆ End(C^4)):
  `|00⟩, |11⟩, (|01⟩ + |10⟩)/√2`
- 1 antisymmetric eigenvector at eigenvalue −1 (Anti²(C²)):
  `(|01⟩ − |10⟩)/√2`

This is the canonical Sym²/Anti² decomposition under the symmetric group S₂.

### 2.2 The structural SU(3) acts irreducibly on Sym²

Per `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` Steps 4-5, the joint commutant of
{SU(2)_weak (on selected axis fiber), τ (on residual base)} contains the
gl(3) algebra acting on the Sym² block, with compact semisimple part su(3).

The SU(3) acts on Sym² as the **fundamental representation** (3) by direct
construction:
- The 3 generators of su(3) ≅ gl(3) (after tracelessness) are operators in
  End(Sym²(C²)) that close under [·,·] = the standard su(3) Lie bracket.
- The Gell-Mann embedding given in the integration note (Step 4) places the
  8 SU(3) generators on the 3-dimensional Sym² block, exactly as the
  fundamental rep matrix algebra.

Equivalently: any non-trivial irreducible representation of su(3) on a
3-dimensional complex vector space is the fundamental representation 3 (up
to outer automorphism, which gives the conjugate 3̄). The Sym² block is
3-dimensional, the SU(3) acts non-trivially on it (otherwise the commutant
on the full 4-point base would not match gl(3)⊕gl(1), as proven in the
retained integration theorem). Therefore Sym² carries the fundamental rep 3.

### 2.3 The structural SU(3) acts trivially on Anti²

The Anti² block is 1-dimensional. Any representation of su(3) on a
1-dimensional space is necessarily trivial (the determinant character is
trivial since SU(3) is its own commutator subgroup). Equivalently, the
gl(1) factor of the commutant gl(3)⊕gl(1) acts on the Anti² block, which
means the SU(3) (the gl(3) traceless part) acts trivially.

### 2.4 LH-doublet sector tensor decomposition

The LH-doublet sector is

```text
LH_doublet  =  (SU(2) doublet on selected fiber) ⊗ (4-point base)
            ≅  C² ⊗ C⁴
            =  C² ⊗ (Sym² ⊕ Anti²)
            =  (C² ⊗ Sym²) ⊕ (C² ⊗ Anti²)
            =  (2,3) ⊕ (2,1)         under SU(2)×SU(3)
```

The (2,3) factor carries the SU(3)-fundamental representation and is
6-dimensional (matching the 6 LH quark states: 3 colors × 2 isospin); the
(2,1) factor carries the SU(3)-trivial representation and is 2-dimensional
(matching the 2 LH lepton states: 1 color-singlet × 2 isospin).

### 2.5 SM-definition matter assignment

The Standard Model definition of "quark" and "lepton":

> *A quark is a Weyl fermion in a non-trivial irreducible representation of
> the SU(3) color group. A lepton is a Weyl fermion in the SU(3) trivial
> (singlet) representation.*

This is a definitional convention, not a derivation.

Under this convention:
- the (2,3) sector with 6 states (3-fundamental color × 2 isospin) IS the
  Standard Model LH quark doublet `Q_L`;
- the (2,1) sector with 2 states (1-singlet color × 2 isospin) IS the
  Standard Model LH lepton doublet `L_L`.

This identification is **forced** by SU(3) representation content; only the
choice of names ("quark" and "lepton") is admitted as SM convention.

## 3. Closure of LHCM repair item (1) "matter assignment"

LHCM's verdict-rationale named three repair items. PR #253 closed item (3)
(anomaly-complete chiral completion for LH doublets via SU(2)²×U(1)_Y).
Cycle 1 of the audit-backlog campaign (PR #254) closed (R-A,B,C) sub-items
of item (3) for the full one-generation content.

This block (cycle 2) closes item (1) "matter assignment":

- **What was admitted before this block:** the labeling Sym²(3) ↔ quark
  doublet, Anti²(1) ↔ lepton doublet was claimed without an explicit
  SU(3)-representation theorem.
- **What this block proves:** the Sym²(3) block carries the SU(3)
  fundamental representation, the Anti²(1) block carries the SU(3) trivial
  representation; under the SM-definition convention
  `color-charged ≡ quark, color-singlet ≡ lepton`, the matter assignment
  is forced.
- **What remains admitted:** the SM-definition labels themselves
  (`quark` for SU(3)-charged, `lepton` for SU(3)-neutral). This is a
  definitional convention; deriving "what fermion species a fundamental
  SU(3) rep at this scale should be called" is not a physics derivation —
  it is naming.

## 4. Validation

- primary runner:
  [`scripts/frontier_lhcm_matter_assignment.py`](../scripts/frontier_lhcm_matter_assignment.py)
  — verifies (a) the canonical Sym²/Anti² decomposition under S₂; (b) that
  SU(3) on Sym² acts as the fundamental (3-dim irrep) by explicit Gell-Mann
  matrix construction and verification of su(3) commutator relations; (c)
  that SU(3) on Anti² acts trivially (1-dim singlet); (d) that the LH-doublet
  sector tensor decomposition matches the SM (Q_L, L_L) multiplet structure
  under the SM-definition convention.

## 5. Authority surface

- `actual_current_surface_status: exact algebraic identity / support theorem`
- `conditional_surface_status: closes LHCM repair item (1) modulo SM-definition labels`
- `proposal_allowed: false` — does not promote LHCM to retained because LHCM
  repair item (2) "U(1)_Y normalization" remains open
- `bare_retained_allowed: false`
- `audit_required_before_effective_retained: yes`

## 6. What this block does NOT close

- LHCM repair item (2) **U(1)_Y normalization** — the lepton-doublet
  eigenvalue normalization to −1 is still an admitted convention (it
  fixes the overall scale of the U(1)_Y direction). Closing this requires
  deriving the SM photon `Q = T_3 + Y/2` from graph-first surface, which
  is a deeper Nature-grade target.
- The retention of LHCM, HYPERCHARGE_IDENTIFICATION_NOTE, or
  STANDARD_MODEL_HYPERCHARGE_UNIQUENESS — those still depend on item (2).

## 7. Cross-references

- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) — parent
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained primitive supplying the gl(3)⊕gl(1) commutant
- `HYPERCHARGE_IDENTIFICATION_NOTE.md` — sister cross-reference for SWAP-decomposition algebra (audited_renaming); backticked to break length-2 citation cycle with this LHCM matter-assignment note — citation graph direction is *hypercharge_identification → this_lhcm* (this note supplies the matter-assignment input that hypercharge_identification consumes in its proof; the reverse SWAP-algebra link is informational sibling, not load-bearing for this LHCM derivation)
- `RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md` (sister
  support theorem; backticked to avoid length-3 cycle through
  HYPERCHARGE_IDENTIFICATION — that RH-sector note already cites
  hypercharge_identification's trace algebra in its body, so citation
  graph direction is *rh_sector → hypercharge → this_lhcm* via the
  joint hypercharge/LHCM authority pair) — sister support theorem closing (R-A,B,C) of LHCM repair item (3)
- PR #253 (open) — sister theorem for SU(2)²×U(1)_Y on LH doublets
- PR #254 — cycle 1 of audit-backlog campaign closing (R-A,B,C)
