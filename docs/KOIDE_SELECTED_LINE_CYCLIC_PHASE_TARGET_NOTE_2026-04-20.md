# Koide Selected-Line Cyclic Phase Target Theorem

**Date:** 2026-04-20  
**Status:** exact sharpening of the ambient endpoint target on current `main`  
**Runner:** `scripts/frontier_koide_selected_line_cyclic_phase_target_2026_04_20.py`

## Question

The current constructive charged-lepton stack already reduced the live endpoint
burden to one ambient one-clock law for the microscopic selected-line scalar

```text
m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3.
```

Is that best thought of only as a scalar `kappa` bridge, or is there a cleaner
geometric target on the exact cyclic Koide carrier?

## Bottom line

There is a cleaner target.

On the exact selected line, the cyclic response pair already lies on the exact
Koide circle

```text
r1^2 + r2^2 = 2 r0^2.
```

So the remaining endpoint datum is equivalently one **phase**

```text
theta = atan2(r2, r1).
```

The scalar bridge

```text
kappa = sqrt(3) r2 / (2 r0 - r1)
```

is exactly the same information, but written in phase form:

```text
kappa(theta) = sqrt(6) sin(theta) / (2 - sqrt(2) cos(theta)).
```

On the physical first branch:

- the phase starts at the exact threshold value
  `theta_pos = -3 pi / 4`,
- `theta(m)` is strictly monotone,
- so fixing one phase already fixes the unique first-branch selected endpoint.

Therefore the live constructive target can now be read as:

```text
derive one ambient cyclic-response phase law.
```

That is sharper than saying only “derive one scalar law,” and it lines up much
more naturally with the surviving ambient Wilson / transport routes.

## Input stack

This note sharpens:

1. [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)
2. [KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md](./KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md)
3. [KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md)
4. [KOIDE_ONE_CLOCK_ENDPOINT_TARGET_THEOREM_NOTE_2026-04-20.md](./KOIDE_ONE_CLOCK_ENDPOINT_TARGET_THEOREM_NOTE_2026-04-20.md)

## Theorem 1: on the Koide cone, the cyclic response pair is already a circle

Write the exact cyclic/orbit bridge:

```text
r0 = u + v + w,
r1 = 2u - v - w,
r2 = sqrt(3) (v - w).
```

Then a direct algebraic elimination gives

```text
r1^2 + r2^2 - 2 r0^2
  = -3 (u^2 + v^2 + w^2 - 4uv - 4uw - 4vw).
```

So on the exact Koide cone

```text
u^2 + v^2 + w^2 = 4(uv + uw + vw),
```

the cyclic response pair obeys exactly

```text
r1^2 + r2^2 = 2 r0^2.
```

That means the Koide-relevant response data already live on a circle of radius
`sqrt(2) r0` in the `(r1,r2)` plane.

## Corollary 1: one phase reconstructs the response pair

Because of that exact circle law, there exists a unique phase `theta` such that

```text
r1 = sqrt(2) r0 cos(theta),
r2 = sqrt(2) r0 sin(theta).
```

So once `r0` is fixed, the remaining cyclic information is just one phase.

## Theorem 2: the scalar bridge is exactly a phase law

The exact selected-line bridge already proved

```text
kappa = sqrt(3) r2 / (2 r0 - r1).
```

Substituting the circle parameterization gives

```text
kappa(theta) = sqrt(6) sin(theta) / (2 - sqrt(2) cos(theta)).
```

So the previous scalar target `kappa` is not an unrelated extra coordinate. It
is exactly the same endpoint datum written as a phase law on the cyclic circle.

## Theorem 3: the physical first branch has one canonical threshold phase

On the exact selected line, the small branch turns on at

```text
m_pos ~= -1.295794904067
```

with exact scalar value

```text
kappa_pos = -1 / sqrt(3).
```

In the phase language this becomes

```text
theta_pos = -3 pi / 4.
```

So the physical branch begins at one exact circle point: the southwest
forty-five-degree direction on the cyclic response circle.

## Theorem 4: on the first selected-line branch, the phase is strictly monotone

Numerically, on the physical first branch from `m_pos` up to `m = 0`,

```text
theta(m)
```

is strictly increasing.

Therefore any retained target phase in that interval fixes one unique
first-branch selected endpoint. This is exactly the same uniqueness statement
as the previous `kappa(m)` bridge, but in a more geometric form.

## Current candidate route in phase language

The current coordinate-closed route imports one scalar `kappa_*` from the
earlier `H_*` witness and hence fixes one selected-line point

```text
m_* ~= -1.160469470087.
```

On the cyclic circle, that same point carries the phase

```text
theta_* ~= -2.316624963970.
```

The runner verifies directly that

```text
kappa(theta_*) = kappa_*.
```

So the current witness can already be read as one cyclic-response phase target.

## Why this matters

This sharpening changes the feel of the open problem:

- it is still one endpoint law,
- but it is no longer best described only as an abstract scalar selector,
- because the exact cyclic carrier already packages the endpoint as one phase
  on a circle.

That is a much better fit to the surviving constructive ambient routes:

- Wilson descendants already land on the cyclic response carrier,
- transport/continuation laws naturally produce phases,
- and the new bare-resolvent boundary shows the answer is not hiding in the
  smallest local selected-line family.

So the live endpoint burden is best read as:

```text
derive one ambient cyclic-response phase law selecting theta_*.
```

## What this does not yet close

This note does **not** derive the final ambient phase law.

It does not claim:

- a Wilson selector theorem,
- a transport holonomy theorem,
- or a promotion of charged leptons to retained closure.

It only fixes the exact geometric form of the remaining endpoint datum.

## Consequence

The constructive charged-lepton lane is now sharp enough to attack in one of
two honest ways:

1. derive the ambient law that fixes the phase `theta_*`,
2. or prove that a proposed ambient family still cannot fix that phase.

Either way, the target is now cleaner than a generic microscopic scalar.
