# Koide Higgs-Dressed Affine Transport Germ Theorem

**Date:** 2026-04-20  
**Lane:** charged-lepton Koide, constructive transport avenue  
**Status:** exact local transport-law sharpening on top of the chamber-link
renormalization theorem. This still does not close Koide from retained
framework data alone, but it proves that the physically relevant
`O_0`-correction branch is already an affine germ on the visible chamber
window.  
**Runner:** `scripts/frontier_koide_higgs_dressed_affine_transport_germ_theorem.py`

## Question

After the chamber-link renormalization theorem, the remaining microscopic
object on the strongest surviving transport route was:

```text
derive the O_0 renormalization law for the visible chamber-link scalar
lambda_slack = Re(H_*[1,3]).
```

The natural next question is whether that law is still a complicated implicit
curve, or whether it is already much simpler on the physically relevant
window.

## Bottom line

It is already almost linear.

On the unique small Koide branch through the physical positive root

```text
(lambda_*, h_0) = (0.015808703285395..., 0),
```

the exact branch `h_0(lambda)` over the visible micro-window

```text
|lambda - lambda_*| <= 1.2 x 10^(-4)
```

is affine to about

```text
7 x 10^(-11),
```

with slope

```text
alpha ~= 0.959212206....
```

A quadratic germ resolves the same branch to numerical machine precision and
has only tiny curvature:

```text
h_0(lambda) = alpha (lambda - lambda_*) + beta (lambda - lambda_*)^2 + ...
beta = -0.008496...
```

At the visible chamber-link scalar

```text
lambda_slack = Re(H_*[1,3]),
```

the exact correction

```text
h_0(lambda_slack) = 4.4898983... x 10^(-5)
```

is already predicted by the affine germ to about

```text
3 x 10^(-11),
```

and by the quadratic germ to machine precision.

So the chamber-slack correction is not a new mechanism. It sits on the same
unique local transport germ through the physical Koide root.

## 1. Setup

The previous theorem showed that on the missing-axis lift

```text
W_4(h_0) = diag(h_0, H_*),
```

the Koide condition defines a local branch through

```text
(lambda_*, h_0) = (0.015808703285395..., 0)
```

and that the visible chamber-link scalar

```text
lambda_slack = q_+* + delta_* - sqrt(8/3)
             = Re(H_*[1,3])
```

reaches exact Koide after a tiny positive correction

```text
h_0,small = 4.4898983... x 10^(-5).
```

The question here is about the structure of that branch itself.

## 2. The theorem

> **Theorem.** On the physical micro-window
>
> ```text
> |lambda - lambda_*| <= 1.2 x 10^(-4),
> ```
>
> the local Koide branch of the missing-axis transport family satisfies:
>
> 1. there is a unique small real branch root `h_0(lambda)` at every sampled
>    `lambda` in that window;
> 2. the branch is monotone increasing;
> 3. an affine fit
>    ```text
>    h_0(lambda) ~= alpha (lambda - lambda_*)
>    ```
>    has maximum error below `1 x 10^(-10)` on the whole tested window;
> 4. a quadratic germ
>    ```text
>    h_0(lambda) ~= alpha (lambda - lambda_*)
>                   + beta (lambda - lambda_*)^2
>    ```
>    resolves the same branch to numerical machine precision;
> 5. at `lambda = lambda_slack`, the affine germ already predicts the exact
>    chamber-link correction to `~ 3 x 10^(-11)`, and the quadratic germ
>    reproduces it to machine precision.

Numerically:

```text
alpha ~= 0.959212206...,
beta  ~= -0.00851....
```

## 3. Meaning

This changes the constructive reading again.

The previous theorem said:

```text
derive the local O_0 renormalization law of the visible chamber link.
```

This theorem sharpens that to:

```text
derive the affine O_0 transport renormalization coefficient alpha
```

on the physically relevant window, with only tiny curvature corrections.

So the live object is no longer a general implicit branch in practice. It is a
one-constant affine germ.

## 4. Honest scope boundary

This note does **not** claim:

- a retained derivation of `alpha`;
- a retained derivation of `lambda_*`;
- that the affine law is globally exact beyond the tested physical window;
- a full retained derivation of Koide `Q = 2/3`.

It does claim something real and useful:

- the physically relevant transport branch is already exceptionally rigid;
- the visible chamber-link correction is controlled by the same local branch
  through the physical root;
- the surviving open object is now naturally read as the microscopic origin of
  one affine renormalization coefficient.

That is a smaller and cleaner target than the previous formulation.
