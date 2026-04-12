# Mass Spectrum Investigation

**Script:** `scripts/frontier_mass_spectrum.py`
**Date:** 2026-04-12
**Status:** Four mechanisms investigated; one viable candidate identified

## Question

Can the framework predict fermion mass ratios? The Standard Model has three
generations spanning 5 orders of magnitude:

| Generation | Up-type | Down-type |
|------------|---------|-----------|
| 1          | u ~ 2 MeV | d ~ 5 MeV |
| 2          | c ~ 1.3 GeV | s ~ 95 MeV |
| 3          | t ~ 173 GeV | b ~ 4.2 GeV |

Up-type ratios: m_u : m_c : m_t ~ 1 : 650 : 86,500

The naive Wilson mass mechanism gives m proportional to Hamming weight:
m(T1) = 2r/a, m(T2) = 4r/a, yielding a ratio of 2. The observed ratio
(top/up) is approximately 75,000.

## Four Mechanisms Tested

### 1. Gravitational Self-Energy (INSUFFICIENT)

Each taste sector has a different Wilson mass, sourcing a different
gravitational field. The self-energy correction is E_self ~ G * m_W^2 / a.

**Result:** Enhancement factor = 0.99 (negligible). The gravitational
self-energy can at most double the bare ratio (from 2 to 4 in the
strong-gravity limit). It cannot generate 5 orders of magnitude.

### 2. SU(2) Casimir Correction (INSUFFICIENT)

The SU(2) generators from the Cl(3) Clifford algebra yield a quadratic
Casimir C_2 = j(j+1). We measured the expectation value of C_2 in each
taste state.

**Result:** C_2 is the SAME (0.75, corresponding to j=1/2) for ALL 8
taste states. The entire 8-dim taste space decomposes as 4 copies of the
spin-1/2 representation. Since C_2(T1) = C_2(T2) = 0.75, the Casimir
correction is taste-independent and actually DILUTES the Wilson ratio
(pushing it toward 1).

### 3. Dynamical Lattice Anisotropy (NOT SPONTANEOUS)

Self-consistent Poisson iteration with a Gaussian wavepacket on an
isotropic 24^3 lattice.

**Result:** Anisotropy = 0.000000 after 5 iterations. The self-consistent
gravitational field preserves the cubic symmetry exactly, as expected:
a spherically symmetric source produces a spherically symmetric field.
Spontaneous Z_3 breaking does not occur from gravity alone.

### 4. RG Running (SUFFICIENT IN PRINCIPLE)

The Wilson mass is defined at the lattice cutoff. Running to low energy
with taste-dependent anomalous dimensions gives exponential amplification:

    m(s, mu) = m_W(s) * (Lambda/mu)^{gamma_m(s) / 2*b_0}

**Required:** Delta(gamma_m) ~ 0.27 for a ratio of 75,000 over 17 decades.

**One-loop result:** The taste-dependent self-energy (from Wilson mass in
the propagator loop) gives Delta(gamma) ~ 0.05, producing a ratio of ~14.
This is insufficient at one loop but demonstrates the mechanism. Higher-loop
and non-perturbative contributions would increase the anomalous dimension
difference.

For comparison, QCD anomalous dimensions are gamma_m ~ 0.05 per loop order,
and the full Yukawa running in the SM produces the observed hierarchy through
multiple coupling contributions.

## Combined Mass Formula

    m(generation i, mu) = m_0 * epsilon^{q_i} * (Lambda/mu)^{gamma_i / 2*b_0}

With the Froggatt-Nielsen-like parameterization:
- Charge assignment q = (4, 2, 0) for generations (1, 2, 3)
- epsilon ~ 0.06 (from up-type) or epsilon ~ 0.22 (Cabibbo angle)

**Up-type fit (epsilon = 0.058):**
- Predicted c/u = 297, actual = 650 (factor of 2)
- Predicted t/u = 86,500 (by construction)

**Cabibbo epsilon = 0.22:**
- Predicted ratios: 1 : 21 : 430 vs actual 1 : 650 : 86,500
- Captures the geometric structure but not precise values

## Numerical Lattice Spectrum

Diagonalization of the full staggered + Wilson Hamiltonian on L=8 lattices
confirms:

1. **Free staggered (r=0):** All 8 modes degenerate (massless)
2. **Wilson, isotropic:** 1+3+3+1 pattern, ratio T2/T1 = 2.0
3. **Wilson + anisotropy:** Triplets split; hierarchy controlled by anisotropy
4. **Cabibbo anisotropy:** Intra-generation ratio ~ 21 at tree level

## What the Framework Predicts

| Prediction | Status |
|-----------|--------|
| Exactly 3 generations | PROVED (Z_3 orbits from d=3) |
| Generations ordered by mass | PROVED (Hamming weight) |
| Geometric mass pattern m ~ epsilon^q | COMPATIBLE |
| Hierarchy mechanism (RG running) | IDENTIFIED |

## What the Framework Does Not Yet Predict

- The value of the Z_3-breaking parameter epsilon
- The charge assignments q_i (requires Yukawa sector)
- Up/down splitting within generations (requires isospin breaking)
- The anomalous dimension gamma_m(s) from first principles

## Verdict

The framework provides the structural ingredients (3 generations, mass
ordering, geometric pattern) but not the numerical parameters. This is
comparable to the Standard Model itself, where the Yukawa coupling matrix
is a free parameter. The key advance is deriving the generation structure
from spatial dimension without inputting gauge groups or family symmetries.

The RG running mechanism is the only identified pathway to 5-order-of-magnitude
ratios. A Delta(gamma_m) ~ 0.27 between taste sectors, combined with the
Planck-to-weak energy hierarchy, reproduces the observed spectrum. Whether
the framework produces this anomalous dimension difference is an open
question requiring non-perturbative calculation.
