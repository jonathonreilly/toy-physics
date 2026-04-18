# Gauge-Vacuum Plaquette Beta=6 Identity-Rim Finite-Moment Packet Reduction

**Date:** 2026-04-18  
**Status:** exact fixed-depth plaquette bulk reduction from the finite Jacobi
packet to an equivalent finite cyclic-moment packet, plus sharper noncollapse
that the propagated retained triple still does **not** determine even the first
nontrivial moment pair on the current bank  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_beta6_identity_rim_finite_moment_packet_reduction_2026_04_18.py`

## Question

After the finite-Jacobi reduction, is the sharp fixed-depth plaquette bulk
datum still most honestly stated as a Jacobi packet?

Or can it be reduced one scalar step further to a finite cyclic-moment packet?

And if so, does the propagated retained triple at least determine the first
nontrivial moment layer?

## Answer

Yes, it reduces one step further.

At fixed propagation depth `d = L_perp - 1`, the sharp bulk datum is
equivalently:

- the finite Jacobi packet of the `eta_6(e)`-generated Krylov compression,
- or the corresponding finite cyclic-moment packet
  `m_n = <eta, S^n eta>` up to the same finite depth.

By the cyclic-bulk reduction, the identity-rim cyclic object is already
determined by its moment sequence. By the finite-Jacobi reduction, the fixed-
depth bulk front is already reduced to one finite Jacobi packet. Therefore the
fixed-depth bulk front is equally one finite moment packet.

Sharper still, the current propagated retained triple does **not** determine
even the first nontrivial moment pair `(m_1, m_2)`. The same explicit witness
pair with a common identity rim state and the same propagated retained triple
already has:

`m_1^P != m_1^Q`,

`m_2^P != m_2^Q`.

So the propagated retained triple still fails already at the first scalar bulk
layer.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_CYCLIC_BULK_REDUCTION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_CYCLIC_BULK_REDUCTION_NOTE_2026-04-17.md):

- the identity-rim cyclic bulk object is equivalently determined by its moment
  sequence.

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_JACOBI_PACKET_REDUCTION_NOTE_2026-04-18.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_JACOBI_PACKET_REDUCTION_NOTE_2026-04-18.md):

- the sharp fixed-depth bulk datum is one finite Jacobi packet,
- and the propagated retained triple still does not determine even its first
  nontrivial Jacobi packet.

The new point is the scalar reformulation:

- at fixed depth, that same bulk datum is equivalently one finite cyclic-moment
  packet,
- and the current bank already fails even at the first nontrivial moment pair.

## Theorem 1: exact finite-moment reduction of the fixed-depth plaquette bulk front

Let `eta` be the normalized identity rim state and let `J_d` be the finite
Jacobi matrix of the `eta`-generated Krylov compression.

Then the finite cyclic moments

`m_n = <eta, S^n eta> = e_1^T J_d^n e_1`

are determined by the same finite Jacobi packet.

Conversely, on the finite cyclic subspace, the cyclic-bulk reduction already
states that the reduced bulk object is determined by its moment sequence.

Therefore the sharp fixed-depth plaquette bulk datum is equivalently one finite
cyclic-moment packet.

## Corollary 1: the first Jacobi layer is already the first nontrivial moment layer

For normalized `eta`,

`alpha_0 = m_1`,

`beta_1^2 = m_2 - m_1^2`.

So the first nontrivial Jacobi packet `(alpha_0, beta_1)` is already
equivalent to the first nontrivial cyclic-moment pair `(m_1, m_2)`.

## Theorem 2: the propagated retained triple still does not determine even the first nontrivial moment pair

For the same explicit witness pair `S_P`, `S_Q` from the finite-Jacobi
reduction:

- the propagated retained triples agree exactly,
- but

  `m_1^P != m_1^Q`,

  `m_2^P != m_2^Q`.

So even the first nontrivial scalar bulk layer is still not fixed by the
propagated retained triple on the current bank.

## What this closes

- exact scalar reformulation of the sharp fixed-depth plaquette bulk front as a
  finite cyclic-moment packet
- exact equivalence between the first Jacobi layer and the first nontrivial
  cyclic-moment pair
- exact sharper noncollapse theorem: the propagated retained triple still does
  not determine even `(m_1, m_2)`

## What this does not close

- the true explicit finite moment packet of the actual `beta = 6` bulk object
- the explicit identity rim datum `eta_6(e)`
- the explicit plaquette framework-point PF data
- the global sole-axiom PF selector theorem

## Why this matters

This is the sharpest scalar formulation yet of the non-Wilson plaquette seam.

The branch can now say:

- the fixed-depth plaquette bulk lane is one finite moment packet,
- the boundary side is already one explicit `K(W)` evaluation law,
- and the current bank still does not determine even the first nontrivial
  moment pair.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_beta6_identity_rim_finite_moment_packet_reduction_2026_04_18.py
```
