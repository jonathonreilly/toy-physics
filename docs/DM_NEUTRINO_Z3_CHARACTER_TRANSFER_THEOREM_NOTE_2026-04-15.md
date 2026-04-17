# DM Neutrino `Z_3` Character-Transfer Theorem

**Date:** 2026-04-15  
**Status:** exact theorem on the activation law of the invented phase-lift
family  
**Script:** `scripts/frontier_dm_neutrino_z3_character_transfer_theorem.py`

## Question

The branch already had the invented mixed-bridge family

`K_lambda = d I + r (e^{i lambda delta_src} S + e^{-i lambda delta_src} S^2)`

with exact weak-only source

`delta_src = 2pi/3`.

Was `lambda` really a free amplitude? Or does exact source transfer force it
onto discrete branches?

## Bottom line

Exact source transfer forces it onto discrete branches.

The coefficient multiplying `S` is

`chi(lambda) = exp(i lambda delta_src)`.

If the bridge is to carry the exact weak-only `Z_3` source, `chi` must be a
true one-dimensional `Z_3` character, so

`chi^3 = 1`.

Since `delta_src = 2pi/3`, this becomes

`exp(i 3 lambda delta_src) = exp(i 2pi lambda) = 1`,

therefore

`lambda in Z`.

So on the local continuity strip `|lambda| <= 1`, the only exact
source-faithful branches are

`lambda in {-1, 0, +1}`.

With the retained source orientation `delta_src = +2pi/3`, the nontrivial
physical branch is

`lambda = +1`,

while `lambda = -1` is the conjugate / reflected companion and `lambda = 0`
is the retained zero law.

## Why this matters

This removes the old ambiguity in the invented phase-lift family.

The branch no longer has to say:

- "maybe `lambda` is some continuous activation amplitude"

It can now say:

- exact `Z_3` source transfer gives only three local branches
- the physical nontrivial one is `lambda = 1`

So the phase-lift family itself no longer carries a free local activation
parameter.

## What this closes

This closes the activation law on the invented mixed-bridge family itself.

It is now exact that:

- the phase-lift family is only source-faithful at discrete branches
- `lambda = 1` is the source-oriented full-transfer branch

## What this does not close

This note does **not** yet prove that the exact `Z_3`-covariant circulant
family gives a nonzero physical leptogenesis CP tensor in the heavy-neutrino
mass basis.

That is a different question, and it is the next theorem boundary.

## Command

```bash
python3 scripts/frontier_dm_neutrino_z3_character_transfer_theorem.py
```
