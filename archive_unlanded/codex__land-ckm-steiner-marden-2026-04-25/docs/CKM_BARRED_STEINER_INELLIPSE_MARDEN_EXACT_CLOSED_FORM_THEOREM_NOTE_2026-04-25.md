# Barred Unitarity-Triangle Steiner Inellipse + Marden's Theorem: EXACT Closed Form

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives the
**EXACT closed forms** for the **Steiner inellipse** of the barred
unitarity triangle (centre, semi-axes, eccentricity) and the
**Marden foci** (the two roots of `p'(z)` for `p(z) = z(z-1)(z-V_3)`,
which by Marden's theorem are exactly the Steiner inellipse foci).

The headline closed forms:

```text
(M5)  semi-axes squared, individual:
        semi_a^2  =  ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))) / 1728,
        semi_b^2  =  ((alpha_s^2 - 4 alpha_s + 96) - sqrt(P(alpha_s))) / 1728.

(M6)  Eccentricity squared:
        e^2  =  2 sqrt(P(alpha_s)) / ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))).

(M7)  Marden foci (roots of p'(z) = 3z^2 - 2(1 + V_3)z + V_3):
        F_+/-  =  ((1 + V_3) +/- sqrt(V_3^2 - V_3 + 1)) / 3.

(M8)  Striking modulus identity:
        |V_3^2 - V_3 + 1|^2  =  P(alpha_s) / 9216
                              =  P(alpha_s) / (N_pair^4 N_quark)^2.

(M9)  Distance squared between Marden foci:
        |F_+ - F_-|^2  =  sqrt(P(alpha_s)) / 216
                       =  sqrt(P(alpha_s)) / N_quark^3.
```

where in all formulas

```text
P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  -  240 (4 - alpha_s)^2.
```

**The headline observation (M10):** the polynomial `P(alpha_s)`
**simultaneously controls THREE classical equilateral conditions** on
the retained NLO Wolfenstein protected-γ̄ surface:

1. `cot²(ω̄) − 3 = P(α_s)/[80(4 − α_s)²]` → Brocard equality
   `ω̄ = π/6` ⟺ `P(α_s) = 0`.
2. `(semi_a² − semi_b²)² = P(α_s)/746496` → Steiner inellipse circular
   ⟺ `P(α_s) = 0`.
3. `|F_+ − F_-|² = √P(α_s)/216` → Marden foci coincide ⟺ `P(α_s) = 0`.

`P(α_s) > 0` strictly on the physical α_s range, so the unitarity
triangle is uniformly bounded away from equilateral in **all three
equivalent senses simultaneously**. A single polynomial controls the
entire equilateral locus.

**Primary runner:**
`scripts/frontier_ckm_barred_steiner_inellipse_marden_closed_form.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface (where `tan(γ̄) = √5`
is α_s-protected, vertex `V_3 = (rho_bar, eta_bar) = ((4-α_s)/24, sqrt(5)(4-α_s)/24)`
is retained, and the centroid `G = ((28-α_s)/72, sqrt(5)(4-α_s)/72)` is
retained):

```text
(M1)  Steiner inellipse centre:  G  =  ((28 - alpha_s)/72,  sqrt(5)(4 - alpha_s)/72).

      LO recovery: G | LO = (7/18, sqrt(5)/18).

(M2)  Sum of semi-axes squared:
        S'  :=  semi_a^2 + semi_b^2  =  perim_sq / 18
            =  (alpha_s^2 - 4 alpha_s + 96) / 864
            =  (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)
               / (N_pair^5 N_color^3).

(M3)  Product of semi-axes squared:
        P'  :=  (semi_a * semi_b)^2  =  Area^2 / 27
            =  5 (4 - alpha_s)^2 / 62208
            =  (N_quark - 1) (N_pair^2 - alpha_s)^2 / (N_pair^8 N_color^5).

(M4)  Semi-axis quadratic discriminant:
        S'^2 - 4 P'  =  P(alpha_s) / 746496
                     =  P(alpha_s) / (N_pair^10 N_color^6),

      where  P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2
                            -  240 (4 - alpha_s)^2

                       =  alpha_s^4 - 8 alpha_s^3 - 32 alpha_s^2
                            + 1152 alpha_s + 5376.

(M5)  Individual semi-axes squared:
        semi_a^2  =  ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))) / 1728,
        semi_b^2  =  ((alpha_s^2 - 4 alpha_s + 96) - sqrt(P(alpha_s))) / 1728.

      LO numerical: semi_a^2 ≈ 0.0980, semi_b^2 ≈ 0.0131,
                    semi_a  ≈ 0.3131, semi_b  ≈ 0.1146.

