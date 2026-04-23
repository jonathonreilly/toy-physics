# Majorana Endpoint-Exchange Midpoint Theorem

**Date:** 2026-04-15
**Status:** exact positive bridge theorem on the minimal non-homogeneous
finite-register lift
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_neutrino_majorana_endpoint_exchange_midpoint_theorem.py`

## Question

After the exact local Majorana selector fixes the self-dual point

`rho = 1`,

can the branch write a genuinely new **non-homogeneous** local-to-generation
bridge on the exact finite taste staircase, rather than searching for another
homogeneous source-side observable?

Equivalently:

- the current exact stack by itself does not lift the selected local point
- the remaining honest missing object was a new non-homogeneous bridge or a
  new absolute-scale datum
- does the hierarchy lane already provide the right finite datum once the
  bridge is written correctly?

## Bottom line

Yes, on the minimal finite-register bridge.

The hierarchy / taste-decoupling lane already gives the exact staircase

`lambda_k = alpha_LM^k`, `k in {0,...,16}`,

with two exact endpoints:

- UV endpoint: `k = 0`, `lambda_0 = 1`
- IR endpoint: `k = 16`, `lambda_16 = alpha_LM^16`

If the local normal/pairing axis exchange is lifted to the finite staircase as
the exact exchange of those two endpoints, then the bridge is no longer
arbitrary. On the finite ordered register, the unique endpoint-preserving
order-reversing involution is

`k -> 16 - k`,

equivalently

`lambda -> alpha_LM^16 / lambda`.

The self-dual local point must then map to the unique fixed point of that
involution:

`k_B = 8`,

with exact scale

`lambda_* = alpha_LM^8`.

So the branch no longer lacks an absolute staircase anchor once this minimal
non-homogeneous endpoint-exchange bridge is admitted.

## Inputs

This theorem combines four already-exact surfaces:

- [NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md](./NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md)
- [NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md](./NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md)
- [HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md](./HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md)
- [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md)

Those notes already prove:

1. the admitted local Majorana selector is the self-dual point `rho = 1`
2. the current exact stack does **not** lift that point by itself
3. the hierarchy lane is an exact finite `16`-step taste staircase between two
   exact endpoints, not just an unbounded scale family

So the remaining honest bridge question is:

> how should the exact local axis exchange act on that exact finite register?

## Exact theorem

### 1. The hierarchy lane supplies an exact finite register

The hierarchy / taste-decoupling chain gives

`lambda_k = alpha_LM^k`, `k = 0,...,16`.

So the Majorana scale no longer needs to be embedded into a featureless
positive ray if we are willing to use the exact finite hierarchy register.

### 2. Endpoint exchange on the finite register is unique

On the finite totally ordered set `{0,...,16}`, any endpoint-preserving
order-reversing involution is forced by rank complement:

`E(k) = 16 - k`.

There is no second finite endpoint-exchange involution on this ordered
register.

### 3. The corresponding scale exchange is exact

Because `lambda_k = alpha_LM^k`, the endpoint exchange acts in scale form as

`E(lambda_k) = lambda_{16-k} = alpha_LM^16 / lambda_k`.

So the finite-register bridge is genuinely non-homogeneous: it is tied to the
two exact endpoints of the hierarchy lane.

### 4. The self-dual local point lifts to the unique midpoint

The exact local selector already forces the self-dual point under local axis
exchange:

`rho = 1`.

If that same exchange is lifted to the finite staircase via the unique
endpoint-exchange involution above, the image of the local self-dual point must
be a fixed point of

`k -> 16-k`.

There is one such fixed point:

`k = 8`.

Equivalently in scale variables:

`lambda = alpha_LM^16 / lambda`

forces

`lambda_* = alpha_LM^8`.

## The theorem-level statement

**Theorem (Endpoint-exchange midpoint theorem on the finite Majorana
staircase bridge).**
Assume:

1. the exact local Majorana selector is the self-dual point `rho = 1`
2. the hierarchy lane supplies the exact finite staircase
   `lambda_k = alpha_LM^k`, `k = 0,...,16`
3. the local axis exchange is lifted to the staircase as the exact exchange of
   the two finite hierarchy endpoints

Then:

1. the lifted staircase exchange is uniquely `k -> 16-k`
2. in scale form it is uniquely `lambda -> alpha_LM^16 / lambda`
3. the unique fixed point is `k = 8`
4. therefore the absolute Majorana staircase anchor on this minimal
   non-homogeneous bridge is

   `k_B = 8`

## Relationship to the earlier obstruction theorems

This does **not** contradict the earlier self-dual staircase-lift obstruction.

That obstruction theorem was about the **current exact stack alone**:

- selected local point still projective
- current `Z_3` texture class still homogeneous
- no lift from those data alone

This new theorem is different:

- it adds a genuinely new non-homogeneous bridge
- that bridge is not another source-side scalar or another homogeneous algebraic
  construction
- it uses the exact finite hierarchy register and its two exact endpoints

So this note is the constructive positive theorem that the obstruction notes
left open in principle.

## What this closes

This closes one real denominator-side gap:

- the absolute Majorana staircase anchor is no longer open on the minimal
  endpoint-exchange bridge

The branch can now say:

- the exact local Majorana point is self-dual
- the exact hierarchy lane is a finite `16`-step register
- the minimal endpoint-exchange lift of that self-dual point forces
  `k_B = 8`

## What this does not close

This note still does **not** derive the full three-generation texture
numerically.

What remains downstream is:

- how the activated source amplitude populates the three-generation
  `A/B/epsilon` texture
- whether the singlet/doublet placement beyond the midpoint anchor is fixed
  without extra choices
- whether `eps/B` is derived rather than fitted
- the remaining `m_3` / texture-factor inputs in the leptogenesis chain

So this theorem closes the **absolute staircase anchor**, not the full DM
denominator.

## Safe wording

**Can claim**

- the branch now has a genuinely new non-homogeneous local-to-generation bridge
- on that bridge, the exact local self-dual point lifts to the unique midpoint
  of the exact finite `16`-step hierarchy register
- the corresponding absolute staircase anchor is `k_B = 8`
- the remaining denominator blocker is now downstream texture/amplitude closure,
  not the absolute staircase anchor itself

**Cannot claim**

- the full three-generation `A/B/epsilon` amplitudes are already derived
- full zero-import `eta` is already closed
- the entire DM lane is fully across the line

## Command

```bash
python3 scripts/frontier_neutrino_majorana_endpoint_exchange_midpoint_theorem.py
```
