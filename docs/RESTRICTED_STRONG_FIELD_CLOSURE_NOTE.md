# Restricted Strong-Field Closure on the Exact `O_h` Shell Class

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Status:** Promotable restricted strong-field gravity theorem; not full nonlinear GR

## Statement

On the exact local `O_h` star-supported source class currently realized on the
branch, the strong-field gravity program now has an exact restricted closure:

1. **Exact shell source**
   - the sewing shell is represented exactly as
     `sigma_R = H_0 (Pi_R^ext phi)` on `3 < r <= 5`
2. **Exact same-charge bridge**
   - the unique common-harmonic bridge is fixed by charge inheritance:
     `psi = 1 + phi_ext`, `chi = 1 - phi_ext = alpha psi`
3. **Exact pointwise shell law**
   - on the exact local `O_h` class, the shell observables are already
     pointwise orbit laws on the whole sewing band
4. **Exact local shell-to-`3+1` lift**
   - the pointwise fields
     `rho = sigma_R / (2 pi psi^5)` and
     `S = 0.5 rho (1/alpha - 1)`
     satisfy
     `H_0 psi = 2 pi psi^5 rho`,
     `H_0 chi = -2 pi alpha psi^5 (rho + 2S)`
     identically
5. **Exact microscopic boundary action**
   - the shell trace law is the stationary point of the exact Schur-complement
     boundary energy of the lattice Laplacian on the exterior domain
6. **Exact microscopic Dirichlet principle**
   - the shell trace is the unique global minimizer of that same boundary
     energy, so the native same-charge bridge is the minimum-energy discrete
     Dirichlet extension of the shell data

So on this source class, the shell law, bridge, shell-to-`3+1` lift, and
boundary action are no longer open. They form one exact restricted strong-field
closure package.

## Broader bounded consequence

For the broader exact finite-rank source family already on the branch:

- the same local static conformal constraints hold exactly
- the same microscopic Schur boundary action reproduces the exact shell trace
  law exactly
- the remaining non-`O_h` difference is the already-controlled small
  within-orbit shell variation:
  - `rho` about `1.4%`
  - `S` about `2.7%`
- the same strict convexity also turns the bridge into a unique minimum-energy
  Dirichlet extension on the current bridge surface

So the broader-family gap is no longer a new shell law or new boundary action.
It is a small pointwise deformation of the same closure package.

## What is promotable now

The following is now defensible to promote:

> On the exact local `O_h` strong-field source class, the framework admits an
> exact restricted strong-field closure consisting of an exact shell source,
> unique same-charge bridge, exact local static conformal constraint lift,
> exact microscopic Schur boundary action, and exact microscopic Dirichlet
> principle.

That is stronger than the earlier weak-field-only gravity surface.

## What is not yet promotable

This does **not** justify claiming:

1. fully general nonlinear GR
2. full pointwise Einstein/Regge closure beyond the current static conformal
   bridge
3. fully general non-`O_h` strong-field closure
4. no-horizon / no-echo as theorem-level downstream consequences

## Practical conclusion

Gravity is now promotable only in a **restricted strong-field** form, not as a
full universal GR derivation.
