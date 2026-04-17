# Derivation: Charged-Lepton Mass-Square-Root Vector on the hw=1 Observable-Principle Surface

## Date
2026-04-17

## Target Behavior

On the retained `Cl(3)` on `Z^3` framework surface, the charged-lepton
mass-square-root vector
```
v_L = (√m_e, √m_μ, √m_τ)
```
satisfies Koide's invariant
```
Q  ≡  (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²  =  2/3
```
as an exact algebraic output (not a floating-point near-miss), and
the full direction `[v_L]` on the resulting 45° cone is uniquely
fixed by one additional `C_3`-character invariant extracted from the
observable-principle curvature kernel.

Observed numerical targets:
- Normalized direction
  `(v_e, v_μ, v_τ) / ||·||  ≈  (0.0165, 0.2369, 0.9713)`.
- `Q_{obs}  ≈  0.6668`, exact target `2/3 = 0.66667`.
- `m_μ / m_τ  ≈  0.0594`, `m_e / m_μ  ≈  0.00484`.

## Axioms Used

The derivation anchors on the **full retained** `Cl(3)` on `Z^3`
framework surface:

1. Three-Generation Observable Algebra — retained `hw=1` triplet,
   exact translation projectors, exact induced `C_{3[111]}` cycle.
   Authority:
   `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`.
   Runner: `scripts/frontier_three_generation_observable_theorem.py`
   (47 PASS, 0 FAIL).

2. Observable Principle from Axiom — unique additive CPT-even
   scalar generator `W[J] = log|det(D + J)|`, local source-response
   curvature kernel. Authority:
   `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`.
   Runner:
   `scripts/frontier_hierarchy_observable_principle_from_axiom.py`
   (13 PASS, 0 FAIL).

3. Anomaly-Forced Dirac Bridge — retained `Γ_1` definition on
   `C^{16}`, retained second-order-return identity
   `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} = I_3`. Authority:
   `DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md`.
   Runner: `scripts/frontier_dm_neutrino_dirac_bridge_theorem.py`
   (28 PASS, 0 FAIL).

4. Anomaly-Forced 3+1 Closure — retained `3+1` surface for APBC
   constructions. Authority:
   `ANOMALY_FORCES_TIME_THEOREM.md`.

5. Plaquette Self-Consistency — retained
   `α_{LM}, u_0, ⟨P⟩`. Authority:
   `PLAQUETTE_SELF_CONSISTENCY_NOTE.md`.

No quark, charged-lepton, PMNS, CKM, or fitted-flavor input appears
in any derivation step. Observed charged-lepton masses appear only
as comparators and as the observational pin in the closure theorem.

## Minimal Example

The smallest network configuration carrying the full structure is
the minimal `3+1` APBC block with three retained `hw=1` species on
a single spatial `Z^3` unit cell, evaluated through one `L_t = 4`
temporal orbit.

## Derivation Chain

### Step 1: Unique observable-principle curvature kernel on hw=1

Restrict sources to the retained `hw=1` triplet:
`J = j_1 P_1 + j_2 P_2 + j_3 P_3`.
The restricted curvature kernel `K_{ij}` on the hw=1 species basis is:
- Real (CPT-even).
- Symmetric (cyclic trace).
- `C_3`-covariant: the induced `C_{3[111]}` cycle maps
  `P_i → P_{i+1 mod 3}`, and the kernel transforms equivariantly.

### Step 2: Circulant two-parameter form

A real symmetric `C_3`-invariant 3×3 matrix has the circulant form
`K = a·I + b·(J − I)` with `a, b ∈ ℝ`, where `J` is the all-ones
matrix. Spectrum:
- `α = a + 2b` on the trivial `C_3` character `E_+`.
- `β = a − b` on the nontrivial `C_3` characters
  `E_ω`, `E_{ω²}` (doubled by reality).

### Step 3: Dirac spectral amplitude from K

On the retained minimal `3+1` APBC block, the Matsubara
source-response structure gives `K_{ii}^{(spec)} = 16 /
(m_i² + (7/2) u_0²)` at `L_t = 4`. The factor `7/2 = 3 + 1/2`
matches the `(7/8)^{1/4}` selector in the retained
electroweak-hierarchy theorem (`v = 246.28…` GeV). The physical
mass-square-root vector is proportional to the Dirac spectral
amplitude vector `(λ_1, λ_2, λ_3)` with `λ_i ∼ \sqrt{m_i}`.

