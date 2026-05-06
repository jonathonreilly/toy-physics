# Hypercharge U(1)_Y Identification from the Commutant

**Type:** bounded_theorem (rewritten 2026-05-05; previous load-bearing
identification step was ratified `audited_renaming`; the rewrite reroutes
that step through citation chain).
**Status:** chain claim — the load-bearing step is the
structural eigenvalue ratio 1:(-3) on the (Sym², Anti²) sub-decomposition of
the LH-doublet sector, supplied by the retained-grade narrow ratio theorem,
combined with the (Sym², Anti²) ↔ (SU(3)-fundamental, SU(3)-singlet)
representation-theory chain supplied by the LHCM matter assignment note.
The SM-Y matching on the LH-doublet surface follows from those two upstream
chains under the SM-definition convention `color-charged ≡ quark, color-singlet ≡ lepton`.

**Re-audit handoff (2026-05-05).** The previous load-bearing step (named
"With conventional normalization a=1/3, the (2,3) subspace is identified with
the left-handed quark doublet and the (2,1) subspace is identified with the
left-handed lepton doublet, so the traceless commutant U(1) matches SM
hypercharge on that surface.") was ratified as `audited_renaming` on the
basis that the matter-sector identification was not derived. This rewrite
removes that identification from the load-bearing chain and replaces it
with a citation to the matter-assignment representation theorem (cited
authority below). The absolute normalization choice (`a = 1/3`) is now
moved out of the load-bearing chain and explicitly admitted as SM
convention; closing it requires the still-open LHCM repair item (2),
covered by the parent atlas.

## Audit boundary

This note carries no derivation of the (Sym², Anti²) ↔ (color triplet,
color singlet) assignment internally. That assignment is forwarded to
[`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md)
which derives, from the retained graph-first SU(3) integration note's
gl(3) ⊕ gl(1) commutant theorem, that:

- the Sym²(C²) block carries the SU(3) fundamental representation (3);
- the Anti²(C²) block carries the SU(3) trivial representation (1).

The SM-definition convention `color-charged Weyl fermion ≡ quark,
color-singlet Weyl fermion ≡ lepton` is then a definitional convention,
not a derivation; the matter assignment Q_L ↔ (2, 3), L_L ↔ (2, 1)
follows from SU(3) representation content. This note imports that chain
as a one-hop authority.

This note does **not** claim to:

- derive the (Sym², Anti²) ↔ (triplet, singlet) assignment internally;
- derive the absolute normalization `a = 1/3` from the framework
  (admitted SM convention; this is the still-open LHCM repair item 2);
- complete the full anomaly-canceling Standard Model spectrum.

Audit history: the audit lane recorded `audit_status=audited_renaming`
under cross-confirmation by `codex-audit-loop-round-2` and
`codex-fresh-context-20260430-03-hypercharge` on the previous version
whose load-bearing step internally identified (2, 3) ≡ Q_L. The current
rewrite reroutes that step through the cited authority chain and is
proposed for re-audit at `bounded_theorem` / `audited_clean`.

## Statement

**Theorem (chained ratio + matter assignment ⇒ SM-Y match on LH-doublet
surface).** Let C^8 = (C²)^{⊗3} be the LH-doublet sector with SU(2)_weak
on factor 1 (from the retained graph-first selector + bipartite lattice
structure) and SWAP_{23} on factors 2, 3 (from the retained Z₂ spatial
permutation symmetry). Let Y_α = α(P_sym − 3 P_anti) be the
one-parameter family of traceless U(1) generators in the (gl(3) ⊕
gl(1))-commutant of {SU(2)_weak, SWAP_{23}}, parameterized by α ∈ ℝ. Then:

1. *(Ratio)* The eigenvalues of Y_α on the (2, 3) and (2, 1) sub-blocks
   stand in the ratio 1 : (−3) for every α ≠ 0. *Source:*
   [`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md).
2. *(Matter assignment under SM-definition convention)* Under the
   SM-definition convention `color-charged ≡ quark, color-singlet ≡
   lepton`, the (2, 3) sector is the LH quark doublet Q_L and the
   (2, 1) sector is the LH lepton doublet L_L. *Source:*
   [`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md).
3. *(Normalization is admitted SM convention)* Setting α = +1/3
   produces eigenvalues (+1/3, −1) on (Q_L, L_L), matching the SM
   hypercharge values. The absolute scale `α = 1/3` is **not derived**
   in this note and is imported as the SM convention `Y(L_L) = −1`.

The combined SM-Y matching follows from (1) + (2) once the convention
in (3) is fixed. This note is the chain assembly point for these three
items; the new load-bearing step is the chain itself, not any of (1),
(2), or (3) individually (each is supplied by — or admitted as input to —
its own ledger row).

## Setup

The taste space C^8 = (C²)^{⊗3} carries two structures that follow from
the retained graph-first selector + integration chain:

1. **SU(2)_weak**: S_i = σ_i / 2 on factor 1, derived from the bipartite
   lattice structure of the selected-axis surface (see
   `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`).
2. **SWAP_{23}**: exchanges tensor factors 2 and 3, the residual Z₂
   permutation after axis selection (same upstream).

The commutant of {SU(2), SWAP_{23}} in End(C^8) is gl(3, ℂ) ⊕ gl(1, ℂ),
with semisimple part su(3). Under the SWAP_{23} eigendecomposition,
C⁴ = Sym²(C²) ⊕ Anti²(C²) = C³ ⊕ C¹, and the LH-doublet sector
decomposes as:

    C^8 = C² ⊗ (C³ ⊕ C¹) = (C² ⊗ C³) ⊕ (C² ⊗ C¹) = (2, 3) ⊕ (2, 1)

under SU(2) × SU(3). All of this is retained-grade content of
[`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
(claim_type: bounded_theorem, audit_status: audited_clean,
effective_status: retained_bounded, cross-confirmed).

## The U(1) Generator (structural part)

The commutant gl(3) ⊕ gl(1) on C⁴ contains a 2-parameter family of U(1)
generators:

    Y(α, β) = α P_sym + β P_anti       (on the C⁴ factor)

Embedded in C^8: Y_8 = I_2 ⊗ Y(α, β). Eigenvalues on C^8: α (× 6, on
the (2, 3) sector), β (× 2, on the (2, 1) sector).

**Tracelessness** (removing the trivial overall phase):

    Tr_{C^8}[Y_8] = 6α + 2β = 0   ⇒   β = −3α.

This leaves a one-parameter traceless family Y_α = α(P_sym − 3 P_anti)
with eigenvalue ratio +1 : (−3) on (Sym², Anti²) — independent of α.

**Source for the ratio:** the structural ratio +1 : (−3) is the load-bearing
content of
[`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md)
(claim_type: bounded_theorem; audit_status: audited_conditional —
conditional only on the still-open staggered-Dirac realization gate, not
on any internal renaming step).

## Chained matter assignment (Sym²/Anti² ↔ triplet/singlet)

The (Sym², Anti²) ↔ (SU(3)-fundamental, SU(3)-singlet) representation-theory
mapping is supplied by
[`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md):

> 1. the 3-dimensional Sym² block is the **unique** non-trivial irreducible
>    representation of the structural SU(3) on the 4-point base;
> 2. the 1-dimensional Anti² block is the **unique** trivial (singlet)
>    representation of the structural SU(3) on the 4-point base.

Combined with the SM-definition convention `color-charged ≡ quark,
color-singlet ≡ lepton`, the matter assignment Q_L ↔ (2, 3) and
L_L ↔ (2, 1) is **forced** by SU(3) representation content. The labels
"quark" and "lepton" themselves are SM-definition conventions; deriving
"what fermion species an SU(3) fundamental rep at this scale should be
called" is naming, not physics derivation.

## Structural consequences (downstream of the chain)

Each consequence below follows from the chain (1) + (2) + the admitted
SM-convention normalization (3) of the **Statement** section. None is
load-bearing for this note's theorem; all are downstream consistency
checks under the chained inputs.

### 1. Eigenvalue Pattern at α = 1/3 (SM-convention scale)

With α = 1/3 (SM convention `Y(L_L) = −1`):

| Sub-block | Multiplicity | Y_α | SM identification (via LHCM matter assignment) |
|----------|-------------|---------|-------------------|
| (2, 3) = C² ⊗ Sym²(C²) | 6 | +1/3 | Left-handed quark doublet Q_L |
| (2, 1) = C² ⊗ Anti²(C²) | 2 | −1 | Left-handed lepton doublet L_L |

These match the SM hypercharge values on the LH-doublet surface — under
the chained matter assignment and the admitted SM-convention scale.

### 2. Electric Charge (downstream, under chain)

With T_3 = σ_3/2 on the weak factor and the SM Gell-Mann–Nishijima
convention Q = T_3 + Y/2, applied to the chained matter assignment at
α = 1/3:

| Particle | T_3 | Y | Q = T_3 + Y/2 |
|----------|------|---|----------------|
| u_L (3 colors) | +1/2 | +1/3 | +2/3 |
| d_L (3 colors) | −1/2 | +1/3 | −1/3 |
| ν_L | +1/2 | −1 | 0 |
| e_L | −1/2 | −1 | −1 |

These charges match the SM pattern. The Gell-Mann–Nishijima formula
itself is an SM-convention bridge; it is not derived in this note.

### 3. Uniqueness (structural part of the chain)

The argument that the traceless U(1) is unique up to scale is purely
algebraic and is the load-bearing step of the narrow ratio theorem cited
above:

1. The commutant contains a 2-dimensional space of U(1) generators
   (two independent projectors P_sym and P_anti on the Sym² and Anti²
   sub-blocks).
2. The tracelessness condition 6α + 2β = 0 imposes one linear constraint.
3. This reduces the space to **dimension 1** — a unique generator up to
   normalization.
4. That unique generator has eigenvalue ratio +1 : (−3) on (Sym², Anti²).

Step 4 is **the load-bearing structural fact**. Identification with SM
hypercharge follows from the chain in (Statement, items 1–3); it is
**not** a separate uniqueness claim for this note.

### 4. Consistency Checks on the Left-Handed Surface

For the 8 LH states under the chain:

- **Tr[Y_α] = 0 on C^8:** 6α + 2(−3α) = 0. By construction of the
  traceless family.
- **Tr[Y_α {S_i, S_j}] = 0:** the SU(2)² – U(1) mixed trace vanishes on
  the LH-doublet surface because Tr_color[Y_α] = 3α + 1·(−3α) = 0. This
  is a structural consequence of the ratio +1 : (−3) and the fact that
  SU(2) acts diagonally on the color factor.
- **Tr[Y_α³] ≠ 0 on the LH-doublet surface only:** Expected; full anomaly
  cancellation requires the right-handed fermions, supplied by
  [`RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md`](RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md).

### 5. GUT Normalization (structural; α-independent ratio)

The GUT-normalized hypercharge satisfies Y_GUT = √(3/5) Y_SM. The ratio
Tr[Y_α²] / (multiplicity-weighted) is α² × 8/3; the GUT factor √(3/5)
is a structural consequence of the eigenvalue ratio +1 : (−3) and the
6 + 2 = 8 multiplicity split, independent of α. The squared-trace
arithmetic is now packaged as the standalone retained subtheorem
[`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md).

## Identification boundary (what is and isn't load-bearing)

The hypercharge identification is **not** an independent A_min input. It
follows from three structural ingredients on the LH-doublet surface, **none
of which is internally derived in this note** — each is chained to its own
authority:

| Chain element | Authority | Effective status |
|---|---|---|
| Eigenvalue ratio +1:(−3) on (Sym², Anti²) | [`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md) | bounded_theorem, audited_conditional (only on staggered-Dirac gate) |
| (Sym², Anti²) ↔ (SU(3)-fundamental, SU(3)-singlet) | [`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md) | positive_theorem (unaudited at time of this rewrite; chain target for parent atlas) |
| (color triplet ≡ quark, color singlet ≡ lepton) | SM-definition convention | admitted naming, not load-bearing physics |
| Absolute scale α = 1/3 (`Y(L_L) = −1`) | SM-convention normalization | admitted; LHCM repair item (2), still open |

The load-bearing step **of this note** is the chain assembly itself —
i.e., the statement that, jointly, these chains plus the admitted SM
convention reproduce the SM hypercharge pattern on the LH-doublet
surface. No internal renaming step remains in the load-bearing chain;
the runner verifies the structural ingredients (ratio, commutation,
chain-consequent charges, uniqueness, GUT trace) and explicitly labels
the matter-sector identifications as **chain consequents under the
LHCM matter assignment**, not as internal claims.

## Files

- [`scripts/frontier_hypercharge_identification.py`](../scripts/frontier_hypercharge_identification.py):
  Numerical verification of the chain. The runner is structured so each
  numerical block reports whether it verifies a structural fact (ratio,
  commutation, multiplicity) or a chain-consequent (matter-assignment
  labels, charges, anomaly traces). The matter-assignment labels are
  explicitly tagged as imported from the LHCM matter-assignment note.
- [`scripts/frontier_su3_commutant.py`](../scripts/frontier_su3_commutant.py):
  Prior result establishing the gl(3) ⊕ gl(1) commutant.
- [`scripts/frontier_lh_doublet_traceless_abelian_ratio.py`](../scripts/frontier_lh_doublet_traceless_abelian_ratio.py):
  Independent runner for the structural ratio theorem.
- [`scripts/frontier_lhcm_matter_assignment.py`](../scripts/frontier_lhcm_matter_assignment.py):
  Independent runner for the matter-assignment representation theorem.