(M6)  Eccentricity squared:
        e^2  =  (semi_a^2 - semi_b^2) / semi_a^2
             =  2 sqrt(P(alpha_s)) / ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))).

      LO: e^2 | LO  ≈  0.866   (eccentricity e ≈ 0.931 — highly stretched).

(M7)  Marden's theorem application:
        p(z)   =  z (z - 1) (z - V_3)  =  z^3 - (1 + V_3) z^2 + V_3 z,
        p'(z)  =  3 z^2 - 2(1 + V_3) z + V_3,
        F_+/-  =  ((1 + V_3) +/- sqrt(V_3^2 - V_3 + 1)) / 3.

      The two Marden foci are the **Steiner inellipse foci** (Marden's
      theorem; classical).

(M8)  Striking modulus identity:
        |V_3^2 - V_3 + 1|^2  =  P(alpha_s) / 9216
                              =  P(alpha_s) / (N_pair^4 N_quark)^2.

      So |V_3^2 - V_3 + 1| = sqrt(P(alpha_s))/96 — the SAME polynomial
      P(α_s) appears in the modulus of the discriminant of p'(z).

(M9)  Distance squared between Marden foci:
        |F_+ - F_-|^2  =  (4/9) |V_3^2 - V_3 + 1|
                       =  sqrt(P(alpha_s)) / 216
                       =  sqrt(P(alpha_s)) / N_quark^3.

(M10) UNIFICATION: P(alpha_s) governs THREE classical equilateral conditions:

      Condition (1) -- Brocard equality:
          cot^2(omega_bar) - 3  =  P(alpha_s) / [80 (4 - alpha_s)^2]
        => omega_bar = pi/6  iff  P(alpha_s) = 0.

      Condition (2) -- Steiner inellipse circular:
          (semi_a^2 - semi_b^2)^2  =  P(alpha_s) / 746496
        => semi_a = semi_b  iff  P(alpha_s) = 0.

      Condition (3) -- Marden foci coincide:
          |F_+ - F_-|^2  =  sqrt(P(alpha_s)) / 216
        => F_+ = F_-  iff  P(alpha_s) = 0.

      All THREE are equivalent on the retained surface, controlled by a
      SINGLE polynomial P(alpha_s). On the physical alpha_s range,
      P(alpha_s) > 0 strictly, so all three equilateral conditions are
      simultaneously avoided — and the unitarity triangle has a
      well-defined Steiner inellipse with distinct foci, a strictly
      acute Brocard angle, and distinct circumcenter / symmedian point.
```

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `rho_bar = (4 - alpha_s)/24`, `eta_bar = sqrt(5)(4 - alpha_s)/24` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = N_pair * N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |
| Centroid `G = ((28 - alpha_s)/72, sqrt(5)(4 - alpha_s)/72)` | [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note
is load-bearing. No unmerged branch is cited. No new
selector for `d`, `N_color`, or `N_pair` is asserted — all structural
integers are retained inputs and the closed forms are forced
consequences of those retained values combined with classical
triangle / inellipse geometry.

## Derivation

### Steiner inellipse: classical formulas

For any triangle with vertices `(V_1, V_2, V_3)`, the **Steiner
inellipse** is the unique ellipse inscribed in the triangle that is
tangent to each side at its midpoint. Its centre is the centroid `G`,
and its semi-axes `(semi_a, semi_b)` (with `semi_a ≥ semi_b`) satisfy

```text
semi_a^2 + semi_b^2  =  (a^2 + b^2 + c^2) / 18,        [classical]
semi_a * semi_b      =  Area_triangle / (3 sqrt(3)),    [classical]
```

where `(a, b, c)` are the triangle side lengths.

### M2, M3: symmetric functions of the semi-axes squared

For our barred triangle:

```text
perim_sq  =  a^2 + b^2 + c^2  =  (alpha_s^2 - 4 alpha_s + 96) / 48,
Area      =  eta_bar / 2      =  sqrt(5) (4 - alpha_s) / 48.
```

So

```text
S'  =  perim_sq / 18  =  (alpha_s^2 - 4 alpha_s + 96) / 864,
P'  =  Area^2 / 27    =  5 (4 - alpha_s)^2 / 62208.
```

In structural integers `(N_pair = 2, N_color = 3, N_quark = 6)`:
`864 = N_pair⁵ N_color³`, `62208 = N_pair⁸ N_color⁵`,
`96 = N_pair⁴ N_quark`, `5 = N_quark - 1`, `4 = N_pair²`. Both
recodings follow.

### M4: semi-axis quadratic discriminant equals P(α_s)/746496

The two semi-axes squared `(semi_a², semi_b²)` are the roots of

```text
X^2  -  S' X  +  P'  =  0.
```

Discriminant:

```text
S'^2 - 4 P'  =  ((alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2) / 746496
             =  P(alpha_s) / 746496.
```

Where `P(α_s) = (α_s² − 4α_s + 96)² − 240(4 − α_s)²` is the same
shape polynomial that is independently recovered below from the
classical Brocard formula. Its appearance here as the Steiner
inellipse semi-axis discriminant is the central new algebraic identity
of this note.

`746496 = 864² = N_pair^10 N_color^6` — a clean structural-integer
factorisation.

### M5, M6: individual semi-axes and eccentricity

```text
semi_a^2  =  (S' + sqrt(S'^2 - 4 P')) / 2
          =  ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))) / 1728,

