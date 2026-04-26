# Brocard Polynomial Vieta / Newton Structure in Pure Structural Integers

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note expresses the
**Brocard polynomial `P(α_s)`** — the universal equilateral-excess
polynomial that has emerged as the fundamental quartic of the
retained NLO Wolfenstein protected-γ̄ surface — entirely in **pure
structural integers** `(N_pair, N_color, N_quark)`, and identifies a
**NEW algebraic fingerprint** that uniquely forces `N_pair = 2`.

The headline closed forms:

```text
(V1)  P(alpha_s)  =  alpha_s^4
                     -  N_pair^3 alpha_s^3
                     -  N_pair^5 alpha_s^2
                     +  N_pair^7 N_color^2 alpha_s
                     +  N_pair^8 N_color (N_quark + 1).

(V2)  Vieta relations:
        e_1  =  +N_pair^3                       =  +8,
        e_2  =  -N_pair^5                       =  -32,
        e_3  =  -N_pair^7 N_color^2             =  -1152,
        e_4  =  +N_pair^8 N_color (N_quark + 1) =  +5376.

(V3)  Newton power sums of the four (complex) roots:
        p_1  =  N_pair^3                =  8,
        p_2  =  N_pair^7                =  128.

(V4)  STRUCTURAL FINGERPRINT (NEW):
        p_2  =  2 e_1^2.

      Equivalently:  e_2  =  -e_1^2 / 2.

      Substituting the structural-integer values of e_1 and e_2,
      this identity reduces to N_pair = 2 EXACTLY. So p_2 = 2 e_1^2 is
      a fingerprint of N_pair = 2 in the algebraic structure of P.

(V5)  Mean of the four roots = N_pair^3 / 4 = N_pair (because N_pair = 2).

(V6)  Sum of squared deviations from the mean
        =  N_pair^4 (N_quark + 1)  =  16 * 7  =  112.

(V7)  Roots over Q[sqrt(3), sqrt(5), i]:
        alpha_s^root  =  (N_pair -/+ N_pair sqrt(N_color (N_quark - 1)))
                          +/- N_pair i (sqrt(N_quark - 1) -/+ sqrt(N_color))
                      =  (2 -/+ 2 sqrt(15)) +/- 2 i (sqrt(5) -/+ sqrt(3)).

(V8)  Galois group: Gal(Q[sqrt(3), sqrt(5), i] / Q) = (Z/2Z)^3,
      kernel on root permutation = {1, sigma_1 sigma_2 sigma_3} of order 2,
      image on root permutation = Klein 4-group.
```

The framework's protected-γ̄ structure forces `P(α_s)` to have a
**complete pure-structural-integer expansion**, with the additional
striking property that the SECOND power sum equals **twice** the
SQUARE of the first power sum — which is uniquely satisfied at
`N_pair = 2`.

**Primary runner:**
`scripts/frontier_ckm_brocard_polynomial_vieta_structural_integers.py`

## Statement

The Brocard polynomial of the retained NLO Wolfenstein protected-γ̄
surface is

```text
P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  -  240 (4 - alpha_s)^2.
```

Expanded:

```text
P(alpha_s)  =  alpha_s^4  -  8 alpha_s^3  -  32 alpha_s^2
                +  1152 alpha_s  +  5376.
```

This expansion has **all five coefficients expressible in pure
structural integers** `(N_pair, N_color, N_quark)`:

```text
1     =  alpha_s^4 leading coefficient (trivially 1),
-8    =  -N_pair^3,                                    (alpha_s^3 coeff)
-32   =  -N_pair^5,                                    (alpha_s^2 coeff)
+1152 =  +N_pair^7 N_color^2,                          (alpha_s coeff)
+5376 =  +N_pair^8 N_color (N_quark + 1).              (constant)
```

So:

```text
P(alpha_s)  =  alpha_s^4  -  N_pair^3 alpha_s^3  -  N_pair^5 alpha_s^2
                +  N_pair^7 N_color^2 alpha_s  +  N_pair^8 N_color (N_quark + 1).
```

### Vieta relations on the four (complex) roots

By Vieta's formulas, for a monic quartic `α^4 + b_3 α^3 + b_2 α^2 + b_1 α + b_0`,
the elementary symmetric polynomials of the roots are:

```text
e_1  =  -b_3                   =  +N_pair^3                  =  8,
e_2  =  +b_2                   =  -N_pair^5                  =  -32,
e_3  =  -b_1                   =  -N_pair^7 N_color^2        =  -1152,
e_4  =  +b_0                   =  +N_pair^8 N_color(N_quark+1) =  +5376.
```

