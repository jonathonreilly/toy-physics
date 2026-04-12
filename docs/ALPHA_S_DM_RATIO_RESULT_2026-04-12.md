# α_s and Dark Matter Ratio — Preliminary Result

**Date:** 2026-04-12
**Status:** Intriguing but not yet sharp. Needs review scrutiny.

## What Was Computed

The bare coupling on a 3D staggered lattice: α_bare = 1/(4π) = 0.0796.
With tadpole improvement: α_V = 0.092 ± 0.01.
The dark matter to baryon ratio R = Ω_DM/Ω_b depends on α through
Sommerfeld enhancement.

## The Match

| Quantity | Framework | Observed | Ratio |
|---|---|---|---|
| α_s(lattice) | 0.092 ± 0.01 | 0.092 (required for R_obs) | 1.00 |
| R = Ω_DM/Ω_b | 5.48 | 5.47 | 1.00 |

## Honest Assessment

**Why this might be real:**
- The bare coupling 1/(4π) comes from the lattice geometry with no tuning
- The DM ratio match is a parameter-free consequence

**Why this might be coincidental:**
- Multiple "approaches" give α from 0.079 to 0.119 — wide range
- The tadpole correction (15.9%) is an estimate, not exact
- The Sommerfeld model for DM is itself an assumption
- The derivation chain has several weak links

**Verdict:** Suggestive but not yet at the level of the CC result.
Needs tighter control on the tadpole correction and a clear
single derivation path (not 6 different approaches).

## Scripts

- `scripts/frontier_alpha_s_determination.py`
- `scripts/frontier_alpha_s_robustness.py`