semi_b^2  =  (S' - sqrt(S'^2 - 4 P')) / 2
          =  ((alpha_s^2 - 4 alpha_s + 96) - sqrt(P(alpha_s))) / 1728.

e^2  =  1 - semi_b^2 / semi_a^2  =  (semi_a^2 - semi_b^2) / semi_a^2

      =  (sqrt(P(alpha_s)) / 864) / (((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))) / 1728)

      =  2 sqrt(P(alpha_s)) / ((alpha_s^2 - 4 alpha_s + 96) + sqrt(P(alpha_s))).
```

`1728 = 12³ = N_pair⁶ N_color³`. The eccentricity `e^2 | LO ≈ 0.866`
(numerical) — the LO Steiner inellipse is highly stretched, reflecting
the strong asymmetry of the LO unitarity triangle.

### M7: Marden's theorem

**Marden's theorem** (classical): for a complex polynomial
`p(z) = (z − r_1)(z − r_2)(z − r_3)` of degree 3, the **foci of the
Steiner inellipse** of the triangle with vertices `(r_1, r_2, r_3)`
are exactly the two **roots of p'(z)**.

Applying to our triangle with `V_1 = 0, V_2 = 1, V_3 = rho_bar + i eta_bar`:

```text
p(z)   =  z (z - 1) (z - V_3)  =  z^3 - (1 + V_3) z^2 + V_3 z,
p'(z)  =  3 z^2 - 2 (1 + V_3) z + V_3.
```

Solving the quadratic:

```text
F_+/-  =  [2(1 + V_3) +/- sqrt(4(1 + V_3)^2 - 12 V_3)] / 6
        =  ((1 + V_3) +/- sqrt(V_3^2 - V_3 + 1)) / 3,
```

with the discriminant

```text
(1 + V_3)^2 - 3 V_3  =  1 + 2 V_3 + V_3^2 - 3 V_3  =  V_3^2 - V_3 + 1.
```

### M8: striking modulus identity

Computing real and imaginary parts of `V_3^2 − V_3 + 1` on the
protected-γ̄ surface (where `eta_bar = sqrt(5) rho_bar`, so
`eta_bar² = 5 rho_bar²`):

```text
Re(V_3^2 - V_3 + 1)  =  rho_bar^2 - eta_bar^2 - rho_bar + 1
                     =  -4 rho_bar^2 - rho_bar + 1
                     =  (104 + 14 alpha_s - alpha_s^2) / 144,

Im(V_3^2 - V_3 + 1)  =  2 rho_bar eta_bar - eta_bar  =  eta_bar (2 rho_bar - 1)
                     =  -sqrt(5) (4 - alpha_s)(8 + alpha_s) / 288
                     =  -sqrt(5) (32 - 4 alpha_s - alpha_s^2) / 288.
```

Squaring and summing:

```text
|V_3^2 - V_3 + 1|^2
   =  (104 + 14 alpha_s - alpha_s^2)^2 / 20736
       +  5 (32 - 4 alpha_s - alpha_s^2)^2 / 82944.

