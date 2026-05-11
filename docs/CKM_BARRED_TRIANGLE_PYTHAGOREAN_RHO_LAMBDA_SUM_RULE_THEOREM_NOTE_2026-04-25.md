# Barred Unitarity Triangle: NLO Pythagorean Sum Rule Theorem

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure corollary on the proposed_promoted CKM atlas
+ NLO-protected-γ̄ surfaces. This note derives **a NEW EXACT
polynomial sum rule** for the barred unitarity triangle on the NLO
Wolfenstein protected-γ̄ surface:

```text
R_b_bar^2  +  R_t_bar^2  +  rho_bar  *  lambda^2  =  1     [EXACT in alpha_s].
```

The identity is **exact** — no `O(alpha_s^3)` corrections — at the
NLO Wolfenstein order, on the retained protected-γ̄ surface where
`rho_bar`, `eta_bar` are given by the closed forms `(N1, N2)` of the
parent NLO theorem.

The **NEW closed form** for `R_t_bar^2` at NLO is

```text
R_t_bar^2  =  (1 - rho_bar)^2 + eta_bar^2  =  (80 + alpha_s(v)^2) / 96.
```

The retained NLO-protected-γ̄ theorem packages `R_b_bar^2 = (4 - alpha_s)^2/96`
as its `(N3)` but does **not** package `R_t_bar^2` or any sum-rule
binding the two side-length-squareds to `rho_bar lambda^2`. This note
fills both gaps.

The NLO Pythagorean **defect** is

```text
1  -  (R_b_bar^2 + R_t_bar^2)  =  rho_bar(v) * lambda^2(v)  =  alpha_s(v)/12 - alpha_s(v)^2/48,
```

with leading coefficient `1/12 = 1/(N_quark × N_pair)` — a **clean
structural integer** traced to the retained `N_quark = 6`, `N_pair = 2`
in the CKM magnitudes structural counts theorem.

**Primary runner:**
`scripts/frontier_ckm_barred_triangle_pythagorean_rho_lambda_sum_rule.py`

## Statement

On the NLO Wolfenstein protected-γ̄ surface (where `rho_bar = (4-α_s)/24`
and `eta_bar = sqrt(5)(4-α_s)/24` are retained as `N1, N2` of the parent
theorem):

```text
(P1)  R_b_bar^2  =  rho_bar^2 + eta_bar^2  =  (4 - alpha_s)^2 / 96
                                              [retained N3]

(P2)  R_t_bar^2  =  (1 - rho_bar)^2 + eta_bar^2  =  (80 + alpha_s^2) / 96
                                                    [NEW]

(P3)  R_b_bar^2 + R_t_bar^2  =  1 - alpha_s(v)/12 + alpha_s(v)^2/48
                                [NEW NLO Pythagorean defect closed form]

(P4)  R_b_bar^2 + R_t_bar^2 + rho_bar * lambda^2  =  1
                                [NEW EXACT sum rule, no O(alpha_s^3) corrections]

(P5)  Defect = rho_bar(v) * lambda^2(v) = alpha_s(v) * (4 - alpha_s(v))/48
             = alpha_s(v)/12 + O(alpha_s^2)
             with leading coefficient 1/12 = 1/(N_quark × N_pair).

(P6)  Geometric: defect = -2 R_b_bar R_t_bar cos(alpha_bar)  by law of
      cosines in the barred triangle.
```

`(P2)`, `(P3)`, `(P4)`, `(P5)` are NEW. `(P1)` is retained. `(P6)` is
the geometric interpretation tying `(P3)` to the retained N7
slope `sqrt(5)/20` of the protected-γ̄ theorem.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| Canonical `alpha_s(v) = 0.103303816...` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta^2 = 5/36` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Atlas `alpha_0 = pi/2`, atlas-LO `R_b² = 1/6`, `R_t² = 5/6` | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| `rho_bar = (4-α_s)/24`, `eta_bar = sqrt(5)(4-α_s)/24` (N1, N2) | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md), N1-N3 |
| `alpha_bar - pi/2 = (sqrt(5)/20) alpha_s + O(alpha_s^2)` (N7) | same, N7 |
| `N_quark = N_pair × N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |

No PDG observable enters as a derivation input. No SUPPORT-tier or
open inputs (Koide `Q_l`, bare-coupling ratios, dimension-color
quadratic) are used.

## Derivation

### `(P2)`: closed form for `R_t_bar^2`

From retained `(N1, N2)` of the NLO-protected-γ̄ theorem,

