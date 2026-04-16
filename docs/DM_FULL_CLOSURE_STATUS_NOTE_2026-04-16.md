# DM Full-Closure Status

**Date:** 2026-04-16  
**Script:** `scripts/frontier_dm_full_closure_status.py`  
**Framework convention:** “axiom” means only `Cl(3)` on `Z^3`

## Bottom line

On the current flagship branch, the DM gate is now closed on the
PMNS-assisted `N_e` route.

The branch now has:

1. exact one-flavor theorem-native transport baseline  
   - `eta / eta_obs = 0.188785929502`

2. theorem-grade PMNS selector closure on the exact reduced `N_e` domain  
   - three stationary branches
   - one unique global minimum
   - selected branch gives `eta / eta_obs = 1`

3. final quantitative mapping / normalization closure  
   - `R = 5.48285209497574`
   - `Omega_b = 0.04919295758525652`
   - `Omega_DM = 0.26971771055437643`

So the old one-flavor `5.297x` miss is not the flagship end state anymore.
It is the baseline that the PMNS-assisted route repairs.

## Meaning

The two live gaps that had kept DM open on this branch are now closed:

- theorem-grade PMNS selector closure
- final DM quantitative mapping / normalization closure

That is the full-closure status relevant for review on the current science
surface.

## Command

```bash
python3 scripts/frontier_dm_full_closure_status.py
```
