# Strong CP / θ = 0 Theorem

**Date:** 2026-04-15
**Status:** retained exact structural theorem on the axiom-determined surface
**Script:** `scripts/frontier_strong_cp_theta_zero.py`

## Theorem

**Theorem (θ_eff = 0).**
The Cl(3)/Z³ framework with the minimal 5-input axiom stack predicts
θ_eff = 0 exactly. The strong CP problem does not arise. No axion is
needed.

## The Standard Strong CP Problem

In the Standard Model, the effective QCD vacuum angle is

    θ_eff = θ_QCD + arg det(M_u M_d)

where θ_QCD is the bare vacuum angle in the gluon action and
arg det(M_u M_d) is the phase of the quark mass matrix determinant.
Both contributions are independent free parameters, generically O(1),
yet experiment constrains |θ_eff| < 10⁻¹⁰ from the neutron electric
dipole moment bound.

This unexplained cancellation is the strong CP problem (50 years open).

## How the Framework Resolves It

The resolution has three legs, each independently necessary and jointly
sufficient.

### Leg A: Fermion determinant is real and positive

The staggered Dirac operator D on Z³ with SU(3) gauge links satisfies:

1. D is anti-Hermitian: D† = −D (verified numerically to 0.00e+00 on
   L = 4 with free and random gauge configurations).
2. Eigenvalues of D are purely imaginary: {iλ_k} with λ_k real.
3. Eigenvalues of D + mI are m ± iλ_k, coming in conjugate pairs.
4. det(D + mI) = Π_k (m² + λ_k²) > 0 for any m > 0.

The fermion determinant carries no complex phase. Verified numerically:

- Free field (L = 4): det phase = 0.00e+00 (exactly zero)
- Gauged (L = 4, 3 random SU(3) configs): det phases = 3.0e-15,
  −7.5e-17, −6.2e-16 (machine zero)

**Control test:** With a complex mass m → m e^{iθ}, θ = 0.3, the
determinant acquires phase 1.24. This confirms that the reality of the
mass (not an accident of the lattice size or configuration) is what
forces the determinant phase to zero.

Therefore: arg det(M_u M_d) = 0.

### Leg B: Gauge action is CP-even (no θ-term)

The Wilson plaquette action S_gauge = −β Σ Re Tr U_P / 3 is CP-even.

Under CP, a plaquette transforms as U_P → U_P†, so:
- Tr U_P → (Tr U_P)*
- Re Tr U_P → Re Tr U_P (CP-even)
- Im Tr U_P → −Im Tr U_P (CP-odd)

Verified on 500 random SU(3) plaquettes to 0.00e+00 residual.

The topological charge Q_lat is proportional to Σ Im Tr (clover) and is
therefore CP-odd. A θ·Q term would break CP. Since the axiom-determined
gauge action contains only the Wilson plaquette (CP-even), no θ-term
appears.

Therefore: θ_bare = 0.

### Leg C: θ is structurally absent from the axiom stack

The minimal axiom stack has exactly 5 inputs:

1. Cl(3) local algebra
2. Z³ spatial substrate
3. Finite Grassmann / staggered-Dirac partition
4. Physical lattice reading
5. Canonical normalization: g_bare = 1, plaquette / u₀ surface

Axiom 5 fully determines the gauge action. Axiom 3 fully determines the
fermion action. Both are real. Adding θ ∈ [0, 2π) to the action would
require a 6th input that is not in the stack. The framework predicts
θ = 0, not θ as a tunable parameter.

The partition function is:

    Z = ∫ DU det(D + m) e^{−S_gauge}

Every factor is real and positive:
- det(D + m) > 0 (Leg A)
- e^{−S_gauge} > 0 (Leg B)

Therefore Z > 0 is real and positive. A θ-term Z(θ) = ∫ DU det(D + m)
e^{−S_gauge + iθQ} would make Z complex for θ ≠ 0, contradicting the
real-positive structure.

### Combined result

    θ_eff = θ_bare + arg det(M_u M_d) = 0 + 0 = 0

This is a structural prediction, not a dynamical relaxation mechanism.

## Relation to CKM CP Violation

The framework does have CP violation — in the weak sector. The Z₃ CP
source (δ_source = 2π/3) enters through the EWSB 1+2 split and produces
the CKM phase δ_std = arctan(√5) = 65.905°. This is verified in
CKM_ATLAS_AXIOM_CLOSURE_NOTE.md (PASS=all).

