# YT Bound Status Review

**Date:** 2026-04-15
**Branch:** `codex/yt-unbounded-main-package-2026-04-15`
**Scope:** reviewer-grade analysis of the live `y_t` lane on the current branch
after the new bridge stack

## Verdict

The current `y_t` lane is now best stated as **derived with explicit
package-native systematic** on this branch:

- `1.2147511%` conservative
- `0.75500635%` support-tight on the current viable family average

That status is not due to a missing central value. The branch already has a
strong zero-import central route, and it now has a substantial bridge stack that
narrows the remaining problem. The reason the lane still stays systematic-limited is more
specific:

- the low-energy endpoint is still obtained through the backward-Ward / QFP
  surrogate above `v`
- the exact interacting lattice bridge now has an exact Schur coarse operator,
  a unique stable Schur class, and branch-scale microscopic admissibility into
  that class, but it still carries an explicit endpoint budget
- the branch still has no theorem that drives the higher-order and nonlocal
  corrections of that exact bridge to zero or below the paper bar

So the current state is:

- **theorem-grade core exists**
- **proxy support is strong**
- **the remaining uncertainty is explicit, but not yet eliminated**

## What is theorem-grade

The following are the strongest live results on this branch that should be
treated as theorem-grade or near-theorem-grade:

1. **Lattice-scale ratio theorem**
   `y_t / g_s = 1 / sqrt(6)` from the `Cl(3)` trace identity.

2. **Boundary selection theorem**
   the physical crossover endpoint is `v`, not `M_Pl`.

3. **QFP insensitivity theorem**
   the backward-Ward transport is stable to bounded coefficient changes at the
   few-percent level.

4. **One-shot gauge-crossover companion no-go**
   the self-consistent one-shot route does not close the lane by itself.

5. **Leading-order selector explanation**
   the bridge Hessian note explains why the exact interacting bridge induces a
   positive local quadratic selector on the forced UV window at leading order.

These results are enough to say that the lane is not vague, not arbitrary, and
not merely numerological. They are not yet enough to declare the lane
unbounded.

## What is proxy support

The following bridge-stack results are strong and useful, but they are still
proxy support rather than final theorem closure:

- interacting bridge locality scan
- operator-closure scan
- constructive UV-localized bridge class
- bridge-action invariant reduction
- rearrangement principle
- moment-closure reduction
- variational selector
- Hessian selector

Each of these narrows the residual target. They are no longer carrying the
whole structural burden by themselves: the exact Schur coarse operator,
Schur-class uniqueness, stability gap, and microscopic admissibility theorems
now close that structural layer on the branch.

## Current quantitative picture

The branch now supports a strong central value and an explicit bounded
transport budget:

- accepted central route: `y_t(v) ~= 0.9176`
- corresponding top mass: `m_t(pole) ~= 172.6 GeV`
- residual bound:
  `1.2147511%` conservative or `0.75500635%` support-tight
- source of the bound: package-native control of the exact interacting bridge
  around the local selector; broad scanned-family uniqueness, exact Schur
  normal-form uniqueness, Schur stability, and branch-scale microscopic
  admissibility are all closed, but the exact bridge still carries the
  explicit endpoint budget

That is the honest current boundary. The older QFP-only few-percent envelope is
now a historical fallback, not the best live branch budget.

## What would have to be true for a narrower bounded status

The lane could be reclassified from the current explicit bounded budget to an
even narrower bounded status if the branch proves a still smaller, explicit
error budget for the remaining bridge. Concretely, one of the following would
have to happen:

- the exact interacting bridge is shown to lie in the forced UV-localized class
  with a computed correction envelope smaller than the current QFP budget
- the higher-order and nonlocal corrections above the local Hessian selector are
  bounded explicitly and that bound is below the current
  `1.2147511% / 0.75500635%` bridge envelope
- a direct branch-native step-scaling or matching calculation replaces the
  current surrogate and returns a smaller, validated uncertainty band

Without one of those, the current explicit bridge budget remains the correct
live posture.

## Why the branch now clears "derived with explicit systematic"

The lane now meets that bar on branch because:

1. The low-energy endpoint is carried by the package-native bridge itself on
   the forced UV window.
2. The residual uncertainty is decomposed into explicit named pieces:
   higher-order local tail and nonlocal tail.
3. Structural class ambiguity is closed at branch scale, so the residual is no
   longer a generic bridge loophole.
4. The package wording can now honestly read as a derived central value with
   explicit systematic rather than as a merely bounded bridge caveat.

## What still blocks a status change

The blocker is now very narrow:

- the higher-order and nonlocal corrections above the local Hessian selector
  are not yet controlled tightly enough to collapse the explicit endpoint
  budget
- direct low-energy lattice extraction on accessible lattices remains infeasible

So the remaining gap is no longer “what profile works?” or “why UV-localized?”
It is the intrinsic correction control above the leading-order selector on the
exact bridge.

## Bottom line

The current branch has enough structure to say the `y_t` lane is highly
constrained and internally coherent. It now justifies promoting the branch
read from the older few-percent fallback to **derived with explicit
systematic**. The next work step is no longer a status move from bounded to
systematic; it is whether the explicit systematic can be tightened further or
collapsed entirely toward unbounded closure.
