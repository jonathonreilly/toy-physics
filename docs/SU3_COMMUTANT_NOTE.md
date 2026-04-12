# SU(3) as Commutant of SU(2)_weak + Z_2 in Taste Space

## Summary

Pure algebraic computation on C^8 = (C^2)^{otimes 3} shows that
**su(3) + u(1) is the unique commutant** of {SU(2)_weak, SWAP_23}
within End(C^8).  No physics assumptions are needed beyond the
tensor product structure of the staggered lattice taste space and
the identification of SU(2) with the first tensor factor.

## Setup

| Object | Definition | Dimension |
|--------|-----------|-----------|
| Taste space | C^8 = C^2 otimes C^2 otimes C^2 | 8 |
| SU(2)_weak generators | S_i = (sigma_i / 2) otimes I_2 otimes I_2 | 3 generators |
| SWAP_23 | Exchange of tensor factors 2 and 3 | 1 operator |
| Cl(3) generators (KS) | gamma_1 = sx.I.I, gamma_2 = sz.sx.I, gamma_3 = sz.sz.sx | 3 generators |

## Main Result

### Commutant hierarchy

| Constraint set | Commutant | Complex dim | Compact form |
|---------------|-----------|-------------|--------------|
| SU(2) only | gl(4,C) | 16 | u(4) |
| SU(2) + SWAP_23 | gl(3,C) + gl(1,C) | 10 | u(3) + u(1) |
| Full Cl(3) | Right Cl(3) | 8 | u(2) x u(2) |
| SU(2) + full Cl(3) | center | 4 | su(2) + u(1) |

### The key step: SWAP_23 forces the 3 + 1 split

The commutant of SU(2) acting on the first factor of C^2 otimes C^4 is
gl(4,C) = End(C^4), by Schur's lemma.

The SWAP operator on the C^4 = C^2 otimes C^2 factor (exchanging the
second and third tensor factors) decomposes C^4 into eigenspaces:

- **Sym^2(C^2) = C^3**: the symmetric subspace (SWAP eigenvalue +1)
- **Anti^2(C^2) = C^1**: the antisymmetric subspace (SWAP eigenvalue -1)

Any matrix in gl(4,C) that commutes with SWAP must preserve this
decomposition, giving **gl(3,C) + gl(1,C)**.

The compact subalgebra is **u(3) + u(1) = su(3) + u(1) + u(1)**.
Removing the overall U(1) phase (trace on C^8) leaves:

> **su(3)_color + u(1)_hypercharge**

This is exactly the Standard Model color + hypercharge structure.

## What does NOT work: full Cl(3)

The full Clifford algebra Cl(3) in the Kawamoto-Smit representation
spans all three tensor factors.  Its commutant has dimension 8
(the right Cl(3) copy), with compact form U(2) x U(2).

This is **too small** to contain SU(3): the full Cl(3) constraint
is too strong.  The dimension sequence 16 -> 10 -> 8 shows that
SU(3) + U(1) sits strictly between the SU(2) commutant and the
Cl(3) commutant.

No single element of Cl(3), nor any pair, produces dimension 9 or 10.
The Cl(3) constraints always jump directly from 16 to 8 (adding one
odd element drops from 16 to 8; adding a second odd element drops to 4).

## Physical interpretation

### What SWAP_23 means on the lattice

On the staggered lattice with three spatial dimensions, the three
tensor factors in (C^2)^{otimes 3} correspond to the three spatial
directions.  SWAP_23 is the **transposition of spatial directions
2 and 3** -- a discrete spatial symmetry.

This is physically natural: if the lattice has a Z_2 symmetry
exchanging two spatial directions (e.g., a reflection or rotation
in the 2-3 plane), then the gauge symmetry must commute with it.

### The 3 + 1 decomposition

The symmetric subspace Sym^2(C^2) = C^3 carries the **color triplet**.
The antisymmetric subspace Anti^2(C^2) = C^1 carries the **color singlet**.

The full fermion representation is:

    C^8 = C^2_weak otimes (C^3_color + C^1_singlet)
         = (2, 3) + (2, 1)

This is precisely the left-handed quark doublet (2, 3) plus the
lepton doublet (2, 1) in the Standard Model.

### Why SU(3) and not SU(4)

Without SWAP_23, the commutant of SU(2) is gl(4,C), whose compact
form is u(4) with semisimple part su(4).  The SWAP symmetry breaks
SU(4) -> SU(3) x U(1) by distinguishing the symmetric and antisymmetric
subspaces.

This is the **same mechanism** as the Georgi-Glashow SU(5) breaking
pattern, but here it arises from a discrete spatial symmetry rather
than a Higgs field.

## Numerical verification

All results verified by explicit linear algebra in
`scripts/frontier_su3_commutant.py`:

1. SU(2) generators satisfy [S_i, S_j] = i epsilon_{ijk} S_k -- VERIFIED
2. Cl(3) generators satisfy {gamma_i, gamma_j} = 2 delta_{ij} -- VERIFIED
3. dim Comm(SU(2)) = 16 -- VERIFIED (Schur's lemma)
4. dim Comm(SU(2) + SWAP_23) = 10 = dim(gl(3) + gl(1)) -- VERIFIED
5. dim Comm(Cl(3)) = 8 (double commutant: 8 x 8 = 64) -- VERIFIED
6. SWAP_23 commutes with SU(2): YES -- VERIFIED
7. SWAP_23 does NOT commute with L_2, L_3: confirmed -- VERIFIED
8. Explicit SU(3) x U(1) generators commute with SU(2) + SWAP: YES -- VERIFIED
9. Systematic search: no Cl(3) subset gives dim 9 -- VERIFIED

## Statement of the theorem

**Theorem.** Let V = (C^2)^{otimes 3} and let SU(2) act on the first
tensor factor via S_i = (sigma_i/2) otimes I_2 otimes I_2.
Let SWAP_23 be the transposition of factors 2 and 3.  Then:

1. The commutant of {S_1, S_2, S_3, SWAP_23} in End(V) is
   gl(3, C) oplus gl(1, C), with complex dimension 10.

2. The maximal compact subalgebra is u(3) oplus u(1).

3. The traceless compact subalgebra is **su(3) oplus u(1)**.

4. This is the unique gauge algebra compatible with both SU(2)_weak
   and the Z_2 spatial symmetry on the staggered lattice taste space.
