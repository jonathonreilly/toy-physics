# Derivation: G5 Residual-S₂ Symmetry-Reduction Theorem

## Date

2026-04-17

## Status

PROPOSED — new theorem + verification runner. Forward science push on
the G5 charged-lepton sole-axiom open gate. Not a closure of G5 — it is
a structural explanation of WHY the 14-agent attack surface on `main`
failed to close sole-axiom, plus a concrete falsification test for any
future S₂-breaking candidate.

## Context

The G5 omnibus closure review on `main`
(`docs/G1_OMNIBUS_CLOSURE_REVIEW_NOTE_2026-04-17.md` and
`docs/CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md`) reports that 14
independent attack lanes have all failed to identify a retained sole-axiom
primitive breaking the residual `S₂` symmetry on axes `{2, 3}` after
EWSB axis-1 selection. Agent 12 explicitly lists 8 exhausted channels,
and Agent 10 v2 describes the structural-shape theorem showing that the
retained framework has the right diagonal slots but not the right
symmetry-breaking content.

This note supplies a **single clean symmetry-group argument** explaining
the architectural pattern: **any retained operator respecting `O_h` cubic
symmetry plus EWSB axis-1 selection automatically preserves `S₂` on
axes `{2, 3}`**, because the intersection of those two conditions is the
tetragonal group `D_{4h}`, which contains the `σ_v` reflection swapping
axes 2 and 3.

## Target Behavior

**Theorem (Residual-S₂).** Let `G_full = O_h` be the cubic point group
acting on the retained `Z^3` lattice, and let `V_sel` be the EWSB axis-1
selector that picks axis 1 as the charged-lepton mass axis. The
stabilizer of `V_sel` in `O_h` is exactly the tetragonal group `D_{4h}`:

```
Stab_{O_h}(V_sel at axis 1) = D_{4h}
```

and `D_{4h}` contains the reflection `σ_v(23)` swapping axes 2 and 3,
which generates an `S₂` subgroup.

**Corollary.** Any operator `M` on the retained framework that:

- respects `O_h` cubic symmetry on the lattice (retained),
- AND is compatible with EWSB axis-1 selection

automatically respects the residual `S₂` on axes `{2, 3}`. Therefore
`M` assigns identical scalar weights to the two `T_2` partner states
`(1, 1, 0)` and `(1, 0, 1)` on the `hw=1` triplet.

**Falsifiability.** Any putative G5 sole-axiom primitive must either
(a) break `O_h` cubic symmetry explicitly, or (b) break EWSB
axis-1-preservation explicitly. This is a concrete falsification test
for any candidate.

## Axioms Used

**A1.** `Cl(3)` on `Z^3` is the physical theory.

### Retained theorems reused

- **Cubic `O_h` symmetry of `Z^3`** — standard lattice symmetry of the
  retained cubic surface.
- **EWSB axis-1 selection** — from
  `docs/DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md`: on the
  `hw=1` triplet, `Γ_1` is diagonal in the generation axis basis,
  singling out axis 1.
- **Three-generation observable algebra on `hw=1`** — from
  `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`: exact rank-1
  projectors on the `T_1` sector.
- **S₂-preservation in Agent 10 v2** — the retained `Γ_1` second-order
  return has `(w_a, w_b)` structurally forced equal under residual S₂
  (empirically observed across 14 agents).

## Derivation

### Step 1: `O_h` action on `Z^3`

The full cubic point group `O_h` has order 48. It acts on `Z^3` by
permutations and sign flips of the three coordinate axes:

```
O_h = { (π, ε) : π ∈ S_3 permutes axes, ε ∈ {±1}^3 signs of axes,
        det (sign-flip action) arbitrary }
```

equivalently, `O_h ≅ S_3 ⋉ (Z_2)^3`. This is the full symmetry group of
the cubic lattice before any external structure is imposed.

### Step 2: EWSB picks axis 1 as the charged-lepton mass axis

On the retained `hw=1` triplet, the EWSB selector `V_sel = 32 Σ_{i<j} φ_i² φ_j²`
has a minimum at `φ = e_1` (or any permutation), and the retained
Dirac-bridge theorem places charged leptons on the `Γ_1`-coupled
direction in the axis basis. Consistently, the EWSB selector on axis 1
preserves the direction `e_1` and transforms the remaining axes
`{e_2, e_3}` among themselves.

### Step 3: Stabilizer of a single axis in `O_h`

The stabilizer of axis 1 (equivalently, the subgroup of `O_h` fixing the
direction `e_1` as a set, possibly flipping its sign) is

