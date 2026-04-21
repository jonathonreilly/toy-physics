# Koide Brannen-Phase Endpoint Pullback

**Date:** 2026-04-21  
**Status:** exact support reduction on the current constructive endpoint target  
**Runner:** `scripts/frontier_koide_brannen_phase_endpoint_pullback_2026_04_21.py`

## Question

The new orbit bridge proved that the current selected-line cyclic phase target

```text
theta = atan2(r2, r1)
```

is already the Brannen/circulant phase variable up to fixed `C_3` bookkeeping.
Can that be pushed one step further, so that the whole selected-line endpoint
target is written directly as a pullback of the ambient Brannen phase?

## Bottom line

Yes.

Composing the exact orbit bridge with the existing selected-line phase law gives
one direct pullback:

```text
delta
  -> theta = -(delta + 2 pi / 3)
  -> kappa(delta)
  -> r(delta) = w/v
  -> unique first-branch endpoint m(delta).
```

The exact scalar pullback is

```text
kappa(delta)
  = -sqrt(6) cos(delta + pi / 6) / (2 + sqrt(2) sin(delta + pi / 6)).
```

So once the ambient Brannen phase `delta` is fixed, the current exact
selected-line stack already fixes:

- the selected-line phase `theta`,
- the scale-free scalar bridge `kappa`,
- the reachable-slot ratio `r = w/v`,
- and the unique first-branch endpoint `m`.

This does **not** yet prove which ambient law fixes `delta`. It proves that the
selected-line endpoint is no longer an additional independent target once
`delta` is in hand.

## Input stack

This note composes:

1. [KOIDE_SELECTED_LINE_CYCLIC_PHASE_TARGET_NOTE_2026-04-20.md](./KOIDE_SELECTED_LINE_CYCLIC_PHASE_TARGET_NOTE_2026-04-20.md)
2. [KOIDE_SELECTED_LINE_BRANNEN_PHASE_ORBIT_BRIDGE_NOTE_2026-04-21.md](./KOIDE_SELECTED_LINE_BRANNEN_PHASE_ORBIT_BRIDGE_NOTE_2026-04-21.md)
3. [KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md](./KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md)
4. [KOIDE_ONE_CLOCK_ENDPOINT_TARGET_THEOREM_NOTE_2026-04-20.md](./KOIDE_ONE_CLOCK_ENDPOINT_TARGET_THEOREM_NOTE_2026-04-20.md)

## Theorem 1: exact scalar pullback from the Brannen phase

The orbit bridge proved:

```text
theta = -(delta + 2 pi / 3)    (mod 2 pi).
```

The selected-line cyclic-phase theorem proved:

```text
kappa(theta) = sqrt(6) sin(theta) / (2 - sqrt(2) cos(theta)).
```

Composing them gives exactly:

```text
kappa(delta)
  = sqrt(6) sin(-(delta + 2 pi / 3)) / (2 - sqrt(2) cos(-(delta + 2 pi / 3)))
  = -sqrt(6) cos(delta + pi / 6) / (2 + sqrt(2) sin(delta + pi / 6)).
```

So the current selected-line scalar bridge is already an explicit function of
the ambient Brannen phase alone.

## Corollary 1: the reachable-slot ratio is also a direct pullback

The selected-line cyclic-response bridge proved

```text
r = w/v = (1-kappa)/(1+kappa).
```

Therefore:

```text
r(delta) = (1-kappa(delta)) / (1+kappa(delta)).
```

So once `delta` is fixed, the selected-line ratio target is fixed immediately.

## Theorem 2: on the physical branch, `delta` fixes a unique selected-line endpoint

The selected-line stack already proved that on the physical first branch:

- `theta(m)` is strictly monotone,
- equivalently `kappa(m)` is strictly monotone,
- and any target `kappa` in the physical interval fixes one unique first-branch
  point `m`.

Combining this with Theorem 1:

```text
delta -> kappa(delta) -> unique first-branch m(delta).
```

So the endpoint target is not an extra free theorem burden once the ambient
phase is known.

## Numerical check at the current charged-lepton target

At the support-route value

```text
delta = 2/9,
```

the pullback gives:

```text
theta(2/9) ~= -2.316617324615,
kappa(2/9) ~= -0.607918569997,
r(2/9)     ~=  4.100981191542,
m(2/9)     ~= -1.160443440065.
```

The runner checks that these land directly on the same first-branch selected
endpoint window as the current constructive witness:

```text
theta_* ~= -2.316624963970,
kappa_* ~= -0.607905698005,
m_*     ~= -1.160469470087.
```

So the exact pullback is not merely formal. It lands numerically on the same
physical branch already isolated by the current one-clock stack.

## What this changes

This note does **not** close the ambient Brannen-phase bridge by itself.

It sharpens the open target:

- before: ambient phase law plus a potentially separate selected-line endpoint law,
- now: one ambient law selecting the physical Brannen phase is enough, because
  the endpoint is already its exact pullback.

So the remaining scientific question is narrower:

```text
what fixes the physical Brannen phase delta?
```

not

```text
what fixes delta, and then separately what fixes the selected-line endpoint?
```

## Scope boundary

This note does **not** claim:

- that the APS support route is already the physical Brannen phase,
- that `delta = 2/9` is retained closed on the current surface,
- or that the charged-lepton Koide lane is fully promoted on current `main`.

It only proves that once the physical Brannen phase is fixed, the selected-line
endpoint data follow automatically through the current exact stack.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_brannen_phase_endpoint_pullback_2026_04_21.py
```
