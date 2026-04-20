# Review Note for `morning4-4-20`

## Verdict

Not ready to promote into the canonical review branch as-is.

The branch contains useful structural ideas, but it does **not** honestly close the remaining Koide open items at current branch standards. The top-level claim of full closure is stronger than what the supporting notes and runners actually establish.

## What Is Useful

- The branch sharpens the structural picture around `d = 3`.
- The single-real-doublet / `Cl(3)` spinor-qubit interpretation is a useful explanatory layer.
- The Fourier-basis identities around `Im(b_F)`, `T_M_F = T_M`, and `|Im(b_F)|^2 = Q/d` look like legitimate supporting structure.

Those are potentially worth salvaging later, but only after the closure claims are made honest.

## Main Blocking Issues

### 1. `Q = 2/3` is still not independently closed here

The new `Q` route still depends on the retained Lane-2 / MRU extremum structure:

- `Q = (1 + 2 / kappa) / d` is fine as an algebraic formula.
- But the branch still gets to `Q = 2/3` by using `kappa = 2`.
- That is not a new native derivation unless `kappa = 2` itself is rederived from strictly more primitive retained structure than the existing lane.

As written, this is a re-expression of the existing route, not a replacement for it.

### 2. The CPC chain is circular with respect to the remaining gap

The CPC chain script explicitly takes retained `Q = 2/3` as input and then derives:

- `SELECTOR^2 = Q`
- `|Im(b_F)|^2 = Q/d`
- `d delta = Q`

That is fine as a conditional chain, but it does **not** close the remaining `Q` gap. It only says:

> if retained `Q` is accepted, then the rest of the chain matches numerically/algebraically.

That is weaker than “CPC is now derived with zero additional cost.”

### 3. The radian-bridge / physical forcing step is still not independently proved

Several supporting scripts still effectively treat

- `delta = |Im(b_F)|^2`
- or equivalently `d delta = Q`

as the decisive forcing step.

The branch gives strong evidence, equivalences, and numerical confirmation, but it does not yet produce a clean theorem showing that the physical Berry phase **must** equal the structural `Q/d` value without smuggling that statement back in as CPC, equivalence, or point-selection.

In short:

- `|Im(b_F)|^2 = Q/d` looks structural.
- `delta(m_*) = Q/d` is verified numerically.
- The missing step is still the theorem that these are the same physical quantity for a retained reason.

### 4. Some runners still contain hardcoded `PASS` checks

That makes the branch non-canonical for review landing.

Examples include checks that are literally `check(..., True, ...)` in the new `Q` and forcing scripts.

Those need to be removed or replaced with actual computed assertions.

### 5. The note overclaims relative to the support stack

The top note currently says the residual gaps are closed, but parts of the runner stack still describe the forcing step as:

- residual
- equivalent to CPC
- candidate theorem / candidate axiom

That mismatch has to be resolved before promotion.

## What Would Count as a Real Closure

Any one of the following would materially improve this branch:

### A. Honest downgrade + salvage

Recast this branch as:

- structural sharpening of the `Q/d` story
- new explanatory interpretation of `d = 3`
- support for the remaining open forcing theorem

This is the fastest path if the goal is to preserve the good parts without overclaiming.

### B. Genuine new `Q = 2/3` theorem

To count as new closure, the branch would need a route to `Q = 2/3` that does **not** merely pass through the existing retained `kappa = 2` / MRU lane in renamed form.

The real question is:

> what primitive retained structure forces the cone value before Lane 2 is invoked?

If the answer is still “the same 2-block MRU extremum,” then this branch is explanatory, not closing.

### C. Genuine radian-bridge theorem

To close the remaining phase gap, the branch needs a theorem of the form:

> the physical selected-line Berry phase is the same retained object as the structural doublet phase unit `|Im(b_F)|^2`

without taking CPC, `delta = Q/d`, or equivalent point-selection as input.

That is the real unresolved target.

## Concrete Next-Step Recommendations

1. Remove every hardcoded `check(..., True, ...)` and replace with computed checks or delete them.
2. Rewrite the top note status from “closed” to “proposal / partial closure” unless a real new theorem is added.
3. Split the material into three buckets:
   - structural identities that are actually proved
   - numerical confirmations
   - remaining forcing claims
4. In the CPC chain, explicitly label `Q = 2/3` as an input unless it is independently rederived in the same proof stack.
5. Decide whether this branch is trying to:
   - close `Q = 2/3`, or
   - close the radian bridge, or
   - provide interpretation only

Trying to claim all three at once is what currently makes the branch read stronger than the actual proof state.

## Review-Safe Status After This Pass

What this branch currently supports best is:

- better structure around why `d = 3` is special
- stronger algebraic support for `|Im(b_F)|^2 = Q/d`
- stronger evidence that the physical point satisfies the same value

What it does **not** yet support at canonical review level is:

- independent native closure of `Q = 2/3`
- independent native closure of the physical radian bridge

If those two claims are softened or one of them is genuinely closed, this branch becomes much more useful.