```
Stab_{O_h}(axis 1) = { g ∈ O_h : g · e_1 = ± e_1 } = D_{4h}
```

The tetragonal group `D_{4h}` has order 16 = 48/3, consistent with
orbit-stabilizer for the 3 axes.

`D_{4h}` is the full symmetry group of a square (with inversion), where
the "square" is the cross-section perpendicular to axis 1. It contains:

- rotations `C_4` around axis 1 (order 4)
- rotations `C_2` around axes 2 and 3 (order 2)
- mirror planes `σ_h` (perpendicular to axis 1) and `σ_v` (containing
  axis 1 and bisecting 2–3 plane)
- inversion `i`
- improper rotations `S_4` around axis 1

### Step 4: `σ_v` reflection swaps axes 2 and 3

The `σ_v` reflections in `D_{4h}` are the two mirror planes containing
axis 1 that pass through the diagonals of the 2–3 plane. The reflection
through the plane `y = z` (containing axis 1 and the diagonal of the
2–3 plane) acts as:

```
σ_v^(2↔3): (x, y, z) ↦ (x, z, y)
```

In particular:
- `e_2 = (0, 1, 0) ↦ (0, 0, 1) = e_3`
- `e_3 = (0, 0, 1) ↦ (0, 1, 0) = e_2`
- `(1, 1, 0) ↦ (1, 0, 1)`
- `(1, 0, 1) ↦ (1, 1, 0)`

This is the `S₂` action on axes `{2, 3}`.

### Step 5: Any `D_{4h}`-respecting operator has equal matrix elements on 2↔3

Let `M` be any operator acting on the retained framework that commutes
with every element of `D_{4h}`. Then in particular `M` commutes with
`σ_v^(2↔3)`, so for any pair of states `|ψ⟩, |φ⟩` related by `σ_v^(2↔3)`:

```
⟨ σ_v^(2↔3) ψ | M | σ_v^(2↔3) φ ⟩ = ⟨ ψ | M | φ ⟩
```

Applied to the `T_1` triplet: the species-2 state `|(0,1,0)⟩` and
species-3 state `|(0,0,1)⟩` are `σ_v^(2↔3)` partners, so

```
⟨ (0,0,1) | M | (0,0,1) ⟩ = ⟨ (0,1,0) | M | (0,1,0) ⟩
```

**Therefore any `D_{4h}`-respecting retained operator assigns the same
species-diagonal weight to species 2 and species 3 on the `T_1`
triplet.**

### Step 6: Same for `T_2` partner states

By the same argument, `σ_v^(2↔3)` swaps the `T_2` states `(1, 1, 0)`
and `(1, 0, 1)`. Any `D_{4h}`-respecting operator has equal matrix
elements between these partner states.

Applied to the retained `Γ_1` second-order return
`Σ = P_{T_1} Γ_1 P_{O_0 ⊕ T_2} Γ_1 P_{T_1}`, this forces `w_a = w_b`
for any `D_{4h}`-respecting choice of intermediate propagator.

### Step 7: Consequence — G5 sole-axiom requires `D_{4h}`-breaking

Closing G5 sole-axiom on the retained `Γ_1` second-order lane requires
producing `w_a ≠ w_b`. By Steps 5–6, this requires an operator that
does **not** commute with `σ_v^(2↔3) ∈ D_{4h}`. Equivalently, the
operator must break `D_{4h}` explicitly.

This gives a **concrete falsification test**: any retained G5 primitive
claimant must exhibit an explicit `D_{4h}`-violating element (either
`O_h` spatial-rotation-breaking, or EWSB axis-1-selection-breaking).

The retained framework's operators — built from the retained cubic
Clifford algebra `Cl(3)`, the retained `SU(2)` gauge generators, the
anomaly-forced `Γ_i` operators, and the EWSB Higgs mechanism — all
respect `O_h` cubic symmetry by construction, and are all compatible
with EWSB axis-1 selection. Therefore they all respect `D_{4h}`, and
therefore they all fail the G5 sole-axiom test. This matches the
14-agent empirical result exactly.

## Novel Prediction

**P1 (Falsifiability).** Any future candidate G5 sole-axiom primitive
must violate at least one of:

- cubic `O_h` symmetry on the lattice, or
- EWSB axis-1 selection preservation

If neither is violated, the candidate is structurally forbidden from
breaking `S₂` on axes `{2, 3}`, regardless of its specific form.

**P2 (Necessary direction for future attempts).** The following classes
of retained primitives are structurally incapable of breaking `S₂`:

