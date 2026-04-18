# Gauge-Vacuum Plaquette Beta=6 Fixed-Depth Scalar Certificate

**Date:** 2026-04-18  
**Status:** exact scalar packaging of the fixed-depth non-Wilson plaquette
route; the whole lane is one minimal `moment + K` certificate, and the current
bank already fails at the first nontrivial moment pair  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_beta6_fixed_depth_scalar_certificate_2026_04_18.py`

## Question

After the finite-moment packet reduction, can the fixed-depth plaquette lane be
put in a fully scalar hard-review-safe form?

## Answer

Yes.

At fixed depth, the whole non-Wilson plaquette route is exactly one minimal
scalar certificate:

1. one finite cyclic-moment packet of the identity-rim bulk object;
2. one already-explicit downstream boundary law
   `Z_beta^env(W) = <K(W), v_beta>`.

So the lane is no longer most honestly described as:

- an operator-evaluation problem,
- or even a Jacobi-packet problem.

It is one minimal **`moment + K` certificate**.

And the current bank already fails at the first nontrivial moment layer:
the propagated retained triple still does not determine `(m_1, m_2)`.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_MOMENT_PACKET_REDUCTION_NOTE_2026-04-18.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_MOMENT_PACKET_REDUCTION_NOTE_2026-04-18.md):

- the sharp fixed-depth bulk datum is equivalently one finite cyclic-moment
  packet,
- and the current bank still does not determine even the first nontrivial
  moment pair.

From
[GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md):

- the downstream boundary law is already explicit as
  `Z_beta^env(W) = <K(W), v_beta>`.

## Theorem 1: exact fixed-depth `moment + K` certificate form

Fix propagation depth `d = L_perp - 1`.

Then fixed-depth class-sector plaquette closure is equivalent to:

1. one finite cyclic-moment packet of the identity-rim bulk object,
2. one explicit downstream boundary evaluation law through `K(W)`.

So the whole fixed-depth non-Wilson plaquette lane is one minimal `moment + K`
certificate.

## Corollary 1: current-bank failure already occurs at the first scalar layer

The finite-moment reduction theorem already gives a witness pair with:

- the same propagated retained triple,
- but different first nontrivial moment pair `(m_1, m_2)`.

Therefore the current bank still fails already at the first scalar layer of the
fixed-depth plaquette certificate.

## What this closes

- one fully scalar hard-review-safe packaging of the fixed-depth non-Wilson
  plaquette route
- exact clarification that the remaining plaquette seam is one finite
  `moment + K` certificate
- exact current-bank failure location at the first nontrivial moment layer

## What this does not close

- the true explicit finite moment packet of the actual `beta = 6` bulk object
- the explicit plaquette framework-point PF data
- the global sole-axiom PF selector theorem

## Why this matters

This is the cleanest scalar statement yet of the non-Wilson PF frontier.

The branch can now say:

- Wilson positive reopening is one local `2-edge + 3` certificate,
- fixed-depth plaquette non-Wilson closure is one minimal `moment + K`
  certificate,
- and the current bank already fails at the first constructive layer on both.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_beta6_fixed_depth_scalar_certificate_2026_04_18.py
```
