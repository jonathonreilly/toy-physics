# Anderson Phase Map Note at `mu2 = 0.001`

**Date:** 2026-04-11  
**Status:** bounded retained companion on `main`  
**Script:** `scripts/frontier_anderson_phase_unscreened_periodic.py`

## Scope

This is a fresh unscreened recheck of the Anderson-vs-gravity phase-map lane on
the **corrected periodic 2D torus surface** after the validated minimum-image
wraparound fix.

This note intentionally does **not** update the retained mixed
eigenvalue/Anderson note. It answers one narrower question:

> On the corrected periodic torus, does lowering the field mass to
> `mu2 = 0.001` strengthen, weaken, or qualitatively change the
> gravity-vs-disorder separation?

## Surface

- periodic `L x L` staggered lattices with `L in {6, 8, 10, 12}`
- `G in {0.5, 1, 2, 5, 10, 20, 50}`
- `mu2 = 0.001`
- `MASS = 0.30`, `DT = 0.12`, `N_STEPS = 30`, `SIGMA = 1.5`
- disorder controls: 5 matched Gaussian draws per row using the self-gravity
  mean and standard deviation of `Phi`
- primary discriminator: boundary-law coefficient separation `sigma_alpha`
- auxiliary discriminator: sign-margin separation `sigma_sign`

## Result

### 1. The boundary-law separation strengthens numerically

Every tested row satisfies `sigma_alpha > 3`:

- `L=6`: `sigma_alpha = 3.3` for all tested `G`
- `L=8`: `sigma_alpha = 20.9 - 21.3`
- `L=10`: `sigma_alpha = 3.1 - 3.3`
- `L=12`: `sigma_alpha = 6.0 - 6.3`

Strongest single point:

- `L=8`, `G=50`: `sigma_alpha = 21.3`

Cross-size support on the two more stable larger sizes:

- both `L=10` and `L=12` exceed `3σ` at **every tested `G`**

So relative to the screened `mu2 = 0.22` phase note, the numerical separation
from matched disorder is stronger.

### 2. The interpretation changes qualitatively

At `mu2 = 0.001`, both the gravitational and random-control boundary-law
coefficients collapse toward zero as `G` increases. Representative rows:

- `L=10`, `G=0.5`:
  - `alpha_grav = 1.3033e-02`
  - `alpha_rand = 1.2916e-02`
  - `delta_alpha = 1.1669e-04`
- `L=10`, `G=5`:
  - `alpha_grav = 2.6403e-04`
  - `alpha_rand = 2.6100e-04`
  - `delta_alpha = 3.0305e-06`
- `L=10`, `G=50`:
  - `alpha_grav = 3.8307e-06`
  - `alpha_rand = 3.7849e-06`
  - `delta_alpha = 4.5803e-08`

The same pattern holds on every size:

- `alpha_grav > alpha_rand_mean` on all 28 rows
- but the **absolute** differences are small and get extremely small at large
  `G`
- the large `sigma_alpha` values arise because the matched-disorder control
  variance is also very small

So the unscreened lane is **not** best described as a sharper perturbative
window. It becomes a nearly size-stable, near-uniform low-`alpha` separation.

## Sign Diagnostic

The sign row is not the main result here and remains weak as a disorder
discriminator:

- gravity sign margin is positive on all `28/28` rows
- random-control mean sign margin is also positive on `21/28` rows
- `sigma_sign` stays modest:
  - `L=6`: `2.0`
  - `L=8`: `0.5`
  - `L=10`: `0.8`
  - `L=12`: `0.5`

So the unscreened phase-map distinction lives in the boundary-law coefficient,
not in the sign-margin row.

## Comparison to the screened note

Relative to the corrected screened periodic note:

- **strengthens numerically:** yes
  - the largest `sigma_alpha` values are much bigger
  - `L=10` and `L=12` stay above `3σ` on all tested `G`
- **weakens:** no, not on the main boundary-law metric
- **qualitatively changes:** yes
  - the old finite perturbative-window reading no longer fits well
  - the unscreened result is closer to a uniform low-`alpha` flattening
    separation on this torus surface

## Honest interpretation

The clean statement is:

> On the corrected periodic 2D torus, lowering the field mass to
> `mu2 = 0.001` strengthens the **numerical** boundary-law separation from
> matched Anderson disorder, but the lane changes character. The result is no
> longer best described as a narrow perturbative window; it becomes a
> near-uniform low-`alpha` separation whose significance comes from small,
> consistent offsets against a low-variance matched-disorder control.

That is useful and worth preserving, but it is still a bounded torus-surface
result. It does **not** by itself promote the lane to an architecture-wide or
continuum claim.

## Retention boundary

- Keep this as a dedicated unscreened companion note to the corrected periodic
  Anderson lane.
- Use it to say:
  - unscreening does **not** kill the gravity-vs-disorder distinction
  - the main discriminator is still the boundary-law coefficient
  - the meaning of the phase map changes under unscreening
- Do **not** use it to say:
  - the disorder separation is now universally stronger in a physically
    stronger sense
  - sign selectivity cleanly separates gravity from disorder on this surface
  - the torus lane closes gravity-vs-disorder generally
