# SU(3) Commutant Theorem: Basis-Free Proof

**Status:** FORMAL THEOREM -- paper appendix material
**Date:** 2026-04-12

## Statement

**Theorem (SU(3) Commutant).** Let Z^3 be the cubic lattice with
staggered fermion phases eta_mu(x) = (-1)^{x_1 + ... + x_{mu-1}}.
Then:

1. The staggered phases determine, via the Kawamoto-Smit construction,
   a canonical tensor product decomposition of the 8-dimensional taste
   space: V = C^2_1 tensor C^2_2 tensor C^2_3, where each factor
   corresponds to a spatial direction.

2. Each choice of distinguished direction mu_0 in {1, 2, 3} defines
   an su(2) subalgebra acting on the factor C^2_{mu_0}, with
   4-dimensional multiplicity space W = C^2 tensor C^2 (the product
   of the remaining two factors).

3. The transposition of the two non-distinguished directions acts as
   the SWAP operator on W. This SWAP commutes with the distinguished
   su(2).

4. The multiplicity space decomposes canonically under SWAP as
   W = Sym^2(C^2) + Anti^2(C^2) = C^3 + C^1.

5. The compact semisimple commutant of {su(2), SWAP} in End(V)
   is uniquely su(3).

6. The unique traceless U(1) generator in the commutant is hypercharge,
   with eigenvalues Y = +1/3 (on C^3, quarks) and Y = -1 (on C^1,
   leptons).

---

## Proof

### Step 1. Staggered phases and the canonical tensor decomposition

**Claim.** The Kawamoto-Smit representation of the staggered fermion
phases on Z^3 canonically identifies the 8-dimensional taste space
with V = C^2 tensor C^2 tensor C^2, where the mu-th tensor factor
corresponds to the mu-th spatial direction.

*Proof.* The 2^3 = 8 corners of a single hypercube of Z^3 are labeled
by bit strings alpha = (a_1, a_2, a_3) with a_mu in {0, 1}. This
labeling defines a canonical identification

    V = C^{2^3} = C^2_1 tensor C^2_2 tensor C^2_3

where the mu-th tensor factor has basis {|0>, |1>} corresponding to
the mu-th bit of the hypercube corner label.

The staggered fermion phases eta_mu(x) = (-1)^{x_1 + ... + x_{mu-1}}
define shift operators Gamma_mu on V via the Kawamoto-Smit construction:

    (Gamma_mu psi)(alpha) = eta_mu(alpha) psi(alpha + hat{mu})

where the shift alpha + hat{mu} flips the mu-th bit. In the tensor
product basis, these operators take the explicit form:

    Gamma_mu = sigma_z^{tensor(mu-1)} tensor sigma_x tensor I^{tensor(3-mu)}

*Verification:* For Gamma_1 = sigma_x tensor I tensor I, the shift
flips bit 1, and there is no sign factor (eta_1 = 1 always). For
Gamma_2 = sigma_z tensor sigma_x tensor I, the shift flips bit 2,
and the sign factor eta_2 = (-1)^{a_1} is implemented by sigma_z on
factor 1. For Gamma_3 = sigma_z tensor sigma_z tensor sigma_x, the
shift flips bit 3, and eta_3 = (-1)^{a_1 + a_2} requires sigma_z on
both factors 1 and 2.

The Clifford relations {Gamma_mu, Gamma_nu} = 2 delta_{mu nu} I
follow from sigma_x^2 = I, sigma_z^2 = I, and
{sigma_x, sigma_z} = 0.

**Uniqueness of the tensor decomposition.** The tensor product
structure V = C^2_1 tensor C^2_2 tensor C^2_3 is determined by the
hypercube labeling, which is canonical once the coordinate axes of Z^3
are specified. The assignment of tensor factors to spatial directions
is equivariant under the axis permutation group S_3: a permutation
pi in S_3 of the coordinates induces a permutation of the tensor
factors. QED


