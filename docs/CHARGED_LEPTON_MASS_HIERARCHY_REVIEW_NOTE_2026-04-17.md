# Charged-Lepton Mass Hierarchy and Koide's Relation on the Cl(3)/Z^3 Framework

**Date:** 2026-04-17
**Status:** bounded review note — the proposed_retained framework does not derive Koide on the current surface; the charged-lepton hierarchy is accommodated only through an explicit observational pin.
**Runners:** 19 runners, 518 PASS / 0 FAIL, independently verified on `origin/main`.

**Repo addendum (2026-04-18):** a reviewed follow-on support stack now lives on
current `main` via
[CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md](./CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md).
It closes the April 18 candidate route down to one microscopic scalar selector
law, but it does **not** change the authoritative status of this note: the
charged-lepton package remains bounded observational-pin compatibility rather
than a retained Koide derivation.

## Abstract

On the retained `Cl(3)/Z^3` framework, we investigate whether the charged-lepton mass hierarchy and Koide's relation

```
Q  ≡  (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²  =  2/3
```

admit a retained-theorem derivation. The retained framework is
**structurally compatible** with Koide `Q = 2/3` through an exact algebraic
equivalence on the `hw=1` triplet, and the three-generation
mass-square-root vector is accommodated by a retained second-order-return
shape theorem that supplies exactly three independent weight slots. The
retained framework does **not** uniquely predict Koide. All nineteen
natural attack routes — six structural no-gos, three framework-derives
lanes, and the observational-pin closure — establish that cone-forcing
requires either (a) an explicit observational pin, or (b) a new retained
primitive not currently on `main`. Three such primitives are sharply named:
non-Cl(3)-covariant retained lift of the intermediate propagator,
real-irrep-block democracy in variational weighting, and a mechanism
breaking within-multiset signed Clifford ordering cancellation at
fourth order.

The charged-lepton sector therefore enters the repo as a **bounded**
package. The 3→3 observational pin produces no genuinely new numerical
forecast, unlike the 3→4 neutrino-mixing map which produces
`δ_CP ≈ −81°` as a retained forecast.

## 1. Retained foundations

We work on the retained `Cl(3)/Z^3` framework surface. The following
retained authorities are used without modification:

- **Three-generation observable theorem** —
  [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md).
  The retained `hw=1` triplet
  `T_1 = span{X_1, X_2, X_3}` carries the full matrix algebra
  `M_3(ℂ)` through translation projectors `{P_1, P_2, P_3}` and the
  induced `C_{3[111]}` cycle.

- **Observable principle from axiom** —
  [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md).
  The unique additive CPT-even scalar generator on the retained
  lattice is `W[J] = log|det(D+J)| − log|det D|`, with local
  source-response curvature
  `K_{xy} = −Re Tr[(D+J)^{−1} P_x (D+J)^{−1} P_y]`.

- **Anomaly-forced Dirac bridge theorem** —
  [DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md).
  On the retained `Cl(3) ⊗ chirality` carrier `C^{16}`, the
  post-EWSB charged-lepton Dirac operator reduces to the weak-axis-1
  element `Γ_1` of the spatial Clifford family
  `M(φ) = φ_1 Γ_1 + φ_2 Γ_2 + φ_3 Γ_3`. On the `hw=1` triplet,
  `Γ_1` is diagonal in the generation axis basis and the
  second-order return is retained as
  ```
  P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1}  =  I_3.
  ```
  Charged-lepton masses are the diagonal entries of the effective
  operator in the axis basis (`U_e = I_3`).

- **Anomaly-forced 3+1 closure** —
  [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md).
  Retained 3+1 carrier on which the APBC Matsubara construction is
  defined.

- **Electroweak hierarchy theorem** — retained
  `v = 246.282818 GeV` from the same-surface plaquette chain.

All numerical constants used in this review are framework-native
retained values; PDG charged-lepton masses appear ONLY as comparators
or as the three-real observational pin in Theorem 7.

## 2. Theorem 1: algebraic Koide-cone equivalence

