# Geometry Lane Head-to-Head Note

**Date:** 2026-04-02  
**Status:** support - structural or confirmatory support note

## Setup

This note compares the best bounded hard-geometry lanes on exactly the
same seeds and the same readout:

- `16` matched seeds
- `npl = 25`
- `y_range = 12`
- `connect_radius = 3.0`
- `N = 25, 40, 60, 80, 100`
- readout: `pur_min` under layer normalization, plus gravity mean and
  `g/SE`

Compared lanes:

1. imposed modular gap = 2
2. imposed modular gap = 4
3. central-band removal `|y-center| < 1`
4. central-band removal `|y-center| < 2`

Source log:
[logs/2026-04-02-geometry-lane-head-to-head.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-02-geometry-lane-head-to-head.txt)

## Results

| N | Best decoherence | Best joint coexistence | Notes |
|---|---|---|---|
| 25 | modular gap=2 (`pur_min 0.619`) | modular gap=4 or gap=2 | modular remains strongest at small `N` |
| 40 | central `|y|<1/2` (`pur_min ~0.735`) | central `|y|<2` (`g/SE +2.0`) | central-band clearly wins here |
| 60 | modular gap=4 (`pur_min 0.769`) | modular gap=4 (`g/SE +1.9`) | best matched modular pocket |
| 80 | modular gap=2 (`pur_min 0.852`) | central `|y|<1` (`g/SE +2.6`) | decoherence vs gravity tradeoff |
| 100 | central `|y|<2` (`pur_min 0.876`) | central-band slightly cleaner | modular gap=2 gravity turns negative |

Removal fractions are modest and stable:

- `|y-center| < 1`: about `8.5-8.6%`
- `|y-center| < 2`: about `16.2-17.2%`

## Safe interpretation

There is **no single universal winner** across the whole matched sweep.

What is established:

- imposed modular gaps are still the strongest decoherence lane at the
  smallest `N`
- central-band removal is a real competing hard-geometry lane
- central-band removal often gives cleaner positive gravity than the
  imposed modular gaps at larger `N`
- by `N=100`, central-band removal is the better balanced lane in this
  matched comparison

What is not established:

- that central-band removal dominates modular gaps at all `N`
- that any one bounded hard-geometry lane has already solved the
  asymptotic problem

## Practical conclusion

The repo should keep **both** of these as top bounded geometry lanes:

1. **imposed modular gap + layer norm**
   - strongest small-`N` decoherence
2. **simple central-band removal + layer norm**
   - simpler hard-geometry rule
   - competitive through `N=100`
   - often cleaner on the gravity side

The next clean discriminator is not another broad sweep. It is a
same-family gravity-law cleanup on the best `N=80-100` pockets from
both lanes.
