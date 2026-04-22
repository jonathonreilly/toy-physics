# hw=1 Second-Order-Return Shape Theorem

**Date:** 2026-04-17
**Status:** exact structural theorem; publication-grade robustness certification
**Runners:**
- `scripts/frontier_hw1_second_order_return_shape_theorem.py` (20 PASS, 0 FAIL)
- `scripts/frontier_shape_theorem_robustness_audit.py` (57 PASS, 0 FAIL)

## Safe statement

On the retained `Cl(3) ⊗ chirality` carrier `C^{16}`, the second-order
effective operator on the `hw=1` generation triplet takes the exact
affine form
```
P_{T_1} Γ_1 (w_{O_0} P_{O_0}  +  w_a P_{(1,1,0)}  +  w_b P_{(1,0,1)}  +  w_c P_{(0,1,1)}) Γ_1 P_{T_1}
      =  diag(w_{O_0}, w_a, w_b)
```
on the generation axis basis of `T_1`, independent of the value of
`w_c`. The retained identity from the Dirac-bridge theorem (uniform
weight `w = 1`) gives the baseline `diag = I_3` (mass-degenerate
generations). Physical charged-lepton masses require three distinct
retained weights on the intermediate states.

## Retained inputs

- [DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md):
  canonical `Γ_1` definition; retained second-order identity
  `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} = I_3`.
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md):
  retained `hw=1` triplet with translation projectors and induced
  `C_3` cycle.

## Γ_1 hopping structure

`Γ_1 = σ_x ⊗ I ⊗ I ⊗ I` flips axis 1 of the spatial Clifford
coordinate `(a_1, a_2, a_3) ∈ {0, 1}^3`. Restricted to hops
`T_1 → {hw=0, hw=2}`:

| Generation | Species label | `Γ_1`-reached intermediate | Weight slot |
|---|---|---|---|
| 1 (electron) | `(1, 0, 0)` | `O_0 = (0, 0, 0)` | `w_{O_0}` |
| 2 (muon) | `(0, 1, 0)` | `T_2(1, 1, 0)` | `w_a` |
| 3 (tau) | `(0, 0, 1)` | `T_2(1, 0, 1)` | `w_b` |

The fourth `T_2` state `(0, 1, 1)` is not reachable from `T_1` by a
single `Γ_1` hop (it requires flipping either axis 2 or axis 3, which
`Γ_1` does not touch), so the weight `w_c` contributes identically
zero to the species diagonal.

## Theorem 2: shape theorem

**Theorem 2.** Under the construction above,
```
P_{T_1} Γ_1 W Γ_1 P_{T_1}  =  diag(w_{O_0}, w_a, w_b)
```
on the generation-species basis, where
`W = w_{O_0} P_{O_0} + w_a P_{(1,1,0)} + w_b P_{(1,0,1)} + w_c P_{(0,1,1)}`.
In particular:

1. The map `(w_{O_0}, w_a, w_b, w_c) ↦ diag(w_{O_0}, w_a, w_b)` is
   **affine** in the weight assignment.
2. `w_c` is **irrelevant** — it drops out identically.
3. The retained identity at uniform weight `w = 1` gives the baseline
   `diag = I_3` (mass-degenerate generations).

*Proof.* On the retained Cl(3) carrier, the four rank-1 intermediate
projectors commute pairwise and with `Γ_1·Γ_1`. Direct matrix
computation:
```
P_{T_1} Γ_1 P_{O_0} Γ_1 P_{T_1}     =  diag(1, 0, 0)
P_{T_1} Γ_1 P_{(1,1,0)} Γ_1 P_{T_1} =  diag(0, 1, 0)
P_{T_1} Γ_1 P_{(1,0,1)} Γ_1 P_{T_1} =  diag(0, 0, 1)
P_{T_1} Γ_1 P_{(0,1,1)} Γ_1 P_{T_1} =  diag(0, 0, 0)
```
Linearity in the weight assignment gives the shape-theorem
expression. □

## Theorem 2.1: robustness certification

The shape theorem passes seven independent stress tests on the
retained surface. All seven are exact symbolic verifications.

### Stress test 1 — alternative weak-axis choices

For each axis `i ∈ {1, 2, 3}`, the second-order return through
`Γ_i` has exactly one unreachable `T_2` state, namely the `T_2`
state that has zero in coordinate `i`. The map
`axis → unreachable-T_2` is an `S_3`-equivariant bijection under the
retained `S_3` symmetry of the cubic spatial lattice:
```
axis 1  →  T_2(0, 1, 1)  [unreachable]
axis 2  →  T_2(1, 0, 1)  [unreachable]
axis 3  →  T_2(1, 1, 0)  [unreachable]
```
The shape theorem survives unchanged under any axis choice; the
species-to-weight-slot mapping permutes `S_3`-equivariantly.

### Stress test 2 — O_3 contribution at higher order

