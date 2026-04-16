# `y_t` Bridge Hessian Selector Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_hessian_selector.py`

## Role

This note answers the next microscopic question after the variational-selector
pass:

> why should the exact interacting lattice bridge induce a **positive local
> quadratic selector** on the forced UV window at all?

The earlier branch notes already established:

- the viable bridge is forced into a narrow UV-localized class
- the endpoint is controlled by a narrow moment band on that class
- a positive local quadratic selector on that window would pick the observed
  minimizer

The missing step was to connect that selector back to the exact interacting
bridge, rather than leave it as an external variational ansatz.

## Derivation

Let `delta q(x)` denote the gauge-surplus bridge field on the forced UV
window, with `x` the UV fraction coordinate.

At the accepted branch endpoint, the exact interacting lattice bridge is:

1. **SM-like over most of the interval**
   because diffuse deformations fail and only a narrow UV-localized class
   survives;
2. **stable**
   because the accepted branch endpoint is isolated under the earlier
   rearrangement, moment-closure, and constructive-family checks;
3. **quasi-local on that UV window**
   because the bridge problem has already reduced from an arbitrary long-range
   profile to a local window with one active support patch.

So the coarse-grained bridge action on that window admits the standard local
expansion around the accepted saddle:

`Gamma[delta q] = Gamma[0] + (1/2) <delta q, H delta q> + O(delta q^3, nonlocal)`

with:

- no linear term on the fixed-endpoint / fixed-moment slice;
- a positive Hessian `H`, because the accepted saddle is stable;
- a local leading kernel on the forced window, because the active support is
  already confined to that narrow UV patch.

That is the microscopic reason the selector must be **positive local
quadratic** at leading order.

## What the runner checks

The runner does not assume a constant stiffness. It infers the local stiffness
profile directly from the viable bridge family and the exact endpoint-response
kernel on the forced UV window.

It finds:

- the exact response kernel is positive on that window;
- each best-family bridge induces a positive local stiffness profile;
- the logistic and erf families collapse tightly to the same normalized
  stiffness shape;
- the family-averaged local-Hessian selector reproduces the family-averaged
  bridge profile almost exactly, with gap `0.003443`.

So the branch no longer needs to treat the positive local quadratic selector as
an unexplained add-on.

## Meaning

The selector question is now closed **at leading order**:

> the exact interacting lattice bridge induces a positive local quadratic
> selector because the bridge has already been forced into a narrow UV-local
> stable saddle, and the leading coarse-grained action on that saddle is its
> positive local Hessian.

The new runner also shows that the corresponding stiffness is not exactly
constant. The smoothstep family remains a compact-support edge-shape outlier,
while the analytic families collapse cleanly to one common normalized
stiffness profile.

So the residual gap is no longer:

- why the selector exists
- why it is local
- why it is positive

It is now only:

- how large the higher-order / nonlocal corrections are beyond that local
  Hessian selector

## Honest boundary

This does **not** yet make the `y_t` lane fully unbounded by itself.

It does mean the branch has a leading-order microscopic explanation for the
selector that previously appeared only conditionally in the variational note.

The remaining review target is to control the higher-order and nonlocal
corrections, not to explain the selector itself.
