# Gauge-Vacuum Plaquette Spatial Environment Transfer Theorem

**Date:** 2026-04-17
**Type:** positive_theorem
**Claim scope:** the structural existence of one positive self-adjoint
spatial transfer operator `S_beta^env` on the gauge-invariant boundary
Hilbert space of one orthogonal-direction slice of the unmarked spatial
Wilson environment, plus the boundary-amplitude realization formula
`z_(p,q)^env(beta) = <chi_(p,q), (S_beta^env)^(L_perp-1) eta_beta>` and
its dependency on the explicit upstream `tensor_transfer_theorem`
authority. The **explicit `beta = 6` matrix elements** of `S_beta^env`,
equivalently the **explicit Perron / boundary data of `S_6^env`**, are
**out of scope** here. The script is a finite class-sector witness only.
**Status:** audit pending. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline from `audit_status` +
`claim_type` + dependency chain; no author-side tier is asserted in source.
The current audit verdict is `audited_conditional` and audit-lane
ratification is required before any retained-grade status applies. The
verdict identifies the upstream `tensor_transfer_theorem` authority as
the unratified one-hop dependency.
**Script:** `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py`

## Question

After identifying the remaining plaquette datum as the boundary character
measure `Z_beta^env(W)` of the unmarked spatial Wilson environment, is that
still just one arbitrary central positive-type class function, or does the
accepted `3 spatial + 1 derived-time` geometry force a sharper operator
realization?

## Answer

It forces a sharper operator realization.

Because the marked plaquette spans exactly two spatial directions on the
accepted Wilson `3+1` source surface, there is one distinguished orthogonal
spatial direction. Slicing the unmarked spatial Wilson environment along that
orthogonal direction gives one exact positive self-adjoint spatial transfer
operator

`S_beta^env`

on the gauge-invariant boundary Hilbert space of one spatial slice through the
unmarked environment.

The environment boundary class function is therefore not an arbitrary central
positive-type class function. It is exactly a boundary amplitude of this
explicit transfer operator. After compression to the marked-plaquette
class-function sector, its character coefficients are exact transfer matrix
elements:

`z_(p,q)^env(beta) = <chi_(p,q), (S_beta^env)^(L_perp-1) eta_beta>`,

for one positive conjugation-symmetric boundary state `eta_beta` determined by
the local rim coupling of the marked plaquette.

So the remaining framework-point target is narrower than before:

> explicitly identify the `beta = 6` matrix elements of the spatial
> environment transfer operator, equivalently the `beta = 6` Perron / boundary
> data of `S_6^env`, rather than treating `rho_(p,q)(6)` as a generic free
> positive character sequence; the stronger explicit local matrix-element class
> is now carried by the tensor-transfer theorem.

## Setup

From the exact spatial-environment character-measure theorem already on
`main`:

- the residual source-sector environment operator is exactly the normalized
  boundary class function `C_(Z_beta^env)` of the unmarked spatial Wilson
  environment with fixed marked holonomy;
- the remaining exact coefficients are
  `rho_(p,q)(beta) = z_(p,q)^env(beta) / z_(0,0)^env(beta)`.

From the exact operator-realization and factorization stack already on `main`:

- the marked plaquette source sector lives on the accepted Wilson
  `3 spatial + 1 derived-time` surface;
- the marked plaquette spans exactly two spatial directions;
- therefore one orthogonal spatial direction remains available for a genuine
  environment-only slicing of the unmarked spatial Wilson sector.

## Theorem 1: exact orthogonal spatial slicing of the unmarked environment

Choose coordinates so the marked plaquette lies in the `(x,y)` plane. Then the
remaining unmarked spatial environment can be sliced along the orthogonal
spatial direction `z`.

Let `U_k` denote the gauge-invariant boundary data on the `k`-th `z`-slice of
the unmarked environment, with the marked plaquette boundary holonomy held
fixed.

Integrating the Wilson weight between adjacent slices defines one exact kernel

`K_beta^env(U_(k+1), U_k)`,

which is real and nonnegative.

By Haar invariance and reversal of the `z` orientation, this kernel is
symmetric in its two slice arguments. Hence it defines one positive
self-adjoint spatial transfer operator

`S_beta^env`

on the gauge-invariant slice Hilbert space of the unmarked environment.

## Theorem 2: exact boundary-amplitude realization of `Z_beta^env`

Let `eta_beta(W)` be the exact boundary state induced on one edge slice by the
local rim coupling of the marked plaquette holonomy `W` to the adjacent
unmarked spatial slice.

