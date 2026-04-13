# V_CKM Directly from the Lattice Hamiltonian with EWSB

**Date:** 2026-04-13
**Script:** `scripts/frontier_ckm_direct_hamiltonian.py`
**Status:** BOUNDED -- mechanism demonstrated, quantitative match not yet achieved

## Idea

Compute V_CKM directly from the lattice Hamiltonian without going through
NNI coefficients or intermediate decompositions.

The CKM matrix is V = U_u^dag U_d where U_u, U_d diagonalize the up-type
and down-type quark mass matrices.  On the staggered lattice with EWSB,
these mass matrices are obtained by projecting each sector's Hamiltonian
onto generation space (the 3 hw=1 BZ corners).

The up and down Hamiltonians differ because:
1. **Yukawa coupling:** y_u * v != y_d * v (m_t/m_b ~ 40)
2. **EW charges:** Q_u = 2/3, T3_u = +1/2 vs Q_d = -1/3, T3_d = -1/2

These enter the lattice Hamiltonian as:
- H_EWSB(y_q) = y_q * v * Gamma_1 (shift in VEV direction)
- H_EW(Q_q, T3_q) = alpha_W * [g_Z(q) * hops in dir-1 + g_gamma(q) * hops in dir-2,3]

## Procedure

1. Build gauge config on Z^3_L with SU(3) near-identity links
2. For each sector q in {u, d}:
   - H_q = H_Wilson + H_EWSB(y_q) + H_EW(Q_q, T3_q)
3. Project onto generation space: M_q^{ij} = <X_i | H_q | X_j>
4. Diagonalize M_u, M_d -> V_CKM = U_u^dag U_d

No NNI decomposition. No K normalization. One lattice, two Hamiltonians.

## Key Results

### Origin decomposition (L=6, seed=42)

| Component | |V_us| | |V_cb| | |V_ub| |
|-----------|--------|--------|--------|
| Wilson only (same H for u,d) | ~0 | ~0 | ~0 |
| Wilson + EWSB (y_u != y_d) | 1.0e-2 | 7.4e-3 | 2.7e-2 |
| Wilson + EWSB + EW (full) | 7.8e-3 | 5.8e-3 | 2.3e-2 |

- Wilson alone: V = I (exact, since same H for both sectors)
- EWSB Yukawa difference is the PRIMARY source of mixing
- EW charge correction is ~22% perturbative correction

### Ensemble average (L=6, 20 configs)

- <|V_us|> = 0.073 +/- 0.060
- <|V_cb|> = 0.024 +/- 0.025
- <|V_ub|> = 0.070 +/- 0.055
- Correct hierarchy (|V_us| > |V_cb| > |V_ub|): 20% of configs

### L-dependence

| L | dim | |V_us| | |V_cb| | |V_ub| |
|---|-----|--------|--------|--------|
| 4 | 192 | 0.134 | 0.006 | 0.485 |
| 6 | 648 | 0.008 | 0.006 | 0.023 |
| 8 | 1536 | 0.025 | 0.009 | 0.021 |

## What is demonstrated

1. **Mechanism works:** Different y*v for up and down sectors, acting on the
   same EWSB-broken lattice, produces V_CKM != I. This is a direct lattice
   computation with no intermediate steps.

2. **Wilson alone gives no mixing:** When both sectors see the same H,
   V_CKM = I exactly (trivially, since U_u = U_d).

3. **EWSB is the driver:** The Yukawa difference is responsible for ~80%
   of the mixing; EW charge asymmetry adds ~20%.

4. **Signal is present but noisy:** On L=6 with quenched configs,
   the mixing elements are O(0.01-0.1) but the hierarchy pattern
   |V_us| >> |V_cb| >> |V_ub| does not emerge robustly.

## What is not derived (bounded)

- Yukawa couplings y_u, y_d are model inputs (not derived from the lattice)
- Gauge configurations are quenched (not dynamical)
- Continuum limit not taken
- The correct CKM hierarchy requires either larger L, dynamical fermions,
  or a mechanism that correlates the Yukawa couplings with the lattice geometry

## Relation to previous scripts

- `frontier_ckm_lattice_direct.py`: found no hierarchy (C3 unbroken)
- `frontier_ckm_with_ewsb.py`: added EWSB, found C3 breaking but used
  ad-hoc kappa_u, kappa_d coefficients to build M_u, M_d
- **This script:** builds H_up, H_down directly with all EW physics
  included, then extracts M_u, M_d by projection. No intermediate coefficients.

## Open questions

1. Can the hierarchy be recovered with dynamical fermions?
2. Does the continuum limit (L -> infinity) improve the hierarchy?
3. Is there a lattice mechanism that fixes y_u/y_d rather than treating it as input?
4. Connection to the Z3 Higgs charge (still open per review.md)
