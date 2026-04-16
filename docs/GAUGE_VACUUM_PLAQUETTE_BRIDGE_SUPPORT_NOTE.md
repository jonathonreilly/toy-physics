# Gauge-Vacuum Plaquette Scalar-Bridge Support

**Date:** 2026-04-16
**Status:** exact local/source/class-level support stack plus exact constant-lift obstruction and exact distinct-shell theorem; the final physical-vacuum reduction remains open
**Scripts:** `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py`, `scripts/frontier_scalar_3plus1_temporal_ratio.py`, `scripts/frontier_gauge_scalar_temporal_completion_theorem.py`, `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py`, `scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py`

## Question

How much of the plaquette bridge is actually closed on `main`, and what still
prevents a full analytic promotion of the physical gauge-vacuum plaquette?

## Answer

The bridge is materially stronger, but not fully closed.

What is exact now:

1. **Local Wilson source-response on the one-plaquette block.**
   The one-plaquette expectation is exactly the source derivative of the local
   Wilson scalar generator
   `W_loc(j) = log Z_1plaq(beta+j) - log Z_1plaq(beta)`.
2. **Exact accepted gauge-source temporal completion law.**
   On the accepted Wilson nearest-neighbor local bosonic scalar gauge-source
   class, the normalized endpoint ratio is exactly
   `A_inf / A_2 = 2 / sqrt(3)`.
3. **Exact plaquette four-link coupling map.**
   Under a uniform link rescaling one has the exact algebraic identity
   `P(u_0 V) = u_0^4 P(V)`.
4. **Exact `3+1` incidence factor.**
   On the hypercubic `3+1` lattice, `Gamma_coord = 6 / 4 = 3 / 2`.

What is **not** closed by those facts alone is the final physical statement

`P(beta) = P_1plaq(beta * (3/2) * (2 / sqrt(3))^(1/4))`

for the interacting gauge vacuum.

In fact, the live repo now proves that this exact **constant-lift** law cannot
hold on the full interacting Wilson surface, because the full-vacuum
strong-coupling slope is exactly `1/18` while the constant-lift ansatz would
force the slope to be

`[(3/2) (2 / sqrt(3))^(1/4)] / 18`.

So the remaining open object is not a generic missing lift anymore. It is a
more specific target:

> derive a nontrivial `beta`-dependent full-vacuum reduction law.

## Exact support piece 1: local Wilson source-response

For the one-plaquette Wilson weight

`Z_1plaq(beta) = integral dU exp[(beta / 3) Re Tr U]`,

the source-deformed local scalar generator is

`W_loc(j) = log Z_1plaq(beta+j) - log Z_1plaq(beta)`.

Its source derivative is exactly the local plaquette expectation:

`dW_loc/dj |_(j=0) = d/d(beta) log Z_1plaq(beta) = P_1plaq(beta)`.

So the plaquette is exactly the local bosonic scalar source-response
coefficient of the Wilson block.

## Exact support piece 2: accepted gauge-source temporal completion law

The bridge factor is no longer tied only to one chosen scalar toy kernel.

On the accepted Wilson nearest-neighbor plaquette surface:

- one common source weight across the six plaquette orientations induces equal
  directional coefficients on `x,y,z,t`;
- on the minimal APBC `L_s = 2` spatial cube, every accepted local bosonic
  scalar gauge source therefore reduces exactly to
  `K_O(omega) = 3w (3 + sin^2 omega)`;
- so the normalized endpoint ratio is universal on the accepted gauge-source
  class:
  `A_inf / A_2 = 2 / sqrt(3)`.

Authorities:

