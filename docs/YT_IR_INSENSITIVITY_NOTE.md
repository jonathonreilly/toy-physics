# y_t IR Insensitivity: Does the Quasi-Fixed Point Kill the Gauge Crossover?

**Date:** 2026-04-13
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_yt_ir_insensitivity.py`

---

## Status

**BOUNDED** -- the IR quasi-fixed-point of y_t/g_3 provides partial
focusing (factor 0.71) but does NOT make m_t insensitive to g_3(M_Pl).
The gauge crossover remains a genuine blocker.

---

## Theorem / Claim

**Claim (IR insensitivity hypothesis).** Because the top Yukawa y_t has
an IR quasi-fixed-point ratio y_t/g_3 -> sqrt(2/9), and the framework
enforces y_t = g_3/sqrt(6) at M_Pl, the prediction m_t(M_Z) should be
insensitive to the exact value of g_3(M_Pl). If true, the gauge crossover
(matching framework alpha_s to SM alpha_s) would be irrelevant for m_t.

**Result: REFUTED.**

The m_t spread across g_3(M_Pl) in [0.5, 2.0] is 55%, not <5%.

---

## Assumptions

1. **SM 2-loop RGEs** for the coupled (g1, g2, g3, yt, lambda) system.
2. **Framework boundary condition:** y_t(M_Pl) = g_3/sqrt(6), where g_3
   is varied as a free parameter.
3. **Split approach:** SM gauge coupling trajectory (from observed
   alpha_s(M_Z) = 0.1179) is used for the RGE evolution; only the y_t
   boundary is varied.

---

## What Is Actually Proved

### (A) Landau pole obstruction (EXACT)

For g_3(M_Pl) >= 0.8, the 1-loop QCD coupling develops a Landau pole
before reaching M_Z when run downward from M_Pl. Specifically:

| g_3(M_Pl) | Landau pole scale |
|-----------|------------------|
| 0.5       | none (safe)      |
| 0.8       | 10^11.4 GeV      |
| 1.0       | 10^14.2 GeV      |
| 1.075     | ~10^14.8 GeV     |
| 1.5       | 10^16.9 GeV      |
| 2.0       | 10^17.9 GeV      |

The framework value g_3 = 1.075 (alpha_s = 0.092) hits its Landau pole
around 10^15 GeV. This means the naive approach (running the framework
coupling all the way down) is impossible.

### (B) Split approach: m_t IS sensitive to y_t(M_Pl) (10/10 PASS, 1 FAIL)

Using the SM g_3 trajectory but varying y_t(M_Pl) = g_3_test/sqrt(6):

| g_3_test | y_t(M_Pl) | y_t(M_Z) | m_t [GeV] | dev   |
|---------|----------|---------|----------|-------|
| 0.5     | 0.204    | 0.685   | 119.3    | -31%  |
| 0.8     | 0.327    | 0.925   | 161.0    | -7%   |
| 1.0     | 0.408    | 1.028   | 178.9    | +3%   |
| 1.5     | 0.612    | 1.174   | 204.4    | +18%  |
| 2.0     | 0.817    | 1.244   | 216.5    | +25%  |

Total spread: 97.3 GeV (55.3%).

### (C) IR focusing is real but weak (BOUNDED)

The Pendleton-Ross attractor does partially compress the y_t spread:

    y_t(M_Pl) ratio (framework/SM): 2.20x
    y_t(M_Z) ratio (framework/SM):  1.57x
    Focusing factor: 0.71

A 2.2x range in UV boundary conditions is compressed to 1.57x at M_Z.
This is consistent with the convergence exponent of 1/14 found in
YT_FIXED_POINT_NOTE.md -- very weak focusing.

### (D) Framework split prediction (BOUNDED)

Using the framework y_t(M_Pl) = 0.439 (from g_3 = 1.075) with the SM
gauge trajectory gives m_t = 184.2 GeV (+6.5% from observed 173 GeV).
This is within the expected matching uncertainty.

### (E) The sensitivity decreases at large y_t (BOUNDED)

The numerical derivative d(m_t)/d(g_3_test) decreases with g_3_test:

    g_3 in [0.5, 0.8]: 139 GeV per unit g_3
    g_3 in [0.8, 1.0]:  90 GeV per unit g_3
    g_3 in [1.0, 1.5]:  51 GeV per unit g_3
    g_3 in [1.5, 2.0]:  24 GeV per unit g_3

The approach to the quasi-fixed-point is visible (the curve flattens),
but the residual sensitivity at the framework value is still ~50 GeV
per unit g_3.

---

## What Remains Open

The gauge crossover remains a genuine open problem. The framework predicts
alpha_s(M_Pl) = 0.092 (V-scheme), which is 4.8x the SM MSbar value at
M_Pl (0.019). This mismatch cannot be resolved by IR focusing of y_t/g_3.

---

## How This Changes The Paper

This result CONFIRMS the existing blocker assessment. The gauge crossover
is NOT rendered irrelevant by the IR quasi-fixed-point.

Paper-safe statement:

> The Pendleton-Ross quasi-infrared fixed point provides a focusing
> factor of 0.71 for the y_t/g_3 ratio from M_Pl to M_Z, but this
> is insufficient to make m_t insensitive to the UV boundary condition.
> The m_t prediction in the split approach (SM gauge trajectory with
> framework y_t boundary) gives m_t = 184 GeV (+6.5%), contingent on
> resolving the strong coupling crossover.

NOT paper-safe:

> The IR quasi-fixed-point makes the gauge crossover irrelevant.
> m_t is insensitive to g_3(M_Pl).

---

## Commands Run

```bash
cd "/Users/jonBridger/Toy Physics"
python3 scripts/frontier_yt_ir_insensitivity.py   # 10 PASS, 1 FAIL (expected)
```
