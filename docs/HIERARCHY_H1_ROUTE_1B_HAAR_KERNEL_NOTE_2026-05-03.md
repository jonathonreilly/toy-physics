# Hierarchy H1 Route 1B — Numerical Haar-Integration Kernel and Onset-Jet Diagnostic

**Date:** 2026-05-03
**Type:** numerical_diagnostic + bounded_finding
**Primary runner:** `scripts/frontier_hierarchy_route_1b_haar_evaluation.py`

## Question

Direct numerical evaluation of the framework's single-plaquette block
`P_1plaq(beta)` via Haar integration on SU(3), as a sanity check on the
reduction-law onset-jet prediction
`beta_eff(beta) = beta + beta^5 / 26244 + O(beta^6)` at the framework
point `beta = 6`.

## Method

Direct 2D numerical Haar integration on SU(3) in eigenvalue
parameterization. SU(3) eigenvalues `(e^{i theta_1}, e^{i theta_2}, e^{i theta_3})`
with constraint `theta_1 + theta_2 + theta_3 = 0`. After eliminating
`theta_3`, the Haar measure reads

```
d mu_Haar  =  (1 / (6 (2 pi)^2))  *  |Delta(e^{i theta})|^2
              d theta_1 d theta_2,
```

with Vandermonde
`|Delta|^2 = prod_{i<j} 4 sin^2((theta_i - theta_j)/2)` (Weyl integration
formula). Tensor-product trapezoidal grid on `(-pi, pi)^2` with
`n = 128` per direction reaches Haar normalization `<1>_Haar = 1` to
ten digits.

## Results

### Sanity checks

```
<1>_Haar              =  1.0000000000   (target 1)
Z_1plaq(0)/Z_1plaq(0) =  1.0000000000   (target 1)
P_1plaq(0)            =  0.0000000000   (target 0)
```

### Single-plaquette block at sample beta values

```
   beta        P_1plaq(beta)
   1.000        0.0601265548
   3.000        0.2030750500
   6.000        0.4225317396
   6.296        0.4413841852
   7.000        0.4833085169
  10.000        0.6181757390
  20.000        0.8031936767
```

**Cross-check vs framework reference Perron solve:**

The framework's
`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` Theorem 2
reports `P_triv(6) = 0.4225317396` from the explicit Perron solve with
the trivial-projection reference environment `rho = delta_{(p,q),(0,0)}`.

This Haar-integration value `P_1plaq(6) = 0.4225317396` agrees to
**ten digits**, confirming that the trivial-projection reference Perron
solve in the framework is exactly the single-plaquette block `P_1plaq`.
This is a strong cross-check on both calculations.

### Inversion: beta_eff(6) such that `P_1plaq(beta_eff) = <P>_canonical`

```
canonical <P>(6)             =  0.5934
beta_eff(6) inferred         =  9.326168     (Brent inversion, xtol = 1e-6)
onset-jet prediction (5th)   =  6.296296     (beta + beta^5/26244 at beta=6)
gap (higher-order residual)  =  +3.029872    (50.5% relative)
```

## Significant finding (revises earlier closure estimates)

The leading-order onset jet prediction `beta_eff(6) ~= 6.30` is
**~50% short** of the value needed to reach the canonical
`<P>(6) = 0.5934`. The gap of `~3.03` on the reduction parameter must be
closed by higher-order onset coefficients in the series

```
beta_eff(beta)  =  beta  +  beta^5 / 26244  +  c_6 beta^6
                  +  c_7 beta^7  +  ...
```

This is a much bigger correction than the order-`beta^5` term provides
on its own.

## Implications for the closure-program timeline

**The Route 1A onset-jet extension target was previously underestimated.**

The Bessel-majorant bound `6^N / N! < threshold` reaches `N ~ 22` for
the 0.022% canonical-vs-bridge window. But the relevant *baseline* gap
(from the leading-order onset jet to actual `<P>(6) = 0.5934`) is not
0.022% — it is **50%**. Closing 50% via direct onset-jet extension is a
qualitatively harder task than closing 0.022% on top of an already-near
prediction.

