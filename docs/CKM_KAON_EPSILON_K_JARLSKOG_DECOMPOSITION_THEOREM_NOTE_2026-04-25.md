# Kaon ε_K Jarlskog Decomposition Theorem

**Date:** 2026-04-25

**Status:** Retained derivation theorem on `main`. **Pushes the framework
forward** by deriving how the three CKM combinations entering the
Standard Model expression for the kaon CP-violation parameter `epsilon_K`
factor through the framework's retained Jarlskog invariant
`J = alpha_s(v)^3 sqrt(5)/72`. Specifically, at atlas-leading
Wolfenstein order:

```text
(K1)  Im[(V_cs^* V_cd)^2]              =  +2 J,
(K2)  Im[V_cs^* V_cd  V_ts^* V_td]     =  -J,
(K3)  Im[(V_ts^* V_td)^2]              =  -(5 alpha_s(v)^2 / 18) J.
```

These three identities convert the standard `epsilon_K` formula's
CKM-imaginary-part bracket into a single overall factor of `J` times
a kinematic and Wilson-coefficient combination of Inami-Lim functions
and short-distance QCD running factors:

```text
Im(L)  =  J x [ 2 eta_cc S_0(x_c)
              - 2 eta_ct S_0(x_c, x_t)
              - (5 alpha_s(v)^2 / 18) eta_tt S_0(x_t) ],
```

where `Im(L)` is the imaginary part of
`lambda_c^2 eta_cc S_0(x_c) + lambda_t^2 eta_tt S_0(x_t) + 2 lambda_c lambda_t eta_ct S_0(x_c, x_t)`
with `lambda_q = V_qs^* V_qd`. This is **the new pure-framework
structural content** for the kaon CP-violation observable: the
Jarlskog invariant `J` becomes the universal CKM scale for `|epsilon_K|`,
and the relative weights between charm-charm, charm-top, and top-top
contributions are fixed by the framework as exact rational coefficients
in `alpha_s(v)`.

The factor `5 alpha_s(v)^2 / 18` in `(K3)` is the structural origin of
the top-loop CKM suppression in `epsilon_K`. With canonical
`alpha_s(v) = 0.10330...` it evaluates to `0.00296`, so the top
contribution to the CKM bracket is suppressed by this small factor
relative to the charm-charm contribution before the much-larger
Inami-Lim function `S_0(x_t)/S_0(x_c) ~ 1e4` is applied.

**Primary runner:**
`scripts/frontier_ckm_kaon_epsilon_k_jarlskog_decomposition.py`

## Statement

Adopt the standard PDG-Wolfenstein expansion of the CKM matrix to the
order in `lambda` needed for the imaginary parts. Define
`lambda_q = V_qs^* V_qd` for the kaon mixing entries. Then on the
retained framework atlas surface

```text
A^2     = 2/3              [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM]
lambda^2 = alpha_s(v)/2    [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM]
rho     = 1/6              [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM]
eta     = sqrt(5)/6        [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM]
J       = A^2 lambda^6 eta = alpha_s(v)^3 sqrt(5)/72
                           [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM]
```

the leading-order imaginary parts of the three CKM kaon combinations are

```text
(K1)  Im[(V_cs^* V_cd)^2]        =  2 J,
(K2)  Im[V_cs^* V_cd  V_ts^* V_td] =  -J,
(K3)  Im[(V_ts^* V_td)^2]        =  -(5 alpha_s^2 / 18) J
                                  =  -2 A^2 lambda^4 (1 - rho) J.
```

Identities `(K1)` and `(K2)` carry rational coefficients
`(+2, -1)`. Identity `(K3)` carries an `alpha_s^2`-suppressed
coefficient that rewrites in compact form as
`-2 A^2 lambda^4 (1 - rho) = -(5 alpha_s^2 / 18)` in framework
values.

Plugging into the standard `epsilon_K` formula, the framework
prediction is

