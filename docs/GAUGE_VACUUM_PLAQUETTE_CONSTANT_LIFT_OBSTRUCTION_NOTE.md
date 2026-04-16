# Gauge-Vacuum Plaquette Constant-Lift Obstruction

**Date:** 2026-04-16
**Status:** exact obstruction on the constant-lift plaquette reduction ansatz
**Script:** `scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py`

## Question

Can the full interacting gauge-vacuum plaquette be exactly reduced by the
constant-lift law

`P(beta) = P_1plaq(Gamma beta)`

with

`Gamma = (3/2) (2 / sqrt(3))^(1/4)`?

## Answer

No.

That constant-lift law is incompatible with the exact strong-coupling slope of
the interacting Wilson plaquette observable.

So the current bridge stack does **not** close to a constant multiplicative
effective-coupling law. The remaining open object is narrower and more precise:

> if an exact full-vacuum reduction exists, it must be a nontrivial
> `beta`-dependent reduction law rather than the constant lift above.

## Theorem 1: the full interacting plaquette has exact strong-coupling slope `1/18`

For the Wilson gauge action

`Z(beta) = integral DU exp[(beta / 3) sum_p Re Tr U_p]`,

the plaquette expectation is

`P(beta) = <(1/3) Re Tr U_p>`.

Expand at small `beta`:

`exp[(beta / 3) sum_p Re Tr U_p] = 1 + (beta / 3) sum_p Re Tr U_p + O(beta^2)`.

At `beta = 0`, the zeroth-order plaquette average vanishes by Haar symmetry.
At first order, only the same plaquette survives the link integrations, so

`P(beta) = (beta / 9) integral dU (Re Tr U)^2 + O(beta^2)`.

Using Haar orthogonality:

`integral dU Tr U Tr U^dagger = 1`,

and

`integral dU (Tr U)^2 = integral dU (Tr U^dagger)^2 = 0`,

so

`integral dU (Re Tr U)^2 = 1 / 2`.

Therefore

`P(beta) = beta / 18 + O(beta^2)`.

That coefficient is exact for the interacting Wilson plaquette observable.

## Theorem 2: the local one-plaquette block has the same exact slope `1/18`

For the exact local block

`Z_1plaq(beta) = integral dU exp[(beta / 3) Re Tr U]`,

the exact local plaquette is

`P_1plaq(beta) = d/d beta log Z_1plaq(beta)`.

The same Haar computation gives

`P_1plaq(beta) = beta / 18 + O(beta^2)`.

So the local one-plaquette block and the full interacting Wilson plaquette have
the same exact strong-coupling slope.

## Corollary: any exact constant-lift reduction must have `Gamma = 1`

Assume

`P(beta) = P_1plaq(Gamma beta)`

with constant `Gamma`.

Then using Theorem 2,

`P(beta) = Gamma beta / 18 + O(beta^2)`.

But Theorem 1 gives

`P(beta) = beta / 18 + O(beta^2)`.

Therefore exact equality forces

`Gamma = 1`.

## Consequence for the current bridge candidate

The current bridge-support stack proposes the sharp candidate

`Gamma_cand = (3/2) (2 / sqrt(3))^(1/4) = 1.554921974442116`.

Since `Gamma_cand != 1`, the exact full-vacuum constant-lift law

`P(beta) = P_1plaq(Gamma_cand beta)`

cannot be true.

So the current analytic candidate remains useful support at `beta = 6`, but it
is not an exact reduction theorem.

## What remains open

This obstruction does **not** rule out analytic plaquette closure entirely.

It rules out only the simplest constant-lift ansatz.

The remaining exact target is now sharper:

> derive a nontrivial `beta`-dependent reduction law
> `P(beta) = P_1plaq(beta_eff(beta))`
> with
> `beta_eff'(0) = 1`
> and with the current bridge stack still explaining why
> `beta_eff(6)` lies close to
> `6 * (3/2) * (2 / sqrt(3))^(1/4)`.

## Why this is useful

This note upgrades the plaquette lane by removing one false closure route.

The live package no longer has to say merely:

> the final reduction is still open.

It can now say more sharply:

> the exact class-level bridge is closed, the naive constant-lift law is
> ruled out, and the remaining open object is a nontrivial `beta`-dependent
> full-vacuum reduction law.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=1 FAIL=0`
