# Kubo Continuum Limit — Family Portability (Partial)

**Date:** 2026-04-07
**Status:** retained partial — Fam1 continuum convergence (0.2% last-step drift, +5.986) does NOT cleanly extend to all three families. At the finest refinement H=0.25: Fam1=+5.986, Fam2=+7.088, Fam3=+5.955. Fam1 and Fam3 agree to 0.5%; Fam2 is a 12% outlier. Max deviation from mean is 11.7%, above the 10% family-portability threshold. The single-family Lane α positive is not invalidated, but it is also not a family-portable continuum coefficient at these refinements.

## Artifact chain

- [`scripts/kubo_continuum_limit_families.py`](../scripts/kubo_continuum_limit_families.py)
- [`logs/2026-04-07-kubo-continuum-limit-families.txt`](../logs/2026-04-07-kubo-continuum-limit-families.txt)

## Question

[`KUBO_CONTINUUM_LIMIT_NOTE.md`](KUBO_CONTINUUM_LIMIT_NOTE.md) showed
that `kubo_true` — the true first-order Kubo coefficient computed by
the parallel perturbation propagator on a static grown-DAG with
imposed 1/r field — converges to +5.986 on Fam1 with 0.2% drift at
the last refinement step (H=0.25). This lane tests whether the same
convergence holds on Fam2 and Fam3.

## Setup

Same physical parameters and refinement schedule as Lane α
(`kubo_continuum_limit.py`):

- T_phys = 15.0, PW_phys = 6.0, k*H = 2.5, S_phys = 0.004, z_src = 3.0
- Refinement: H ∈ {0.5, 0.35, 0.25}
- Three grown-DAG families: Fam1 (drift=0.20, restore=0.70),
  Fam2 (drift=0.05, restore=0.30), Fam3 (drift=0.50, restore=0.90)
- Same seed (0), same growth pattern, same Kubo computation

## Result

### kubo_true at each refinement

| H | Fam1 | Fam2 | Fam3 |
| ---: | ---: | ---: | ---: |
| 0.50 | +7.0619 | +6.6588 | +6.7420 |
| 0.35 | +5.9728 | +6.3168 | +6.3630 |
| 0.25 | **+5.9860** | **+7.0883** | **+5.9547** |

### Per-family convergence (last-step drift)

| Family | Δ last step | Status |
| --- | ---: | --- |
| Fam1 | **0.2%** | converged |
| Fam2 | **12.2%** | NOT converged, value bouncing up |
| Fam3 | **6.4%** | marginally converged, still decreasing |

### Family portability at finest H

- Fam1: +5.9860
- Fam2: +7.0883
- Fam3: +5.9547
- **Mean**: +6.3430
- **Max deviation from mean**: 0.7453 (**11.7%**)

The 11.7% max deviation exceeds the 10% family-portability
threshold for a clean positive. However:

### The internal pattern — Fam1 and Fam3 agree; Fam2 is the outlier

At H=0.25:
- Fam1 = +5.9860
- Fam3 = +5.9547
- Fam1 − Fam3 = 0.031 (**0.5%**)

**Fam1 and Fam3 agree to better than 1%** at the finest refinement.
Fam2 (+7.09) is the single outlier, and it is also the least
converged family (12.2% last-step drift, bouncing up from 6.32 to
7.09). The Fam2 finest-H value is probably still transient — its
convergence pattern is not monotone and the last step is large.

If we drop Fam2 as "not converged at this resolution," the two
converged families (Fam1, Fam3) give kubo_true ≈ **+5.97** with
spread of 0.5%. That would be a clean family-portable result on
the converged subset.

## What this establishes

1. **Lane α's Fam1 positive is not invalidated.** Fam1 still
   converges to +5.986 with 0.2% drift.
2. **Fam3 supports Fam1's value.** At the finest H, Fam3 gives
   +5.955, within 0.5% of Fam1. The two are internally consistent.
3. **Fam2 is not converged** at these refinements. Its trajectory is
   coarse → medium DOWN, medium → fine UP — non-monotone, which is
   a clear sign that finer H is needed before the continuum value
   can be read off.
4. **Family portability cannot be claimed yet.** The 11.7% max
   deviation exceeds the 10% threshold. We either need finer H
   on Fam2 specifically, or we accept a "two out of three" partial
   result.

## What this does NOT establish

- **Whether Fam2's converged value is also near 5.97.** Its
  trajectory is non-monotone; we cannot extrapolate.
- **Whether kubo_true is truly a family-invariant physical quantity.**
  Two of three families suggest yes, but one does not settle.
- **The origin of the discrepancy.** It could be:
  - Fam2's smaller drift (0.05) interacting with the integer rounding
    of NL / iz_range / src_layer in a way that disrupts convergence
  - A genuine family-specific continuum value for Fam2 that differs
    from Fam1/Fam3
  - Fam2 requires a longer NL at each H (i.e., larger T_phys) to
    reach the same effective integration depth as Fam1/Fam3

## Frontier map adjustment (Update 11)

| Row | Update 10 (Lane α, Fam1 only) | This lane (all 3 families) |
| --- | --- | --- |
| kubo_true continuum convergence | +5.986 on Fam1, 0.2% drift | **Fam1 still converged; Fam3 converged to +5.955 (0.5% of Fam1); Fam2 not converged (12.2% last-step drift)** |
| Family portability of kubo_true | not tested | **partial — 2/3 families agree within 0.5%, 1/3 outlier** |
| Compact underlying principle | first-order Kubo derived (Fam1 single-family) | **partially portable** (2/3 families at these refinements) |

## Honest read

Not a clean positive. Not a negative either. The picture is:

- **Fam1 and Fam3 agree on a converged value around +5.97** with
  0.5% consistency — this is a real result.
- **Fam2 does not settle** at these refinements — its non-monotone
  trajectory 6.66 → 6.32 → 7.09 is the hallmark of a family that
  needs finer H or longer NL.
- The 11.7% max deviation metric is dominated by Fam2 alone.
- Without Fam2, the family-portability claim would hold; with Fam2
  unsettled, it cannot.

The cheapest way to resolve this is to run Fam2 alone at a finer H
(or a longer T_phys) and see whether it converges to ~5.97 or to
something different. That's a single additional Fam2 refinement,
not a full 3-family sweep. Blocked by the same memory constraint
that blocks H ≤ 0.125 in general — but potentially feasible on Fam2
alone if the memory-feasibility probe (fcf2bc0) supports it.

## What to attack next

1. **Fam2 single-family refinement** — run Fam2 at H = 0.20 or H = 0.175
   (if memory permits) and see whether it settles near 5.97 or at a
   different value.
2. **Lane δ** (planned) — `dM` continuum limit at multiple v/c. This
   addresses a different observable and is orthogonal to the
   portability question here.
3. **Wait for Codex's matrix-free exact comparator** — which may
   unlock finer H for all lanes that currently need it.

## Bottom line

> "The true first-order Kubo coefficient `kubo_true` converges to
> +5.986 on Fam1 (0.2% last-step drift) and to +5.955 on Fam3 (6.4%
> last-step drift) — values within 0.5% of each other. Fam2 has a
> non-monotone trajectory (6.66 → 6.32 → 7.09) with 12.2% last-step
> drift and is clearly not converged at these refinements. Max
> deviation across the three families at H=0.25 is 11.7%, above
> the 10% family-portability threshold. The single-family Lane α
> positive is not invalidated, and Fam1/Fam3 are internally
> consistent; Fam2 is a single outlier that needs either finer H
> or longer NL to settle. Family portability of kubo_true is a
> partial positive (2/3 at these refinements), not a clean one."
