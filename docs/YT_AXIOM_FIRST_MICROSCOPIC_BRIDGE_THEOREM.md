# Axiom-First Microscopic Bridge Theorem

**Date:** 2026-04-17
**Status:** current supporting theorem for the independent Schur-bridge
cross-check path on the `y_t` lane; reduction theorem, not final UV-to-IR
closure
**Primary runner:** [`scripts/frontier_yt_constructive_uv_bridge.py`](../scripts/frontier_yt_constructive_uv_bridge.py) (4 PASS / 0 FAIL)

## Authority notice

This note is the canonical **axiom-first** summary of the microscopic `y_t`
bridge on the current package surface.

It does not replace the lane authority
[YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md).
Its narrower job is to state the strongest theorem-grade bridge result that now
follows from the accepted framework inputs plus the validated bridge-support
stack.

Read it together with:

- [MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md](./YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md)
- [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md)
- [YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md](./YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)

## Minimal axiom-first input stack

This theorem uses only the current package input stack:

1. local algebra `Cl(3)`
2. spatial substrate `Z^3`
3. finite local Grassmann / staggered-Dirac partition with its exact lattice
   operators
4. physical-lattice reading: the lattice is physical, not merely a regulator
5. canonical normalization with the accepted plaquette / `u_0` surface

Everything else below is a derived bridge statement on top of that stack.

## Theorem statement

> **Axiom-First Microscopic Bridge Theorem.**
> Start from the exact lattice-scale Yukawa/gauge ratio on the accepted
> `Cl(3)` / `Z^3` surface, impose the physical endpoint boundary at `v`, and
> assume the exact interacting UV-to-IR bridge is a quasi-local coarse-grained
> transport on the same physical-lattice surface with leading operator content
> already closed by the derived gauge/Yukawa/Higgs sector.
>
> Then the exact microscopic bridge is not free. On the forced viable window it
> reduces to a UV-centered local transport law whose leading response is
> governed by a positive local selector, whose viable realizations lie in one
> intrinsic UV-centered class, and whose residual departure from the leading
> local selector is captured by explicit higher-order and nonlocal remainder
> terms with a finite endpoint-shift budget.

This is the strongest current package-native bridge theorem.

It does **not** yet prove full exact closure of the microscopic bridge beyond
the current proxy-family support stack, so it does **not** by itself make the
`y_t` lane unbounded.

## Safe corollary

The safe package corollary is:

> The current `y_t(v)` / `m_t` lane is controlled by an axiom-first
> microscopic bridge reduction, not by an unconstrained long-range matching
> ansatz. The remaining bound is now an explicit bridge remainder budget, not a
> vague “matching uncertainty.”

## Proof skeleton

### 1. Exact lattice boundary is fixed by the framework

The lattice-scale ratio theorem fixes the microscopic Yukawa/gauge relation on
the accepted physical surface. This is the exact UV boundary; it is not the
live ambiguity in the lane.

See [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md).

### 2. The physical endpoint is `v`

The package already fixes the physical matching endpoint at the electroweak
scale `v`, rather than treating the bridge as a free interpolation between
arbitrary endpoints.

See [YT_BOUNDARY_THEOREM.md](./YT_BOUNDARY_THEOREM.md) and
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md).

### 3. Broad bridge freedom is eliminated

The constructive bridge scans show that acceptable low-energy endpoints are not
generic. Broad or diffuse bridge deformations fail. Viable solutions occur only
in a narrow UV-localized class.

See [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](./YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md),
[YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md](./YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md), and
[YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](./YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md).

### 4. UV localization is forced, not guessed

The rearrangement principle shows that for positive bridge surplus the endpoint
response is minimized by pushing the surplus as far toward the UV as allowed.
So the viable bridge must be UV-centered rather than spread across the full
interval.

See [YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md](./YT_BRIDGE_REARRANGEMENT_PRINCIPLE_NOTE.md).

### 5. Residual bridge freedom collapses to a moment problem

On the viable UV window, the endpoint-response kernel is nearly affine, so the
bridge no longer behaves like a free profile problem. It collapses to the
weighted-moment data `(I_2, c_2)`, or equivalently one narrow response-weighted
moment band.

See [YT_BRIDGE_ACTION_INVARIANT_NOTE.md](./YT_BRIDGE_ACTION_INVARIANT_NOTE.md)
and [YT_BRIDGE_MOMENT_CLOSURE_NOTE.md](./YT_BRIDGE_MOMENT_CLOSURE_NOTE.md).

### 6. The exact microscopic bridge object is the Schur coarse operator

