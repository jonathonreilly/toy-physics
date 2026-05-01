# DM Neutrino `c_odd` Bosonic Normalization Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_codd_bosonic_normalization_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

Can the odd transfer coefficient in

- `gamma = c_odd a_sel`

be fixed from the single axiom plus the current atlas?

## Bottom line

Yes, canonically.

On their exact minimal blocks, the reduced selector generator

`S_cls = diag(0,0,1,-1)`

and the DM odd triplet generator

`T_gamma = [[0,0,-i],[0,0,0],[i,0,0]]`

have the same exact bosonic source-response law under the unique additive
CPT-even scalar generator

`W[J] = log|det(D+J)| - log|det D|`.

Therefore the canonical odd normalization is

- `|c_odd| = 1`

and on the source-oriented branch convention we record

- `c_odd = +1`.

## Exact reason

The two generators have the same nonzero odd spectrum:

- `S_cls` has eigenvalues `{+1,-1,0,0}`
- `T_gamma` has eigenvalues `{+1,-1,0}`

so they differ only by null multiplicity.

After subtracting the zero-source baseline in `W`, that null multiplicity
drops out. On a scalar baseline `m I`, both source families satisfy

- `W = log|1 - j^2/m^2|`.

So they have:

- the same exact source-response curve
- the same exact small-source bosonic curvature

and therefore the same canonical odd normalization.

## Why this matters

This closes the odd normalization part of the weak-to-triplet transfer law.

The branch no longer has to say:

- “both `c_odd` and `M_even` are still open”

It can now say:

- the odd normalization is fixed canonically: `c_odd = +1`
- the remaining coefficient blocker is the even response matrix `M_even`

## What this does not close

This note does **not** derive:

- the activation law for the selector amplitude `a_sel`
- the even response matrix `M_even`
- the microscopic two-channel readout replacing the current bounded weak tensor
  readout

So this is an odd-normalization theorem, not full transfer-coefficient closure.

## Benchmark consequence

The benchmark stays

- `eta = 1.81e-10`
- `eta / eta_obs ~= 0.30`

because that benchmark was not limited by an unresolved odd normalization
factor. The live remaining gap is the even response law, not `c_odd`.

## Command

```bash
python3 scripts/frontier_dm_neutrino_codd_bosonic_normalization_theorem.py
```
