# Electrostatics Superposition Proxy Note

**Date:** 2026-04-05  
**Status:** first proposed_retained multi-source electrostatics proxy on the proposed_retained ordered lattice family

## One-line read

This note freezes a narrow electrostatics extension of the retained electric-like
sign law:

- same ordered lattice family
- same sign-coupled propagator
- linear superposition of multiple source charges

The review-safe claim surface is intentionally small:

- exact same-point opposite charges cancel to printed precision
- like-charge pairs reinforce the shift approximately linearly
- a dipole gives a reduced but still signed response
- a doubled source scales the response approximately linearly

## Primary artifact

- Script: [`scripts/electrostatics_superposition_proxy.py`](/Users/jonreilly/Projects/Physics/scripts/electrostatics_superposition_proxy.py)

## What was tested

The probe asks whether the same weak-field propagator can support:

- linear source superposition
- cancellation under opposite charges
- a signed dipole response

The observable is the detector centroid shift relative to the free baseline.

## Frozen replay

On the retained run:

- single `+1`: `delta = -1.6872e-4`
- neutral same-point `+1/-1`: `delta = +0.0000e+0`
- like-pair `+1/+1`: `delta = -3.0115e-4`
- dipole `+1/-1`: `delta = -3.3230e-5`
- double source `+2`: `delta = -3.3744e-4`

The two key controls are:

- same-point opposite charges cancel to printed precision
- doubling the source roughly doubles the response

## Review-safe read

The retained statement is only:

- the propagator is compatible with signed electrostatic superposition on the
  tested family
- opposite charges cancel when combined at the same point
- like-charge pairs reinforce the shift rather than cancelling it
- a dipole gives a nonzero signed response, but smaller than the like-charge
  pair on this geometry

What this does **not** establish:

- Maxwell equations
- full vector electromagnetism
- gauge symmetry
- radiation or magnetic effects

## Why this matters

This is a better EM foothold than a single-source sign law because it checks
linearity and cancellation, not just attraction/repulsion.

If later work wants a stronger experimental hook, this note becomes the narrow
baseline for that upgrade.
