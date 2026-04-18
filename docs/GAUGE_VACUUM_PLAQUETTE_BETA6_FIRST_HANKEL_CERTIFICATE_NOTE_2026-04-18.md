# Gauge-Vacuum Plaquette Beta=6 First Hankel Certificate

**Date:** 2026-04-18  
**Status:** exact first-layer scalar reformulation of the non-Wilson plaquette
frontier; the current bank already fails at one first Hankel + `K` certificate  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_beta6_first_hankel_certificate_2026_04_18.py`

## Question

After the fixed-depth plaquette lane has been reduced to one minimal
`moment + K` certificate, can the first constructive obstruction be restated in
a more canonical scalar form?

## Answer

Yes.

At the first nontrivial scalar layer, the moment pair `(m_1, m_2)` is
equivalent to the first Hankel layer

`H_1 = [[1, m_1], [m_1, m_2]]`,

equivalently to the pair `(m_1, Delta_1)` with

`Delta_1 := m_2 - m_1^2 = beta_1^2`.

So the first constructive non-Wilson plaquette obstruction may now be stated
as one first Hankel + `K` certificate:

1. one first Hankel layer `H_1` of the identity-rim cyclic bulk object;
2. one already-explicit boundary law through `K(W)`.

The current bank already fails at that first Hankel layer, because the same
propagated retained triple still does **not** determine even `(m_1, m_2)`,
hence does not determine `H_1`.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_MOMENT_PACKET_REDUCTION_NOTE_2026-04-18.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_MOMENT_PACKET_REDUCTION_NOTE_2026-04-18.md):

- the fixed-depth plaquette bulk datum is equivalently one finite cyclic-moment
  packet,
- and the current bank still does not determine even the first nontrivial
  moment pair `(m_1, m_2)`.

From
[GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md):

- the boundary law is already explicit as
  `Z_beta^env(W) = <K(W), v_beta>`.

## Theorem 1: the first nontrivial moment layer is exactly the first Hankel layer

Assume the normalized identity-rim state so that `m_0 = 1`.

Then the following are equivalent first-layer data:

1. the first nontrivial moment pair `(m_1, m_2)`;
2. the first Hankel matrix
   `H_1 = [[1, m_1], [m_1, m_2]]`;
3. the pair `(m_1, Delta_1)` with
   `Delta_1 = m_2 - m_1^2`.

### Proof

The matrix `H_1` is built directly from `(m_1, m_2)`, so `(1)` implies `(2)`.

Conversely, because the upper-left entry is fixed at `1`, the matrix `H_1`
determines `(m_1, m_2)` exactly. So `(2)` implies `(1)`.

Also `Delta_1 = m_2 - m_1^2` is determined by `(m_1, m_2)`, and conversely
`m_2 = Delta_1 + m_1^2`, so `(1)` and `(3)` are equivalent.

Therefore all three first-layer formulations are equivalent.

## Corollary 1: the first constructive plaquette blocker is one first Hankel + `K` certificate

Because the boundary law through `K(W)` is already explicit, the first honest
non-Wilson constructive plaquette blocker is now:

- one first Hankel layer `H_1`,
- together with one explicit downstream `K(W)` boundary law.

So the current plaquette blocker is sharper than a generic moment packet. It is
one first Hankel + `K` certificate.

## Corollary 2: the current bank already fails at that first Hankel layer

The fixed-depth moment reduction already provides a witness pair with:

- the same propagated retained triple,
- but different `(m_1, m_2)`.

By Theorem 1, that same witness pair therefore has different first Hankel
layers `H_1`.

So the current bank already fails at the first Hankel layer of the plaquette
certificate.

## What this closes

- exact canonical reformulation of the first plaquette scalar layer as a Hankel
  layer
- exact sharper first-layer obstruction certificate on the non-Wilson plaquette
  route
- exact current-bank failure at that first Hankel layer

## What this does not close

- the full finite moment packet of the true `beta = 6` bulk object
- the explicit plaquette framework-point PF data
- a positive global PF selector

## Why this matters

The non-Wilson plaquette frontier is now sharper than a generic scalar packet.

At the first constructive layer it is one first Hankel + `K` certificate.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_beta6_first_hankel_certificate_2026_04_18.py
```
