# DM Neutrino Triplet Normalization Target

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_triplet_normalization_target.py`

## Question

What exact coefficient target must the missing triplet transfer law hit in
order to close the current benchmark, and could that target be achieved by
phase transfer alone?

## Bottom line

No.

At fixed `M_1` and washout:

- current benchmark: `epsilon / epsilon_DI = 0.277`
- closure target: `epsilon / epsilon_DI = eta_obs / eta_DI = 0.936`

So the missing law must enhance the realized CP kernel by

`0.936 / 0.277 = 3.37`.

But the exact source phase is already

`phi = 2 pi / 3`,

so the phase factor is already

`sin(phi) = sqrt(3)/2 = 0.866`.

Even a phase-only improvement to the absolute maximum `sin(phi)=1` would give
only

`1 / (sqrt(3)/2) = 1.155`

which is far too small.

Therefore the missing law cannot be mainly a phase-fixing theorem. It must be
an **amplitude / response normalization law** for the triplet-side carrier:

- `gamma`
- `delta + rho`
- `A + b - c - d`

## Why this matters

This closes the most common false hope on the branch: that the remaining gap is
just “use the right phase.”

It is not.

The exact source phase is already near-maximal. The missing factor is too large
for phase alone. So the next real theorem has to populate the magnitude of the
odd source and/or the even response channels.

## Command

```bash
python3 scripts/frontier_dm_neutrino_triplet_normalization_target.py
```
