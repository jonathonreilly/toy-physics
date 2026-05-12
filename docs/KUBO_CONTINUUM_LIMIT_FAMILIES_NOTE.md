# Kubo Continuum Limit — Family Portability (Partial, Later Narrowed)

**Date:** 2026-04-07
**Status:** proposed_retained partial snapshot, later narrowed by Lane α++ — at H=0.25, Fam1=+5.986 and Fam3=+5.955 agree to 0.5%, while Fam2=+7.088 is a 12% outlier. This note still captures the pre-α++ portability snapshot. The later Fam2 H=0.20 refinement in `KUBO_FAM2_REFINEMENT_NOTE.md` (sibling artifact; cross-reference only — not a one-hop dep of this note) rejects the easy "Fam2 just needs finer H" rescue, so the current program-level read is narrower than the original 2/3-family partial positive.

## Artifact chain

- [`scripts/kubo_continuum_limit_families.py`](../scripts/kubo_continuum_limit_families.py)
- [`logs/2026-04-07-kubo-continuum-limit-families.txt`](../logs/2026-04-07-kubo-continuum-limit-families.txt)
- `docs/KUBO_FAM2_REFINEMENT_NOTE.md` (sibling artifact; cross-reference only — not a one-hop dep of this note)

## Later update

This note is retained because it is the first all-three-family snapshot at
`H = 0.25`. It is **not** the current final read on family portability.

What later changed:

- Lane α++ added Fam2 at `H = 0.20`
- Fam2 moved from `+7.0883` to `+4.5082`
- the oscillation amplitude grew from `12.2%` to `36.4%`
- the hypothesis "Fam2 just needs finer H to settle near `~5.97`" was rejected

So the current family-portability read is:

> Fam1 and Fam3 remain internally consistent near `~+5.97`; Fam2 does not
> share that behavior at the tested refinements. This note should be read as
> the pre-α++ partial snapshot, not as the current final verdict.

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
   coarse → medium DOWN, medium → fine UP — non-monotone. At the time of
   this note, that left open whether finer H would rescue the family-portability
   story.
4. **Family portability cannot be claimed here.** The 11.7% max
   deviation exceeds the 10% threshold. In the original snapshot that left
   a "two out of three" partial result. After Lane α++, even that partial read
   has to be interpreted more narrowly.

## What this does NOT establish

- **Whether Fam2's converged value is also near 5.97.** This was the key open
  question in the original snapshot. Lane α++ later made the easy rescue read
  untenable.
- **Whether kubo_true is truly a family-invariant physical quantity.**
  Two of three families suggest yes, but one does not settle.
- **The origin of the discrepancy.** It could be:
  - Fam2's smaller drift (0.05) interacting with the integer rounding
    of NL / iz_range / src_layer in a way that disrupts convergence
  - A genuine family-specific continuum value for Fam2 that differs
    from Fam1/Fam3
  - Fam2 requires a longer NL at each H (i.e., larger T_phys) to
    reach the same effective integration depth as Fam1/Fam3

## Frontier map adjustment (Update 11, historical snapshot)

| Row | Update 10 (Lane α, Fam1 only) | This lane (all 3 families) |
| --- | --- | --- |
| kubo_true continuum convergence | +5.986 on Fam1, 0.2% drift | **Fam1 still converged; Fam3 converged to +5.955 (0.5% of Fam1); Fam2 not converged (12.2% last-step drift)** |
| Family portability of kubo_true | not tested | **historical partial snapshot** — Fam1/Fam3 agree within 0.5%, Fam2 outlier at H=0.25 |
| Compact underlying principle | first-order Kubo derived (Fam1 single-family) | **historically partially portable** at H=0.25; later narrowed by α++ |

## Honest read

As a standalone H=0.25 snapshot, this was not a clean positive and not a clean
negative either. After Lane α++, it should be read as:

- **Fam1 and Fam3 agree on a converged value around +5.97** with
  0.5% consistency — this is a real result.
- **Fam2 was already unstable** in this snapshot — its non-monotone
  trajectory 6.66 → 6.32 → 7.09 flagged the problem that Lane α++ later
  sharpened into a real negative.
- The 11.7% max deviation metric was dominated by Fam2 alone.
- Without Fam2, the family-portability claim would have held at this stage.
- Lane α++ later showed that the cheap Fam2 rescue does **not** land.

## What to attack next

1. **Treat Fam1/Fam3 as the retained portability subset** and stop citing
   Fam2 as an unresolved follow-up.
2. **If this lane is extended, vary the generator itself** (for example,
   restore strength) rather than re-asking whether the already-negative Fam2
   point "just needs finer H."
3. **Use other observables** like the direct-`dM` or exact-comparator lanes
   for complementary continuum evidence.

## Bottom line

> "At H=0.25, Fam1 and Fam3 already agreed to 0.5% near `~+5.97`,
> while Fam2 was a clear outlier. That original all-family snapshot is
> retained here. The later Fam2 H=0.20 refinement then rejected the easy
> rescue story: Fam2 did not settle toward `~+5.97`, it crashed to `+4.5082`
> with growing oscillation amplitude. So the current read is narrower than
> the original '2/3 partial positive': Fam1/Fam3 remain internally consistent,
> but Fam2 does not share that behavior at the tested refinements."

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [kubo_fam2_refinement_note](KUBO_FAM2_REFINEMENT_NOTE.md)
