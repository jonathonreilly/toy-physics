# Koide Q Reduced Observable Restriction Theorem

**Date:** 2026-04-22
**Status:** exact support theorem on the second-order reduced-carrier route
for charged-lepton Koide `Q`; not a closure theorem
**Purpose:** remove the reviewer objection that

```text
W_red(K) = log det(I + K)
```

on the two-slot second-order carrier is only a plausible additive transplant.

**Primary runner:** `scripts/frontier_koide_q_reduced_observable_restriction_theorem.py`

---

## 1. Exact reduced carrier

Once the first-live second-order charged-lepton sector has been reduced to the
positive two-slot carrier, the split-preserving projectors are exactly

```text
Π_+ + Π_perp = I_2,
Π_+ Π_perp = 0.
```

So the most general split-preserving source is

```text
K = k_+ Π_+ + k_perp Π_perp
  = diag(k_+, k_perp).
```

This is not an ansatz. It is the exact source family on the reduced block
algebra.

---

## 2. Exact restriction of the observable principle

Apply the original observable principle directly on this reduced carrier:

```text
W[J] = log|det(D+J)| - log|det D|.
```

With reduced baseline `D_red = I_2` and reduced source `K`, this gives

```text
W_red(K)
  = log det(I_2 + K)
  = log(1 + k_+) + log(1 + k_perp).
```

So the reduced source law is not "the right additive form by analogy."
It is the exact restriction of the original theorem to the exact reduced
carrier.

Pure-block restriction fixes the coefficients uniquely:

```text
W_red(k_+,0) = log(1+k_+),
W_red(0,k_perp) = log(1+k_perp),
```

leaving no residual coefficient freedom.

---

## 3. Exact dual reduction

The Legendre dual of the reduced source law is therefore exact as well. For
positive `Y = diag(y_1,y_2)`,

```text
K_* = Y^(-1) - I,
S_eff(Y) = Tr(Y) - log det(Y) - 2.
```

So the normalized effective-action theorem is not a separate imported layer. It
is the exact dual of the exact reduced observable generator.

---

## 4. Why this is not the unreduced determinant

On the unreduced `1 ⊕ 2` vector-slot carrier one would have

```text
log det = log(1+k_+) + 2 log(1+k_perp),
```

because the nontrivial doublet is counted twice as ordered vector slots.

The present theorem is different because it works on the **reduced block
algebra of invariant generators**, where there are exactly two independent
positive scalar blocks. That is why the exact restricted law is

```text
log(1+k_+) + log(1+k_perp),
```

not the unreduced `(1,2)` law.

---

## 5. Honest scope

### What this note claims

1. once the normalized second-order two-block carrier is admitted, the reduced
   source law on that carrier is exactly `W_red = log det(I+K)`;
2. its Legendre-dual effective action is then exact on that same carrier;
3. the note removes coefficient ambiguity inside that reduced-carrier route.

### What this note does not claim

1. it does not prove that the physical charged-lepton observable principle must
   live on this reduced two-generator block algebra rather than on the
   unreduced vector-slot carrier or another readout;
2. it does not by itself close the physical/source-law bridge behind
   `Q = 2/3`;
3. it does not touch the separate `δ = 2/9` bridge.

## 6. Bottom line

The strongest exact statement is:

> the reduced two-slot source law `W_red = log det(I+K)` is the exact
> restriction of the original observable principle to the normalized
> second-order block algebra, and its dual effective action is therefore exact
> on that carrier as well.

That is a genuine support theorem for the second-order `Q` route. The
remaining open step is still the physical identification of this reduced
carrier and source law.
