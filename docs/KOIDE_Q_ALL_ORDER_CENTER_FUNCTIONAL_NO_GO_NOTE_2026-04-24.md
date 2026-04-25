# Koide Q all-order center-functional source no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_all_order_center_functional_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Extend source-grammar exhaustion to all-order analytic C3-equivariant center
functionals:

```text
analytic equivariant center source
  -> equal center labels
  -> K_TL = 0.
```

## Executable theorem

Any such source reduces on the two retained central blocks to positive scalar
values:

```text
F_plus
F_perp.
```

After normalization:

```text
u = F_plus / (F_plus + F_perp).
```

The runner verifies:

```text
K_TL = 0 <=> F_plus = F_perp.
```

The strengthened runner also spells this out in functional-calculus form.  For
the retained central involution

```text
Z = P_plus - P_perp,
Z^2 = 1,
```

an analytic source function satisfies:

```text
F(Z) = F(1) P_plus + F(-1) P_perp.
```

For an arbitrary analytic truncation,

```text
F(1)  = F_even + F_odd
F(-1) = F_even - F_odd.
```

Thus the closing condition is exactly:

```text
F_odd = 0.
```

## Obstruction

Analyticity and equivariance do not equalize the two inequivalent retained
real-isotype blocks.  Positive all-order values realize both closing and
non-closing states:

```text
F = (1/3, 2/3) -> u = 1/3, Q = 1,   K_TL = 3/8
F = (1/2, 1/2) -> u = 1/2, Q = 2/3, K_TL = 0
F = (2/3, 1/3) -> u = 2/3, Q = 1/2, K_TL = -3/8.
```

Every `0<u0<1` can be realized by:

```text
F_plus = u0
F_perp = 1-u0.
```

A concrete positive analytic family already realizes a continuum:

```text
F_lambda(Z) = exp(lambda Z)
F_plus = exp(lambda)
F_perp = exp(-lambda).
```

The runner verifies:

```text
K_TL = 0 <=> lambda = 0.
```

For example `lambda = log(2)` is a valid positive analytic source and is
off-Koide.

## Equality escape hatch

Using the same analytic formula does not force equal values on inequivalent
inputs:

```text
F(x_plus) = F(x_perp)
```

requires a new equality of inputs or a special constant/degenerate source
function.  The retained carrier still has:

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

Requiring `F(z)=F(-z)` would remove the odd part, but that is precisely the
unretained `Z -> -Z` block-exchange law in functional language.

## Residual

```text
RESIDUAL_SCALAR = F_plus_minus_F_perp_equiv_center_label_source_u_minus_one_half
RESIDUAL_EQUALITY = all_order_equivariance_does_not_equalize_center_blocks
RESIDUAL_ODD_PART = analytic_center_function_odd_part_not_forced_zero
```

## Why this is not closure

The all-order source grammar broadens the no-go from finite polynomial checks
to analytic center functionals, but it still reduces the Q primitive to a
block-value equality law.  That equality is not derived by equivariance or
analyticity.

## Falsifiers

- A retained theorem forcing equal analytic inputs or equal functional values
  for the two center blocks.
- A physical source grammar excluding all positive unequal block values.
- A higher-order `Cl(3)` invariant whose normalized center restriction has no
  free ratio and yields `u=1/2`.

## Boundaries

- Covers analytic C3-equivariant center functionals whose normalized source is
  determined by positive block values.
- Does not refute non-analytic or genuinely new physical source laws.

## Hostile reviewer objections answered

- **"Higher-order terms may fix it."**  All-order terms still evaluate to two
  positive block values.
- **"Use the same function on both blocks."**  Same function does not imply
  same value on inequivalent inputs.
- **"Set the values equal."**  That is the residual source primitive.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_all_order_center_functional_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_ALL_ORDER_CENTER_FUNCTIONAL_NO_GO=TRUE
Q_ALL_ORDER_CENTER_FUNCTIONAL_CLOSES_Q=FALSE
RESIDUAL_SCALAR=F_plus_minus_F_perp_equiv_center_label_source_u_minus_one_half
RESIDUAL_EQUALITY=all_order_equivariance_does_not_equalize_center_blocks
RESIDUAL_ODD_PART=analytic_center_function_odd_part_not_forced_zero
```
