# Gauge-Vacuum Plaquette Spatial Environment Tensor-Transfer Theorem

**Date:** 2026-04-17
**Type:** positive_theorem
**Claim scope:** the structural identification of the spatial-environment
boundary data as arising from one positive character-tensor transfer built
from exact `SU(3)` Wilson character coefficients `c_lambda(beta)` and exact
`SU(3)` fusion intertwiners — at the level of named local ingredients and
finite truncated support. The **full untruncated tensor-transfer operator
construction at `beta = 6`** (the explicit Perron solve, the convergence /
positivity proof beyond truncated support, and the named-tensor-word check
beyond one example) is **out of scope** here. The script is a finite
truncated support packet only.
**Status:** independent audit required. Under the scope-aware classification
framework, ratified status is computed by the audit pipeline from audit lane
data and the dependency chain; no author-side tier is asserted in source.
**Script:** `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py`

## Question

After reducing the remaining plaquette gap to the unmarked spatial environment,
can the `beta = 6` boundary character data be tied to explicit local Wilson
building blocks rather than left as an abstract positive transfer amplitude?

## Answer

Yes.

On the accepted Wilson `3 spatial + 1 derived-time` source surface, expand each
unmarked spatial plaquette Boltzmann factor in exact `SU(3)` characters,

`exp[(beta/3) Re Tr U_p] = sum_lambda d_lambda c_lambda(beta) chi_lambda(U_p),`

with explicit nonnegative Wilson coefficients `c_lambda(beta)`.

Slice the unmarked spatial environment along the one orthogonal remaining
spatial direction. On each slice interface, integrate the shared spatial links
by Haar orthogonality / Peter-Weyl decomposition. The resulting slice-to-slice
transfer matrix elements are then finite sums of products of:

- explicit Wilson coefficients `c_lambda(beta)`,
- exact nonnegative `SU(3)` fusion / intertwiner multiplicities.

So the remaining spatial-environment boundary character data are not generic
positive amplitudes. They are one explicit positive character-tensor transfer
law on the marked class-function sector.

At `beta = 6`, the remaining constructive target is therefore:

> explicitly evaluate the resulting tensor-transfer matrix elements, or the
> equivalent Perron state of the explicit tensor-transfer operator built from
> `c_lambda(6)` and exact `SU(3)` intertwiners.

## Setup

From the exact transfer-operator / character-recurrence theorem already on
`main`:

- the plaquette source sector carries the exact self-adjoint source operator
  `J = (chi_(1,0) + chi_(0,1)) / 6`;
- the marked plaquette source lives on the `SU(3)` dominant-weight class basis;
- multiplication by `chi_(1,0)` and `chi_(0,1)` closes exactly on the
  dominant-weight graph through the standard six-neighbor recurrence.

From the exact local/environment factorization theorem already on `main`:

- the one-link Wilson class function has exact character coefficients
  `a_(p,q)(beta)`;
- the normalized marked local mixed-kernel factor is already explicit and exact.

From the exact residual-environment identification and spatial-environment
character-measure theorems already on `main`:

- the remaining operator is exactly the unmarked spatial environment
  `R_beta^env = C_(Z_beta^env)`;
- the open data are exactly the coefficients `rho_(p,q)(beta)` of the
  boundary class function `Z_beta^env`.

## Theorem 1: exact local Wilson tensor weights

For every irrep `lambda = (p,q)`, the one-link Wilson class function admits the
exact character expansion

`exp[(beta/3) Re Tr U] = sum_lambda d_lambda c_lambda(beta) chi_lambda(U),`

with

- `c_lambda(beta) >= 0`,
- `c_(p,q)(beta) = c_(q,p)(beta)`.

At `beta = 6`, these coefficients are explicit through the Bessel-determinant
mode sums already used in the local plaquette packet.

So the local plaquette weights entering the spatial environment are fully
explicit on the accepted surface.

## Theorem 2: exact slice integration gives fusion/intertwiner contractions

Slice the unmarked spatial environment along the orthogonal spatial direction.
For one slice step, expand every spatial plaquette factor in characters and
integrate all shared slice links.

By Haar orthogonality and Peter-Weyl decomposition, every resulting matrix
element between boundary class states is a finite sum of products of:

