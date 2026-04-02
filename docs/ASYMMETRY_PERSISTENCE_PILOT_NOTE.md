# Asymmetry Persistence Pilot Note

Date: 2026-04-02

## Purpose

This note records the first bounded **generated hard-geometry** result based on
topological asymmetry.

Earlier topological asymmetry results were post-hoc:
- build a graph
- measure slit-path asymmetry
- prune low-asymmetry nodes

This pilot moves one step closer to a true geometry rule:
- build the graph layer by layer
- after the barrier, maintain slit-conditioned path counts
- in an early post-barrier persistence band, reject candidate nodes whose
  asymmetry is too low

That makes the geometry itself emerge during construction rather than being
edited afterward.

## Script

- [asymmetry_persistence_pilot.py](/Users/jonreilly/Projects/Physics/scripts/asymmetry_persistence_pilot.py)

## Rule

For a candidate post-barrier node:

- `count_A` = number of retained paths from upper-slit nodes into the candidate
- `count_B` = number of retained paths from lower-slit nodes into the candidate
- `asym = |count_A - count_B| / (count_A + count_B)`

If the candidate lies in the first post-barrier persistence band and
`asym < threshold`, the candidate does not persist.

This is still a bounded toy rule, not yet a strict axiom-level local law,
because the slit-conditioned counts are global-to-date rather than purely local.

## Sparse baseline runs

Default sparse setting:
- `npl=30`
- `xyz_range=12`
- `connect_radius=4.0`

Results:

### N = 40

- baseline:
  - `pur_cl = 0.990 ± 0.004`
  - `gravity = +0.893 ± 0.401`
- threshold `0.10`:
  - `pur_cl = 0.910 ± 0.024`
  - `gravity = +1.026 ± 0.511`
  - keep rate `94.6%`
- threshold `0.20`:
  - `pur_cl = 0.910 ± 0.024`
  - `gravity = +0.994 ± 0.548`
  - keep rate `94.5%`

### N = 60

- baseline:
  - `pur_cl = 0.968 ± 0.012`
  - `gravity = -0.025 ± 0.387`
- threshold `0.10`:
  - `pur_cl = 0.939 ± 0.020`
  - `gravity = -0.360 ± 0.261`
  - keep rate `96.0%`
- threshold `0.20`:
  - `pur_cl = 0.934 ± 0.021`
  - `gravity = -0.401 ± 0.272`
  - keep rate `95.8%`

### N = 80

- sparse setting fails for all rows (`0` valid seeds)

Interpretation:
- the mechanism is real at `N=40`
- at sparse `N=60`, decoherence improves but gravity softens
- sparse `N=80` is a graph-density failure, not yet a mechanism verdict

## Dense follow-up runs

### N = 80, dense

Setting:
- `npl=50`
- `8 seeds`

Results:

- baseline:
  - `pur_cl = 0.989 ± 0.004`
  - `gravity = -0.386 ± 0.767`
- threshold `0.10`:
  - `pur_cl = 0.961 ± 0.014`
  - `gravity = +0.756 ± 0.956`
  - keep rate `97.4%`
- threshold `0.20`:
  - `pur_cl = 0.956 ± 0.015`
  - `gravity = +0.612 ± 0.810`
  - keep rate `97.2%`

Interpretation:
- the generated hard-geometry rule survives dense `N=80`
- it improves decoherence and flips the mean gravity sign positive

### N = 100, dense

Setting:
- `npl=60`
- `6 seeds`

Results:

- baseline:
  - `pur_cl = 0.978 ± 0.013`
  - `gravity = +2.269 ± 1.227`
- threshold `0.10`:
  - `pur_cl = 0.932 ± 0.039`
  - `gravity = +1.716 ± 0.784`
  - keep rate `97.9%`
- threshold `0.20`:
  - `pur_cl = 0.921 ± 0.043`
  - `gravity = +2.102 ± 0.825`
  - keep rate `97.7%`

Interpretation:
- the generated hard-geometry rule survives dense `N=100`
- decoherence improves substantially
- gravity stays positive on the retained valid seeds

## Safe conclusion

This is the first strong result in the repo where a **generated geometry rule**
rather than post-hoc pruning creates a useful decoherence lane:

- it is topology-native
- it removes only a small fraction of candidate nodes (`~2–5%` at dense
  `N=80–100`)
- it survives to dense `N=100`
- and it does not obviously destroy gravity on that dense lane

## Limits

- this is still a bounded pilot, not an asymptotic rescue
- the rule is not yet a strict local axiom-level law
- sparse graphs still fail
- the same-graph gravity story is promising but not yet hardened into a full
  joint reviewer card

## Why it matters

This is the best current evidence that **hard geometry generation**, not just
repair or regulation, is still a live science frontier for the project.
