# Koide Brannen-Phase Conjugation-Symmetry Boundary Theorem

**Date:** 2026-04-21  
**Status:** exact boundary theorem on the current one-clock ambient class  
**Runner:** `scripts/frontier_koide_brannen_phase_conjugation_symmetry_boundary_2026_04_21.py`

## Question

After the endpoint-target theorem, the cyclic-phase target theorem, the
selected-line / Brannen orbit bridge, and the endpoint pullback note, the live
charged-lepton question has become very sharp:

> what retained ambient one-clock law can actually fix the physical Brannen
> phase?

Before trying more candidate laws, there is one structural question to settle:

> can the **current exact positive conjugation-symmetric ambient Wilson class**
> already do this by itself?

## Bottom line

No.

On the exact Koide cyclic carrier

```text
B0 = I,
B1 = C + C^2,
B2 = i(C - C^2),
```

entrywise complex conjugation fixes `B0` and `B1` but flips `B2`:

```text
K(B0) = B0,
K(B1) = B1,
K(B2) = -B2.
```

Therefore any charged Hermitian source law descending only through the current
conjugation-symmetric ambient class has zero `B2` response:

```text
r2 = dW(B2) = 0.
```

But the exact selected-line / Brannen bridge already proved that the physical
charged-lepton target carries a genuinely nonzero phase channel:

```text
theta = atan2(r2, r1) ~= -2.316624963970,
delta ~= 2/9,
r2 != 0.
```

So the missing ambient Brannen-phase law is now narrower than before:

> it cannot live inside the current conjugation-even positive one-clock Wilson
> class alone; it must refine that class by an orientation-sensitive /
> conjugation-odd datum.

This is a real reduction, not just another failure note.

## Input stack

This note combines:

1. [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md)
2. [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)
3. [KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md](./KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md)
4. [KOIDE_SELECTED_LINE_BRANNEN_PHASE_ORBIT_BRIDGE_NOTE_2026-04-21.md](./KOIDE_SELECTED_LINE_BRANNEN_PHASE_ORBIT_BRIDGE_NOTE_2026-04-21.md)
5. [KOIDE_BRANNEN_PHASE_ENDPOINT_PULLBACK_NOTE_2026-04-21.md](./KOIDE_BRANNEN_PHASE_ENDPOINT_PULLBACK_NOTE_2026-04-21.md)
6. [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_ORIENTATION_THEOREM_NOTE_2026-04-20.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_ORIENTATION_THEOREM_NOTE_2026-04-20.md)

The gauge-side relevance is simple: the current exact ambient Wilson class on
`main` is positive, self-adjoint, and conjugation-symmetric on the class side.
The present theorem asks what that symmetry means after the exact Koide cyclic
compression.

## Theorem 1: conjugation fixes the even cyclic channels and flips the phase channel

Let `K(X) = X̄` be entrywise complex conjugation on `Herm(3)`.

On the cyclic basis:

```text
B0 = I,
B1 = C + C^2,
B2 = i(C - C^2),
```

one has exactly

```text
K(B0) = B0,
K(B1) = B1,
K(B2) = -B2.
```

So the cyclic carrier splits into:

- an even subspace `span_R{B0, B1}`,
- and one odd phase direction `span_R{B2}`.

This is the exact location of the Brannen phase channel on the Koide carrier.

## Theorem 2: conjugation-even charged Hermitian data have zero phase response

Write a generic conjugation-even Hermitian target as

```text
H_even
 = d1 D1 + d2 D2 + d3 D3
 + x12 X12 + x23 X23 + x13 X13,
```

with no antisymmetric `Yij` part.

Then its exact cyclic compression is

```text
P_cyc(H_even)
  = ((d1+d2+d3)/3) B0
  + ((x12+x23+x13)/3) B1,
```

with **no** `B2` component.

Equivalently, the Koide cyclic response formulas become

```text
r0 = d1 + d2 + d3,
r1 = 2 (x12 + x23 + x13),
r2 = 0.
```

So any charged-lepton descendant living entirely inside the conjugation-even
ambient class has zero cyclic phase channel.

## Corollary 1: the current conjugation-even ambient class cannot select a nonzero Brannen phase

On the exact selected-line cyclic circle,

```text
theta = atan2(r2, r1).
```

If `r2 = 0` and the point is nondegenerate, then

```text
theta in {0, pi}.
```

Using the exact orbit relation

```text
theta = -(delta + 2 pi / 3) mod 2 pi,
```

the corresponding Brannen phases are only the discrete conjugation-even values

```text
delta in {pi/3, 4 pi/3}  mod 2 pi.
```

So the current even class cannot reach the physical interior phase near
`delta = 2/9`.

## Theorem 3: the physical charged-lepton target is genuinely outside the conjugation-even class

The current exact selected-line witness carries:

```text
theta_* ~= -2.316624963970,
delta_* ~= 2/9,
r2_* != 0.
```

Therefore the physical Brannen-phase target is not a hidden point inside the
current conjugation-even ambient class. The obstruction is structural, not
numerical.

## Consequence

This refines the live endpoint target again.

Before this note, the remaining burden was:

```text
derive one ambient law selecting the physical Brannen phase.
```

After this note, the remaining burden is sharper:

```text
derive one ambient orientation-sensitive / conjugation-odd law selecting
the physical Brannen phase.
```

So the search should stop spending time on purely conjugation-even positive
refinements of the current ambient class. Those can only move the even cyclic
channels.

## Positive continuation

The repo already has the right ambient category for this refinement:

- the current exact gauge line work reduces multiplicity to a `rho1/rho2`
  orientation question rather than arbitrary frame freedom;
- the Brannen-phase target now asks for the Koide-side version of that extra
  orientation-sensitive datum.

This note does **not** prove that the existing `rho1/rho2` orientation doublet
already closes the charged-lepton phase. It proves something narrower and
useful:

> if the Brannen bridge closes natively, it must do so through an
> orientation-sensitive refinement, not through the current conjugation-even
> positive one-clock Wilson class alone.

## What this closes

- exact identification of the Brannen phase channel as the conjugation-odd
  cyclic direction `B2`
- exact no-go for all purely conjugation-even cyclic descendants on the current
  one-clock ambient class
- exact explanation of why the present positive Wilson machinery has not yet
  selected the physical Brannen phase

## What this does not close

- the actual orientation-sensitive ambient law selecting `delta = 2/9`
- the explicit pullback `delta_physical = eta_APS`
- the final retained charged-lepton Brannen bridge

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_brannen_phase_conjugation_symmetry_boundary_2026_04_21.py
```
