# Strong CP / θ = 0 Theorem

**Date:** 2026-04-15
**Status:** retained exact structural theorem on the axiom-determined surface
**Script:** `scripts/frontier_strong_cp_theta_zero.py`

## Theorem

**Theorem (θ_eff = 0).**
On the axiom-determined Wilson-plus-staggered action surface of the
Cl(3)/Z³ framework, `θ_eff = 0` exactly: the retained action carries no
bare `θ` term, the real-mass staggered determinant carries no phase, and CKM
CP remains weak-sector only.

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

### Leg C: no bare `θ` term appears on the axiom-determined action surface

The minimal axiom stack has exactly 5 inputs:

1. Cl(3) local algebra
2. Z³ spatial substrate
3. Finite Grassmann / staggered-Dirac partition
4. Physical lattice reading
5. Canonical normalization: g_bare = 1, plaquette / u₀ surface

Axiom 5 fully determines the gauge action. Axiom 3 fully determines the
fermion action. Both are real. On this retained action surface there is no
bare `θ` parameter to tune.

The key point is not merely that `θ` is "unmentioned" — it is that the
retained action is uniquely the Wilson plaquette (real) plus the
staggered-Dirac partition (real). A bare `θ` term would require either a
complex mass term (violating the reality of the staggered action, Leg A) or
an imaginary topological term `iθQ` (violating the reality of the gauge
weight, Leg B). On the retained action surface, both are excluded by the
real-positive partition function.

The partition function is:

    Z = ∫ DU det(D + m) e^{−S_gauge}

Every factor is real and positive:
- det(D + m) > 0 (Leg A)
- e^{−S_gauge} > 0 (Leg B)

