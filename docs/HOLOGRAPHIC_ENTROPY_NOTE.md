# Propagator Entropy Saturation Test

**Script:** `scripts/frontier_holographic_entropy.py`
**Date:** 2026-04-11
**Status:** review hold; single-particle entropy proxy

## Question

Does the single-particle propagator entropy across a 2D surface in a 3D
lattice scale with area, volume, or saturate with lattice size?

## Method

1. Build 3D cubic lattice of side N (tested N = 4, 6, 8, 10, 12).
2. Propagate from each source on the x=0 face to the midplane at x=N/2
   using the corrected propagator with directional measure (k=4, beta=0.8).
3. The propagator creates an amplitude matrix M[mid, src] on the 2D
   cross-section.
4. Bipartition the midplane into A (y >= 0) and B (y < 0).
5. Compute the reduced density matrix rho_A = A-block of M M^dag / Tr,
   then Renyi-2 entropy S_2 = -ln(Tr(rho_A^2)) and von Neumann entropy
   S_vN = -Tr(rho_A ln rho_A).
6. Fit S vs N in log-log to extract the scaling exponent.

## Results

### Entropy scaling (free space)

| N  | n_A | boundary | S_2    | S_vN   |
|----|-----|----------|--------|--------|
| 4  | 15  | 5        | 2.347  | 2.518  |
| 6  | 28  | 7        | 2.512  | 2.853  |
| 8  | 45  | 9        | 2.553  | 2.999  |
| 10 | 66  | 11       | 2.586  | 3.118  |
| 12 | 91  | 13       | 2.632  | --     |

Log-log fit: S_2 ~ N^0.10 (R^2 = 0.94).

The entropy grows very slowly with system size -- sub-area-law, essentially
saturating. This is consistent with the single-particle propagator having
a bounded number of effective transverse modes (~13 at N=12).

### Gravitational effect

A mass cluster at the midplane center *reduces* entropy by ~1.3 nats.
This is a strong effect: gravity focuses the propagator, concentrating
amplitude into fewer modes and reducing the effective rank of rho_A from
~13 (free) to ~4 (with mass).

The mass scaling exponent is 0.37 (vs 0.10 free), suggesting gravity
partially restores a scaling trend, but still sub-area.

### Bipartition asymmetry (N=10)

Varying the y-cut position at fixed N shows S increasing as region A
grows larger. The maximum entropy occurs at the most asymmetric cut
(A much larger than B), not at the symmetric cut. This is the expected
behavior for single-particle entanglement: a larger subsystem captures
more of the correlation structure in rho_A.

## Interpretation

**What was found:**
- The propagator entropy saturates rapidly with lattice size, growing as
  ~N^0.1 rather than N^2 (area) or N^3 (volume).
- Gravity strongly reduces entropy (focusing effect).
- The effective rank of the reduced density matrix is ~10-14, bounded
  by the number of propagator modes, not the Hilbert space dimension.

**What this means:**
- The single-particle propagator does NOT produce volume-law entanglement.
  The entropy is bounded and sub-extensive, which is a necessary (but not
  sufficient) condition for holographic behavior.
- The saturation is consistent with the propagator having O(1) effective
  transverse channels (set by the directional measure width beta and
  wavenumber k), not O(N^2) channels.
- To see true area-law scaling S ~ L^2, one would need either:
  (a) a many-body state (second-quantized propagator filling a Fermi sea),
  (b) a field-theoretic vacuum state on the lattice, or
  (c) much larger lattices where the mode count grows with boundary size.

**What is NOT claimed:**
- We do NOT claim the framework is holographic based on this test alone.
- The sub-volume scaling is necessary but not sufficient for holography.
- The gravitational entropy reduction is qualitative; the magnitude depends
  on lattice parameters (k, beta, field strength).
- Finite-size effects are significant at N <= 12.

## Bounded claims

1. CONFIRMED: the tested propagator entropy is sub-extensive / saturating.
2. CONFIRMED: the gravitational field reduces this entropy proxy.
3. NOT CONFIRMED: area-law scaling `S ~ L^2`.
4. OPEN: whether a many-body or field-theoretic extension would recover
   an area law remains untested.
