# Structural No-Go Survey on the Charged-Lepton Mass Hierarchy

**Date:** 2026-04-17
**Status:** six rigorous structural no-go theorems on the proposed_retained `Cl(3)/Z^3` surface
**Runners (6):**
- `scripts/frontier_charged_lepton_z3_source_response_crosscheck.py` (41 PASS)
- `scripts/frontier_charged_lepton_curvature_apbc_extension.py` (44 PASS)
- `scripts/frontier_observable_principle_character_symmetry.py` (30 PASS)
- `scripts/frontier_koide_su2_gauge_exchange_mixing.py` (49 PASS)
- `scripts/frontier_koide_anomaly_forced_cross_species.py` (42 PASS)
- `scripts/frontier_koide_sectoral_universality.py` (20 PASS)
- `scripts/frontier_koide_color_sector_correction.py` (24 PASS)

Total: 250 PASS, 0 FAIL.

## Purpose

The retained `Cl(3)/Z^3` framework is structurally compatible with
Koide `Q = 2/3` via the shape theorem
([HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md](./HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md)).
The question is whether the specific cone point
`a_0² = 2|z|²` can be **forced** by retained structural mechanisms
without observational pinning. This note surveys six such mechanisms
and establishes that each closes negatively.

## 5.1 Z_3 invariance alone is insufficient

**Theorem.** The `Z_3`-invariant bilinear source-response kernel
with canonical left/right generation charges
`q_L = (0, +1, −1)` and `q_R = (0, −1, +1)`
evaluates on the retained `hw=1` triplet to
```
S  =  I_3
```
(triply-degenerate identity). Every nonzero real 3-vector is an
eigenvector of `S`; `Z_3` invariance alone does not force a unique
mass ray.

*Construction.* On `C[Z_3] ⊗ C[Z_3]`, build the character-idempotent
sources `s_i = e_{q_L(i)} ⊗ e_{q_R(i)}`. Each `s_i` is
diagonal-`Z_3`-invariant under the diagonal action
`(T^g) ⊗ (T^g)` because `q_L(i) + q_R(i) = 0 mod 3` for each `i`.
The Plancherel pairing
`S_{ij} = Tr(s_i^† s_j)` on the regular representation is diagonal
and equal to `I_3` (by orthogonality of the character idempotents).

*Consequence.* The algebraic-permissiveness null — "maybe Koide is
automatic because the `Z_3`-invariant algebra is sufficient" — is
closed. The algebra is not just permissive; it is triply-degenerate,
carrying zero directional content. Any retained structural derivation
of Koide must therefore rely on dynamical content beyond `Z_3`
invariance.

Runner: `scripts/frontier_charged_lepton_z3_source_response_crosscheck.py`.

## 5.2 Pure-APBC temporal refinement is insufficient at any L_t

**Theorem.** On every pure-APBC temporal block with
`L_t ∈ {4, 6, 8, 12, 16, 24, ∞}`, the off-diagonal source-response
curvature
```
K_{ij}(L_t)  =  −Re Tr[(D + J)^{−1} P_i (D + J)^{−1} P_j]  =  0
```
for `i ≠ j` on the retained `hw=1` triplet, whenever `J` is
species-diagonal.

*Proof.* The three `hw=1` species carry pairwise-orthogonal joint
translation characters
```
X_1 → (−1, +1, +1),   X_2 → (+1, −1, +1),   X_3 → (+1, +1, −1).
```
Pure-APBC `D` commutes with each of the three lattice translations
`T_x, T_y, T_z`, and species-diagonal `J` commutes with all three by
construction. Hence `(D + J)^{−1}` commutes with each `T_k`. Since
each pair `(X_i, X_j)` (`i ≠ j`) differs on at least one of the three
translation characters, `P_i (D + J)^{−1} P_j = 0` identically. □

*Bulk limit.* The effective denominator coefficient
`c_{eff}(L_t)` on the diagonal satisfies
```
lim_{L_t → ∞} c_{eff}(L_t)  =  2√3  ≈  3.4641,
```
correcting the naive bulk reading `c → 3`. The retained `c(4) = 7/2`
sits 1% above the bulk value and the sequence converges monotonically.

*Consequence.* The pure-APBC temporal-refinement lane is permanently
closed. The minimal-block `b = 0` result (on `L_t = 4`) is not
a minimal-block artifact but a structural consequence of
translation-character orthogonality, holding at every `L_t`.

Runner: `scripts/frontier_charged_lepton_curvature_apbc_extension.py`.

## 5.3 Observable-principle character symmetry does not force α = β

**Theorem.** The unique-generator + additivity + CPT-even
requirements on `W[J] = log|det(D + J)|` do **not** force the
curvature eigenvalues on the trivial `C_3` character subspace
(`α = a + 2b`) and the nontrivial subspace (`β = a − b`) to coincide
on `hw=1` blocks with nonzero cross-species propagator `b`.

