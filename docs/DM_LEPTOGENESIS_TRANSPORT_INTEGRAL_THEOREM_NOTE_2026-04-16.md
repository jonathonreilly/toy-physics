# DM Leptogenesis Transport-Integral Theorem

**Date:** 2026-04-16
**Branch:** `codex/dm-main-refresh`
**Script:** `scripts/frontier_dm_leptogenesis_transport_integral_theorem.py`
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`

## Result

The strong-washout efficiency factor is now replaced by a direct theorem-native
transport solve.

On normalized abundances:

- `N_{N1}^eq(z) = 0.5 z^2 K_2(z)`
- `N_{N1}^eq(0) = 1`

the authority transport equations are

- `dN_{N1}/dz = -D_H(z) (N_{N1} - N_{N1}^eq)`
- `dN_{B-L}/dz = D_H(z) (N_{N1} - N_{N1}^eq) - W_H(z) N_{B-L}`

with

- `D_H(z) = K_H z K_1(z)/K_2(z) / E_H(z)`
- `W_H(z) = K_H z^3 K_1(z) / (4 E_H(z))`

and `kappa_axiom[H] = |N_{B-L}(infty)|`.

## Diagnostic reference branch

On the diagnostic reference radiation branch `E_H(z)=1` with the old benchmark
`K_H = 47.23597962989828`, the direct transport solve gives

- `kappa_axiom,ref = 0.004829545290766509`

and the exact formal transport integral reproduces the same value.

The old fit on that same branch was

- `kappa_fit = 0.01427162724743994`

so the fit overstates transport by a factor

- `2.955066473761705`

and gives the wrong authority result.

Using the direct transport solve plus exact equilibrium bookkeeping gives

- `eta/eta_obs = 0.18878592785084122`

on that same diagnostic reference branch.
