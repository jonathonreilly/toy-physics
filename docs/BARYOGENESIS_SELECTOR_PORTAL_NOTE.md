# Baryogenesis Selector Portal Note

**Date:** 2026-04-16
**Status:** bounded/open support target on `main`
**Script:** `scripts/frontier_baryogenesis_selector_portal.py`

## Safe statement

Yes, the actual derived lattice taste-scalar surface already fixes a natural
portal scale for the old baryogenesis route.

The exact graph-first quartic invariant on the three-component taste-selector
surface determines the ratio between:

- the self-quartic along the selected Higgs axis, and
- the orthogonal taste-scalar portal term.

Once that exact ratio is matched to the promoted Higgs quartic `lambda_H`, the
effective portal in the baryogenesis high-`T` ansatz is no longer free:

`kappa_sel = 6 lambda_H`.

That lands almost exactly on the previously derived cubic-target window.

## Starting point: exact graph-first quartic invariant

The canonical graph-shift surface gives

`H(phi) = sum_i phi_i S_i`

with exact quartic trace

`Tr H(phi)^4 = 8 (sum_i phi_i^4 + 6 sum_{i<j} phi_i^2 phi_j^2)`.

This is the full quartic object. The old selector note isolated only the
anisotropic piece

`V_sel = 32 sum_{i<j} phi_i^2 phi_j^2`

after subtracting the isotropic quartic. For portal physics the full quartic
trace matters, because it fixes both:

- the axis self-quartic
- the orthogonal cross-coupling

with one common prefactor.

## Exact portal ratio

Write the quartic potential on this surface as

`V_4(phi) = A Tr H(phi)^4`.

Then

`V_4(phi) = 8 A sum_i phi_i^4 + 48 A sum_{i<j} phi_i^2 phi_j^2`.

Choose the EWSB axis `phi = (h,0,0)`. Along that axis:

`V_4(h,0,0) = 8 A h^4`.

Matching to the promoted Higgs convention

`V_H(h) = lambda_H h^4 / 4`

gives

`A = lambda_H / 32`.

Now turn on one orthogonal taste-scalar direction `s`:

`V_4(h,s,0) = lambda_H h^4 / 4 + (3/2) lambda_H h^2 s^2 + lambda_H s^4 / 4`.

So the exact graph-first surface fixes the portal coefficient:

`alpha_hs = 3 lambda_H / 2`

for the `h^2 s^2` term.

## Mapping to the baryogenesis `kappa` convention

The baryogenesis cubic-target note parameterized a scalar mode by

`m_s^2(h) = (kappa / 2) h^2`.

For

`V(h,s) superset alpha_hs h^2 s^2`

the orthogonal scalar mass in the Higgs background is

`m_s^2(h) = d^2V/ds^2 = 2 alpha_hs h^2 = 3 lambda_H h^2`.

Therefore

`kappa_sel / 2 = 3 lambda_H`

so the exact selector prediction is

`kappa_sel = 6 lambda_H`.

## Numerical result on the current promoted package

Using the current Higgs routes:

- `lambda_H = 0.118249` at `m_H = 119.77 GeV`
- `lambda_H = 0.129008` at `m_H = 125.10 GeV`

the exact selector portal gives:

- `kappa_sel = 0.7095` on the 2-loop Higgs support route
- `kappa_sel = 0.7740` on the full 3-loop Higgs route

The previously derived cubic-target window was:

- `kappa_target = 0.6853` on the 2-loop support route
- `kappa_target = 0.7441` on the full 3-loop route

So the exact selector portal lands only about `3.5%` to `4.0%` above the bare
target:

- `kappa_sel / kappa_target = 1.035`
- `kappa_sel / kappa_target = 1.040`

## Why this matters

This is the first same-surface result showing that the old taste-scalar
baryogenesis route does not need an arbitrarily inserted portal.

The actual lattice selector surface already gives an order-1 portal of the
right size.

Even better, the slight overshoot is in the correct direction:

- the cubic-target note used the undressed one-loop scalar cubic term
- thermal screening / daisy resummation would increase the required `kappa`
  above the bare target

So the exact selector portal is not too small. It is slightly stronger than
the unscreened target, which is the favorable side of the comparison.

## Conditional minimal-doublet interpretation

The selector note does **not** yet prove the multiplicity of the finite-`T`
scalar spectrum.

But if the old route-history phrase "2HDM-like taste-scalar spectrum" means
one extra complex doublet with `n = 4` real bosonic degrees of freedom, then
inserting the derived selector portal into the one-loop cubic formula gives:

- `Delta E_sel / Delta E_target = 1.053` on the 2-loop support route
- `Delta E_sel / Delta E_target = 1.061` on the full 3-loop route

So on that minimal route interpretation, the exact selector portal almost
exactly saturates the required enhancement before screening effects.

## What this closes

This note closes the next same-surface question:

> "Can the actual derived lattice taste-scalar surface generate the required
> portal scale, or was that scale only an external guess?"

Answer:

- yes, the exact graph-first quartic invariant gives
  `kappa_sel = 6 lambda_H`
- on the current package surface that means `kappa_sel ~= 0.71 - 0.77`
- that is already almost exactly the required baryogenesis portal window

## What remains open

This note does **not** yet close:

- the multiplicity of the relevant finite-`T` scalar modes
- thermal screening / daisy resummation on the retained surface
- a first-principles finite-`T` effective potential
- a lattice sphaleron rate
- transport / diffusion
- a derived `eta`

So the open baryogenesis question is now narrower:

- not "where would a strong enough portal come from?"
- but "does the actual finite-`T` taste-scalar spectrum realize the required
  multiplicity and survive screening strongly enough?"

## Validation

- [frontier_baryogenesis_selector_portal.py](./../scripts/frontier_baryogenesis_selector_portal.py)
- [BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md](./BARYOGENESIS_TASTE_SCALAR_CUBIC_TARGET_NOTE.md)
- [GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md](./GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)

Current runner state:

- `frontier_baryogenesis_selector_portal.py`: expected `PASS>0`, `FAIL=0`