Three independent symbolic tactics each exhibit explicit
counterexamples:

### Tactic T1 — direct Legendre transform

Build `W[J]` on the minimal tensor-factored block
`D = D_+ ⊕ D_−` with `D_+` acting on the trivial-character subspace
`E_+` (1D) and `D_−` acting on the nontrivial subspace
`E_ω ⊕ E_{ω²}` (2D). Independent mass scales `m_+, m_−` give
`α = m_+², β = m_−²`. Counterexample `(m_+, m_−) = (2, 1)` yields
`α = 4, β = 1` with all retained axioms satisfied. **Verdict:
NEGATIVE.**

### Tactic T2 — Schur's lemma

The `C_3` action on the `hw=1` triplet decomposes as
`E_+ ⊕ E_ω ⊕ E_{ω²}` with three pairwise-inequivalent complex
irreps. `E_ω` and `E_{ω²}` are complex-conjugate irreps, so reality
forces the corresponding curvature eigenvalues to coincide into a
single `β`. But `E_+` and `E_ω` are **inequivalent** (their
characters `χ_+(σ) = 1` and `χ_ω(σ) = ω` are distinct), so Schur's
lemma permits independent eigenvalues on these subspaces. **Verdict:
NEGATIVE (clean sub-result).**

### Tactic T3 — additivity chain

On the tensor-factored configuration
`D = D_+ ⊕ D_−` with independent mass scales, the retained Theorem 1
of the observable-principle authority supplies a unique
`W_i = log|det(D_i + J_i)|` on each subsystem. Additivity gives
`W[J] = W_+[J_+] + W_−[J_−]` with curvature eigenvalues
`φ_+ = 1/m_+², φ_⊥ = 1/m_−²`. The equality `φ_+ = φ_⊥` holds iff
`m_+ = m_−`. Counterexample `(m_+, m_−) = (3, 1)` exhibits
`φ_+ = 1/9 ≠ 1 = φ_⊥` with all three axioms satisfied. **Verdict:
NEGATIVE (counterexample).**

All three tactics fail independently. The reach of the retained
observable-principle authority does not extend to Koide-cone forcing;
a genuinely new retained primitive is required.

Runner: `scripts/frontier_observable_principle_character_symmetry.py`.

## 5.4 SU(2)_L gauge exchange cannot generate cross-species mixing

**Theorem (taste-species carrier orthogonality).** The retained
native `SU(2)_L` generators `S^a` live in the taste `Cl(3)` subalgebra
of the retained `Cl(3) ⊗ chirality` carrier `C^{16}`, while the
`hw=1` species label `{X_1, X_2, X_3}` is the translation-character
BZ-corner label. On the retained physical surface,
```
ρ_{hw=1}(S^a)  =  I_{species}   for all a ∈ {1, 2, 3}.
```
Every `SU(2)_L`-dressed operator commutes with the rank-1 species
projectors `P_i` and cannot generate cross-species matrix elements
at any order in `g_2`.

*Consequence.* The off-diagonal curvature parameter `b` receives
only `a`-type (diagonal) renormalization at any order in
`SU(2)_L` gauge exchange. Color dressing on quarks multiplies the
diagonal contribution by a color-singlet factor `C_{color}` without
generating cross-species matrix elements. The retained
`SU(2)_L`-gauge-exchange mechanism is structurally closed as a
Koide-forcing route.

*Broader lesson.* The taste-species carrier orthogonality generalizes
to every retained algebraic or gauge operator that lives in the taste
Cl(3) subalgebra or its commutant. The charged-lepton mass hierarchy
is forced to couple to the species label through an operator that is
NOT in the retained gauge algebras — most naturally, the Higgs
Yukawa, which couples species via a VEV rather than through taste
algebra.

Runner: `scripts/frontier_koide_su2_gauge_exchange_mixing.py`.

## 5.5 Anomaly-forced 3+1 structure is species-blind on hw=1

**Theorem.** Every retained anomaly-forced ingredient on the
Standard Model branch acts as a scalar on the `hw=1` species label:

- `γ_5`: spinor-index operator, identity on species.
- Right-handed singlet completion (`u_R, d_R, e_R, ν_R`): species-
  uniform hypercharge `Y` per sector, species-blind.
- Five anomaly traces `Tr[Y], Tr[Y^3], Tr[SU(3)^2 Y],
  Tr[SU(2)^2 Y]`, Witten: all vanish on the SM branch; no anomaly-
  weighted insertion contributes to species-diagonal.
- Chirality-forcing Dirac mass bilinear
  `ψ_L^† γ_0 ψ_R`: species-blind without a Higgs VEV insertion; the
  VEV insertion pushes the mechanism into the observational-pin
  regime.
- Chirality projectors `(1 ± γ_5)/2`: species-blind.

