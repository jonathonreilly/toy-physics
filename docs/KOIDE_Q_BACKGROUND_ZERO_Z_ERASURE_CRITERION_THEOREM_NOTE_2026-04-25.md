# Koide Q Background-Zero / Z-Erasure Criterion Theorem

**Date:** 2026-04-25
**Status:** exact support / criterion theorem on the second-order `Q` route;
not retained native Koide closure
**Primary runner:**
`scripts/frontier_koide_q_background_zero_z_erasure_criterion.py`

---

## 1. Purpose

The April 22 second-order `Q` support package reduced the surviving
charged-lepton `Q = 2/3` problem to one sharp primitive:

```text
Why should the physical charged-lepton readout be source-free on the
normalized reduced second-order carrier?
```

This note lands the useful algebra from the follow-up branch without promoting
that primitive to a theorem.  It proves that, **once the normalized reduced
carrier and exact reduced source law are admitted**, the following conditions
are equivalent:

```text
background-zero source
<=> Z-erasure
<=> Y = I_2
<=> Q = 2/3.
```

So the remaining `Q` bridge is no longer a vague "value law" gap.  It is the
specific physical theorem that must select the source-free / `Z`-erased
representative as the charged-lepton lane.

---

## 2. Admitted carrier and exact source law

Use the normalized reduced two-block carrier from the April 22 support stack:

```text
Y = diag(y_+, y_perp),       y_+ > 0, y_perp > 0,
Tr(Y) = 2.
```

The exact reduced source generator is

```text
W_red(K) = log det(I + K)
         = log(1+k_+) + log(1+k_perp),
```

with

```text
K = diag(k_+, k_perp).
```

The exact source-response equation is therefore

```text
Y = dW_red/dK = diag(1/(1+k_+), 1/(1+k_perp)).
```

Equivalently,

```text
K = Y^(-1) - I.
```

This is the same admitted carrier and source law as
`KOIDE_Q_REDUCED_OBSERVABLE_RESTRICTION_THEOREM_2026-04-22.md` and
`KOIDE_Q_NO_HIDDEN_SOURCE_AUDIT_2026-04-22.md`.

---

## 3. The `Z` coordinate

Parameterize the trace-2 reduced carrier by the traceless coordinate

```text
Y_Z(z) = diag(1+z, 1-z),      -1 < z < 1.
```

Let

```text
Z = diag(1, -1).
```

Then the normalized `Z` expectation is

```text
<Z> = Tr(Y_Z Z) / Tr(Y_Z) = z.
```

So `Z`-erasure is the exact condition

```text
<Z> = 0  <=>  z = 0.
```

The dual source attached to this point is

```text
K_Z(z) = Y_Z(z)^(-1) - I
       = diag(1/(1+z)-1, 1/(1-z)-1)
       = diag(-z/(1+z), z/(1-z)).
```

Therefore

```text
K_Z = 0  <=>  z = 0  <=>  <Z> = 0.
```

Any nonzero `Z` coordinate is not an independent explanation of the selector
value. It is exactly a nonzero reduced source written in trace-zero
coordinates.

---

## 4. Exact `Q` consequence

On this normalized reduced carrier, the Koide-side dimensionless readout is

```text
Q(z) = (1 + y_perp/y_+) / 3
     = (1 + (1-z)/(1+z)) / 3
     = 2 / (3(1+z)).
```

Thus

```text
Q(0) = 2/3.
```

Conversely,

```text
Q = 2/3  <=>  z = 0.
```

The inverse map is exact:

```text
z(Q) = 2/(3Q) - 1.
```

So a nonzero `Z` value is one-to-one with a chosen non-Koide value of `Q`.
Keeping nonzero `Z` would simply re-encode the selector value in source
coordinates.

---

## 5. Criterion theorem

On the admitted normalized reduced carrier with exact source law
`W_red = log det(I+K)`, the following statements are equivalent:

```text
K = 0
<=> Y = I_2
<=> z = 0
<=> <Z> = 0
<=> Q = 2/3.
```

This is the strongest exact statement the current `Q` support lane can defend.
It converts the remaining `Q` problem into one sharply named physical theorem:

```text
derive physical source-free reduced-carrier selection.
```

---

## 6. What this note closes

This note closes the following **inside the admitted second-order route**:

1. the algebraic equivalence between background-zero source and `Z`-erasure;
2. the exact implication from `Z`-erasure to `Q = 2/3`;
3. the hidden-source objection that a nonzero `Z` could be harmless;
4. the precise residual theorem needed to promote `Q` from support to retained
   native closure.

---

## 7. What this note does not close

This note does **not** prove:

1. that the physical charged-lepton observable must live on the normalized
   reduced two-block carrier;
2. that retained charged-lepton physics forces the source-free condition
   `K = 0` on that carrier;
3. the selected-line boundary-source / based-endpoint bridge behind
   `delta = 2/9`;
4. the Type-B rational-to-radian observable law behind the Brannen phase;
5. full retained dimensionless Koide closure.

Those remain open package boundaries.

---

## 8. Closeout flags

```text
KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION=TRUE
KOIDE_Q_SOURCE_FREE_CRITERION_SUPPORT=TRUE
KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE
KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=FALSE
KOIDE_FULL_DIMENSIONLESS_CLOSURE=FALSE
RESIDUAL_Q=derive_physical_source_free_reduced_carrier_selection
RESIDUAL_DELTA=derive_selected_line_local_boundary_source_and_based_endpoint_plus_Type_B_radian_readout
```

Bottom line: the useful branch science lands as an exact criterion theorem, not
as a discharge of the remaining physical `Q` bridge.
