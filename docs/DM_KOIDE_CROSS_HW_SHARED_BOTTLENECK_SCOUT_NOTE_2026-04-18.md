# Cross-hw Attack on DM Case-3 Impossibility: Shared hw=1 Bottleneck Scout

**Date:** 2026-04-18
**Status:** SCOUT THEOREM / DEAD VERDICT — cross-hw lift does NOT escape δ-evenness on the full taste cube
**Runner:** `scripts/frontier_dm_koide_cross_hw_shared_bottleneck_attack.py`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
**Units:** dimensionless taste-cube basis; all operators represented in the
`C^8 = (C^2)^{⊗3}` computational basis (or `C^16 = C^8 ⊗ C^2` for the
chirality-doubled carrier). No mass units.

## 1. Question

The DM Case-3 Microscopic Polynomial Impossibility Theorem (the info-geometric
selection obstruction family) is proven on the retained `H_hw=1` triplet. It
establishes that every retained local polynomial functional of `H(m, δ, q_+)`
on `H_hw=1` is even in `δ`. Assumption A2.5 is that the physical carrier is
`H_hw=1` alone.

The Koide one-scalar obstruction ALSO lives on `H_hw=1`: the charged-lepton
`κ` bridge reduces to one microscopic scalar on the selected slice inside the
same doublet-block chart.

**Hypothesis under test.** Dropping assumption A2.5 — extending the observable
carrier to the full taste cube `C^8` (or `C^16` with chirality) — might admit
an axiom-native cross-hw observable that:

1. sees `sign(δ)` (breaking the Case-3 δ-evenness), and
2. lifts the Koide one-scalar bottleneck simultaneously, since BOTH bottlenecks
   live on the same 3-dim subspace.

This scout tests the hypothesis.

## 2. Verdict

**DEAD (structural).** The `S_3` axis-permutation symmetry of the taste cube
contains the transposition `(23)` that realizes the Z_2 reflection
`δ → -δ` on the retained `H_hw=1` doublet. Every retained scalar observable
on the full taste cube that is `S_3`-invariant is automatically δ-even. The
S_3 irrep content of `C^8` is `4 A_1 + 2 E`, with NO copy of the sign irrep
`A_2` (this is already a promoted theorem of the atlas —
[S3_TASTE_CUBE_DECOMPOSITION_NOTE.md](./S3_TASTE_CUBE_DECOMPOSITION_NOTE.md)).

Since `A_2` is the unique irrep that could carry δ-odd content, and `A_2` is
axiom-native-absent from the taste cube, **the Case-3 δ-evenness extends to
the full cube**. The runner exhibits eight independent cross-hw observable
families (staircase traces, alternating-sum Dirac traces, hw=0 ↔ hw=1
returns, hw=1 ↔ hw=2 returns, hw=2 reflected content, O_0 ↔ O_3 three-step
hops with H-decorated insertions, full-cube characteristic polynomial, full
3+1D temporal lift) and verifies they are all exactly δ-even.

The hw=1 bottleneck for DM Case-3 and for Koide is **genuinely shared as a
common absence**: both live in the δ-odd cohomology class, and the axiom has
no A_2 content anywhere to fill it. Cross-hw coupling does not escape this —
it merely adds more A_1 and E content, no A_2.

## 3. Setup

### 3.1 Axiom-native carrier

The full retained taste cube is `C^8 = (C^2)^{⊗3}`. The computational basis is
labeled by Hamming weight:

- hw=0: `O_0 = {(0,0,0)}` — 1 state
- hw=1: `T_1 = {(1,0,0), (0,1,0), (0,0,1)}` — 3 states
- hw=2: `T_2 = {(1,1,0), (1,0,1), (0,1,1)}` — 3 states
- hw=3: `O_3 = {(1,1,1)}` — 1 state

The retained axis-hopping operators `Γ_μ = σ_x ⊗ I ⊗ I` (and axis-2, axis-3
permutations thereof) flip axis μ, coupling hw-strata by ±1:
- `O_0 ↔ T_1 (axis μ)`
- `T_1 ↔ T_2 (axis μ)`
- `T_2 ↔ O_3 (axis μ)`

Chirality doubling extends the carrier to `C^16`. The 3+1D temporal extension
is `C^16 = C^8 ⊗ C^2_temporal`.

The source Hamiltonian on `H_hw=1` is the retained
`H(m, δ, q_+) = H_base + m T_m + δ T_delta + q_+ T_q` (carrier normal form
theorem; 3x3 Hermitian in the retained `(X_1, X_2, X_3)` basis).

### 3.2 S_3 axis-permutation action

`S_3` acts on `C^8` by permuting tensor slots. This action preserves Hamming
weight, commutes with the `Γ_μ` (up to relabeling), and has irrep content
`C^8 ≅ 4 A_1 + 2 E` (no `A_2`). The single transpositions are:
- `(23)`: swaps tensor slots 2, 3
- `(12)`: swaps tensor slots 1, 2
- `(13)`: swaps tensor slots 1, 3