```text
|epsilon_K|  =  kappa_eps * (G_F^2 f_K^2 M_K M_W^2)/(12 pi^2 sqrt(2) Delta M_K)
              * B_K * |Im(L)|,

Im(L)  =  J x [ 2 eta_cc S_0(x_c)
              - 2 eta_ct S_0(x_c, x_t)
              - (5 alpha_s^2 / 18) eta_tt S_0(x_t) ].
```

The bracket contains only Inami-Lim functions and short-distance QCD
running factors -- no CKM input. The framework supplies the full CKM
content as the single overall `J` factor.

## Retained Inputs

| Input | Authority |
| --- | --- |
| `A^2 = 2/3`, `lambda^2 = alpha_s(v)/2` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `J = alpha_s(v)^3 sqrt(5)/72` (retained Jarlskog) | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Standard PDG-Wolfenstein expansion of the CKM matrix | textbook |
| Standard `epsilon_K` master formula | textbook |

The Inami-Lim functions `S_0(x_c), S_0(x_t), S_0(x_c, x_t)`, the
running factors `eta_qq`, the bag parameter `B_K`, the decay constant
`f_K`, and the kaon mass-mixing `Delta M_K` are **not** framework-derived.
They are external inputs to the SM `epsilon_K` formula.

This note's claim is therefore the framework's CKM-structural content
of `epsilon_K` -- the identities `(K1)-(K3)` and the resulting `J`
factorization -- not a free-parameter prediction of the absolute
`|epsilon_K|`.

## Derivation

The standard PDG-Wolfenstein expansion of the relevant CKM elements,
truncated at the orders needed for the imaginary parts:

```text
V_cs  =  1 - lambda^2/2 + O(lambda^4)         (real to relevant order),
V_cd  = -lambda + (A^2 lambda^5 / 2)(1 - 2 rho - 2 i eta) + O(lambda^7),
V_ts  = -A lambda^2 + O(lambda^4)             (real to relevant order),
V_td  =  A lambda^3 (1 - rho - i eta) + O(lambda^5).
```

### `(K1)`: `Im[(V_cs^* V_cd)^2] = 2 J`

```text
V_cs^* V_cd  =  (1 - lambda^2/2) [-lambda + A^2 lambda^5 (1/2 - rho - i eta)]
              =  -lambda + lambda^3/2 + A^2 lambda^5 (1/2 - rho)
                       - i A^2 lambda^5 eta + O(lambda^7).

Re(V_cs^* V_cd)  =  -lambda + O(lambda^3),
Im(V_cs^* V_cd)  =  -A^2 lambda^5 eta + O(lambda^7).
```

The imaginary part of the square is

```text
Im[(V_cs^* V_cd)^2]
   =  2 Re(V_cs^* V_cd) Im(V_cs^* V_cd)
   =  2 (-lambda) (-A^2 lambda^5 eta) + O(lambda^8)
   =  2 A^2 lambda^6 eta + O(lambda^8)
   =  2 J.
```

The factor of `lambda` cancels exactly between the LO real and NLO
imaginary parts.

### `(K2)`: `Im[V_cs^* V_cd  V_ts^* V_td] = -J`

```text
V_ts^* V_td  =  (-A lambda^2) (A lambda^3 (1 - rho - i eta))
              =  -A^2 lambda^5 (1 - rho - i eta).

V_cs^* V_cd  V_ts^* V_td
   =  [-lambda + O(lambda^3)] x [-A^2 lambda^5 (1 - rho) + i A^2 lambda^5 eta]
   =  A^2 lambda^6 (1 - rho) - i A^2 lambda^6 eta + O(lambda^8).

Im[V_cs^* V_cd  V_ts^* V_td]  =  -A^2 lambda^6 eta + O(lambda^8)
                              =  -J.
```

### `(K3)`: `Im[(V_ts^* V_td)^2] = -(5 alpha_s^2 / 18) J`

