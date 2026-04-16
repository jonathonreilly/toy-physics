# DM Full Theorem-Closure Audit

**Date:** 2026-04-16  
**Audit runner:** `scripts/frontier_dm_full_closure_audit.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`.

## Verdict

**FULL THEOREM CLOSURE**

There is no remaining transport-side non-axiom ingredient on the authority
path.

## What the audit verifies

1. the source package is theorem-derived
2. the transfer coefficients are theorem-derived
3. the heavy-basis denominator `K00` is theorem-derived
4. the physical projection law `(Y^dag Y)11 = K00` is theorem-derived
5. the equilibrium conversion factors are theorem-derived
6. the radiation expansion law `H_rad(T)` is theorem-derived
7. the direct transport integral is theorem-derived
8. the final authority runner does not use reduced benchmark ingredients
   like `texture_factor`, `doublet_CP`, or `kappa_fit` on the authority path

## Honest end state

The branch is theorem-complete, but not phenomenologically successful on this
lane:

- exact theorem-native `eta / eta_obs = 0.188785929502`

So the final issue is no longer a missing derivation. It is a derived
numerical shortfall on the exact branch.
