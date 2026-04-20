# Koide Higgs-Dressed Transport Susceptibility Theorem

**Date:** 2026-04-20  
**Lane:** charged-lepton Koide, constructive transport avenue  
**Status:** exact local-susceptibility sharpening on top of the affine-germ
theorem. This still does not derive Koide from retained framework data alone,
but it replaces the empirical coefficient `alpha` by an exact local
susceptibility identity.  
**Runner:** `scripts/frontier_koide_higgs_dressed_transport_susceptibility_theorem.py`

## Question

The affine-germ theorem showed that on the physically relevant micro-window

```text
h_0(lambda) ~= alpha (lambda - lambda_*),
alpha ~= 0.959212206...
```

with only tiny curvature corrections. But that still left one honest question:

```text
is alpha just a fit coefficient, or does it have an exact local transport
meaning?
```

This note answers that.

## Bottom line

`alpha` is an exact local susceptibility ratio.

Let

```text
F(lambda, h_0) = 0
```

denote the Koide condition on the missing-axis transport family, written
through the exact chamber-link balance law

```text
P(x, t, d) = 0,
x = 1/(lambda - h_0),
t = Tr(B_lambda),
d = det(B_lambda),
```

with `B_lambda` the reached principal `2 x 2` block of `(lambda I - H_*)^(-1)`.

Then at the physical positive root:

```text
alpha = dh_0/dlambda = -F_lambda / F_h0,
```

and this splits exactly as

```text
alpha = 1 - backreaction,
```

where the backreaction term comes entirely from the `lambda`-variation of the
reached principal transport block:

```text
backreaction
  = lambda_*^2 (P_t t' + P_d d') / P_x.
```

Numerically:

```text
alpha        = 0.959212206684...,
backreaction = 0.040787793364...,
t'(lambda_*) = -6.144428397...,
d'(lambda_*) = -3.073052276....
```

So the visible chamber link would track exact Koide with slope `1` if the
reached `2 x 2` block were frozen. The only local deviation is a small
`~ 4.08%` backreaction from the reached transport sector.

## 1. Exact identity

Write the exact positive-branch Koide balance law as

```text
P(x,t,d) = 0,
```

with

```text
x = 1/(lambda - h_0),
t = Tr(B_lambda),
d = det(B_lambda).
```

Since only `x` depends on `h_0`, while `t` and `d` depend only on `lambda`,
implicit differentiation gives

```text
0 = F_lambda + F_h0 (dh_0/dlambda),
```

hence

```text
alpha := dh_0/dlambda = -F_lambda / F_h0.
```

Expanding through `P(x,t,d)` yields

```text
alpha
  = 1 - (lambda - h_0)^2 (P_t t' + P_d d') / P_x.
```

At the physical root `h_0 = 0`, this becomes

```text
alpha = 1 - lambda_*^2 (P_t t' + P_d d') / P_x.
```

That is the exact local susceptibility identity.

## 2. Meaning

This changes the constructive reading one more time.

The previous note said:

```text
derive the affine O_0 transport renormalization coefficient alpha.
```

This note sharpens it to:

```text
derive the small reached-block backreaction term
lambda_*^2 (P_t t' + P_d d') / P_x.
```

Because the bare `O_0` tracking contribution is just `1`. All the nontrivial
local physics sits in the reached `2 x 2` principal block.

So the live microscopic object is no longer a generic affine coefficient. It is
specifically a small transport-sector backreaction.

## 3. Honest scope boundary

This note does **not** claim:

- a retained derivation of the backreaction term;
- a retained derivation of `lambda_*`;
- a full retained derivation of Koide `Q = 2/3`.

It does claim a real reduction:

- `alpha` is no longer just a fit;
- the entire gap between bare chamber-link tracking and exact Koide is a
  single small reached-block backreaction;
- the remaining transport problem is now localized to that backreaction term.

That is a narrower target than "derive the whole branch."
