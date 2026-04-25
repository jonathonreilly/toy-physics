# Koide Q Quartic-Coefficient Independence No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the Koide-Nishiura /
quartic-potential route but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_quartic_coefficient_independence_no_go.py`

---

## 1. Question

The Koide-Nishiura quartic

```text
V_KN(Phi) = [2 (tr Phi)^2 - 3 tr(Phi^2)]^2
```

is a valid conditional support route. On `Herm_circ(3)` it is proportional to

```text
(E_+ - E_perp)^2,
```

so its minimum is exactly the Koide/A1 leaf:

```text
E_+ = E_perp
<=> K_TL = 0
<=> Q = 2/3.
```

The Nature-grade question is whether retained trace-invariant quartic
structure fixes the coefficient in `V_KN`.

Answer:

```text
No.
```

---

## 2. One-Parameter Quartic Family

The same trace-invariant square construction gives a family

```text
V_c = [c (tr Phi)^2 - tr(Phi^2)]^2.
```

For every `c`, this is:

- trace-invariant;
- quartic;
- nonnegative by square form.

On the two-block carrier its root is

```text
(3c - 1) E_+ - E_perp.
```

Therefore the minimum selects the leaf

```text
E_perp / E_+ = 3c - 1.
```

The Koide leaf `E_perp/E_+ = 1` fixes

```text
c = 2/3.
```

Equivalently, after multiplying the root by `3`, this is exactly

```text
2 (tr Phi)^2 - 3 tr(Phi^2).
```

---

## 3. Consequence

The quartic route closes `Q` only if the coefficient `c = 2/3` is derived or
retained independently.

Without that coefficient theorem, the invariant square family can select
non-Koide leaves just as naturally:

```text
c = 1/2 -> E_perp/E_+ = 1/2
c = 2/3 -> E_perp/E_+ = 1
c = 1   -> E_perp/E_+ = 2
```

So merely allowing a U(3)- or trace-invariant quartic does not select Koide.
The Koide-Nishiura coefficient is the missing value law in polynomial form.

---

## 4. Relation to `K_TL`

On the normalized second-order carrier,

```text
E_+ = E_perp
<=> K_TL = 0.
```

Thus importing `V_KN` without deriving its coefficient is equivalent to
importing the same open primitive:

```text
K_TL = 0.
```

The route remains useful support, but not a retained closure theorem.

---

## 5. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_quartic_coefficient_independence_no_go.py
```

Result:

```text
PASSED: 10/10
KOIDE_Q_QUARTIC_COEFFICIENT_INDEPENDENCE_NO_GO=TRUE
Q_QUARTIC_ROUTE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=c-2/3
```

---

## 6. Boundary

This note does not reject the Koide-Nishiura quartic as a possible future
retained EW-scalar-lane primitive. It rejects only the stronger claim that the
currently retained trace-invariant quartic grammar already derives the Koide
coefficient.

The remaining `Q` target is unchanged:

```text
derive K_TL = 0
```

or equivalently derive the coefficient `c = 2/3` from retained structure
without assuming the Koide leaf.
