# PMNS Graph-Commutant Cycle Value Boundary

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_pmns_graph_commutant_cycle_value_boundary.py`

## Question

Can the graph-first selected-axis route together with the projected commutant /
generation-boundary data derive a positive value law for the reduced oriented
forward-cycle channel

`A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31`

on the retained PMNS blocker?

## Bottom line

No. The route is genuine and exact, but it is value-blind on the reduced
forward-cycle family.

What it fixes:

1. the weak-axis choice on the `hw=1` triplet
2. the residual `Z_2` stabilizer of that selected axis
3. the branch/orientation selector `tau`
4. the passive offset class `q`

What it does not fix:

1. the reduced forward-cycle values `(u, v, w)`
2. the active 4-real / 5-real source data that sit behind them

## Exact statement

The graph-first selector reduces the `hw=1` triplet to a weak-axis surface with
residual `Z_2`. The projected commutant on that surface then supplies the same
selector bundle `(tau, q)` as before, but it is constant on the reduced
forward-cycle family.

Consequently, two distinct reduced-cycle points can share the same graph-first
/ projected-commutant route signature while having different cycle values.
That is the precise reason the route cannot close full positive value
selection.

## Relation to the existing bank

This boundary is compatible with the current exact package:

1. the graph-first route derives alignment, but not the values
2. the projected commutant route derives selectors, but not the reduced cycle
   coefficients
3. the native oriented-cycle observable law reads the coefficients exactly once
   an active block is already supplied
4. the reduced-channel no-go remains correct: the current exact bank does not
   select a unique reduced-channel point

## Honest next target

The next positive candidate is not more commutant. It is a lower-level
source/transport law on the retained lepton surface that actually selects
`(u, v, w)` from `Cl(3)` on `Z^3` or from a genuinely admitted extension.

## Command

```bash
python3 scripts/frontier_pmns_graph_commutant_cycle_value_boundary.py
```