```text
V_ts^* V_td        =  -A^2 lambda^5 (1 - rho) + i A^2 lambda^5 eta,

Re(V_ts^* V_td)    =  -A^2 lambda^5 (1 - rho),
Im(V_ts^* V_td)    =  +A^2 lambda^5 eta,

Im[(V_ts^* V_td)^2]
   =  2 Re(V_ts^* V_td) Im(V_ts^* V_td)
   =  2 [-A^2 lambda^5 (1-rho)] [A^2 lambda^5 eta]
   =  -2 A^4 lambda^10 (1 - rho) eta
   =  -2 A^2 lambda^4 (1 - rho)  *  (A^2 lambda^6 eta)
   =  -2 A^2 lambda^4 (1 - rho) J.
```

In framework values `A^2 = 2/3`, `lambda^2 = alpha_s/2`, `1 - rho = 5/6`:

```text
-2 A^2 lambda^4 (1 - rho)
   =  -2 (2/3) (alpha_s/2)^2 (5/6)
   =  -2 (2/3) (alpha_s^2/4) (5/6)
   =  -2 (10 alpha_s^2)/(3 x 4 x 6)
   =  -(20 alpha_s^2)/72
   =  -(5 alpha_s^2)/18.
```

So `(K3)` evaluates to `-(5 alpha_s(v)^2 / 18) J` in framework values.

### Combined: factorization of `epsilon_K`

The standard `epsilon_K` formula carries the imaginary part of

```text
L  =  lambda_c^2 eta_cc S_0(x_c)
    + lambda_t^2 eta_tt S_0(x_t)
    + 2 lambda_c lambda_t eta_ct S_0(x_c, x_t).
```

Substituting `lambda_q = V_qs^* V_qd` and applying `(K1)-(K3)`:

```text
Im(L)
  =  Im[lambda_c^2] eta_cc S_0(x_c)
   + Im[lambda_t^2] eta_tt S_0(x_t)
   + 2 Im[lambda_c lambda_t] eta_ct S_0(x_c, x_t)
  =  2 J  *  eta_cc S_0(x_c)
   + (-(5 alpha_s^2/18) J) * eta_tt S_0(x_t)
   + 2 (-J) * eta_ct S_0(x_c, x_t)
  =  J x [ 2 eta_cc S_0(x_c)
         - 2 eta_ct S_0(x_c, x_t)
         - (5 alpha_s^2/18) eta_tt S_0(x_t) ].
```

The Jarlskog invariant `J` is the **single CKM-controlling factor**.
Every dependence on `rho`, `eta`, `A`, or `lambda` beyond `J` itself
collapses into either rational coefficients or the explicit
`alpha_s(v)^2`-suppression of the top-loop term.

## Numerical Predictions

With canonical `alpha_s(v) = 0.10330381612227...`,

| Quantity | Closed form | Atlas-LO value |
| --- | --- | ---: |
| `J` | `alpha_s(v)^3 sqrt(5)/72` | `3.424e-5` |
| `Im[(V_cs^* V_cd)^2]` | `2 J` | `+6.847e-5` |
| `Im[V_cs^* V_cd V_ts^* V_td]` | `-J` | `-3.424e-5` |
| `Im[(V_ts^* V_td)^2]` | `-(5 alpha_s^2/18) J` | `-1.015e-7` |
| `5 alpha_s(v)^2 / 18` | -- | `2.964e-3` |

Order-of-magnitude check against standard SM Wolfenstein extraction:

| Quantity | Atlas-LO | Standard SM | Ratio |
| --- | ---: | ---: | ---: |
| `\|J\|` | `3.42e-5` | `3.0e-5` | `1.14` |
| `\|Im(V_ts^* V_td)\|` | `1.51e-4` | `1.4e-4` | `1.08` |
| `\|Im[(V_ts^* V_td)^2]\|` | `1.02e-7` | `~1.4e-7` | `0.73` |

