# Route Portfolio

**Date:** 2026-05-16
**Loop:** koide-l5-spectral-triple-20260516

Five independent routes (one per counterfactual in
ASSUMPTIONS_AND_IMPORTS.md). Each route is independent: agents work in
parallel without coordinating. Synthesis happens after the fan-out.

## R1 — Schur Complement / Alternative γ-Grading

**Premise:** the spectral-triple γ-grading is NOT Γ_χ directly. Instead,
γ is a different (Z_2) grading on a larger Hilbert space H_ext, and the
required anti-commuting H on R³ emerges as a Schur complement when
projecting D onto the 3-gen subspace.

**Concrete starting point:** consider the 2-component Pauli σ_3 grading
on H = R³ ⊗ C² (3-gen ⊗ chirality). Build Dirac D = (1/3)(1⊗h + h⊗1) ⊗ σ_1
(off-diagonal in chirality). Then `{D, I⊗σ_3} = 0` automatically. Project
to the 3-gen subspace via partial trace / projector. Does the projected
matrix equal an H of the required form?

**Success criterion:** explicit (A, H, D, γ, J) on Cl(3)/Z³ ⊗ chirality
such that the projection to R³ gives the required anti-commuting H, with
h derived from framework primitives.

**Failure mode:** the projection averages out the h-dependence, giving
H = 0 or H ∝ Γ_χ.

## R2 — Tensored Connes-Lott Construction (R³ ⊗ H_extra)

**Premise:** D acts on R³ ⊗ H_extra where H_extra carries a Z_2 grading
γ_KO. The Dirac is of the form D = D_R³ ⊗ γ_KO + I_R³ ⊗ D_extra, and the
required anti-commuting structure emerges when restricting to the
γ_KO = ±1 eigenspaces.

**Concrete starting point:** standard Connes-Lott structure has algebra
A = A_L ⊕ A_R, Hilbert space H = H_L ⊕ H_R, D = off-diagonal Yukawa. For
Cl(3)/Z³, take A_L = A_R = Cl(3)/Z³ and D off-diagonal. Then
{D, γ = diag(I, -I)} = 0. The 3×3 block of D from H_L to H_R is the
candidate H.

**Success criterion:** the off-diagonal block has the required H form
with h derived from the Cl(3)/Z³ algebra structure (not fitted).

**Failure mode:** the off-diagonal block is generic Hermitian with no
Σh = 0 constraint, i.e., not in the 2-dim anti-commuting family.

## R3 — Infinite-dim Chamseddine-Connes / Spectral Action

**Premise:** the spectral triple is infinite-dim, with the 3-generation
triplet as the finite internal index. The Dirac is D = D_spatial ⊗ I +
γ_spatial ⊗ M where M is the finite Yukawa matrix on R³ ⊗ R³ (or larger
internal). Spectral action `Tr f(D²/Λ²)` reproduces the bosonic action,
and the equations of motion / minimum of the spectral action determines
the form of M.

**Concrete starting point:** Standard 4D Dirac D_4 = i γ^μ ∂_μ on a
manifold X, tensored with finite spectral triple (A_f, H_f, D_f) on
Cl(3)/Z³. Total D = D_4 ⊗ I + γ^5 ⊗ D_f. The required H is D_f.

**Success criterion:** the finite Yukawa D_f, derived from spectral action
on Cl(3)/Z³, has the anti-commuting form with h derived from algebra
structure.

**Failure mode:** D_f's minimum is degenerate / not the anti-commuting
form / requires PDG inputs to fix h.

## R4 — Complex 4-dim Search Space

**Premise:** the 3-generation triplet is C³, not R³. Hermitian H includes
complex off-diagonals. The space of complex Hermitian anti-commuting H
has 4 real dimensions (2 complex h components with Σh = 0). The lepton
mass-square-root vector v is taken as a real vector in C³, but H mixes
real and imaginary parts.

**Concrete starting point:** any complex 3×3 Hermitian H with Σ_g H_{gg}
appropriately constrained, anti-commuting with Γ_χ. Parametrize as
H = (1/3)(1⊗h_C + h_C^*⊗1) with h_C ∈ C³, Σh_C = 0. Check whether the
extra complex dimensions enable Connes-Lott constructions impossible in
real 2-dim.

**Success criterion:** a complex h_C derived from Cl(3) complex
structure (e.g., bivector eigenvalues being complex) realizes the
required H with the physical v as eigenvector.

**Failure mode:** the complex parameters give the same Koide closure but
add no new framework primitive.

## R5 — Twisted / Modular Spectral Triple (Z_3 Twist)

**Premise:** the γ-grading is Z_3, not Z_2. The Dirac D doesn't
anti-commute with γ — instead it satisfies a twisted relation
`D γ = ω γ D` where ω = exp(2πi/3) is the primitive 3rd root of unity.
This is the "twisted spectral triple" / "modular spectral triple"
generalization (Connes-Moscovici 2008).

**Concrete starting point:** take γ = R (the Z_3 generator). Construct
D such that DR = ωRD. Then D = a I + b R + c R² but with the constraint
that DR − ωRD = 0, i.e., (a + bR + cR²)R = ω R(a + bR + cR²), giving
b - ωa = 0, c - ωb = 0, a - ωc = 0. This is the 1-dim eigenspace of
the cyclic shift acting on (a, b, c). Solving: a/b/c form a single
Z_3-orbit.

**Success criterion:** the twisted Dirac D on Cl(3)/Z³ has eigenvectors
that satisfy Koide naturally (perhaps as a different operator-level
identity than LCC).

**Failure mode:** the twisted route doesn't connect to anti-commuting H
in the standard sense; it gives a different sharpening.

**Note:** This route is OUTSIDE the standard Connes anti-commutation
hypothesis. If R5 succeeds, the retained Level 4 theorem does NOT apply
directly — we'd need a new Level-4-like theorem for twisted spectral
triples. So R5 may produce a SIBLING chain, not extend the current one.

## Cross-Route Ranking (initial)

| Route | Retained-positive likely | Construction effort | Independent of NG-1 |
|---|---|---|---|
| R1 (Schur complement) | medium | medium | yes |
| R2 (Connes-Lott) | high (standard NCG) | medium | yes |
| R3 (Chamseddine-Connes) | medium-high | high (infinite-dim) | yes |
| R4 (Complex 4-dim) | low-medium (might not add structure) | low | yes |
| R5 (Twisted Z_3) | medium (different chain) | medium | YES — orthogonal |

Initial highest-leverage: **R2 (Connes-Lott)**. Most standard, most
likely to land cleanly if it works. R5 is the most ORTHOGONAL — if all
others fail, R5 may give a different chain entirely.

## Order of attack

Special-forces 5-agent fan-out (all in parallel). Each agent gets ONE
route + sharp yes/no deliverable. Synthesis after.
