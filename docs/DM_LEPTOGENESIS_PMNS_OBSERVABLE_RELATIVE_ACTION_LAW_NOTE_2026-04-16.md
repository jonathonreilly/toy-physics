# DM Leptogenesis PMNS Observable-Relative-Action Law

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_leptogenesis_pmns_observable_relative_action_law.py`

## Law

On the fixed native charged-lepton-active seed surface, define the exact
relative bosonic action

`S_rel(H_e || H_seed) = Tr(H_seed^{-1} H_e) - log det(H_seed^{-1} H_e) - 3`

where:

- `H_seed` is the exact aligned-seed charged Hermitian block
- `H_e` is the charged Hermitian block induced by the off-seed source

Then:

1. determine the favored flavor column `i_*` from the exact transport-extremal
   class
2. among all positive off-seed sources on the same seed surface satisfying
   `eta_{i_*} / eta_obs = 1`, choose the one minimizing `S_rel`

This is the strongest framework-internal selector currently available because
its objective is built directly from the exact scalar `log|det|` observable
principle.

## Output

The law selects:

- `x_rel = (0.47167533, 0.55381069, 0.66451397)`
- `y_rel = (0.20806279, 0.46438280, 0.24755440)`
- `delta_rel ~ 0`

so the off-seed source is

- `xi_rel = (-0.09165800, -0.00952264, 0.10118064)`
- `eta_rel = (-0.09860388, 0.15771613, -0.05911224)`
- `delta_rel ~ 0`

and the resulting transport values are

`eta / eta_obs = (1.0, 0.75917896, 0.48458840)`.

The favored column remains column `0`, and exact closure is reached there.

## Why this matters

This is stronger than the earlier minimum-information ansatz because the
objective is no longer imported from information geometry by hand. It is an
exact relative action on `H_e` built from the framework’s existing scalar
observable-principle grammar.

So the remaining philosophical/theorem-level gap is now very narrow:

> does the sole axiom itself force stationary/minimal relative bosonic action
> on the fixed seed surface?

If yes, then the PMNS-assisted DM closure becomes much closer to being
sole-axiom complete.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_observable_relative_action_law.py
```
