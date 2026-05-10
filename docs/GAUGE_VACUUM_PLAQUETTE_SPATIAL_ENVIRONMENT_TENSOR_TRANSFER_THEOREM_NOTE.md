# Gauge-Vacuum Plaquette Spatial Environment Tensor-Transfer Theorem

**Date:** 2026-04-17 (originally); 2026-05-10 narrowed to bounded_theorem
on the truncated finite packet per the `codex-fresh-agent-rawls-2026-05-02`
re-audit (2026-05-10 verdict)'s "split the finite packet into a bounded
theorem" repair path.
**Type:** bounded_theorem
**Claim scope (post-2026-05-10 narrowing):** the structural identification
of the spatial-environment boundary data as arising from one positive
character-tensor transfer built from exact `SU(3)` Wilson character
coefficients `c_lambda(beta)` and exact `SU(3)` fusion intertwiners,
**bounded to the finite truncated support actually verified by the
runner**: dominant-weight box `NMAX = 4`, Wilson Bessel mode sum
`MODE_MAX = 80`, one explicit positive tensor-transfer word. Under that
truncation, the load-bearing identification (Theorem 3) closes as a
class-A algebraic identity over the retained local ingredients named in
§"Setup". The **full untruncated tensor-transfer operator construction
at `beta = 6`** (the explicit Perron solve, the convergence/positivity
proof beyond truncated support, and the named-tensor-word check beyond
one example) is explicitly **not** in scope of this bounded theorem; it
remains the open target named in §"What this does not close".
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane. The
`bounded_theorem` label is a source-side claim-boundary declaration,
not an audit verdict; the 2026-05-10 audit verdict on the prior
`positive_theorem` framing recorded `audited_conditional` (chain_closes
False because the load-bearing bridge from local Wilson ingredients to
the FULL unmarked spatial environment was admitted out of scope). This
scope narrowing implements the named conditional repair path "split the
finite packet into a bounded theorem".
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

## Theorem 3 (truncated): bounded boundary-character generation by the tensor-transfer law on the truncated packet

**Bounded scope.** This theorem is stated and verified on the truncated
finite packet specified in §"Script boundary": dominant-weight box
`NMAX = 4`, Wilson Bessel mode sum `MODE_MAX = 80`, and the one
explicit positive tensor-transfer word checked by the runner. The
extension to the full untruncated case at `beta = 6` (Perron solve,
convergence/positivity beyond truncation, multi-tensor-word coverage)
is the open positive-theorem target named in §"What this does not
close" and is **not** load-bearing for this bounded theorem.

Let `T_beta^env,tensor` denote the resulting compressed spatial
environment tensor-transfer operator on the marked class-function
sector built from the truncated local ingredients (`c_lambda(beta)`
truncated to `NMAX = 4` weight box and `MODE_MAX = 80` Bessel sum,
`SU(3)` fusion intertwiners on that box), and let `eta_beta^env`
denote the corresponding truncated positive boundary state.

Then on the truncated packet, for the one explicit tensor word `W^*`
verified by the runner, the unmarked spatial boundary character
coefficients restricted to the truncation satisfy

```text
z_(p,q)^env,trunc(beta; W^*)
   =  <chi_(p,q), (T_beta^env,tensor)^(L_perp-1) eta_beta^env>     restricted
                                                                   to the
                                                                   truncated
                                                                   packet,
```

and hence

```text
rho_(p,q)^trunc(beta; W^*)
   =  z_(p,q)^env,trunc(beta; W^*) / z_(0,0)^env,trunc(beta; W^*)
```

is the normalized tensor-transfer boundary amplitude sequence of this
explicit positive operator **on the truncated packet, for the one
tested tensor word**. The chain closes as a class-A algebraic identity
over the retained truncated local ingredients (Wilson character
coefficients in the `NMAX = 4` weight box at `MODE_MAX = 80` Bessel
support, plus `SU(3)` fusion intertwiners on that box).

**Bounded statement.** Under the truncation, the remaining
framework-point plaquette object is sharper than "some positive
spatial transfer amplitude law." On the truncated packet it is:

- one explicit positive character-tensor transfer operator (truncated),
- built from exact Wilson coefficients and exact `SU(3)` intertwiners
  on the finite weight box and Bessel mode sum,
- whose Perron / boundary data at `beta = 6` remain to be evaluated
  beyond the truncation (open positive-theorem target).

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

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named
by prior conditional audits so the audit citation graph can track them.
It does not promote this note, change the audited claim scope, or close
the open positive-theorem bridge.

The 2026-05-10 audit verdict (re-audit of the prior `positive_theorem`
framing) named the load-bearing gap as the bridge from local
character/fusion ingredients to the actual full unmarked spatial-
environment boundary amplitudes. The auditor offered two repair paths:
(a) supply the audited construction of the full untruncated
tensor-transfer operator and boundary state with convergence/positivity
and multi-tensor-word coverage, OR (b) split the finite packet into a
bounded theorem. **This note implements path (b)** via the 2026-05-10
narrowing recorded in the header: the load-bearing claim (Theorem 3) is
now scoped to the truncated finite packet (`NMAX = 4`, `MODE_MAX = 80`,
one tested tensor word), and the full untruncated case at `beta = 6`
remains the open positive-theorem target named in §"What this does not
close". The chain now closes as a class-A algebraic identity over the
retained truncated local ingredients.

A bounded partial input now exists on the single-link side:

- [gauge_vacuum_plaquette_rho_pq6_wilson_environment_bounded_note_2026-05-09](GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md) (`audited_clean` / `retained_bounded`) computes the bounded normalized single-link Wilson boundary coefficients `rho_(p,q)(6) = c_(p,q)(6) / (d_(p,q) c_(0,0)(6))` on the finite weight box `0 <= p,q <= 4` by two independent integrators (Schur-Weyl Bessel-determinant and Weyl-Cartan torus integration). This is bounded support for the single-link factor `c_lambda(6)` referenced in Theorem 1 above, on the finite box only.

This bounded input does **not** supply: the all-weight closed form, the
full untruncated tensor-transfer operator at `beta = 6`, multi-tensor-
word generalization, or the `beta = 6` Perron state of the full spatial
environment. Those gaps remain the open positive-theorem target stated
in the existing "What this does not close" and "Out of scope" sections
of this note. The 2026-05-10 narrowing relabels them from "implicitly
out of scope" to "explicitly out of the bounded scope" — the load-
bearing identification of this note is now restricted to the truncated
finite packet only.
