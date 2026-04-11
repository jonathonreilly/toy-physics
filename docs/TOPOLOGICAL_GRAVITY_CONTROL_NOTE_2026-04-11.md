# Gravity-vs-Topology Control Note

**Date:** 2026-04-11  
**Status:** exploratory-reopen on an audited SSH surface

**Scripts:**
- `scripts/frontier_topological_phases.py`
- `scripts/frontier_topological_control.py`

## Question

Does the claimed gravity-driven SSH/topological transition survive a matched
disorder/control comparison, or is it just generic on-site symmetry breaking?

## Main scan

The self-consistent gravity scan on the open SSH chain reports:

- free system: 2 edge modes
- edge modes remain through `G = 0.20`
- edge modes vanish at `G = 0.50`
- the bulk gap is reduced but not closed before the edge modes disappear
- sublattice polarization is nonzero at small `G` and fades again at strong `G`

Taken alone, this is a candidate topological transition, not yet a universal
claim.

## Matched control

The matched disorder control on the same audited SSH surface gives:

- self-gravity transition at `G = 0.50`
- matched random disorder does not destroy the edge modes in the scanned
  `G` window
- the fine disorder scan finds a disorder threshold near `sigma ~ 0.36`
- the gravity-to-disorder variance ratio at the gravity transition is `0.36`

So the gravity signal is not explained by the matched disorder control.

## Interpretation

What survives is narrower than the original headline, but real:

- the gravity-driven edge-mode loss survives the matched disorder comparison
- the control indicates the effect is not just variance-driven
- the broader universality claim is still open because this is one audited SSH
  surface, not a finished classification theorem

## Retained reading

> self-gravity produces a gravity-specific SSH edge-mode transition on the
> audited open chain, but the claim should remain surface-specific and
> exploratory until wider control families are checked

## Conclusion

This lane is worth keeping as an **exploratory-reopen** result, not as a
universal topological theorem:

- the claimed transition survives the matched disorder/control comparison
- the lane is strong enough to retain
- the documentation should stay constrained to the audited surface and not
  generalize beyond it