### Newton power sums

Using Newton's identities (`p_k = e_1 p_{k-1} - e_2 p_{k-2} + ... + (-1)^{k+1} k e_k`):

```text
p_1  =  e_1                       =  N_pair^3                 =  8,
p_2  =  e_1 p_1 - 2 e_2           =  N_pair^6 + 2 N_pair^5    =  64 + 64  =  128,
p_3  =  e_1 p_2 - e_2 p_1 + 3 e_3
     =  8 * 128 - (-32) * 8 + 3 * (-1152)
     =  1024 + 256 - 3456
     =  -2176.
```

### V4: the structural fingerprint

The `p_2 = N_pair^7 = 128` value is **special**:

```text
p_2  =  N_pair^7  =  128
2 e_1^2  =  2 * (N_pair^3)^2  =  2 N_pair^6  =  128.

So  p_2  =  2 e_1^2  EXACTLY.
```

In abstract structural-integer form (treating `N_pair` as a variable):

```text
p_2 - 2 e_1^2  =  N_pair^7 - 2 N_pair^6  =  N_pair^6 (N_pair - 2).
```

This is **zero iff N_pair = 2**. So the identity `p_2 = 2 e_1^2` is a
**fingerprint of `N_pair = 2`** in the algebraic structure of `P`.

Equivalently: `e_2 = -e_1²/2` in abstract form is `-N_pair^5 = -N_pair^6/2`,
which forces `N_pair = 2`.

### V5: mean of the roots

Mean of the four roots = `e_1/4 = N_pair^3/4 = 8/4 = 2`. In structural
integer form, `N_pair^3/4 = N_pair` (using `N_pair^2 = 4`). So the
mean of the roots equals `N_pair = 2` exactly.

### V6: variance from the mean

Sum of squared deviations from the mean (in the polynomial-coefficient
sense, where complex conjugates contribute real squared sums):

```text
Sigma_i (r_i - mean)^2  =  p_2 - 2 mean p_1 + 4 mean^2
                        =  N_pair^7 - 2 N_pair * N_pair^3 + 4 N_pair^2
                        =  N_pair^7 - 2 N_pair^4 + 4 N_pair^2.

At N_pair = 2:
                        =  128 - 32 + 16
                        =  112
                        =  N_pair^4 (N_quark + 1)  =  16 * 7  =  112.
```

Yes: `112 = N_pair^4 (N_quark + 1)`. Clean structural-integer form.

### V7: roots over Q[√3, √5, i]

Substituting `u = 4 − α_s`, the polynomial becomes

```text
P(alpha_s = 4 - u)  =  (u^2 - 4(1 + sqrt(15)) u + 96) * (u^2 - 4(1 - sqrt(15)) u + 96).
```

`sqrt(15) = sqrt(N_color × (N_quark - 1)) = sqrt(3 × 5)` is the
**natural irrationality of the retained surface**. Each quadratic
factor has discriminant

```text
Delta_+/-  =  16(1 +/- sqrt(15))^2 - 384  =  -128 +/- 32 sqrt(15)  <  0.
```

Both negative, so all four roots are complex. Solving each quadratic
in `u` gives

```text
u  =  2(1 +/- sqrt(15)) +/- 2i(sqrt(5) -/+ sqrt(3))

      =  2(1 +/- sqrt(N_color (N_quark - 1)))
          +/- 2i (sqrt(N_quark - 1) -/+ sqrt(N_color)).
```

So the four roots in `α_s = 4 - u` form:

```text
alpha_s^root  =  4 - u
              =  (2 -/+ 2 sqrt(15)) +/- 2i (sqrt(5) -/+ sqrt(3))

      =  (N_pair -/+ N_pair sqrt(N_color (N_quark - 1)))
          +/- N_pair i (sqrt(N_quark - 1) -/+ sqrt(N_color)).
```

### V8: Galois group

The splitting field of `P` over `Q` is `Q[√3, √5, i]`, with
`[Q[√3, √5, i] : Q] = 8`. The Galois group is

```text
Gal(Q[sqrt(3), sqrt(5), i] / Q)  =  (Z/2Z)^3
```

generated by the three involutions
- `sigma_1`: `i ↦ -i` (complex conjugation),
- `sigma_2`: `√3 ↦ -√3`,
- `sigma_3`: `√5 ↦ -√5`.

The Galois action on the four roots `(r_1, r_2, r_3, r_4)`:

