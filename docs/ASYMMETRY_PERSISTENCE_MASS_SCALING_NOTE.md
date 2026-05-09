# Asymmetry Persistence Mass Scaling Note

**Date:** 2026-04-02  
**Status:** dense fixed-anchor follow-up complete

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/asymmetry_persistence_mass_scaling.py` previously timed out under the audit-lane 120s default budget; AUDIT_TIMEOUT_SEC=1800 has been declared and the cache refreshed under the new budget. The runner output and pass/fail semantics are unchanged.

## Question

The generated asymmetry-persistence lane now has a real same-graph joint
card through dense `N=100`.

The next gravity-side question was narrower:

- does generated hard geometry improve the **mass-response window**
- or does it merely preserve a positive mean gravity signal

## Setup

Script:
[scripts/asymmetry_persistence_mass_scaling.py](/Users/jonreilly/Projects/Physics/scripts/asymmetry_persistence_mass_scaling.py)

Log:
[logs/2026-04-02-asymmetry-persistence-mass-scaling.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-02-asymmetry-persistence-mass-scaling.txt)

Protocol:

- dense generated 3D graphs
- `N=100`
- `npl=60`
- `8` matched seeds
- thresholds `0.00, 0.10, 0.20`
- fixed anchor `y = center + 6`
- fixed ordered mass candidates on the gravity layer
- varying `M` takes prefixes of that same ordered set
- fixed post-barrier mid-mass support is held constant

Mass values:

- `M = 1, 2, 3, 5, 8, 12`
- fit window declared in advance on `M in {2,3,5,8}`

## Results

### Baseline generated geometry (`thr = 0.00`)

- linear fit:
  - `delta ~= 0.8508 * M^0.101`
  - `R^2 = 0.592`
- layernorm fit:
  - `delta ~= 0.2098 * M^0.453`
  - `R^2 = 0.875`

Interpretation:
- the linear mass response is almost flat
- the layernorm lane already shows a clearer positive sublinear window

### Persistence threshold `0.10`

- linear fit:
  - `delta ~= 0.7144 * M^0.281`
  - `R^2 = 0.914`
- layernorm fit:
  - `delta ~= 0.4032 * M^0.420`
  - `R^2 = 0.970`

Interpretation:
- generated persistence turns the flat linear response into a cleaner
  positive sublinear mass window
- on the layernorm lane, it preserves a strong positive sublinear trend
  with the cleanest fit of the sweep

### Persistence threshold `0.20`

- linear fit:
  - `delta ~= 0.7403 * M^0.237`
  - `R^2 = 0.950`
- layernorm fit:
  - `delta ~= 0.5332 * M^0.262`
  - `R^2 = 0.892`

Interpretation:
- the stronger threshold still keeps a positive sublinear mass window
- but it does not improve the exponent relative to the `0.10` row

## Safe conclusion

Generated hard geometry helps the **mass window**, but it does not solve
the mass law.

What is retained:

- on dense `N=100` generated graphs, persistence sharpens the mass
  response relative to the baseline generated geometry
- the cleanest retained row is the `thr = 0.10` layernorm lane
- the mass response is positive and sublinear, with strong fit quality

What is not retained:

- exact `F ∝ M`
- a Newtonian mass law on the generated hard-geometry lane

## Bottom line

Generated asymmetry persistence is now doing something meaningful on the
gravity side too:

- it repairs a nearly flat mass response into a clearer positive window
- but the response remains **sublinear**

So this lane now looks like:

1. real bounded joint coexistence through dense `N=100`
2. improved gravity mass response relative to the baseline generated lane
3. still missing a review-safe exact force law
