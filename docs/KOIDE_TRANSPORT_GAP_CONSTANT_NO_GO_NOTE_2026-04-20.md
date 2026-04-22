# Koide Transport-Gap Constant No-Go

**Date:** 2026-04-20  
**Status:** exact support / candidate-route demotion on the charged-lepton Koide lane  
**Primary runner:** `scripts/frontier_koide_transport_gap_constant_no_go.py`

## Scope

The selected-slice scalar-potential note recorded the numerical observation

```text
1 / (eta / eta_obs)  ≈  4pi / sqrt(6).
```

This looked like a possible bridge between the DM transport lane and the Koide
charged-lepton lane. The question is whether it can act as the missing
selected-line `m`-selector.

It cannot.

## The no-go

On the current branch:

- `eta / eta_obs = 0.188785929502` is already a fixed transport-lane constant,
- `4pi / sqrt(6)` is already a fixed Koide-geometry constant.

So the comparison is a relation between two constants:

```text
1 / eta_ratio = 5.29699994...
4pi / sqrt(6) = 5.13019932...
relative gap   = 3.25%.
```

Even if that gap were zero, the statement would still be:

```text
constant = constant.
```

It would not introduce any dependence on the selected-line coordinate `m`, and
so it could not isolate the physical point `m_*`.

## Meaning

The transport-gap comparison is therefore not a live charged-lepton closure
route. At best it is a cross-lane support observation linking:

- one already-fixed DM transport constant, and
- one already-fixed Koide geometry constant.

It should be treated as a geometric curiosity or future bridge target, not as a
missing `m`-selection law on the current branch.
