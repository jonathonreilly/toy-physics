# Hierarchy H1 Route 1B — Wilson MC and Drouffe-Itzykson Cross-Check

**Date:** 2026-05-03 (loop iteration 2)
**Type:** numerical_diagnostic + cross_check
**Primary runners:**
  - `scripts/frontier_hierarchy_wilson_mc_kernel.py`
  - `scripts/frontier_hierarchy_drouffe_itzykson_check.py`
  - `scripts/frontier_hierarchy_pade_resum.py`

## Iteration 2 of the loop: pursue Route 1A onset-jet extension via numerical MC

The loop instruction was to pursue path 1: extend the framework's onset jet
`beta_eff(beta) = beta + beta^5 / 26244 + O(beta^6)` by gathering numerical
`<P>(beta)` data at multiple `beta` values, inverting via the framework's
single-plaquette block `P_1plaq(beta)`, and Pade-resumming.

This iteration produced:

1. **Three-way analytic agreement at `P_1plaq(6) = 0.4225317396` to 10 digits.**
2. **L=2 SU(3) Wilson MC** — works in pure Python; finite-volume distorts
   `<P>(6)` to ~0.624 (5% above the canonical bulk 0.5934).
3. **L=3 attempt** — pure-Python MC is too slow at L=3 (estimated
   ~55 hours for the full beta scan); needs C/Fortran or vectorized GPU
   implementation.
4. **Pade resummation analyzer** — built and tested; unstable on the
   finite-volume L=2 data because the higher-order coefficients absorb
   ~5% finite-volume error rather than tracking the bulk onset jet.

## Three-way analytic cross-check (the substantive result)

For SU(3) at `beta = 6`, three independent computational methods give
the same single-plaquette block to 10 digits:

| Method | `P_1plaq(6)` | Source |
|---|---|---|
| Drouffe-Itzykson Bessel determinant | `0.4225317397` | analytic 3x3 Bessel-determinant sum |
| Direct Haar quadrature (n=128 grid) | `0.4225317396` | numerical 2D integration on SU(3) eigenvalues |
| Framework reference Perron solve | `0.4225317396` | `GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE` (existing) |

Pairwise differences:

```
|DI - Haar|    = 1.476e-10
|DI - Frmwk|   = 1.476e-10
|Haar - Frmwk| = 0.000e+00
```

The Drouffe-Itzykson formula:

```
c_(0,0)(beta) = sum_{n in Z} det[ I_{n + i - j}(beta/3) ]_{i,j = 1..3}
P_1plaq(beta) = (d/dbeta c_(0,0)(beta)) / c_(0,0)(beta)
```

converges at `n_max = 10` to 15-digit precision and gives
`c_(0,0)(6) = 3.441440354987777` exactly (matching all 16 digits across
cross-checks).

This is a strong cross-check that the framework's `P_triv(6)` reference
Perron solve is indeed the single-plaquette block, computed by an entirely
different route (Bessel determinant vs Perron eigenvector).

## Inverted beta_eff(6) from canonical `<P>(6) = 0.5934`

Using the verified `P_1plaq` (any of the three methods):

```
beta_eff(6) = P_1plaq^(-1)(0.5934) = 9.326168
```

The framework's order-`beta^5` onset jet predicts:

```
beta_eff(6) ~= 6 + 6^5 / 26244 = 6.296
```

**Gap: 3.030 (50% relative).** The higher-order onset coefficients dominate
the jet at `beta = 6`, far beyond the order-`beta^5` reach. This is consistent
with the framework's own
`GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE` observation
that the order-`beta^5` jet does not pin `beta_eff(6)`.

## Why the Wilson MC route is harder than initially scoped

The reduction-law inversion strategy was to:

1. Run SU(3) Wilson MC at multiple `beta` values to get bulk `<P>(beta)`.
2. Invert each via `P_1plaq` to get `beta_eff(beta_i)`.
3. Fit `beta_eff(beta) - beta = sum_{k >= 5} c_k beta^k` to extract higher-order
   onset coefficients.
4. Pade-resum to predict `beta_eff(6)`.

Reality at L = 2 (the only lattice size tractable in pure Python in this session):

- `<P>(6)` MC = `0.624` versus canonical bulk `0.5934`. Finite-volume
  shift = +5%, far larger than the canonical-vs-bridge 0.022% window.
