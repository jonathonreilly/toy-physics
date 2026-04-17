# DM Leptogenesis Exact-Kernel Closure

**Date:** 2026-04-15  
**Status:** exact-kernel benchmark theorem on the refreshed `main`-derived DM
lane  
**Script:** `scripts/frontier_dm_leptogenesis_exact_kernel_closure.py`

## Framework sentence

In this note, "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

After the refreshed branch closes

- `c_odd = +1`
- `v_even = (sqrt(8/3), sqrt(8)/3)`
- `a_sel = 1/2`
- `tau_E = tau_T = 1/2`
- `K00 = 2`

what does the standard coherent leptogenesis kernel predict on the retained
benchmark?

## Bottom line

On the exact source-oriented branch,

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`
- `K00 = 2`

so the exact heavy-basis CP tensor channels are

- `cp1 = -2 gamma E1 / 3 = -0.544331...`
- `cp2 =  2 gamma E2 / 3 =  0.314270...`

Using the standard coherent sum

`epsilon_1 = |(1/8pi) y0^2 (cp1 f(x23) + cp2 f(x3)) / K00|`

gives

- `epsilon_1 / epsilon_DI = 0.9276209209...`

and, on the consistent retained-fit benchmark already used on this branch once
the exact `K00` denominator is used in both the CP kernel and the washout path,

- `eta / eta_obs = 0.5578749661...`

So the old reduced `0.30` benchmark is gone on the exact kernel, but the
current exact benchmark still remains quantitatively open.

## Exact source-side kernel package

The refreshed branch already fixes

- odd source: `gamma = 1/2`
- even responses: `E1 = sqrt(8/3)`, `E2 = sqrt(8)/3`
- heavy-basis diagonal: `K00 = 2`

Therefore the physical kernel is no longer an open shape or normalization
problem. It is an exact number on the retained benchmark.

## Exact epsilon law

The coherent heavy-basis kernel is

`epsilon_1 = |(1/8pi) y0^2 (cp1 f23 + cp2 f3) / K00|`.

With the exact source package:

- `cp1 = -0.544331...`
- `cp2 =  0.314270...`
- `K00 = 2`

and the staircase benchmark

- `k_A = 7`
- `k_B = 8`
- `eps/B = alpha_LM/2`

this yields

- `epsilon_1 = 2.4576198796e-6`
- `epsilon_DI = 2.6493795301e-6`
- `epsilon_1 / epsilon_DI = 0.9276209209`.

So the exact kernel now sits just below the DI ceiling, not far below it.

## Exact eta on the consistent retained benchmark

Keeping the same retained-fit washout benchmark already used by the branch, but
now with the exact `K00` normalization propagated consistently through the
washout bookkeeping,

- `K = 11.8090...`
- `kappa = 1.429205e-2`

gives

- `eta = 3.4141947926e-10`
- `eta_obs = 6.12e-10`
- `eta / eta_obs = 0.5578749661`.

## Consequence

This resolves the old DM denominator suppression on the refreshed branch:

- the exact source package is not too small
- the exact diagonal normalization is not open
- the exact coherent leptogenesis kernel sits close to the DI ceiling
- but the consistent retained-fit benchmark still undershoots observation

So this note is a benchmark-conditioned exact-kernel theorem, not a final
closure claim for baryogenesis.

## Scope

This note claims exact kernel closure on the retained benchmark already used on
the branch. It does not claim full baryogenesis closure, and it supersedes the
older reduced-kernel `0.30` reading scientifically.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_exact_kernel_closure.py
```
