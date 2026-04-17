# Persistent Record Overlap Kernel Note

**Date:** 2026-04-03  
**Status:** bounded positive pilot, not asymptotic closure

## Purpose

Test a concrete version of the "graph split creates parallel universes, but
some persistent connection remains" idea.

The pilot does **not** treat different branch records as instantly orthogonal.
Instead:

- each path writes to a **mesoscopic persistent record state**
- record state is a sparse count vector over post-barrier worldtube cells
- detector reduction uses a soft overlap kernel

```text
K(r, r') = exp(-gamma * ||r - r'||^2)
```

So:

- `gamma = 0` is the fully coherent limit
- larger `gamma` weakens branch-to-branch connection
- exact trace over record labels is the fully orthogonal limit for this record model

This is meant to sit between:

- deterministic bookkeeping labels that converge too hard, and
- highly branched orthogonal environments that spread amplitude too thinly

## Implemented pilot

- Script:
  [persistent_record_overlap_kernel.py](/Users/jonreilly/Projects/Physics/scripts/persistent_record_overlap_kernel.py)
- Log:
  [2026-04-03-persistent-record-overlap-kernel.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-03-persistent-record-overlap-kernel.txt)

Default run:

- generated causal DAG barrier setup
- `N = 8, 12, 18`
- `3` seeds
- `k`-band `[3, 5, 7]`
- record grid: `5` `y` bins × `3` direction bins
- per-cell persistent count cap `= 2`
- overlap kernel sweep: `gamma = 0.25, 1.0`

## Result

Mean purities:

| N | `pur_trace` | `pur_g0.25` | `pur_g1.0` | mean overlap `ov_g0.25` | mean overlap `ov_g1.0` |
|---|---:|---:|---:|---:|---:|
| 8  | 0.8317 | 0.9556 | 0.8672 | 0.7216 | 0.3836 |
| 12 | 0.6898 | 0.8744 | 0.7398 | 0.7315 | 0.4763 |
| 18 | 0.8237 | 0.9058 | 0.8126 | 0.6253 | 0.3596 |

Power-law fits on `(1 - pur)` over the bounded `N = 8, 12, 18` run:

- trace: `(1 - pur) ~ 0.182 * N^+0.057`
- `gamma = 0.25`: `(1 - pur) ~ 0.00802 * N^+0.929`
- `gamma = 1.0`: `(1 - pur) ~ 0.0648 * N^+0.425`

## Interpretation

The pilot is **interesting**, but not yet decisive.

Positive:

- the exact-trace version of this record model gives materially stronger mixing
  than the earlier entangling / substrate-memory lanes on the same size range
- the soft-kernel versions keep a real residual branch connection while still
  producing nontrivial decoherence
- detector-weighted branch overlap stays well above zero, so this is not just a
  relabeled orthogonal-environment model

Constraint:

- the strongest row is still the bounded `N = 12` pocket
- `N = 18` rebounds, so the present run does **not** justify an asymptotic
  "problem solved" claim

## Safe wording

The retained safe read is:

- a **mesoscopic persistent-record overlap kernel** is a scientifically live new
  lane
- it behaves better than several earlier record architectures on the bounded
  `N = 8, 12, 18` probe
- but it is still only a **bounded positive pilot**

## Next useful steps

1. Stress-test whether the `N = 12` pocket survives a wider seed count.
2. Profile and compress the `N = 25` row rather than treating it as a free
   extension of the small-`N` default.
3. Compare this worldtube-count kernel directly against node-label,
   graph-scar, and entangling-env baselines on a matched seed slice.
4. Try one slightly richer record geometry:
   same mesoscopic counts, but add one packet-side or slit-side persistence bit
   instead of increasing raw state cardinality broadly.