The atlas-LO predictions match the standard Wolfenstein extraction at
the `O(20%)` level expected for a leading-Wolfenstein truncation.

## Why This Pushes the Framework Forward

The kaon CP-violation parameter `epsilon_K` is one of the most
precisely measured CP observables in the Standard Model. Its
dependence on the CKM matrix involves three distinct combinations
(`lambda_c^2`, `lambda_t^2`, `lambda_c lambda_t`), each with its own
Inami-Lim and running factors. Until now, the framework predicted only
the Jarlskog invariant `J` directly; the imaginary parts of these
three combinations were not separately named.

This note proves that **all three reduce to clean atlas-LO multiples
of the same `J`**, with rational coefficients `+2, -1` plus an
explicit `alpha_s^2`-suppressed coefficient. The framework therefore
controls the entire CKM-imaginary-part bracket of `epsilon_K`
through one invariant, not three. The decomposition exposes:

1. The structural origin of the top-loop suppression `(5 alpha_s^2/18)`,
   small in absolute terms but large after multiplication by
   `S_0(x_t) ~ 2.4`.
2. The relative weight of charm-charm versus charm-top contributions,
   `2 eta_cc S_0(x_c) : -2 eta_ct S_0(x_c, x_t)`, which is
   independent of CKM input.
3. The framework's prediction that **every CKM-imaginary contribution
   to `epsilon_K` shares a common `J = alpha_s(v)^3 sqrt(5)/72`
   factor** -- a non-obvious statement once the three combinations are
   written separately.

This sharpens the framework's predictive surface: future precise
measurements of `epsilon_K` test the framework's `J` value (i.e.,
`alpha_s(v)`) against the Inami-Lim and bag-parameter inputs in a
single combined comparator.

## What This Claims

- `Im[(V_cs^* V_cd)^2] = 2 J` exactly at atlas-LO Wolfenstein +
  NLO `V_cd` phase.
- `Im[V_cs^* V_cd V_ts^* V_td] = -J` exactly at atlas-LO Wolfenstein.
- `Im[(V_ts^* V_td)^2] = -(5 alpha_s(v)^2 / 18) J` exactly at atlas-LO
  Wolfenstein, with the closed-form coefficient
  `-2 A^2 lambda^4 (1 - rho)` matching `-(5 alpha_s^2 / 18)` in the
  framework values.
- The full imaginary part of the SM `epsilon_K` CKM bracket factors
  through `J` with explicit rational and `alpha_s^2`-suppressed
  coefficients on the Inami-Lim/running prefactors.

## What This Does Not Claim

- It does not derive `alpha_s(v)`, `B_K`, `f_K`, `M_K`, the Inami-Lim
  functions, or the QCD running factors `eta_qq`. The absolute value
  of `|epsilon_K|` in the framework still inherits these external
  inputs from the standard SM evaluation.
- It does not claim higher-order Wolfenstein corrections to
  `(K1)-(K3)` beyond the leading non-trivial order; the next
  corrections enter at relative `O(lambda^2) ~ alpha_s/2 ~ 5%`.
- It does not promote any BSM contribution to `epsilon_K` or to
  K-Kbar mixing.
- It does not modify the parent CKM atlas/axiom or CP-phase theorems.
- It does not promote the standard ε_K formula itself; that remains
  textbook short-distance K-Kbar mixing.

## Reproduction

```bash
python3 scripts/frontier_ckm_kaon_epsilon_k_jarlskog_decomposition.py
```

Expected result:

```text
TOTAL: PASS=25, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import.

## Cross-References

- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `J = alpha_s(v)^3 sqrt(5)/72` Jarlskog identity.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`.
- [`CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md`](CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md)
  -- companion B_s mixing phase derivation, similar atlas-LO route
  applied to a different CP observable.
- [`CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md`](CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md)
  -- companion cross-system CP ratio, also using the atlas-LO Thales
  geometry.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` derivation.