Common denominator 82944 (= 288^2):
   =  [4 (104 + 14 alpha_s - alpha_s^2)^2 + 5 (32 - 4 alpha_s - alpha_s^2)^2] / 82944

Expanding the numerator:
   4 (104 + 14 alpha_s - alpha_s^2)^2  =  4 alpha_s^4 - 112 alpha_s^3 - 48 alpha_s^2
                                            + 11648 alpha_s + 43264,
   5 (32 - 4 alpha_s - alpha_s^2)^2    =  5 alpha_s^4 + 40 alpha_s^3 - 240 alpha_s^2
                                            - 1280 alpha_s + 5120.

Sum  =  9 alpha_s^4 - 72 alpha_s^3 - 288 alpha_s^2 + 10368 alpha_s + 48384
     =  9 (alpha_s^4 - 8 alpha_s^3 - 32 alpha_s^2 + 1152 alpha_s + 5376)
     =  9 P(alpha_s).
```

So `|V_3² − V_3 + 1|² = 9 P(α_s)/82944 = P(α_s)/9216 = P(α_s)/(96)² =
P(α_s)/(N_pair⁴ N_quark)²`. Striking: the polynomial `P(α_s)` —
originally the discriminant of the semi-axis quadratic — is also
exactly `(N_pair⁴ N_quark)²` times the modulus squared of the
discriminant of `p'(z)`. **Two distinct algebraic objects collapse
onto the same polynomial.**

### M9: distance squared between Marden foci

```text
F_+ - F_-  =  (2/3) sqrt(V_3^2 - V_3 + 1)
|F_+ - F_-|^2  =  (4/9) |V_3^2 - V_3 + 1|
              =  (4/9) sqrt(P(alpha_s)) / 96
              =  sqrt(P(alpha_s)) / 216
              =  sqrt(P(alpha_s)) / N_quark^3.
```

`216 = 6³ = N_quark³` — striking structural-integer denominator.

### M10: P(α_s) unifies three classical equilateral conditions

**Condition (1) — Brocard equality.** With
`cot(omega_bar) = perim_sq/(4 Area) = (alpha_s^2 - 4 alpha_s + 96)/[4 sqrt(5)(4 - alpha_s)]`:

```text
cot^2(omega_bar)  =  (alpha_s^2 - 4 alpha_s + 96)^2 / (80 (4 - alpha_s)^2),
cot^2(omega_bar) - 3  =  ((alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2)
                          / (80 (4 - alpha_s)^2)
                       =  P(alpha_s) / [80 (4 - alpha_s)^2].
```

So `omega_bar = pi/6` ⟺ `cot(omega_bar) = sqrt(3)` ⟺ `P(α_s) = 0`.

**Condition (2) — Steiner inellipse circular.** From M4,
`(semi_a² − semi_b²)² = P(α_s)/746496`. So `semi_a = semi_b` ⟺
`P(α_s) = 0`.

**Condition (3) — Marden foci coincide.** From M9,
`|F_+ − F_-|² = √P(α_s)/216`. So `F_+ = F_-` ⟺ `P(α_s) = 0`.

All three classical equilateral conditions are **algebraically
equivalent** on the retained NLO Wolfenstein protected-γ̄ surface.
Numerical sweep confirms `P(α_s) > 0` strictly across `α_s ∈ [0, 3.9]`
(the physical range plus headroom).

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| M1 G_x | `(28-α_s)/72` | sympy `simplify(diff) == 0` |
| M1 G_y | `√5(4-α_s)/72` | sympy `simplify(diff) == 0` |
| M1 LO | `(7/18, √5/18)` | exact rational |
| M2 S' | `(α_s²-4α_s+96)/864` | sympy `simplify(diff) == 0` |
| M3 P' | `5(4-α_s)²/62208` | sympy `simplify(diff) == 0` |
| M4 discr | `P(α_s)/746496` | sympy `simplify(diff) == 0` |
| M4 struct | `746496 = N_pair^10 N_color^6` | exact integer |
| M5 semi_a² | `((α_s²-4α_s+96)+√P)/1728` | sympy `simplify(diff) == 0` |
| M5 semi_b² | `((α_s²-4α_s+96)-√P)/1728` | sympy `simplify(diff) == 0` |
| M6 e² | `2√P/((α_s²-4α_s+96)+√P)` | sympy `simplify(diff) == 0` |
| M6 LO | e² ≈ 0.866 | numerical |
| M7 Marden foci | sympy `solve(p'(z), z)` matches `((1+V_3)±√(V_3²-V_3+1))/3` | sympy match |
| M8 modulus | `\|V_3²-V_3+1\|² = P/9216` | sympy `simplify(diff) == 0` |
| M9 foci dist | `\|F_+-F_-\|² = √P/216` | sympy `simplify(diff) == 0` |
| M10(1) Brocard | `cot²(ω̄)-3 = P/[80(4-α_s)²]` | sympy `simplify(diff) == 0` |
| M10(2) Steiner | `(semi_a²-semi_b²)² = P/746496` | sympy `simplify(diff) == 0` |
| M10(3) Marden | `\|F_+-F_-\|² = √P/216` (M9 again) | sympy `simplify(diff) == 0` |
| M10 sweep | `P(α_s) > 0` on `[0, 3.9]` | numerical sweep PASS |

