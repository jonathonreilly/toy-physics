# Algebraic Decoration Policy

**Status:** binding rule for the audit lane.

The CKM atlas demonstrated a pattern in which a small set of input
identities (`λ² = α_s/2`, `A² = 2/3`, `ρ = 1/6`, `η = √5/6`) generated dozens
of "retained NLO CKM-structure corollaries" — Weitzenbock, Brocard,
Napoleon, Pedoe, circumradius, orthocenter, Euler-line, Bernoulli families,
classical-number-theory characterizations, and so on. Each is presented as a
separately retained theorem with its own note, runner, and status badge.
None adds independent physical content beyond the four input identities.

This is **algebraic decoration**: ordinary algebra applied to the same fixed
parameter choice, presented as if the algebraic consequences carry the same
weight as the underlying choice.

This file specifies how the audit lane identifies decoration and what
happens when it does.

## 1. Decoration definition

A claim is decoration with respect to a parent claim P if all three hold:

1. **Algebraic dependence.** The claim follows from P by ordinary algebra
   (arithmetic, polynomial identities, Euclidean geometry, group theory,
   number theory) without introducing a new physical observable, a new
   measurement, or a new connection to the underlying axiom.

2. **No new comparator.** The claim does not produce a quantitative
   prediction that is compared against PDG, lattice QCD, or any external
   data in a way that is independent from comparators already attached to
   P. A claim that says "and now this Brocard polynomial also evaluates
   exactly" without producing a measurable quantity is decoration.

3. **No compression.** The claim does not simplify or compress the parent
   claim. A genuine corollary that lets the parent be stated more sharply,
   or that exposes a new structural integer not visible in P, is **not**
   decoration. Mere expansion of P into more identities is.

## 2. Detection heuristics (mechanical)

The classifier flags candidates by:

- **Single-parent dependency.** Notes whose `cited authorities` reduce to
  exactly one parent claim (plus universal mathematical references) are
  decoration candidates.
- **No D-class runner check.** Notes whose runner has zero `(D)` external
  comparator PASSes are decoration candidates.
- **Closed-form name pattern.** Notes whose title contains
  `EXACT_CLOSED_FORM`, `STRUCTURAL_IDENTITY`, `POLYNOMIAL_UNIFICATION`,
  `BERNOULLI_FAMILY`, `NAPOLEON`, `BROCARD`, `WEITZENBOCK`, `PEDOE`,
  `CIRCUMRADIUS`, `ORTHOCENTER`, `EULER_LINE`, `NUMBER_THEORY`,
  `CHARACTERIZATION`, or similar pure-mathematical terms are heuristically
  flagged for human review of decoration status.
- **Cluster size.** When more than 5 retained-tagged claims share a single
  parent and none has a `(D)` check, the cluster as a whole is flagged.

These are heuristics; the verdict is set by the audit, not by the
heuristic.

## 3. Outcome when audited as decoration

A claim with `audit_status = audited_decoration` triggers two actions:

### 3a. Boxing

The claim no longer appears as a separate row in `CLAIMS_TABLE.md` or
`PUBLICATION_MATRIX.md`. Its content is rolled up into a single
"Algebraic corollaries of P" line under the parent claim's row, with a
link to a consolidated `docs/audit/decoration_clusters/<parent>.md`
file that lists the algebraic consequences as a single corollary box.

The original note may remain on disk (history is preserved), but its
status badge is changed to `audited_decoration` and its inclusion in
publication-facing tables is suppressed.

### 3b. Pruning candidates

A decoration cluster qualifies for **removal** (not just boxing) if all
of:

1. The cluster has more than 10 notes sharing a single parent;
2. No member of the cluster has a `(D)` check;
3. No member of the cluster is referenced as a load-bearing input by any
   non-decoration claim;
4. Removing the cluster would not break any external citation.

When all four hold, the cluster is summarized in a single short
"corollary inventory" paragraph inside the parent note, the individual
notes are deleted, and the change is logged as a pruning event in
`docs/audit/data/pruning_log.json`.

## 4. What is not decoration

The following are explicitly **not** decoration even if they look algebraic:

- **A new structural integer.** If the corollary exposes an integer that
  is not present in the parent (e.g., a new Lie-dimensional identity that
  the parent did not articulate), it is a genuine structural extension.
- **A new comparator.** If the corollary is what gets actually measured
  (e.g., a Jarlskog area that is the directly compared quantity),
  removing it would lose the comparator surface.
- **A compression theorem.** If the corollary lets two previously
  separate claims be stated as one, it is genuine compression and must be
  retained.
- **A no-go.** Negative results that close off otherwise-tempting
  alternative routes (e.g., "no rooted-staggered loophole") are load-bearing
  and not decoration.

## 5. Re-promotion path

A claim demoted to `audited_decoration` may be re-promoted if a later
note attaches a genuine `(D)` external comparator to it, or if it is
shown to be load-bearing for a non-decoration claim. Re-promotion
requires a fresh audit and is logged.

## 6. CKM atlas as the worked example

The CKM cluster of "retained NLO CKM-structure corollaries" is the seed
test case. After audit, the expected outcome is:

- One **retained** row: the underlying input identities
  (`λ² ≈ α_s/2`, `A² ≈ 2/3`, `ρ²+η² ≈ 1/6`) — likely
  `audit_status = audited_renaming` or `audited_numerical_match`
  pending audit, not `audited_clean`.
- One **boxed** corollary inventory listing the geometric / number-theoretic
  consequences (Weitzenbock, Brocard, Napoleon, Pedoe, etc.) without
  treating each as a separate retained theorem.
- One **retained** sharp prediction: `γ̄ = arctan(√5)` as the falsifiable
  number that the package actually stands or falls on.

The decoration cluster shrinks from roughly 25 retained rows to 1
parent + 1 boxed corollary inventory + 1 sharp prediction.

## 7. Author intent and tone

This policy is not a criticism of the algebraic work itself — the
identities are real. It is a claim-surface management policy. A package
that presents 25 separate retained theorems where 3 distinct claims exist
is harder to review, harder to falsify, and harder to take seriously as
an external reader. Pruning decoration improves the signal density of
the publication package.