- any polynomial in the retained `Γ_i` operators
- any operator built from `SU(2)_L` gauge dressing
- any anomaly-forced `Γ_5` or `Ξ_5` insertion
- any Higgs-VEV-only perturbation of `Γ_1`
- any Wilson or staggered improvement term respecting cubic symmetry
- any cubic-harmonic operator from the retained emergent-Lorentz lane
  that sits in an `O_h`-invariant irrep (`A_{1g}`)

To break `S₂`, a primitive must sit in an `O_h` irrep that has a
non-trivial component under `σ_v^(2↔3)`. The candidate irreps are
`E_g`, `T_{1g}`, `T_{2g}` at `ℓ = 4` (retained Lorentz-violation
signature), or non-identity `D_{4h}` irreps.

**P3 (Architecture).** G5 sole-axiom closure therefore requires either:

- extending the retained framework axioms with an `O_h`-breaking
  primitive (axiom modification), or
- accepting G5 as observational-pin-only (which is the current on-main
  closure via Agent 11).

This restates the Agent 12 `S2_BREAKING_PRIMITIVE_AMBIGUOUS` result as
a symmetry-group identity rather than an 8-channel exhaustion.

## Weakest Link

**Is `σ_v^(2↔3)` genuinely in the retained framework?** The `σ_v`
reflection is a combination of a cubic-group element (spatial) and
the EWSB axis-1 selection (internal). For the argument to apply, the
retained framework must actually carry this reflection as a retained
symmetry of the charged-lepton mass operator.

The answer is yes: the cubic `O_h` is the automorphism group of the
`Z^3` lattice (retained), and the EWSB selector on axis 1 stabilizes
`σ_v^(2↔3) ∈ O_h`. The composite is therefore a retained symmetry of
the post-EWSB charged-lepton sector, with no additional axiom input.

**Where the argument could fail**: if the EWSB selector actually breaks
`σ_v^(2↔3)` (which would require asymmetric coupling to axes 2 and 3),
then this theorem is void. Inspection of `V_sel = 32 Σ_{i<j} φ_i² φ_j²`
shows it is `S_3`-symmetric in `(φ_1, φ_2, φ_3)`, so its stationary
surface at `φ = e_1` preserves the `S_2(2↔3)` swap. The EWSB selector
does not break `σ_v^(2↔3)`.

## Relationship To The 14-Agent Attack Surface

This theorem does **not** close G5 sole-axiom. It formalizes the
architectural conclusion of the 14-agent exhaustion into a single
symmetry-group statement. Its value:

- replaces 14 independent empirical no-go results with one symmetry
  argument
- provides a concrete falsification test for any future candidate
  (check whether it violates `D_{4h}`)
- supplies the "why" for the empirical pattern the agents observed

It is orthogonal to the Physicist-G polynomial-invariants impossibility
theorem on G1: that theorem concerns trace-moment invariants of `H`;
this theorem concerns operator matrix elements on the `T_1` triplet.
Physicist-G is about what observables cannot distinguish; this theorem
is about what operators cannot distinguish.

## Runner Design

**Target:** `scripts/frontier_g5_s2_residual_symmetry_theorem.py`.

**Checks:**

1. Construct the cubic point group `O_h` explicitly as 48 orthogonal
   3×3 matrices (signed permutations with arbitrary sign pattern).
2. Verify `|O_h| = 48`.
3. Compute the stabilizer of the vector `e_1 = (1, 0, 0)` in `O_h` and
   verify its order is 16 (`= D_{4h}`).
4. Explicitly find `σ_v^(2↔3)` in the stabilizer and verify it fixes
   axis 1 and swaps axes 2 and 3.
5. For each pair of `σ_v^(2↔3)`-related states on the retained `Z^3`
   taste orbit, verify the partner mapping:
   - `(0, 1, 0) ↔ (0, 0, 1)` (T_1 species pair)
   - `(1, 1, 0) ↔ (1, 0, 1)` (T_2 intermediate pair)
   - `(0, 1, 1)` is fixed (self-partner)
6. Build a generic `D_{4h}`-invariant operator as an explicit matrix on
   the 8-state taste orbit, and verify it produces identical matrix
   elements on the S₂ partner pairs.
7. Cross-check: construct an operator that EXPLICITLY breaks
   `σ_v^(2↔3)` (e.g., asymmetric hopping) and verify it CAN produce
   `w_a ≠ w_b`. This is the falsification test.

## Status Ledger

| Artifact | Status |
|---|---|
| This note | PROPOSED |
| Verification runner | pending (this turn) |