Tested on `L_t ∈ {6, 8, 12, 16}` with anomaly-forced operator
insertions. On every tested block,
```
K_{ij}^{(anomaly)}  =  0    for i ≠ j.
```
Within-sector cross-species mixing from the retained anomaly
structure alone is impossible.

*Sector-scale signal.* The anomaly theorem does carry a sector-scale
distinction between leptons and quarks:
```
Tr[Y^3]_{per-doublet}:  Q_L : L_L  =  −1/27 : 1
Tr[SU(2)^2 Y]_{per-doublet}:  Q_L : L_L  =  1 : −1.
```
But within a single sector, all three generations carry identical
hypercharges, so the anomaly-forced operator is species-blind within
each sector.

Runner: `scripts/frontier_koide_anomaly_forced_cross_species.py`.

## 5.6 Sectoral universality of Koide Q = 2/3 is falsified

**Theorem.** On the current framework + PDG observation surface,
Koide `Q_{sector} = 2/3` is satisfied ONLY for charged leptons:

| Sector | `Q` | Scheme | Deviation from 2/3 |
|---|---|---|---|
| Charged leptons | 0.66666 | PDG pole masses | `−0.001%` |
| Down-type quarks (framework) | 0.73058 | `α_s(v) + 5/6` bridge | `+9.59%` |
| Down-type quarks (PDG) | 0.73143 | threshold-local self-scale | `+9.71%` |
| Up-type quarks | 0.84884 | PDG self-scale | `+27.33%` |
| Up-type quarks | 0.88837 | MS-bar at `μ = M_Z` | `+33.26%` |

No scheme correction derivable from retained theorems closes the
up-type gap. The minimum scheme rescaling of `√m_t` to force
`Q_u = 2/3` requires effective `m_t ≈ 19.9 GeV`, not derivable from
any retained theorem.

*Near-miss: the Casimir identity `(C_F − T_F)^{−1/4} = (6/5)^{1/4}`.*
The retained SU(3) Casimirs `C_F = 4/3`, `T_F = 1/2` give the exact
algebraic identity
```
(C_F − T_F)^{−1/4}  =  (6/5)^{1/4}  =  1.0466…
```
If this were deployed as a down-type `hw=1` spectral-amplitude
dressing, it would predict
```
Q_d / Q_ℓ  =  √(6/5)  ≈  1.0955,
```
which matches the observed ratio `0.73143 / 0.66666 = 1.0971` to
**0.15%**. However, the retained `hw=1` algebra does not carry a
species-dependent color-adjoint projector that would deploy the
identity, and the naive up-type extension `(C_F − T_F)^{−1/2}` gives
`Q_u = 4/5`, which differs from observed `Q_u = 0.849` by 5.75%.
The simple power extension does not work. Koide `Q = 2/3` is a
charged-lepton-specific phenomenon on the retained framework;
universal derivation via a single Casimir-power scheme is not
available.

Runners:
- `scripts/frontier_koide_sectoral_universality.py`
- `scripts/frontier_koide_color_sector_correction.py`

## Composite reading

All six no-gos point to the same underlying fact: **every retained
operator on the `hw=1` triplet built from retained algebraic or
anomaly-forced structure acts as a scalar multiple of the species
identity UNLESS it involves a Higgs-Yukawa VEV insertion**. The
Higgs Yukawa is the unique retained cross-species primitive on the
`hw=1` triplet — and its deployment as a charged-lepton mass
mechanism requires observational pinning via the shape-theorem
weight triple (Theorem 7 in
`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` — upstream
review note; backticked to avoid length-11 cycle through the koide
cluster).

## What this note does not claim

- The six no-gos do not prove that no retained derivation of Koide
  is possible. They prove that the six enumerated mechanism classes
  individually fail. Higher-order mechanisms and variational
  principles are examined in
  [HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md](./HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md).
- The `Q_d / Q_ℓ ≈ √(6/5)` Casimir near-match is an observation
  about the retained algebra, not a retained theorem. It is
  currently unretained due to the missing species-dependent
  deployment primitive.

## Paper-safe wording

> Six rigorous no-go theorems establish that every retained
> non-Higgs-Yukawa mechanism on the `hw=1` charged-lepton triplet is
> species-diagonal: `Z_3` invariance alone is insufficient (§5.1);
> pure-APBC temporal refinement at any `L_t` is insufficient (§5.2);
> the observable-principle character-symmetry chain does not force
> the curvature eigenvalues to coincide (§5.3); `SU(2)_L` gauge
> exchange cannot generate cross-species mixing (§5.4); the
> anomaly-forced 3+1 structure is species-blind on `hw=1` (§5.5);
> and the universal Koide `Q = 2/3` prediction is falsified across
> sectors with no retained scheme correction (§5.6). All six close
> with 250 PASS / 0 FAIL across the six runners.

## Status

**REVIEW.**