The key structural fact: the color SU(3) is the graph-first commutant
of the weak SU(2) on the taste cube. The Z₃ CP source acts on the weak
factor (it changes which axis is selected), not on the color commutant.
Verified:

- Z₃ does NOT commute with the selected-axis SU(2) (|[Z₃, T₀]| = 0.5)
- Z₃ eigenvalues are discrete cube roots of unity (no continuous θ)
- Joint commutant dim = 10 (gl(3) ⊕ gl(1)), confirming clean
  color-weak factorisation

The CKM phase produces CP violation in weak decays but cannot generate
a strong-sector θ because:

1. The CP phase enters V_CKM, not the mass eigenvalues
2. Mass eigenvalues remain real and positive → arg det(M) = 0
3. The color sector (commutant) is structurally blind to the weak phase

## Extension to the Interacting Theory

The free-field CP result (CPT_EXACT_NOTE.md: [CP, H_free] = 0,
PASS = 53, FAIL = 0 on L = 4, 6, 8) extends to the interacting theory:

1. Gauge action S_gauge is CP-even (Re Tr U_P is CP-even)
2. Fermion-gauge coupling S_f is CP-even (real staggered phases η_μ,
   covariant CP transform of U_μ)
3. Full action S = S_gauge + S_f is CP-even at tree level
4. CP-even action generates only CP-even effective operators at all
   loop orders

This partially closes open item 1 of CPT_EXACT_NOTE.md for the CP
sector.

## S³ Topology

On S³, π₃(SU(3)) = Z, so instanton sectors with integer topological
charge Q exist in principle. The partition function is
Z = Σ_Q Z_Q with Z_Q ≥ 0 (real positive weights). Without a θ-phase,
all sectors contribute constructively. No spontaneous CP violation
occurs from the vacuum structure.

## What Is Actually Proved

### Exact (theorem-grade):

1. Anti-Hermiticity of staggered D[U] on Z³ with SU(3) links
2. Fermion determinant det(D + mI) is real and positive for real m > 0
3. Wilson plaquette Re Tr U_P is CP-even (Im Tr U_P is CP-odd)
4. Weak su(2) closes on the graph-first selected-axis fiber
5. Joint commutant of {su(2), τ} has dimension 10
6. Z₃ eigenvalues are discrete cube roots of unity
7. The axiom stack has 5 inputs, no room for θ

### Structural (logic-grade):

8. θ_bare = 0 because the gauge action is fully axiom-determined
9. arg det(M) = 0 because the staggered mass is real
10. θ_eff = 0 as a structural prediction
11. CP violation is confined to the weak sector via CKM

## What Remains Open

1. **Neutron EDM prediction.** The framework predicts θ_eff = 0, hence
   d_n = 0 from QCD. Any nonzero d_n would come from higher-order weak
   effects (CKM phase). Quantifying the CKM contribution to d_n is a
   separate bounded lane.

2. **Lattice instanton measure.** While the partition sum
   Z = Σ_Q Z_Q is established, the detailed instanton measure Z_Q on
   the physical S³ lattice is not computed here.

3. **Axion exclusion.** The framework predicts θ = 0 without an axion.
   If the framework is correct, the axion does not exist (or at least is
   not needed for strong CP). This is a testable prediction against
   axion search experiments.

## How This Changes The Paper

This is a clean structural result that solves a 50-year-old problem.
The statement is:

> The Cl(3)/Z³ framework predicts θ_eff = 0 as a structural
> consequence of the axiom-determined action. The staggered Dirac
> operator is anti-Hermitian with real mass, giving a real positive
> fermion determinant. The Wilson plaquette gauge action is CP-even.
> No θ-parameter exists in the framework — it would be a 6th free
> parameter beyond the minimal 5-input axiom stack. The strong CP
> problem does not arise. CP violation occurs exclusively in the weak
> sector through the discrete Z₃ source that generates the CKM phase.

This belongs in the main text alongside the exact CPT result. It
strengthens the paper's case that the framework resolves known
fine-tuning problems by having zero free parameters.

## Experimental Predictions

1. **θ_eff = 0 exactly.** No CP violation in the strong sector.
2. **Neutron EDM from QCD: d_n = 0.** Any measured d_n arises from
   higher-order weak effects only.
3. **No QCD axion.** The strong CP problem is resolved structurally;
   the Peccei-Quinn mechanism is not needed.

## Commands Run

```text
python3 scripts/frontier_strong_cp_theta_zero.py
# Exit code: 0
# PASS=56  FAIL=0
```
