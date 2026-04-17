# Tetragonal Stabilizer and Residual μ–τ Invariance

## Date

2026-04-17

## Status

PROPOSED — symmetry-group theorem + verification runner.

## Summary

On the cubic lattice `Z³` with retained `O_h` point-group symmetry, the
stabilizer of the electroweak-symmetry-breaking (EWSB) axis-1 direction
`e_1 = (1, 0, 0)` is exactly the tetragonal group `D_{4h}`. This
stabilizer contains the reflection `σ_v(2↔3)` that swaps axes 2 and 3.

**Consequence.** Any retained operator that respects both `O_h` cubic
symmetry and EWSB axis-1 selection automatically commutes with
`σ_v(2↔3)` and therefore assigns **identical matrix elements to the
charged-lepton species pair (μ, τ)** on the retained generation-axis
basis of the `hw = 1` triplet.

The empirical pattern that no sole-axiom-native retained operator can
split the μ–τ degeneracy on the retained charged-lepton mass sector is
therefore a direct corollary of one symmetry-group identity,

```
Stab_{O_h}(e_1) = D_{4h},
σ_v(2↔3) ∈ D_{4h}.
```

## Background

The retained framework places the charged-lepton mass operator on the
`hw = 1` triplet of the cubic `Z³` taste orbit in the generation-axis
basis `{e_1, e_2, e_3}` (see `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
and `docs/DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md`). The
EWSB selector `V_sel = 32 Σ_{i<j} φ_i² φ_j²` has its stationary surface
at `φ = e_i` (any permutation); retained structure places charged
leptons on the branch `φ = e_1`, so axis 1 is singled out as the
charged-lepton mass axis.

On the retained second-order return

```
Σ = P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1},
```

the three `hw = 1` species connect through `Γ_1` hopping to the
intermediate states `O_0 = (0,0,0)` (reached from species 1),
`T_2(1,1,0)` (reached from species 2), and `T_2(1,0,1)` (reached from
species 3). A non-degenerate charged-lepton mass triple
`(m_e, m_μ, m_τ)` requires distinct effective propagator weights on
these three intermediate states; in particular, distinct weights on
the partner pair `(1,1,0)` and `(1,0,1)`.

Multiple independent attack lanes on the retained backbone have so far
failed to identify a sole-axiom-native operator that produces distinct
weights on that partner pair; see
`docs/CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md` for the
catalogue. This note supplies the symmetry-group explanation for why
that empirical pattern holds.

## Theorem

**Tetragonal Stabilizer Theorem.** Let `O_h` be the cubic point group
acting on `Z³` by signed permutations of coordinate axes, `|O_h| = 48`.
The stabilizer of the direction `e_1 = (1, 0, 0)` (as a set, modulo
sign) is the tetragonal group

```
Stab_{O_h}(e_1) = D_{4h},   |D_{4h}| = 16.
```

`D_{4h}` contains the reflection

```
σ_v(2↔3) : (x, y, z) ↦ (x, z, y),
```

which fixes axis 1 and swaps axes 2 and 3.

**Corollary (μ–τ invariance).** Any linear operator `M` on the retained
taste Hilbert space that commutes with every element of `D_{4h}`
satisfies

```
⟨(0,0,1) | M | (0,0,1)⟩ = ⟨(0,1,0) | M | (0,1,0)⟩    (T_1 species pair)
⟨(1,0,1) | M | (1,0,1)⟩ = ⟨(1,1,0) | M | (1,1,0)⟩    (T_2 partner pair)
```

so in particular the retained second-order return restricted to
`D_{4h}`-invariant intermediate propagators is structurally
`(m_e, m, m)`-degenerate: the muon and tau species are interchangeable.

**Falsifiability.** A retained operator `M` produces a non-degenerate
μ–τ mass splitting if and only if `M` does not commute with `σ_v(2↔3)`.
Any candidate primitive must therefore break `D_{4h}`, which requires
breaking at least one of:

- cubic `O_h` symmetry on the lattice, or
- EWSB axis-1 selection preservation.

## Proof

### Step 1: O_h as signed permutations of Z³

The cubic point group is realized as orthogonal matrices of the form
`Π · S`, where `Π` is a 3×3 permutation matrix and `S` is a diagonal
matrix with diagonal entries in `{±1}`. There are `3! = 6` permutations
and `2³ = 8` sign patterns, giving `|O_h| = 48`.

### Step 2: Stabilizer of e_1 has order 16

An element `g = Π · S` fixes the direction `e_1 = (1, 0, 0)` as a set
(i.e., `g e_1 = ± e_1`) iff `Π` fixes axis 1 as a set and `S` is
arbitrary, giving `|Stab_{O_h}(e_1)| = 2 · 2 · 2² = 16` (the first 2
is freedom to flip sign of axis 1; the second 2 is permutations of
{axis 2, axis 3}; the `2²` is signs on axes 2 and 3). By orbit-
stabilizer, `|O_h| / 3 axes = 48/3 = 16`, consistent.

The stabilizer is isomorphic to the tetragonal group `D_{4h}`, the full
symmetry group of a square with inversion.

### Step 3: σ_v(2↔3) is in the stabilizer

The matrix

```
σ_v(2↔3) = [ [1, 0, 0], [0, 0, 1], [0, 1, 0] ]
```

is a signed permutation in `O_h`: its permutation part swaps axes 2 and
3, and its sign pattern is `(+, +, +)`. It fixes `e_1` identically
(`σ_v e_1 = e_1`) so it is in `Stab_{O_h}(e_1) = D_{4h}`. Its action on
the retained taste orbit is:

```
(1,0,0) ↦ (1,0,0)    fixed
(0,1,0) ↦ (0,0,1)    swap (muon ↔ tau species axis)
(0,0,1) ↦ (0,1,0)    swap
(1,1,0) ↦ (1,0,1)    swap (Γ_1 intermediate partner pair)
(1,0,1) ↦ (1,1,0)    swap
(0,1,1) ↦ (0,1,1)    fixed
```

The `T_1` muon-species axis `(0,1,0)` and tau-species axis `(0,0,1)` are
interchanged by `σ_v`. Likewise the two `T_2` states that receive `Γ_1`
hops from the muon and tau axes respectively.

### Step 4: EWSB preserves σ_v(2↔3)

The retained EWSB selector

```
V_sel(φ) = 32 [ φ_1² φ_2² + φ_1² φ_3² + φ_2² φ_3² ]
```

is fully permutation-symmetric in `(φ_1, φ_2, φ_3)`. Under
`σ_v(2↔3) : (φ_1, φ_2, φ_3) ↦ (φ_1, φ_3, φ_2)`, each term is mapped to
another term (or itself), and the sum is unchanged. `V_sel(σ_v φ) =
V_sel(φ)` identically, and the EWSB vacuum `φ = e_1` is fixed as a set
by `σ_v`. EWSB does not break the reflection.

### Step 5: Corollary follows

If `M` commutes with every element of `D_{4h}`, then `M` commutes with
`σ_v(2↔3)`. For any pair of states `|α⟩, |β⟩` with `|β⟩ = σ_v |α⟩`:

```
⟨β | M | β⟩ = ⟨σ_v α | M | σ_v α⟩ = ⟨α | σ_v† M σ_v | α⟩ = ⟨α | M | α⟩.
```

Applied to the `T_1` muon-tau pair and the `T_2` partner pair, the
corollary follows.

## Novel Predictions

**P1 — Falsifiability test.** Any future retained primitive claimant
for charged-lepton μ–τ mass splitting must exhibit an explicit
`D_{4h}`-violating element. If none is present, the candidate is
structurally forbidden from producing `w_{(1,1,0)} ≠ w_{(1,0,1)}`, and
therefore cannot generate the observed `m_τ ≠ m_μ` hierarchy.

**P2 — Exhaustive class exclusion.** The following retained operator
classes all respect `D_{4h}` and therefore cannot split μ–τ:

- polynomials in the retained spatial Clifford generators `Γ_i`;
- operators built from `SU(2)_L` gauge dressing on the retained
  selected-axis surface;
- anomaly-forced `γ_5` or `Ξ_5` insertions;
- Higgs-VEV-only perturbations of `Γ_1` consistent with EWSB axis-1
  selection;
- Wilson or staggered lattice-improvement terms that respect the full
  cubic symmetry;
- retained emergent-Lorentz cubic harmonics that sit in the `A_{1g}`
  representation of the cubic group.

This predicts the outcome of previously-untested lanes (for instance
Wilson improvement, non-APBC temporal mixing) without needing to run
them explicitly: as long as they respect `D_{4h}`, they cannot close
the μ–τ gap sole-axiom-natively.

**P3 — Architectural corollary.** Closing the charged-lepton μ–τ mass
splitting from retained framework operators alone therefore requires
either extending the retained axioms with a `D_{4h}`-breaking primitive
or accepting an observational promotion for the μ–τ species distinction.
The latter is the path taken by the existing retained charged-lepton
closure note, which pins the mass triple observationally.

## Weakest Link

The argument assumes `σ_v(2↔3)` is a retained symmetry of the charged-
lepton mass sector. This requires:

- the `O_h` lattice automorphism group contains `σ_v` (evidently true,
  verified in the runner), and
- the EWSB selector does not individually break `σ_v` (verified
  explicitly: `V_sel` is permutation-symmetric).

No retained spontaneous `σ_v`-breaking mechanism has been identified on
main. If one is discovered, the theorem is void; the runner's Step 4
check becomes the falsifier.

## Verification Runner

Runner: `scripts/frontier_tetragonal_stabilizer_mu_tau_invariance.py`.

Checks:

1. Explicit construction of `O_h` as 48 signed-permutation matrices.
2. `|O_h| = 48`; closure under composition (spot check); orthogonality;
   `det ∈ {±1}`.
3. Stabilizer of `e_1` has order 16 (consistent with orbit-stabilizer
   `|O_h| / 3 = 16`), and is closed as a subgroup.
4. `σ_v(2↔3)` matrix is in the stabilizer; fixes `e_1`; swaps
   `e_2 ↔ e_3`; `σ_v² = I`; `det(σ_v) = -1`.
5. Action on the retained 8-state taste orbit: `(0,1,0) ↔ (0,0,1)`,
   `(1,1,0) ↔ (1,0,1)`, `(0,1,1)` fixed.
6. Generic `D_{4h}`-invariant diagonal operators (100 random trials)
   have `max |w_{(1,1,0)} - w_{(1,0,1)}| = 0` exactly.
7. Falsification sanity: explicitly asymmetric diagonal operators do
   *not* commute with `σ_v` and *do* produce
   `w_{(1,1,0)} ≠ w_{(1,0,1)}`.
8. `V_sel(φ) = V_sel(σ_v φ)` for 100 random `φ`, to machine precision.

Runner result: **18 THEOREM + 8 SUPPORT, 0 FAIL**.

## Relationship To Existing Retained Results

This theorem is orthogonal to the polynomial-invariants impossibility
result on the neutrino-sector Hermitian `H`
(`docs/G1_PHYSICIST_G_MICROSCOPIC_AXIOM_LEVEL_NOTE_2026-04-17.md`):
that result concerns trace-moment invariants of `H`; this theorem
concerns operator matrix elements on the charged-lepton `T_1` triplet.
One is about observables that cannot distinguish; the other is about
operators that cannot distinguish.

The empirical attack catalogue on the charged-lepton sector
(`docs/CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md`) exhausted
roughly a dozen candidate primitives. This theorem replaces the
exhaustion with a single symmetry argument and extends it to the full
infinite class of `D_{4h}`-invariant operators via one invariance test.

## What This Does And Does Not Claim

**Does claim.**

- The identity `Stab_{O_h}(e_1) = D_{4h}` holds on the cubic lattice.
- `σ_v(2↔3) ∈ D_{4h}`.
- Any `D_{4h}`-invariant operator forces
  `w_{(1,1,0)} = w_{(1,0,1)}`.
- The charged-lepton μ–τ mass splitting cannot arise from retained
  `D_{4h}`-invariant operators; a `D_{4h}`-breaking primitive is
  necessary.

**Does not claim.**

- Does not close the charged-lepton sole-axiom mass-hierarchy question.
- Does not contradict the existing observational-pin charged-lepton
  closure on the retained manuscript surface.
- Does not modify any retained axiom.
- Does not rule out `D_{4h}`-breaking extensions of the retained
  framework; the theorem identifies `D_{4h}`-breaking as necessary,
  not impossible.

## Next

The theorem gives a concrete checklist for any future primitive
candidate: exhibit the `D_{4h}`-breaking element explicitly. Without
it, the candidate is structurally ruled out regardless of its specific
form.