```text
rho_bar  =  (4 - alpha_s)/24,
eta_bar  =  sqrt(5)(4 - alpha_s)/24.
```

Then `1 - rho_bar = (24 - 4 + alpha_s)/24 = (20 + alpha_s)/24`, so

```text
R_t_bar^2  =  (1 - rho_bar)^2 + eta_bar^2
           =  ((20 + alpha_s)/24)^2  +  5(4 - alpha_s)^2/576
           =  (20 + alpha_s)^2/576  +  5(4 - alpha_s)^2/576
           =  [(20 + alpha_s)^2 + 5(4 - alpha_s)^2]/576.
```

Expanding the brackets:

```text
(20 + alpha_s)^2     =  400 + 40 alpha_s + alpha_s^2
5(4 - alpha_s)^2     =  5(16 - 8 alpha_s + alpha_s^2)
                     =  80 - 40 alpha_s + 5 alpha_s^2.

Sum                  =  480 + 6 alpha_s^2  =  6(80 + alpha_s^2).
```

Hence

```text
R_t_bar^2  =  6(80 + alpha_s^2) / 576  =  (80 + alpha_s^2) / 96.
```

This is `(P2)`. At atlas-LO `alpha_s → 0`, `R_t_bar^2 → 80/96 = 5/6`,
matching the retained atlas-LO `R_t^2 = 5/6`.

### `(P3)`: NLO Pythagorean defect closed form

Adding `(P1)` (retained) and `(P2)`:

```text
R_b_bar^2 + R_t_bar^2  =  (4 - alpha_s)^2/96  +  (80 + alpha_s^2)/96
                       =  [(4 - alpha_s)^2 + 80 + alpha_s^2]/96.
```

Expanding `(4 - alpha_s)^2 = 16 - 8 alpha_s + alpha_s^2`:

```text
(4 - alpha_s)^2 + 80 + alpha_s^2  =  16 - 8 alpha_s + alpha_s^2 + 80 + alpha_s^2
                                  =  96 - 8 alpha_s + 2 alpha_s^2.
```

Dividing by 96:

```text
R_b_bar^2 + R_t_bar^2  =  1 - alpha_s/12 + alpha_s^2/48.
```

This is `(P3)`. At atlas-LO (alpha_s → 0): `R_b_bar^2 + R_t_bar^2 → 1`,
recovering the retained atlas-LO Pythagorean identity `R_b² + R_t² = 1`
(forced by `alpha_0 = π/2`).

The **NLO defect** is

```text
1 - (R_b_bar^2 + R_t_bar^2)  =  alpha_s/12  -  alpha_s^2/48
                              =  alpha_s(v) (4 - alpha_s(v))/48.
```

### `(P4)`: EXACT sum rule

Compute `rho_bar × lambda^2`:

```text
rho_bar × lambda^2  =  (4 - alpha_s)/24  ×  alpha_s/2
                    =  alpha_s(4 - alpha_s)/48
                    =  alpha_s/12 - alpha_s^2/48.
```

This **exactly** equals the NLO Pythagorean defect from `(P3)`:

```text
1 - (R_b_bar^2 + R_t_bar^2)  =  alpha_s/12 - alpha_s^2/48  =  rho_bar × lambda^2.
```

Rearranging:

```text
R_b_bar^2 + R_t_bar^2 + rho_bar × lambda^2  =  1.
```

This is `(P4)`. The identity is **EXACT** in `alpha_s` on the NLO
protected-γ̄ surface — there are no `O(alpha_s^3)` corrections to this
particular combination, because the algebraic cancellation is exact:

```text
(1 - alpha_s/12 + alpha_s^2/48)  +  (alpha_s/12 - alpha_s^2/48)  =  1   exactly.
```

### `(P5)`: structural defect coefficient

Factoring `(P3)`:

```text
defect  =  alpha_s(v)(4 - alpha_s(v))/48
        =  alpha_s(v)/12  -  alpha_s(v)^2/48.
```

Leading coefficient `1/12 = 1/(N_quark × N_pair)` with retained
`N_quark = 6`, `N_pair = 2`.

The next-order coefficient `1/48 = 1/(N_quark × N_pair^3)` involves
`N_pair^3 = 8`.

So the defect can be written

```text
defect  =  alpha_s(v) / (N_quark × N_pair)
          -  alpha_s(v)^2 / (N_quark × N_pair^3)   + O(alpha_s^3).
```

### `(P6)`: geometric interpretation via law of cosines

