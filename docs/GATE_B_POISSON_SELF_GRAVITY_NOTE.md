# Gate B Poisson Self-Gravity Note

**Date:** 2026-04-05  
**Status:** bounded no-go for a minimal Poisson-like self-gravity loop on the
retained grown row

## Artifact chain

- [`scripts/gate_b_poisson_self_gravity_probe.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_poisson_self_gravity_probe.py)

## Question

Can the retained Gate B grown row support a minimal Poisson-like self-gravity
loop, where the propagated amplitude itself sources the next field update,
without breaking the zero-coupling reduction or the weak-field class?

This probe stays narrow:

- retained grown geometry row only: `drift = 0.2`, `restore = 0.7`
- one static source-resolved baseline field scaled by the source strength
- one amplitude-sourced backreaction update between propagations
- exact `eps = 0` reduction check
- one promoted bounded observable: detector centroid shift

## Architecture

This is deliberately not edge surgery.

The loop is:

1. propagate on the fixed retained grown graph using the static baseline field
2. compute a layer-sourced backreaction field from the propagated amplitude
3. propagate again with the updated field

The propagation itself remains linear on each fixed field. The nonlinearity is
only between steps.

## What to look for

The useful signs are:

- exact `eps = 0` reduction back to the frozen grown baseline
- monotone change in detector centroid shift as the backreaction coupling grows
- weak-field exponent near `1` on the smallest retained source strengths

The failure sign is:

- the loop collapses the weak-field law immediately, or the centroid shift does
  not move in a structurally meaningful way

## Frozen Result

The frozen probe uses the retained grown row with one backreaction loop and a
one-seed minimal sweep.

Reduction check:

- `max |psi(eps=0) - baseline| = 0.000e+00`

Frozen readout:

| `eps` | mean escape | mean delta | direction |
| --- | ---: | ---: | --- |
| `0.00` | `1.000` | `+1.666562e-04` | `TOWARD` |
| `0.05` | `0.000` | `+9.188697e-02` | `TOWARD` |
| `0.10` | `0.000` | `+1.628822e-01` | `TOWARD` |
| `0.20` | `0.000` | `+5.838140e-02` | `TOWARD` |
| `0.50` | `0.000` | `+2.926221e-01` | `TOWARD` |

Weak-field law check:

- `eps = 0.00`: `F~M exponent = 1.00`
- `eps = 0.10`: `F~M exponent = -0.60`

## Safe Read

The narrow, honest statement is:

- exact `eps = 0` reduction survives
- the backreaction loop is materially different from the static field
- the detector centroid shift moves and stays TOWARD in this tiny run
- but the weak-field mass law collapses as soon as the backreaction is turned
  on at the tested coupling

That means this is **not** a retained self-gravity bridge.

It is a bounded no-go for the minimal one-loop Poisson-like backreaction idea
on the retained grown row.

## Branch Verdict

Freeze this as a bounded no-go.

The exact reduction is real, but the backreaction loop does not preserve the
weak-field class on the retained sweep. The promoted readout is therefore the
bounded centroid shift, not a self-gravity closure.