Therefore Z > 0 is real and positive. A θ-term `Z(θ) = ∫ DU det(D + m)
e^{−S_gauge + iθQ} would make Z complex for θ ≠ 0, contradicting the
real-positive structure of the retained action surface.

### Combined result

    θ_eff = θ_bare + arg det(M_u M_d) = 0 + 0 = 0

This is an action-surface structural prediction, not a dynamical relaxation
mechanism.

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

## Chiral Rotation Argument

In the Standard Model, the strong CP problem involves basis freedom:
a chiral rotation ψ → e^{iαγ₅} ψ can shift phase between θ_QCD and
arg det(M). The physical quantity θ_eff = θ_QCD + arg det(M) is
basis-independent, but the individual contributions are not.

In the Cl(3)/Z³ framework, this basis freedom does not exist because:

1. The staggered mass term m ψ̄ψ is real (H is real, all η_μ are real)
2. A chiral rotation would introduce a complex mass m e^{iα}, making
   the action complex
3. A complex action would violate the real-positive partition function
   established in Legs A and B
4. Therefore: no chiral rotation is available to redistribute phase
   between the mass term and the gauge sector

The reality of the staggered action is not a basis choice — it is a
structural property of the Cl(3)/Z³ framework (real Hamiltonian, real
staggered phases). The framework has no axial U(1) phase freedom.

## Extension to the Interacting Theory

The free-field CP result (CPT_EXACT_NOTE.md: [CP, H_free] = 0,
PASS = 53, FAIL = 0 on L = 4, 6, 8) extends to the interacting theory
at tree level:

1. Gauge action S_gauge is CP-even (Re Tr U_P is CP-even)
2. Fermion-gauge coupling S_f is CP-even (real staggered phases η_μ,
   covariant CP transform of U_μ)
3. Full action S = S_gauge + S_f is CP-even at tree level

The standard argument that CP-even actions generate only CP-even
effective operators applies, but an explicit one-loop verification
in the full gauge+fermion theory is not computed here. This is a
companion-level open item, not a gap in the θ = 0 argument (which
rests on the real-positive partition function, not on loop-level CP).

This partially addresses open item 1 of CPT_EXACT_NOTE.md for the CP
sector. A full one-loop computation would close it completely.

## S³ Topology

On S³, π₃(SU(3)) = Z, so instanton sectors with integer topological
charge Q exist in principle. The partition function is
Z = Σ_Q Z_Q with Z_Q ≥ 0 (real positive weights). Without a θ-phase,
all sectors contribute constructively. No spontaneous CP violation
occurs from the vacuum structure.

## 3+1D APBC Extension

The strong-CP question is intrinsically `3+1`-dimensional because the
continuum topological density is `F \tilde F`. The retained framework is also
`3+1` on its physical spacetime surface: spatial `Z^3` with a single temporal
direction and antiperiodic temporal boundary conditions from the
spin-statistics side of the anomaly-forced time closure.

The original determinant audit was carried out on the spatial `Z^3` surface.
The theorem is now strengthened by an explicit `3+1` APBC extension on
`4^3 x 4`:

- the staggered phases remain real in `3+1`
- the APBC boundary signs are also real
- the resulting `3+1` staggered Dirac operator stays anti-Hermitian on sampled
  `SU(3)` configurations
- `det(D + mI)` remains real positive on those sampled `3+1` configurations
- sampled clover topological-charge values vary while the determinant phase
  remains zero to machine precision

This is still not a full instanton-measure theorem. It is the narrower and
useful point needed here: the retained `θ_eff = 0` statement survives the
physically relevant `3+1` APBC lattice surface.

## Algebraic Extension of Leg A

Leg A is not just a numerical observation on a few sample configurations. The
anti-Hermiticity mechanism is structural:

1. the staggered phases `η_μ(x)` are real
2. the temporal APBC signs are real
3. the gauge links are unitary
4. the forward and backward hopping terms therefore remain exact Hermitian
   conjugates with opposite sign

So the same anti-Hermitian structure that gives determinant positivity on the
spatial audit surface extends directly to the retained `3+1` APBC operator
surface. The runner now verifies this numerically on sampled `3+1`
configurations as an explicit audit.

## What Is Actually Proved

### Exact (theorem-grade):

1. Anti-Hermiticity of staggered D[U] on Z³ with SU(3) links
2. Fermion determinant det(D + mI) is real and positive for real m > 0
3. Wilson plaquette Re Tr U_P is CP-even (Im Tr U_P is CP-odd)
4. Weak su(2) closes on the graph-first selected-axis fiber
5. Joint commutant of {su(2), τ} has dimension 10
6. Z₃ eigenvalues are discrete cube roots of unity
7. The axiom stack has 5 inputs, no room for θ
8. The determinant-positivity audit extends to the retained `3+1` APBC
   staggered operator surface on sampled `SU(3)` configurations

### Structural (logic-grade):

9. The anti-Hermitian determinant mechanism extends algebraically from the
   spatial surface to the retained `3+1` APBC surface
10. θ_bare = 0 because the gauge action is fully axiom-determined
11. arg det(M) = 0 because the staggered mass is real
12. θ_eff = 0 on the retained action surface
13. CP violation is confined to the weak sector via CKM

## External Consistency Support

These items strengthen the interpretation of the retained theorem surface, but
they are **not** promoted here as new framework-native closure theorems.

1. **Vafa-Witten consistency support.** The retained strong sector is
   vector-like and uses a real-positive fermion determinant, so the
   Vafa-Witten no-spontaneous-CP-breaking argument is consistent with the
   retained `θ_eff = 0` surface.

2. **Topological-sector consistency support.** In a confining large-volume
   regime, the standard extensive-free-energy argument gives Gaussian sector
   weights `Z_Q / Z_0 ~ exp(-Q^2 / (2 χ_t V))`. This is consistent with the
   retained `θ = 0` minimum, but the project does **not** yet claim a
   framework-native derivation of the full `Z_Q` measure on the physical
   `S^3` lattice.

## What Remains Open

1. **Neutron EDM bounded lane.** The framework predicts θ_eff = 0, hence
   d_n = 0 from QCD on the retained surface. The surviving CKM-only estimate
   is now tracked separately in
   [CKM_NEUTRON_EDM_BOUND_NOTE.md](CKM_NEUTRON_EDM_BOUND_NOTE.md)
   as a bounded lane using the promoted CKM package plus a standard
   EFT bridge.

2. **Lattice instanton measure.** While the partition sum
   Z = Σ_Q Z_Q is established, the detailed instanton measure Z_Q on
   the physical S³ lattice is not computed here.

3. **Radiative / chiral closure beyond support level.** The current repo has
   strong consistency support for radiative stability of the retained
   `θ_eff = 0` surface, but it does not yet promote a framework-native
   interacting chiral/anomaly closure theorem.

4. **Axion necessity beyond the retained action surface.** The theorem here is
   only that the retained action surface already gives `θ_eff = 0`. Whether
   broader axion-model exclusion follows is a separate question, not part of
   this theorem.

## How This Changes The Paper

This is a clean structural result on the retained action surface.
The statement is:

> The Cl(3)/Z³ framework predicts θ_eff = 0 as a structural
> consequence of the axiom-determined action. The staggered Dirac
> operator is anti-Hermitian with real mass, giving a real positive
> fermion determinant. The Wilson plaquette gauge action is CP-even.
> No bare θ-term appears on that retained action surface, and CP
> violation occurs exclusively in the weak sector through the discrete
> Z₃ source that generates the CKM phase.

This belongs in the main text alongside the exact CPT result. It
strengthens the paper's case that the framework fixes the retained action
surface tightly enough to remove a bare strong-sector CP phase there.

## Experimental Predictions

1. **θ_eff = 0 exactly.** No CP violation in the strong sector.
2. **Neutron EDM from QCD: d_n = 0.** The current bounded CKM-only
   estimate is `d_n ~ 8 x 10^-33 e cm`; any observed neutron EDM is therefore
   not sourced by a bare strong-sector `θ` on the retained action surface.
3. **No bare strong-sector CP phase on the retained action surface.**
   Any additional axion-style extension would be extra structure beyond the
   theorem proved here.

## References

- Vafa, C. and Witten, E. (1984). *Restrictions on Symmetry Breaking in
  Vector-Like Gauge Theories*, PRL 53, 535.
- Leutwyler, H. and Smilga, A. (1992). *Spectrum of Dirac operator and role of
  winding number in QCD*, PRD 46, 5607.
- Witten, E. (1979). *Current algebra theorems for the U(1) Goldstone boson*,
  Nucl. Phys. B 156, 269.
- Veneziano, G. (1979). *U(1) without instantons*, Nucl. Phys. B 159, 213.

## Commands Run

```
python3 scripts/frontier_strong_cp_theta_zero.py
# Exit code: 0
# PASS=60  FAIL=0
```
