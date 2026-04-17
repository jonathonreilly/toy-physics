# Plaquette Self-Consistency: `<P>` as a Derived Same-Surface Constant

**Date:** 2026-04-15  
**Status:** retained evaluation theorem (no free parameter), with exact bridge-support stack
**Script:** `scripts/frontier_plaquette_self_consistency.py`

## Claim

The plaquette expectation

`<P>(beta = 6, SU(3), 4D) ~= 0.5934`

is a uniquely determined observable of the axiom-defined partition function on
the retained graph-first `SU(3)` Wilson-plaquette evaluation surface. It is not
a fit parameter and it is not an experimental import.

Computing the number requires non-perturbative evaluation. That is evaluation
of a derived quantity, not introduction of a free degree of freedom.

## Why This Matters

The current quantitative stack uses the canonical plaquette chain

`<P> -> u_0 = <P>^(1/4) -> alpha_s(v) = alpha_bare / u_0^2`

and then reuses `u_0`, `alpha_s(v)`, and downstream quantities across the
hierarchy, EW, CKM, confinement, Yukawa, and Higgs lanes.

The review-safe point is:

- `<P>` is not an externally chosen knob
- `<P>` is not a hidden fit parameter
- `<P>` is a same-surface evaluated observable of the retained theory

## Argument

### 1. The partition function is well-defined

On the retained graph-first gauge surface:

- the gauge group is `SU(3)`
- the Wilson plaquette action at `g_bare^2 = 1` gives `beta = 2 N_c / g^2 = 6`
- the finite periodic lattice gives a finite product of compact Haar integrals

So

`Z(beta) = integral DU exp(-S_W[U])`

is finite and well-defined.

### 2. The plaquette is a unique observable

The average plaquette is

`<P> = (1 / N_plaq) d(ln Z) / d beta`.

Since `Z(beta)` is well-defined, `<P>` is a unique observable of the same
partition function. There is no independent freedom to choose it.

### 3. No phase-transition ambiguity is present at `beta = 6` on symmetric `L^4`

The deconfining transition in `SU(3)` lattice gauge theory is a finite-
temperature transition on asymmetric lattices, not a bulk transition on
symmetric `L^4` lattices. So the plaquette on the symmetric `L^4` surface is
the smooth same-phase observable that the framework actually uses.

### 4. Monte Carlo evaluates the observable; it does not parameterize it

Monte Carlo is the numerical evaluation method for this partition-function
expectation value, exactly as numerical quadrature evaluates an analytically
defined integral. The computation is non-perturbative, but the quantity is
still framework-derived.

## Verification Surface

The runner checks:

1. self-consistency of the uniqueness argument
2. multi-volume plaquette convergence at `beta = 6`
3. smooth monotone `beta`-dependence on a symmetric lattice
4. perturbative-window sanity checks
5. downstream consistency of `u_0` and `alpha_s(v)`

## Exact bridge-support stack on `main`

The live repo now also carries a materially stronger exact support stack:

- exact local `SU(3)` one-plaquette block
- exact accepted Wilson gauge-source temporal completion theorem
- exact distinct-shell theorem for connected plaquette shells on the accepted
  `3 spatial + 1 derived-time` surface
- exact mixed repeated-plaquette audit and exact first nonlinear coefficient
  of the full-vacuum reduction law
- exact implicit reduction-law existence/uniqueness theorem on the finite
  Wilson evaluation surface
- exact nonperturbative susceptibility-flow theorem for the implicit reduction
  law
- exact connected plaquette-hierarchy theorem for the implicit reduction law
- exact obstruction to any finite-order connected-hierarchy truncation
- exact compact plaquette spectral-measure generating object for the full
  finite Wilson hierarchy
- exact framework-point underdetermination theorem showing that the current
  closed jet and structure theorems still do not force a unique analytic
  `P(6)`
- exact transfer-operator / character-recurrence realization of the plaquette
  generating object on the accepted `3+1` source surface
- exact Perron-state reduction theorem on the explicit transfer operator
- exact source-sector matrix-element factorization theorem at `beta = 6`
- exact local/environment factorization theorem isolating the exact local
  Wilson marked-link factor on the source sector