### Step 2. Distinguished su(2) from a choice of direction

**Claim.** Each choice of a distinguished spatial direction mu_0
defines an su(2) subalgebra of End(V) that acts on the factor
C^2_{mu_0} and trivially on the remaining factors.

*Proof.* Choose (without loss of generality) mu_0 = 1. Define

    T_k = (sigma_k / 2) tensor I_2 tensor I_2,   k = 1, 2, 3

where sigma_1 = sigma_x, sigma_2 = sigma_y, sigma_3 = sigma_z are
the Pauli matrices. These satisfy

    [T_i, T_j] = i epsilon_{ijk} T_k

because [sigma_i/2, sigma_j/2] = i epsilon_{ijk} sigma_k/2 and the
identity factors contribute nothing to the commutator.

Note that T_1 = Gamma_1 / 2 (since Gamma_1 = sigma_x tensor I tensor I),
so one of the su(2) generators is directly a Clifford element. The
other two generators T_2 and T_3 involve sigma_y and sigma_z on the
first factor, which are NOT elements of the Clifford algebra Cl(3).
They are, however, canonical operators determined by the tensor product
structure.

Under this su(2), the taste space decomposes as

    V = C^2_1 tensor W,   W = C^2_2 tensor C^2_3 = C^4

where su(2) acts irreducibly (as spin-1/2) on C^2_1, and W is the
4-dimensional multiplicity space. Every state in V transforms as one
of 4 copies of the spin-1/2 representation. QED


### Step 3. The SWAP operator on the multiplicity space

**Claim.** The transposition (23) of the two non-distinguished
directions defines a SWAP operator on W = C^2_2 tensor C^2_3 that
commutes with the distinguished su(2).

*Proof.* Define SWAP_{23}: V -> V by

    SWAP_{23}(|a> tensor |b> tensor |c>) = |a> tensor |c> tensor |b>

for all |a> in C^2_1, |b> in C^2_2, |c> in C^2_3. Equivalently,

    SWAP_{23} = I_2 tensor P

where P: C^2_2 tensor C^2_3 -> C^2_2 tensor C^2_3 is the swap
operator P(|b> tensor |c>) = |c> tensor |b>.

Since SWAP_{23} acts as the identity on C^2_1, it commutes with all
operators of the form T tensor I_4 on V = C^2_1 tensor C^4. In
particular, [SWAP_{23}, T_k] = 0 for all k.

Properties of SWAP_{23}:
- SWAP_{23}^2 = I (involution)
- SWAP_{23} is Hermitian (self-adjoint)
- SWAP_{23} is unitary

These follow from the corresponding properties of the swap P on
C^2 tensor C^2. QED


### Step 4. Symmetric/antisymmetric decomposition of multiplicity space

**Claim.** Under SWAP_{23}, the multiplicity space W = C^2 tensor C^2
decomposes as

    W = Sym^2(C^2) + Anti^2(C^2) = C^3 + C^1.

*Proof.* The swap operator P on C^2 tensor C^2 satisfies P^2 = I, so
its eigenvalues are +1 and -1. The eigenspaces are:

    Sym^2(C^2) = {w in C^2 tensor C^2 : P(w) = +w}  (symmetric tensors)
    Anti^2(C^2) = {w in C^2 tensor C^2 : P(w) = -w}  (antisymmetric tensors)

The projectors onto these subspaces are P_+ = (I + P)/2 and
P_- = (I - P)/2.

**Dimension count:** For C^n tensor C^n in general,
dim Sym^2(C^n) = n(n+1)/2 and dim Anti^2(C^n) = n(n-1)/2.
For n = 2: dim Sym^2 = 3, dim Anti^2 = 1.

A basis for Sym^2(C^2):

    |00>,   (|01> + |10>)/sqrt(2),   |11>

A basis for Anti^2(C^2):

    (|01> - |10>)/sqrt(2)

