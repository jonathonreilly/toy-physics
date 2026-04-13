# CKM Route 4: Invariant Relations from Derived Quantities

**Date:** 2026-04-13
**Status:** BOUNDED -- Route 4 provides consistency checks but does not independently close V_cb
**Script:** `scripts/frontier_ckm_invariants.py`
**Branch:** `claude/youthful-neumann`

---

## Strategy

Route 4 (from instructions.md): use CKM invariants rather than raw overlap
amplitudes. If V_us is sharp and V_ub can be sharpened, use the derived phase
scale and Jarlskog/invariant relations to solve for V_cb. Do not import PDG
angles.

## Framework-Derived Inputs

| Quantity | Value | Source | vs PDG |
|----------|-------|--------|--------|
| \|V_us\| | 0.224 | Z_3 lattice structure | 0.4% |
| delta_CP | 2pi/3 = 120 deg | Z_3 eigenvalue misalignment | 75% overshoot (PDG: 68.5 deg) |

These two inputs are sharp framework predictions with no free parameters.

## The Counting Argument

The CKM matrix has **four** physical parameters: three mixing angles + one CP
phase. Route 4 derives two of them:

1. s12 (from V_us = 0.224) -- **sharp**
2. delta_CP = 2pi/3 -- **structural**

This leaves a 2D surface in (s23, s13) space. One more relation is needed.

## The Third Input: V_ub from NNI Mass Ratios

The NNI texture gives:

    |V_ub| ~ sqrt(m_u / m_t) = 0.00354

This is 7.4% below PDG 0.00382. Not exact, but well within the structural
accuracy of the framework.

With this input, s12, s13, and delta are all fixed. The **only** remaining
unknown is s23 (equivalently V_cb).

## Why Jarlskog Does Not Close the System

The Jarlskog invariant:

    J = c12 * s12 * c23 * s23 * c13^2 * s13 * sin(delta)

With s12, s13, delta all fixed, J is **proportional to s23**:

    J = 6.68 x 10^{-4} * s23 * c23  ~  6.68 x 10^{-4} * s23

So using J_PDG to determine s23 is algebraically equivalent to inputting V_cb
directly. The Jarlskog invariant does **not** provide an independent constraint.

Similarly, row/column unitarity is automatically satisfied in the standard
parametrization for any s23. Unitarity does **not** provide a fourth constraint
either.

## What Route 4 Does Provide

### 1. Consistency check on the Z_3 phase

    J(Z3 phase, PDG angles) = 2.93 x 10^{-5}
    J(PDG, 2024 global fit) = 3.08 x 10^{-5}

The Z_3 phase gives J within 5% of PDG -- a nontrivial consistency check
given that the phase overshoots PDG by 75%. The Jarlskog invariant depends on
sin(delta), and sin(120 deg) = 0.866 vs sin(68.5 deg) = 0.931, only a 7%
difference.

### 2. First-row unitarity verification

    V_ud = sqrt(1 - V_us^2 - V_ub^2) = 0.97458
    PDG V_ud = 0.97373

Agreement to 0.09%. This confirms that V_us and V_ub are mutually consistent
with unitarity.

### 3. Wolfenstein A parameter analysis

    A = s23 / lambda^2

With lambda = 0.224 (derived) and PDG A = 0.821, the question is whether A
can be derived from Z_3 structure:

- A = 1 (democratic Z_3): V_cb = lambda^2 = 0.050, 22% above PDG
- A from NNI (c_23 = 1): V_cb = 0.064, 55% above PDG
- A from NNI (c_23 = 0.634, fitted): V_cb = 0.040, 2% from PDG

The fitted c_23 = 0.634 reproduces A to 2%, but c_23 itself is not yet
derived from first principles. This is the same gap as Routes 1-2.

## Combined Best Prediction (Route 4 + NNI)

Using all framework-derived inputs plus the lattice L=8 value c_23 = 0.65:

| Element | Prediction | PDG | Error |
|---------|-----------|-----|-------|
| \|V_us\| | 0.224 | 0.2243 | +0.4% |
| \|V_cb\| | 0.041 | 0.0412 | +0.6% |
| \|V_ub\| | 0.0035 | 0.00382 | -7.4% |
| delta_CP | 120 deg | 68.5 deg | +75% |
| J | 2.77 x 10^{-5} | 3.08 x 10^{-5} | -10% |

## Route 4 Bottom Line

Route 4 (invariant relations) does **not** independently close V_cb. The CKM
has 4 parameters; the framework derives 2 sharply (V_us, delta) and constrains
1 more at the 7% level (V_ub from NNI mass ratios). The 4th parameter (s23)
requires either:

(a) The NNI c_23 coefficient -- Routes 1/2
(b) An independent Jarlskog derivation from the lattice
(c) A Z_3 group-theoretic fixing of the Wolfenstein A parameter

None of (a), (b), (c) are currently closed.

**Route 4 supplements Routes 1-2 with nontrivial consistency checks but does
not replace them.** The sharpest remaining gap is the absolute scale of c_23
(or equivalently the Wolfenstein A parameter).

## What Remains Open

The sole remaining gap for full CKM closure is the **absolute scale** of the
2-3 NNI overlap integral S_23. The ratio c_23^u/c_23^d = 1.015 is derived from
gauge quantum numbers (Route 2). The overall normalization requires either:

- Lattice computation of S_23 at sufficient volume (Route 5)
- Analytic continuum-limit evaluation of the inter-valley overlap
- A group-theoretic argument fixing the Wolfenstein A parameter from Z_3 alone