### Step 4: Character decomposition of the spectral vector

Plancherel on `C_3`:
`|λ|² = a_0² + 2|z|²`,
`(Σ λ_i)² = 3 a_0²`
where `a_0 = (Σ λ_i) / √3` and
`z = (λ_1 + ω̄ λ_2 + ω λ_3) / √3`.

### Step 5: Koide-cone algebraic equivalence

Under the proportionality `v_L ∝ λ`:
```
3 Σ λ_i² = 2 (Σ λ_i)²     ⟺     a_0² = 2 |z|².
```
Therefore Koide `Q = 2/3` is **exactly equivalent** to the
equal-character-weight condition. This is an algebraic identity —
it rephrases Koide in `C_3`-character language but does not by
itself derive the cone point.

### Step 6 (open on retained surface): forcing the spectral vector onto the cone

The derivation at Steps 1–5 establishes an algebraic equivalence;
it does NOT yet force the physical spectral vector onto the
`a_0² = 2|z|²` surface.

Three forcing candidates identified at the derivation stage:
- **Candidate A.** Spontaneous `C_3` breaking at the
  equal-contribution stationary point of the curvature landscape.
- **Candidate B.** Observable-principle second-variation character
  symmetry — `α = β` via the retained `log|det(D + J)|`
  uniqueness + additivity + CPT-even chain.
- **Candidate C.** `L_t = 4` selector arithmetic producing `1/√2`
  as the relative weight of the nontrivial character.

On the minimal `L_t = 4` APBC block, all three candidates fail
structurally: the off-diagonal `b = K_{12} = 0` because the three
`hw=1` species live in orthogonal translation-character
eigenspaces, collapsing the circulant kernel to `a · I_3`.

The 19-agent campaign documented in the review-note package
extends this analysis across every natural attack surface. The
final verdict is that no retained mechanism on the current framework
surface forces the spectral vector onto the Koide cone; closure
proceeds at the observational-pin class (Theorem 7 of the review
note) with strict-review verdict `TRUE_NO_PREDICTION`.

### Step 7: Residual-ratio algebraic extraction (open on retained surface)

After cone-forcing, the residual degree of freedom is the position
of `v_L` on the 2D Koide cone. For a sole-axiom derivation, the
framework must fix this further invariant. On the current retained
surface, it does not.

## Novel Prediction

If the structural route worked as originally hypothesized, the
following quantitative statements would hold:

1. `|z| / a_0 = 1/√2 ≈ 0.70710678` exactly (from Koide-cone
   equivalence).
2. Applied to down-type quarks, `Q_d = 2/3`.
3. Applied to up-type quarks, `Q_u = 2/3`.

**Result.** Predictions 2 and 3 are **falsified** on the current
framework + PDG observation surface:
- `Q_d (framework-native) ≈ 0.73058` (`+9.59%` off `2/3`).
- `Q_u (PDG self-scale)   ≈ 0.84884` (`+27.33%` off `2/3`).

This sectoral-universality falsification rigorously confirms that
Koide `Q = 2/3` is a charged-lepton-specific phenomenon on the
retained framework, not a universal derivation. A tantalizing
retained SU(3) Casimir identity `(C_F − T_F)^{−1/4} = (6/5)^{1/4}`
reproduces `Q_d / Q_ℓ ≈ √(6/5)` to `0.04%` precision if deployed
as a species-dependent color-adjoint dressing — but the retained
`hw=1` algebra carries no such deployment primitive.

## Weakest Link

Step 6 (cone-forcing) is the weakest link. At the time of the
derivation chain, it was a single candidate-identification; in the
final review-note package, it has become the rigorous negative
conclusion summarized across six structural no-gos and three
framework-derives routes.

## Outcome Summary

- Steps 1–5: **rigorously confirmed** on the retained framework
  surface. Koide is equivalent to `a_0² = 2|z|²` as an algebraic
  identity (Theorem 1 of the review note).
- Step 6: **cone-forcing fails** on the retained surface. Three
  higher-order routes (transport-identity, variational-principle,
  fourth-order-mixed-Γ) all close negatively.
- Step 7: **residual-ratio extraction** requires observational pin.

Charged-lepton closure at the retained-map-plus-observational-
promotion class (Theorem 7 of the review note). Strict-review
verdict `TRUE_NO_PREDICTION`.

## Status
RESOLVED (negative on retained surface; review-note package is the
consolidated report).
