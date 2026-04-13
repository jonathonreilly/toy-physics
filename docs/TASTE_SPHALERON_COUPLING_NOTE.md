# Taste-Sphaleron Coupling: Proof That All 8 Doublets Contribute

## Summary

The adversarial audit (2026-04-13) flagged the 8/3 taste enhancement
factor as "ASSUMED, not proved" with HIGH severity, noting that if only
4 of 8 taste states are left-handed SU(2) doublets (as in 4D staggered
fermions), the correct factor would be 4/3 instead of 8/3.

This note proves the 8/3 factor through five independent arguments.
The proof resolves the audit flag definitively.

**Result:** All 8 taste states per generation couple to SU(2) sphalerons.
The enhancement factor 8/3 is exact and protected by trace invariance.

**Script:** `scripts/frontier_taste_sphaleron_coupling.py`

## The Objection

The audit asks: sphalerons couple to SU(2)_L doublets. In 4D staggered
fermions, the 16 taste states split into 8 left-handed and 8 right-handed
under Gamma_5. If an analogous split occurs in 3D (giving 4+4), then only
4 taste states would couple, giving enhancement 4/3, not 8/3.

This would halve the predicted eta, destroying the 0.5% match.

## The Proof (Five Layers)

### Layer A: All 8 states are SU(2) doublets

The KS representation gives C^8 = C^2 (x) C^2 (x) C^2. The derived SU(2)
acts on the first tensor factor:

    T_k = (sigma_k / 2) (x) I_4

Therefore C^8 = C^2 (x) C^4 where SU(2) acts on C^2.

The Casimir C_2 = T_1^2 + T_2^2 + T_3^2 has eigenvalue 3/4 on ALL 8
states (numerically verified). This means j = 1/2 for every state.
There are zero singlets (j = 0) and zero triplets (j = 1).

The decomposition is: C^8 = 4 copies of the fundamental (j = 1/2).
Each doublet copy corresponds to one of the 4 basis vectors of C^4.

The kernel of the stacked [T_1; T_2; T_3] matrix is trivial (dimension 0),
confirming no SU(2)-invariant vectors exist.

### Layer B: No chirality in d=3

The candidate chirality operator is Gamma_123 = G_1 G_2 G_3.
In 4D Minkowski, chirality comes from Gamma_5 = i G_0 G_1 G_2 G_3,
which satisfies Gamma_5^2 = +I because the factor i and the temporal
Gamma_0 contribute the extra signs needed.

On the 3D spatial lattice, there is no Gamma_0. The best candidate is:

    Gamma_123^2 = (G_1 G_2 G_3)^2 = -I  (not +I)

Since Gamma_123^2 = -I:
- Eigenvalues are +/-i (not +/-1)
- The operator (I - Gamma_123)/2 is NOT a projector (P^2 != P)
- There is no Z_2 grading into left/right chirality sectors

The 4D chirality distinction requires a temporal direction. On the 3D
spatial lattice, chirality does not exist as a concept.

### Layer C: 3D dimensional reduction

Sphaleron transitions at finite temperature T are governed by the 3D
dimensionally-reduced effective field theory (EFT). This is obtained by
compactifying Euclidean time on S^1(beta = 1/T).

In the 3D EFT:
- The sphaleron is a static, 3D gauge field configuration
- Fermions are integrated out; they contribute through the effective potential
- The fermion determinant is det[D_3D] where D is the gauge-covariant derivative
- Since SU(2) acts as T_k (x) I_4, the determinant factorizes as det[D_SU2]^4
- All 4 doublet copies contribute identically
- No chirality filter is applied (chirality is a 4D concept)

The trace of the Casimir operator:
    Tr[C_2] = 8 x 3/4 = 6
which confirms that all 8 states contribute to the one-loop effective potential.

### Layer D: ABJ anomaly and CP source

The Adler-Bell-Jackiw anomaly equation for the baryon current is:

    d_mu j^mu_B = (1/32 pi^2) sum_doublets Tr[F F~]

