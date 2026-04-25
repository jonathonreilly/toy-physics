# Koide Q Minimal-Selector Value No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the minimal
scale-free selector route but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_minimal_selector_value_no_go.py`

---

## 1. Theorem Attempt

The minimal-selector theorem proves a real support statement:

> on the accepted first-live second-order carrier, there is exactly one
> nontrivial scale-free `C_3`-invariant selector coordinate.

The tempting closure upgrade is:

> uniqueness of the selector coordinate forces the Koide value.

The executable result is negative.

---

## 2. Unique Coordinate

Use the positive projective coordinate

```text
r = E_perp / E_+.
```

It is scale-free:

```text
(s E_perp)/(s E_+) = E_perp/E_+.
```

It parametrizes the normalized trace-2 carrier:

```text
Y(r) = diag(2/(1+r), 2r/(1+r)).
```

The traceless source and `Q` value are reparametrizations of this same
coordinate:

```text
K_TL(r) = (r^2 - 1)/(4r),
Q(r) = (1+r)/3.
```

So the minimal-selector theorem has done useful work: it removes the
coordinate ambiguity.

---

## 3. Missing Value Law

A coordinate is not a value law. For every `c > 0`, the law

```text
F_c(r) = (r-c)^2
```

is:

- scale-free;
- `C_3`-invariant, because it depends only on the invariant coordinate `r`;
- local to the same first-live second-order carrier;
- uniquely minimized at `r=c`.

The runner checks the exact sample family:

```text
c = 1/2 -> Q = 1/2, K_TL = -3/8
c = 1   -> Q = 2/3, K_TL = 0
c = 2   -> Q = 1,   K_TL = 3/8
```

Only `c=1` is the Koide/source-free value. The current retained structure does
not select `c=1` from the one-variable family.

---

## 4. Relation To Block Exchange

A quotient-level involution

```text
r -> 1/r
```

would have the unique positive fixed point:

```text
r = 1.
```

But the block-exchange obstruction note already shows that the retained
three-generation `C_3` carrier does not supply an actual singlet/doublet
exchange symmetry. Adding this involution as a value law would be another form
of the missing primitive.

---

## 5. Review Consequence

The minimal-selector theorem should be retained as support:

```text
there is only one nontrivial scale-free selector coordinate.
```

It should not be promoted to closure:

```text
the coordinate's physical value is c=1.
```

That value statement is exactly equivalent to:

```text
K_TL = 0.
```

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_minimal_selector_value_no_go.py
```

Result:

```text
PASSED: 10/10
KOIDE_Q_MINIMAL_SELECTOR_VALUE_NO_GO=TRUE
Q_MINIMAL_SELECTOR_UNIQUENESS_CLOSES_Q=FALSE
RESIDUAL_VALUE_PARAMETER=c=r_selected
```

---

## 7. Boundary

This note does not demote the first-live carrier or the minimal-selector
coordinate theorem. It demotes only the stronger claim that coordinate
uniqueness determines the physical value.

Package status is unchanged:

- `Q = 2/3` still needs the normalized traceless-source law `K_TL = 0`;
- `delta = 2/9` still needs the physical selected-line Berry/APS bridge;
- `v0` remains a separate support lane.
