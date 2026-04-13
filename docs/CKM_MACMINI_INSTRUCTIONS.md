# CKM NNI Coefficients: Mac Mini M4 Production Run

## Overview

This script computes the CKM mixing matrix from first principles on the staggered lattice with EWSB. It generates thermalized SU(3) gauge configurations via Metropolis at beta=6, builds the full Dirac operator (staggered + Wilson + EWSB), and extracts inter-valley scattering amplitudes that determine the NNI texture coefficients.

## Hardware Requirements

- **Machine:** Mac Mini M4, 16 GB RAM
- **L=8:** dim = 1536, matrix = 0.04 GB (trivial)
- **L=12:** dim = 5184, matrix = 0.4 GB (comfortable)
- **Dependencies:** Python 3, NumPy, SciPy (standard install)

## Quick Test (verify everything works)

```bash
cd ~/Toy\ Physics
python3 scripts/frontier_ckm_macmini.py --quick 2>&1 | tee ~/Desktop/ckm_quick_test.txt
```

This runs 5 gauge configurations at L=6 (~2 minutes). Verify the output shows:
- Plaquette values near expected thermalized value
- Non-zero inter-valley amplitudes with R_12/R_23 > 1
- CKM hierarchy |V_us| > |V_cb| > |V_ub|

## Full Production Run

```bash
cd ~/Toy\ Physics
python3 scripts/frontier_ckm_macmini.py 2>&1 | tee ~/Desktop/ckm_results.txt
```

**Default parameters:**
- L = 8 and L = 12
- 50 gauge configurations per lattice size
- beta = 6 (g = 1)
- Wilson r = 1.0
- EWSB y*v = 0.5

**Estimated wall time:**
- L=8, 50 configs: ~30 minutes
- L=12, 50 configs: ~4-8 hours
- Total: ~5-9 hours

## High-Statistics Run

For publication-quality results:

```bash
python3 scripts/frontier_ckm_macmini.py --ncfg 100 2>&1 | tee ~/Desktop/ckm_results_100cfg.txt
```

## Command-Line Options

| Flag | Default | Description |
|------|---------|-------------|
| `--quick` | off | Quick test: 5 configs, L=6 only |
| `--ncfg N` | 50 | Number of gauge configurations |
| `--beta B` | 6.0 | Gauge coupling beta |
| `--rwilson R` | 1.0 | Wilson parameter r |
| `--yv Y` | 0.5 | EWSB coupling y*v |
| `--seed S` | 20260413 | Base RNG seed |

## What the Script Computes

1. **Gauge configurations:** Metropolis SU(3) at beta=6 with 100 thermalization sweeps and 20 decorrelation sweeps between configs (cold start per config for independent sampling).

2. **Dirac operator:** H = H_KS + H_W + H_EWSB in position space (not taste-expanded), so dim = 3*L^3 not 12*L^3.

3. **Inter-valley amplitudes:** T_ij = <psi_i|H|psi_j> where psi_i are Gaussian wave packets at BZ corners X1=(pi,0,0), X2=(0,pi,0), X3=(0,0,pi), averaged over color.

4. **EWSB breaking pattern:** The VEV in direction 1 breaks C3 -> Z2, making T_12,T_13 (involving the weak corner X1) differ from T_23 (color-color).

5. **NNI coefficients:** c_ij derived from lattice ratio R_12/R_23, 1-loop normalization (alpha_s, N_c, log enhancement), and EW charge weighting.

6. **CKM matrix:** Diagonalize NNI mass matrices M_u, M_d and compute V_CKM = U_u^T * U_d.

## Output Quantities

- `c12_u, c23_u, c12_d, c23_d` with jackknife error bars
- `|V_us|, |V_cb|, |V_ub|` with jackknife error bars
- Comparison to PDG values
- Volume dependence (L=8 vs L=12)
- Average plaquette (thermalization monitor)
- Structural checks (parameter-free predictions)

## Interpreting Results

**Key predictions (parameter-free):**
- c_12 > c_23 (weak-axis enhancement from EWSB)
- c_12^u > c_12^d (up-type has larger EW charge)
- |V_us| > |V_cb| > |V_ub| (CKM hierarchy)
- All c_ij are O(1)

**What closes CKM:** If the lattice ratio R_12/R_23 is stable across L=8 and L=12 (volume independence) and the derived c_ij values match the fitted values within statistical errors, the CKM derivation is complete.

## Troubleshooting

- **Out of memory:** Should not happen at L=12 (0.4 GB). If it does, reduce to `--ncfg 20`.
- **Slow thermalization:** Check plaquette values. At beta=6 in 3D SU(3), expect plaquette ~ 0.5-0.7. If plaquette is near 1.0 (cold) after thermalization, increase n_therm.
- **Large error bars:** Increase `--ncfg`. Statistical errors scale as 1/sqrt(N).
