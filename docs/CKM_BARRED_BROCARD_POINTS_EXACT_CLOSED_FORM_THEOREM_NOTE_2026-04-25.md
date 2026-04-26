# Barred Unitarity-Triangle Brocard POINTS: EXACT Closed Form Theorem

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives the
**EXACT closed forms** for the two **Brocard points** `Ω₁, Ω₂` of the
barred unitarity triangle on the retained NLO Wolfenstein protected-γ̄
surface, and identifies a **NEW Q-polynomial** `Q(α_s)` whose
sibling-relation to the Brocard polynomial `P(α_s)` is exactly
`Q = P + 320(4 − α_s)²`.

The headline closed forms:

```text
(B1)  Omega_1_x  =  (4 - alpha_s)^2 (alpha_s^2 - 4 alpha_s + 96) / Q(alpha_s),
      Omega_1_y  =  4 sqrt(5) (4 - alpha_s)^3 / Q(alpha_s).

(B2)  Omega_2_x  =  4 (4 - alpha_s) (alpha_s^2 - 24 alpha_s + 176) / Q(alpha_s),
      Omega_2_y  =  4 sqrt(5) (4 - alpha_s) (80 + alpha_s^2) / Q(alpha_s).

(B3)  Q(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  +  80 (4 - alpha_s)^2.

(B4)  Q-P relation:
        Q(alpha_s)  =  P(alpha_s)  +  320 (4 - alpha_s)^2,

      where P(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2
      is the Brocard polynomial (universal equilateral excess).
      So Q(alpha_s) is the "Brocard polynomial PLUS 320 (4 - alpha_s)^2 sibling".

(B5)  Q-Weitzenbock relation:
        Q(alpha_s)  =  2304 [(perim_sq)^2 + 16 Area^2]
                     =  N_pair^8 N_color^2 [(perim_sq)^2 + N_pair^4 Area^2].

      Compare to the Weitzenbock identity
        P(alpha_s)  =  2304 [(perim_sq)^2 - 48 Area^2]
                     =  N_pair^8 N_color^2 [(perim_sq)^2 - N_pair^4 N_color Area^2].

(B6)  LO recovery in pure structural integers:
        Omega_1 | LO  =  (N_quark, sqrt(N_quark - 1)) / (N_quark^2 + N_quark - 1)
                       =  (6, sqrt(5))/41,

        Omega_2 | LO  =  (2 N_quark - 1, (N_quark - 1)^(3/2)) / (N_quark^2 + N_quark - 1)
                       =  (11, 5 sqrt(5))/41.

(B7)  NEW Brocard-Brocard distance squared at LO:
        |Omega_1 - Omega_2|^2 | LO  =  N_color (N_quark^2 - 1) / (N_quark^2 + N_quark - 1)^2
                                     =  105 / 1681  =  105/41^2.
```

The denominator `(N_quark² + N_quark − 1) = 41` is also the denominator
of the Brocard-angle trigonometric readout derived here:
`sin²(ω̄|_LO) = (N_quark − 1)/(N_quark² + N_quark − 1) = 5/41`,
`cos²(ω̄|_LO) = N_quark²/(N_quark² + N_quark − 1) = 36/41`. Thus both
Brocard points and the Brocard angle of the same retained triangle are tied
via `(N_quark² + N_quark − 1)` to the LO Wolfenstein imaginary part.

**Primary runner:**
`scripts/frontier_ckm_barred_brocard_points_exact_closed_form.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface, with vertices

```text
V_1 = (0, 0),  V_2 = (1, 0),  V_3 = (rho_bar, eta_bar)
                                 = ((4 - alpha_s)/24, sqrt(5)(4 - alpha_s)/24),
```

side-length squares `a² = (80+α_s²)/96`, `b² = (4-α_s)²/96`, `c² = 1`,
and `Area = √5(4-α_s)/48`, the two Brocard points are:

```text
(B1)  First Brocard point Omega_1 (defined by ∠Omega_1 V_i V_{i+1} = omega_bar
      at each vertex, with cyclic ordering V_1 -> V_2 -> V_3):

        Omega_1_x  =  (4 - alpha_s)^2 (alpha_s^2 - 4 alpha_s + 96) / Q(alpha_s)
                    =  (N_pair^2 - alpha_s)^2 (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)
                       / Q(alpha_s).

        Omega_1_y  =  4 sqrt(5) (4 - alpha_s)^3 / Q(alpha_s)
                    =  N_pair^2 sqrt(N_quark - 1) (N_pair^2 - alpha_s)^3 / Q(alpha_s).

