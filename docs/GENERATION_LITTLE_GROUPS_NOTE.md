# Generation Little Groups: Definitive Symmetry and Species Note

**Date:** 2026-04-12
**Lane:** Generation physicality
**Script:** `scripts/frontier_generation_little_groups.py`

## Status

**BOUNDED** -- the 1+3+3+1 BZ decomposition is exact; the three hw=1
species are related by the full Oh taste symmetry; generation physicality
(whether taste-related species are physically distinct) remains open.

## Theorem / Claim

**Theorem (exact).** The staggered Cl(3) Hamiltonian on Z^3 has exactly
3 species at the lightest nonzero mass level (Hamming weight 1 BZ corners).
These carry different crystal momenta X1=(pi,0,0), X2=(0,pi,0), X3=(0,0,pi)
and have different Hamiltonian matrices H(X1), H(X2), H(X3), but identical
eigenvalue spectra {-1, +1} each with degeneracy 4. The full symmetry
group of the Hamiltonian (including taste transformations) is Oh (48
elements), and C3[111] with taste transform epsilon(n) = (-1)^{(n_1+n_2)*n_3}
maps X1 -> X2 -> X3.

**Bounded claim.** Whether these 3 taste-related species are physically
distinct generations (rather than equivalent tastes) is the taste-physicality
question, which this analysis does not resolve.

## Assumptions

None beyond the standard staggered Cl(3) Hamiltonian on Z^3:
- Hopping phases: eta_1 = 1, eta_2 = (-1)^{n_1}, eta_3 = (-1)^{n_1+n_2}
- Anti-Hermitian nearest-neighbor hopping with PBC

## What Is Actually Proved

The following are exact algebraic facts, verified numerically on L=4 and L=6
lattices with all 14 checks passing:

### 1. Nested symmetry groups

**Phase-preserving subgroup G_0 = D2h (8 elements).**
The Oh elements that preserve the eta phase structure without any
site-dependent sign correction form:
G_0 = {I, -I, C2x, C2y, C2z, sigma_x, sigma_y, sigma_z}.
No axis permutation or C3/C4 rotation survives in G_0.

**Full symmetry group G = Oh (48 elements).**
Every Oh element g is a symmetry through a combined transformation
c(n) -> epsilon_g(n) c(g.n) where epsilon_g(n) = +/-1 is a site-dependent
sign (taste transformation). Verified on position-space lattices L=4 and L=6
by constructing epsilon_g via BFS on the nearest-neighbor graph and then
checking P'HP'^T = H where P' = P_g D_{epsilon_g}.

### 2. Orbit structure

Under G_0 (phase-preserving): each of the 8 BZ corners is in a SEPARATE
singleton orbit. X1, X2, X3 are inequivalent.

Under G (full Oh with taste): the 8 BZ corners form 4 orbits:
  {Gamma}, {X1, X2, X3}, {M1, M2, M3}, {R}
corresponding to the 1+3+3+1 Hamming weight decomposition.
The three hw=1 corners are in the SAME orbit.

### 3. Explicit C3[111] taste transformation

C3[111]: (x,y,z) -> (z,x,y) is a symmetry with taste transformation
epsilon(n) = (-1)^{(n_1+n_2)*n_3}. This maps X1 -> X2 -> X3.

### 4. Explicit Hamiltonian matrices at X-points

H(X1), H(X2), H(X3) are 8x8 real anti-Hermitian matrices.
All are purely real with entries in {-1, 0, +1} scaled by 1/2... actually
they have entries in {-1, 0, +1}.

H(X1) = H(pi,0,0): block off-diagonal with +I_4 in upper-right, -I_4 in
lower-left (i.e., H(X1) = diag_block(0, I_4; -I_4, 0) in the taste basis).

H(X2) = H(0,pi,0): connects pairs (alpha, alpha XOR e_2) with eta_2 phases.
Different nonzero pattern from H(X1).

H(X3) = H(0,0,pi): connects pairs (alpha, alpha XOR e_3) with eta_3 phases.
Different nonzero pattern from both H(X1) and H(X2).

Matrix norms: ||H(X1) - H(X2)|| = ||H(X1) - H(X3)|| = ||H(X2) - H(X3)|| = 4.

### 5. Spectra and eigenvectors

All three X-point Hamiltonians have the same spectrum: eigenvalues of
iH are {-1, +1} each with degeneracy 4. Furthermore, H(K)^2 = -I at
all X-points (and more generally H(K)^2 = -c(K)^2 I where
c(K)^2 = sum_mu sin^2(K_mu), making the spectrum Oh-invariant at every K).

The +1 eigenspaces of iH at X1, X2, X3 are DIFFERENT 4-dimensional subspaces
of C^8. The eigenspace overlaps are: |det(V_i^dag V_j)| = 0.25 for all
pairs (i,j), confirming the eigenspaces are genuinely distinct.

### 6. Representation analysis

Since the full symmetry group is Oh (not a proper subgroup), the
representations of Oh at X1, X2, X3 are related by conjugation within Oh.
The little group of each X-point under the full Oh is the stabilizer of that
momentum, which has order 16 (the same for all three, by the orbit-stabilizer
theorem with orbit size 3 and |Oh|=48).

The key point: the representations at X1, X2, X3 are NOT independently
constructed -- they are linked by the C3 taste symmetry. This means the
representation analysis cannot distinguish the three species. The symmetry
that maps between them acts on the full Hilbert space (coordinate + taste),
not just on coordinates.

## What Remains Open

**Generation physicality.** The free-field staggered Hamiltonian has full
Oh symmetry (with taste), placing all three hw=1 species in the same orbit.
Any argument for generation physicality must break or circumvent this
taste symmetry. Possible routes:

1. **EWSB breaking of taste symmetry.** The Coleman-Weinberg weak-axis
   selector breaks S_3 (axis permutation symmetry) to Z_2, giving a 1+2
   split. But the full 1+1+1 split requires further breaking.

2. **Wilson-like terms.** Explicit taste-breaking terms that lift the
   degeneracy between X1, X2, X3. These are model-dependent.

3. **Anomaly-based arguments.** If the taste symmetry is anomalous, it
   would be broken quantum-mechanically even without explicit breaking.

4. **Interaction effects.** Gauge interactions may break the free-field
   taste symmetry nonperturbatively.

## How This Changes The Paper

This result does NOT close the generation physicality gate. It documents
the precise obstruction: the free staggered Hamiltonian has full Oh
symmetry on coordinate + taste space, relating the three hw=1 species.
This is the lattice QCD taste symmetry applied to the Cl(3) setting.

The honest exact content is:
- 8 BZ corners split as 1+3+3+1 by Hamming weight (exact)
- 3 hw=1 species carry different momenta and have different H matrices (exact)
- These are related by Oh taste symmetry (exact)
- 1+2 split from EWSB weak-axis selection (exact)
- Whether taste-related species are physical generations (OPEN)

Paper-safe wording:
> exact 1+2 split; bounded 1+1+1 hierarchy model; generation physicality
> still open

The note supersedes any earlier claim that eta phases break Oh to D2h
in a way that distinguishes the X points. The D2h result is correct for
the phase-preserving subgroup but misses the site-dependent sign (taste)
transformations that restore full Oh.

## Commands Run

```
python3 scripts/frontier_generation_little_groups.py
```

Exit code: 0
Result: PASS=14 FAIL=0