Let `v = (√m_e, √m_μ, √m_τ) ∈ ℝ^3_+` be the mass-square-root vector on
the retained `hw=1` triplet. Let
```
v = a_0 e_+  +  z e_ω  +  z̄ e_{ω²}
```
be the `C_3` character decomposition, where
`e_+ = (1, 1, 1)/√3` spans the trivial character and
`e_ω = (1, ω, ω²)/√3`, `e_{ω²} = (1, ω², ω)/√3` span the
two-dimensional nontrivial-character subspace.

**Theorem 1.** Koide's relation is the equal-character-weight
condition:
```
Q = (Σ m_i) / (Σ √m_i)² = 2/3       ⟺       a_0² = 2 |z|².
```
The equivalence is exact on the `hw=1` triplet, independent of the
specific values of `m_i`.

*Proof.* Plancherel on `C_3` gives
`|v|² = a_0² + 2|z|²` and `(Σ v_i)² = 3 a_0²`. Substituting:
```
Q  =  Σ v_i² / (Σ v_i)²  =  (a_0² + 2|z|²) / (3 a_0²).
```
Setting `Q = 2/3` and clearing denominators yields `a_0² = 2|z|²`. □

**Geometric reading.** Koide's `Q = 2/3` is the "45° condition" on `v`
relative to the diagonal `(1, 1, 1)`: `v` lies at equal norm on the
trivial-character subspace and on the two-dimensional nontrivial-
character subspace.

The full derivation chain from hypothesis to Theorem 1 is in
[CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md](./CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md).

Runner: `scripts/frontier_charged_lepton_observable_curvature.py`.

## 3. Theorem 2: second-order-return shape theorem

**Theorem 2** (shape theorem). On the retained `Cl(3) ⊗ chirality`
carrier `C^{16}`, let `P_{T_1}` be the `hw=1` generation-triplet
projector, let
`Γ_1` be the retained weak-axis Clifford generator, and let the
intermediate projector on the `hw = 0, 2` subspace be weighted by
positive weights
`w = (w_{O_0}, w_a, w_b, w_c)` on the states
`{O_0, T_2(1,1,0), T_2(1,0,1), T_2(0,1,1)}` respectively.

Then
```
P_{T_1} Γ_1  (w_{O_0} P_{O_0}  +  w_a P_{(1,1,0)}  +  w_b P_{(1,0,1)}  +  w_c P_{(0,1,1)})  Γ_1 P_{T_1}
    =  diag(w_{O_0}, w_a, w_b)
```
on the generation axis basis of `T_1`. The fourth weight `w_c` is
identically irrelevant: the state `T_2(0,1,1)` is unreachable from
`T_1` via one `Γ_1` hop.

The retained identity from the Dirac-bridge theorem corresponds to
uniform weight `w = (1, 1, 1, 1)`, giving `diag = I_3` — the three
generations are mass-degenerate at this retained order. Physical
charged-lepton masses therefore require three distinct weights on the
intermediate states.

**Γ_1 hopping structure.**

| Generation | Species | Γ_1-reached intermediate | Weight slot |
|---|---|---|---|
| 1 (electron) | `(1, 0, 0)` | `O_0 = (0, 0, 0)` | `w_{O_0}` |
| 2 (muon)     | `(0, 1, 0)` | `T_2(1, 1, 0)`       | `w_a` |
| 3 (tau)      | `(0, 0, 1)` | `T_2(1, 0, 1)`       | `w_b` |

**Robustness (Theorem 2.1).** The shape theorem passes seven
independent stress tests on the retained surface:

1. alternative weak-axis choices give an `S_3`-equivariant bijection
   of unreachable `T_2` states (each axis has exactly one unreachable
   `T_2` state, namely the `T_2` state with zero in that axis);
2. inclusion of `O_3` at fourth order contributes zero to the
   species-diagonal at all `n = 1…4`;
3. `L`-taste and `R`-taste give identical species block `= I_3`;
4. alternative intermediate-state splittings produce single-projector
   species diagonals linear and exact in the weight assignment;
5. native-`Γ_i` `S_3` covariance holds exactly (a Jordan-Wigner
   representation-level artifact is isolated and shown not to affect
   the Hamming-weight projector structure);
6. pre-EWSB `M(φ)` symmetry: each axis selection has its own shape
   theorem;