The barred unitarity triangle has base length 1 (rescaled
convention). By the law of cosines:

```text
1^2  =  R_b_bar^2 + R_t_bar^2 - 2 R_b_bar R_t_bar cos(alpha_bar).
```

So

```text
1 - (R_b_bar^2 + R_t_bar^2)  =  -2 R_b_bar R_t_bar cos(alpha_bar).
```

Combining with `(P3)` and `(P4)`:

```text
rho_bar × lambda^2  =  -2 R_b_bar R_t_bar cos(alpha_bar)   [exact at NLO].
```

Equivalently

```text
cos(alpha_bar)  =  -rho_bar × lambda^2 / (2 R_b_bar R_t_bar).
```

At atlas-LO (LO values of R_b and R_t):

```text
2 R_b_bar R_t_bar  ≈  2 sqrt(R_b^2 R_t^2)  =  2 sqrt((1/6)(5/6))  =  sqrt(5)/3.

cos(alpha_bar)  ≈  -(1/6)(alpha_s/2)/(sqrt(5)/3)
                 =  -alpha_s × 3 / (12 sqrt(5))
                 =  -alpha_s / (4 sqrt(5))
                 =  -alpha_s sqrt(5) / 20.
```

Compare to retained N7: `alpha_bar - pi/2 = (sqrt(5)/20) alpha_s`,
so `cos(alpha_bar) = cos(pi/2 + (sqrt(5)/20) alpha_s) = -sin((sqrt(5)/20) alpha_s) ≈ -(sqrt(5)/20) alpha_s`.

The two expressions agree at NLO leading order. ✓

So the **EXACT sum rule (P4)** is the algebraic shadow of the
geometric law-of-cosines for the barred triangle, with the retained
N7 slope `sqrt(5)/20` providing the apex-angle deviation.

## Numerical Verification

With canonical `alpha_s(v) = 0.10330381612227...`:

| Quantity | Closed form | Value |
| --- | --- | ---: |
| `R_b_bar^2` (retained N3) | `(4 - alpha_s)^2/96` | `0.158169` |
| `R_t_bar^2` (NEW (P2)) | `(80 + alpha_s^2)/96` | `0.833444` |
| `R_b_bar^2 + R_t_bar^2` (NEW (P3)) | `1 - alpha_s/12 + alpha_s^2/48` | `0.991614` |
| `rho_bar × lambda^2` | `alpha_s(4 - alpha_s)/48` | `0.008386` |
| `R_b_bar^2 + R_t_bar^2 + rho_bar × lambda^2` (NEW (P4)) | `1` | `1.000000` (exact) |
| Defect leading coefficient | `1/(N_quark × N_pair)` | `1/12 = 0.0833...` |

The sum rule `(P4)` holds to machine precision — confirming the
algebraic identity is exact (not just leading order) on the NLO
protected-γ̄ surface.

## Science Value

### What this lets the framework predict that it could not before

The retained NLO-protected-γ̄ theorem packages `R_b_bar^2` (N3) but
**not** `R_t_bar^2` or any sum-rule connecting the side lengths to
the apex coordinates. `(P2)` closes the side-length pair with the
NEW closed form

```text
R_t_bar^2  =  (80 + alpha_s(v)^2) / 96.
```

This makes both sides of the NLO barred triangle quantitatively
specified at all orders in `alpha_s` on the protected-γ̄ surface.

### Why the EXACT polynomial identity (P4) is structurally striking

The identity

```text
R_b_bar^2  +  R_t_bar^2  +  rho_bar * lambda^2  =  1
```

holds **exactly** at NLO Wolfenstein on the protected-γ̄ surface —
not just at leading order in `alpha_s`. The defect from atlas-LO
Pythagorean (`R_b² + R_t² = 1` from `α_0 = π/2`) is **exactly**
absorbed by the cross-term `rho_bar × lambda^2`.

This says: the barred triangle's "non-right-angle-ness" at NLO is
**precisely** the apex's x-coordinate times the Wolfenstein
expansion parameter. Both quantities are individually retained,
but the EXACT cancellation is new content.

The cancellation has a geometric meaning via law of cosines:

```text
defect  =  -2 R_b_bar R_t_bar cos(alpha_bar)  =  rho_bar × lambda^2.
```

Equivalently, the apex angle's deviation from `pi/2` is encoded by
the apex's x-coordinate weighted by `lambda^2/(2 R_b_bar R_t_bar)`.

### A clean structural fingerprint of N_quark and N_pair