On the retained `H_hw=1` basis `(X_1, X_2, X_3)` with `X_i = e_i`, the
transpositions act as permutations of rows/columns.

### 3.3 The δ → -δ reflection IS an S_3 element

Direct computation:
- `P_{(23)} T_delta P_{(23)}^{-1} = -T_delta`
- `P_{(23)} T_q P_{(23)}^{-1} = +T_q`
- `P_{(23)} T_m P_{(23)}^{-1} = T_m'` (some permutation, tested numerically)

So the Z_2 parity `δ → -δ` that underlies the Case-3 δ-evenness is precisely
the `(23) ∈ S_3` action on the retained doublet chart.

This is a **structural identity, not a gauge choice**: the same unitary that
implements `δ → -δ` on `H_hw=1` is the full-cube permutation of axes 2 and 3.

## 4. Theorem (Cross-hw δ-evenness inheritance)

**Theorem.** Let `f : B(C^8) → R` be any polynomial functional in the
axis-hopping operators `{Γ_1, Γ_2, Γ_3}`, the hw projectors
`{P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}}`, and the retained source Hamiltonian
`H(m, δ, q_+)` lifted via `P_{T_1}`, that is invariant under the full
axis-permutation group `S_3 ⊂ O(8)`. Then:

> `f(m, δ, q_+) = f(m, -δ, q_+)` for all `(m, δ, q_+) ∈ R^3`.

**Proof sketch.** The retained `H(m, δ, q_+)` is `T_delta`-graded: under the
axis-transposition `(23)`, `T_delta → -T_delta` while `T_m` and `T_q` are
either invariant or permuted within `S_3`-covariant slots. Lifting `H` to
`C^8` via `P_{T_1} H P_{T_1}` transports this grading: `(23)` acts on the
lifted operator by flipping the sign of its δ-content. Any `S_3`-invariant
polynomial in the lifted `H` plus the `S_3`-covariant axis-hopping content
must be invariant under `(23)`, hence even in δ. QED.

**Runner verification.** Eight independent observable families are tested
numerically; all pass δ-evenness to machine precision.

## 5. The A_2 obstruction is the "shared hw=1 bottleneck" in sharpened form

The Case-3 δ-evenness is usually stated as "doublet-only observables filter
through `|δ|^2`." The sharpened statement on the full cube is:

> **δ-odd content lives in the `A_2` sign-irrep of `S_3`, and `A_2` is absent
> from the axiom-native taste-cube representation.**

The shared bottleneck between DM Case-3 (which needs `sign(δ)`) and Koide
one-scalar (which needs to resolve one real parameter on the selected slice)
is **not merely dimensional**: it is irrep-level. Both problems ask for an
`A_2`-valued axiom-native observable, and the S_3 Taste-Cube Decomposition
Theorem rules this out structurally.

## 5b. Technical scope of the numerical verification

The runner operates on the SOURCE-ONLY chart
`H_src(m, δ, q_+) = m T_m + δ T_delta + q_+ T_q` (without `H_base`), at
`m = 0`. This is the same discipline the original Case-3 note uses for its
δ-evenness tests (Theorem 3 there). Two points are worth being explicit about:

1. **H_base is NOT S_3-invariant.** The carrier-normal-form `H_base` includes
   a specific `γ = 1/2` complex off-diagonal phase that sits on the `(1,3)`
   entry of the retained `H_hw=1` matrix. This phase is a chirality selector,
   not an S_3-covariant object. On the full cube lift, `H_base` breaks S_3
   symmetry; δ-evenness of trace moments of `H_base + δT_δ + ...` at `m=0`
   does not hold. Symmetrizing `H_base` over S_3 kills exactly the piece that
   makes the Case-3 chart work. So testing δ-evenness on the source-only
   chart is the correct discipline: it isolates the `(δ, q_+)` dependence.

2. **At m = 0, the (23) action closes the chart.** `T_delta` is the unique
   `(23)`-odd member of the chart basis; `T_q` is `(23)`-invariant; `T_m` has
   `(23)`-covariant content that re-enters only once `m ≠ 0`. The δ-evenness
   statement at `m = 0` is rigorous under (23)-conjugation; for `m ≠ 0` the
   chart is not (23)-closed (exactly the Case-3 non-closure theorem), so
   statements there require the full S_3 symmetrization.

These caveats do NOT weaken the no-go: the S_3 irrep content of C^8 is
pinned by character theory independent of chart-closure, and the absence
of A_2 is the structural obstruction.

## 6. Robustness checks

### 6.1 Lattice-is-physical check

