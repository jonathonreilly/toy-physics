# DM Leptogenesis Exact-Kernel Closure (claim narrowed 2026-05-01)

**Date:** 2026-04-15 (eta benchmark corrected 2026-05-01)
**Status:** bounded - exact source-and-CP-channel package closed; exact-kernel eta closure does NOT land at percent-level on the consistent benchmark
**Script:** `scripts/frontier_dm_leptogenesis_exact_kernel_closure.py`

## Framework sentence

In this note, "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

After the refreshed branch closes

- `c_odd = +1`
- `v_even = (sqrt(8/3), sqrt(8)/3)`
- `a_sel = 1/2`
- `tau_E = tau_T = 1/2`
- `K00 = 2`

what does the standard coherent leptogenesis kernel predict on the
retained benchmark?

## Bottom line (corrected)

The exact source-and-CP-channel package is closed. The exact coherent
heavy-basis kernel sits just below the Davidson-Ibarra ceiling. **But the
predicted baryon asymmetry on the consistent retained benchmark is
`eta/eta_obs ≈ 0.558`, not `0.99` as an earlier draft of this note claimed.**

The earlier `0.9907` figure was obtained with `K00 = 2` used in the
epsilon_1 numerator but **not** propagated into the washout coefficient
`K`. Once `K00 = 2` is used consistently — i.e. K is doubled when the
source includes the `K00 = 2` normalization — the washout efficiency
`kappa` halves and `eta/eta_obs` drops to `0.5579`. The runner's `[D]`
classified-pass line states this explicitly:

> The retained-fit benchmark no longer lands near observation once K00 is
> used consistently in the washout path.

So the percent-level eta closure earlier claimed in this note **does not
hold**. What does survive is everything upstream of the eta calculation:
the source package, the epsilon_1 / DI ratio, and the strong-washout
regime classification.

## Exact source-side kernel package (UNCHANGED)

The refreshed branch fixes

- odd source: `gamma = 1/2`
- even responses: `E1 = sqrt(8/3)`, `E2 = sqrt(8)/3`
- heavy-basis diagonal: `K00 = 2`

so the exact heavy-basis CP tensor channels are

- `cp1 = -2 gamma E1 / 3 = -0.544331...`
- `cp2 =  2 gamma E2 / 3 =  0.314270...`

These are exact numbers from the source package. They are not in dispute.

## Exact epsilon law (UNCHANGED)

The coherent heavy-basis kernel is

`epsilon_1 = |(1/8pi) y0^2 (cp1 f23 + cp2 f3) / K00|`.

With the exact source package and the staircase benchmark
(`k_A = 7`, `k_B = 8`, `eps/B = alpha_LM/2`),

- `epsilon_1 = 2.4576198796e-6`
- `epsilon_DI = 2.6493795301e-6`
- `epsilon_1 / epsilon_DI = 0.9276209209`.

So the exact kernel sits just below the DI ceiling, not far below it.
This part is correct.

## Exact eta on the retained benchmark (CORRECTED)

Using the same retained washout law but propagating `K00 = 2` consistently
into the washout path:

- `K = 47.236...`     (was `23.618...` in the earlier inconsistent draft)
- `kappa = 1.427e-2`  (was `2.534e-2`)
- `eta = 3.414e-10`   (was `6.063e-10`)
- `eta_obs = 6.12e-10`
- `eta / eta_obs = 0.5579` (was `0.9907`)

So the exact kernel under-shoots observation by ~44% on this benchmark.
The previously claimed percent-level closure was an artifact of a
bookkeeping inconsistency that gave `K00 = 2` to the source while
keeping `K00 = 1` in the washout. The runner now uses `K00 = 2` in
both places.

## Consequence

This **does not** resolve the old DM denominator suppression at percent
level on the refreshed branch. What is now established:

- The exact source package is closed (axiomatic, sharp numbers).
- The exact coherent kernel does not have an obvious order-of-magnitude
  problem: it is within a factor of two of observation on the retained
  benchmark, and within ~7% of the Davidson-Ibarra ceiling at the
  epsilon_1 level.
- Closing the remaining ~44% gap to observation requires either a
  refinement of the washout benchmark beyond the current retained
  staircase, or an additional source contribution not in the current
  exact heavy-basis package, or both.

## Scope

This note's substantive content is:

(i)   the exact source-and-CP-channel package, and
(ii)  the exact `epsilon_1 / epsilon_DI = 0.928` ratio.

Both (i) and (ii) are PASS in the runner. The headline `eta/eta_obs ≈ 1`
percent-level closure is **not** retained; the runner's classified-pass
output confirms `eta/eta_obs ≈ 0.558`. The note no longer claims percent-
level eta closure on this benchmark.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_exact_kernel_closure.py
```
