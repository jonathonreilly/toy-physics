# Koide `Gamma`-Orbit Cyclic Return Candidate

**Date:** 2026-04-18
**Status:** exact axis-1 reduction on the charged-lepton Koide lane; the old
cross-axis candidate step is now closed by the companion full-cube orbit-law
note
**Runner:** `scripts/frontier_koide_gamma_orbit_cyclic_return_candidate.py`

## Question

If we stay positive and close to the physical `3+1` lattice picture, what is
the cleanest `Gamma`/orbit-return route from the exact retained second-order
return structure to the Koide cyclic basis?

The target here is not yet a full mass derivation. It is narrower and more
constructive:

> prove exactly how a local `Gamma`-return law descends to the Koide cyclic
> carrier, and isolate the one genuinely new microscopic ingredient still
> needed.

## Bottom line

There is now a clean fresh candidate route.

The exact retained `Gamma_1` second-order return already gives a `3`-slot
species-orbit object:
```text
R_{Gamma_1}(W_1) = diag(u, v, w)
```
for a general reachable-state weight operator
```text
W_1 = u P_{O_0} + v P_{(1,1,0)} + w P_{(1,0,1)} + z P_{(0,1,1)}.
```

That diagonal triple lives on the exact charged-species `C_3` orbit. Under the
species Fourier transport it becomes the unique Hermitian circulant
```text
H_Gamma = F diag(u, v, w) F^dagger
        = (r0/3) B0 + (r1/6) B1 + (r2/6) B2,
```
with
```text
B0 = I,
B1 = C + C^2,
B2 = i(C - C^2),

r0 = u + v + w,
r1 = 2u - v - w,
r2 = sqrt(3) (v - w).
```

So the basis engineering step is closed exactly. A positive local
`Gamma`-return law does **not** need to hit a generic Hermitian `3 x 3`
operator. It already lands on the Koide cyclic carrier.

The old fresh candidate at this stage was “axis-oriented orbit-slot
universality.” That step is now replaced by the exact full-cube transport law
in
[KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md](./KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md):
one local axis-1 template, transported by the exact `C_3[111]` cycle on the
full cube, produces the full cyclic family
```text
D1 = diag(u, v, w),
D2 = diag(w, u, v),
D3 = diag(v, w, u).
```
So that cross-axis basis step is no longer open.

## Exact retained input

This route uses only already-live exact structure:

- the retained `hw=1` charged triplet with induced species cycle `C`;
- the exact `Gamma_i` family on the physical `3+1` Clifford carrier;
- the exact second-order-return shape theorem on `T_1`;
- the exact `C_3` Fourier/character decomposition on the charged triplet.

So this note does not depend on any particular negative evaluation result. If a
better future microscopic evaluation changes the numeric story, the algebraic
compression proved here still stands.

## 1. Exact `Gamma_1` return already gives a three-slot orbit object

On the retained carrier, define
```text
R_{Gamma_1}(W)
 = P_{T_1} Gamma_1 W Gamma_1 P_{T_1}
```
and restrict to the charged species basis.

For the general reachable-state weight operator
```text
W_1 = u P_{O_0} + v P_{(1,1,0)} + w P_{(1,0,1)} + z P_{(0,1,1)},
```
the exact shape theorem gives
```text
R_{Gamma_1}(W_1) = diag(u, v, w).
```

So one local `Gamma_1` return already produces exactly three real microscopic
channels. The fourth `T_2` slot is invisible at this order.

That is already the right size for Koide.

## 2. Historical candidate: axis-oriented orbit-slot universality

Here is the one fresh first-principles candidate input:

> For each selected spatial axis `i`, the three reachable second-order return
> slots of `Gamma_i` are assigned the same ordered abstract triple `(u, v, w)`,
> with the order read relative to the species `C_3` orbit.

This is the only non-derived step in the note.

Under that candidate assignment, the exact `Gamma_i` returns become
```text
D1 = diag(u, v, w),
D2 = diag(w, u, v),
D3 = diag(v, w, u),
```
which satisfy
```text
D2 = C D1 C^dagger,
D3 = C^2 D1 (C^dagger)^2.
```

So the full `Gamma` orbit is not a large unconstrained family. It is exactly
one real triple together with the canonical species-cycle action.

## 3. Exact Fourier transport to the Koide cyclic basis

Let
```text
F = (1/sqrt(3))
    [[1, 1, 1],
     [1, omega, omega^2],
     [1, omega^2, omega]]
```
be the species Fourier matrix, where `omega = exp(2 pi i / 3)`.

Transport the diagonal `Gamma` return to the cyclic basis:
```text
H_Gamma = F D1 F^dagger.
```

The runner proves exactly that
```text
H_Gamma
 = (r0/3) B0 + (r1/6) B1 + (r2/6) B2
```
with
```text
r0 = u + v + w,
r1 = 2u - v - w,
r2 = sqrt(3) (v - w).
```

Equivalently, in real orbit moments,
```text
m0 = (u + v + w)/3,
mc = (2u - v - w)/3,
ms = (v - w)/sqrt(3),
```
so
```text
H_Gamma = m0 B0 + (mc/2) B1 + (ms/2) B2.
```

This is the exact reduction we needed:

- local `Gamma` return slots `(u, v, w)`
- become exact orbit moments `(m0, mc, ms)`
- which are exactly the Koide cyclic coordinates.

## 4. What this buys immediately

This means the positive path no longer needs to hunt for a generic matrix law.

If a physical local `Gamma`/orbit-return law exists, then:

1. it already has the right native three-channel size;
2. it already descends canonically to `B0`, `B1`, `B2`;
3. it already packages the charged-lepton question into the cyclic responses
   `(r0, r1, r2)`.

So even if the current conventional evaluation framework is missing some live
microscopic effect, this exact compression result survives. What can change is
the microscopic triple `(u, v, w)`, not the correct carrier it must feed.

## 5. Observed charged-lepton witness

If we set
```text
(u, v, w) = (sqrt(m_e), sqrt(m_mu), sqrt(m_tau)),
```
then the transported operator `H_Gamma` is exactly the observed charged-lepton
circulant amplitude operator. Its cyclic responses satisfy the Koide selector
to PDG precision:
```text
2 r0^2 = r1^2 + r2^2
```
up to the known tiny observational residual.

So the `Gamma`/orbit-return route is not only structurally correct. It already
hits the observed target family.

## What remains open

This note does **not** yet derive:

- the microscopic positive lattice rule fixing `(u, v, w)`;
- the selector law that forces
  ```text
  2 r0^2 = r1^2 + r2^2.
  ```

But it does shrink the live problem sharply.

The remaining positive task is no longer “find some matrix mechanism.”
It is:

> derive one local `Gamma`-orbit **value law** for the real triple `(u, v, w)`,
> then derive one scalar selector relation on its cyclic moments.

The companion
`KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md`
now makes that second step completely explicit: the cyclic Koide selector pulls
back to the symmetric orbit-slot cone
`u^2 + v^2 + w^2 = 4 (uv + uw + vw)`.
(Reference is backticked rather than markdown-linked because that note
CONSUMES this cyclic-return content; citation graph direction is
*selector_bridge → cyclic_return*. A markdown link would create a
length-2 cycle.)

## Bottom line

The clean fresh `Gamma`/orbit-return route now looks like this:

```text
exact local Gamma return slots  ->  exact species-orbit triple (u, v, w)
                                ->  exact C_3 Fourier transport
                                ->  exact Koide cyclic basis (B0, B1, B2)
                                ->  one remaining selector equation
```

That is a genuinely positive next step. The basis step is done exactly; only
the microscopic orbit law and its selector remain open.
