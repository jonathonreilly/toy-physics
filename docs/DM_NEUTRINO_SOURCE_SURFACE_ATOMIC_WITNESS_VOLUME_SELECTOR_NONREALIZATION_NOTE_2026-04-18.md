# DM Neutrino Source-Surface Atomic Witness-Volume Selector Nonrealization

**Date:** 2026-04-18  
**Status:** support - structural or confirmatory support note
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_atomic_witness_volume_selector_nonrealization.py`

## Question

After full-family descent to the canonical rank-one positive-probe family, does
the current exact bank already force a unique threshold-volume selector?

## Bottom line

No.

Fix one common positive comparison window

```text
A_mu(H) = H + mu I > 0
```

on the recovered bank, and define the full-family threshold witness-volume
field

```text
V_tau(H)
  = Vol{P rank-one positive : W(A_mu(H); P) >= tau}
```

using the unitary-invariant probability measure on the full rank-one family.

This field is already:

- exact,
- intrinsic / basis-free,
- presentation-blind,
- and fully determined by the atomic singleton response field.

But minimizing `V_tau` on the recovered bank does **not** pick one stable
winner:

- at `tau = 0.13`, the unique minimum is recovered lift `1`,
- at `tau = 0.14`, the unique minimum is recovered lift `0`.

So even after full-family descent to this intrinsic selector family, the
current exact bank still does not force a unique value. The remaining selector
datum is now sharper: it is an **intrinsic threshold law**, not generic family
choice.

## Exact theorem shape

Let the positive eigenvalues of `A_mu(H)` be

```text
lambda_1 <= lambda_2 <= lambda_3
```

and write

```text
a = 1/lambda_1,  b = 1/lambda_2,  g = 1/lambda_3
```

so `a >= b >= g > 0`.

For a rank-one probe `P = |u><u|`, the exact response is

```text
W(A_mu(H); P) = log(1 + u^* A_mu(H)^(-1) u).
```

In the eigenbasis of `A_mu(H)`, if `p_i = |u_i|^2`, then the Haar law on the
complex projective rank-one family pushes forward to the uniform
`Dirichlet(1,1,1)` law on the simplex

```text
p_1 + p_2 + p_3 = 1,  p_i >= 0.
```

So the witness event

```text
W(A_mu(H); P) >= tau
```

is exactly the simplex half-plane cut

```text
a p_1 + b p_2 + g p_3 >= c,   c = exp(tau) - 1.
```

Therefore `V_tau(H)` is an exact piecewise-quadratic function:

```text
V_tau(H) = 1,                                         c <= g
V_tau(H) = 1 - (c-g)^2 / ((a-g)(b-g)),               g < c <= b
V_tau(H) = (a-c)^2 / ((a-b)(a-g)),                   b < c < a
V_tau(H) = 0,                                         c >= a
```

This uses only the atomic singleton response field.

## Recovered-bank flip

On the recovered bank, the exact threshold-volume values are:

At `tau = 0.13`:

```text
V_0.13 = [
  0.968800060485,
  0.962763473368,
  0.966503874340,
  0.976434649984,
  0.996932254453
]
```

So the unique minimum is lift `1`.

At `tau = 0.14`:

```text
V_0.14 = [
  0.863786803367,
  0.918633276346,
  0.926735302209,
  0.952120950531,
  0.994318948728
]
```

So the unique minimum is lift `0`.

Therefore the current exact bank does not force a unique threshold-volume
selector winner without an intrinsic threshold law.

## Consequence

This is stronger than the earlier generic selector-side obstruction phrasing.

The selector-side non-closure is no longer just:

- “maybe some other family-level scalarization exists.”

It is now:

- the full canonical rank-one family already gives an exact intrinsic
  threshold-volume selector family,
- and the current exact bank still does not determine which threshold should
  be used.

So the remaining selector-side positive theorem target is sharper:

1. derive an intrinsic threshold law; or
2. prove a current-bank no-go that no such law is forced on the retained stack.

## Boundary

This theorem does **not** rule out a future theorem deriving one distinguished threshold
from stronger microscopic structure.

It is a current-bank nonrealization theorem only.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_atomic_witness_volume_selector_nonrealization.py
```
