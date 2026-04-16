# DM Neutrino Post-Canonical Slot-Supported Support Class

**Date:** 2026-04-15  
**Status:** exact support-class theorem after the canonical denominator lanes
close negatively  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_postcanonical_slot_support_class.py`

## Question

After the branch proves that the surviving positive denominator object must be
a post-canonical right-sensitive mixed bridge with two slot amplitudes `u,v`,
is there still support-class ambiguity about what that bridge must act on?

Or can the support class itself now be reduced exactly?

## Bottom line

It can be reduced exactly.

On the full `Z_3`-basis singlet-doublet carrier

```text
K_Z3 =
[ sigma,            (u+v)e^{-i phi},   (u-v)e^{+i phi} ]
[ (u+v)e^{+i phi},  tau+rho,           m               ]
[ (u-v)e^{-i phi},  m^*,               tau-rho         ]
```

the physical heavy-neutrino-basis CP tensor depends only on the slot amplitudes
`u,v` and the phase `phi`. It is exactly insensitive to the spectator data
`sigma, tau, rho, m`.

Therefore the minimal surviving support class is the slot-supported family

```text
K_Z3^slot =
[ 0,               (u+v)e^{-i phi},   (u-v)e^{+i phi} ]
[ (u+v)e^{+i phi}, 0,                 0               ]
[ (u-v)e^{-i phi}, 0,                 0               ]
```

So the remaining positive DM bridge is now support-resolved too:

> a post-canonical right-sensitive slot-supported mixed bridge with two real
> slot amplitudes `u` and `v`.

## Inputs

This note sharpens:

- [DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md)
- [DM_NEUTRINO_POSTCANONICAL_EXTENSION_CLASS_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_EXTENSION_CLASS_NOTE_2026-04-15.md)

The first note identifies the physical carrier and proves spectator-data
independence of the CP tensor in effect. The second identifies the surviving
positive extension class after all admitted canonical routes die. This note
turns that into an exact support-class reduction.

## Exact theorem

### 1. Spectator data are CP-inert

For the full singlet-doublet carrier, the heavy-neutrino-basis tensor is

`Im[(K_mass)_{0j}^2] = -2 u v sin(2 phi)`.

It does not depend on:

- `sigma`
- `tau`
- `rho`
- `m`

So those entries are spectator data with respect to the actual leptogenesis
CP tensor.

### 2. The slot support is all that survives

Once the spectator entries are quotiented out, the remaining nonzero support is
exactly:

- `K_01`
- `K_02`
- and their Hermitian conjugates

That is, the support is exactly the singlet-doublet slot support.

### 3. Minimal surviving support class

So the smallest honest support class after the canonical no-gos is the
slot-supported family `K_Z3^slot` above.

It is:

- right-sensitive
- non-circulant
- post-canonical
- and minimal on support

## The theorem-level statement

**Theorem (Minimal post-canonical slot-supported support class).**
Assume the exact singlet-doublet CP-slot theorem and the exact post-canonical
extension-class theorem. Then the physical heavy-neutrino-basis CP tensor is
independent of the spectator diagonal / doublet-block data of the full
singlet-doublet carrier, and depends only on the slot amplitudes `u,v` and the
source phase `phi`. Therefore the minimal surviving positive support class is
the slot-supported singlet-doublet family `K_Z3^slot`.

## What this closes

This closes the support-class ambiguity on the remaining denominator object.

The branch no longer needs to say only:

- “some post-canonical mixed bridge”

It can now say more sharply:

- the remaining positive bridge is post-canonical
- and its minimal support is exactly the singlet-doublet slot support

## What this does not close

This note still does **not** derive:

- the microscopic source/support realization of that slot-supported bridge
- the activation law for `u`
- the activation law for `v`

So it is a support-class theorem, not yet a realization theorem.

## Command

```bash
python3 scripts/frontier_dm_neutrino_postcanonical_slot_support_class.py
```
