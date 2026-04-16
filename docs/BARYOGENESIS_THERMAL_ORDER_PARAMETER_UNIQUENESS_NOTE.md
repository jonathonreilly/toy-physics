# Baryogenesis Thermal Order-Parameter Uniqueness Note

**Date:** 2026-04-16
**Status:** bounded current-surface thermal-order-parameter theorem on `main`
**Script:** `scripts/frontier_baryogenesis_thermal_order_parameter_uniqueness.py`

## Safe statement

Yes, the APBC / bosonic-bilinear selector stack does derive a genuinely
finite-`T` order-parameter surface on the current framework package.

But it is a **unique** thermal order-parameter surface, not a hidden extra
scalar family.

That is the important baryogenesis consequence.

## What is derived here

The hierarchy observable-principle stack already fixes:

1. the additive CPT-even scalar generator as the local source response of

   `W[J] = log|det(D+J)| - log|det D|`

2. the local bosonic curvature kernel as the thermal scalar observable surface
3. the exact Klein-four orbit closure of that kernel on the APBC temporal
   circle
4. the unique minimal resolved orbit

   `L_t = 4`

5. the exact endpoint band

   - `A_2 = 1/8`
   - `A_4 = 1/7`
   - `A_inf = 1/(4 sqrt(3))`

So the APBC stack does more than route history. It really does derive a
finite-`T` order-parameter surface.

## Why this is not a new scalar sector

The same derivation also shows what that surface is:

- one additive scalar generator
- one bosonic-bilinear curvature kernel
- one unique minimal resolved thermal orbit at `L_t = 4`

That means the APBC stack refines the normalization of the **same** Higgs
order-parameter surface. It does not by itself derive:

- a second Higgs doublet
- a second independent thermal scalar family
- a hidden multiplicity enhancement of the old taste-scalar route

On the current authority surface, the Higgs lane still derives exactly one
doublet from the `G_5` condensate.

## Exact consequence for baryogenesis

This closes the obvious rescue attempt:

> “maybe the APBC / bosonic-bilinear selector stack secretly generates the
> extra finite-`T` scalar structure the old baryogenesis route needs.”

Answer:

- no
- it gives one unique thermal order-parameter surface
- it does not derive a second same-surface scalar family

That does **not** make baryogenesis impossible. It does mean this particular
APBC rescue route is not available on current `main`.

## Bounded quantitative consequence

The exact APBC endpoint band is only an `O(10%)` normalization effect:

- `A_4/A_2 = 8/7 = 1.142857...`
- `A_inf/A_2 = 2/sqrt(3) = 1.154700...`

By contrast, the current matched one-doublet scalar-side baryogenesis gap on
the old imported one-loop scalar-cubic ansatz is still about:

- `2.41x` on the 2-loop Higgs support route
- `2.39x` on the full 3-loop Higgs route

This is a bounded consequence, not a direct theorem of scalar cubic strength.
But it strongly reinforces the structural conclusion:

- the APBC stack is a normalization/selection surface
- not an extra-sector generator

## What this closes

This note closes the question:

> “Does the APBC / bosonic-bilinear selector stack provide a new finite-`T`
> order-parameter surface for baryogenesis?”

Answer:

- yes, it provides a real finite-`T` order-parameter surface
- but that surface is unique and stays on the same Higgs order-parameter lane
- it does not reopen the old taste-scalar EWPT route

## What remains open

This note does **not** close baryogenesis.

The remaining open question is now narrower:

- is there any genuinely new derived finite-`T` bosonic sector beyond this
  unique thermal order-parameter surface?
- or must baryogenesis closure come from a different nonperturbative
  EWPT/transport route altogether?

## Relation to the existing baryogenesis notes

- [BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md](./BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md)
  killed the old 2HDM-like route on the current authority surface
- this note kills the remaining APBC rescue hatch for that route

Together they say:

- the current package has a real finite-`T` thermal order-parameter surface
- but it is not the extra scalar structure the old route would need

## Validation

- [frontier_baryogenesis_thermal_order_parameter_uniqueness.py](./../scripts/frontier_baryogenesis_thermal_order_parameter_uniqueness.py)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md](./HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
- [BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md](./BARYOGENESIS_OLD_ROUTE_SURFACE_NO_GO_NOTE.md)

Current runner state:

- `frontier_baryogenesis_thermal_order_parameter_uniqueness.py`: expected
  `PASS>0`, `FAIL=0`