- exact Perron/Jacobi underdetermination theorem showing that even the
  sharpened factorized operator class still does not force unique `beta = 6`
  Perron moments or Jacobi coefficients until the residual
  environment-response sequence is fixed
- exact scalar `3+1` bridge endpoint ratio
  `A_inf / A_2 = 2 / sqrt(3)`
- exact plaquette four-link coupling map
  `P(U) = u_0^4 P(V)`
- exact `3+1` plaquette/link incidence factor `6 / 4 = 3 / 2`
- exact obstruction to the naive constant-lift law
  `P(beta) = P_1plaq(beta * (3/2) * (2 / sqrt(3))^(1/4))`

Those ingredients sharply narrow the last insertion bridge and give the current
best analytic candidate

`P(6) = 0.593530679977098`.

This sits only `1.3068e-4` (`0.022%`) above the current canonical same-surface value
`0.5934`, so it materially strengthens the plaquette lane.

Current authorities for that support stack:

- [GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_DISTINCT_SHELL_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_DISTINCT_SHELL_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md)
- [GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md](./GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)
- [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](./SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)

Current support runners:

- `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py`
- `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py`
- `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py`
- `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py`
- `scripts/frontier_gauge_vacuum_plaquette_transfer_operator_character_recurrence.py`
- `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py`
- `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py`
- `scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py`
- `scripts/frontier_gauge_scalar_temporal_completion_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py`
- `scripts/frontier_scalar_3plus1_temporal_ratio.py`

The honest live read is now sharper than before:

- the exact class-level bridge ingredients are real
- the simplest constant multiplicative effective-coupling lift is ruled out
- the minimal distinct connected shell is fixed exactly by the cube boundary
  theorem
- the first nonlocal full-vacuum coefficient is now fixed exactly by the mixed
  cumulant audit:
  `P_full(beta) = P_1plaq(beta) + beta^5 / 472392 + O(beta^6)`
- the exact implicit reduction law on the finite Wilson evaluation surface is
  now also closed and unique
- the exact nonperturbative susceptibility-flow law for that implicit reduction
  is now also closed
- the exact connected plaquette hierarchy governing that susceptibility flow is
  now also closed
- no exact finite-order connected-hierarchy truncation can close that object
- the exact equivalent generating object is now also closed as one compact
  plaquette spectral measure on each finite Wilson surface
- the current exact jet and structural theorems still do **not** determine a
  unique analytic framework-point value `P(6)`
- the plaquette generating object is now also explicit at the operator level:
  one positive one-clock Wilson transfer operator plus one exact self-adjoint
  `SU(3)` character-recurrence source operator
- the exact `beta = 6` source-sector transfer matrix elements are now also
  explicit in factorized form:
  `T_src(6) = exp(3 J) D_6 exp(3 J)`
- the exact local Wilson marked-link contribution is now also explicit:
  `D_6 = D_6^loc E_6` with `D_6^loc chi_(p,q) = a_(p,q)(6)^4 chi_(p,q)`
- so the remaining analytic target is explicit identification of the residual
  environment-response sequence `E_6`, equivalently the exact Perron state of
  the factorized operator after the local factor is stripped off, and
  therefore the explicit nonperturbative form of the reduction law at
  `beta = 6`, not the old
  constant-lift ansatz, not the onset coefficient, and not reduction-law
  existence, transport, hierarchy identification, generating-object existence,
  operator realization, or the broad operator-level underdetermination question
  itself

## Safe Reuse Rule

Downstream lanes may safely treat the following as canonical same-surface
evaluated quantities:

- `<P> = 0.5934`
- `u_0 = <P>^(1/4)`
- `alpha_s(v) = alpha_bare / u_0^2`

with the understanding that the number is:

- not structural in the same sense as an exact symmetry theorem
- not imported from experiment
- not a free parameter

## Scope

This note does **not** by itself upgrade the plaquette to a fully analytic
physical-vacuum theorem at the framework point `beta = 6`. It does not migrate
the full repo-wide numeric package from the historical same-surface value
`0.5934` to an analytic replacement.

It claims the narrower and sufficient point needed by the package:

> the plaquette is a uniquely determined observable of the retained theory,
> Monte Carlo is same-surface evaluation of that observable rather than
> parameter fitting, and the exact bridge-support stack materially narrows the
> remaining analytic insertion gap without yet closing it.
