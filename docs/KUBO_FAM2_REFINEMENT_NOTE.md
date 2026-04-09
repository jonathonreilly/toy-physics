# Fam2 Single-Family Refinement — Strong Negative on the Tested Ladder

**Date:** 2026-04-07
**Status:** retained negative on the tested ladder — Fam2 kubo_true at H=0.20 gives **+4.5082**, a 36.4% crash from H=0.25's +7.0883 and 24.5% below the Fam1/Fam3 converged value of ~5.97. The oscillation amplitude grows rather than shrinks across the tested H sequence. This strongly weakens the simple "Fam2 just needs one more refinement to settle near ~5.97" rescue story, but it does **not** prove literal divergence or rule out later settling at much finer H. The lane supports a genuinely different observed refinement behavior on Fam2 relative to Fam1/Fam3. A weaker lattice-pull story is a plausible interpretation, but the current data do **not** isolate `restore` alone because drift and restore vary together across families.

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

## What this strongly weakens

The simple near-term rescue story
"Fam2 is slow to converge but will settle near 5.97 on this tested
ladder" is not supported. If Fam2 were approaching the Fam1/Fam3
value smoothly, we would expect Δ(H=0.25 → H=0.20) to be smaller
than Δ(H=0.35 → H=0.25). Instead, the Δ amplitude GREW from 12.2%
to 36.4%. On the tested sequence, the oscillation is getting worse,
not better.

The Fam2 series is:

```
6.66  →  6.32  →  7.09  →  4.51
       -5.1%    +12.2%    -36.4%
```

This is non-monotone and still bouncing on the tested ladder.
It is enough to say "not converged here," not enough to prove
mathematical divergence.

## What this does not reject

Lane α (Fam1 alone converging to +5.986 with 0.2% drift) is not
affected. Lane α+'s finding that Fam1 and Fam3 agree to 0.5% at
H=0.25 is not affected. What this lane kills is the weaker claim
that Fam2 *would* join them at finer H.

## Scientific interpretation (inference, not isolated mechanism)

The three tested families have very different generator parameters, and
one plausible reading is that they differ in effective "lattice pull":

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

That makes the following interpretation plausible, but not yet proven:
**Fam2 may not preserve the same effective geometry under refinement in
the way the higher-restore families do.** The current data are
consistent with Fam2 producing a more H-sensitive grown DAG, but they do
not isolate whether `restore`, `drift`, or some interaction between the
two is the operative cause.

In this reading:

- Fam1 and Fam3 have a well-defined observed continuum limit of
  `kubo_true` at the tested refinements
- Fam2 is not converged on the tested H ladder
- The ~5.97 continuum value currently holds on the two higher-restore
  families tested, but not on Fam2 at these refinements

This is a meaningful distinction, not just a failure to converge:
it says the continuum-limit claim for `kubo_true` is generator-
conditional at the currently tested parameter choices. The weak-lattice-
pull reading is a leading explanation, not yet an isolated theorem.

## Frontier map adjustment (Update 13)

| Row | Update 12 (Lane α+ + Lane δ) | This lane |
| --- | --- | --- |
| kubo_true continuum limit on Fam2 | not yet settled | **not converged on the tested H ladder** H ∈ {0.5, 0.35, 0.25, 0.20} |
| Family portability of kubo_true | partial (Fam1/Fam3 agree, Fam2 bouncing) | **partial narrowed**: agrees on the two higher-restore families tested, does NOT hold on Fam2 at these refinements |
| Hypothesis "Fam2 just needs one more refinement" | open | **strongly weakened** — Fam2 oscillation amplitude grows with refinement |

## What this does NOT resolve

- Whether a 5th refinement point (H=0.15 or finer) would reveal a
  different pattern — blocked by memory / compute budget.
- Whether the higher-restore / weaker-restore reading is the right
  one, or whether some other property of Fam2 (e.g., its smaller
  drift producing less path diversity) is the real cause.
- Whether there exists a modified family generator that would
  make Fam2's behavior converge while keeping its weak restore.

## Bottom line

> "At a new refinement point H=0.20, Fam2's kubo_true is +4.5082 — a
> 36.4% crash from H=0.25's +7.0883 and 24.5% below the Fam1/Fam3
> converged value of ~5.97. The Fam2 oscillation amplitude grows
> with refinement on the tested ladder (5.1% → 12.2% → 36.4%), so
> Fam2 is still bouncing rather than settling at H ∈ {0.5, 0.35,
> 0.25, 0.20}. This strongly weakens the easy near-term rescue story,
> but it does not by itself prove literal divergence or rule out
> later settling at much finer H. Fam2 shows a genuinely different
> observed refinement behavior from Fam1/Fam3 at the tested H values.
> A weaker-lattice-pull explanation is plausible, but the current data
> do not isolate `restore` alone because drift and restore co-vary.
> The ~5.97 continuum value currently holds on Fam1/Fam3 and not on
> Fam2 at these refinements. This narrows the claim rather than
> invalidating it — Lane α and Lane α+'s Fam1/Fam3 agreement are
> unaffected."
