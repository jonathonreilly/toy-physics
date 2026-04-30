# Universal GR A1 Invariant Section on `PL S^3 x R`

**Status:** unknown (pending author classification)
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / selector note  
**Purpose:** isolate the strongest exact projector candidate latent in the
current universal stack before attempting full curvature localization

## Verdict

The current universal stack does not yet supply a canonical full
curvature-localization bundle, but it does supply an exact invariant
`A1` section.

That invariant section is the rank-2 projector onto:

- lapse `h_00`
- spatial trace `tr(h_ij)`

In the canonical symmetric `3+1` polarization basis, this is the projector

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

This is the strongest exact projector structure latent in the current direct
universal construction. It is exact, frame-independent, and already visible
in the localization orbit.

## What is exact

The universal stack already gives:

- the exact scalar observable generator `W[J]`;
- the exact `3+1` background `PL S^3 x R`;
- the exact tensor-valued variational candidate
  `S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`;
- the exact unique symmetric `3+1` quotient kernel on the finite prototype.

On top of that, the localization orbit contains an exact invariant section:

- the lapse channel `h_00`;
- the spatial-trace channel `tr(h_ij)`.

These two channels are the exact `A1` block. They do not move under valid
`3+1` polarization-frame rotations.

## What the runner checks

The new audit runner tests the strongest exact projector candidate directly:

1. it samples valid `3+1` polarization frames by spatial rotation;
2. it evaluates the localization coefficients on random symmetric
   perturbations;
3. it checks that the `A1` projection is invariant to machine precision;
4. it checks that the complementary `E \oplus T1` channels still move with
   frame choice.

The exact result is:

- `Pi_A1` is invariant across the sampled valid frames;
- the complement remains frame-dependent;
- no larger canonical projector structure is visible from the current stack.

Representative numbers from the audit runner:

- `max Pi_A1 delta = 1.110e-16`
- `max complement delta = 8.537e-01`
- invariant coordinates = `(0, 4)`

## Strongest exact selector candidate

The strongest exact projector candidate already latent in the current
construction is:

> the rank-2 `A1` projector onto lapse and spatial trace.

This is a minimal-covariance selector. It is the exact invariant section of
the current localization orbit.

## What remains open

The invariant `A1` section is not enough to close full GR.

What is still missing is the complementary covariant structure that would
canonically split the remaining `E \oplus T1` channels into a full
`3+1` polarization-frame / projector bundle with a distinguished connection.

Equivalently, the missing primitive is still the canonical `Pi_curv` on the
full symmetric quotient, not the `A1` projector itself.

## Honest status

The current direct universal route is now:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the symmetric quotient-kernel level;
- exact at the invariant `A1` projector level;
- blocked at the full curvature-localization level.
