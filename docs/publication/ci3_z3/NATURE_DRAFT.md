# Gravity, Gauge Structure, and Matter from `Cl(3)` on `Z^3`

## Abstract

We study the hypothesis that `Cl(3)` on the cubic lattice `Z^3` is the physical
theory and ask how much known physics follows from that single discrete
framework. On the retained surface of the program, the lattice yields exact
native `SU(2)` from the Clifford bivectors, a graph-first selector that fixes a
weak axis on the canonical cube-shift surface, and a structural `su(3)` closure
from the selected graph fibers plus the residual cubic swap. The same framework
supports anomaly-forced `3+1` closure on a single-clock codimension-1 theorem
surface, after which anomaly cancellation fixes the right-handed completion on
the Standard Model branch. The exact orbit algebra `8 = 1 + 1 + 3 + 3` then
supplies a retained three-generation matter structure in the same framework. We
also carry exact supporting theorems for vanishing third-order interference
(`I_3 = 0`) on the Hilbert surface and exact CPT on the free staggered lattice.
What remains open is explicit and narrower: topology / `S^3`
compactification, dark-matter relic mapping, renormalized top-Yukawa matching,
and quantitative flavor closure.

## 1. Introduction

Modern high-energy theory still lacks a compact framework that derives gravity,
gauge structure, spacetime dimension, and matter organization from one common
discrete origin. Existing approaches capture important pieces of that story, but
typically only after substantial additional structure is imposed. The program
studied here is narrower and harsher: take `Cl(3)` on `Z^3` as the physical
theory and ask which parts of known physics survive direct audit on that exact
lattice surface.

The answer is no longer a loose stack of suggestive numerics. On the current
retained surface, the framework carries exact native `SU(2)`, graph-first
structural `SU(3)`, anomaly-forced `3+1`, a full-framework one-generation
closure, and a retained three-generation matter structure. The important shift
is not merely that more lanes exist. It is that the paper can now separate its
retained theorem surface from bounded phenomenology and still remain a coherent
flagship claim.

We therefore organize the manuscript around the retained backbone only. Bounded
phenomenological bridges remain valuable, but they are not the center of the
present letter. The live attack surface is now concentrated in four explicit
bridge problems: topology / `S^3`, dark-matter relic mapping, renormalized
`y_t`, and quantitative flavor closure.

## 2. Framework

The framework sentence is simple:

> We take `Cl(3)` on `Z^3` as the physical theory. Everything else is derived.

This is the concrete working axiom of the paper. A more compressed
Hilbert/locality reduction exists in the background architecture, but the
manuscript stays on the explicit `Cl(3)` / `Z^3` surface because that is where
the strongest audited derivations live.

Several exact consequences belong to this surface immediately. The cubic
staggered construction carries the Clifford algebra natively, supports exact
native `SU(2)` through its bivectors, and lives on a physical lattice rather
than a regulator destined to be removed. On the Hilbert surface of the
framework, interference is exactly pairwise: the Sorkin parameter `I_3`
vanishes identically once amplitudes compose linearly and probabilities are
quadratic. Likewise, the free staggered lattice carries exact CPT symmetry.

These exact supporting results do not by themselves close the Standard Model.
What matters is that they sit inside the same audited discrete structure rather
than entering as separate continuum assumptions.

## 3. Gauge Structure

The first retained gauge result is exact native `SU(2)`. On the cubic lattice,
the Clifford bivectors close with the expected commutation relations and deliver
the unique native weak algebra on the retained surface.

The second retained gauge result is structural `SU(3)`, but the route matters.
The paper-safe closure is graph-first. A selector on the canonical cube-shift
surface chooses a weak axis directly on the graph. Once that axis is fixed, the
selected graph fibers carry weak `su(2)`, the residual swap of the remaining two
axes yields the `3 \oplus 1` split, and the joint commutant carries structural
`su(3) \oplus u(1)`.

