# y_t Flagship Boundary Note

## Authority Notice

This note is a **supporting boundary note**, not the sole lane authority.

For current package decisions, read it together with:

- [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](./YT_ZERO_IMPORT_AUTHORITY_NOTE.md)
- [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md)
- [YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md](./YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
- [YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md](./YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md)
- [YT_AXIOM_FIRST_MICROSCOPIC_BRIDGE_THEOREM.md](./YT_AXIOM_FIRST_MICROSCOPIC_BRIDGE_THEOREM.md)
- [YT_MICROSCOPIC_SCHUR_CLASS_ADMISSIBILITY_NOTE.md](./YT_MICROSCOPIC_SCHUR_CLASS_ADMISSIBILITY_NOTE.md)

Its purpose is narrower: say exactly what remains systematic-limited in the
live `y_t` lane after the recent cleanup and direct-extraction audit.

**Date:** 2026-04-15
**Status:** DERIVED with explicit systematic
**Current central values:** `y_t(v) = 0.9176`, canonical
`m_t(pole) = 173.10 GeV` (3-loop), with retained `172.57 GeV` (2-loop)
support

---

## Final reviewer answer

The current `y_t` lane is best described as:

- **zero external SM observables**
- **derived central value**
- **carrying an explicit package-native transport budget:
  `1.2147511%` conservative, `0.75500635%` support-tight**

That is the honest final boundary on the current package today.

## What is exact

These parts of the `y_t` lane are not the live blocker:

1. `y_t / g_s = 1 / sqrt(6)` from the Cl(3) trace identity
2. `G_5` centrality in Cl(3), giving lattice-scale ratio protection
3. the derivation of the SM gauge group and matter content
4. the use of SM beta coefficients as consequences of that derived field content
5. the hierarchy / electroweak matching scale `v`

Those pieces explain why the lane is predictive at all.

## What is still systematic-limited

One real explicit systematic remains.

### The remaining explicit systematic

The low-energy `y_t(v)` value is obtained by transferring the lattice Ward
boundary condition through the backward-Ward route. That route uses the SM RGE
as the perturbative surrogate for the true lattice blocking flow over the full
`v -> M_Pl` interval.

The current package stack narrows the live transport bound materially below the
older QFP-only fallback. On the forced UV window, the exact interacting bridge
is now controlled by:

- a positive local-Hessian selector,
- higher-order local corrections below `1%` of the quadratic leading term on
  the `10%` probe tube,
- a nonlocal tail with operator-norm ratio `5.023669e-3`,
- and an explicit endpoint-shift budget of `1.2147511%` conservative or
  `0.75500635%` support-tight around the local selector.

That narrower budget is real and propagates to the physical top mass.

### What the bound means

- the central value can still be very strong
- the lane is still zero-import
- but the exact numerical closure is not yet unbounded

The right read is:

- `y_t(v)`: derived central value with explicit systematic
  `1.2147511%` conservative
  (`0.75500635%` support-tight on the current family average)
- `m_t(pole)`: derived central value, inherits the same explicit transport
  systematic

## Direct-lattice bypass audit

The obvious way to remove the bound would be to avoid the backward-Ward
surrogate entirely and measure `y_t(v)` directly on the lattice.

That route was checked in
[scripts/frontier_direct_yt_extraction.py](../scripts/frontier_direct_yt_extraction.py).

Current conclusion:

- direct response / vertex / susceptibility methods measure the Yukawa at the
  lattice scale, not at the low-energy endpoint `v`
- applying the Ward identity directly at `v` fails badly
- lattice-native step-scaling would in principle work, but it would require an
  absurdly large blocking range and is not feasible on accessible lattices

So the current package does **not** have a practical direct-lattice bypass for
the backward-Ward route.

## Therefore

The current `y_t` lane is **not** blocked by a missing algebraic theorem.
It is limited by a real but understood methodological systematic:

- the backward-Ward / QFP surrogate remains the minimal feasible bridge
- but the current package support stack now narrows the live endpoint budget to
  `1.2147511%` conservative or `0.75500635%` support-tight

The supporting bridge theory is now stronger than that summary alone suggests:

- [YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](./YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
  gives a real candidate bridge class: once the bridge is forced into the
  narrow UV-localized window, independent profile families all reproduce the
  accepted low-energy endpoint with negligible spread.
- [YT_BRIDGE_ACTION_INVARIANT_NOTE.md](./YT_BRIDGE_ACTION_INVARIANT_NOTE.md)
  reduces that viable class further: the endpoint is overwhelmingly controlled
  by a common gauge-surplus action invariant and a tight UV centroid.
- [YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](./YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md)
  explains why the viable class must be UV-localized in the first place: the
  downward endpoint-response kernel is weakest near the UV endpoint and
  strongest near the IR endpoint, so equal positive surplus gives the smallest
  endpoint shift when it is placed as far toward the UV as allowed.
- [YT_BRIDGE_MOMENT_CLOSURE_NOTE.md](./YT_BRIDGE_MOMENT_CLOSURE_NOTE.md)
  reduces the residual bridge freedom further: on the viable UV-localized
  window, the accepted response kernel is nearly affine, so the package closes
  to a two-moment problem `(I_2, c_2)` or one narrow response-weighted moment
  band rather than a free profile-selection problem.
- [YT_BRIDGE_VARIATIONAL_SELECTOR_NOTE.md](./YT_BRIDGE_VARIATIONAL_SELECTOR_NOTE.md)
  turns that weighted-moment reduction into a concrete conditional selector:
  if the microscopic bridge selector is a positive local quadratic action on
  the forced UV window, then the minimizer is unique and already matches the
  observed best-family bridge band.
- [YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md](./YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md)
  closes the next microscopic step at leading order: the viable bridge family
  itself induces the positive local stiffness profile of the coarse-grained
  bridge Hessian on the forced UV window, so the local quadratic selector is
  no longer an unexplained ansatz. What remains is higher-order or nonlocal
  correction control above that local Hessian selector.
- [YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md](./YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md)
  quantifies the first local corrections above that selector on the viable
  UV-localized family: cubic plus quartic terms stay below `1%` of the
  quadratic leading term on the `10%` probe tube, so the local-Hessian
  picture remains the right leading description.
- [YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md](./YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md)
  quantifies the first nonlocal correction on the forced UV window: the
  residual nonlocal tail stays at `5.024e-3` in operator norm and at or below
  the per-mille level when integrated against the viable bridge families.
- [YT_BRIDGE_ENDPOINT_SHIFT_BOUND_NOTE.md](./YT_BRIDGE_ENDPOINT_SHIFT_BOUND_NOTE.md)
  combines those two audits into one explicit endpoint budget around the local
  selector: `1.2147511%` conservative or `0.75500635%` support-tight.
- [YT_EXACT_INTERACTING_BRIDGE_TRANSPORT_NOTE.md](./YT_EXACT_INTERACTING_BRIDGE_TRANSPORT_NOTE.md)
  packages the strongest honest UV-to-IR transport law currently supported:
  an affine local kernel on the forced UV window plus explicit higher-order
  and nonlocal remainders.
- [YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md](./YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md)
  promotes the theorem object from the scanned proxy family to the exact Schur
  coarse bridge operator on the forced UV window; the proxy family is then a
  normal-form chart on that exact operator rather than the ontology.
- [YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md](./YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md)
  closes the next remaining ambiguity on the current tested scale: within the intrinsic
  remainder budgets, the exact Schur coarse operator does not jump across
  multiple normal-form classes.
- [YT_SCHUR_STABILITY_GAP_NOTE.md](./YT_SCHUR_STABILITY_GAP_NOTE.md)
  shows the exact Schur class is not knife-edge; it sits inside an open
  stability basin separated from the first normal-form escape.
- [YT_BRIDGE_UV_CLASS_UNIQUENESS_NOTE.md](./YT_BRIDGE_UV_CLASS_UNIQUENESS_NOTE.md)
  closes broad-family uniqueness at the intrinsic UV-centered class level:
  the old outside-the-box survivors were a coarse parametric-cut artifact.
- [YT_MICROSCOPIC_SCHUR_CLASS_ADMISSIBILITY_NOTE.md](./YT_MICROSCOPIC_SCHUR_CLASS_ADMISSIBILITY_NOTE.md)
  closes the remaining tested-scale structural loophole: local positive
  microscopic bridge operators in the axiom-native locality tube reduce
  exactly into that same unique stable Schur class and stay inside the
  conservative endpoint budget.
- [YT_AXIOM_FIRST_MICROSCOPIC_BRIDGE_THEOREM.md](./YT_AXIOM_FIRST_MICROSCOPIC_BRIDGE_THEOREM.md)
  packages the full bridge stack as one axiom-first microscopic reduction
  theorem: the remaining gap is no longer broad-family ambiguity or
  tested-scale microscopic admissibility, but only the explicit endpoint
  budget carried by the exact bridge.

## Paper-safe claim

The honest paper-safe wording is:

> The framework derives the lattice-scale Yukawa-to-gauge ratio exactly and
> propagates it to low energy with zero external SM observables. The current
> low-energy `y_t` and `m_t` central values are strong and near observation, and
> they carry an explicit transport systematic because the branch still uses the
> backward-Ward / QFP surrogate as the practical realization of the true
> lattice blocking flow above `v`. On the current package support stack, that
> systematic is narrowed to `1.2147511%` conservative or `0.75500635%`
> support-tight around the local selector. The selector origin is understood,
> the Schur class is unique and stable, and microscopic admissibility into that
> class is closed on the current tested scale. The remaining uncertainty is explicit rather
> than structural.

## Cannot claim

Do not claim any of the following from this branch today:

- that the `y_t` lane is fully unbounded
- that the backward-Ward surrogate has been bypassed
- that direct lattice extraction already delivers `y_t(v)` on accessible lattices
- that the bridge systematic has disappeared
- that the current endpoint budget is theorem-grade uniqueness rather than a
  named transport systematic

## Why this still matters

The bound is now as narrow as we know how to make it without a genuinely new
low-energy `y_t` route:

- no external SM observable is used as an input
- the central value remains close to observation
- the selector origin is now closed at leading order
- the first higher-order and nonlocal corrections above that selector are
  quantified and small on the viable bridge family
- the exact bridge endpoint is confined to an explicit package-native budget
  around the selector
- the remaining uncertainty is explicit, localized, and method-specific

That is a much stronger posture than “`y_t` is still vague or open.”
