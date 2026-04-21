# DM Current-Bank Quantitative Mapping

**Date:** 2026-04-21
**Status:** reviewer-facing mapping item closed; the flagship gate remains open.
**Runner:** `scripts/frontier_dm_current_bank_quantitative_mapping_2026_04_21.py`

---

## Review-surface target

One of the remaining DM review items was purely quantitative packaging:

> explicit quantitative DM observable mapping from the current exact bank.

This note closes that item by assembling the already-retained exact bank into
one reviewer-facing table and checking that every mapped quantity is finite,
internally consistent, and physically interpretable.

This is **not** a new selector theorem and **not** full DM flagship closure.
It is the explicit quantitative readout of the current bank.

## Approach

The exact package in `scripts/dm_leptogenesis_exact_common.py` already
contains the needed ingredients:

- source-sector primitives `gamma`, `E_1`, `E_2`, `cp_1`, `cp_2`
- heavy-neutrino masses `M_1`, `M_2`, `M_3`
- CP asymmetry `epsilon_1` and Davidson-Ibarra benchmark `epsilon_DI`
- thermal scales `m_tilde`, `m_star`, `k_decay`, `kappa_fit`
- baryon-asymmetry ratio `eta_fit / eta_obs`

The work here is to expose that bank as one explicit quantitative mapping.

## Mapping table

| Bank quantity | Value | Physical observable | Compares to |
|---|---|---|---|
| `gamma` | `0.5` | Source breaking-triplet amplitude | retained constant `1/2` |
| `E_1` | `1.6330` | Source breaking-triplet amplitude | `sqrt(8/3)` retained |
| `E_2` | `0.9428` | Source breaking-triplet amplitude | `sqrt(8)/3` retained |
| `cp_1` | `-0.5443` | Breaking-triplet CP parameter | `-2 gamma E_1 / 3` |
| `cp_2` | `+0.3143` | Breaking-triplet CP parameter | `+2 gamma E_2 / 3` |
| `M_1` | `5.323 x 10^10 GeV` | Lightest RH neutrino mass | seesaw scale |
| `M_2` | `5.829 x 10^10 GeV` | Second RH neutrino mass | quasi-degenerate pair |
| `M_3` | `6.150 x 10^11 GeV` | Heaviest RH neutrino mass | hierarchical `2+1` pattern |
| `M_3/M_1` | `11.55` | Heavy-mass hierarchy ratio | current exact bank |
| `epsilon_1` | `2.458 x 10^-6` | CP asymmetry in `N_1` decay | leptogenesis source |
| `epsilon_DI` | `2.650 x 10^-6` | Davidson-Ibarra upper bound | benchmark |
| `epsilon_1/epsilon_DI` | `0.9276` | CP asymmetry relative to DI bound | near saturation |
| `m_tilde` | `0.1012 eV` | Effective neutrino mass | strong-washout scale |
| `m_star` | `2.143 x 10^-3 eV` | Equilibrium washout mass | thermal benchmark |
| `k_decay` | `47.24` | Dimensionless washout | strong-washout regime |
| `kappa_fit` | `0.01427` | Thermal efficiency | Kolb-Turner fit |
| `eta_fit/eta_obs` | `0.5579` | Baryon-asymmetry ratio | Planck `eta_obs` |

## What the numbers show

The assembled map is internally coherent:

- the source-sector identities match the retained exact formulas
- the heavy-neutrino masses form the expected quasi-degenerate-plus-hierarchical pattern
- the CP asymmetry sits close to the Davidson-Ibarra benchmark
- the washout parameters lie in a sensible strong-washout regime
- the resulting baryon asymmetry is of the correct order of magnitude

That last point matters, but should be read honestly. `eta_fit/eta_obs = 0.5579`
means the current bank produces a quantitatively meaningful cosmological
output, not that the full flagship gate is closed.

## Runner summary

The accompanying runner passes `17/17` checks across:

- source-sector primitives
- heavy-neutrino spectrum
- CP asymmetry and DI comparison
- washout scales
- baryon-asymmetry bookkeeping
- cosmological constants
- mapping completeness
- overall consistency

## Honest verdict

What closes here:

- the reviewer-facing **current-bank quantitative DM mapping** item
- explicit quantitative exposure of the current exact bank
- completeness of the mapping table for the retained bank quantities used in
  the current leptogenesis package

What does **not** close here:

- the `A-BCC` branch-choice law
- the finer right-sensitive microscopic selector law
- the residual split-2 exact-carrier dominance/completeness theorem
- the full DM flagship gate

So the right package read is:

> the quantitative mapping item is closed as bookkeeping and reviewer-facing
> presentation of the exact bank, while the science-critical selector and
> carrier-side theorem gaps remain open.