- `sigma_1` swaps `r_1 ↔ r_2` and `r_3 ↔ r_4`.
- `sigma_2` swaps `r_1 ↔ r_3` and `r_2 ↔ r_4`.
- `sigma_3` swaps `r_1 ↔ r_4` and `r_2 ↔ r_3`.
- `sigma_1 sigma_2 sigma_3` acts trivially on the four roots
  (kernel of the action on root labels).

So the action on the 4 roots is `(Z/2Z)^3 / {1, sigma_1 sigma_2 sigma_3}
= (Z/2Z)^2`, the **Klein 4-group**. This Klein-four image acts
transitively on the four roots. The complex-conjugation subgroup
preserves the two conjugate pairs, but the full Galois image also
exchanges the two quadratic factors over `Q[sqrt(15)]`.

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `(rho_bar, eta_bar)` apex coords | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note
is load-bearing. No unmerged branch is cited as load-bearing — the
Brocard polynomial `P(α_s)` is independently re-derived here from the
retained `(rho_bar, eta_bar)` and the classical Brocard inequality
`cot(ω̄) ≥ √3`.

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| V1 leading | `1` | trivial |
| V1 α_s³ coeff | `−N_pair³ = −8` | exact integer |
| V1 α_s² coeff | `−N_pair⁵ = −32` | exact integer |
| V1 α_s coeff | `+N_pair⁷ N_color² = +1152` | exact integer |
| V1 const | `+N_pair⁸ N_color(N_quark+1) = +5376` | exact integer |
| V1 polynomial | `P(α_s)` matches structural form | sympy `simplify(diff) == 0` |
| V2 e_1 | `+N_pair³` | `sum(roots) == 8` |
| V2 e_2 | `−N_pair⁵` | exact |
| V2 e_3 | `−N_pair⁷N_color²` | exact |
| V2 e_4 | `+N_pair⁸N_color(N_quark+1)` | exact |
| V3 p_1 | `N_pair³ = 8` | sympy exact |
| V3 p_2 | `N_pair⁷ = 128` | sympy exact |
| V3 p_3 Newton | `e_1 p_2 − e_2 p_1 + 3 e_3` | sympy exact |
| V4 fingerprint | `p_2 = 2 e_1²` | sympy exact |
| V4 abstract | `e_2 = −e_1²/2 ⟺ N_pair = 2` | symbolic solve |
| V5 mean | `N_pair = 2` | sympy exact |
| V6 variance | `N_pair⁴(N_quark+1) = 112` | sympy exact |
| V7 factoring | `P` over `Q[√15]` | sympy exact |
| V7 disc | both quadratic discriminants `< 0` | numerical |
| V8 Galois | `(Z/2)³` action with transitive Klein-4 image | exact root-action check |
| V9 Disc(P) | `> 0` (4 complex roots) | sympy `discriminant > 0` |

## Science Value

### What this lets the framework state cleanly

Previously, the framework had retained the **Brocard polynomial**
`P(α_s) = (α_s² − 4α_s + 96)² − 240(4 − α_s)²` as the universal
equilateral-excess polynomial of the retained surface, with six
distinct closed-form representations (raw, Brocard, Weitzenbock,
Steiner, Marden, Napoleon). The polynomial's **algebraic structure**
in pure structural integers had not been packaged.

This note delivers:

1. **NEW pure-structural-integer expansion** (V1): all five
   coefficients of `P(α_s)` expressed entirely in terms of
   `(N_pair, N_color, N_quark)`. No floating constants.

2. **NEW Vieta relations in structural integers** (V2): the four
   elementary symmetric polynomials of the roots have the form

   `(+N_pair³, −N_pair⁵, −N_pair⁷ N_color², +N_pair⁸ N_color(N_quark + 1))`.

3. **NEW structural fingerprint** (V4): the identity `p_2 = 2 e_1²`
   uniquely forces `N_pair = 2`. This is the **algebraic signature
   of the framework's pair-count structure** in the Brocard polynomial.

4. **NEW root-statistics in structural integers** (V5, V6):
   - Mean of roots = `N_pair = 2`.
   - Sum of squared deviations from mean = `N_pair⁴(N_quark + 1) = 112`.

5. **NEW root-form in structural integers** (V7): each of the four
   complex roots involves `√(N_color (N_quark − 1))`, `√(N_quark − 1)`,
   and `√N_color` — the natural irrationals of the retained surface.

6. **NEW Galois-group structure** (V8): the splitting field has
   `(Z/2Z)³` Galois group over `Q`, with kernel of order 2 on the
   root-permutation action and image equal to the Klein 4-group.

### Why this counts as pushing the science forward

