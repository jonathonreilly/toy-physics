# Kaon epsilon_K Jarlskog Decomposition Theorem

**Date:** 2026-04-25

**Status:** proposed_retained atlas-leading CKM-structure corollary on the proposed_promoted
atlas/axiom surface. This note derives how the three CKM combinations
entering the Standard Model expression for the kaon CP-violation parameter
`epsilon_K` factor through the framework's atlas Jarlskog-area factor
`J_0 = alpha_s(v)^3 sqrt(5)/72`. Specifically, at leading non-trivial
Wolfenstein order:

```text
(K1)  Im[(V_cs^* V_cd)^2]              =  +2 J_0,
(K2)  Im[V_cs^* V_cd  V_ts^* V_td]     =  -J_0,
(K3)  Im[(V_ts^* V_td)^2]              =  -(5 alpha_s(v)^2 / 18) J_0.
```

These three identities convert the standard `epsilon_K` formula's
CKM-imaginary-part bracket into a single overall factor of `J_0` times
a kinematic and Wilson-coefficient combination of Inami-Lim functions
and short-distance QCD running factors:

```text
Im(L)  =  J_0 x [ 2 eta_cc S_0(x_c)
              - 2 eta_ct S_0(x_c, x_t)
              - (5 alpha_s(v)^2 / 18) eta_tt S_0(x_t) ],
```

where `Im(L)` is the imaginary part of
`lambda_c^2 eta_cc S_0(x_c) + lambda_t^2 eta_tt S_0(x_t) + 2 lambda_c lambda_t eta_ct S_0(x_c, x_t)`
with `lambda_q = V_qs^* V_qd`. This is the framework's new
CKM-structural content for the kaon CP-violation observable: the
atlas Jarlskog-area factor `J_0` becomes the universal CKM scale for the
epsilon_K imaginary-part bracket, and the relative weights between
charm-charm, charm-top, and top-top contributions are fixed at
atlas-leading order as rational coefficients plus one explicit
`alpha_s(v)^2` suppression.

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
J_0     = A^2 lambda^6 eta = alpha_s(v)^3 sqrt(5)/72
                           [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM]
```

the leading-order imaginary parts of the three CKM kaon combinations are

```text
(K1)  Im[(V_cs^* V_cd)^2]        =  2 J_0,
(K2)  Im[V_cs^* V_cd  V_ts^* V_td] =  -J_0,
(K3)  Im[(V_ts^* V_td)^2]        =  -(5 alpha_s^2 / 18) J_0
                                  =  -2 A^2 lambda^4 (1 - rho) J_0.
```

Identities `(K1)` and `(K2)` carry rational coefficients
`(+2, -1)`. Identity `(K3)` carries an `alpha_s^2`-suppressed
coefficient that rewrites in compact form as
`-2 A^2 lambda^4 (1 - rho) = -(5 alpha_s^2 / 18)` in framework
values.

Plugging into the standard `epsilon_K` formula, the framework's CKM
factorization statement is

```text
|epsilon_K|  =  kappa_eps * (G_F^2 f_K^2 M_K M_W^2)/(12 pi^2 sqrt(2) Delta M_K)
              * B_K * |Im(L)|,

Im(L)  =  J_0 x [ 2 eta_cc S_0(x_c)
              - 2 eta_ct S_0(x_c, x_t)
              - (5 alpha_s^2 / 18) eta_tt S_0(x_t) ].
```

The bracket contains only Inami-Lim functions and short-distance QCD
running factors -- no CKM input. The framework supplies the full CKM
content as the single overall `J_0` factor.

## Retained Inputs

| Input | Authority |
| --- | --- |
| `A^2 = 2/3`, `lambda^2 = alpha_s(v)/2` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `J_0 = alpha_s(v)^3 sqrt(5)/72` (atlas Jarlskog-area factor) | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Standard PDG-Wolfenstein expansion of the CKM matrix | textbook |
| Standard `epsilon_K` master formula | textbook |

The Inami-Lim functions `S_0(x_c), S_0(x_t), S_0(x_c, x_t)`, the
running factors `eta_qq`, the bag parameter `B_K`, the decay constant
`f_K`, and the kaon mass-mixing `Delta M_K` are **not** framework-derived.
They are external inputs to the SM `epsilon_K` formula.

This note's claim is therefore the framework's CKM-structural content
of `epsilon_K` -- the identities `(K1)-(K3)` and the resulting `J_0`
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

### `(K1)`: `Im[(V_cs^* V_cd)^2] = 2 J_0`

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
   =  2 J_0.
```

The factor of `lambda` cancels exactly between the LO real and NLO
imaginary parts.

### `(K2)`: `Im[V_cs^* V_cd  V_ts^* V_td] = -J_0`

