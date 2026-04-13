# y_t Framework-Seeded Chain: RETRACTED

**Date:** 2026-04-13
**Script:** `frontier_yt_framework_seeded.py`
**Status:** RETRACTED — the /4 taste projection contradicts the Feshbach theorem

## What happened

The framework-seeded script divided α_plaq by N_taste = 4 to get α_s^EFT(M_Pl).
This gives m_t = 151 GeV (-13%).

## Why it's wrong

The Feshbach theorem (frontier_yt_gauge_crossover_theorem.py, 15/15 PASS) proves
Z_gauge = 1 EXACTLY to machine precision. The gauge coupling is NOT reduced by
taste projection. The /4 divisor directly contradicts this proven result.

## What replaces it

The gauge crossover chain WITHOUT the /4 gives m_t = 171.0 GeV (-1.1%):
1. α_plaq = 0.092 (framework)
2. α_MSbar(M_Pl) = 0.082 (V-to-MSbar, Schrödinger coefficients)
3. y_t(M_Pl) = g_s(M_Pl)/√6 (Ward identity, scheme-independent)
4. 2-loop SM RGE downward → m_t = 171.0 GeV

This chain uses framework coupling at M_Pl and runs downward. The observed
α_s(M_Z) does NOT enter. The gauge coupling at M_Z is a PREDICTION: the
crossover chain gives α_s(M_Z) ~ 0.12, close to observed 0.118.

## Gate status

y_t is CLOSED by the gauge crossover theorem chain. The framework-seeded /4
chain is retired.
