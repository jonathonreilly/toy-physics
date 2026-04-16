# DM Leptogenesis Numerator / Denominator Consistency Audit

**Date:** 2026-04-16  
**Audit runner:** `scripts/frontier_dm_leptogenesis_numden_consistency_audit.py`  
**Framework convention:** "axiom" means only `Cl(3)` on `Z^3`.

## Verdict

The current exact authority path is internally consistent on the numerator and
denominator.

What the audit checks:

1. the coherent CP-kernel numerator `epsilon_1` is reproduced directly from the
   exact source package and exact denominator `K00`
2. the same `K00 = 2` is used consistently in the washout-side effective mass
   `m_tilde`
3. the old stale exact-kernel runner no longer carries the pre-`K00` near-1
   benchmark
4. the retained-fit comparator and the direct-transport authority path are now
   cleanly separated

## Main conclusion

The old near-observation value was coming from a stale normalization split.
After that is removed:

- retained-fit comparator: `eta/eta_obs = 0.557874966110017`
- direct-transport authority: `eta/eta_obs = 0.188785929502`

So the remaining mismatch is not a hidden numerator/denominator swap inside the
exact authority path. It is a transport-content / model-content issue. 
