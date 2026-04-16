# Historical YT Unbounded Program Note

**Date:** 2026-04-15
**Status:** historical planning/program note; not live authority

This note says one narrow thing: what is still needed to move the current
`y_t` lane from **bounded** to **unbounded**.

The current canonical axiom-first summary of the bridge stack is
[YT_AXIOM_FIRST_MICROSCOPIC_BRIDGE_THEOREM.md](./YT_AXIOM_FIRST_MICROSCOPIC_BRIDGE_THEOREM.md).
The current theorem object for the bridge itself is
[YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md](./YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md).
The current package also has a normal-form class uniqueness theorem at the
coarse-operator level:
[YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md](./YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md).
The current package also has a stability-gap theorem for that class:
[YT_SCHUR_STABILITY_GAP_NOTE.md](./YT_SCHUR_STABILITY_GAP_NOTE.md).
And it now has branch-scale microscopic admissibility of local positive bridge
operators into that same class:
[YT_MICROSCOPIC_SCHUR_CLASS_ADMISSIBILITY_NOTE.md](./YT_MICROSCOPIC_SCHUR_CLASS_ADMISSIBILITY_NOTE.md).

## What is already closed

The package already has the following exact or verified surfaces:

1. The lattice-scale ratio theorem
   `y_t / g_s = 1 / sqrt(6)` from the `Cl(3)` trace identity.
2. `G_5` centrality and ratio protection on the lattice side.
3. Boundary selection: the physical crossover endpoint is `v`, not `M_Pl`.
4. Quasi-fixed-point insensitivity of the backward-Ward transport at the
   current bounded level.
5. A one-shot Feshbach-verified lattice-to-`MSbar` companion bridge via
   [YT_GAUGE_CROSSOVER_THEOREM.md](./YT_GAUGE_CROSSOVER_THEOREM.md).
6. A no-go result showing that the self-consistent one-shot version of that
   bridge fails, so it cannot by itself close the lane.
7. A smooth bridge-family locality proxy showing that viable low-energy
   endpoints occur only when the lattice correction is confined to a narrow UV
   window, not when the bridge is a broad deformation across the whole
   interval.
8. An operator-closure proxy showing that broad electroweak-side deformations
   do not rescue diffuse bridges; the missing structure still sits in the
   dominant gauge/Yukawa transport.
9. A constructive UV-localized bridge class whose accepted low-energy endpoint
   is shape-stable across multiple independent profile families.
10. A bridge-action invariant showing that the viable class is controlled
    primarily by a common normalized gauge-surplus action and UV centroid.
11. A rearrangement principle showing that, once the bridge surplus is
    positive, the endpoint response is smallest when that surplus is pushed
    toward the UV boundary rather than spread broadly or shifted toward the
    IR.
12. A moment-closure reduction showing that, on the viable UV-localized
    window, the accepted response kernel is nearly affine and the remaining
    bridge problem collapses to the two moments `(I_2, c_2)`, or equivalently
    to one narrow response-weighted moment band.
13. A local-Hessian selector derivation showing that, on the forced UV
    window, the viable bridge family itself induces the positive local
    stiffness profile of the coarse-grained bridge Hessian, so the positive
    local quadratic selector is explained at leading order rather than merely
    assumed.
14. A higher-order correction audit showing that, on the viable UV-localized
    bridge family, cubic plus quartic local corrections stay below `1%` of
    the quadratic leading term on the `10%` probe tube.
15. A nonlocal correction audit showing that, on the forced UV window, the
    residual nonlocal tail beyond the local-Hessian selector has operator-norm
    ratio `5.024e-3` and per-mille-level integrated effect on the viable
    bridge families.
16. An intrinsic endpoint-shift bound showing that the exact interacting
    bridge can move the endpoint by at most `1.2147511%` relative to the
    local selector, with a support-tight family-average budget of
    `0.75500635%`.
17. A package-native exact-transport statement showing that, on the forced UV
    window, the branch now supports an affine local transport kernel plus
    explicit higher-order and nonlocal remainder terms.
18. A broad-family uniqueness audit showing that the current support hypotheses force
    every scanned survivor into the same intrinsic UV-centered class; the old
    outside-the-box cases were a coarse parametric-cut artifact, not a true
    diffuse-family escape.

These close the old “missing algebra” and “toy Hamiltonian only” objections.

## What is not yet closed

One quantitative bridge remainder remains bounded:

> eliminate, or push below the paper bar, the explicit package-native endpoint
> budget carried by the exact interacting bridge on the forced UV window.

That is the entire residual.

## What will not close it

The following are not the main lever anymore:

- more Higgs work
- more EW normalization work
- direct one-scale lattice Yukawa response measurements
- applying the Ward identity directly at `v`

Those checks can be useful diagnostics, but they do not replace the full
UV-to-IR transport.

## The actual unbounded target

To make `y_t` unbounded, the package needs a stronger theorem than the current
QFP insensitivity statement.

The clean target is:

