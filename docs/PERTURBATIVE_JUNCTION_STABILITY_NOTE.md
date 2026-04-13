# Perturbative Junction Stability for the Finite-Rank Non-`O_h` Source Class

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_perturbative_junction_stability.py`  
**Status:** Exact orbit-mean base law plus bounded first-order correction on the active finite-rank sector

## Purpose

The exact `O_h` shell/junction results already established that the whole-shell
bridge law is pointwise exact on each cubic orbit. The broader finite-rank
class is the remaining non-`O_h` test case.

This note turns the measured within-orbit deviations into a perturbative
statement:

> the finite-rank non-`O_h` family is a small deformation of the exact orbit-
> mean junction law, not a new shell law

## Orbit-mean base law

On the sewing band `3 < r <= 5`, the exact local `O_h` family and the broader
finite-rank family share the same orbit-mean profiles per unit charge:

- `u = phi_ext / Q`
- `k = sigma_R / Q`

So the exact orbit-mean junction law is fixed by the universal pair

- `ubar(r_orbit)`
- `kbar(r_orbit)`

and the same native bridge map as before:

- `rho_Q = Q k / (2 pi (1 + Q u)^5)`
- `S_Q = 0.5 rho_Q (1 / alpha_Q - 1)`
- `alpha_Q = (1 - Q u) / (1 + Q u)`

## Measured perturbation size

For the finite-rank family, the within-orbit corrections are small:

- `u` spread: about `1.3905%`
- `k` spread: about `1.6747%`
- bridge-side `rho` spread: about `1.3905%`
- bridge-side `S` spread: about `2.6295%`

The exact orbit-mean data also stay in a regular regime:

- `Q max(u) = 0.0906374`

So the bridge map remains uniformly smooth on the whole sewing band.

The band also splits into degenerate exact sectors and an active perturbative
sector:

- `6` orbit types have `ubar = 0` and remain exact zero-potential sectors
- `3` orbit types have `kbar = 0` and remain exact zero-shell sectors
- `8` orbit types are active and carry the nontrivial perturbative correction

## Perturbative correction theorem

Write the finite-rank orbit data as

- `u = ubar + du`
- `k = kbar + dk`

on each cubic orbit.

Then the junction map

- `J_Q(u, k) = (rho_Q(u, k), S_Q(u, k))`

is smooth on the sewing band, and on the active orbit sector it admits the
first-order correction

`J_Q(ubar + du, kbar + dk) = J_Q(ubar, kbar) + DJ_Q[du, dk] + R_Q`

with a bounded remainder `R_Q = O(epsilon^2)` for the perturbation size

`epsilon = max( ||du|| / ||ubar||, ||dk|| / ||kbar|| )`.

In the current finite-rank family, the measured linear-response remainder is:

- relative residual in `rho`: `2.18e-5`
- relative residual in `S`: `3.54e-5`

That is roughly a `6e2 - 7e2 x` reduction relative to the raw within-orbit
spread.

## Interpretation

This is the perturbative extension of the junction law that the broader
finite-rank non-`O_h` source class suggests:

- the `O_h` orbit law is the base solution
- the finite-rank family stays in a small perturbative tube around it
- the first-order correction captures the non-`O_h` deviation to about
  `10^-5` relative accuracy at the level of the tested orbit data

So the open problem is no longer whether the non-`O_h` family destroys the
junction law. It does not, at least on the tested star-supported family.
The remaining problem is to derive the correction operator a priori from the
microscopic lattice dynamics.

## What this closes

This closes the strongest perturbative objection on the current source
classes:

> the broader finite-rank non-`O_h` family is a controlled first-order
> deformation of the exact `O_h` junction law

## What this still does not close

This note still does **not** close:

1. the microscopic derivation of the correction operator from the lattice
   Hamiltonian
2. the general theorem for arbitrary non-`O_h` finite-rank source classes
3. the final pointwise 4D Einstein / Regge lift

## Updated gravity target

After this note, the remaining perturbative target is precise:

- prove the correction operator from the lattice dynamics rather than
  extracting it a posteriori
- then promote the corrected junction law into the full 4D metric closure
