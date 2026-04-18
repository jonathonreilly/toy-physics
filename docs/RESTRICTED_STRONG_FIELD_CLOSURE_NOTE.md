# Restricted Strong-Field Closure on the Exact `O_h` Shell Class

**Date:** 2026-04-13  
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

So the broader-family gap is no longer a new shell law or new boundary action.
It is a small pointwise deformation of the same closure package.

## What is promotable now

The following is now defensible to promote:

> On the exact local `O_h` strong-field source class, the framework admits an
> exact restricted strong-field closure consisting of an exact shell source,
> unique same-charge bridge, exact local static conformal constraint lift, and
> exact microscopic Schur boundary action.

That is stronger than the earlier weak-field-only gravity surface.

## What is not yet promotable

This does **not** justify claiming:

1. fully general nonlinear GR
2. full pointwise Einstein/Regge closure beyond the current static conformal
   bridge
3. fully general non-`O_h` strong-field closure
4. no-horizon / no-echo as theorem-level downstream consequences
   (a NARROWER retained pair is now available in
   [EVANESCENT_BARRIER_AMPLITUDE_SUPPRESSION_THEOREM_NOTE.md](./EVANESCENT_BARRIER_AMPLITUDE_SUPPRESSION_THEOREM_NOTE.md):
   (A) a rigorous discrete-Schroedinger lattice transfer-matrix amplitude
   bound on `Cl(3)/Z^3` with `a = l_Planck` and (B) the exact
   Schwarzschild-interior tortoise-length identity.  These do NOT
   promote the Planck-unit astrophysical exponent
   `exp[-(R_S/l_P) ln(R_S/R_min)]` to retained — that step requires an
   open conditional (C-rate) on the per-unit-tortoise-length evanescent
   rate that is NOT on the retained surface — but they do give the
   bounded GW-echo companion a retained pair it can quote by name)

## Practical conclusion

Gravity is now promotable only in a **restricted strong-field** form, not as a
full universal GR derivation.