> **Zero-Input Interacting Bridge Theorem.**
> The exact lattice boundary condition and the physical-taste interacting
> low-energy bridge determine the same `y_t(v)` endpoint without an
> uncontrolled backward-Ward surrogate and without imported crossover
> coefficients.

On the current tested scale, most of the old structural parts of that target are now in
hand: the theorem object is the exact Schur coarse bridge operator, its
normal-form class is unique, the class is stable, and microscopic
admissibility into that class is closed on the tested locality tube.

So the remaining unbounded target is narrower than before. In practical terms,
it now means proving or validating these pieces together:

1. **intrinsic exact-bridge remainder control**
   showing that the higher-order local tail and nonlocal tail of the exact
   bridge are intrinsically bounded below the paper bar rather than merely
   measured at current package scale
2. **endpoint-collapse or endpoint-negligibility theorem**
   showing that those intrinsic tails cannot move `y_t(v)` by more than a
   negligible amount on the accepted UV window
3. **zero-input closure of the crossover**
   replacing the current import-allowed one-shot `MSbar` matching companion,
   whose self-consistent version fails, with an internal package authority if
   any residual bridge normalization step remains

If those three are closed, the current explicit bridge budget
(`1.2147511%` conservative, `0.75500635%` support-tight) collapses and the
lane becomes unbounded.

The new locality proxy also sharpens the shape of the target:

- the missing bridge is not allowed to be an arbitrary smooth deformation over
  all `17` decades
- the viable window is much closer to an SM-like transport over most of the
  interval, with a narrow UV-localized lattice correction

See [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](./YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md).
See also [YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md](./YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md).
See also [YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](./YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md).
See also [YT_BRIDGE_ACTION_INVARIANT_NOTE.md](./YT_BRIDGE_ACTION_INVARIANT_NOTE.md).
See also [YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](./YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md).
See also [YT_BRIDGE_MOMENT_CLOSURE_NOTE.md](./YT_BRIDGE_MOMENT_CLOSURE_NOTE.md).
See also [YT_BRIDGE_VARIATIONAL_SELECTOR_NOTE.md](./YT_BRIDGE_VARIATIONAL_SELECTOR_NOTE.md).
See also [YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md](./YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md).
See also [YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md](./YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md).
See also [YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md](./YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md).
See also [YT_BRIDGE_ENDPOINT_SHIFT_BOUND_NOTE.md](./YT_BRIDGE_ENDPOINT_SHIFT_BOUND_NOTE.md).
See also [YT_EXACT_INTERACTING_BRIDGE_TRANSPORT_NOTE.md](./YT_EXACT_INTERACTING_BRIDGE_TRANSPORT_NOTE.md).
See also [YT_BRIDGE_UV_CLASS_UNIQUENESS_NOTE.md](./YT_BRIDGE_UV_CLASS_UNIQUENESS_NOTE.md).
See also [YT_EXPLICIT_SYSTEMATIC_STATUS_REVIEW_2026-04-15.md](./YT_EXPLICIT_SYSTEMATIC_STATUS_REVIEW_2026-04-15.md).
See also [YT_EXPLICIT_SYSTEMATIC_REDUCTION_OPTIONS_2026-04-15.md](./YT_EXPLICIT_SYSTEMATIC_REDUCTION_OPTIONS_2026-04-15.md).

## Immediate program

The strongest next package-facing tasks are:

1. treat the current one-shot gauge-crossover result as a bounded companion
   plus a self-consistent no-go, not as the likely final closure route
2. build the next bridge on top of that no-go: the zero-input interacting
   bridge must be richer than a single finite one-shot `MSbar` conversion
3. use the new locality constraint to target a UV-localized operator bridge,
   rather than a broad smooth deformation of the whole interval
4. connect that bridge directly to the accepted central `y_t(v) ~= 0.918`
   route rather than the older `0.973 / 169.4 GeV` zero-import branch

At this point, the branch already has a constructive candidate class for that
bridge, and the rearrangement principle explains why the bridge must localize
toward the UV boundary.

The remaining work is narrower still:

- not to guess a viable profile numerically
- not to explain UV localization in general
- not even to choose a general profile inside that class
- not even to choose the weighted moment band conditionally
- but to turn the current package-native bridge budget
  (`1.2147511%` conservative, `0.75500635%` support-tight), exact Schur class
  uniqueness, stability gap, and branch-scale microscopic admissibility into
  either a full vanishing/negligibility theorem or a fully enumerated final
  systematic strong enough to remove the remaining bridge qualifier

## Honest conclusion today

Today’s package already shows that the `y_t` bound is no longer a vague
“something about matching.” The selector origin is now closed at leading
order, the Schur class is unique and stable, branch-scale microscopic
admissibility into that class is closed, and the first higher-order and
nonlocal corrections above that selector are quantitatively small on the
viable bridge family. The branch now also has an explicit package-native
endpoint budget below the old QFP-only few-percent fallback. What remains is
to turn that exact-bridge budget into either an intrinsic negligibility theorem
or a fully enumerated final systematic.

That is the path to unbounded `y_t`.