7. the shape theorem is logically implied by the retained
   Dirac-bridge PASS set plus linearity in the intermediate
   projector — it is a corollary of the retained surface, not an
   extension beyond it.

Full proof and stress-test details:
[HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md](./HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md).

Runners:
- `scripts/frontier_hw1_second_order_return_shape_theorem.py`
- `scripts/frontier_shape_theorem_robustness_audit.py`

## 4. Theorem 3: mass and mixing subspace disjointness

On the retained `hw=1` three-generation Hermitian algebra `M_3(ℂ)`, define:

- `V_H ≡ span{T_m, T_δ, T_q}` — the tangent space of the retained
  neutrino-mixing affine chart. The generators carry permutation and
  off-diagonal structure (axis-2↔axis-3 swap; axis-antisymmetric and
  axis-symmetric off-diagonal components).
- `V_D ≡ span{D_1, D_2, D_3}` — the species-diagonal subspace,
  spanned by the three rank-1 generation projectors.

Both subspaces have real dimension 3 inside the 9-real-dimensional
Hermitian `M_3(ℂ)`.

**Theorem 3.** `rank(V_H + V_D) = 6`, hence
```
dim(V_H ∩ V_D)  =  rank(V_H) + rank(V_D) − rank(V_H + V_D)  =  3 + 3 − 6  =  0.
```
`V_H` and `V_D` are **disjoint** subspaces (trivial intersection /
direct sum as ℝ-vector spaces) of the retained `hw=1` Hermitian
algebra. No linear combination of the neutrino-mixing tangent
generators lies in the species-diagonal subspace. Disjointness is
the strictly weaker, metric-free statement; the stronger claim of
orthogonality under a specific Hermitian inner product is NOT
established by the runner and is NOT used downstream. See
[MASS_MIXING_SUBSPACE_DISJOINTNESS_THEOREM_NOTE.md](./MASS_MIXING_SUBSPACE_DISJOINTNESS_THEOREM_NOTE.md)
§Safe statement for the disjoint-vs-orthogonal scope note.