(B2)  Second Brocard point Omega_2 (with reversed cyclic ordering
      V_1 -> V_3 -> V_2):

        Omega_2_x  =  4 (4 - alpha_s) (alpha_s^2 - 24 alpha_s + 176) / Q(alpha_s)
                    =  N_pair^2 (N_pair^2 - alpha_s) (alpha_s^2 - N_pair^2 N_quark alpha_s
                                                       + N_pair^4 (2 N_quark - 1))
                       / Q(alpha_s).

        Omega_2_y  =  4 sqrt(5) (4 - alpha_s) (80 + alpha_s^2) / Q(alpha_s)
                    =  N_pair^2 sqrt(N_quark - 1) (N_pair^2 - alpha_s) (N_pair^4 (N_quark-1) + alpha_s^2)
                       / Q(alpha_s).

(B3)  Q-polynomial:
        Q(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  +  80 (4 - alpha_s)^2.

      In structural integers:
        Q(alpha_s)  =  (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)^2
                       +  N_pair^4 (N_quark - 1) (N_pair^2 - alpha_s)^2.

(B4)  Q-P relation (NEW):
        Q(alpha_s)  =  P(alpha_s)  +  320 (4 - alpha_s)^2
                     =  P(alpha_s)  +  N_pair^6 (N_quark - 1) (N_pair^2 - alpha_s)^2.

      P is the Brocard polynomial (universal equilateral excess); Q is its
      "sibling" obtained by replacing the -240 with +80 sign in the second
      term (equivalent to adding 320 (4 - alpha_s)^2). The two polynomials
      P and Q both appear as fundamental algebraic invariants of the
      retained surface.

(B5)  Q-Weitzenbock relation (NEW):
        Q(alpha_s)  =  2304 [(perim_sq)^2 + 16 Area^2]
                     =  N_pair^8 N_color^2 [(perim_sq)^2 + N_pair^4 Area^2].

      Compare to the Weitzenbock-form (W7c) of P:
        P(alpha_s)  =  2304 [(perim_sq)^2 - 48 Area^2]
                     =  N_pair^8 N_color^2 [(perim_sq)^2 - N_pair^4 N_color Area^2].

      P and Q differ only in the sign-and-coefficient of the Area^2 term:
        P uses -N_pair^4 N_color Area^2,
        Q uses +N_pair^4 Area^2.
      The structural-integer factor of N_color is what distinguishes them.

(B6)  LO recovery -- pure structural integers:
        Omega_1 | LO  =  (N_quark, sqrt(N_quark - 1)) / (N_quark^2 + N_quark - 1)
                       =  (6, sqrt(5))/41,

        Omega_2 | LO  =  (2 N_quark - 1, (N_quark - 1)^(3/2)) / (N_quark^2 + N_quark - 1)
                       =  (11, 5 sqrt(5))/41.

(B7)  NEW Brocard-Brocard distance squared at LO:
        |Omega_1 - Omega_2|^2 | LO  =  N_color (N_quark^2 - 1) / (N_quark^2 + N_quark - 1)^2
                                     =  105 / 1681  =  105/41^2.

      In structural integers, the numerator factors as
        N_color (N_quark - 1)(N_quark + 1)  =  N_color (N_quark^2 - 1).

(B8)  Concyclicity: O, K, Omega_1, Omega_2 lie on the Brocard circle
      (with center M = (O + K)/2 and radius^2 = OK^2/4). All four
      |M - X|^2 distances verified equal symbolically.

(B9)  Brocard angle property: at each vertex of the unitarity triangle,
      the angle subtended from Omega_1 to the next vertex (in cyclic
      order) equals omega_bar. Verified numerically at LO and canonical
      alpha_s.
```

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `rho_bar = (4 - alpha_s)/24`, `eta_bar = sqrt(5)(4 - alpha_s)/24` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note or
unmerged branch is load-bearing. The Brocard-points closed forms here are
derived directly from the retained vertex coordinates plus the classical
Brocard-point definition (barycentric `(ac/b, ab/c, bc/a)`).

## Derivation

### B1, B2: Brocard points via barycentric coordinates

The first and second Brocard points have classical trilinear
coordinates

```text
Omega_1 :  (c/b, a/c, b/a),
Omega_2 :  (b/c, c/a, a/b),
```

where `(a, b, c)` are the side lengths opposite vertices `(A, B, C) =
(V_1, V_2, V_3)`. Converting to barycentric (multiplying each
trilinear by the corresponding side length):

```text
Omega_1 barycentric :  (a c/b, b a/c, c b/a)  =  (m_1, m_2, m_3),
Omega_2 barycentric :  (a b/c, b c/a, c a/b)  =  (m_2, m_3, m_1),
```

with `m_1 = ac/b, m_2 = ab/c, m_3 = bc/a`. So `Ω_1` and `Ω_2` are
related by a cyclic shift of the same triple of weights.

For our retained triangle:

```text
m_1  =  ac/b  =  sqrt(80 + alpha_s^2)/(4 - alpha_s),
m_2  =  ab/c  =  sqrt(80 + alpha_s^2) (4 - alpha_s)/96,
m_3  =  bc/a  =  (4 - alpha_s)/sqrt(80 + alpha_s^2).
```

The sum `m_1 + m_2 + m_3` (after clearing denominators
`96(4 - α_s)√(80 + α_s²)`) becomes

```text
96 (4 - alpha_s) sqrt(80 + alpha_s^2) (m_1 + m_2 + m_3)
   =  96 (80 + alpha_s^2)
       +  (4 - alpha_s)^2 (80 + alpha_s^2)
       +  96 (4 - alpha_s)^2

   =  alpha_s^4 - 8 alpha_s^3 + 288 alpha_s^2 - 1408 alpha_s + 10496

   =  (alpha_s^2 - 4 alpha_s + 96)^2  +  80 (4 - alpha_s)^2

   =:  Q(alpha_s).
```

This is the Q-polynomial defined in B3.

### Closed-form Brocard-point coordinates

```text
Omega_1_x  =  (m_2 + m_3 rho_bar) / (m_1 + m_2 + m_3),
Omega_1_y  =  m_3 eta_bar / (m_1 + m_2 + m_3).
```

After multiplying numerator and denominator by `96(4 - α_s)√(80+α_s²)`:

```text
m_2 + m_3 rho_bar
  =  sqrt(80 + alpha_s^2)(4 - alpha_s)/96  +  (4 - alpha_s)^2/(24 sqrt(80 + alpha_s^2))

After common denominator 96 sqrt(80 + alpha_s^2):
  =  ((80 + alpha_s^2)(4 - alpha_s) + 4(4 - alpha_s)^2) / (96 sqrt(80 + alpha_s^2))
  =  (4 - alpha_s) ((80 + alpha_s^2) + 4(4 - alpha_s)) / (96 sqrt(80 + alpha_s^2))
  =  (4 - alpha_s) (alpha_s^2 - 4 alpha_s + 96) / (96 sqrt(80 + alpha_s^2)).

Multiplying through by 96 (4 - alpha_s) sqrt(80 + alpha_s^2):
Omega_1_x  =  (4 - alpha_s)^2 (alpha_s^2 - 4 alpha_s + 96) / Q(alpha_s).
```

Similarly for `Ω_1_y` and the cyclic-shifted `Ω_2`.

### B3, B4: Q-polynomial and its relation to P

`Q(α_s) = (α_s² − 4α_s + 96)² + 80(4 − α_s)²` is the natural
Brocard-point denominator polynomial. Compare to the Brocard polynomial
`P(α_s) = (α_s² − 4α_s + 96)² − 240(4 − α_s)²`:

```text
Q  -  P  =  (80 - (-240)) (4 - alpha_s)^2  =  320 (4 - alpha_s)^2.
```

So Q is P shifted by `320(4-α_s)²`. In structural integers,
`320 = 64 × 5 = N_pair⁶ × (N_quark − 1)`. The Q polynomial is the
"Brocard-points sibling" of the equilateral-excess polynomial.

### B5: Q-Weitzenbock relation

In the Weitzenbock form, the perimeter² and Area appear:

```text
Q(alpha_s)  =  2304 [(perim_sq)^2 + 16 Area^2].
```

For the comparison polynomial `P` on the same retained surface, the
Weitzenbock-form expression is:

```text
P(alpha_s)  =  2304 [(perim_sq)^2 - 48 Area^2].
```

Both have the same `(perim_sq)²` head; they differ only in the sign
and coefficient of the `Area²` term. The structural-integer
distinction is `+N_pair⁴` (in Q) versus `−N_pair⁴ N_color` (in P).

### B6: LO recovery in pure structural integers

At `α_s = 0`:

```text
Q(0)  =  96^2 + 80 * 16  =  9216 + 1280  =  10496  =  256 * 41
       =  N_pair^8 (N_quark^2 + N_quark - 1).

Omega_1 | LO_x  =  16 * 96 / 10496  =  1536/10496  =  6/41
                =  N_quark / (N_quark^2 + N_quark - 1).

Omega_1 | LO_y  =  4 sqrt(5) * 64 / 10496  =  256 sqrt(5)/10496  =  sqrt(5)/41
                =  sqrt(N_quark - 1) / (N_quark^2 + N_quark - 1).
```

For `Ω_2`:

```text
At alpha_s = 0:
  alpha_s^2 - 24 alpha_s + 176 |_{alpha_s = 0}  =  176  =  N_pair^4 (2 N_quark - 1),
  80 + alpha_s^2 |_{alpha_s = 0}                =  80  =  N_pair^4 (N_quark - 1).

Omega_2 | LO_x  =  4 * 4 * 176/10496  =  2816/10496  =  11/41
                =  (2 N_quark - 1)/(N_quark^2 + N_quark - 1).

Omega_2 | LO_y  =  4 sqrt(5) * 4 * 80/10496  =  1280 sqrt(5)/10496  =  5 sqrt(5)/41
                =  (N_quark - 1) sqrt(N_quark - 1)/(N_quark^2 + N_quark - 1).
```

The denominator `N_quark² + N_quark − 1 = 41` is the same one that
appears in the locally derived Brocard-angle readout
`sin²(ω̄|_LO) = 5/41`, `cos²(ω̄|_LO) = 36/41`. This algebraically ties
the Brocard angle and Brocard points of the same triangle.

### B7: Brocard-Brocard distance squared at LO

```text
Omega_1 - Omega_2 | LO  =  ((6 - 11)/41,  (sqrt(5) - 5 sqrt(5))/41)
                         =  (-5/41,  -4 sqrt(5)/41).

|Omega_1 - Omega_2|^2 | LO  =  (5/41)^2 + (4 sqrt(5)/41)^2
                              =  (25 + 80)/41^2
                              =  105/41^2.

In structural integers:
  105  =  3 * 5 * 7  =  N_color * (N_quark - 1) * (N_quark + 1)  =  N_color (N_quark^2 - 1).

So |Omega_1 - Omega_2|^2 | LO  =  N_color (N_quark^2 - 1) / (N_quark^2 + N_quark - 1)^2.
```

### B8, B9: concyclicity and Brocard angle property

The four points `O, K, Ω_1, Ω_2` lie on the Brocard circle (center
`M = (O+K)/2`, radius `OK/2`). The runner verifies symbolically that
all four `|M − X|² = OK²/4`.

The Brocard angle property (`∠Ω_1 V_i V_{i+1} = ω̄` at each vertex)
is verified numerically at LO and canonical `α_s`, with all three
angles matching `ω̄` to within `10⁻²` degrees.

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| B1 Ω_1_x | `(4-α_s)²(α_s²-4α_s+96)/Q` | sympy `simplify(diff) == 0` |
| B1 Ω_1_y | `4√5(4-α_s)³/Q` | sympy `simplify(diff) == 0` |
| B2 Ω_2_x | `4(4-α_s)(α_s²-24α_s+176)/Q` | sympy `simplify(diff) == 0` |
| B2 Ω_2_y | `4√5(4-α_s)(80+α_s²)/Q` | sympy `simplify(diff) == 0` |
| B3 Q-form | `(α_s²-4α_s+96)² + 80(4-α_s)²` | sympy exact |
| B3 Q(0) | `10496 = 256·41 = N_pair⁸(N_quark²+N_quark-1)` | exact integer |
| B4 Q-P | `Q = P + 320(4-α_s)²` | sympy `simplify(diff) == 0` |
| B4 struct | `320 = N_pair⁶(N_quark-1)` | exact integer |
| B5 Q-Weitz | `Q = 2304[(perim²)²+16·Area²]` | sympy `simplify(diff) == 0` |
| B5 struct | `2304 = N_pair⁸N_color²`, `16 = N_pair⁴` | exact integer |
| B6 Ω_1 LO | `(N_quark, √(N_quark-1))/(N_quark²+N_quark-1) = (6,√5)/41` | sympy exact |
| B6 Ω_2 LO | `(2N_quark-1, (N_quark-1)^(3/2))/(N_quark²+N_quark-1) = (11, 5√5)/41` | sympy exact |
| B7 |Ω_1-Ω_2|² LO | `N_color(N_quark²-1)/(N_quark²+N_quark-1)² = 105/41²` | sympy exact |
| B9 Brocard-angle LO | `sin²(ω̄)=5/41`, `cos²(ω̄)=36/41` | exact |
| B8 concyclic O | `\|M-O\|² = OK²/4` | sympy `simplify == 0` |
| B8 concyclic K | `\|M-K\|² = OK²/4` | sympy exact |
| B8 concyclic Ω_1 | `\|M-Ω_1\|² = OK²/4` | sympy exact |
| B8 concyclic Ω_2 | `\|M-Ω_2\|² = OK²/4` | sympy exact |
| B9 angle property | `∠Ω_1V_iV_{i+1} = ω̄` at all vertices | numerical PASS |

Numerical readout for `|Ω_1 − Ω_2|²` across α_s:

| `α_s(v)` | `|Ω_1 − Ω_2|²` |
| ---: | ---: |
| 0 (LO) | 0.0624628 (= 105/1681) |
| 0.118 | 0.0622329 |
| 0.30 | 0.0614725 |
| 0.50 | 0.0600576 |

The Brocard-Brocard distance decreases mildly over this sample range.

## Science Value

### What this lets the framework state cleanly

The current main surface already carries several exact barred-triangle
geometry corollaries, including apex-angle, circumradius/circumcenter,
orthocenter/Euler-line, and Pedoe similarity-deficit formulae. The two
**Brocard points** themselves — the classical interior triangle points
whose triple-equal-angle property generates the Brocard angle — were not
previously expressed in closed form on the retained surface.

This note delivers:

1. **NEW closed forms for both Brocard points** (B1, B2): the first
   and second Brocard points have rational-function coordinates in
   `α_s`, with the same denominator polynomial `Q(α_s)`.

2. **NEW Q-polynomial** (B3): `Q(α_s) = (α_s² − 4α_s + 96)² + 80(4 − α_s)²`
   — the natural Brocard-point denominator. Q is **the second
   fundamental polynomial of the retained surface**, complementary to
   the Brocard polynomial P.

3. **NEW Q-P sibling relation** (B4): `Q = P + 320(4 − α_s)²`. The
   Brocard polynomial P (universal equilateral excess) and the
   Brocard-points denominator Q (interior-point structure) differ by
   a clean structural-integer multiple of `(4 − α_s)²`.

4. **NEW Q-Weitzenbock relation** (B5):
   `Q = 2304[(perim²)² + 16·Area²]`. Compare to
   `P = 2304[(perim²)² − 48·Area²]` (Weitzenbock form).
   P and Q differ only in the sign-and-coefficient of the `Area²`
   term — `−N_pair⁴N_color` vs `+N_pair⁴`.

5. **NEW LO structural-integer recoveries** (B6):
   - `Ω_1|_LO = (N_quark, √(N_quark − 1))/(N_quark² + N_quark − 1) = (6, √5)/41`,
   - `Ω_2|_LO = (2N_quark − 1, (N_quark − 1)^(3/2))/(N_quark² + N_quark − 1) = (11, 5√5)/41`.
   The denominator `N_quark² + N_quark − 1 = 41` is the same structural
   integer that appears in `sin²(ω̄|_LO) = (N_quark − 1)/(N_quark² + N_quark − 1)`.

6. **NEW Brocard-Brocard distance** (B7):
   `|Ω_1 − Ω_2|²|_LO = N_color(N_quark² − 1)/(N_quark² + N_quark − 1)² = 105/41²`.
   The numerator factors as `N_color × (N_quark − 1)(N_quark + 1)` —
   purely structural-integer.

7. **NEW concyclicity verification** (B8): the four points
   `O, K, Ω_1, Ω_2` lie on the Brocard circle, with all four `|M − X|²`
   distances exactly equal symbolically.

### Why this counts as pushing the science forward

The Brocard points are the **central interior points** of the
classical Brocard structure of any triangle. Together with the
Brocard angle, they characterise the "rotational asymmetry" of the
triangle. For the retained CKM unitarity triangle, the Brocard points
have **closed-form coordinates** with structural-integer denominators.

The Q-P sibling relation (B4) and Q-Weitzenbock form (B5) reveal that
**Q is a sibling polynomial of P** in the same algebraic sense that
the Brocard points are siblings of the Brocard angle. This pairs P
and Q as the **two fundamental quartic polynomials** of the retained
NLO Wolfenstein protected-γ̄ surface:

- `P(α_s)` measures **non-equilateralness** (zero iff equilateral),
- `Q(α_s)` parameterises the **Brocard-point denominator**.

Both are degree-4 polynomials in `α_s`, both have the same `(α_s² − 4α_s + 96)²`
head term, and they differ only in their `(4 − α_s)²` second term:
P uses `−240(4−α_s)²`, Q uses `+80(4−α_s)²`. The Q-P difference
`320(4−α_s)²` is `N_pair⁶(N_quark − 1)(N_pair² − α_s)²` in structural form.

The recurrence of `(N_quark² + N_quark − 1) = 41` as the LO
denominator in B6, B7, and the locally derived `sin²(ω̄|_LO)` is
structurally striking: a single irrational-free integer governs the
Brocard structure of the LO unitarity triangle. This is **algebraic
rigidity**: the framework's protected-γ̄ and structural-integer inputs
force `41 = N_quark² + N_quark − 1` to appear as the universal Brocard
denominator at LO.

### Falsifiable structural claim

The closure (B1-B7) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
forces:
  Q(alpha_s)  =  P(alpha_s)  +  N_pair^6 (N_quark - 1)(N_pair^2 - alpha_s)^2,
  Omega_1 | LO  =  (N_quark, sqrt(N_quark - 1))/(N_quark^2 + N_quark - 1),
  |Omega_1 - Omega_2|^2 | LO  =  N_color (N_quark^2 - 1)/(N_quark^2 + N_quark - 1)^2.
```

Any framework revision moving `(rho_bar, eta_bar)` off the retained
protected-γ̄ surface would break the Q-polynomial structure
simultaneously. The recurrence of `(N_quark² + N_quark − 1)` at LO is
algebraically rigid: it derives from `1 + (N_quark − 1)/N_quark² =
(N_quark² + N_quark − 1)/N_quark²` (the LO `1 + tan²(ω̄)` identity).

## What This Claims

- `(B1, B2)`: NEW retained closed forms for both Brocard points
  `Ω_1, Ω_2` on the protected-γ̄ surface.
- `(B3)`: NEW retained Q-polynomial
  `Q(α_s) = (α_s² − 4α_s + 96)² + 80(4 − α_s)²`.
- `(B4)`: NEW retained Q-P sibling relation `Q = P + 320(4 − α_s)²`.
- `(B5)`: NEW retained Q-Weitzenbock relation
  `Q = 2304[(perim²)² + 16·Area²]`.
- `(B6)`: NEW retained LO recoveries in pure structural integers:
  `Ω_1|_LO = (N_quark, √(N_quark − 1))/41`,
  `Ω_2|_LO = (2N_quark − 1, (N_quark − 1)^(3/2))/41`.
- `(B7)`: NEW retained Brocard-Brocard distance squared at LO,
  `|Ω_1 − Ω_2|²|_LO = N_color(N_quark² − 1)/(N_quark² + N_quark − 1)² = 105/41²`.
- `(B8)`: NEW retained concyclicity verification of the four points
  `O, K, Ω_1, Ω_2` on the Brocard circle.
- `(B9)`: NEW retained Brocard angle property of `Ω_1` (numerical
  verification that `∠Ω_1 V_i V_{i+1} = ω̄` at each vertex).

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing or contextual
  authorities.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs.
- Does **not** depend on any α_s-running pipeline.
- Does **not** make a direct CKM-observable claim about the Brocard
  points; they are derived geometric structures of the unitarity
  triangle.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_brocard_points_exact_closed_form.py
```

Expected:

```text
TOTAL: PASS=39, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs (`rho_bar`, `eta_bar`,
  `N_pair`, `N_color`, `N_quark`).
- Computes B1–B9 symbolically via sympy at the retained values and
  asserts each closed form by `simplify(diff) == 0`.
- Verifies the Q-polynomial form, the Q-P relation, and the
  Q-Weitzenbock relation.
- Verifies that all four points `O, K, Ω_1, Ω_2` lie on the Brocard
  circle by checking `|M − X|² = OK²/4` for each.
- Verifies the Brocard angle property of `Ω_1` numerically at LO and
  canonical `α_s`.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.

**Companion barred-triangle closed forms already on main (cited for context,
not load-bearing here):**

- [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — circumradius `R̄`, circumcenter `O`.
- [`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — apex angle `α̃`.
- [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — orthocenter, centroid, Euler line.
- [`CKM_BARRED_PEDOE_SIMILARITY_DEFICIT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_PEDOE_SIMILARITY_DEFICIT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — Pedoe similarity-deficit metric on the same retained surface.

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
