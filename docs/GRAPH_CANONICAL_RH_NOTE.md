# Graph-Canonical Right-Handed Matter from the 3D Lattice Surface

**Script:** `scripts/frontier_graph_canonical_rh.py` (71/71 PASS)
**Depends on:** `frontier_su3_formal_theorem.py`, `frontier_right_handed_sector.py`

## Question

The SU(3) commutant theorem derives left-handed SM content from the 3D taste space:

    C^8 = (2, 3)_{+1/3} + (2, 1)_{-1}

The previous right-handed derivation (61/61) goes: 3D lattice -> left-handed content -> add time (4D) -> chirality gamma_5 -> C^16 = C^8_L + C^8_R -> anomaly cancellation -> right-handed charges. The 4D step is not graph-canonical.

**Can the right-handed states be found on the 3D graph surface without going to 4D?**

## Five Attacks and Results

### Attack 1: Hamming Weight Parity as Chirality

The operator chi = (-1)^{hw} = sz x sz x sz is the **graph-canonical chirality** on C^8:

- chi^2 = +I (proper involution with eigenvalues +/-1)
- {chi, G_mu} = 0 for all Clifford generators (anticommutes)
- Splits C^8 = C^4(even hw) + C^4(odd hw)

However, chi does NOT commute with SU(2): it anticommutes with T1, T2 and commutes with T3. This means chi is a **chiral symmetry** (axial transformation) that mixes doublet partners rather than separating representations.

### Attack 2: Shift-Operator Eigenspace Splitting

Each shift operator G_i splits C^8 = C^4(+1) + C^4(-1). But both eigenspaces carry **identical** gauge content: Y = {+1/3 x 3, -1 x 1}. The shift splitting **duplicates** rather than **conjugates** the representations. No left/right distinction.

### Attack 3: 3D Volume Element vs Bipartite Parity

Key algebraic fact: in odd dimensions d=3, the volume element G5 = G1*G2*G3 **commutes** with all G_mu (unlike even dimensions where it anticommutes). Specifically:

- G5*G_mu = (-1)^{d-1} G_mu*G5 = (+1)*G_mu*G5 for d=3
- G5^2 = -I (complex structure, not involution)
- G5 != chi (they are distinct operators; {chi, G5} = 0)

The bipartite parity chi (not the volume element) plays the chirality role in 3D.

### Attack 4: CPT Self-Conjugation

The KS Clifford algebra is **real** (all G_mu are real matrices). Complex conjugation K commutes with the entire Clifford algebra, providing a canonical antiparticle sector.

- K preserves Y eigenvalues (Y is real)
- The charge conjugation C_KS = sy x sy x sy acts within the same representation
- The antiparticle sector exists by the real structure of the Clifford algebra

This is **graph-canonical**: any real graph Laplacian has K as a symmetry.

### Attack 5: Particle-Hole (Dirac Sea) Doubling

The staggered Hamiltonian H(p) = sum sin(p_mu) G_mu satisfies:

- {chi, H} = 0 (particle-hole symmetry)
- Every eigenvalue +E is paired with -E
- chi maps +E eigenstates to -E eigenstates exactly

The Dirac sea (filled negative-energy states) provides holes = antiparticles. Both energy sectors carry the **same** SU(2) doublet content (Casimir = 3/4 uniformly). This is graph-canonical: bipartiteness is a graph property.

## Answer

**YES** for existence and quantum numbers: CPT + Dirac sea + anomaly cancellation give all 16 states of one SM generation with correct charges. These mechanisms are graph-canonical.

**NO** for SU(2) chirality: the 3D surface cannot produce SU(2) **singlets** from SU(2) **doublets**. The bipartite parity chi anticommutes with T1, T2, meaning both energy sectors carry SU(2) doublets (no singlets). Getting SU(2)-singlet right-handed fermions requires chirality, which is intrinsically 4-dimensional.

## What Is and Is Not Graph-Canonical

| Feature | Graph-canonical? | Mechanism |
|---------|-----------------|-----------|
| Antiparticle existence | Yes | Real Clifford algebra (K symmetry) |
| Particle-hole doubling | Yes | Bipartite parity {chi, H} = 0 |
| Right-handed Y charges | Yes | Anomaly cancellation (topological) |
| Right-handed SU(3) content | Yes | Taste algebra (commutant) |
| SU(2)-singlet right-handed | **No** | Requires 4D chirality gamma_5 |

The 4D step is not "adding a time direction by hand" -- it is the **minimal additional structure** needed to break the L/R degeneracy of the SU(2) representations. Everything else is graph-canonical.
