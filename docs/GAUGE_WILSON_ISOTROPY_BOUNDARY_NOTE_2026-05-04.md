# Gauge Wilson Isotropy Boundary Note

**Date:** 2026-05-04
**Closure update:** 2026-05-06
**Type:** no_go
**Claim type:** no_go
**Claim scope:** route-specific exact negative boundary for the accepted
Wilson gauge-action isotropy surface: the two PR #528 mechanisms checked here
do not produce a spatial/temporal or orientation-dependent gauge-coupling
split, and therefore do not justify replacing the accepted isotropic Wilson
surface by a new anisotropic Wilson action.
**Status authority:** independent audit lane only. This source note proposes a
route-specific exact negative boundary; effective `retained_no_go` status
requires independent re-audit.
**Primary runner:** `scripts/frontier_gauge_wilson_isotropy_boundary_2026_05_04.py`

## Question

PR #528 asked whether the accepted Wilson gauge action should be changed or
re-described by a derived anisotropy. The repo governance constraint is that
review-loop must not add new axioms, new foundational premises, or new theory
language without explicit user approval.

Within that constraint, what exact boundary can be salvaged from the isotropy
discussion?

## Answer

Two narrow boundary checks close as a route-specific no-go:

1. The `Cl(3)` pseudoscalar squares to `-I` in the Pauli irrep, but it is
   central in odd-dimensional `Cl(3)` and therefore does not anticommute with
   the three spatial generators. It cannot by itself be used as a fourth
   Clifford generator forcing a new `Cl(3,1)` gauge-coupling ratio.
2. The standard staggered-eta product around all six plaquette orientations
   has the same sign. This check does not generate a spatial/temporal
   plaquette-weight split from an isotropic input lattice.

These checks support the exact negative boundary statement:

> on the accepted Wilson nearest-neighbor plaquette surface, the two PR #528
> mechanisms checked here do not derive orientation-dependent plaquette
> coefficients. They provide no basis for changing the accepted isotropic
> Wilson action or adding an anisotropy axiom.

## Closed Derivation

The target object is a Wilson plaquette action with orientation weights
`c_mu_nu` on the six plaquette orientations. A new anisotropic Wilson action
would require a derivation of unequal weights, for example a split between
spatial-spatial and spatial-temporal plaquettes. The accepted Wilson grammar
cited below supplies one common coefficient; this note only asks whether the
two proposed PR #528 mechanisms force a different coefficient pattern.

### 1. The `Cl(3)` pseudoscalar is not a fourth generator

Let `G_1, G_2, G_3` satisfy the `Cl(3)` relations

```text
{G_i, G_j} = 2 delta_ij I.
```

Set

```text
omega = G_1 G_2 G_3.
```

For any fixed `i`, moving `G_i` through the other two generators gives two
minus signs and therefore no net sign change. Using `G_i^2 = I`,

```text
omega G_i = G_i omega.
```

So `[omega, G_i] = 0` for all three spatial generators. In the Pauli irrep,
`omega = i I` and `omega^2 = -I`, matching the runner's pseudoscalar-square
check. But a fourth Clifford generator `T` capable of supplying an independent
time-like Clifford direction would need

```text
{T, G_i} = 0
```

for the three spatial generators. Since `omega` commutes with every `G_i`,

```text
{omega, G_i} = 2 omega G_i != 0.
```

Thus the `Cl(3)` pseudoscalar is a central complex-structure element on this
surface, not a standalone fourth anticommuting generator. It cannot force a
new temporal Clifford direction, and it cannot by itself derive an anisotropic
Wilson gauge-coupling ratio.

### 2. Staggered eta plaquette products are orientation-blind

Use the standard staggered phases on four directions:

```text
eta_0(x) = 1,
eta_mu(x) = (-1)^(x_0 + ... + x_{mu-1}) for mu > 0.
```

For `mu < nu`, the plaquette sign product is

```text
E_mu_nu(x)
  = eta_mu(x) eta_nu(x + e_mu) eta_mu(x + e_nu) eta_nu(x).
```

The factor `eta_mu` is independent of `x_nu`, so
`eta_mu(x + e_nu) = eta_mu(x)`. The factor `eta_nu` does depend on `x_mu`, so
`eta_nu(x + e_mu) = -eta_nu(x)`. Therefore

```text
E_mu_nu(x) = - eta_mu(x)^2 eta_nu(x)^2 = -1
```

for every site `x` and every one of the six orientations
`xy`, `xz`, `xt`, `yz`, `yt`, and `zt`.

An anisotropic Wilson action would need an orientation-dependent coefficient
pattern. The eta-product mechanism supplies the same factor `-1` on every
orientation, so it can at most multiply all six plaquette orientations by one
common sign. It does not generate a spatial/temporal plaquette-weight split.

### Boundary theorem

Combining the two checks:

1. the `Cl(3)` route supplies no fourth anticommuting generator;
2. the staggered eta route supplies no orientation-dependent plaquette factor;
3. the accepted Wilson source grammar already has one common coefficient on
   all six plaquette orientations.

Therefore these two PR #528 routes do not derive a new anisotropic Wilson
gauge action. The live action surface remains the accepted isotropic Wilson
surface unless a separate, explicitly approved theorem derives a different
orientation-dependent coefficient pattern.

## Relation To Existing Authority

[`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
states the accepted Wilson nearest-neighbor plaquette grammar with one common
coefficient across the six plaquette orientations. This note does not promote
that statement or re-axiomatize it. It records that two candidate mechanisms
from PR #528 do not force a different action surface.

[`GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)
also remains in force: response-ratio or scalar-bridge factors cannot be
reused as an exact constant action-coupling lift.

## Runner Result

Command:

```bash
python3 scripts/frontier_gauge_wilson_isotropy_boundary_2026_05_04.py
```

Expected summary:

```text
SUMMARY: PASS=19 FAIL=0
```

The runner verifies:

- the Pauli-irrep `Cl(3)` anticommutation relations;
- the `Cl(3)` pseudoscalar has square `-I`;
- the pseudoscalar commutes with each `Cl(3)` generator and so is not a
  standalone fourth anticommuting generator;
- all staggered eta-products around `xy`, `xz`, `xt`, `yz`, `yt`, and `zt`
  plaquettes equal `-1` on the tested parity cube.

## What This Does Not Close

This exact negative boundary does not prove a global no-go for every possible
spacetime-emergence route. A future retained-grade theorem could still derive
a metric ratio or a specific anisotropic Wilson action from an explicitly
approved and repo-conventional primitive.

Until such a theorem is reviewed and audited, the live boundary is:

- no repo-wide anisotropy axiom has been added;
- no new gauge-action language has been introduced;
- isotropic Wilson remains the scoped accepted surface already present in the
  plaquette stack;
- the analytic plaquette value at `beta = 6` remains open.
