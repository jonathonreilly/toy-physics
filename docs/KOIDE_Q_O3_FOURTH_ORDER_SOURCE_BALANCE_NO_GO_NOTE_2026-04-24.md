# Koide Q O3 Fourth-Order Source-Balance No-Go

**Date:** 2026-04-24
**Status:** Branch-local negative audit. This sharpens the higher-order `O_3`
escape hatch but does not close charged-lepton `Q = 2/3`.
**Primary runner:** `scripts/frontier_koide_q_o3_fourth_order_source_balance_no_go.py`

---

## 1. Theorem Attempt

The first-live `Gamma_1` return cannot see `O_3`. The next assumption inversion
is:

> higher-order `O_3` paths might supply the missing source balance and force
> `K_TL = 0`.

The executable result is negative.

Individual fourth-order mixed-`Gamma` orderings through the full non-`T_1`
carrier can produce signed species-resolved diagonals. But the retained
Clifford ordering sum cancels exactly, and the full `M(phi)^4` return vanishes
identically on the `T_1` species block for arbitrary `phi`.

---

## 2. Exact Signed Cancellation

The runner works in the exact retained spatial `Cl(3)` matrix model:

```text
{Gamma_i, Gamma_j} = 2 delta_ij I.
```

For each mixed multiset:

```text
{Gamma_1^2, Gamma_2^2},
{Gamma_1^2, Gamma_3^2},
{Gamma_2^2, Gamma_3^2},
```

some individual orderings have nonzero signed species diagonals. For example:

```text
(Gamma_1, Gamma_2, Gamma_1, Gamma_2) -> signed single-species support,
(Gamma_1, Gamma_2, Gamma_2, Gamma_1) -> opposite signed support.
```

But summing retained signed orderings inside each multiset gives:

```text
sum_orderings P_T1 Gamma_i Pi Gamma_j Pi Gamma_k Pi Gamma_l P_T1 = 0.
```

This is the existing fourth-order signed-ordering obstruction, now restated as
a Koide `K_TL` source-law audit.

---

## 3. EWSB Weighting Cannot Rescue It

For the retained Higgs family:

```text
M(phi) = phi_1 Gamma_1 + phi_2 Gamma_2 + phi_3 Gamma_3,
```

the full fourth-order return is:

```text
sum_seq phi_i phi_j phi_k phi_l
  P_T1 Gamma_i Pi Gamma_j Pi Gamma_k Pi Gamma_l P_T1.
```

The runner verifies exactly:

```text
P_T1 M(phi) Pi M(phi) Pi M(phi) Pi M(phi) P_T1 = 0
```

on the species block for symbolic `phi`.

The reason is structural: the monomial `phi_i phi_j phi_k phi_l` depends only
on the multiset, so it factors out of each signed multiset sum, and each such
sum is already zero.

---

## 4. What A Positive O3 Route Would Need

To turn the individual signed channels into a positive source law, one would
have to add a new rule such as:

```text
erase Clifford signs,
select a preferred ordering,
or assign non-retained positive order weights.
```

That is not currently retained.

Even if such a sign-erasure primitive were granted, the resulting positive
three-slot family would be:

```text
Q(a,b,c) = (a^2+b^2+c^2)/(a+b+c)^2.
```

Koide would still require:

```text
a^2+b^2+c^2 = 4(ab+ac+bc),
```

which is the same three-slot selector/source law in another coordinate.

Exact samples:

```text
(1,1,1)           -> Q = 1/3
(1,2,3)           -> Q = 7/18
(1,4+3 sqrt(2),1) -> Q = 2/3
(4,1,1)           -> Q = 1/2
```

---

## 5. Review Consequence

The higher-order `O_3` route proves:

```text
O_3 participation can expose signed species channels before retained summation.
```

It does not prove:

```text
retained Cl(3)/Z^3 charged-lepton structure -> K_TL = 0.
```

The residual is:

```text
sign_erasure_or_ordering_selector
plus
three_slot_selector_cone
equiv K_TL = 0.
```

So this route cannot be promoted as a Koide closeout without a new retained
ordering/sign source law.

---

## 6. Executable Result

Run:

```bash
python3 scripts/frontier_koide_q_o3_fourth_order_source_balance_no_go.py
```

Result:

```text
PASSED: 11/11
KOIDE_Q_O3_FOURTH_ORDER_SOURCE_BALANCE_NO_GO=TRUE
Q_O3_FOURTH_ORDER_SOURCE_BALANCE_CLOSES_Q=FALSE
RESIDUAL_PRIMITIVE=sign_erasure_or_ordering_selector_plus_three_slot_K_TL_law
```

No PDG masses, `K_TL = 0`, `K = 0`, `P_Q = 1/2`, `Q = 2/3`,
`delta = 2/9`, or `H_*` observational pin is used as an input.

---

## 7. Boundary

This note does not demote:

- the existing higher-order signed-ordering theorem;
- `O_3` as a useful audit channel;
- future retained sign/order mechanisms, if one is independently derived.

It rejects only the stronger claim that `O_3` fourth-order source balancing
itself derives the Koide source law.
