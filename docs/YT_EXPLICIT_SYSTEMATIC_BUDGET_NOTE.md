# `y_t` Explicit Systematic Budget Note

**Date:** 2026-04-15
**Status:** branch authority for `derived with explicit systematic` wording
**Primary runner:** `scripts/frontier_yt_explicit_systematic_budget.py`

## Role

This note closes the branch status question:

> is the remaining `y_t` uncertainty still a generic bounded caveat, or is it
> now explicit enough to be carried as a named systematic?

On this branch, the answer is now the second.

## Status

The live branch-safe status for the Yukawa / top lane is:

> `y_t(v)` and `m_t(pole)` are **derived with explicit systematic**.

They are not unbounded, but they are no longer merely “bounded because the
bridge is unresolved.”

## Why the status changes

Three separate structural questions are now closed on branch:

1. the theorem object is the exact Schur coarse bridge operator
2. the coarse operator’s normal-form class is unique and stable
3. axiom-native local positive microscopic bridge operators reduce into that
   same class at branch scale

That means the remaining uncertainty is no longer structural bridge
admissibility. It is an explicit exact-bridge endpoint budget.

## Named systematic pieces

The remaining branch uncertainty is carried by two named exact-bridge tails:

- higher-order local tail:
  `7.123842e-3 = 0.7123842%`
- nonlocal tail:
  `5.023669e-3 = 0.5023669%` conservative
  or
  `4.262215e-4 = 0.04262215%` support-tight on the current viable family

Two further diagnostics are now negligible or closed:

- selector-anchor mismatch:
  `5.44897e-6` relative
- structural class residual:
  closed at branch scale on the tested locality tube

## Final branch budget

So the live branch systematic is:

- conservative:
  `1.2147511%`
- support-tight:
  `0.75500635%`

around the current central value

- `y_t(v) = 0.9176`

This is now an explicit package-native systematic budget rather than a generic
bounded-surrogate caveat.

## Propagation

The same explicit systematic propagates directly to the top-mass readout:

- `m_t(pole, 2-loop) = 172.57 GeV`
  with explicit systematic
  `±2.097 GeV` conservative,
  `±1.303 GeV` support-tight
- `m_t(pole, 3-loop) = 173.10 GeV`
  with explicit systematic
  `±2.103 GeV` conservative,
  `±1.307 GeV` support-tight

The Higgs / vacuum lane inherits this same branch systematic from the Yukawa
lane rather than a separate Higgs-specific closure failure.

## Safe branch claim

> The framework derives the central Yukawa / top values with zero external SM
> observables. On the current branch, the remaining uncertainty is carried as
> an explicit package-native exact-bridge systematic: `0.7123842%` from the
> higher-order local tail plus `0.5023669%` conservative nonlocal tail
> (`0.04262215%` support-tight on the viable family average), for a total
> conservative branch systematic of `1.2147511%` or support-tight branch
> systematic of `0.75500635%`.

## Honest boundary

This note does **not** claim:

- full unbounded closure of `y_t`
- vanishing of the exact-bridge tails
- a final submission-grade systematic accepted on `main`

What it does claim is narrower and sufficient for this branch:

> the branch now justifies `derived with explicit systematic` wording for the
> Yukawa / top lane.
