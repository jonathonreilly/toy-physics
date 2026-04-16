# DM Leptogenesis Exact-Kernel Benchmark Audit

**Date:** 2026-04-15  
**Status:** benchmark audit on the refreshed `main`-derived DM lane  
**Script:** `scripts/frontier_dm_leptogenesis_exact_kernel_audit.py`

## Framework sentence

In this note, "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

After the refreshed branch lands the exact source package and the exact
diagonal normalization `K00 = 2`, how harshly should the resulting exact-kernel
leptogenesis benchmark be read?

## Bottom line

The refreshed branch now has a much stronger denominator story than before:

- the source amplitudes are closed
- the transfer coefficients are closed
- the heavy-basis diagonal normalization is closed
- the standard coherent kernel lands at
  `eta / eta_obs = 0.9907305394...`

But as a **benchmark audit**, two caution points remain:

1. the closure runner still uses retained benchmark ingredients for washout and
   thermal dilution
2. the code now makes the denominator bridge `/K00` explicit, so the remaining
   harsh-review question is the physical interpretation of that bridge inside
   the retained benchmark, not the source-side kernel itself

## Sensitivity

Because the refreshed exact-kernel result sits at

`eta / eta_obs = 0.9907305394...`,

it is percent-level close to observation. That is encouraging, but it also
means small retained-benchmark shifts matter:

- a `2%` shift in the retained prefactor moves the result across `eta_obs`
- a `5%` shift moves the ratio over the range
  `0.941 < eta/eta_obs < 1.040`

So the exact-kernel result is robust at order unity, but not yet intrinsically
sub-percent.

## What is now genuinely closed

The old weak-source story is no longer the right criticism.

The branch now has:

- exact source package:
  `gamma = 1/2`, `E1 = sqrt(8/3)`, `E2 = sqrt(8)/3`
- exact heavy-basis diagonal normalization:
  `K00 = 2`
- exact coherent benchmark kernel:
  `epsilon_1 / epsilon_DI = 0.9276209209...`

So the source-side kernel is no longer the soft spot.

## What is still benchmark-level

The refreshed closure runner still uses:

- retained thermal dilution `D_THERMAL`
- retained strong-washout fit
  `kappa ~ (0.3/K)(ln K)^0.6`

and it now makes the denominator bridge explicit through

`epsilon_1 = |(1/8pi) y0^2 (cp1 f23 + cp2 f3) / K00|`.

That is a strong benchmark closure. It is not yet the same thing as an
independent theorem that every physical projector in the full leptogenesis
chain is exhausted by `K00`.

## Harsh-review read

The right harsh-review sentence is now:

> the refreshed branch has exact source-side kernel closure on the retained
> benchmark, but the final percent-level `eta` match is still benchmark-level,
> not yet a theorem-level elimination of all washout / projection modelling.

That is a much stronger state than the old `0.30x` benchmark, but it is the
honest read.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_exact_kernel_audit.py
```