Then the full unmarked spatial environment with fixed marked holonomy `W`
reduces exactly to a boundary amplitude of the spatial transfer operator:

`Z_beta^env(W) = <eta_beta(W), (S_beta^env)^(L_perp-1) eta_beta(e)>`,

for the appropriate orthogonal spatial depth `L_perp`.

So `Z_beta^env` is not merely an abstract central positive-type class function.
It is an exact transfer amplitude of one explicit positive operator built from
the unmarked spatial Wilson environment.

## Theorem 3: exact character-coefficient matrix-element law

Compress `S_beta^env` to the marked-plaquette class-function sector. Because
the Wilson environment and the boundary coupling are invariant under
simultaneous conjugation of the marked holonomy, the compressed transfer law
preserves the central character basis `chi_(p,q)`.

Therefore the boundary character coefficients satisfy one exact matrix-element
law:

`z_(p,q)^env(beta) = <chi_(p,q), (S_beta^env)^(L_perp-1) eta_beta>`,

for one positive conjugation-symmetric boundary state `eta_beta`.

Equivalently,

`rho_(p,q)(beta)
 = <chi_(p,q), (S_beta^env)^(L_perp-1) eta_beta>
   / <chi_(0,0), (S_beta^env)^(L_perp-1) eta_beta>`.

So the remaining exact object is no longer a generic normalized positive
sequence. It is the normalized boundary matrix-element sequence of one
explicit positive spatial transfer operator.

## Corollary 1: exact narrowing of the live plaquette gap

At the framework point `beta = 6`, the remaining constructive plaquette target
is exactly:

- the boundary matrix elements of `S_6^env` on the marked class-function
  sector,
- or equivalently the boundary-state / Perron data of that explicit spatial
  transfer operator.

This is sharper than the previous live phrasing
"explicit boundary character data `rho_(p,q)(6)`" because it fixes the exact
operator class from which those coefficients must arise.

## What this closes

- exact spatial transfer-operator realization of the unmarked spatial Wilson
  environment on the accepted `3+1` surface
- exact reduction of `Z_beta^env` to a boundary amplitude of one positive
  self-adjoint spatial transfer operator
- exact realization of the boundary character coefficients as transfer matrix
  elements rather than as a generic positive central sequence
- exact narrowing of the remaining framework-point plaquette target to
  explicit `beta = 6` spatial-transfer matrix elements / Perron data

## What this does not close

- explicit matrix elements of `S_6^env`
- explicit coefficients `rho_(p,q)(6)` of `Z_6^env`
- explicit `beta = 6` Perron moments after the spatial environment transfer is
  fully included
- analytic closure of canonical `P(6)`
- repo-wide repinning of the canonical plaquette

## Script boundary

The theorem above is structural. The companion runner is only a finite
class-sector witness for positivity, conjugation symmetry, and boundary-state
compatibility on a truncated transfer example. It is not itself the explicit
`beta = 6` spatial environment solve.

The fully explicit local matrix-element class is now carried separately by:

- [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md)

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=3 FAIL=0`

## Out of scope (admitted-context to this note)

The following items are explicitly **NOT** load-bearing claims of this
note. They depend on separate authority rows / open derivations and
enter only as admitted-context. Per the audit verdict on this row,
items (1)-(2) below are the **specific** unclosed dependencies the
audit lane identifies:

1. **Tensor-transfer theorem upstream.** The fully constructive
   matrix-element packet for `S_beta^env` passes through
   [`GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md`](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md),
   which is itself currently `audited_conditional`. This note imports
   that authority as a structural one-hop dep and does not derive its
   matrix-element content here.

2. **Explicit `beta = 6` Perron / boundary data.** The matrix elements
   of `S_6^env` on the marked class-function sector — equivalently the
   `beta = 6` Perron eigenvector / boundary state of the spatial
   transfer operator — are **not** derived in this note. They remain
   the audit lane's identified open object for the framework-point
   plaquette target.

3. **Reference Perron solves at structural `rho` hypotheses.** Any
   numerical Perron solves cited in cross-referenced support notes
   under `rho = 1` or `rho = delta_{(p,q),(0,0)}` are
   audit-comparator readouts under explicit structural input
   hypotheses, not load-bearing physical claims of this note.

The in-scope content of this note is the **structural existence** of
the spatial transfer operator `S_beta^env` and the **boundary-amplitude
realization formula** for `Z_beta^env`, conditional on the upstream
tensor-transfer theorem authority. Theorems 1, 2, 3 plus Corollary 1
are the in-scope content.
