# y_t Interacting Bridge Locality Proxy Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_interacting_bridge_locality.py`

## Role

This note is not the final `y_t` bridge theorem. It is a bounded support scan
that sharpens the remaining target.

The question is narrower:

> If the exact lattice endpoint data are fixed, how diffuse can the remaining
> interacting UV-to-IR bridge be before the accepted low-energy
> `y_t(v) = 0.9176` endpoint is lost?

## Setup

The runner scans a family of smooth bridge profiles that all preserve the same
endpoint data:

- `g_3(v)` fixed by the coupling-map theorem
- `g_3(M_Pl)` fixed by the lattice coupling
- `y_t(M_Pl) = g_3(M_Pl) / sqrt(6)` fixed by the Ward identity

The family interpolates between:

1. an SM-like transport anchored at the accepted low-energy strong coupling,
   and
2. a lattice-side UV bridge profile satisfying the exact UV endpoint

So the scan does not ask whether the endpoints are right. It asks how the
*shape* of the interacting bridge can vary while preserving the accepted
low-energy answer.

## Result

The result is sharp:

- diffuse / early bridge deformations overshoot the accepted `y_t(v)` badly
- a viable smooth profile exists only when the lattice correction is confined
  to a very narrow UV window near `M_Pl`
- in the scanned family, `9 / 70` profiles land within `1%` of the accepted
  central value, and all of them occur only for center fraction `>= 0.95` and
  width fraction `<= 0.03`
- by contrast, all diffuse / early profiles with center fraction `<= 0.85`
  overshoot the accepted endpoint by more than `5%`

That means the accepted low-energy `y_t` endpoint is **not** generic under
arbitrary smooth bridge deformations.

## What this strengthens

This strengthens the live package story in one specific way:

- the remaining bridge does not look like a broad unknown distortion across the
  full `v -> M_Pl` interval
- it looks much closer to an SM-like transport over most of that interval, with
  the lattice correction concentrated near the UV endpoint

So the current backward-Ward route is not being defended as “any arbitrary
interpolation works.” The proxy instead says:

> only a tightly UV-localized correction window preserves the accepted low-
> energy endpoint inside this smooth bridge family.

## What this does **not** prove

This note does not make `y_t` unbounded.

It does **not** yet prove:

- that the exact interacting lattice bridge is uniquely forced into that
  UV-localized window
- that the current `~3%` surrogate bound disappears
- that the bridge theorem is closed

Those still require an operator-level interacting bridge theorem.

## Why it matters anyway

This materially narrows the remaining theorem target.

Before this scan, the residual could still be read as:

- “some unknown smooth UV-to-IR bridge deformation”

After this scan, the residual is sharper:

- “a bridge that must remain SM-like over most of the interval and localize the
  lattice correction near the UV endpoint”

That is a smaller and more testable target.