Numerical readout at canonical α_s sample points:

| `α_s(v)` | `P(α_s)` | `e (Steiner)` | `\|F_+−F_-\|²` |
| ---: | ---: | ---: | ---: |
| 0 (LO) | 5376.0 | 0.9305 | 0.3394 |
| 0.10330 (canonical `alpha_s(v)`) | 5494.7 | 0.9346 | 0.34318 |
| 0.30 | 5718.5 | 0.9418 | 0.35010 |

`P(α_s)` increases mildly with α_s; the Steiner inellipse becomes
slightly more eccentric and the Marden foci move slightly farther
apart. All quantities stay well-behaved across the physical range.

## Science Value

### What this lets the framework state cleanly

Previously the framework had retained closed forms for the
**centroid**, **circumradius/circumcenter**, **orthocenter / Euler line**,
the **apex angle** `α̃`, the **Jarlskog** `J̄`, and the
**right-angle / Pythagorean** structure of the barred unitarity
triangle. The **Steiner inellipse** (an internal geometric structure
of the triangle) and the **Marden foci** (the algebraic-geometric
bridge between the cubic `p(z) = (z − V_1)(z − V_2)(z − V_3)` and the
Steiner inellipse) had not been derived in closed form.

This note delivers:

1. **NEW Steiner-inellipse semi-axis closed forms** (M5):
   `semi_a²` and `semi_b²` as compact rational-function-plus-radical
   expressions in `α_s`, with the radical being the common shape
   polynomial `P(α_s)`.

2. **NEW eccentricity closed form** (M6):
   `e² = 2√P/[(α_s²-4α_s+96) + √P]`. At LO, `e² ≈ 0.866` — the LO
   Steiner inellipse is highly stretched.

3. **NEW Marden foci closed form** (M7): the two foci of the Steiner
   inellipse, expressed via the discriminant `V_3² − V_3 + 1` of the
   derivative of the vertex polynomial.

4. **NEW striking modulus identity** (M8): `|V_3² − V_3 + 1|² =
   P(α_s)/(N_pair⁴ N_quark)²`. The polynomial that arose as the
   semi-axis discriminant ALSO arises as the squared modulus of the
   discriminant of `p'(z)` — two algebraically distinct objects
   collapse onto the same polynomial.

5. **NEW foci-distance closed form** (M9):
   `|F_+ − F_-|² = √P(α_s)/N_quark³`. Pure structural-integer
   denominator.

6. **NEW unification observation** (M10): `P(α_s) = 0` simultaneously
   characterises **three classical equilateral conditions**:
   - Brocard equality `ω̄ = π/6`
   - Steiner inellipse circular
   - Marden foci coincide

   On the retained NLO Wolfenstein protected-γ̄ surface, `P(α_s) > 0`
   strictly. So all three equilateral conditions are simultaneously
   avoided, and a single polynomial `P(α_s)` controls the entire
   "non-equilateral" structure.

### Why this counts as pushing the science forward

Marden's theorem is a deep classical result connecting the algebra of
cubic polynomials to the geometry of triangles via the Steiner
inellipse. Applying it to the unitarity triangle gives a NEW kind of
invariant: the **two Marden foci** are interior points of the
triangle that play a role analogous to the foci of the inscribed
ellipse — they encode the "shape" of the triangle algebraically.