This decomposition is canonical: it depends only on the swap operator P,
which is uniquely determined by the tensor product structure. No basis
choice is required. QED


### Step 5. su(3) as the unique compact semisimple commutant

**Claim.** The compact semisimple part of the commutant of
{su(2), SWAP_{23}} in End(V) is su(3).

*Proof.* We proceed in three sub-steps.

**(5a) Commutant of su(2) alone.**

By Schur's lemma, since su(2) acts irreducibly on the factor C^2_1
in V = C^2_1 tensor W, every operator commuting with all T_k has the
form I_2 tensor M for some M in End(W). Therefore

    Comm_{End(V)}(su(2)) = {I_2 tensor M : M in End(W)} = I_2 tensor M(4, C).

This is isomorphic to gl(4, C) as an associative algebra
(complex dimension 4^2 = 16).

**(5b) Adding SWAP_{23}.**

An operator A = I_2 tensor M in Comm(su(2)) also commutes with
SWAP_{23} = I_2 tensor P if and only if M commutes with P:

    [I_2 tensor M, I_2 tensor P] = I_2 tensor [M, P] = 0
    <==> [M, P] = 0.

Since P is diagonalizable with eigenvalues +1 (on Sym^2 = C^3) and
-1 (on Anti^2 = C^1), an operator M in End(W) commutes with P if
and only if M preserves the decomposition W = Sym^2 + Anti^2. That
is, M must be block diagonal in the Sym/Anti decomposition.

Therefore:

    Comm(su(2), SWAP_{23}) = I_2 tensor [End(Sym^2) + End(Anti^2)]
                            = I_2 tensor [M(3, C) + M(1, C)]
                            = I_2 tensor [gl(3, C) + gl(1, C)].

This has complex dimension 3^2 + 1^2 = 10.

**(5c) Extracting the compact semisimple part.**

The reductive Lie algebra of the unitary (compact) form is

    u(3) + u(1) = [su(3) + u(1)_{center}] + u(1).

The overall scalar multiples of I_8 account for one u(1).
The center of u(3) provides another u(1). The compact semisimple
part -- meaning the maximal semisimple subalgebra of the compact
form -- is **su(3)**.

This is unique because:

(i) gl(3, C) has a unique semisimple part, namely sl(3, C)
(the traceless matrices);

(ii) The compact real form of sl(3, C) is su(3);

(iii) gl(1, C) is abelian, contributing no semisimple part.

Therefore the compact semisimple commutant is su(3). QED


### Step 6. Hypercharge from the traceless U(1) constraint

**Claim.** There is a unique traceless U(1) generator in the commutant,
and it has eigenvalues +1/3 (with multiplicity 6) and -1 (with
multiplicity 2). This is the hypercharge generator.

*Proof.* The center of the commutant algebra I_2 tensor [gl(3) + gl(1)]
is spanned by two elements:

    Z_+ = I_2 tensor Pi_+   (the projector onto C^2 tensor Sym^2 = C^6)
    Z_- = I_2 tensor Pi_-   (the projector onto C^2 tensor Anti^2 = C^2)

where Pi_+ = (I_4 + P)/2 and Pi_- = (I_4 - P)/2 are the projectors
on the multiplicity space W.

Note Z_+ + Z_- = I_8. Any central generator is Y = a Z_+ + b Z_-
for constants a, b in R (restricting to Hermitian generators).

The tracelessness condition Tr(Y) = 0 gives:

    a * 6 + b * 2 = 0   =>   b = -3a.

So the traceless central generator is unique up to normalization:

    Y = a(Z_+ - 3 Z_-) = a(4 Z_+ - 3 I_8).

Normalizing so that the eigenvalue on the Anti^2 (singlet) subspace
is -1, we set b = -1, hence a = 1/3:

    Y has eigenvalue +1/3 on C^2 tensor Sym^2 = C^6  (multiplicity 6)
    Y has eigenvalue -1   on C^2 tensor Anti^2 = C^2  (multiplicity 2)