- [GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md](./GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
- [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](./SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)

This closes the class-level temporal bridge. It still does **not** by itself
reduce the full interacting gauge-vacuum observable to the local one-plaquette
response.

## Exact support piece 3: plaquette four-link coupling map

Let

`P(U) = (1/3) Re Tr(U_1 U_2 U_3^dag U_4^dag)`

be the oriented plaquette density. Under a uniform link rescaling

`U_mu = u_0 V_mu`,

one has exactly

`P(U) = u_0^4 P(V)`.

So the plaquette is an exact **four-link** local scalar density. This fixes the
natural scalar-density exponent to the fourth root on any route that already
proves the bridge acts through a uniform scalar-density normalization.

That is strong support. It is not yet a proof that the interacting gauge vacuum
must inherit the scalar bridge in exactly that way.

## Exact support piece 4: `3+1` incidence factor

On the hypercubic `3+1` lattice:

- each link lies in `3` coordinate planes
- each plane contributes `2` plaquettes touching that link

So each link lies in `6` plaquettes, while each plaquette contains `4` links.
Therefore

`Gamma_coord = 6 / 4 = 3 / 2`.

Again, this is exact combinatorics. What remains open is the unique reduction
law taking this factor into the full interacting plaquette expectation.

## Exact obstruction to the naive constant-lift law

The live repo now also carries an exact obstruction theorem:

- [GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)

The exact facts are:

- the full interacting Wilson plaquette has strong-coupling slope
  `P(beta) = beta / 18 + O(beta^2)`;
- the local one-plaquette block also has slope `beta / 18 + O(beta^2)`;
- therefore any exact constant-lift law
  `P(beta) = P_1plaq(Gamma beta)`
  must have `Gamma = 1`.

Since the bridge candidate uses

`Gamma_cand = (3/2) (2 / sqrt(3))^(1/4) = 1.554921974442116`,

that constant-lift law is ruled out exactly.

So the bridge stack now supports two honest statements at once:

1. the class-level temporal bridge is exact;
2. the naive constant multiplicative lift is not the full interacting answer.

## Current best analytic candidate

If one composes the exact local/source/class-level pieces above, the sharp current
analytic candidate is

`beta_eff = beta * (3/2) * (2 / sqrt(3))^(1/4)`

and therefore

`P_cand(beta) = P_1plaq(beta_eff)`.

At the framework point `beta = 6`:

- `beta_eff = 9.329531846652698`
- `P_cand(6) = 0.593530679977098`
- `u_0,cand = P_cand^(1/4) = 0.877729698485538`

This sits only `1.3068e-4` (`0.022%`) above the current canonical same-surface
value `0.5934`, so it remains a very strong support candidate at the framework
point `beta = 6`.

The new exact distinct-shell theorem now fixes the minimal connected shell
geometry built from distinct plaquettes:

- the first distinct connected numerator shell is order `beta^5`;
- the first connected vacuum shell is order `beta^6`.

## Remaining gap

The remaining theorem-grade gap is now sharper:

> perform the mixed repeated-plaquette connected-cumulant audit and derive the
> exact higher-order coefficients of the nontrivial reduction law
> `P(beta) = P_1plaq(beta_eff(beta))`,
> rather than the now-ruled-out constant lift
> `beta_eff(beta) = beta * (3/2) * (2 / sqrt(3))^(1/4)`.

Until that step is closed, the live package should keep the plaquette as:

- exact local/source/class-level support stack plus
- exact obstruction to the naive constant-lift law plus
- canonical same-surface evaluated value on the live quantitative surface

## Honest status on `main`

Current clean read:

- exact local/source/class-level ingredients: closed
- exact constant-lift obstruction: closed
- exact distinct-shell theorem: closed
- full physical-vacuum reduction to the local one-plaquette response: still open
- canonical plaquette on the live package: still `0.5934`

So there is **not** yet a basis for repo-wide numeric migration or for removing
the residual “same-surface evaluated” language from downstream quantitative
lanes.

## Commands run

```bash
python3 scripts/frontier_scalar_3plus1_temporal_ratio.py
python3 scripts/frontier_gauge_scalar_temporal_completion_theorem.py
python3 scripts/frontier_gauge_vacuum_plaquette_bridge_support.py
python3 scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py
python3 scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py
```

Expected summary:

- scalar ratio runner: `EXACT PASS=4 SUPPORT=1 FAIL=0`
- gauge scalar completion runner: `PASS=8 FAIL=0`
- bridge support runner: `EXACT PASS=6 SUPPORT=2 FAIL=0`
- distinct-shell runner: `THEOREM PASS=6 SUPPORT=1 FAIL=0`
- constant-lift obstruction runner: `THEOREM PASS=6 SUPPORT=1 FAIL=0`
