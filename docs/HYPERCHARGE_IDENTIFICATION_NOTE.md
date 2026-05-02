# Hypercharge U(1)_Y Identification from the Commutant

**Status:** support: structural identification of the unique traceless commutant U(1) generator with Standard Model hypercharge within A_min; audit_status=audited_renaming. This note is an identification (a labelling step matching commutant-algebra eigenvalues to Standard Model hypercharge labels), not a first-principles derivation of Standard Model hypercharge.

**Type:** bounded_theorem (proposed; audit-lane to ratify)

**Claim scope:** bounded left-handed-doublet identification: in C^8 with SU(2)_weak on factor 1 and SWAP_23 on factors 2 and 3, the unique traceless commutant U(1) has eigenvalue ratio 1:(-3) and, after identifying the (2,3) and (2,1) sectors as Q_L and L_L with conventional normalization a=1/3, reproduces their SM hypercharges Y(Q_L)=+1/3 and Y(L_L)=-1 and the corresponding electric charges via Q = T_3 + Y/2. The renaming step (matching abstract eigenspaces to SM left-handed fermion labels) is in the load-bearing chain and is recorded by the audit lane as audited_renaming. The structural ratio 1:(-3) and the no-nu_R RH derivation are NOT in this row's load-bearing chain - they live in the sibling theorems listed under "Audit boundary".

**Primary runner:** [`scripts/frontier_hypercharge_identification.py`](../scripts/frontier_hypercharge_identification.py) (PASS=9 on retained-grade structural-algebra checks per archived 2026-05-02 audit)

## Audit boundary

This note identifies the unique traceless U(1) direction in the
commutant algebra `su(3) + u(1)` of `{SU(2)_weak, SWAP_23}` within
A_min.

The identified Standard Model construct is hypercharge on the
left-handed doublet surface, with the conventional normalization shown
below.

This note does **not** claim to derive the numerical hypercharge
normalization from first principles, to derive the existence of the
Standard Model hypercharge construct independent of this identification,
or to complete the full anomaly-canceling Standard Model spectrum.

Audit history: the audit lane records `audit_status=audited_renaming`
for `hypercharge_identification_note`, cross-confirmed as class F by
`codex-audit-loop-round-2` and
`codex-fresh-context-20260430-03-hypercharge`. The renaming verdict is
the honest scope of this note. Two sibling theorems package the
substantive structural and anomaly-derived content separately and are
NOT load-bearing on this renaming row:

- `LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`
  (effective_status `retained` as of 2026-05-02): retains the structural
  eigenvalue ratio `1 : (-3)` on the Sym^2 (6-state) and Anti^2 (2-state)
  decompositions of the LH-doublet sector, with no SM-identification
  step in its load-bearing chain.
- `SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md`
  (positive_theorem, awaiting independent audit): derives the SM
  right-handed hypercharges `(y_1, y_2, y_3) = (+4/3, -2/3, -2)` from
  anomaly cancellation alone on the no-nu_R minimal completion, with
  NO load-bearing dependency on this identification note.

