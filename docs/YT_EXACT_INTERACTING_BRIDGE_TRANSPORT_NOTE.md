# Exact Interacting Bridge Transport Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_exact_interacting_bridge_transport.py`

## Role

This note packages the strongest honest transport statement currently supported
by the branch.

It is not another profile scan. It is the branch-native UV-to-IR transport law
that remains after the selector, moment, rearrangement, higher-order, and
nonlocal audits.

The current stack already established:

1. broad / diffuse bridges fail
2. the viable bridge is forced into a narrow UV-localized class
3. the UV-localized class collapses to a dominant action invariant `I_2`
4. the forced UV window reduces to a two-moment closure `(I_2, c_2)`
5. the local selector is positive and quadratic at leading order
6. the first higher-order and nonlocal corrections above that selector are
   small on the viable branch families

This note turns those facts into a transport equation with an explicit
remainder budget.

## Transport law

Let `x` denote the UV fraction coordinate, with `x = 1` at the UV boundary and
`x = 0` at the physical IR endpoint `v`.

Let the bridge surplus be

`delta q(x) = g_3^2(x) - g_{3,SM}^2(x)`

on the forced UV window `x in [x_uv, 1]`, where the package-native support cut
is `x_uv = 0.95`.

Then the exact-interacting-bridge transport law supported by this branch is:

`delta y_t(v) = T_loc[delta q] + Delta_higher[delta q] + Delta_nonlocal[delta q]`

with the leading transport operator

`T_loc[delta q] = integral_{x_uv}^1 K_loc(x) delta q(x) dx`

and

`K_loc(x) = a x + b`

the affine local-Hessian kernel inferred from the accepted branch bridge.

Equivalently, on the forced UV window the branch can write:

`K_exact(x) = K_loc(x) + R_higher(x) + R_nonlocal(x)`

so that

`delta y_t(v) = integral_{x_uv}^1 K_exact(x) delta q(x) dx`

with the explicit remainder split above.

## Moment form

Because `K_loc(x)` is nearly affine on the forced UV window, the leading
transport law can also be written in moment form:

`delta y_t(v) = J_aff + epsilon`

where

`J_aff = I_2 (a c_2 + b)`

and the remainder `epsilon` is controlled by the current higher-order and
nonlocal audits.

This is the tightest package-native formulation currently supported.

## Explicit assumptions

This transport statement assumes:

1. the bridge is evaluated on the forced UV-localized window identified by the
   current locality and rearrangement audits
2. the current accepted bridge is the stable saddle around which the coarse
   grained action admits a local Hessian expansion
3. the bridge response is represented by the current endpoint kernel on that
   window, with the affine local piece plus explicit higher-order and
   nonlocal corrections
4. the bridge surplus is positive on the viable class, so the rearrangement
   ordering remains valid

These are the same assumptions already used implicitly by the selector and
correction notes; this note just writes them as one transport law.

## Validation checks

The runner validates four separate pieces:

1. the exact endpoint-response kernel stays positive on the forced UV window
2. the kernel is well approximated by an affine local-Hessian model there
3. the higher-order local corrections remain subleading on a 10 percent
   amplitude tube around the selector
4. the nonlocal tail remains small both in operator norm and in action against
   the viable branch profiles

The branch-level explicit budgets currently supported are:

- higher-order local ratio: about `7.1e-3` on the probe tube
- nonlocal operator ratio: about `5.0e-3` on the forced UV window
- conservative combined remainder budget: about `1.3e-2`

That is the best honest package-native transport budget available on this
branch.

## Honest boundary

This note does **not** claim full unbounded closure for `y_t`.

What it does claim is the strongest conditional transport statement currently
supported:

> on the forced UV window, the exact interacting bridge is well described by a
> positive local affine transport kernel plus a small explicit higher-order
> and nonlocal remainder.

If a future theorem shows that the remainder vanishes or is absorbed into a
fully enumerated package-native systematic, then the same transport law will
promote from bounded support to unbounded closure.

Until then, the bridge is conditional but sharply controlled.