The unification observation (M10) is the highest-leverage piece. The
shape polynomial `P(α_s)` appears here as the semi-axis discriminant of
the Steiner inellipse, as the squared modulus of the discriminant of
`p'(z)`, and as the self-contained Brocard-bound polynomial obtained
from `cot(omega_bar)=perim_sq/(4 Area)`. This is deeper than the mere
equality of polynomials: it shows that the "non-equilateralness" of
the unitarity triangle has multiple algebraically-distinct
manifestations that all collapse onto the SAME polynomial.

In CKM physics, the polynomial `P(α_s)` is therefore a
fundamental shape-invariant of the protected-γ̄ surface. Any
modification of the framework that preserves the retained inputs
(`rho_bar`, `eta_bar`, structural integers) preserves `P(α_s)`, and
therefore preserves all three equilateral conditions simultaneously.
This is structural rigidity at the algebraic level.

### Falsifiable structural claim

The closure (M1–M10) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
  + retained centroid closed form
forces
  semi_a^2, semi_b^2  =  ((α_s^2 - 4 α_s + 96) ± sqrt(P(α_s))) / 1728,
  |F_+ - F_-|^2       =  sqrt(P(α_s)) / N_quark^3,
  |V_3^2 - V_3 + 1|^2 =  P(α_s) / (N_pair^4 N_quark)^2.
```

Any framework revision moving `(rho_bar, eta_bar)` off the retained
protected-γ̄ surface, or shifting any of the structural integers,
would break the M5/M8/M9 closed forms simultaneously. The M10
unification is structurally rigid: the **single polynomial** `P(α_s)`
controlling all three equilateral conditions cannot be perturbed
without breaking each closed form independently.

## What This Claims

- `(M1)`: NEW retained verification that the Steiner inellipse centre
  is the retained centroid `G`.
- `(M2, M3)`: NEW retained closed forms for the symmetric functions
  `S' = perim²/18` and `P' = Area²/27` of the Steiner inellipse
  semi-axes squared.
- `(M4)`: NEW retained closed form `S'² − 4P' = P(α_s)/746496` —
  the common shape polynomial appears as the semi-axis discriminant.
- `(M5, M6)`: NEW retained closed forms for the individual
  semi-axes squared and the eccentricity squared, in terms of
  `√P(α_s)`.
- `(M7)`: NEW retained closed form for the Marden foci via Marden's
  theorem applied to `p(z) = z(z-1)(z-V_3)`.
- `(M8)`: NEW striking algebraic identity
  `|V_3² − V_3 + 1|² = P(α_s)/(N_pair⁴ N_quark)²`.
- `(M9)`: NEW retained closed form
  `|F_+ − F_-|² = √P(α_s)/N_quark³`.
- `(M10)`: NEW unification observation that the shape polynomial
  `P(α_s)` simultaneously controls THREE classical equilateral
  conditions on the retained surface.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches; the polynomial `P(α_s)` is
  recomputed here from retained inputs and
  `cot(omega_bar) = perim_sq/(4 Area)`.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs.
- Does **not** depend on any α_s-running pipeline; all results live
  on the protected-γ̄ surface at canonical `α_s(v)`.
- Does **not** make a direct CKM-observable claim about the Steiner
  inellipse or Marden foci; these are derived geometric structures
  of the unitarity triangle.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_steiner_inellipse_marden_closed_form.py
```

Expected:

```text
TOTAL: PASS=34, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs (`rho_bar`, `eta_bar`,
  `N_pair`, `N_color`, `N_quark`, centroid).
- Computes M1–M10 symbolically via sympy at the retained values and
  asserts each closed form by `simplify(diff) == 0`.
- Verifies Marden's theorem by solving `p'(z) = 0` symbolically and
  matching against the closed-form expression.
- Confirms the M10 unification: `P(α_s)` is the simultaneous polynomial
  governing the Brocard inequality, semi-axis discriminant, and
  Marden foci coincidence.
- Sweeps `α_s` to numerically certify `P(α_s) > 0` strictly across
  the physical range.
- Reports a numerical readout at canonical α_s sample points.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.
- [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — centroid `G` closed form.

**Companion barred-triangle closed forms (cited for context, not
load-bearing here):**

- [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — circumradius `R̄`.
- [`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — apex angle `α̃`.
- [`CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md)
  — Pythagorean structure.
- [`CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — Jarlskog `J̄`.

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch; the shape polynomial `P(α_s)` is independently
  derived here from retained inputs.
- Any candidates-tier theorem.
