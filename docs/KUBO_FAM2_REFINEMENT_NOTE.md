# Fam2 Single-Family Refinement — Hard Negative

**Date:** 2026-04-07
**Status:** retained negative — Fam2 kubo_true at H=0.20 gives **+4.5082**, a 36.4% crash from H=0.25's +7.0883 and 24.5% below the Fam1/Fam3 converged value of ~5.97. The oscillation amplitude is GROWING with refinement, not shrinking. The hypothesis "Fam2 just needs finer H to converge to ~5.97" is decisively rejected. Fam2 has a genuinely different continuum behavior from Fam1/Fam3, most likely because its weak lattice pull (drift=0.05, restore=0.30) produces qualitatively different grown geometry at each H.

## Artifact chain

- [`scripts/kubo_fam2_refinement.py`](../scripts/kubo_fam2_refinement.py)
- [`logs/2026-04-07-kubo-fam2-refinement.txt`](../logs/2026-04-07-kubo-fam2-refinement.txt)

## Question

The family-portability lane
([`KUBO_CONTINUUM_LIMIT_FAMILIES_NOTE.md`](KUBO_CONTINUUM_LIMIT_FAMILIES_NOTE.md))
left one open question: is Fam2's non-monotone trajectory
(6.66 → 6.32 → 7.09 across H ∈ {0.5, 0.35, 0.25}) a sign that it
would converge to ~5.97 (like Fam1 and Fam3) at even finer H, or
is it converging to a genuinely different value?

This lane probes Fam2 at a single additional refinement point
H = 0.20 (between the previous H=0.25 and the memory-feasibility
limit) to test both possibilities.

## Setup

Same physical parameters and Kubo machinery as Lane α and Lane α+:

- T_phys = 15.0, PW_phys = 6.0, k*H = 2.5, S_phys = 0.004, z_src = 3.0
- Grown DAG with Fam2 parameters: drift=0.05, restore=0.30, seed=0
- Parallel perturbation propagator computes kubo_true at s=0
- New H=0.20 refinement point: NL=75, n_nodes=275355

## Result

Full Fam2 series across four refinements:

| H | NL | kubo_true | Δ from previous |
| ---: | ---: | ---: | ---: |
| 0.50 | 30 | +6.6588 | — |
| 0.35 | 43 | +6.3168 | **−5.1%** |
| 0.25 | 60 | +7.0883 | **+12.2%** |
| **0.20** | **75** | **+4.5082** | **−36.4%** |

Comparison to Fam1/Fam3 at H=0.25:

- Fam1: +5.9860
- Fam3: +5.9547
- Fam2 at H=0.20: **+4.5082**
- Deviation from Fam1/Fam3 target: **24.5%**

## What this rejects

The hypothesis "Fam2 is slow to converge but will settle near 5.97
at finer H" is decisively rejected. If Fam2 were approaching the
Fam1/Fam3 value, we would expect Δ(H=0.25 → H=0.20) to be smaller
than Δ(H=0.35 → H=0.25). Instead, the Δ amplitude GREW from 12.2%
to 36.4%. The oscillation is getting worse with refinement, not
damping out.

The Fam2 series is:

```
6.66  →  6.32  →  7.09  →  4.51
       -5.1%    +12.2%    -36.4%
```

This is non-monotone and divergent — the very pattern that
indicates NOT converging.

## What this does not reject

Lane α (Fam1 alone converging to +5.986 with 0.2% drift) is not
affected. Lane α+'s finding that Fam1 and Fam3 agree to 0.5% at
H=0.25 is not affected. What this lane kills is the weaker claim
that Fam2 *would* join them at finer H.

## Scientific interpretation

The three tested families have very different "lattice pull"
strengths:

| Family | drift | restore | character |
| --- | ---: | ---: | --- |
| Fam1 | 0.20 | **0.70** | strongly crystalline |
| Fam2 | 0.05 | **0.30** | **weakly crystalline** |
| Fam3 | 0.50 | **0.90** | most crystalline |

The grown-DAG generator's `restore` term is what pulls each node
back toward the integer grid after the random drift step. At
restore=0.70 (Fam1) or 0.90 (Fam3), 70–90% of each node's position
is locked to the grid and only 10–30% comes from the random-walk
contribution. At **restore=0.30** (Fam2), only 30% is locked to
the grid and **70% of the position** is determined by the
previous layer's drift trajectory.

This has a key implication: **Fam2 at different H values is not
the same physical system with a finer lattice — it is qualitatively
different geometry at each H**. The "crystalline" structure that
Fam1 and Fam3 preserve under refinement is not preserved by Fam2.
Each refinement step produces a distinctly-structured grown DAG
because the weak restore + the changing drift*H magnitude yields
a different balance.

In this reading:

- Fam1 and Fam3 have a well-defined continuum limit of `kubo_true`
  because the geometry is stable under refinement
- Fam2 does NOT have a well-defined continuum limit at these
  refinements because the geometry keeps changing qualitatively
- The family-portable continuum value (~5.97) holds on
  strongly-crystalline families, not weakly-crystalline ones

This is a meaningful distinction, not just a failure to converge:
it says the continuum-limit claim for `kubo_true` is conditional
on the generator having enough lattice pull to produce geometry-
invariant behavior across refinements.

## Frontier map adjustment (Update 13)

| Row | Update 12 (Lane α+ + Lane δ) | This lane |
| --- | --- | --- |
| kubo_true continuum limit on Fam2 | not yet settled | **explicitly DOES NOT converge** at H ∈ {0.5, 0.35, 0.25, 0.20} |
| Family portability of kubo_true | partial (Fam1/Fam3 agree, Fam2 bouncing) | **partial narrowed**: agrees on strongly-crystalline families (restore ≥ 0.70), does NOT hold on Fam2 (restore=0.30) |
| Hypothesis "Fam2 just needs finer H" | open | **REJECTED** — Fam2 oscillation amplitude grows with refinement |

## What this does NOT resolve

- Whether a 5th refinement point (H=0.15 or finer) would reveal a
  different pattern — blocked by memory / compute budget.
- Whether the "strongly crystalline" classification is the right
  one, or whether some other property of Fam2 (e.g., its smaller
  drift producing less path diversity) is the real cause.
- Whether there exists a modified family generator that would
  make Fam2's behavior converge while keeping its weak restore.

## Bottom line

> "At a new refinement point H=0.20, Fam2's kubo_true is +4.5082 — a
> 36.4% crash from H=0.25's +7.0883 and 24.5% below the Fam1/Fam3
> converged value of ~5.97. The Fam2 oscillation amplitude is
> GROWING with refinement (5.1% → 12.2% → 36.4%), not shrinking. The
> hypothesis 'Fam2 is slow to converge but will settle near 5.97
> at finer H' is decisively rejected. Fam2's weak lattice pull
> (restore=0.30, vs 0.70/0.90 for Fam1/Fam3) means its grown
> geometry is qualitatively different at each H, so there is no
> single 'continuum limit' in the same sense as Fam1/Fam3. The
> family-portable continuum value ~5.97 now holds specifically on
> strongly-crystalline families, not on weakly-crystalline Fam2.
> This narrows the claim rather than invalidating it — Lane α and
> Lane α+'s Fam1/Fam3 agreement are unaffected."