That statement is stronger and cleaner than the older commutant-only language.
It means the paper can now say, without overselling, that exact native `SU(2)`
and graph-first structural `SU(3)` both arise on the retained cubic graph.
Left-handed charge matching is also retained on that selected-axis surface,
though the manuscript should continue to describe the abelian factor carefully
outside the full-framework one-generation closure.

## 4. Matter and `3+1`

The retained matter story is now full-framework, not purely spatial. The
spatial graph fixes the left-handed gauge and matter structure. The anomaly
analysis then forces a chiral completion, and the single-clock theorem surface
selects `3+1`. Once the temporal direction is derived, chirality becomes
available, and anomaly cancellation fixes the right-handed singlet completion
on the Standard Model branch. This closes one full generation at the
framework level.

The three-generation step now sits on the exact orbit algebra
`8 = 1 + 1 + 3 + 3`. In this framework the lattice is physical, not a
regulator. That matters because it blocks the old escape route in which the
triplet sectors are dismissed as disposable taste artifacts. The paper-safe
claim is therefore no longer “family-like orbit structure appears,” but rather
that the retained framework carries a three-generation matter structure.

What remains bounded in the matter/flavor sector is narrower: detailed
`1+1+1` hierarchy, the physical role of the two singlets, and quantitative CKM
closure.

## 5. Exact Supporting Theorems

Two exact companions strengthen the current manuscript surface without widening
its claims.

First, the framework carries an exact `I_3 = 0` theorem on the Hilbert surface.
This is best read as exact pairwise interference, not as a freestanding derivation
of the Born rule from nothing. The manuscript should use the more precise
interference statement.

Second, the free staggered `Cl(3)` lattice is exactly CPT invariant. That is a
clean consistency theorem worth carrying in the main text or Extended Data,
with the caveat that the full interacting extension remains a separate step.

## 6. What Remains Open

The present letter is strongest when it states the remaining gaps directly.

The first is topology. The `S^3` lane has improved materially, but the
compactification step is not yet at the paper bar.

The second is the dark-matter relic bridge. Direct lattice contact enhancement
is real, but the full relic mapping still depends on a bounded coarse-graining
story rather than a self-contained first-principles theorem.

The third is renormalized `y_t`. The bare UV theorem and `Cl(3)` preservation
under block-spin RG are strong, but the full low-energy matching chain remains
bounded.

The fourth is quantitative flavor closure. The current CKM route is still a
bounded pattern argument, not a quantitative theorem.

These are substantial problems, but they no longer erase the structural
backbone. They now define the difference between a strong flagship theory paper
and a fully closed unification paper.

## 7. Code and Reproducibility

The public-facing code and note surface for this letter should be limited to
the curated publication package on the corresponding commit. The minimal release
bundle is:

- the claims ledger in [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- the section-to-runner map in [RESULTS_INDEX.md](./RESULTS_INDEX.md)
- the exact-runner instructions in [REPRODUCE.md](./REPRODUCE.md)
- the manuscript asset map in [FIGURE_PLAN.md](./FIGURE_PLAN.md)

This keeps the public release aligned to the retained theorem surface instead
of the full internal repo chronology.

## 8. Discussion

The correct claim surface is therefore disciplined and unusually strong. On the
retained cubic graph, `Cl(3)` yields exact `SU(2)`, graph-first structural
`SU(3)`, anomaly-forced `3+1`, a full-framework one-generation Standard Model
closure, and a retained three-generation matter structure. Exact `I_3 = 0` and
exact CPT provide additional consistency theorems on the same framework
surface.

That package is already significant. It is not yet everything. The remaining
bridge problems must stay visible in the paper. But the center of gravity has
shifted: the strongest objection is no longer that the framework lacks matter
structure. It is that the topology, relic, renormalized matching, and flavor
bridges are not yet fully closed.

That is a much stronger submission posture than the program had before.