On the finite local Grassmann partition, coarse/fine marginalization is exact.
So the theorem object is not the scanned profile family by itself; it is the
exact Schur coarse-grained bridge operator on the forced UV window. The current
proxy family is then read as a normal-form chart on that operator.

See [YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md](./YT_EXACT_COARSE_GRAINED_BRIDGE_OPERATOR_NOTE.md).

### 7. The leading selector is induced by the bridge itself

The branch no longer assumes an ad hoc selector. The variational and local
Hessian notes show that on the forced UV window the viable family induces the
positive local selector at leading order.

See [YT_BRIDGE_VARIATIONAL_SELECTOR_NOTE.md](./YT_BRIDGE_VARIATIONAL_SELECTOR_NOTE.md)
and [YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md](./YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md).

### 8. The remainder structure is explicit

The next departures from the leading selector are no longer hidden:

- higher-order local corrections are small
- nonlocal corrections are small
- the induced endpoint shift is bounded explicitly

See [YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md](./YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md),
[YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md](./YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md),
and [YT_BRIDGE_ENDPOINT_SHIFT_BOUND_NOTE.md](./YT_BRIDGE_ENDPOINT_SHIFT_BOUND_NOTE.md).

### 9. The transport law is package-native at leading order

Combining the selector and remainder analyses yields the strongest honest
transport statement currently supported on branch: an affine local transport
kernel on the forced UV window plus explicit higher-order and nonlocal
remainders.

See [YT_EXACT_INTERACTING_BRIDGE_TRANSPORT_NOTE.md](./YT_EXACT_INTERACTING_BRIDGE_TRANSPORT_NOTE.md).

### 10. The constructive family closes to one intrinsic class

The updated uniqueness audit shows that the old diffuse survivors were a coarse
parametric-cut artifact. Inside the broad constructive family, every surviving
profile lies in the same intrinsic UV-centered class.

See [YT_BRIDGE_UV_CLASS_UNIQUENESS_NOTE.md](./YT_BRIDGE_UV_CLASS_UNIQUENESS_NOTE.md).

Together, steps 1-10 prove the theorem boundary stated above.

## What this theorem does and does not give

### What it gives

- an axiom-first microscopic bridge reduction statement
- a forced UV-centered bridge class
- a package-native leading transport law
- explicit higher-order and nonlocal remainder channels
- an explicit endpoint budget instead of a vague matching caveat

### What it does not yet give

- a proof that the exact interacting bridge is fully identical to the current
  proxy-family realization
- a proof that the remainder terms vanish identically
- an unbounded `y_t` lane

So the current lane status remains bounded, but by an explicit microscopic
budget rather than by an opaque surrogate objection.

## Current quantitative boundary

On the current package support stack:

- conservative endpoint budget: `1.2147511%`
- support-tight family-average budget: `0.75500635%`

That budget is the current safe bridge remainder on the `y_t` / `m_t` lane.

## Validation path

This theorem is validated by the branch bridge stack, not by a single runner.
The main validation path is:

- [frontier_yt_constructive_uv_bridge.py](../scripts/frontier_yt_constructive_uv_bridge.py)
- [frontier_yt_bridge_action_invariant.py](../scripts/frontier_yt_bridge_action_invariant.py)
- [frontier_yt_bridge_rearrangement_principle.py](../scripts/frontier_yt_bridge_rearrangement_principle.py)
- [frontier_yt_bridge_moment_closure.py](../scripts/frontier_yt_bridge_moment_closure.py)
- [frontier_yt_bridge_variational_selector.py](../scripts/frontier_yt_bridge_variational_selector.py)
- [frontier_yt_bridge_hessian_selector.py](../scripts/frontier_yt_bridge_hessian_selector.py)
- [frontier_yt_bridge_higher_order_corrections.py](../scripts/frontier_yt_bridge_higher_order_corrections.py)
- [frontier_yt_bridge_nonlocal_corrections.py](../scripts/frontier_yt_bridge_nonlocal_corrections.py)
- [frontier_yt_bridge_endpoint_shift_bound.py](../scripts/frontier_yt_bridge_endpoint_shift_bound.py)
- [frontier_yt_exact_interacting_bridge_transport.py](../scripts/frontier_yt_exact_interacting_bridge_transport.py)
- [frontier_yt_bridge_uv_class_uniqueness.py](../scripts/frontier_yt_bridge_uv_class_uniqueness.py)

## Safe reuse

Use this theorem when the question is:

- why the YT bridge is now microscopic rather than ad hoc
- why the bridge is forced into a UV-centered class
- why the current `y_t` bound is explicit and localized
- why the remaining gap is no longer broad matching ambiguity

Do **not** use this theorem as permission to call the lane unbounded.