```text
V_ts^* V_td  =  (-A lambda^2) (A lambda^3 (1 - rho - i eta))
              =  -A^2 lambda^5 (1 - rho - i eta).

V_cs^* V_cd  V_ts^* V_td
   =  [-lambda + O(lambda^3)] x [-A^2 lambda^5 (1 - rho) + i A^2 lambda^5 eta]
   =  A^2 lambda^6 (1 - rho) - i A^2 lambda^6 eta + O(lambda^8).

Im[V_cs^* V_cd  V_ts^* V_td]  =  -A^2 lambda^6 eta + O(lambda^8)
                              =  -J_0.
```

### `(K3)`: `Im[(V_ts^* V_td)^2] = -(5 alpha_s^2 / 18) J_0`

```text
V_ts^* V_td        =  -A^2 lambda^5 (1 - rho) + i A^2 lambda^5 eta,

Re(V_ts^* V_td)    =  -A^2 lambda^5 (1 - rho),
Im(V_ts^* V_td)    =  +A^2 lambda^5 eta,

Im[(V_ts^* V_td)^2]
   =  2 Re(V_ts^* V_td) Im(V_ts^* V_td)
   =  2 [-A^2 lambda^5 (1-rho)] [A^2 lambda^5 eta]
   =  -2 A^4 lambda^10 (1 - rho) eta
   =  -2 A^2 lambda^4 (1 - rho)  *  (A^2 lambda^6 eta)
   =  -2 A^2 lambda^4 (1 - rho) J_0.
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

So `(K3)` evaluates to `-(5 alpha_s(v)^2 / 18) J_0` in framework values.

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
  =  2 J_0  *  eta_cc S_0(x_c)
   + (-(5 alpha_s^2/18) J_0) * eta_tt S_0(x_t)
   + 2 (-J_0) * eta_ct S_0(x_c, x_t)
  =  J_0 x [ 2 eta_cc S_0(x_c)
         - 2 eta_ct S_0(x_c, x_t)
         - (5 alpha_s^2/18) eta_tt S_0(x_t) ].
```

The atlas Jarlskog-area factor `J_0` is the **single CKM-controlling factor**.
Every dependence on `rho`, `eta`, `A`, or `lambda` beyond `J_0` itself
collapses into either rational coefficients or the explicit
`alpha_s(v)^2`-suppression of the top-loop term.

## Numerical CKM Readout

With canonical `alpha_s(v) = 0.10330381612227...`,

| Quantity | Closed form | Atlas-LO value |
| --- | --- | ---: |
| `J_0` | `alpha_s(v)^3 sqrt(5)/72` | `3.424e-5` |
| `Im[(V_cs^* V_cd)^2]` | `2 J_0` | `+6.847e-5` |
| `Im[V_cs^* V_cd V_ts^* V_td]` | `-J_0` | `-3.424e-5` |
| `Im[(V_ts^* V_td)^2]` | `-(5 alpha_s^2/18) J_0` | `-1.015e-7` |
| `5 alpha_s(v)^2 / 18` | -- | `2.964e-3` |

Order-of-magnitude check against standard SM Wolfenstein extraction:

| Quantity | Atlas-LO | Standard SM | Ratio |
| --- | ---: | ---: | ---: |
| `\|J_0\|` | `3.42e-5` | `3.0e-5` | `1.14` |
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
the atlas Jarlskog-area factor `J_0` directly; the imaginary parts of these
three combinations were not separately named.

This note proves that all three reduce to clean atlas-LO multiples
of the same `J_0`, with rational coefficients `+2, -1` plus an
explicit `alpha_s^2`-suppressed coefficient. The framework therefore
controls the entire CKM-imaginary-part bracket of `epsilon_K`
through one invariant, not three. The decomposition exposes:

1. The structural origin of the top-loop suppression `(5 alpha_s^2/18)`,
   small in absolute terms but large after multiplication by
   `S_0(x_t) ~ 2.4`.
2. The relative weight of charm-charm versus charm-top contributions,
   `2 eta_cc S_0(x_c) : -2 eta_ct S_0(x_c, x_t)`, which is
   independent of CKM input.
3. The framework's structural statement that every CKM-imaginary contribution
   to `epsilon_K` shares a common `J_0 = alpha_s(v)^3 sqrt(5)/72`
   factor -- a non-obvious statement once the three combinations are
   written separately.

This sharpens the framework's predictive surface: future precise
measurements of `epsilon_K` test the framework's atlas `J_0` value (i.e.,
`alpha_s(v)`) against the Inami-Lim and bag-parameter inputs in a
single combined comparator.

## What This Claims

- `Im[(V_cs^* V_cd)^2] = 2 J_0` at atlas-leading Wolfenstein order with
  the NLO `V_cd` phase retained.