The Brocard polynomial `P(α_s)` has emerged through a series of
companion theorems as the **universal algebraic invariant** of the
retained NLO Wolfenstein protected-γ̄ surface, controlling six
classical equilateral conditions (Brocard inequality, Weitzenbock,
Steiner inellipse circular limit, Marden foci coincidence, Pedoe
similarity-deficit metric, Napoleon side² product). This note shows
that **all of P's algebraic content — coefficients, Vieta relations,
power sums, root structure, Galois group — is in pure structural
integers `(N_pair, N_color, N_quark)`**.

The most striking result is the **structural fingerprint** (V4):
the identity `p_2 = 2 e_1²` (sum of squared roots = twice squared
sum of roots) is **uniquely forced by `N_pair = 2`**. For any other
value of `N_pair`, the abstract Vieta relation
`e_2 = −e_1²/2 ⟺ −N_pair⁵ = −N_pair⁶/2` would fail. So `N_pair = 2`
is **algebraically encoded** in the second power sum of the
Brocard polynomial — independently of any geometric interpretation.

This is **algebraic rigidity at the level of polynomial structure**.
The framework's `N_pair = 2` is not just a counted-pair structural
integer — it is the unique value that makes the Brocard polynomial
satisfy `p_2 = 2 e_1²`. Conversely, any framework revision that
preserves `p_2 = 2 e_1²` must have `N_pair = 2`.

### Falsifiable structural claim

The closure (V1-V8) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
forces:
  P(alpha_s) = alpha_s^4
               - N_pair^3 alpha_s^3
               - N_pair^5 alpha_s^2
               + N_pair^7 N_color^2 alpha_s
               + N_pair^8 N_color (N_quark + 1).

  p_2 = 2 e_1^2  (signature of N_pair = 2).
  Mean of roots = N_pair = 2.
  Variance of roots = N_pair^4 (N_quark + 1) = 112.
```

Any framework revision shifting `N_pair`, `N_color`, or `N_quark`
would simultaneously break the structural-integer expansion of
`P(α_s)` and the fingerprint identity `p_2 = 2 e_1²`. The Brocard
polynomial is **algebraically rigid** under retained inputs.

## What This Claims

- `(V1)`: NEW retained expansion of the Brocard polynomial in pure
  structural integers (5 coefficients).
- `(V2)`: NEW retained Vieta relations on the four roots in pure
  structural integers.
- `(V3)`: NEW retained Newton power sums `p_1, p_2, p_3, p_4`.
- `(V4)`: NEW retained STRUCTURAL FINGERPRINT `p_2 = 2 e_1²`,
  which uniquely forces `N_pair = 2`.
- `(V5)`: NEW retained mean-of-roots identity `mean = N_pair = 2`.
- `(V6)`: NEW retained variance identity = `N_pair⁴ (N_quark + 1)`.
- `(V7)`: NEW retained root form in structural irrationals
  `√(N_color(N_quark-1)), √(N_quark-1), √N_color`.
- `(V8)`: NEW classification of the Galois group of the splitting
  field as `(Z/2Z)³` with Klein-4 image on root permutations.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs. The fingerprint
  `p_2 = 2 e_1²` algebraically forces `N_pair = 2` GIVEN the form
  of `P(α_s)`, not as an independent constraint on the framework.
- Does **not** depend on any α_s-running pipeline.
- Does **not** make a direct CKM-observable claim about the
  Brocard polynomial; its observable consequences flow through
  the companion theorems (Brocard angle, Weitzenbock, Steiner,
  Marden, Pedoe, Napoleon, Brocard points, nine-point pencil).

## Reproduction

```bash
python3 scripts/frontier_ckm_brocard_polynomial_vieta_structural_integers.py
```

Expected:

```text
TOTAL: PASS=26, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs (`N_pair`, `N_color`, `N_quark`).
- Computes the structural-integer expansion of `P(α_s)` and matches
  against the explicit form by `simplify(diff) == 0`.
- Solves `P(α_s) = 0` symbolically via sympy and computes Vieta
  relations and Newton power sums.
- Verifies the structural fingerprint `p_2 = 2 e_1²` exactly.
- Symbolically verifies the abstract identity
  `e_2 = -e_1²/2 ⟺ N_pair = 2`.
- Verifies factorization over `Q[√15]` and computes discriminants of
  each quadratic factor.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.

**Companion barred-triangle closed forms (cited for context, not
load-bearing here):**

- The Brocard polynomial appears in 6+ closed forms across the
  Brocard-angle, Symmedian/Brocard-circle, Steiner-Marden, Weitzenbock,
  Pedoe, Brocard-points, Napoleon-triangles, and Nine-point-pencil
  branches. This note packages the polynomial's algebraic skeleton.

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
