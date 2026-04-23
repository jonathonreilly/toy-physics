# Koide Q No-Hidden-Source Audit

**Date:** 2026-04-22
**Status:** exact support audit on the second-order `Q` route; not a closure
theorem
**Purpose:** sharpen two review risks at once:

1. show that no earlier/admissible carrier closes `Q` cleanly, and
2. show that any nonzero reduced source on the normalized second-order carrier
   would merely re-encode an arbitrary selector choice.

**Primary runner:** `scripts/frontier_koide_q_no_hidden_source_audit.py`

---

## 1. Earlier carrier audit

The branch-local route remains consistent with the earlier no-gos:

- the raw chiral bridge `Y = P_R Γ_1 P_L` has zero bosonic
  `log|det|` response on a scalar baseline;
- the unreduced determinant carrier still lands on the `(1,2)` leaf and gives
  `kappa = 1`, not `2`.

So the present route is not hiding a contradiction. It really does live on a
later carrier.

---

## 2. Hidden-source audit on the normalized carrier

On the normalized positive carrier,

```text
Y = diag(y, 2-y),   0 < y < 2,
```

the exact dual equation is

```text
K = Y^(-1) - I.
```

So every normalized point determines a unique reduced source

```text
K(y) = diag(1/y - 1, 1/(2-y) - 1).
```

The crucial consequence is:

```text
K = 0   <=>   y = 1   <=>   Y = I_2.
```

So there is exactly one datum-free point.

If one also imposes the normalized trace condition `Tr(Y)=2`, then the
admissible nonzero sources form a **one-parameter family**. That family is
exactly the same one free parameter as the selector variable itself.

In other words:

> a hidden nonzero source does not explain the selector value; it merely
> re-parameterizes an arbitrary chosen point on the selector family.

That is why `K = 0` is load-bearing. It is not a convenience choice. It is the
only source choice that does not smuggle in the value being derived.

---

## 3. Review consequence

The clean reviewer statement is:

```text
source-free on the normalized second-order carrier
```

means exactly:

- no added target matrix,
- no nonzero selector source,
- no hidden one-parameter datum equal in content to the unknown `Q` value.

Then the exact dual equation gives

```text
Y = I_2,
```

which is exactly

```text
E_+ = E_perp
-> kappa = 2
-> Q = 2/3.
```

---

## 4. Bottom line

The second-order route survives the hidden-source audit:

> any nonzero reduced source is just the selector value written in source
> coordinates, while the source-free point `K = 0` is the unique datum-free
> closure point of the normalized carrier.

That sharply narrows the remaining primitive. What it does **not** yet prove is
that retained charged-lepton physics forces the physical lane to be source-free
on that carrier.
