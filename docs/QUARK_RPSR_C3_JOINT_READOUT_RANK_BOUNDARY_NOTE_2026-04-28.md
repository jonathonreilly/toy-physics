# Quark RPSR-C3 Joint Readout Rank Boundary Note

**Date:** 2026-04-28

**Status:** exact no-go / boundary theorem for Lane 3 targets 3B and 3C.
This block-12 artifact tests whether combining the exact RPSR up-amplitude
scalar with the exact `C3[111]` Ward splitter closes the up-type two-ratio
readout. It does not claim retained `m_u`, `m_c`, `m_u/m_c`, or `m_c/m_t`.

**Primary runner:**
`scripts/frontier_quark_rpsr_c3_joint_readout_rank_boundary.py`

## 1. Question

Blocks 10 and 11 sharpened the 3B route:

```text
RPSR gives one exact reduced up-amplitude scalar a_u.
One scalar does not by itself determine both y_u/y_c and y_c/y_t.
```

Blocks 06 and 07 sharpened the 3C route:

```text
C3[111] gives an exact Hermitian Fourier-basis splitter/carrier.
The C3 coefficients and physical readout remain source data.
```

This block asks the joint question:

```text
Does exact RPSR + exact C3 close the two-ratio up-type Yukawa readout without
adding a new source law for the C3 coefficients?
```

## 2. Minimal Premise Set

Allowed premises:

1. the exact RPSR reduced amplitude
   `a_u = sqrt(5/6) * (1 - 48/(49 sqrt(42)))`;
2. the exact `C3[111]` Hermitian Ward normal form
   `W(A,B,C) = A I + B(C3+C3^2) + C(C3-C3^2)/(i sqrt(3))`;
3. top-scale normalization of a positive ordered up-type triple;
4. scale covariance and finite-dimensional spectral algebra.

Forbidden proof inputs:

1. observed quark masses;
2. fitted Yukawa entries;
3. CKM singular values treated as mass inputs;
4. a hidden C3 source law for `A,B,C`;
5. a hidden generation-gap assignment from cyclic Fourier channels to
   physical `u,c,t`;
6. treating one scalar constraint as if it fixed a two-coordinate readout.

## 3. C3 Carrier Rank

In the Fourier basis, the `C3` normal form has eigenvalues:

```text
lambda_0 = A + 2 B,
lambda_+ = A - B + C,
lambda_- = A - B - C.
```

Conversely, any real triple `(lambda_0, lambda_+, lambda_-)` is represented
by:

```text
A = (lambda_0 + lambda_+ + lambda_-)/3,
B = (2 lambda_0 - lambda_+ - lambda_-)/6,
C = (lambda_+ - lambda_-)/2.
```

After top-scale normalization, an ordered positive up-type ratio triple can
be written as:

```text
(y_u/y_t, y_c/y_t, 1) = (r_uc r_ct, r_ct, 1),
```

with two independent positive ratios `r_uc = y_u/y_c` and
`r_ct = y_c/y_t`. The C3 carrier can represent any such real triple. That is
useful support, but it is a carrier rank statement rather than a prediction.

## 4. RPSR Scalar Rank

The RPSR theorem supplies one scalar `a_u`. A single scalar can constrain at
most one coordinate or one relation on the two-ratio surface unless an
additional readout theorem supplies the missing function.

Two generous one-scalar identifications illustrate the residual:

```text
product constraint:      y_u/y_t = a_u
middle-gap constraint:   y_c/y_t = a_u
```

The product constraint gives a continuum:

```text
y_c/y_t = t,
y_u/y_c = a_u/t,
```

for any admissible `t` with `a_u <= t <= 1`.

The middle-gap constraint gives another continuum:

```text
y_c/y_t = a_u,
y_u/y_c = s,
```

for any admissible `0 < s <= 1`.

Every member of both families has exact C3 coefficients by the inverse map
above. Therefore exact C3 carrier support does not remove the missing RPSR
readout/source law.

## 5. Theorem

**Theorem (RPSR-C3 joint readout rank boundary).** In the current Lane 3
support bank, exact RPSR plus the exact `C3[111]` Hermitian Ward carrier does
not determine the two independent up-type Yukawa ratios. The C3 normal form
represents the two-ratio surface, while RPSR contributes one scalar. Without
a retained source law for the C3 coefficients and a physical assignment of
cyclic Fourier channels to `u,c,t`, the joint route remains underdetermined.

## 6. What This Retires

This retires the joint shortcut:

```text
RPSR scalar a_u + C3 Fourier carrier
=> retained up-type ratio pair.
```

The result does not retire either support surface. It says their combination
still needs a source/readout theorem.

## 7. What Remains Open

Lane 3 remains open. A future route can still move the claim state by deriving:

1. a C3 coefficient law for `A,B,C` from retained quark source data;
2. a physical channel assignment from C3 Fourier strata to the `u,c,t`
   singular-value gaps;
3. a two-ratio RPSR readout law or equivalent exponent law;
4. a top-compatible sector/scale bridge;
5. compatibility with the existing CKM and one-Higgs gauge-selection
   boundaries.

## 8. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_rpsr_c3_joint_readout_rank_boundary.py
```

Expected result:

```text
TOTAL: PASS=87, FAIL=0
VERDICT: exact RPSR plus exact C3 is carrier support, not retained up-type
two-ratio readout closure without a new source/readout theorem.
```