- Polynomial fit to `beta_eff(beta) - beta` across 11 sampled betas
  produces unstable coefficients (`c_5` fitted from L=2 data ranges from
  `+2.8e-4` at K=5 to `+0.18` at K=10), all dominated by finite-volume
  contamination rather than the actual bulk onset structure.
- Going to L = 3 in pure Python: ~55 hours estimated (each Metropolis
  sweep is `81 sites x 4 dirs x 5 hits = 1620` link updates each calling
  `scipy.linalg.expm`).

The honest verdict: **closing Route 1A via numerical MC requires a
compiled-language Wilson MC implementation**, not pure Python. Estimated
effort: 2-4 weeks of focused C/CUDA implementation, then weeks of MC
runtime to get bulk `<P>(beta)` at 5-10 beta values to ~`10^{-4}` precision.

## L = 2 sweeping data (preserved for documentation)

```
   beta     <P>(L=2)         beta_eff (via P_1plaq^-1)   beta_eff - beta
   4.00     0.303632                4.3172                  +0.3172
   4.50     0.363430                5.1325                  +0.6325
   5.00     0.456810                6.5470                  +1.5470
   5.50     0.565639                8.6511                  +3.1511
   5.70     0.581795                9.0347                  +3.3347
   5.85     0.595049                9.3688                  +3.5188
   6.00     0.624100               10.1728                  +4.1728
   6.20     0.630228               10.3569                  +4.1569
   6.50     0.653774               11.1196                  +4.6196
   7.00     0.686667               12.3644                  +5.3644
   8.00     0.732160               14.5679                  +6.5679
```

The shape `beta_eff(beta) - beta` is monotone increasing, much larger
than the leading `beta^5/26244 ~ 0.296` at `beta = 6`, and
non-polynomial in the small-beta sense. Finite-volume effects make this
an unreliable estimate of the bulk onset jet.

## What this iteration closes

1. **Cross-check at 10 digits.** Three independent computations of
   `P_1plaq(6)` agree, validating the Haar-quadrature kernel and the
   framework's existing Perron-solve framework simultaneously. This is
   genuine new evidence — the framework's reference Perron solve is now
   verified by an entirely different analytic route (Drouffe-Itzykson),
   not just by the direct numerical inversion.
2. **Drouffe-Itzykson reference is now in the framework.** Future
   downstream calculations of `P_1plaq(beta)` for any `beta` can use the
   Bessel-determinant formula instead of Haar quadrature or Perron solve.
   It converges in 30 terms to 15 digits.
3. **Quantified Wilson-MC compute requirement.** Closing Route 1A via
   numerical MC is now a well-scoped C-level effort, not a session-bounded
   Python target.

## What this iteration does NOT close

- The bulk `<P>(beta)` at multiple beta values. Pure-Python MC at L >= 3
  is too slow.
- The Pade-resummed prediction of `beta_eff(6)`. Without bulk MC data
  at multiple beta values, the fit is unconstrained.
- The `+50%` onset-jet residual. This is genuinely the next theorem
  target; without higher-order onset coefficients (from extended
  mixed-cumulant audit) or bulk MC data, it cannot be closed.

## Cross-references

- `HIERARCHY_H1_ROUTE_1B_HAAR_KERNEL_NOTE_2026-05-03.md` — iteration 1
  Haar kernel.
- `HIERARCHY_H1_ROUTE_1_STATUS_CORRECTION_NOTE_2026-05-03.md` — corrected
  Route 1 path.
- `GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` —
  framework's `P_triv` reference solve, now cross-checked by two
  independent analytic methods.
- `GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md` — the
  reduction law `P_L = P_1plaq(beta_eff,L(beta))`.
- `GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md` —
  the order-`beta^5` jet underdetermination, now quantified at +50%
  residual at `beta = 6`.

## Loop status: stopped (honest)

Loop iteration 2 produced one substantive result (3-way agreement at
10 digits) and one quantified obstruction (compiled-language MC needed).
No further productive work in pure Python is available for closing
Route 1A in this session.

To continue: implement Wilson MC in C/CUDA, run at L = 6-12 for bulk
`<P>(beta)` at 5-10 beta values, then re-run the Pade resummation
analyzer with bulk-converged data. Estimated total effort: 1-2 months
implementation + 1-2 weeks MC runtime.