- the explicit local Wilson coefficients `c_lambda(beta)`,
- exact nonnegative integer fusion/intertwiner multiplicities from `SU(3)`.

Therefore the spatial environment transfer matrix on the marked class-function
sector is an exact positive tensor-transfer operator.

## Theorem 3: exact boundary-character generation by the tensor-transfer law

Let `T_beta^env,tensor` denote the resulting compressed spatial environment
tensor-transfer operator on the marked class-function sector, and let
`eta_beta^env` denote the exact positive boundary state induced by the rim
coupling of the marked plaquette to the unmarked environment.

Then the unmarked spatial boundary character coefficients satisfy

`z_(p,q)^env(beta)
  = <chi_(p,q), (T_beta^env,tensor)^(L_perp-1) eta_beta^env>,`

and hence

`rho_(p,q)(beta)
  = z_(p,q)^env(beta) / z_(0,0)^env(beta)`

is the normalized tensor-transfer boundary amplitude sequence of this explicit
positive operator.

So the remaining framework-point plaquette object is now sharper than
"some positive spatial transfer amplitude law." It is:

- one explicit positive character-tensor transfer operator,
- built from exact Wilson coefficients and exact `SU(3)` intertwiners,
- whose Perron / boundary data at `beta = 6` remain to be evaluated.

## Corollary 1: the current gap is no longer hidden in operator class freedom

The remaining open object is not:

- the existence of a transfer law,
- the local Wilson coefficient stack,
- the source recurrence,
- or the generic positivity class of the environment amplitudes.

It is specifically:

- explicit evaluation of the `beta = 6` tensor-transfer matrix elements,
- equivalently the exact `beta = 6` Perron state / boundary moments of the
  explicit tensor-transfer operator.

## What this closes

- exact realization of the residual spatial environment as a tensor-transfer
  law built from explicit Wilson character coefficients and exact `SU(3)`
  fusion/intertwiner data
- exact clarification that the remaining plaquette gap is an explicit
  tensor-transfer Perron solve at `beta = 6`, not generic boundary-sequence
  freedom
- exact upgrade of the spatial-environment packet from "positive transfer law"
  to "explicit local tensor-transfer class"

## What this does not close

- explicit evaluated tensor-transfer matrix elements at `beta = 6`
- explicit `rho_(p,q)(6)` values
- explicit Perron moments after the full spatial environment is included
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Script boundary

The theorem above is structural and exact. The linked runner is intentionally a
finite support packet only:

- it audits a truncated dominant-weight box with `NMAX = 4`,
- it truncates the Wilson Bessel mode sum at `MODE_MAX = 80`,
- it checks one explicit positive tensor-transfer word built from those exact
  local ingredients,
- it does **not** evaluate the full `beta = 6` tensor-transfer matrix
  elements,
- it does **not** compute the `beta = 6` Perron state or the boundary
  coefficients `rho_(p,q)(6)`.

So the script is evidence for the explicit local Wilson coefficient stack and
the tensor-transfer class, not a numerical closure of the remaining
environment solve.

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`

## Out of scope (admitted-context to this note)

The following items are explicitly **NOT** load-bearing claims of this
note. They depend on separate authority rows / open derivations / open
construction work and enter only as admitted-context:

1. **Full untruncated tensor-transfer operator at `beta = 6`.** The
   exact untruncated construction (positivity, convergence, full
   support beyond `NMAX = 4`, full Bessel-mode sum beyond
   `MODE_MAX = 80`) is not constructed or checked here.

2. **`beta = 6` tensor-transfer Perron solve.** The explicit `beta = 6`
   matrix elements, Perron state, and boundary coefficients
   `rho_(p,q)(6)` are **not** computed here. The script is a finite
   truncated support packet only.

3. **Multi-tensor-word generalization.** The runner verifies one
   explicit positive tensor-transfer word; the general case beyond
   that example is asserted but not exhaustively enumerated.

The **in-scope content** of this note is the structural
character-tensor-transfer identification — the named local ingredients
(Wilson character coefficients `c_lambda(beta)`, `SU(3)` fusion
intertwiners) and the finite truncated support packet that exhibits
their consistency under one tensor word. Theorems that depend on the
full untruncated construction at `beta = 6` are out of scope here and
must cite the unresolved open object directly.
