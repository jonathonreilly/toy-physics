# y_t/g_3 Quasi-Infrared Fixed Point: Independent Derivation

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_yt_fixed_point.py`

---

## Status

**BOUNDED** -- the Pendleton-Ross quasi-infrared fixed point of y_t/g_3 is
analytically derived as sqrt(2/9), which is NOT equal to the Cl(3) lattice
value 1/sqrt(6). The "double protection" hypothesis is false.

---

## Theorem / Claim

**Theorem (Pendleton-Ross fixed point, QCD-only limit).** The 1-loop SM
RGE system for y_t and g_3 has a quasi-infrared fixed point at

    R* = (y_t/g_3)^2 = 2/9

i.e. y_t/g_3 = sqrt(2/9) = 0.4714.

**Proof.** Define R = y_t^2 / g_3^2. The 1-loop beta functions give:

    dR/dt = (2 g_3^2 / (16 pi^2)) * R * [(9/2) R - 1]

Setting dR/dt = 0 with R > 0 yields R* = 2/9.

**Claim (comparison with Cl(3) lattice).** The lattice trace identity gives
R_lattice = 1/(2 N_c) = 1/6.  The ratio R*/R_lattice = 4/3 exactly.
The discrepancy in y_t/g_3 is 15.5%.

The lattice boundary condition is NOT at the IR fixed point.

---

## Assumptions

1. **Standard Model 1-loop beta functions.** The top Yukawa beta function
   is beta_yt = yt/(16pi^2) [9/2 yt^2 - 8 g3^2 - 9/4 g2^2 - 17/12 g1^2].
   The QCD beta function is beta_g3 = -7 g3^3/(16pi^2).

2. **QCD-only limit for the analytical fixed point.** Setting g_1 = g_2 = 0
   gives the cleanest result. Including EW contributions makes the
   discrepancy worse (R* increases further from 1/6).

---

## What Is Actually Proved

### Exact results (13/13 PASS):

**(A) Analytical fixed point.** R*_QCD = 2/9 exactly.  This follows from
(c_3 + b_3)/c_t = (8 - 7)/(9/2) = 2/9 where:
- c_3 = 8 (QCD contribution to top Yukawa anomalous dimension)
- b_3 = -7 (QCD beta function coefficient, n_f = 6)
- c_t = 9/2 (top Yukawa self-coupling)

**(B) Discrepancy.** R* = 2/9 != R_lattice = 1/6.  The ratio is exactly
4/3.  In terms of y_t/g_3: sqrt(2/9) = 0.4714 vs 1/sqrt(6) = 0.4082,
a 15.5% discrepancy.

**(C) Full SM fixed point.** Including electroweak contributions at M_Z:
R*_full = 0.392 (y_t/g_3 = 0.626), which is further from 1/6 than the
QCD-only value.

**(D) IR attractor.** The fixed point is an infrared attractor. The
linearized convergence exponent is 1/14, giving very weak focusing:
deviations from R* shrink by only ~2% from M_Planck to M_Z.

**(E) Numerical verification.** Full 1-loop RGE integration confirms:
- Lattice BC (1-loop extrapolated g_3): R evolves from 1/6 to 0.265 at M_Z
- The flow is toward the fixed point but very slow
- The UV boundary condition dominates the IR prediction

---

## What Remains Open

Nothing is open in this lane -- the question has a definitive negative
answer. The Pendleton-Ross fixed point is sqrt(2/9), not 1/sqrt(6).

---

## How This Changes The Paper

This result does NOT change the paper claims. It refutes a speculative
hypothesis that was never part of the audited surface.

Paper-safe statement:

> The Pendleton-Ross quasi-infrared fixed point of the SM y_t/g_3 system
> is R* = 2/9 (y_t/g_3 = sqrt(2/9) = 0.471), which differs from the
> Cl(3) lattice value R = 1/6 (y_t/g_3 = 1/sqrt(6) = 0.408) by 15.5%.
> The lattice boundary condition is not at the IR fixed point. The top
> Yukawa prediction depends entirely on the UV boundary condition being
> protected by Cl(3) centrality and carried through SM RGE running.

NOT paper-safe:

> The lattice boundary condition is automatically at the IR fixed point.
> The y_t prediction is doubly protected.

---

## Detailed Derivation

### Setup

The 1-loop SM RGEs (neglecting bottom and tau Yukawas):

    d(y_t)/dt = y_t/(16 pi^2) [9/2 y_t^2 - 8 g_3^2 - 9/4 g_2^2 - 17/12 g_1^2]
    d(g_3)/dt = -7 g_3^3 / (16 pi^2)

where t = ln(mu/M_Z).

### Fixed point of the ratio

Define R = y_t^2 / g_3^2. Then:

    dR/dt = (2/g_3^2) [y_t * dy_t/dt - R * g_3 * dg_3/dt]

Substituting the betas and simplifying (QCD only, g_1 = g_2 = 0):

    dR/dt = (2 g_3^2 / (16 pi^2)) * R * [(9/2) R - (8 - 7)]
          = (2 g_3^2 / (16 pi^2)) * R * [(9/2) R - 1]

The fixed point dR/dt = 0 gives:

    R* = 2/9

### Comparison

    R*       = 2/9     = 0.2222...   (Pendleton-Ross)
    R_lattice = 1/6     = 0.1667...   (Cl(3) trace identity)
    Ratio    = (2/9)/(1/6) = 4/3     (exact)

### Stability

Near R*, the linearized flow has exponent:

    d(delta R)/dt ~ (2 g_3^2 / (16 pi^2)) * delta R

The convergence rate scales as (alpha_s)^{1/14}, giving negligible
focusing over the desert from M_Planck to M_Z.

### Including electroweak corrections

With g_1, g_2 nonzero:

    R* = [1 + (9/4)(g_2/g_3)^2 + (17/12)(g_1/g_3)^2] / (9/2)

At M_Z this gives R* = 0.392, i.e. y_t/g_3 = 0.626, which is
even further from the lattice value 1/sqrt(6) = 0.408.

---

## Commands Run

```bash
cd "/Users/jonBridger/Toy Physics"
python3 scripts/frontier_yt_fixed_point.py   # 13/13 PASS
```