Consumers of "the LH-sector hypercharges are `+1/3` and `-1`" should
prefer the structural-ratio sibling for the ratio and use this note
only for the conventional renaming step. Downstream rows that take
literal `Y(Q_L) = +1/3` and `Y(L_L) = -1` as inputs (notably
`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md` and
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`)
inherit the renaming via this note; the no-nu_R sibling above provides
a parallel chain that does not require this note as an input.

## Statement

**Identification.** The unique traceless U(1) direction in the commutant algebra
su(3) + u(1) of {SU(2)\_weak, SWAP\_{23}} in End(C^8) matches the Standard
Model hypercharge assignments on the left-handed doublet surface.

## Setup

The taste space C^8 = (C^2)^{x3} carries two structures:

1. **SU(2)\_weak**: S\_i = sigma\_i/2 on factor 1, derived from the bipartite
   lattice structure.
2. **SWAP\_{23}**: exchanges tensor factors 2 and 3, from the Z\_2 spatial
   permutation symmetry.

The commutant of {SU(2), SWAP\_{23}} in End(C^8) is gl(3,C) + gl(1,C),
established in `frontier_graph_first_su3_integration.py`. The mechanism:

- SU(2) on factor 1 restricts the commutant to gl(4,C) on factors 2,3
  (by Schur's lemma).
- SWAP\_{23} decomposes C^4 = C^2 x C^2 into Sym^2(C^2) = C^3 and
  Anti^2(C^2) = C^1.
- gl(4) restricted to this decomposition = gl(3) + gl(1).
- Compact + traceless form: su(3) + u(1).

## The U(1) Generator

The commutant gl(3) + gl(1) contains two independent U(1) generators:

- P\_sym: the projector onto Sym^2(C^2) (center of gl(3))
- P\_anti: the projector onto Anti^2(C^2) (the gl(1))

General U(1): Y(a,b) = a P\_sym + b P\_anti, embedded in C^8 as I\_2 x Y.

Eigenvalues on C^8: a (x6 quark states), b (x2 lepton states).

**Tracelessness condition** (removing the trivial overall phase):

    6a + 2b = 0  =>  b = -3a

This leaves a unique traceless generator (up to normalization):

    Y = a (P_sym - 3 P_anti)

## Structural check: matching the hypercharge pattern

### 1. Eigenvalue Matching

With conventional normalization a = 1/3:

| Subspace | Multiplicity | Y value | SM identification |
|----------|-------------|---------|-------------------|
| (2,3) = C^2 x Sym^2(C^2) | 6 | +1/3 | Left-handed quark doublet |
| (2,1) = C^2 x Anti^2(C^2) | 2 | -1 | Left-handed lepton doublet |

These match the Standard Model hypercharge values on the left-handed
doublet surface:
- Q\_L = (u\_L, d\_L): Y = +1/3
- L\_L = (nu\_L, e\_L): Y = -1

### 2. Electric Charge

With T\_3 = sigma\_3/2 on the weak factor and Q = T\_3 + Y/2:

| Particle | T\_3 | Y | Q = T\_3 + Y/2 |
|----------|------|---|----------------|
| u\_L (3 colors) | +1/2 | +1/3 | +2/3 |
| d\_L (3 colors) | -1/2 | +1/3 | -1/3 |
| nu\_L | +1/2 | -1 | 0 |
| e\_L | -1/2 | -1 | -1 |

Under this identification, all listed charges match the Standard Model
pattern exactly.

### 3. Uniqueness

The argument is purely algebraic:

1. The commutant contains a 2-dimensional space of U(1) generators
   (center of u(3), plus the explicit u(1)).
2. The tracelessness condition imposes one linear constraint.
3. This reduces the space to **dimension 1** -- a unique generator up to
   normalization.
4. That unique generator has eigenvalue ratio 1:(-3) on (2,3) vs (2,1).
5. This matches hypercharge on the left-handed doublet surface.

### 4. Consistency Checks on the Left-Handed Surface

For the 8 left-handed states:

- **Tr[Y] = 0**: 6(1/3) + 2(-1) = 0. The traceless direction removes the
  overall phase.
- **Tr[Y {S\_i, S\_j}] = 0**: The SU(2)^2-U(1) mixed trace vanishes on this
  left-handed surface because Tr\_color[Y] = 3(1/3) + 1(-1) = 0.
- **Tr[Y^3] != 0**: Expected on a left-handed-only surface. Full anomaly
  cancellation requires the right-handed fermions as well.

### 5. GUT Normalization

The GUT-normalized hypercharge Y\_GUT = sqrt(3/5) Y\_SM. The ratio
Tr[Y^2] = 8/3 and Tr[T\_a^2]\_SU(3) = 1 are consistent with the standard
SU(5) embedding.
This squared-trace arithmetic is now packaged as the standalone retained
subtheorem
`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`.

## Identification boundary

The hypercharge identification is not added as an independent A_min
input. It follows from three structural ingredients on the left-handed
surface:

1. C^8 = (C^2)^{x3} (taste space from the staggered lattice)
2. SU(2)\_weak on factor 1 (from bipartite structure)
3. SWAP\_{23} symmetry (from spatial permutation)

Within this setup, the commutant algebra isolates su(3) + u(1), and the
traceless U(1) generator is **unique up to normalization**. The audit
status records the final step as an identification with hypercharge, not
a first-principles derivation of hypercharge itself.

The structural part of this argument (the existence and uniqueness of
the traceless direction, and the eigenvalue ratio `1 : (-3)` on
Sym^2(C^2) vs Anti^2(C^2)) is now packaged separately as the
retained-grade narrow theorem
`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`.
The remaining content of this note - calling the conventional choice
`a = 1/3` the Standard Model normalization and labelling
`Y(Q_L) = +1/3` and `Y(L_L) = -1` - is the renaming step that the
audit lane records as `audited_renaming`.

## Files

- `scripts/frontier_hypercharge_identification.py`: Full numerical verification of the renaming step (primary runner for this row).
- `scripts/frontier_graph_first_su3_integration.py`: Prior result establishing the gl(3) + gl(1) commutant.
- `scripts/frontier_lh_doublet_traceless_abelian_ratio.py`: Retained-grade
  structural ratio theorem (`1 : (-3)`) on the LH-doublet sector,
  independent of the SM-identification step.
- `scripts/frontier_sm_hypercharge_no_nu_r_derivation.py`: SM RH
  hypercharges `(+4/3, -2/3, -2)` from anomaly cancellation alone on
  the no-nu_R completion, decoupled from this renaming.