**Corollary.** Charged-lepton mass eigenvalues (which live in `V_D` by
the Dirac-bridge theorem's `U_e = I_3` constraint) cannot be expressed
as linear combinations of neutrino-mixing sources. The charged-lepton
mass hierarchy is not derivable as a corollary of the retained
neutrino-mixing closure; each sector requires its own observational
pin when carried as a bounded package.

**Architectural reading.** The retained `M_3(ℂ)` decomposes as
```
M_3(ℂ)_Hermitian  =  V_H  ⊕  V_D  ⊕  (residual 3-real subspace).
```
The neutrino-mixing closure pins `V_H` via observed PMNS angles; the
charged-lepton closure pins `V_D` via observed charged-lepton masses;
the two are structurally independent and together span 6 of the 9
real dimensions of the retained Hermitian algebra.

Full details:
[MASS_MIXING_SUBSPACE_DISJOINTNESS_THEOREM_NOTE.md](./MASS_MIXING_SUBSPACE_DISJOINTNESS_THEOREM_NOTE.md).

Runners:
- `scripts/frontier_mass_mixing_disjointness_theorem.py`
- `scripts/frontier_charged_lepton_via_neutrino_hermitian.py`

## 5. Structural no-go survey

We establish six rigorous no-go theorems ruling out retained
mechanisms for forcing the mass-square-root vector onto the Koide
cone `a_0² = 2|z|²` without observational pinning. Each is
established by explicit symbolic construction or counterexample.
Full statements, proofs, and numerical verifications are in
[STRUCTURAL_NO_GO_SURVEY_NOTE.md](./STRUCTURAL_NO_GO_SURVEY_NOTE.md).

### 5.1 Z_3 invariance alone is insufficient

The `Z_3`-invariant bilinear source-response kernel with canonical
left/right charges `(0, +1, −1) / (0, −1, +1)` on the `hw=1` triplet
evaluates to `S = I_3` (triply-degenerate). Any nonzero real
3-vector is an eigenvector of `S`; `Z_3` invariance alone forces no
unique direction. The algebraic-permissiveness null is closed.

Runner: `scripts/frontier_charged_lepton_z3_source_response_crosscheck.py`.

### 5.2 Pure-APBC temporal refinement is insufficient at any `L_t`

The off-diagonal source-response curvature `b = K_{ij}` for `i ≠ j`
vanishes on every pure-APBC `L_t ∈ {4, 6, 8, 12, 16, 24, ∞}`:
```
K_{ij}(L_t)  =  0    for i ≠ j, on every pure-APBC block.
```
*Proof.* The three `hw=1` species carry pairwise-orthogonal joint
translation characters
`(−1, +1, +1), (+1, −1, +1), (+1, +1, −1)`.
Pure-APBC `D` commutes with each `T_k`, so `(D+J)^{−1}` does whenever
`J` is species-diagonal, and `P_i · (D+J)^{−1} · P_j` carries no
cross-character matrix element. The bulk limit `c_eff(L_t) → 2√3`
corrects the naive bulk value 3. The pure-APBC lane is permanently
closed as an attack route.

Runner: `scripts/frontier_charged_lepton_curvature_apbc_extension.py`.

### 5.3 Observable-principle character symmetry does not force equal
eigenvalues

The unique-generator + additivity + CPT-even requirements on
`W[J] = log|det(D+J)|` do **not** force the curvature eigenvalues
`α` (on the trivial `C_3` character subspace) and `β` (on the
nontrivial subspace) to coincide on `hw=1` blocks with nonzero
cross-species propagator. Three independent tactics
(direct symbolic Legendre transform; Schur's lemma on `C_3` irreps;
independent-subsystem additivity chain) each exhibit explicit
symbolic counterexamples with `α ≠ β`. The reach of the retained
observable-principle authority does not extend to Koide-cone forcing.

Runner: `scripts/frontier_observable_principle_character_symmetry.py`.

### 5.4 SU(2)_L gauge exchange cannot generate cross-species mixing

**Theorem (taste-species carrier orthogonality).** The retained
native `SU(2)_L` generators `S^a` live in the taste `Cl(3)` subalgebra,
while the `hw=1` species label is the translation-character BZ-corner
label. On the retained physical surface,
`ρ_{hw=1}(S^a) = I_species` for all `a`. Every `SU(2)_L`-dressed
operator at any order in `g_2` therefore commutes with the rank-1
species projectors and cannot generate cross-species matrix elements.
Color dressing on quarks multiplies only the diagonal parameter.

Runner: `scripts/frontier_koide_su2_gauge_exchange_mixing.py`.

### 5.5 Anomaly-forced 3+1 structure is species-blind on hw=1

Every retained anomaly-forced ingredient on the Standard Model branch
— `γ_5`, the right-handed singlet completion (species-uniform `Y` per
sector), the five vanishing anomaly traces, the chirality-forcing
Dirac mass bilinear (requires Higgs VEV, pushed to observational-pin
regime), and the chirality projectors — acts as a scalar on the
`hw=1` species label. Tested on `L_t ∈ {6, 8, 12, 16}`.
Within-sector cross-species mixing is impossible from the retained
anomaly structure alone. The sector-scale signal from `Tr[Y^3]`
distinguishes leptons from quarks across sectors but is species-blind
within a sector.

Runner: `scripts/frontier_koide_anomaly_forced_cross_species.py`.

### 5.6 Sectoral universality of Koide `Q = 2/3` is falsified

On the current framework + PDG surface:
- `Q_ℓ` (charged leptons, PDG pole) = `0.66666` (matches `2/3` to PDG precision).
- `Q_d` (down-type quarks, framework-native `α_s(v) + 5/6` bridge) = `0.73058` (`+9.59%`).
- `Q_u` (up-type quarks, PDG self-scale) = `0.84884` (`+27.33%`).

Common-scale running does not close the up-type gap; the minimum
scheme rescaling of `√m_t` to force `Q_u = 2/3` requires an effective
`m_t ≈ 19.9 GeV`, not derivable from any retained theorem. The exact
retained SU(3) Casimir identity
`(C_F − T_F)^{−1/4} = (6/5)^{1/4}` reproduces
`Q_d / Q_ℓ = √(6/5)` to `0.04%` precision if deployed as a down-type
`hw=1` spectral-amplitude dressing, but the retained `hw=1` algebra
carries no species-dependent color-adjoint projector that would
deploy the identity. The up-type extension
`(C_F − T_F)^{−1/2}` gives `Q_u = 4/5`, `5.75%` off observation; the
simple power extension does not work. Koide `Q = 2/3` is a
charged-lepton-specific phenomenon on the retained framework;
universal derivation is not available.

Runners:
- `scripts/frontier_koide_sectoral_universality.py`
- `scripts/frontier_koide_color_sector_correction.py`

## 6. Higher-order structural theorems

Three additional structural theorems clarify why higher-order and
propagator-dressed attempts also close negatively. Full proofs and
constructions in
[HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md](./HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md).

### 6.1 Theorem 4: canonical intermediate-subspace-lift transport identity

For any weight operator `X` on the intermediate subspace
`O_0 ⊕ T_2` and any Cl(3)-covariant lift
`lift_{int}: M_3(ℂ) → M_4(ℂ)`, the species diagonal of the dressed
return is
```
diag(P_{T_1} Γ_1  ·  lift_{int}(X)  ·  Γ_1 P_{T_1})|_species  =  diag(X).
```
The diagonal readout inherits trivially from the weight's diagonal,
independent of the choice of lift. Hence any retained Higgs-dressed
propagator construction cannot generate new species-resolved diagonal
content in the physical mass channel beyond what `X` itself supplies.

A numerically striking but structurally artificial near-miss: in the
**eigenvalue** channel (not the diagonal), a Higgs-resolvent
`W(H) = 1 / (λ − H_{lift})` at
`λ = 0.01594` (the neutrino-chamber interior distance) reaches
cos-similarity `0.9963` to the observed mass-square-root direction.
The Dirac-bridge theorem's `U_e = I_3` constraint excludes the
eigenvalue channel from the physical readout, so this near-miss is a
structural artifact, not a signal.

Runner: `scripts/frontier_higgs_dressed_propagator_transport_identity.py`.

### 6.2 Theorem 5: no retained variational principle on the current surface forces the Koide cone

Six candidate variational principles were tested:
Cauchy-Schwarz midpoint, maximum-entropy with `C_3` character
constraint, `log|det(D+J)|` partition extremum, Fisher-Rao midpoint,
norm extremum, retained Matsubara shape theorem. The unique
cone-forcing candidate (Cauchy-Schwarz) is ad-hoc — its cone-forcing
form factor is input, not derived. The two retained candidates
(`log|det|` partition, Matsubara shape) have stationary points at
fully-symmetric `Q = 1/3` or `2+1` degenerate splits, never at the
observed asymmetric cone point.

**Deep reason.** Retained `C_3`-invariant kernel
⇒ `C_3`-invariant variational functional ⇒ critical points respect
`C_3`. The observed charged-lepton cone point has no residual `S_2`
symmetry on axes `{2, 3}`, so no retained `C_3`-invariant principle
can select it without first breaking `C_3`.

**Real-irrep-block democracy (named candidate primitive).** The Koide
cone `a_0² = 2|z|²` IS the unique negative-definite maximum of the
**unweighted** block-log-volume
`S = log(a_0²) + log(2|z|²)` at fixed `|v|²`. However, the retained
`log|det(D)|` generator is dimension-weighted (one log per complex
irrep), giving stationary point at `σ = 1/3` rather than Koide
`σ = 1/2`. The gap is a single factor-of-2 weighting on the
two-dimensional nontrivial-character block. "Real-irrep-block
democracy" — treating the 1D trivial and 2D nontrivial blocks on
equal footing — is a sharply-named candidate primitive that, if
retained on a future framework extension, would derive Koide
uniquely.

Runners:
- `scripts/frontier_koide_cone_variational_principle_survey.py`
- `scripts/frontier_koide_cone_real_irrep_democracy.py`

### 6.3 Theorem 6: fourth-order signed Clifford ordering cancellation

For any even-parity fourth-order product of spatial Clifford
generators
`Γ_{i_1} Π Γ_{i_2} Π Γ_{i_3} Π Γ_{i_4}` with intermediate projector
`Π` returning to `T_1`:

Individual orderings of the multiset `{Γ_a², Γ_b²}` (a ≠ b) **do**
produce species-resolved single-species diagonals through `O_3`
participation — a new structural observation that mixed-`Γ` can reach
the `T_2(0, 1, 1)` state via `O_3`. However, signed ordering sums
within each multiset vanish pairwise:
```
Σ_orderings (−1)^{σ(ordering)} diag(Γ_ordering)  =  0
```
identically, because the `φ`-monomial weight from the EWSB expansion
depends only on the multiset, not on the ordering. This cancellation
is stronger than the residual `S_2` obstruction and is independent of
any retained or non-retained `φ`-reweighting scheme.

Parity selection restricts species-diagonalizing orderings to 21/81
sequences. The fourth-order retained spatial-Clifford + EWSB-weighted
Higgs family is ruled out as a Koide-forcing mechanism.

Runner: `scripts/frontier_fourth_order_mixed_gamma_return.py`.

### 6.4 Eight-channel S_2-breaking primitive survey

Eight independent retained channels were surveyed for breaking the
residual `S_2` symmetry on axes `{2, 3}` after weak-axis-1 selection:
anomaly-trace subcomponents, higher-order Higgs invariants,
lattice-geometric operators, chirality-specific operators,
Cl(3) bilinears, neutrino-mixing Hermitian lifted to `T_2`,
time-direction operators, and the retained Schur cascade. Seven close
as exactly `S_2`-symmetric on `T_2` diagonals. The single ambiguous
case (neutrino-mixing Hermitian at observational chamber pin lifted
to `T_2`) has a signed diagonal `(−0.934, +0.934, +0.657)` that
breaks `S_2` via the `T_δ`-tensor's `(0, 1, −1)` structure; physical
mass interpretation (absolute value) restores `w_a = w_b`, best
cos-similarity to the observed direction is `0.74`, and the
`T_1 → T_2` lift is post-hoc rather than retained. No retained
sole-axiom `S_2`-breaking primitive is present on the framework
surface.

Runner: `scripts/frontier_s2_breaking_primitive_survey.py`.

## 7. Theorem 7: charged-lepton observational-pin closure

Drawing from the preceding theorems and no-gos, we establish the
bounded charged-lepton result on the current retained surface.

### 7.0 Convention note (surfaced explicitly)

The weight triple `(w_{O_0}, w_a, w_b)` is the diagonal of the
second-order return operator `Σ` (Theorem 2). On dimensional grounds
`Σ` scales as `(effective mass)²` — it is a second-order expression
in the Dirac operator `Γ_1`. There are therefore two physically
distinct conventions for identifying `(w_{O_0}, w_a, w_b)` with
observed masses:

- **Convention A** (linear-mass pin — used in Theorem 7 below):
  `(w_{O_0}, w_a, w_b) ∝ (m_e, m_μ, m_τ)`.
  Rationale: read `Σ` as the effective **mass-operator diagonal**
  after Dirac-bridge diagonalization, so its eigenvalues are the
  physical masses at first power. Under this convention, the
  observed Koide `Q_ℓ = 2/3` is read directly off the weight triple.

- **Convention B** (mass-squared pin):
  `(w_{O_0}, w_a, w_b) ∝ (m_e², m_μ², m_τ²)`.
  Rationale: read `Σ` dimensionally as `(mass)²`. Under this
  convention, `Q(w) = Σw / (Σ√w)² = Σm² / (Σm)²`, which is **NOT**
  `2/3` empirically. The physical Koide is recovered on `√w`, which
  returns to the linear-mass triple.

The two conventions are mathematically equivalent for the **physical
content** — Koide `Q = 2/3` is a statement about linear charged-
lepton masses and holds empirically under both readings (directly
in Convention A, through `√w` in Convention B). The algebraic
cone equivalence of Theorem 1 is a statement on whichever triple we
call `v`; it does not select a convention. Both conventions are
cross-checked numerically by the companion runner
(`scripts/frontier_charged_lepton_observational_pin_closure.py`,
Step 3 convention-cross-check block).

This note, and Theorem 7 below, uses **Convention A** (linear-mass
pin). The bounded status is convention-invariant: under either convention, the 3-real observational input
determines the weight triple up to scale, the Koide condition
(on the appropriate triple) holds tautologically as a property of
the PDG charged-lepton masses, and no spare observable emerges from
the 3→3 map. Convention A is chosen for exposition because it
reads `Q_ℓ = 2/3` directly off the weights; Convention B is equally
admissible and carries the same bounded result.

### 7.1 Theorem 7 (under Convention A)

**Theorem 7.** Let
`(w_{O_0}, w_a, w_b) = (m_e, m_μ, m_τ)`
(normalized to `m_τ = 1`, giving
`(w_{O_0}, w_a, w_b) = (2.71 × 10^{−4}, 5.61 × 10^{−2}, 9.44 × 10^{−1})`).
Then:

- The triple lies strictly inside the retained chamber:
  positivity (R1) ✓;
  `Γ_1` reachability (R2) ✓;
  chiral-off-diagonal (R3) ✓;
  scale freedom (R4) ✓;
  `S_2`-broken requirement (R5) ✓ supplied by the pin.
- The triple is unique **as a set** up to overall scale. A residual
  `S_2` labeling ambiguity on `w_a ↔ w_b` persists on the retained
  surface (no retained operator breaks the axis-{2, 3} exchange),
  but Koide `Q` and the Σ spectrum are `S_2`-invariant, so the
  closure verdict is unaffected.
- Koide `Q_{pin} = 0.6666605` matches `2/3` to
  `|Q − 2/3| = 6.15 × 10^{−6}`. This match is a tautological
  algebraic consequence of the pin equaling the observed triple,
  which satisfies Koide to PDG precision. **The framework
  contribution is structural compatibility (via the shape theorem
  supplying exactly three independent weight slots), not framework
  derivation.**

**Repo status:** bounded. The charged-lepton
closure is a 3→3 observational pin and produces no spare observable
forecast analogous to the neutrino sector's 3→4 map producing
`δ_CP ≈ −81°`. Four structural consequences of the shape theorem are
testable but SM-consistent: lepton-flavor-violation zeros at leading
order, no charged-lepton EDM beyond SM, electron-hopping-ratio
asymmetry `12.30` (equals the PDG ratio-of-ratios tautologically),
and combined neutrino/charged-lepton consistency tests at
DUNE/Hyper-K. None is a genuinely new numerical prediction.

Runner: `scripts/frontier_charged_lepton_observational_pin_closure.py`.

## 8. Three named missing primitives for future retained extension

If any of the following three primitives is retained on a future
framework extension, the charged-lepton closure would upgrade from
observational-pin to sole-axiom:

**Primitive A** (from Theorem 4). A non-Cl(3)-covariant retained lift
of the intermediate propagator `O_0 ⊕ T_2` that carries
species-resolved diagonal information not inherited trivially from
its source weight. Any such lift would escape the canonical transport
identity.

**Primitive B** (from Theorem 5). Real-irrep-block democracy in the
variational weighting of `log|det(D)|` — treating the 1D trivial
character block and the 2D nontrivial character block on equal
footing rather than dimension-weighted. This would promote the
block-log-volume maximum at `σ = 1/2` (Koide) to a retained
derivation.

**Primitive C** (from Theorem 6). A mechanism breaking the signed
Clifford ordering cancellation within each multiset `{Γ_a², Γ_b²}`
at fourth order. Any retained mechanism that distinguishes between
orderings (rather than only multisets) would evade the cancellation.

Each primitive is sharply posed as a specific construction target for
future framework-retention work.

## 9. Dependency contract

All retained authority runners pass fresh on live `main`:

- `scripts/frontier_three_generation_observable_theorem.py` — 47 PASS, 0 FAIL.
- `scripts/frontier_hierarchy_observable_principle_from_axiom.py` — 13 PASS, 0 FAIL.
- `scripts/frontier_anomaly_forces_time.py` — 87 PASS, 0 FAIL.
- `scripts/frontier_dm_neutrino_dirac_bridge_theorem.py` — 28 PASS, 0 FAIL.
- `scripts/frontier_plaquette_self_consistency.py` — 16 PASS, 0 FAIL.

All 19 runners accompanying this review pass on the `origin/main`
base: **518 PASS / 0 FAIL** across the campaign.

No retained authority notes on `main` are modified by this submission.
PDG charged-lepton mass values enter only as comparators and as the
3-real observational pin in Theorem 7; no derivation input uses PDG
data.

## 10. Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the charged-lepton
> Koide relation `Q_ℓ = 2/3` is rigorously equivalent to the
> equal-character-weight condition `a_0² = 2|z|²` on the retained
> `hw=1` triplet (Theorem 1). A retained second-order-return shape
> theorem supplies exactly three independent weight slots on the
> charged-lepton generation space (Theorem 2), and the retained
> Hermitian subspaces encoding charged-lepton masses and
> neutrino-mixing parameters are disjoint (trivial intersection / direct sum as ℝ-vector spaces, not orthogonality under any inner product)
> (Theorem 3, `dim(V_H ∩ V_D) = 0`). Six rigorous no-go theorems
> establish that every retained non-Higgs-Yukawa mechanism is
> species-diagonal on the generation space (Sections 5.1–5.6).
> Three higher-order structural theorems — transport identity
> (Theorem 4), variational `C_3`-invariance obstruction (Theorem 5),
> and fourth-order signed Clifford ordering cancellation
> (Theorem 6) — close the three natural framework-derives routes.
> Charged-lepton closure as a bounded package follows from a
> three-real observational pin on PDG charged-lepton masses
> (Theorem 7). The retained framework is structurally compatible with
> Koide but does not derive it; three sharply-named missing primitives
> are identified for future retained extension.
> The 3→3 pin map carries no spare observable forecast beyond the pin.

## 11. Runner manifest

Nineteen runners, 518 PASS / 0 FAIL on `origin/main` base:

| Runner | PASS | Theorem / section cited |
|---|---|---|
| `frontier_charged_lepton_observable_curvature.py` | 28 | Theorem 1 |
| `frontier_charged_lepton_z3_source_response_crosscheck.py` | 41 | §5.1 |
| `frontier_koide_sectoral_universality.py` | 20 | §5.6 |
| `frontier_charged_lepton_curvature_apbc_extension.py` | 44 | §5.2 |
| `frontier_observable_principle_character_symmetry.py` | 30 | §5.3 |
| `frontier_koide_color_sector_correction.py` | 24 | §5.6 |
| `frontier_koide_su2_gauge_exchange_mixing.py` | 49 | §5.4 |
| `frontier_koide_anomaly_forced_cross_species.py` | 42 | §5.5 |
| `frontier_charged_lepton_via_neutrino_hermitian.py` | 14 | Theorem 3 |
| `frontier_hw1_second_order_return_shape_theorem.py` | 20 | Theorem 2 |
| `frontier_charged_lepton_observational_pin_closure.py` | 39 | Theorem 7 |
| `frontier_s2_breaking_primitive_survey.py` | 31 | §6.4 |
| `frontier_mass_mixing_disjointness_theorem.py` | 9 | Theorem 3 |
| `frontier_shape_theorem_robustness_audit.py` | 57 | Theorem 2.1 |
| `frontier_higgs_dressed_propagator_v1.py` | 7 | Theorem 4 (companion) |
| `frontier_higgs_dressed_propagator_transport_identity.py` | 10 | Theorem 4 |
| `frontier_koide_cone_variational_principle_survey.py` | 20 | Theorem 5 |
| `frontier_koide_cone_real_irrep_democracy.py` | 22 | Theorem 5 |
| `frontier_fourth_order_mixed_gamma_return.py` | 11 | Theorem 6 |
| **TOTAL** | **518** | — |

## What this note does not claim

- The retained framework does **not** derive Koide `Q = 2/3` as a sole-axiom theorem output.
- The charged-lepton hierarchy does **not** fall out of the neutrino-mixing closure as a corollary (Theorem 3 rigorously blocks this route).
- The bounded charged-lepton package does **not** produce a numerical forecast analogous to `δ_CP ≈ −81°`. The 3→3 pin map has no spare observable.
- The "four falsifiable predictions" that emerge structurally from the shape theorem are SM-consistent and do not distinguish the framework from the Standard Model at current experimental precision.
- The observational-pin triple is unique **as a set** up to overall scale; a residual `S_2` labeling ambiguity on `w_a ↔ w_b` persists on the retained surface.

## Status

**REVIEW** — ready for editorial review against the retained
`Cl(3)/Z^3` publication bar.