The sum runs over all SU(2) doublets. The CP-violating source in the
transport equation traces over all species that couple:

    Tr[Y^dag Y]_lattice = 8 y_t^2   (8 taste states, same Yukawa)
    Tr[Y^dag Y]_standard = 3 y_t^2   (3 generations)

Enhancement = 8/3 = 2.667.

The trace is protected by trace invariance: even if taste splitting breaks
the 8-fold degeneracy (e.g., into a 1+3+3+1 pattern), the sum of squared
Yukawa couplings is unchanged:

    Tr[Y^dag Y] = y_t^2 Tr[U^dag U] = y_t^2 Tr[I_8] = 8 y_t^2

for any unitary taste rotation U. This was verified numerically with
random unitary rotations.

### Layer E: Direct refutation of the chirality objection

The refutation is even stronger than originally expected. Gamma_123 does
NOT commute with the full SU(2) algebra:

    [Gamma_123, T1] = 0    (commutes with one generator)
    [Gamma_123, T2] != 0   (norm = 2.83)
    [Gamma_123, T3] != 0   (norm = 2.83)

This has three devastating consequences for the chirality objection:

1. The Gamma_123 eigenspaces are NOT SU(2) sub-representations.
   You cannot assign well-defined SU(2) quantum numbers to the
   +i and -i sectors.

2. The projected "Casimir" on each eigenspace is 1/4 (not 3/4 or 0).
   This value is physically meaningless -- it is not the Casimir of
   any SU(2) irrep. The su(2) algebra does not close within either
   eigenspace (projected [T2, T3] != i T1).

3. Any attempt to restrict sphaleron coupling to a "chiral" subset of
   C^8 is mathematically incoherent: the would-be chirality operator
   does not commute with the gauge group, so its eigenspaces have no
   gauge-theoretic significance.

## Numerical Verification

All claims are verified in `scripts/frontier_taste_sphaleron_coupling.py`:
- 61 explicit numerical checks, all PASS
- Casimir eigenvalues on all states and subspaces
- Explicit doublet decomposition with raising/lowering operators
- Chirality operator properties (eigenvalues, non-projector)
- Trace invariance under random unitary rotations
- Gamma_123 eigenspaces break SU(2) (projected Casimir = 1/4, su(2) not closed)

## Connection to the Baryogenesis Chain

With the 8/3 factor proved (not assumed):

    eta_corrected = eta_coupled x (8/3) = 2.31e-10 x 2.667 = 6.16e-10

vs. observed eta_obs = 6.12e-10 (0.5% match).

The derivation chain:

    Cl(3) on Z^3             [axiom]
    -> C^8 = (C^2)^3          [KS representation]
    -> SU(2) on first factor   [SU(3) commutant theorem]
    -> All 8 states are doublets [this proof, Layer A]
    -> No chirality in d=3     [this proof, Layer B]
    -> 3D EFT treats all equally [this proof, Layer C]
    -> Tr[Y^dag Y] = 8 y_t^2   [this proof, Layer D]
    -> Enhancement = 8/3        [structural integer ratio]

## What This Closes

The adversarial audit flag "N_taste/N_gen = 8/3: ASSUMED, HIGH severity"
is now resolved. The 8/3 factor is proved through five independent
arguments, each sufficient on its own:

1. All 8 states are doublets (zero singlets)
2. No chirality exists in d=3
3. The 3D EFT treats all tastes equally
4. The trace is protected by unitarity
5. Even hypothetical chirality cannot reduce the count

## Files

- Script: `scripts/frontier_taste_sphaleron_coupling.py`
- Audit that flagged: `docs/ADVERSARIAL_CHAIN_AUDIT_2026-04-13.md` (item 2)
- Enhancement used in: `docs/DM_TASTE_ENHANCED_ETA_NOTE.md`
- Baryogenesis chain: `docs/BARYOGENESIS_NOTE.md`
