# Koide Higgs-Dressed Chamber-Link Renormalization Theorem

**Date:** 2026-04-20  
**Lane:** charged-lepton Koide, constructive transport avenue  
**Status:** exact transport-structure sharpening on top of the missing-axis
resolvent root theorem. This still does not finish a retained Koide
derivation, but it reduces the surviving Higgs-dressed route from "derive some
lambda-law" to "derive the local `O_0` renormalization law of a visible
chamber-link entry of `H_*`."  
**Runner:** `scripts/frontier_koide_higgs_dressed_chamber_link_renormalization_theorem.py`

## Question

The previous theorem already reduced the strongest surviving Higgs-dressed
transport avenue to one exact positive Koide root on the missing-axis lift:

```text
W_4(h_0) = diag(h_0, H_*),
R_lambda(h_0) = (lambda I - W_4(h_0))^(-1).
```

But that still left one ambiguity:

```text
is lambda_* a genuinely new free scalar, or is it a renormalized form of
some scalar already visible in the retained H_* chamber data?
```

This note answers that question.

## Bottom line

The visible chamber scalar is already present.

On the retained missing-axis Hermitian `H_* = H(m_*, delta_*, q_+*)`, the old
comparison scalar

```text
lambda_slack = q_+* + delta_* - sqrt(8/3)
```

is exactly the real part of the chamber-link entry

```text
lambda_slack = Re(H_*[1,3]),
Im(H_*[1,3]) = -1/2.
```

Moreover, the induced species block of the missing-axis resolvent is not a
generic `3 x 3` compression. It is exactly

```text
Sigma_{lambda,h_0}
  = [scalar O_0 resolvent channel] direct-sum [reached 2 x 2 principal
      T_2 resolvent block].
```

So on the positive branch the Koide condition `Q = 2/3` reduces to one exact
balance law between:

```text
x = 1/(lambda - h_0),
t = Tr(B_lambda),
d = det(B_lambda),
```

where `B_lambda` is the reached `2 x 2` principal block of
`(lambda I - H_*)^(-1)`.

At the visible chamber scalar itself, `lambda = lambda_slack`, exact Koide is
restored by a tiny positive `O_0` renormalization

```text
h_0,small = 4.4898983... x 10^(-5).
```

So the surviving transport lane is now sharper than the previous note: the
remaining microscopic object is not a new free scalar `lambda`, but the local
`O_0` renormalization law of the already-visible chamber-link scalar
`Re(H_*[1,3])`.

## 1. Exact transport decomposition

Let

```text
W_4(h_0) = diag(h_0, H_*)
```

on the missing-axis basis

```text
(O_0, T_2[011], T_2[101], T_2[110]).
```

Because `Gamma_1` hops the three `T_1` species only to

```text
O_0, T_2[110], T_2[101],
```

the induced species block is exactly

```text
Sigma_{lambda,h_0}
  = P_{T_1} Gamma_1 (lambda I - W_4(h_0))^(-1) Gamma_1 P_{T_1}
  =
    [ x, 0, 0 ]
    [ 0, B_{11}, B_{12} ]
    [ 0, B_{21}, B_{22} ],
```

with

```text
x = 1/(lambda - h_0),
B_lambda = ((lambda I - H_*)^(-1))_{reached principal block}.
```

So this route is a scalar channel plus a principal `2 x 2` transport sector,
not a general `3 x 3` spectral compression.

## 2. Exact positive-branch balance law

Let the positive eigenvalues of `Sigma_{lambda,h_0}` be

```text
a = x,
b, c = eig(B_lambda),
```

and write

```text
t = b + c = Tr(B_lambda),
d = bc = det(B_lambda).
```

Then Koide `Q = 2/3` is equivalent to

```text
a + b + c = 4 (sqrt(ab) + sqrt(ac) + sqrt(bc)).
```

Using

```text
b + c = t,
sqrt(b) + sqrt(c) = sqrt(t + 2 sqrt(d)),
sqrt(bc) = sqrt(d),
```

this becomes the exact single-root transport balance law

```text
(a + t - 4 sqrt(d))^2 = 16 a (t + 2 sqrt(d)).
```

Equivalently, on the positive branch:

```text
P(a,t,d) = 0,
```

with quartic polynomial

```text
P(a,t,d)
  = a^4
    - 28 t a^3
    + (198 t^2 - 1568 d) a^2
    - (28 t^3 + 1088 d t) a
    + t^4 - 32 d t^2 + 256 d^2.
```

So the Koide condition on this avenue is an exact principal-block balance law.

## 3. Jacobi complement identity

The reached transport block also satisfies a clean complement formula.

Since `B_lambda` is the principal `2 x 2` block of `(lambda I - H_*)^(-1)`,
Jacobi's complementary-minor identity gives

```text
det(B_lambda) = (lambda - M_*) / det(lambda I - H_*),
```

because the complementary `1 x 1` block is exactly the `O_0`-linked scalar
entry `lambda - H_*[1,1] = lambda - M_*`.

So one part of the transport balance law is already fixed directly by the
complementary scalar channel.

## 4. Visible chamber-link scalar and local renormalization branch

The old chamber comparison scalar is not ad hoc:

```text
H_*[1,3] = q_+* + delta_* - sqrt(8/3) - i/2
         = lambda_slack - i/2.
```

So `lambda_slack` is exactly the real part of a visible missing-axis chamber
link inside `H_*`.

At `h_0 = 0`, exact Koide occurs at the unique small positive root

```text
lambda_* = 0.015808703285395...
```

while the visible chamber scalar is

```text
lambda_slack = 0.015855511490548....
```

These are close but not equal. However, fixing

```text
lambda = lambda_slack
```

and solving only in `h_0` restores exact Koide at

```text
h_0,small = 4.4898983... x 10^(-5).
```

Numerically the Koide locus through `(lambda_*, 0)` is nondegenerate in the
`h_0` direction and has local slope

```text
dh_0 / d lambda = 0.959212...
```

at the physical positive root. So near the physical point, `h_0` acts as a
local renormalization of the visible chamber-link scalar, not as an unrelated
parameter.

## 5. What changed

The previous theorem said:

```text
derive one scalar lambda-law on the missing-axis resolvent lane.
```

This theorem is sharper:

```text
derive the local O_0 renormalization law of the visible chamber-link scalar
lambda_slack = Re(H_*[1,3]).
```

That is a materially smaller and more concrete microscopic target.

## 6. Honest scope boundary

This note does **not** claim:

- a retained derivation of `Q = 2/3`;
- a retained derivation of `lambda_*`;
- a retained derivation of the local `h_0(lambda)` branch;
- that the G1-pinned chamber data inside `H_*` are already themselves
  retained-derived.

It does claim the following exact sharpening:

- the transport lane is a scalar-plus-principal-block problem;
- Koide is an exact balance law on that reduced transport data;
- the visible chamber scalar is already in `H_*`;
- the residual microscopic object is now specifically an `O_0`
  renormalization law of that chamber link.

So the constructive frontier is cleaner again.
