# Physics from `Cl(3)` on `Z^3`

## Abstract

We present the current retained theorem surface of the `Cl(3)` on `Z^3`
framework. The main claim is not that every phenomenological lane is already
closed, but that a nontrivial structural backbone now survives direct audit on
one discrete theory: exact native `SU(2)`, graph-first structural `SU(3)`,
anomaly-forced `3+1`, a full-framework one-generation Standard Model closure,
and a retained three-generation matter structure. We also record exact
supporting theorems for vanishing third-order interference (`I_3 = 0`) on the
Hilbert surface and exact CPT on the free staggered lattice. We separate these
retained results from bounded phenomenology and from four still-live bridge
problems: `S^3` compactification, dark-matter relic mapping, renormalized
top-Yukawa matching, and quantitative flavor closure. The purpose of this draft
is to provide a coherent arXiv surface aligned to the audited repo state and
backed by reproducible runners.

## 1. Introduction

This manuscript is an arXiv-length companion to the flagship Nature-style
letter. Its job is different. The letter should carry the strongest retained
backbone. This version should make the theorem stack explicit, record the
bounded phenomenology honestly, and preserve the negative results that prevent
overclaiming.

The guiding framework sentence is:

> We take `Cl(3)` on `Z^3` as the physical theory. Everything else is derived.

That sentence should not be confused with a claim that every downstream bridge
is already finished. The correct reading is that the paper’s retained backbone
now lives on this exact discrete surface, while bounded and open lanes are
reported with their actual status.

## 2. Retained Framework Surface

The retained core contains five main layers.

### 2.1 Exact native `SU(2)`

The cubic `Cl(3)` bivectors close exactly into the weak algebra. This is the
strongest native gauge result on the framework surface and no longer depends on
review-only phenomenology.

### 2.2 Graph-first structural `SU(3)`

The current safe `SU(3)` statement is graph-first. A selector on the canonical
cube-shift surface chooses a weak axis directly on the graph. On that selected
surface, the fibers plus residual cubic swap yield the `3 \oplus 1` split and
the commutant carries structural `su(3) \oplus u(1)`.

This point matters because it replaces older, looser commutant language with a
cleaner closure path tied to the graph itself.

### 2.3 Anomaly-forced `3+1`

The spatial graph by itself fixes the left-handed surface but does not provide
chirality. The anomaly-forces-time theorem closes the `3+1` lane on the
single-clock codimension-1 surface: chirality requires even total dimension,
while multi-time continuations conflict with the framework’s one-clock state
semantics. The safe statement is that the framework selects `3+1`, not merely
“minimal odd time.”

### 2.4 Full-framework one-generation closure

Once the temporal direction is derived, chirality becomes available. The
spatial graph fixes the left-handed gauge and matter structure, and anomaly
cancellation fixes the right-handed singlet completion on the Standard Model
branch. That is the current paper-safe one-generation claim.

### 2.5 Three-generation matter structure

The exact orbit algebra `8 = 1 + 1 + 3 + 3` remains central. On the present
framework surface, the lattice is treated as physical rather than as a
regulator. Within that framework, the three-generation matter structure is now
retained. What remains bounded is the detailed hierarchy and flavor data, not
the existence of three species itself.

## 3. Exact Supporting Theorems

### 3.1 Exact `I_3 = 0`

The retained exact statement is that third-order interference vanishes
identically once amplitudes add linearly and probabilities are quadratic on the
Hilbert surface. This should be carried as an exact `I_3 = 0` theorem, not as
a loose claim that the entire Born rule has been derived from scratch.

### 3.2 Exact CPT

The free staggered `Cl(3)` lattice is exactly CPT invariant. This is a clean
finite-lattice theorem and a useful structural consistency check. The open part
is extension to the full interacting sector, not the free theorem itself.

## 4. Bounded but Important Lanes

The following lanes raise the paper ceiling but remain bounded at the current
bar.

### 4.1 `S^3` topology / compactification

The cap-map uniqueness attacks and related topology notes materially narrow the
gap. The current safe reading is that the topology lane is stronger, not that
`S^3` is fully forced.

### 4.2 Dark matter

The direct lattice contact-enhancement story is now real and significantly
stronger than before. The remaining issue is not the existence of a useful
Sommerfeld-like structural effect, but the full relic mapping from the graph
framework to cosmological abundance.

### 4.3 Renormalized `y_t`

The bare UV theorem and `Cl(3)` preservation under block-spin RG are strong
positive results. The missing step remains the low-energy matching chain and
its imported continuum-running structure.

### 4.4 Flavor and CKM

The current flavor work gives bounded route-pruning and obstruction notes, not
yet a quantitative CKM theorem.

## 5. Negative Results That Matter

This program is stronger when it keeps its negative results visible.

- generation hierarchy is not closed just because a modeled `1+1+1` split can
  be written down
- the topology lane is not closed just because cap attacks look plausible
- the DM lane is not closed just because coarse-graining looks physically
  reasonable
- the renormalized `y_t` lane is not closed just because one RG sub-theorem
  lands

These negatives are not a weakness in the arXiv version. They are part of what
makes the retained backbone credible.

## 6. Reproducibility Surface

The arXiv version should point directly to:

- the publication state document
- the claims table
- the results index
- the reproduce guide
- the paired note+runner artifacts for each retained theorem

That repo surface now exists in `docs/publication/ci3_z3/` and should be the
only public-facing navigation layer used in the paper.

## 7. Submission and Release Workflow

The arXiv version should be assembled from the same curated package as the
letter, not from ad hoc note selection. The working release documents are:

- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [RESULTS_INDEX.md](./RESULTS_INDEX.md)
- [REPRODUCE.md](./REPRODUCE.md)
- [SUBMISSION_CHECKLIST.md](./SUBMISSION_CHECKLIST.md)
- [FIGURE_PLAN.md](./FIGURE_PLAN.md)

That package should be pinned to one commit hash before public release.

## 8. Manuscript Strategy

The clean split is:

- Nature version:
  - retained backbone only
  - four gates stated openly
- arXiv version:
  - retained backbone
  - exact supporting theorems
  - bounded phenomenology
  - negative and obstruction notes

This avoids the old problem where the paper oscillated between an overclaim
stack and an underconfident outline.

## 9. Conclusion

The current state of the project is stronger than a “promising discrete toy
model,” but not yet a fully closed unification paper. The retained backbone is
real and unusually broad: exact native `SU(2)`, graph-first structural `SU(3)`,
anomaly-forced `3+1`, a full-framework one-generation Standard Model closure,
and a retained three-generation matter structure. Exact `I_3 = 0` and exact
CPT add further support on the same framework surface.

The remaining bridge problems are explicit. They should stay explicit. That is
the right arXiv posture and the right way to maximize the credibility of the
core result.