- `Im[V_cs^* V_cd V_ts^* V_td] = -J_0` at atlas-leading Wolfenstein order.
- `Im[(V_ts^* V_td)^2] = -(5 alpha_s(v)^2 / 18) J_0` at atlas-leading
  Wolfenstein, with the closed-form coefficient
  `-2 A^2 lambda^4 (1 - rho)` matching `-(5 alpha_s^2 / 18)` in the
  framework values.
- The full imaginary part of the SM `epsilon_K` CKM bracket factors
  through `J_0` with explicit rational and `alpha_s^2`-suppressed
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
- It does not promote the standard `epsilon_K` formula itself; that remains
  textbook short-distance K-Kbar mixing.

## Exact-symbolic verification

The closed-form Jarlskog-decomposition identities `(K1)`, `(K2)`, `(K3)`
and the resulting `J_0`-factorization of the `epsilon_K` imaginary
bracket are certified at exact-symbolic precision via `sympy` in
`scripts/audit_companion_ckm_kaon_epsilon_k_jarlskog_decomposition_exact.py`.
The companion runner treats `alpha_s(v)` as a free positive real
symbol and `lambda` as the Wolfenstein expansion parameter, imports
the upstream atlas inputs verbatim as exact `sympy.Rational` /
`sympy.sqrt` values, and checks each identity by computing
`sympy.simplify(lhs - rhs)` (or comparing series-coefficient extracts)
and asserting the residual equals `0` exactly. The cited inputs
themselves (`lambda^2 = alpha_s/2`, `A^2 = 2/3`, `rho = 1/6`,
`eta = sqrt(5)/6`, `J_0 = alpha_s^3 sqrt(5)/72`) are imported from
upstream authority notes and are not re-derived here.

| Identity | Symbolic form | Verification |
| --- | --- | --- |
| `J_0` cited | `A^2 lambda^6 eta == alpha_s^3 sqrt(5)/72` | `sympy.simplify` residual `= 0` |
| `(K1)` leading | `Im[(V_cs^* V_cd)^2]` lam^6 coefficient `== 2 A^2 eta = sqrt(5)/9` | series-coefficient match |
| `(K1)` reduction | leading `== 2 J_0` parametric in `alpha_s` | `sympy.simplify` residual `= 0` |
| `(K1)` rational | coefficient on `J_0` is the rational `+2` | exact rational |
| `(K2)` leading | `Im[V_cs^* V_cd V_ts^* V_td]` lam^6 coefficient `== -A^2 eta = -sqrt(5)/18` | series-coefficient match |
| `(K2)` reduction | leading `== -J_0` parametric in `alpha_s` | `sympy.simplify` residual `= 0` |
| `(K2)` rational | coefficient on `J_0` is the rational `-1` | exact rational |
| `(K3)` leading | `Im[(V_ts^* V_td)^2]` lam^10 coefficient `== -2 A^4 (1-rho) eta` | series-coefficient match |
| `(K3)` closed-form | `-2 A^2 lambda^4 (1 - rho) == -(5 alpha_s^2 / 18)` | `sympy.simplify` residual `= 0` |
| `(K3)` reduction | leading `== -(5 alpha_s^2/18) J_0` parametric in `alpha_s` | `sympy.simplify` residual `= 0` |
| `Im(L)` | factorizes through `J_0` with `(+2 eta_cc, -2 eta_ct, -(5 alpha_s^2/18) eta_tt)` | `sympy.simplify` residual `= 0` |

Counterfactual probes confirm the imported atlas inputs are each
individually load-bearing for the closed-form `(K3)` coefficient:

- substituting `A^2 = 1` collapses the `(K3)` coefficient to
  `-(5 alpha_s^2 / 12)`, not `-(5 alpha_s^2 / 18)`;
- substituting `rho = 0` collapses the `(K3)` coefficient to
  `-alpha_s^2 / 3`, not `-(5 alpha_s^2 / 18)`;
- substituting `lambda^2 = alpha_s` (i.e. `n_pair = 1`) collapses the
  `(K3)` coefficient to `-(10 alpha_s^2 / 9)`, not `-(5 alpha_s^2 / 18)`;
- substituting `eta = 0` collapses `J_0` to `0` and all of `(K1)`,
  `(K2)`, `(K3)` vanish.

The structural relations are therefore exact-symbolic over the
imported atlas inputs and do not depend on the floating-point pin of
`alpha_s(v)`. The numerical pin enters only the parent runner's
trailing comparator section, which is not load-bearing for the
algebra.

## Reproduction

```bash
python3 scripts/frontier_ckm_kaon_epsilon_k_jarlskog_decomposition.py
PYTHONPATH=scripts python3 scripts/audit_companion_ckm_kaon_epsilon_k_jarlskog_decomposition_exact.py
```

Expected result:

```text
TOTAL: PASS=25, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import.

## Cross-References

- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained atlas `J_0 = alpha_s(v)^3 sqrt(5)/72` Jarlskog-area identity.
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
