# Majorana Local Nilpotent Reduction

**Date:** 2026-04-15  
**Status:** exact one-generation local reduction theorem; not a global
nonlocal/multi-generation no-go  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_majorana_local_nilpotent_reduction.py`

## Question

Even after the current-stack zero law, one might still imagine a future **local
nonlinear** fermionic charge-`2` primitive on the one-generation Majorana lane.

Does the one-generation local Grassmann algebra actually leave such a local
nonlinear tower available?

## Bottom line

No.

On the one-generation local lane, the unique charge-`2` seed

`S_unique = nu_R^T C P_R nu_R`

is Grassmann-nilpotent:

`S_unique^2 = 0`.

Therefore any local polynomial in that seed truncates exactly to

`P(S_unique) = a_0 + a_1 S_unique`.

If one asks specifically for a local fermionic charge-`2` primitive, the
charge-zero constant term is forbidden, so the local primitive reduces exactly
to

`Xi_local^(-2) = a_1 S_unique`.

So there is **no genuinely nonlinear local fermionic charge-`2` tower** on the
one-generation lane.

## Inputs

This theorem uses:

- [NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md](./NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md)
- [NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md](./NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md)
- [NEUTRINO_MAJORANA_QUADRATIC_PFAFFIAN_UNIQUENESS_NOTE.md](./NEUTRINO_MAJORANA_QUADRATIC_PFAFFIAN_UNIQUENESS_NOTE.md)

The logic is:

- the operator-classification theorem fixes the unique local charge-`2` seed
- the canonical local-block theorem reduces the one-generation local block to
  the `2 x 2` canonical channel
- the quadratic Pfaffian uniqueness theorem then controls the unique finite
  quadratic completion class once a local seed is turned on

This note now removes the remaining local nonlinear-polynomial loophole.

## Exact theorem

There are three exact steps.

### 1. The unique local seed is bilinear and nilpotent

The one-generation local seed uses two Grassmann variables. Because Grassmann
variables square to zero and anticommute, the bilinear seed satisfies

`S_unique^2 = 0`.

### 2. Any local polynomial truncates after first order

For any polynomial

`P(S_unique) = a_0 + a_1 S_unique + a_2 S_unique^2 + ...`,

nilpotency gives

`P(S_unique) = a_0 + a_1 S_unique`.

So there is no infinite or higher-order local polynomial tower built only from
the one-generation local fermionic seed.

### 3. A local charge-`2` primitive keeps only the linear term

The constant term `a_0` has fermion-number charge `0`, not `-2`. So a local
fermionic charge-`2` primitive must be exactly the linear seed term:

`Xi_local^(-2) = a_1 S_unique`.

Thus the local one-generation Majorana search space is not:

- quadratic seed plus independent higher local polynomial fermionic terms

but only:

- one linear local seed direction

## The theorem

**Theorem (Local nilpotent reduction on the one-generation Majorana lane).**
Assume the current anomaly-fixed one-generation Majorana channel and restrict to
local fermionic primitives built polynomially from that same local seed. Then
every local charge-`2` primitive is exactly linear in `S_unique`:

`Xi_local^(-2) = a_1 S_unique`.

Equivalently: there is no genuinely nonlinear local fermionic charge-`2`
polynomial tower on the one-generation lane.

## What this closes

This closes one more local loophole.

Before:

- a reader could still imagine a future local nonlinear fermionic primitive
  built from the same one-generation seed

After:

- that local nonlinear escape route is gone
- any future alternative to the current local Pfaffian picture must come from
  nonlocal structure, multi-generation structure, or additional spectator
  sectors rather than a higher local fermionic polynomial in `S_unique`

## What this does not close

This note does **not** prove:

- that no nonlocal charge-`2` primitive could exist
- that no multi-generation extension could change the story
- that no spectator-coupled local completion could exist
- that the Pfaffian sector is axiom-forced
- that the full neutrino problem is solved

It is a one-generation local-polynomial reduction theorem only.

## Safe wording

**Can claim**

- the unique one-generation local charge-`2` seed is nilpotent
- any local fermionic charge-`2` polynomial primitive reduces exactly to a
  linear seed term
- there is no genuinely nonlinear local fermionic charge-`2` tower on the
  one-generation lane

**Cannot claim**

- all future nonlocal or multi-generation routes are impossible
- the full Majorana problem is closed

## Command

```bash
python3 scripts/frontier_neutrino_majorana_local_nilpotent_reduction.py
```
