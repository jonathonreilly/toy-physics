# Native Same-Charge Static Bridge Closure

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_native_static_bridge_closure.py`  
**Status:** Exact same-charge bridge closure on current source classes plus bounded 4D support

## Purpose

The last substantial conceptual objection in the gravity line was:

> the static isotropic bridge might still be an imported GR closure condition
> rather than something fixed by the lattice source law itself

The previous work had already solved:

- exact shell-source decomposition
- exact radial DtN shell kernel
- exact reduced junction operator
- exact reduced whole-shell stress lift
- exact orbit-mean whole-shell law

What was still not said cleanly enough was why the bridge pair

- `psi = 1 + phi`
- `chi = alpha psi = 1 - phi`

should be the **same-charge** bridge fixed by the lattice source law rather
than an arbitrary harmonic reparameterization of the exterior field.

This note closes that point on the current exact source classes.

## Exact same-charge bridge theorem

Take the exact exterior projector field `phi_ext` with shell source

`sigma_R = H_0 phi_ext`

and total shell charge

`Q = sum sigma_R`.

Now consider the most general common-harmonic bridge family built from the same
exact exterior harmonic object:

- `psi_c = 1 + c phi_ext`
- `chi_c = 1 - c phi_ext`

Then:

- `H_0(psi_c - 1) = c sigma_R`
- `-H_0(chi_c - 1) = c sigma_R`

So both bridge channels carry shell charge magnitude `cQ`.

That means the bridge is not free to rescale `phi_ext` arbitrarily if it is
supposed to remain the **same-source / same-charge** closure of the exact
lattice exterior field. Exact charge inheritance fixes:

- `c = 1`

Therefore the unique same-charge common-harmonic bridge on the current exact
source classes is:

- `psi = 1 + phi_ext`
- `chi = alpha psi = 1 - phi_ext`

## Exact exterior harmonicity

Because `phi_ext` is harmonic outside the sewing shell, both:

- `psi`
- `chi`

are exact exterior harmonic functions there as well.

So the bridge equations are no longer imported as an external GR target on the
current source classes. They are fixed directly by:

1. the exact lattice exterior field
2. exact charge inheritance
3. the native sign choice of the temporal sector (slower clocks / attractive
   lapse branch)

## Bounded 4D support

There is still a legitimate question:

> perhaps even if the exact same-charge bridge is fixed, the 4D residual might
> prefer different spatial and temporal harmonic coefficients

The script checks the natural two-parameter common-harmonic metric family:

- `psi = 1 + b phi`
- `alpha psi = 1 - a phi`

on the exact coarse exterior laws of both:

1. the exact local `O_h` source family
2. the broader exact finite-rank source family

and finds that off-diagonal mismatch `a != b` increases the exterior 4D vacuum
residual by more than an order of magnitude on both families.

So the remaining bridge freedom is not “pick unrelated temporal and spatial
coefficients.” The common-coefficient structure is numerically preferred, while
the exact same-charge source law then fixes that coefficient to `1`.

## What this closes

This closes the last serious bridge ambiguity on the current exact source
classes:

> the static common-harmonic bridge is no longer an arbitrary imported
> reparameterization; it is the unique same-charge bridge carried by the exact
> lattice exterior field

## What this still does not close

This note still does **not** close:

1. the final pointwise 4D Einstein/Regge lift across the broader finite-rank
   source family
2. fully general nonlinear GR beyond the current exact source classes

## Updated gravity target

After this note, the remaining blocker narrows again:

- the bridge itself is fixed on the current exact source classes
- the remaining work is the final pointwise 4D lift, especially beyond the
  exact local `O_h` family