This matches the Standard Model hypercharge assignment for one
generation of left-handed fermions:

    Left-handed quarks:  weak doublet x color triplet, Y = +1/3
    Left-handed leptons: weak doublet x color singlet, Y = -1

The uniqueness of Y (up to overall normalization) follows from the
one-dimensionality of the traceless part of the center. QED

---

## Summary of the logical chain

    Staggered phases on Z^3
        => KS representation on C^8 = C^2 x C^2 x C^2  [Step 1]
        => choose distinguished direction mu_0 = 1  [INPUT]
        => su(2) on first factor, multiplicity W = C^4  [Step 2]
        => SWAP_{23} commutes with su(2)  [Step 3]
        => W = C^3 + C^1 (Sym + Anti)  [Step 4]
        => Comm(su(2), SWAP) = gl(3) + gl(1)  [Step 5]
        => compact semisimple part = su(3)  [Step 5]
        => traceless U(1) = hypercharge  [Step 6]

---

## Relation to the Clifford algebra

The Kawamoto-Smit Clifford generators Gamma_mu are related to but
distinct from the su(2) generators used above:

- Gamma_1 = sigma_x tensor I tensor I = 2 T_1 (a Clifford element)
- T_2 = sigma_y/2 tensor I tensor I (NOT in Cl(3))
- T_3 = sigma_z/2 tensor I tensor I (NOT in Cl(3))

The full su(2) used in the proof requires the tensor product structure
provided by the KS representation, not just the Clifford algebra.

The bivector algebra B_k = -(i/2) epsilon_{ijk} Gamma_i Gamma_j
forms a DIFFERENT su(2) that couples multiple tensor factors and
does NOT commute with SWAP_{23}. The two su(2) algebras (T_k and B_k)
are independent 3-dimensional subalgebras of End(C^8).

This distinction is important: the theorem uses the tensor product
structure of the KS representation (which is canonical given the lattice
coordinates), not just the abstract Clifford algebra Cl(3).

---

## Relation to Standard Model structure

The full 8-dimensional representation decomposes as:

    C^8 = (2, 3)_{1/3} + (2, 1)_{-1}

under SU(2)_weak x SU(3)_color x U(1)_Y. This is precisely one
generation of left-handed fermions in the Standard Model:

| Subspace | dim | SU(2) | SU(3) | Y | Particles |
|----------|-----|-------|-------|---|-----------|
| C^2 tensor Sym^2(C^2) | 6 | 2 | 3 | +1/3 | (u_L, d_L) in 3 colors |
| C^2 tensor Anti^2(C^2) | 2 | 2 | 1 | -1 | (nu_L, e_L) |

---

## Assumptions and scope

1. **Input:** staggered fermion phases on Z^3 (standard lattice QCD construction).
2. **Choice:** identification of direction 1 as the weak isospin axis.
   This is the lattice analog of electroweak symmetry breaking.
3. **Output:** SU(3)_color x U(1)_Y with correct quantum numbers.
4. **Not derived:** why direction 1 is special (this is EW symmetry
   breaking); the existence of three generations; right-handed fermion
   representations.
5. **Scope:** This is a KINEMATIC result about the symmetry structure
   of the taste space. It does not address dynamics (confinement,
   mass generation, etc.).

---

## References

- Kawamoto, N. and Smit, J. "Effective Lagrangian and dynamical symmetry
  breaking in strongly coupled lattice QCD." Nucl. Phys. B192 (1981) 100.
- Atiyah, M.F., Bott, R., and Shapiro, A. "Clifford modules."
  Topology 3, suppl. 1 (1964) 3-38.
- Lawson, H.B. and Michelsohn, M.L. "Spin Geometry."
  Princeton University Press (1989). Ch. I for Clifford algebra
  classification.
