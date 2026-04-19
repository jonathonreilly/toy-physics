# Quark Endpoint Ratio-Chain Law

**Date:** 2026-04-19  
**Status:** theory-first bounded endpoint-ratio-chain candidate  
**Primary runner:** `scripts/frontier_quark_endpoint_ratio_chain_law.py`

## Safe statement

The endpoint-quotient law already reduced the remaining `E`-channel primitive
to the candidate

```text
gamma_E(center)/gamma_E(shell) = 15/8.
```

This note goes one step more structural.

On the live endpoint data, three simpler endpoint ratios are all nearest to
small rationals:

```text
gamma_T(center)/gamma_T(shell) = 5/6
gamma_T(shell)/gamma_E(shell)  = -2
gamma_T(center)/gamma_E(center)= -8/9
```

These imply

```text
gamma_E(center)/gamma_E(shell)
  = [gamma_E(center)/gamma_T(center)]
    [gamma_T(center)/gamma_T(shell)]
    [gamma_T(shell)/gamma_E(shell)]
  = (-9/8) * (5/6) * (-2)
  = 15/8.
```

So the current best theory-first bounded endpoint law is no longer just one
quotient. It is a **ratio chain**:

```text
{5/6, -2, -8/9} => 15/8 => r_E = 21/4 => D_E = 21/8.
```

This is still bounded, not retained.

## 1. Exact endpoint chain identity

The endpoint coefficients already satisfy exact identities:

```text
r_E = 6 * (gamma_E(center)/gamma_E(shell) - 1)
r_T = 6 * (gamma_T(center)/gamma_T(shell) - 1).
```

And the `E` quotient itself factors exactly as

```text
gamma_E(center)/gamma_E(shell)
  = [gamma_E(center)/gamma_T(center)]
    [gamma_T(center)/gamma_T(shell)]
    [gamma_T(shell)/gamma_E(shell)].
```

So once three endpoint ratios are selected, the `E` quotient is fixed.

## 2. Controlled small-rational candidates

Inside the same low-rational endpoint class used on this branch, the nearest
candidates are:

- `gamma_T(center)/gamma_T(shell) = 5/6`
- `gamma_T(shell)/gamma_E(shell) = -2`
- `gamma_T(center)/gamma_E(center) = -8/9`

The first was already structurally privileged by the exact-support `T` law.
The new science is that the two `T/E` endpoint ratios also collapse to very
small rational candidates.

## 3. Implied E-channel law

Those three candidates force:

```text
gamma_E(center)/gamma_E(shell) = 15/8
```

and therefore

```text
r_E = 6 * (15/8 - 1) = 21/4.
```

So the earlier standalone `15/8` law is no longer an isolated rationalization.
It is the exact output of a smaller endpoint-ratio chain.

## 4. Anchored denominator candidate

Using the live shell-multiplicity candidate

```text
a_T / a_E = -2
```

together with the exact-support `T` law

```text
r_T = -1,
```

the ratio chain implies

```text
|b_E / b_T| = 21/8.
```

This remains very close to the live bounded denominator and lands on the same
anchored quark branch.

## Honest endpoint

The theorem-grade target is now narrower than before.

It is no longer simply:

> derive `gamma_E(center)/gamma_E(shell) = 15/8`.

It is:

> derive the exact endpoint ratio chain
> `{5/6, -2, -8/9}`
> from the exact Route-2 tensor observable.

If that lands, the bounded `E`-channel quotient law, the `r_E = 21/4` law,
and the anchored denominator candidate `D_E = 21/8` all follow immediately.

## Validation

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_endpoint_ratio_chain_law.py
```

Current expected result on this branch:

- `frontier_quark_endpoint_ratio_chain_law.py`: `PASS=14 FAIL=0`
