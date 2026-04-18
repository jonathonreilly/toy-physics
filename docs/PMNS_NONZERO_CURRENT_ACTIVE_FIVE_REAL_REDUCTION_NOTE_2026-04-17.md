# PMNS Nonzero Current Active Five-Real Reduction

**Date:** 2026-04-17  
**Status:** exact reduction theorem on the PMNS-native strong production lane  
**Script:** `scripts/PMNS_NONZERO_CURRENT_ACTIVE_FIVE_REAL_REDUCTION_2026_04_17.py`

## Question

After the fixed-slice readout frontier is closed, what is the strongest honest
next **PMNS-native microscopic** theorem target for producing nonzero

`J_chi`?

## Answer

On the strong PMNS-native microscopic lane, the remaining production object is
exactly the active off-seed `5`-real packet

`(xi_1, xi_2, eta_1, eta_2, delta)`

beyond the already native seed pair `(xbar, ybar)`.

More precisely:

1. the transfer-dominant and orbit-averaged corner-transport laws already fix
   the seed pair / aligned seed kernel;
2. seed pair plus the active off-seed `5`-real packet reconstruct the active
   microscopic block exactly;
3. the native current `J_chi` is therefore algorithmic from that packet;
4. distinct packets with the same seed pair and the same current-bank
   transport summaries can still carry distinct nonzero currents.

So the strongest honest next theorem target on the **PMNS-native strong route**
is no longer generic “holonomy production.” It is:

> derive a sole-axiom law for the active off-seed `5`-real packet, hence for
> nonzero `J_chi`.

## Exact reduction

### 1. The seed pair is already the closed part of the microscopic data

The current PMNS-native dynamical laws already recover:

- the aligned seed pair `(xbar, ybar)` from the transfer-dominant mode law;
- the same seed data and branch/orbit summaries from corner transport.

So the strong microscopic production problem is already downstream of those
seed data.

### 2. The remaining strong-route packet reconstructs the active block exactly

Write

`xi = (xi_1, xi_2, -xi_1 - xi_2)`,

`eta = (eta_1, eta_2, -eta_1 - eta_2)`.

Then

`x = xbar * (1,1,1) + xi`,

`y = ybar * (1,1,1) + eta`

and the active microscopic block is

`T_act = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`.

So once `(xbar, ybar, xi_1, xi_2, eta_1, eta_2, delta)` is supplied, the
active block is fixed exactly, and therefore the native current

`J_chi`

is fixed exactly.

### 3. Explicit witness: same seed data, different packet, different current

Take

- `A = T_act(x^A, y^A, 0.63)` with
  `x^A = (1.15, 0.82, 0.95)`,
  `y^A = (0.41, 0.28, 0.54)`
- `B = T_act(x^B, y^B, 0.63)` with
  `x^B = (1.20, 0.79, 0.93)`,
  `y^B = (0.52, 0.17, 0.54)`

These satisfy:

- the same seed pair
  `(xbar, ybar) = (0.9733333333333333, 0.41)`;
- the same projected transfer kernel;
- the same orbit-averaged corner-transport moments;
- but different active off-seed packets
  - `packet(A) = (0.17666666666666675, -0.15333333333333332, 0.0, -0.13, 0.63)`
  - `packet(B) = (0.22666666666666668, -0.18333333333333335, 0.11000000000000004, -0.24, 0.63)`
- and different nonzero native currents
  - `J_chi(A) = 0.423167427244281 - 0.159069084644413 i`
  - `J_chi(B) = 0.478167427244281 - 0.159069084644413 i`

So the current-producing content left after the current PMNS seed laws is
exactly this `5`-real packet.

## Consequence

This sharpens the PMNS-native production front one level further.

Before:

> derive a sole-axiom law producing a nontrivial fixed-slice holonomy pair,
> equivalently nonzero `J_chi`

Now, on the strongest purely PMNS-native microscopic route:

> derive a sole-axiom law for the active off-seed `5`-real packet beyond the
> already exact seed pair; nonzero `J_chi` is downstream and exact from that
> packet

That is the strongest honest next theorem surface on the PMNS-native **strong**
production lane.

## Boundary

This theorem does **not** prove a positive sole-axiom law for nonzero `J_chi`.

It proves only:

- exact reduction of the strong PMNS-native production problem to one active
  off-seed `5`-real packet;
- exact algorithmicity of `J_chi` once that packet is supplied;
- and an explicit witness that the current bank summaries stop before that
  packet.

It does **not** prove:

- a compressed-route `dW_e^H` theorem;
- a Wilson descendant theorem;
- a plaquette theorem;
- a global PF selector.

## Verification

```bash
python3 scripts/PMNS_NONZERO_CURRENT_ACTIVE_FIVE_REAL_REDUCTION_2026_04_17.py
```
