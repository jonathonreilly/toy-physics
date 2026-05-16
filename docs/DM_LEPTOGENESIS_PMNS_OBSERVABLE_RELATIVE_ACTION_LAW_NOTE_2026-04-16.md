# DM Leptogenesis PMNS Observable-Relative-Action Law

**Date:** 2026-04-16 (initial); 2026-05-16 prose recast so the load-bearing
selector law is explicitly carried by its already-derived effective-action
identity rather than presented as a free postulate.  
**Status:** support - structural / confirmatory support note attached to the
already-landed `DM_LEPTOGENESIS_PMNS_RELATIVE_ACTION_STATIONARITY_THEOREM_NOTE_2026-04-16`.  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_observable_relative_action_law.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`.

## Role of this note

This note records the **operational PMNS-assisted off-seed source selector**
used on the current refreshed DM branch and the numerical source it picks
out. It is a support note, not a free selector ansatz: the underlying
**why** of the selector — that the seed-relative bosonic action is the exact
Legendre-dual effective action of the sole-axiom observable generator — is
the load-bearing content of the sister theorem note
`DM_LEPTOGENESIS_PMNS_RELATIVE_ACTION_STATIONARITY_THEOREM_NOTE_2026-04-16`
and is exercised here so a reader of this note alone still sees the
derivation chain wired in.

## Selector law (operational form)

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

## Why the operational law is not an extra postulate

The seed-normalized matrix `Y = H_seed^{-1/2} H_e H_seed^{-1/2}` satisfies

`S_rel(Y) = sup_K [ log det(I + K) - Tr(K Y) ]`

with unique maximizer `K_* = Y^{-1} - I`. That is, `S_rel` is the **exact
Legendre dual** of the sole-axiom scalar observable generator
`W(K) = log det(I + K)`. This identity is proved and numerically exercised
in `DM_LEPTOGENESIS_PMNS_RELATIVE_ACTION_STATIONARITY_THEOREM_NOTE_2026-04-16`
(`scripts/frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem.py`,
Part 1) and is **re-exercised inside this note's own runner** in Part 0 so
the derivation chain is visible from the support runner alone.

Because `S_rel` is the effective action attached to the framework's exact
observable generator, the operational law above is the **native
effective-action selector** on the fixed seed surface, restricted by the
exact transport-favored column. The previous prose treated the
minimization step as a separate philosophical assumption; on the current
branch that assumption has already been discharged at the effective-action
reduction level, and uniqueness of the lowest-action closure branch on the
current closure patch is verified directly by the stationarity-theorem
runner.

Operationally, that means the support law inherits from its sister theorem:

- exact Legendre-dual / effective-action reduction of the objective
- exact transport-favored column on the fixed seed surface
- exact closure constraint `eta_{i_*}(H_e) / eta_obs = 1`
- uniqueness of the lowest-action closure branch on the current closure
  patch (bounded uniqueness, sampled feasible starts)

so the operational law here is a re-statement of that already-derived
selector on the same closure patch, used to produce the explicit numerical
source on the current refreshed DM branch.

## Output of the operational law on the current branch

The operational law selects:

- `x_rel = (0.47167533, 0.55381069, 0.66451397)`
- `y_rel = (0.20806279, 0.46438280, 0.24755440)`
- `delta_rel ~ 0`

so the off-seed source is

- `xi_rel = (-0.09165800, -0.00952264, 0.10118064)`
- `eta_rel = (-0.09860388, 0.15771613, -0.05911224)`
- `delta_rel ~ 0`

and the resulting transport values are

`eta / eta_obs = (1.0, 0.75917896, 0.48458840)`,

with the exact relative action value `S_rel = 0.240906701369` (matches the
Legendre-dual functional to ~1e-12 in the runner's Part 0).

The favored column remains column `0`, and exact closure is reached there.

## What this note still does not claim

This note does **not** claim, on its own:

1. a branch-global analytic proof that no second disconnected closure
   component exists anywhere else on the full seed surface
2. a full PMNS microscopic solve beyond the current branch
3. promotion of any upstream row beyond what
   `DM_LEPTOGENESIS_PMNS_RELATIVE_ACTION_STATIONARITY_THEOREM_NOTE_2026-04-16`
   itself claims

The current bounded scope is identical to that of the sister theorem
note: exact at the effective-action reduction, branch-exact at the
closure equation, and bounded-unique on the sampled current closure
patch.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_observable_relative_action_law.py
```
