# Magnetic Monopoles from Lattice Topology

**Script:** `scripts/frontier_magnetic_monopoles.py`
**PStack experiment:** magnetic-monopoles
**Date:** 2026-04-12

## Question

Does the lattice framework predict magnetic monopoles?  If so, what is
their mass and cosmological abundance?

## Summary

**YES** -- the framework predicts magnetic monopoles as an automatic
consequence of compact U(1) on the lattice.  They are topologically
stable, satisfy the Dirac quantization condition automatically, and
have mass M ~ 2 M_Planck.  They are unobservably heavy and consistent
with all experimental null results.

## Key Results

### 1. Existence: Automatic from Compact U(1)

On the lattice, U(1) is naturally compact: gauge phases live in
[0, 2pi).  Magnetic monopoles are topological defects defined by
nonzero total magnetic flux through an elementary cube.  Their
existence is not optional -- it is forced by the lattice structure.

- At strong coupling (random phases): monopole density ~ 0.48 per cube
- At weak coupling (physical QED regime): density exponentially suppressed
- Total magnetic charge is always zero on a periodic lattice (Gauss's law)
- Charge quantization: m is an exact integer (verified numerically)

### 2. Phase Structure: Coulomb Phase

Compact U(1) in 4D has a phase transition at beta_c ~ 1.01:
- beta < beta_c: confined (monopole condensation)
- beta > beta_c: Coulomb (free photons, massive monopoles)

Physical QED: beta = 1/(4*pi*alpha) ~ 10.9, deep in the Coulomb phase.
At the Planck scale: beta(M_Pl) ~ 2.0, still in the Coulomb phase.

Monte Carlo verification on L=6 lattice confirms the transition:
monopole density drops sharply near beta ~ 1.0.

### 3. Monopole Mass

Using the DeGrand-Toussaint lattice self-energy (c = 0.51 in 4D)
and RG-improved alpha(M_Pl) ~ 1/40:

    M_mono = c * beta(M_Pl) * M_Pl
           = 0.51 * 3.18 * 1.22e19 GeV
           = 2.0e19 GeV  (~1.6 M_Planck)

Comparison:
- Classical Coulomb: M = (pi/2*alpha) * M_Pl ~ 215 M_Pl
- GUT 't Hooft-Polyakov: M ~ M_GUT/alpha ~ 8e17 GeV
- Lattice (this work): M ~ 2e19 GeV (~25x heavier than GUT monopoles)

### 4. Dirac Quantization: Automatic

The Dirac condition eg = 2*pi*n follows from:
1. Gauge phases are periodic (compact U(1))
2. Magnetic flux through plaquettes is defined mod 2*pi
3. Total flux through a closed surface is quantized: 2*pi * integer
4. Therefore eg = 2*pi*n -- no additional postulate needed

Minimum magnetic charge: g_D = 1/(2*alpha) ~ 68.5 (natural units).
Magnetic fine structure constant: alpha_m ~ 374 (strongly coupled).

### 5. Cosmological Abundance

**Without inflation (Kibble mechanism):**
- n_mono/n_gamma ~ 4 at formation
- Omega_mono ~ 7e27 today
- CATASTROPHIC overclosure -- ruled out

**With standard inflation (T_RH ~ 1e15 GeV):**
- T_RH < M_mono: no thermal production possible
- Pre-existing monopoles diluted to zero
- Schwinger pair production: negligible for M >> M_Pl
- Quantum production during inflation: suppressed (H_inf << M_mono)
- **Prediction: essentially zero monopoles today**

### 6. Experimental Consistency

| Bound | Value | Status |
|-------|-------|--------|
| Parker (galactic B field) | flux < 1e-15 cm^-2 s^-1 sr^-1 | CONSISTENT |
| MACRO | flux < 1.4e-16 cm^-2 s^-1 sr^-1 | CONSISTENT |
| MoEDAL (LHC) | M > few TeV | CONSISTENT (M >> TeV) |
| IceCube | flux < 1e-18 cm^-2 s^-1 sr^-1 | CONSISTENT |

## Theoretical Implications

1. **Inflation argument:** The framework requires inflation to avoid the
   monopole problem, providing an independent argument for inflation.

2. **Dirac quantization for free:** Charge quantization is automatic on
   the lattice -- explaining why electric charge is quantized without
   needing GUT unification or magnetic monopole detection.

3. **Not dark matter:** Unlike the suggestion in the dark matter closure
   note, the RG-improved mass (~1.6 M_Pl rather than ~M_Pl) and the
   extreme suppression after inflation make monopoles negligible as DM.

4. **GUT vs lattice:** Lattice monopoles are heavier (2e19 vs 8e17 GeV)
   but both are unobservable.  The lattice monopoles are a MORE robust
   prediction because they don't depend on GUT symmetry breaking.

## Robustness Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Existence | RIGOROUS | Topological, lattice-independent |
| Dirac quantization | RIGOROUS | Follows from compactness |
| Phase (Coulomb) | STRONG | beta >> beta_c numerically verified |
| Mass estimate | MODERATE | Depends on c coefficient and alpha(M_Pl) |
| Abundance (zero) | STRONG | Multiple suppression mechanisms |
| Experimental consistency | STRONG | All bounds satisfied by large margin |

## Verdict

The lattice framework predicts magnetic monopoles with mass ~ 2 M_Planck.
They are topologically stable, satisfy Dirac quantization automatically,
and are unobservably rare in the post-inflation universe.  The prediction
is CONSISTENT with all experimental null results and provides an
independent argument for cosmic inflation.
