# Koide Q Readout Factorization Theorem

**Date:** 2026-04-22
**Status:** exact support theorem on the admitted first-live second-order
readout grammar; not a closure theorem
**Purpose:** replace the weakest remaining phrase in the second-order `Q` route

> the selector should live on the second-order returned operator

with the strongest exact quotient statement currently available on the retained
`Γ_1 / T_1` grammar.

**Primary runner:** `scripts/frontier_koide_q_readout_factorization_theorem.py`

---

## 1. Exact map

On the retained charged-lepton readout grammar, define the second-order map

```text
L(W) = P_{T_1} Γ_1 W Γ_1 P_{T_1}
```

on the four reachable/intermediate-state weight slots

```text
W = u P_{O_0} + v P_{(1,1,0)} + w P_{(1,0,1)} + z P_{(0,1,1)}.
```

The exact single-slot images are

```text
P_{T_1} Γ_1 P_{O_0} Γ_1 P_{T_1}     = diag(1,0,0)
P_{T_1} Γ_1 P_{(1,1,0)} Γ_1 P_{T_1} = diag(0,1,0)
P_{T_1} Γ_1 P_{(1,0,1)} Γ_1 P_{T_1} = diag(0,0,1)
P_{T_1} Γ_1 P_{(0,1,1)} Γ_1 P_{T_1} = 0.
```

So the readout map is exactly

```text
L(u,v,w,z) = diag(u,v,w).
```

---

## 2. Quotient theorem

The map `L : R^4 -> Diag_3(R)` has:

- rank `3`,
- kernel `span{(0,0,0,1)}`,
- image equal to the full diagonal species space.

Therefore

```text
R^4 / span(e_unreach)  ≅  Diag_3(R),
```

and two weight packages have the same first-live returned operator if and only
if they differ only in the unreachable slot `z`.

So the exact first-live second-order returned operator is not just one natural
representation of the species data. It is the **classification quotient** of
the entire first-live local bosonic readout grammar.

---

## 3. Selector consequence

Within the retained scope:

- local,
- bosonic/even in `Γ_1`,
- first-live on `T_1`,
- species-resolving,
- `C_3`-covariant,

every admissible selector depends on the weight package only through the
returned operator

```text
R_{Γ_1}(W) = diag(u,v,w).
```

The exact species Fourier transport then sends that returned operator to the
Koide carrier `H_cyc`, and the cyclic quadratic scalar sector reduces to the
same two-slot carrier `(E_+, E_perp)`.

So this note upgrades the old identification language inside the admitted
first-live second-order class:

```text
admitted first-live selector = scalar on the exact second-order returned
operator
```

from a plausible carrier choice to the exact quotient statement available on
the first-live readout grammar.

---

## 4. Honest scope

### What this note claims

1. on the first-live second-order readout grammar, the returned operator is the
   exact quotient/classification object;
2. the unreachable slot is the entire kernel;
3. every admissible first-live bosonic species-resolving selector factors
   uniquely through that returned operator.

### What this note does not claim

1. it does not claim a universal statement about all possible higher-order or
   nonlocal carriers;
2. it does not touch the separate `delta` bridge;
3. it does not rewrite authority surfaces;
4. it does not by itself prove that the physical charged-lepton selector must
   belong to this admitted class.

---

## 5. Bottom line

The strongest clean statement for review is:

> on the retained `Γ_1 / T_1` grammar, the exact second-order returned operator
> is the quotient of the entire first-live species-resolving bosonic readout
> sector, so every admissible first-live selector factors uniquely through it.

That removes most of the remaining ambiguity in the carrier-identification
step of the admitted second-order `Q` route. The remaining open issue is still
the physical identification of that route.