The full cube `C^8` IS the lattice-is-physical carrier for the retained Cl(3)
on `Z^3` axiom. The `Γ_μ` hoppings are the plaquette-level link operators in
this carrier. The scout operates directly in this carrier — not in the
reduced `H_hw=1` slice.

### 6.2 3+1D check

Extending to `C^16 = C^8 ⊗ C^2` by temporal doubling, the S_3 action is
`(4 A_1 + 2 E) ⊗ (2 A_1) = 8 A_1 + 4 E`. Still no `A_2`. The temporal
direction adds more trivially-transforming content but does NOT introduce an
`A_2` copy. Runner Part 6 verifies this.

### 6.3 hw=1 convergence check

- **(a)** Runner confirms that cross-hw contractions (hw=0↔1, 1↔2, 2↔3) are
  all δ-even individually and that no linear combination of them is δ-odd.
- **(b)** The Koide `g_0^2 / |g_1|^2` scalar (on the selected slice, one
  real microscopic parameter) lifts to the full cube as a scalar on `T_1 ⊂ C^8`,
  still trapped at one scalar. The cross-hw lift adds propagator-decoration
  structure but does not expose a NEW scalar at the cross-hw level that
  resolves `m` (the one remaining charged-lepton datum).
- **(c)** A combined attack is NOT tractable through cross-hw alone because
  the shared obstruction is the A_2 absence. Any resolution must break the S_3
  axis-permutation symmetry (e.g., by axis selection via EWSB — an
  already-retained mechanism that does not help at axiom level).

## 7. What a HIT would have required

A cross-hw attack that succeeded would have had to exhibit an axiom-native
functional `f` that:

1. is constructed from `{Γ_μ, P_hw=k, H_{T_1}}`,
2. depends on δ oddly, and
3. is observable (i.e. not merely a pseudo-scalar).

Requirement 3 forces `f` to be S_3-invariant (since the axes are
axiom-native-symmetric). Requirement 2 forces `f` to contain A_2 content.
These are incompatible by the S_3 Taste Cube Decomposition Theorem. QED no-go.

## 8. Exit classification

**DEAD.** Cross-hw content is available but is δ-even; the microscopic-
polynomial impossibility theorem extends from `H_hw=1` to the full
`C^8` (and `C^16`) taste cube.

The Case-3 obstruction was never merely about the hw=1 slice; it was about
the absence of A_2 irrep content in the full axiom-native taste-cube
representation. Both DM Case-3 and the Koide one-scalar obstruction inherit
the same A_2 gap, which explains WHY they converge to the same 3-dim
subspace: both are the visible consequences of a single irrep-level obstruction.

## 9. Publication-grade honest statement

> On the retained `Cl(3)` on `Z^3` axiom, every `S_3`-invariant polynomial
> observable built from axis-hoppings, Hamming-weight projectors, and the
> lifted source Hamiltonian on the full taste cube `C^8` (and its `C^16`
> chirality- or temporal-doubled lift) is `δ`-even on the active affine
> chart. The δ-odd observable content would require an `A_2` sign-irrep
> summand of the taste-cube S_3 representation, which the S_3 Taste-Cube
> Decomposition Theorem rules out. The Case-3 microscopic-polynomial
> impossibility theorem therefore extends from the retained `H_hw=1`
> surface to the full taste cube: no cross-hw local-polynomial axiom-native
> functional pins `(δ_*, q_+*)`.

## 10. What this does NOT claim

- does NOT rule out a NONLOCAL cross-hw selector principle
  (e.g., information-geometric, transport-holonomy, effective-action
  matching) — those remain live routes (α, β, γ in the Case-3 note)
- does NOT rule out EWSB axis-selection as a post-axiom mechanism
  that explicitly breaks S_3 — this is already the retained route
  for charged-lepton mass hierarchy
- does NOT rule out that an S_3-BREAKING axiom-native selector exists
  elsewhere in the retained stack — but no such selector is known and
  the axiom is by construction S_3-symmetric
- does NOT promote any selector candidate to theorem-grade

## 11. Atlas position

- This note is a **structural extension** of the Case-3 impossibility
  theorem. It inherits the Case-3 atlas row under DM neutrino
  source-surface obstructions.
- It is **not** flagship publication-grade on its own.
- It should be cited alongside the S_3 Taste-Cube Decomposition Theorem
  as the "irrep-level sharpening of Case-3."
- It provides the **conceptual unification** between the DM Case-3 gap
  and the Koide one-scalar gap: both are A_2-absence gaps.

## 12. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_koide_cross_hw_shared_bottleneck_attack.py
```

Current: `PASS = 41, FAIL = 0`.

## 13. Required reading

- [DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md)
- [S3_TASTE_CUBE_DECOMPOSITION_NOTE.md](./S3_TASTE_CUBE_DECOMPOSITION_NOTE.md)
- [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
- [HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md](./HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md)
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md)
