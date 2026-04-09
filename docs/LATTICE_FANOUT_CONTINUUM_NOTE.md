# Fan-Out Normalized Kernel Continuum Limit — FALSIFIED

**Date:** 2026-04-08
**Status:** retained NEGATIVE — replacing the default `spacing²` kernel factor with fan-out normalization (each edge carries amplitude/√fan_out) does NOT give a continuum limit. Probability is not preserved across refinements, h=0.5 fails outright, and h=0.25 overflows by 10¹¹ in amplitude. This was Approach 3 from [`humble-puzzling-spring.md`](../.claude/plans/humble-puzzling-spring.md); it is now removed from the candidate pool.

## Artifact chain

- [`scripts/lattice_fanout_continuum.py`](../scripts/lattice_fanout_continuum.py)
- [`logs/2026-04-08-lattice-fanout-continuum.txt`](../logs/2026-04-08-lattice-fanout-continuum.txt)

## The scheme

The plan's Approach 3: replace the per-edge kernel from

```
ea = exp(i·k·act) · w / L · spacing²          (default, lattice_continuum_limit.py)
```

with

```
ea = exp(i·k·act) · w / (L · sqrt(fan_out[i]))     (fan-out normalized)
```

where `fan_out[i]` is the number of outgoing edges from node i. The theoretical
argument: if each outgoing edge carries amplitude `amp/√fan_out`, the sum of
|edge|² over the fan-out equals |amp|² (before the 1/L and w weights kick in),
so total outgoing amplitude norm is preserved per node regardless of fan-out.
This is still strictly linear in amplitudes.

## Result

| h | nodes | gravity | k=0 | MI | d_TV | max\|A\| | P_total |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2.0 | 441 | −0.9844 | 0 | 0.432 | 0.654 | 1.0e+0 | **4.2e−17** |
| 1.0 | 1681 | +0.1355 | 0 | 0.495 | 0.759 | 1.0e+0 | **1.5e−23** |
| 0.5 | — | — | — | — | — | — | **FAIL** |
| 0.25 | 25921 | −0.2692 | 0 | 0.999 | 1.000 | **2.4e+11** | **4.6e+23** |

**All three failure modes fire simultaneously:**

1. **Probability is not conserved**: P_total ranges from 1e−23 to 1e+23 across
   refinements — a 46-order-of-magnitude swing. A physically valid propagator
   must keep `Σ |amp_det|²` order unity (or at least bounded).
2. **h=0.5 fails outright** (likely numerical zero division or overflow inside
   a single measurement).
3. **h=0.25 overflows by 10¹¹** in amplitude — worse than the original
   unnormalized kernel the plan was trying to fix.
4. **Gravity sign flips** between every refinement (−0.98 → +0.14 → −0.27).

## Why it fails

The argument "amplitude/√fan_out preserves outgoing norm" only holds when the
edge carries a pure `amp/√fan_out` with no further weighting. But the real
kernel multiplies by `w/L`, and 1/L = 1/spacing for forward edges. At h=0.25,
`1/L` contributes a factor 4× larger than at h=1.0, and `√fan_out` grows like
`√(1/h)` because fan_out ∝ (2·MAX_DY_PHYS/h+1) ∝ 1/h. The net per-edge
amplitude ≈ 1/(L·√fan_out) ≈ 1/(h·√(1/h)) = 1/√h, which DIVERGES as h→0.

In other words: fan-out normalization doesn't cancel the 1/L blowup because
fan-out only grows like √(1/h) while 1/L grows like 1/h. The math of the
proposed normalization simply doesn't match the kernel's actual h-scaling.

The default lattice_continuum_limit.py's `spacing²` hack works precisely
because it picks up the two powers of h needed: one for the 1/L blowup and
one for the fan-out's (1/h) count.

## What this rules out

- Fan-out normalization as a continuum-limit recipe for this kernel
- Any claim that "linear edge normalization by √branch_count" is sufficient
  for Born-clean refinement — the branch count's h-scaling is the wrong power

## What remains from the plan

From [`humble-puzzling-spring.md`](../.claude/plans/humble-puzzling-spring.md):

1. **Approach 1 (nearest-neighbor-only edges)** — already done in prior sessions,
   Born-clean through h=0.25, blocked at h=0.125 by runtime cost (see
   [`LATTICE_NN_HIGH_PRECISION_NOTE.md`](LATTICE_NN_HIGH_PRECISION_NOTE.md)).
2. **Approach 2 (k_eff = k·h coupling renormalization)** — still open, cheaper
   than Approach 3, preserves dense connectivity.
3. **Approach 3 (fan-out normalization)** — **FALSIFIED by this note.**

## Frontier map adjustment (Update 19)

| Row | Before | Fan-out falsification |
| --- | --- | --- |
| Continuum-limit candidate pool | {NN (blocked), k_eff (open), fan-out (open)} | **{NN (blocked), k_eff (open)}** |
| Approaches retired | 0 | 1 |

## Bottom line

> "The fan-out normalized kernel exp(i·k·act)·w/(L·√fan_out) does not give
> a continuum limit. Probability P_total swings across 46 orders of
> magnitude between h=2 and h=0.25, h=0.5 fails outright, and h=0.25
> overflows amplitudes by 10¹¹. The underlying reason: fan-out grows
> like 1/h while 1/L also grows like 1/h, so per-edge amplitude scales
> like 1/√h which still diverges. The √fan_out factor is the wrong
> power to cancel the 1/L blowup. Approach 3 from the continuum-limit
> plan is removed from the candidate pool. Only Approach 2 (k_eff = k·h)
> remains untried."
