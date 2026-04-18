# Koide Selected-Line Cyclic-Response Bridge

**Date:** 2026-04-18  
**Status:** exact reduction of the remaining charged-lepton promotion gap to
one scalar cyclic-response law  
**Runner:** `scripts/frontier_koide_selected_line_cyclic_response_bridge.py`

## Question

After the current positive Koide route was reduced to the selected line
```text
G_m = H(m, sqrt(6)/3, sqrt(6)/3)
```
and then coordinate-closed by threshold continuity plus the imported `H_*`
witness ratio, what exactly is the smallest remaining charged-lepton gap?

## Bottom line

It is only one scalar.

The exact missing charged-lepton bridge can be written as the scale-free
cyclic-response ratio
```text
kappa := sqrt(3) r2 / (2 r0 - r1),
```
equivalently
```text
kappa = (v-w) / (v+w),
```
where `(r0, r1, r2)` are the cyclic Koide responses and `(u, v, w)` are the
physical orbit-slot amplitudes on the small branch.

Once `kappa_*` is fixed by a retained charged-lepton law, everything else on
the current Koide route is already fixed:

1. `w/v = (1-kappa_*) / (1+kappa_*)`;
2. the small-branch direction is fixed;
3. on the selected line, the first-branch point `m_*` is fixed uniquely by the
   monotone bridge `kappa(m)`;
4. threshold continuity fixes the physical branch.

So the charged-lepton Koide route is now **one scalar retained law away** from
promotion.

## Input stack

This bridge sharpens:

1. [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)
2. [KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md)
3. [KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md)
4. [KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md)

## Theorem 1: exact cyclic/orbit inversion

The fresh `Gamma`-orbit reduction gives
```text
r0 = u + v + w,
r1 = 2u - v - w,
r2 = sqrt(3) (v - w).
```

This inverts exactly to
```text
u = (r0 + r1) / 3,
v = r0/3 - r1/6 + sqrt(3) r2/6,
w = r0/3 - r1/6 - sqrt(3) r2/6.
```

So the cyclic responses and the physical orbit slots are exactly equivalent
coordinates.

## Corollary 1: the remaining bridge is one scalar cyclic ratio

Define
```text
kappa := sqrt(3) r2 / (2 r0 - r1).
```

Using the inversion formulas above,
```text
2 r0 - r1 = 3 (v+w),
sqrt(3) r2 = 3 (v-w),
```
so
```text
kappa = (v-w) / (v+w).
```

Therefore
```text
w/v = (1-kappa) / (1+kappa).
```

So fixing one scalar `kappa` is exactly the same thing as fixing the
reachable-slot ratio `w/v`.

## Corollary 2: on the small branch, fixing `kappa` fixes the full direction

On the small Koide branch,
```text
u = 2(v+w) - sqrt(3(v^2 + 4vw + w^2)).
```

That means the normalized amplitude direction depends only on `w/v`, hence only
on `kappa`.

So once `kappa_*` is known, the full charged-lepton amplitude direction is
known on the current route.

## Theorem 2: exact threshold value on the selected line

On the selected line `G_m`, the small branch turns on at the exact threshold
```text
m_pos ~= -1.2957949
```
where
```text
u_- = 0.
```

At that threshold the exact cone gives
```text
v^2 + w^2 = 4vw,
```
so with `w > v`,
```text
w/v = 2 + sqrt(3),
kappa_pos = -1 / sqrt(3).
```

So the scalar bridge starts at one exact algebraic endpoint.

## Theorem 3: on the first selected-line branch, `kappa(m)` is monotone

Numerically, on the first branch from `m_pos` up to the turnover window,
```text
kappa(m)
```
is strictly monotone.

Therefore any target value
```text
kappa_* in [kappa(0), kappa_pos]
```
fixes a unique first-branch point `m_*`.

That is the exact statement needed for promotion:

> a retained charged-lepton law fixing `kappa_*` would already fix the
> selected-line point.

## Current candidate route in this language

The current coordinate-closed candidate route imports one scalar from the
earlier `H_*` witness:
```text
kappa_* ~= -0.607905698005.
```

Solving
```text
kappa(m) = kappa_*
```
on the first branch gives
```text
m_* ~= -1.16046947.
```

That reproduces the same selected-line Koide witness as the current closure
note.

So the imported datum is not “a whole matrix witness” anymore. It is exactly
one scalar.

## Why this matters

This is the sharpest honest charged-lepton status now visible in the repo:

- the route is no longer blocked by a generic parent/readout problem;
- it is no longer blocked by a generic three-response law;
- it is not even blocked by a free one-real line;
- it is blocked only by one scale-free charged-lepton scalar law for
  `kappa_*`.

That is the smallest concrete retained target currently on the charged-lepton
Koide lane.

## What remains open

The remaining charged-lepton promotion target is now:

```text
derive kappa_* from a retained charged-lepton law.
```

Equivalent formulations are:

- derive `w/v` on the selected line;
- derive the cyclic ratio `sqrt(3) r2 / (2 r0 - r1)`;
- derive one scale-free charged-lepton response ratio on the cyclic Koide
  carrier.
- derive the selected-slice microscopic scalar
  `m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3`;
- derive the compressed `dW_e^H` ratio
  `sqrt(3) (y12 + y23 - y13) / (d_sum - x_sum)`.

Everything downstream of that scalar is already fixed by the current exact
stack.

The companion
[KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md)
sharpens this further: on the exact selected slice `delta = q_+ = sqrt(6)/3`,
the remaining microscopic datum is already just one `Z_3` doublet-block scalar,
and `kappa` is a monotone function of that scalar on the physical first branch.

## Consequence

The charged-lepton Koide route is not fully retained yet.

But it is now only **one scalar retained bridge law away**.

That is substantially sharper than “find a parent,” “find a readout,” or
“derive the whole cyclic response law.”

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_selected_line_cyclic_response_bridge.py
```