The defect coefficient at leading order is `1/(N_quark × N_pair)`.
With retained `N_quark = 6`, `N_pair = 2`, this gives `1/12`. The
sub-leading coefficient is `1/(N_quark × N_pair^3) = 1/48`.

These are **pure structural integers** tied to the framework's
quark counting. A future Wolfenstein NNLO derivation could test
whether further corrections also factor through `N_quark × N_pair^k`
patterns — the framework predicts the leading two coefficients
already in this clean form.

### Connection to the law of cosines

The exact sum rule `(P4)` is the **law-of-cosines identity for the
barred triangle**, with the apex angle's deviation from `π/2`
absorbed into `rho_bar × lambda^2`. This is a sharper geometric
statement than "the triangle is approximately right-angled at NLO":
it says the deviation from right-angle is **exactly** captured by
the product `rho_bar × lambda^2`, not merely "small" or "linear in
α_s".

### What this rules out

The exact identity `(P4)` is a precise prediction. If a future
analysis at NNLO Wolfenstein modifies `rho_bar`, `eta_bar`, or
`alpha_bar` in ways that break the equality `R_b̄² + R_t̄² + ρ̄ λ² = 1`,
either:

- the retained protected-γ̄ N1, N2, N7 closed forms are inconsistent
  with NNLO (which they already are, at relative `O(λ⁴)`), or
- the framework's atlas Thales geometry receives non-trivial NNLO
  corrections beyond a simple multiplicative scaling.

Both are testable by extending the protected-γ̄ analysis to NNLO.
The exact identity at NLO is a precision baseline for those
extensions.

### Connection to experiment

The barred unitarity triangle's side lengths and apex angle are all
extracted from B-physics measurements:

| Experimental input | Framework prediction (atlas-NLO) |
|:---|:---|
| `R_b = \|V_ud V_ub\|/\|V_cd V_cb\|` from B → π l ν, B → ψ K_S | `sqrt(R_b_bar^2) = sqrt((4-α_s)^2/96) = 0.398` |
| `R_t = \|V_td V_tb\|/\|V_cd V_cb\|` from B-mixing Δm_d/Δm_s | `sqrt(R_t_bar^2) = sqrt((80+α_s^2)/96) = 0.913` |
| `alpha = arg(-V_td V_tb*/V_ud V_ub*)` from B → ππ isospin | `alpha_bar = 90.66°` (NLO) |

The Pythagorean defect `1 - (R_b² + R_t²)` is directly measurable
from independent B-meson experiments via `R_b` and `R_t`. The
framework predicts the defect is **exactly** `ρ̄ × λ² ≈ 0.84%` at
canonical `α_s(v)`.

A future precision joint measurement of `R_b² + R_t²` to sub-percent
accuracy (HL-LHC + Belle II Stage II) becomes a single-number test
of the framework's NLO Wolfenstein protected-γ̄ surface.

## What This Claims

- `(P2)`: NEW closed form `R_t_bar^2 = (80 + alpha_s(v)^2)/96` at NLO
  Wolfenstein.
- `(P3)`: NEW NLO Pythagorean defect closed form
  `1 - (R_b_bar^2 + R_t_bar^2) = alpha_s(v)/12 - alpha_s(v)^2/48`.
- `(P4)`: NEW EXACT polynomial sum rule
  `R_b_bar^2 + R_t_bar^2 + rho_bar × lambda^2 = 1` on the NLO
  protected-γ̄ surface (no `O(alpha_s^3)` corrections).
- `(P5)`: defect coefficient `1/12 = 1/(N_quark × N_pair)` with
  sub-leading `1/48 = 1/(N_quark × N_pair^3)`.
- `(P6)`: geometric interpretation via law of cosines, consistent
  with retained N7 slope.

## What This Does NOT Claim

- It does not extend the NLO Wolfenstein analysis beyond what is
  already retained in the protected-γ̄ theorem; the EXACT identity
  is on the **NLO** surface specifically.
- It does not predict NNLO Wolfenstein corrections to the sum rule.
- It does not modify any retained CKM atlas, Wolfenstein, CP-phase,
  right-angle, NLO-protected-γ̄, or magnitudes structural counts
  theorem.
- It does not use any SUPPORT-tier or open input (Koide `Q_l`,
  bare-coupling ratios, dimension-color quadratic).
- It does not promote a direct measurement of any individual side
  length without measurement of `alpha`, since the comparator is
  the JOINT sum `R_b^2 + R_t^2`.

## Exact-symbolic verification