In particular:

- The framework's underdetermination note witness gap (10^-7 at order
  beta^6, contributing 0.005 to beta_eff(6)) is six orders of magnitude
  smaller than the actual residual (~3.03). So the underdetermination
  argument is correct *as far as it goes*, but it implicitly assumed
  the underlying onset-jet series is well-behaved at beta = 6.

- Direct order-by-order extension of the onset jet would need many
  more orders than 22 to close the 50% gap, because the series is
  presumably oscillatory or has growing coefficients in this regime.

- A more productive route is **Borel/Padé resummation** of the series,
  combined with the framework's bridge-support stack (which already
  reaches `P(6) = 0.59353` via different means).

## What this kernel closes

1. The numerical Haar integration of `P_1plaq(beta)` is now a controlled
   computation reproducible via a single Python script with
   numpy/scipy (no MC, no fit parameters).
2. The cross-check `P_1plaq(6) = 0.4225317396` exactly matches the
   framework's `P_triv(6)` from the existing tensor-transfer Perron
   solve, validating both computations.
3. The inferred `beta_eff(6) = 9.33` provides a concrete numerical
   target for any onset-jet extension or resummation effort.
4. The 50%-gap finding correctly scopes the difficulty of Route 1A:
   it is months-grade not weeks-grade, even with the framework's
   existing mixed-cumulant audit machinery.

## What this kernel does NOT close

- The actual analytic value of `<P>(6)`. This kernel computes
  `P_1plaq` (the *one-plaquette block*), not the full
  `P_L(beta)` for the multi-plaquette Wilson partition function.
  The closure path remains: extend the onset jet, or use spectral-moment
  Hausdorff bracketing (Route 1B SDP), or V-invariant lattice bootstrap
  (Route 3).

- The Route 1A timeline. The 50% gap is qualitatively larger than the
  0.022% canonical-vs-bridge window, suggesting Route 1A as
  direct order-by-order extension is unlikely to be the fastest path.
  Borel resummation or direct multi-plaquette numerical evaluation are
  more promising.

## v-prediction sensitivity

For completeness, the kernel computes `dv/d<P>` at the canonical
`<P>(6) = 0.5934` point:

```
dv / d<P>                 =  -1.66 x 10^3 GeV per unit <P>
```

So a `0.022%` window on `<P>(6)` (canonical-vs-bridge) corresponds to
a `0.0876%` window on `v`. The bridge candidate `<P> = 0.59353`
gives `v = 246.07 GeV`, only `0.07%` from the canonical
`v = 246.28 GeV`. Both are within `0.07%` of the PDG `v = 246.22 GeV`.

## Verification

```bash
python3 scripts/frontier_hierarchy_route_1b_haar_evaluation.py
```

Reports the eight-step kernel pipeline. No assertions; this is a
numerical diagnostic note, not a class-A theorem note.

## Cross-references

- `HIERARCHY_H1_ROUTE_1_STATUS_CORRECTION_NOTE_2026-05-03.md` — parent;
  Route 1A and Route 1B paths.
- `GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md` — the
  reduction-law `P_L(beta) = P_1plaq(beta_eff,L(beta))`; this kernel
  computes the LHS factor `P_1plaq` numerically.
- `GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md` — the
  reference Perron solves; this kernel verifies `P_triv(6) =
  P_1plaq(6) = 0.4225317396` to ten digits.
- `GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md`
  — the order-`beta^5` jet underdetermination; this kernel demonstrates
  that the relevant *baseline* gap is 50%, not the 10^-7 witness-law
  gap, sharpening the Route 1A scope statement.
- `HIERARCHY_CLOSURE_PROGRAM_NOTE_2026-05-03.md` — top-level program;
  this kernel implies the Route 1A timeline is months-grade not
  weeks-grade and recommends Borel/Padé resummation as the more
  promising path.