At the retained second order, `O_3` does not appear. Check that at
fourth order `P_{T_1} (Γ_1 P_{not T_1} Γ_1)^n P_{T_1}` for
`n = 1, …, 4`, the contribution of `O_3` to the species-diagonal
vanishes at each `n`. `O_3` is doubly-suppressed: the single hop
`T_1 → O_3` is forbidden (`T_1` has Hamming weight 1 and `O_3` has
Hamming weight 3; `Γ_1` changes Hamming weight by ±1), so `O_3`
enters first at third order (`T_1 → T_2 → O_3`), and its
contribution to the fourth-order return through
`T_1 → T_2 → O_3 → T_2 → T_1` is `diag(0, 0, 0)`.

### Stress test 3 — L-taste vs R-taste

The retained `T_1` carrier is taste-doubled:
`dim(T_1) = 6 = 2 · 3` (two tastes × three species). The full
second-order return on the taste-doubled space is `I_6`; restricting
to either the L-taste or R-taste generation block gives
`diag(I_3)` identically. The shape theorem holds in both tastes.

### Stress test 4 — alternative intermediate-state splittings

Testing single-projector species diagonals for `P_{O_0}`,
`P_{(1,1,0)}`, `P_{(1,0,1)}`, `P_{(0,1,1)}`:
```
diag(P_{T_1} Γ_1 P_{X} Γ_1 P_{T_1})
```
is, respectively, `(1,0,0), (0,1,0), (0,0,1), (0,0,0)` — the
canonical basis of `ℝ^3` plus a null vector for the unreachable
state. Linearity in the weight assignment is exact.

### Stress test 5 — S_3 gauge representation

The retained native `Γ_i` operators are `S_3`-covariant under the
cubic spatial lattice symmetry. A Jordan-Wigner representation-level
artifact arises if one attempts naive bit-permutation Clifford
equivariance: under odd permutations, the Jordan-Wigner ordering
breaks `{U Γ_i U^†, γ_5} = 0`. This is a matrix-realization artifact
and does not affect the Hamming-weight projector structure the
shape theorem rests on. The `S_3`-covariant statement using native
`Γ_i` operators holds exactly.

### Stress test 6 — pre-EWSB M(φ) symmetry

Before EWSB axis selection, the retained Higgs family
`M(φ) = φ_1 Γ_1 + φ_2 Γ_2 + φ_3 Γ_3` acts on `C^{16}`. At each axis
point `e_i`, the shape theorem holds for `Γ_i`. The `S_3` symmetry
of the pre-EWSB configuration permutes the three axis points and
permutes the three shape theorems equivariantly. At generic `φ`
(not on an axis), `M(φ)² = |φ|² I`, and the second-order return on
species is `|φ|² I_3` — still species-diagonal, with the uniform
structure broken by subsequent axis selection.

### Stress test 7 — retained-surface logical derivability

The shape theorem is **logically implied** by the retained
Dirac-bridge theorem's PASS set plus linearity in the intermediate
projector. Specifically, the retained authority proves
```
P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1}  =  I_3.
```
Linearity in the intermediate projector plus the single-projector
identities from Stress test 4 gives the full shape theorem. Hence
the shape theorem is a **corollary** of the retained surface, not
an extension beyond it.

## Implication for charged-lepton masses

The shape theorem supplies exactly **three independent weight slots**
`(w_{O_0}, w_a, w_b)` on the retained `hw=1` generation space, with
a specific species-to-slot assignment dictated by the `Γ_1` hopping
structure. Physical charged-lepton mass hierarchy requires three
distinct weights; the retained surface supplies the shape but the
specific values are unfixed on the current retained authorities.

The question of whether retained operators on the intermediate
subspace `O_0 ⊕ T_2` can fix these three weights to match observed
charged-lepton masses is addressed by the three framework-derives
routes (Theorems 4, 5, 6 in
[HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md](./HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)),
all of which close negatively on the current retained surface.

## What this does not claim

- The shape theorem does NOT supply the three weight values. It only
  establishes the structural form.
- The identity baseline `diag = I_3` means the retained framework
  at uniform weight is mass-degenerate; charged-lepton hierarchy
  requires additional retained structure, not yet on `main`.
- The `T_2(0, 1, 1)` unreachability is a first-order statement. At
  higher orders in the `Γ_1` expansion, `T_2(0, 1, 1)` can be
  reached via `O_3` intermediate states; see Theorem 6 (signed
  ordering cancellation) for the analysis of fourth-order returns.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the second-order
> effective charged-lepton mass operator on the `hw=1` generation
> triplet has the exact affine form
> `diag(Σ(w)) = (w_{O_0}, w_a, w_b)`, where `(w_{O_0}, w_a, w_b)`
> are positive weights on the three reachable intermediate states
> `O_0, T_2(1, 1, 0), T_2(1, 0, 1)` respectively. The fourth `T_2`
> state `T_2(0, 1, 1)` is unreachable at this order. The shape
> theorem passes seven independent stress tests and is logically
> implied by the retained Dirac-bridge theorem plus linearity.

## Status

**REVIEW.**