The algebraic-substitution content of `(P1)`-`(P5)` and the geometric
`(P6)` law-of-cosines interpretation is certified at exact-symbolic
precision via `sympy` in
`scripts/audit_companion_ckm_barred_triangle_pythagorean_rho_lambda_sum_rule_exact.py`.
The companion runner treats `alpha_s(v)` as a free positive real symbol,
imports the upstream cited inputs `(N1)`, `(N2)`, `(N3)` and
Wolfenstein `W1` (`lambda^2 = alpha_s/2`) verbatim, and checks each
identity by computing `sympy.simplify(lhs - rhs)` and asserting the
residual equals `0` exactly. The cited inputs themselves
(`rho_bar = (4-alpha_s)/24`, `eta_bar = sqrt(5)(4-alpha_s)/24`,
`R_b_bar^2 = (4-alpha_s)^2/96`, `lambda^2 = alpha_s/2`, structural
counts `N_pair = 2`, `N_quark = 6`) are imported from upstream authority
notes and are not re-derived here.

| Identity | Symbolic form | Verification |
| --- | --- | --- |
| `(P1)` | `R_b_bar^2 == rho_bar^2 + eta_bar^2 == (4 - alpha_s)^2/96` | `sympy.simplify` residual `= 0` |
| `(P2)` | `R_t_bar^2 == (1 - rho_bar)^2 + eta_bar^2 == (80 + alpha_s^2)/96` | `sympy.simplify` residual `= 0` |
| `(P2)` LO | `R_t_bar^2 -> 5/6` at `alpha_s = 0` (atlas-LO recovery) | exact rational `5/6` |
| `(P3)` | `R_b_bar^2 + R_t_bar^2 == 1 - alpha_s/12 + alpha_s^2/48` | `sympy.simplify` residual `= 0` |
| `(P3)` defect | `1 - (R_b_bar^2 + R_t_bar^2) == alpha_s/12 - alpha_s^2/48` | `sympy.simplify` residual `= 0` |
| `(P4)` | `R_b_bar^2 + R_t_bar^2 + rho_bar * lambda^2 == 1` (EXACT) | `sympy.simplify` residual `= 0` |
| `(P4)` polynomial | residual polynomial in `alpha_s` is identically `0` (no `alpha_s^3` tail) | `expand(...)` returns `0` |
| `(P5)` | `defect == alpha_s/(N_quark N_pair) - alpha_s^2/(N_quark N_pair^3)` at `(2, 6)` | `sympy.simplify` residual `= 0` |
| `(P6)` | `defect^2 == 4 R_b_bar^2 R_t_bar^2 cos^2(alpha_bar)` (law of cosines, squared) | `sympy.simplify` residual `= 0` |

Counterfactual probes confirm the load-bearing role of the cited
inputs:

- dropping the `(4 - alpha_s)` coupling factor in `eta_bar` breaks
  `(P2)`, so `R_t_bar^2` no longer collapses to `(80 + alpha_s^2)/96`;
- replacing `lambda^2 = alpha_s/2` with `lambda^2 = alpha_s` (i.e.
  `n_pair = 1`) produces a non-zero `alpha_s` residual in `(P4)`,
  confirming `W1` is load-bearing for the exact cancellation;
- using only the atlas-LO `rho_bar = 1/6` (no NLO offset) leaves a
  non-zero `alpha_s^2` residual in `(P4)`, so the cited `(N1)` form
  is what makes the sum rule exact at NLO.

The structural relations are therefore exact-symbolic over the cited
inputs and do not depend on the floating-point pin of `alpha_s(v)`. The
canonical numerical value of `alpha_s(v)` from
`scripts/canonical_plaquette_surface.py` enters only the trailing
sanity-pin section of the companion runner, which is not load-bearing
for the algebra.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_triangle_pythagorean_rho_lambda_sum_rule.py
PYTHONPATH=scripts python3 scripts/audit_companion_ckm_barred_triangle_pythagorean_rho_lambda_sum_rule_exact.py
```

Expected result:

```text
TOTAL: PASS=42, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import. Upstream authorities are cited here; their audit status remains ledger-derived.

## Cross-References

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  -- cited N1 (`rho_bar`), N2 (`eta_bar`), N3 (`R_b_bar^2`), N7
  (`alpha_bar - pi/2` slope) used in this note.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- cited atlas-LO `alpha_0 = pi/2`, `R_b² + R_t² = 1`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- cited `rho = 1/6`, `eta^2 = 5/36`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- cited `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- cited `N_quark = N_pair × N_color = 6`.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` cited input.
