# Gravity-vs-Topology Control Note

**Date:** 2026-04-11  
**Status:** exploratory only on one audited SSH surface

**Scripts:**
- `scripts/frontier_topological_phases.py`
- `scripts/frontier_topological_control.py`

## Question

Does the claimed gravity-driven SSH edge-mode transition survive lower
screening or a better matched control surface, or is it reproduced by a
non-self-consistent structured potential?

## Surfaces checked

- low-screening parity-coupled SSH control surface with `mu2 = 0.001`
- matched random disorder at the same field variance
- shuffled self-consistent `Phi`
- new static structured template built from the free half-filled density and
  rescaled to match the self-consistent on-site field scale `std(G*Phi)`

## Main control result

The low-screening parity-coupled SSH lane still shows edge-mode loss:

- free system: 2 edge modes
- self-consistent gravity: edge modes remain through `G = 0.30`
- self-consistent gravity: edge modes vanish at `G = 0.50`
- fine random-disorder threshold is much later, near `sigma ~ 0.36`
- at the gravity transition, the random matched-disorder median still keeps
  `1.0` edge mode

So the effect is not explained by matched random disorder alone.

## Better matched control

The stronger test is the structured static template. On the same low-screening
surface, that control reproduces the self-consistent lane almost exactly once
the on-site field scale is matched:

- `G = 0.10`: gravity `2` modes, static `2`
- `G = 0.20`: gravity `2` modes, static `2`
- `G = 0.30`: gravity `2` modes, static `2`
- `G = 0.50`: gravity `0` modes, static `0`
- `G = 1.00`: gravity `0` modes, static `0`
- `G = 2.00`: gravity `0` modes, static `0`
- `G = 5.00`: gravity `0` modes, static `0`

Bulk gaps also match at the `1e-4` to `1e-3` level across the scan.

This means the current lane is sensitive to a **smooth parity-coupled structured
field**, not specifically to the self-consistent feedback loop.

## Interpretation

What survives:

- lower screening does **not** kill the edge-mode-loss signal
- matched random disorder is too weak a control to explain the transition
- shuffled `Phi` also differs from the self-consistent lane near and above the
  transition

What does **not** survive:

- a gravity-specific or Einstein-like topological claim
- any statement that dynamic backreaction is the load-bearing ingredient

The new structured static control is a better match than random disorder, and it
reproduces the transition. So the honest reading is:

> on this audited open SSH surface, edge-mode loss is triggered by a smooth
> parity-coupled structured field at the same scale as the self-consistent
> field; dynamic self-consistency is not yet isolated as the cause

## Lane state

Keep this lane as **exploratory only**.

It is worth preserving because the edge-mode loss is real on the audited
surface and survives naive disorder controls, but it is **not** ready to be
retained as a gravity-specific topological transition.

## Next work required

- build a structured non-gravitational control family beyond the free-density
  template
- test the same observable on a Wilson or open 2D surface
- isolate whether any residual dynamic effect survives after matching both
  field scale and low-frequency spatial profile
