# Barred Unitarity-Triangle Symmedian Point + Brocard Circle: EXACT Closed Form Theorem

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives the
**EXACT closed forms** for the **Symmedian (Lemoine) point `K`**, the
**circumcenter–symmedian distance `OK`**, the **Brocard axis slope at LO**,
and the **Brocard circle** (centre and radius) of the barred unitarity
triangle.

The headline closed forms:

```text
(K1)  K_x  =  (4 - alpha_s)(8 - alpha_s)
              /  [2 (alpha_s^2 - 4 alpha_s + 96)]
            =  (N_pair^2 - alpha_s)(N_pair^3 - alpha_s)
              /  [N_pair (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)].

(K2)  K_y  =  2 sqrt(5) (4 - alpha_s)
              /  (alpha_s^2 - 4 alpha_s + 96)
            =  N_pair sqrt(N_quark - 1) (N_pair^2 - alpha_s)
              /  (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark).

(K6)  OK^2 =  (80 + alpha_s^2) * P(alpha_s)
              /  [320 (alpha_s^2 - 4 alpha_s + 96)^2]

      where  P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  -  240 (4 - alpha_s)^2

(K7)  OK^2 | LO  =  (N_quark + 1) / (N_pair^4 N_color)  =  7/48.

(K8)  slope_{OK} | LO  =  -sqrt(N_quark - 1) / N_pair^2  =  -sqrt(5)/4.
```

**Two striking discoveries:**

1. **LO recovery `K | LO = (rho | LO, eta | LO / 2)` (K3, K4):** at LO the
   apex of the unitarity triangle is the right angle (retained
   `α_LO = π/2`), and a classical right-triangle property forces the
   symmedian from the right-angle vertex to land at exactly `V_3 / 2`
   in the y-direction — so `K | LO` lies directly below the apex at
   half the height. This is the same structural integer ratio
   `1/N_pair = 1/2` that appears throughout the framework.

2. **The polynomial `P(alpha_s)` governs both the Brocard inequality
   AND the Brocard circle radius (K10).** This is a NEW deep
   observation: `P(alpha_s) > 0` is exactly the condition for
   `omega_bar < pi/6` (strict Brocard inequality), AND `P(alpha_s) > 0`
   is exactly the condition for `OK > 0` (i.e. circumcenter and
   symmedian are distinct). The equilateral limit `omega_bar = pi/6`
   is the SAME locus as `OK = 0` (i.e. `P = 0`), tying together two
   classical triangle invariants on a single algebraic surface.

**Primary runner:**
`scripts/frontier_ckm_barred_symmedian_brocard_circle_closed_form.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface (where
`tan(γ̄) = √5` is α_s-protected; `tan(β̄)` and apex coordinates
`(rho_bar, eta_bar) = ((4-α_s)/24, sqrt(5)(4-α_s)/24)` are retained
closed forms; circumcenter `O = (1/2, -alpha_s sqrt(5)/40)` and
`R̄^2 = 1/4 + alpha_s^2/320` are retained):

```text
(K1)  Symmedian (Lemoine) point K, x-coordinate:
        K_x  =  (4 - alpha_s)(8 - alpha_s)
                / [2 (alpha_s^2 - 4 alpha_s + 96)].

      In structural integers (N_pair = 2, N_color = 3, N_quark = 6):
        K_x  =  (N_pair^2 - alpha_s)(N_pair^3 - alpha_s)
                / [N_pair (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)].

(K2)  Symmedian point K, y-coordinate:
        K_y  =  2 sqrt(5) (4 - alpha_s) / (alpha_s^2 - 4 alpha_s + 96)
             =  N_pair sqrt(N_quark - 1) (N_pair^2 - alpha_s)
                / (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark).

(K3)  LO recovery:
        K | LO  =  ( 1/N_quark, sqrt(N_quark - 1) / (2 N_quark) )
                =  ( rho | LO, eta | LO / 2 )
                =  ( 1/6, sqrt(5)/12 ).

      The symmedian's x-coordinate at LO equals the apex's x-coordinate;
      its y-coordinate is exactly HALF the apex's y-coordinate.

(K4)  Right-triangle property at LO:
        K_y / V_3_y | LO  =  1/N_pair  =  1/2.

      (At LO the apex is the right-angle vertex of the unitarity
      triangle [retained alpha_LO = pi/2]. For any right triangle, the
      symmedian from the right-angle vertex meets the opposite side at
      its foot of altitude, so K lies on the vertical through the
      foot — half-way to the apex.)

(K5)  Ratio K_y / eta_bar:
        K_y / eta_bar  =  N_pair^3 N_quark
                           / (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark).

      LO: K_y / eta_bar | LO = N_pair^3 N_quark / (N_pair^4 N_quark) = 1/N_pair = 1/2.

(K6)  Circumcenter-Symmedian distance squared:
        OK^2  =  (80 + alpha_s^2) * P(alpha_s)
                  / [320 (alpha_s^2 - 4 alpha_s + 96)^2]

      where  P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2
                          =  alpha_s^4 - 8 alpha_s^3 - 32 alpha_s^2 + 1152 alpha_s + 5376.

      Equivalent form (any-triangle identity):
        OK^2  =  R_bar^2 * (1  -  48 * Area^2 / perim_sq^2)
              =  R_bar^2 * P(alpha_s) / (alpha_s^2 - 4 alpha_s + 96)^2.

(K7)  LO value:
        OK^2 | LO  =  (N_quark + 1) / (N_pair^4 N_color)  =  7/48.

(K8)  Brocard axis (line OK from circumcenter to symmedian) slope at LO:
        slope_{OK} | LO  =  -sqrt(N_quark - 1) / N_pair^2  =  -sqrt(5)/4.

      Pure structural-integer ratio at LO.

(K9)  Brocard circle:
        center M  =  (O + K) / 2,
        radius^2  =  OK^2 / 4.

      The Brocard circle passes through O, K, and both Brocard points
      (the two interior cevian-intersection points generating the
      Brocard angle omega_bar). At LO:
        radius_Brocard^2 | LO  =  (N_quark + 1) / (4 N_pair^4 N_color)  =  7/192.

(K10) P(alpha_s) governs BOTH the Brocard inequality AND OK^2:
        P(alpha_s) >= 0   <=>   cot(omega_bar) >= sqrt(3)   <=>   omega_bar <= pi/6,
        P(alpha_s) >= 0   <=>   OK^2 >= 0   <=>   Brocard circle exists.

      The equilateral limit P(alpha_s) = 0 is the SAME locus as the
      Brocard-circle collapse limit. On the protected-γ̄ surface
      P(alpha_s) is strictly positive for all physical alpha_s; both
      limits are unattained.
```

## Retained Inputs

Each authority is a retained-tier note on `main`. The runner extracts
the verbatim `Status:` line from each file and verifies the tier label.

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `rho_bar = (4 - alpha_s)/24`, `eta_bar = sqrt(5)(4 - alpha_s)/24` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = N_pair * N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |
| `R_bar^2 = 1/4 + alpha_s^2/320`, circumcenter `O = (1/2, -alpha_s sqrt(5)/40)` | [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md) | retained |
| `alpha_LO = pi/2` (right-angle property of LO triangle) | [`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note
is load-bearing. No unmerged branch is cited. No new selector is
asserted — all structural integers are retained inputs and the closed
forms are forced consequences of those retained values combined with
classical triangle geometry.

## Derivation

### Vertex layout and side lengths

In the barred `(rho_bar, eta_bar)` plane:

```text
V_1 = (0, 0),
V_2 = (1, 0),
V_3 = (rho_bar, eta_bar) = ( (4 - alpha_s)/24, sqrt(5)(4 - alpha_s)/24 ).
```

Side-length squares (with sides labeled by the OPPOSITE vertex):

```text
a^2 = |V_2 V_3|^2 = (1 - rho_bar)^2 + eta_bar^2 = (80 + alpha_s^2)/96,
b^2 = |V_1 V_3|^2 = rho_bar^2 + eta_bar^2       = (4 - alpha_s)^2/96,
c^2 = |V_1 V_2|^2 = 1.
```

### K1, K2: symmedian point closed form

The Lemoine (symmedian) point has barycentric coordinates `(a², b², c²)`:

```text
K  =  (a^2 V_1 + b^2 V_2 + c^2 V_3) / (a^2 + b^2 + c^2).
```

With `a²+b²+c² = (alpha_s^2 - 4 alpha_s + 96)/48` (perimeter squared
on the protected-γ̄ surface) and `c² = 1`:

```text
K_x  =  (b^2 + rho_bar) / perim_sq
     =  ((4 - alpha_s)^2/96  +  (4 - alpha_s)/24) / ((alpha_s^2 - 4 alpha_s + 96)/48)
     =  ((4 - alpha_s)((4 - alpha_s) + 4)/96) / ((alpha_s^2 - 4 alpha_s + 96)/48)
     =  (4 - alpha_s)(8 - alpha_s) / [2 (alpha_s^2 - 4 alpha_s + 96)],

K_y  =  eta_bar / perim_sq
     =  (sqrt(5) (4 - alpha_s)/24) / ((alpha_s^2 - 4 alpha_s + 96)/48)
     =  2 sqrt(5)(4 - alpha_s) / (alpha_s^2 - 4 alpha_s + 96).
```

In structural integers `(N_pair = 2, N_color = 3, N_quark = 6)`:
`4 = N_pair²`, `8 = N_pair³`, `2 = N_pair`,
`96 = N_pair^4 N_quark`, `sqrt(5) = sqrt(N_quark - 1)`, and the
denominator polynomial is `α_s² - N_pair² α_s + N_pair⁴ N_quark`. Both
numerator factorizations follow.

### K3, K4: LO recovery and right-triangle property

At `alpha_s = 0`:

```text
K_x | LO  =  4 * 8 / (2 * 96)  =  1/6  =  1/N_quark  =  rho | LO,
K_y | LO  =  2 sqrt(5) * 4 / 96  =  sqrt(5)/12  =  eta | LO / 2.
```

So `K | LO` lies directly below the apex `V_3 | LO = (1/6, √5/6)` at
exactly half the height. The structural-integer ratio
`K_y / V_3_y | LO = 1/N_pair = 1/2` is forced because:

- At LO the apex angle is `α_LO = π/2` (retained right-angle theorem).
- For any right triangle with the right angle at vertex `C`, the
  symmedian from `C` lies on the altitude from `C` — i.e. perpendicular
  to the hypotenuse. The symmedian point `K` lies at the foot of the
  altitude in the x-direction and at `V_C_y / 2` in the y-direction
  (because `c² = a² + b²` collapses the barycentric weight sum to
  `2c²` for a right triangle, giving the y-coordinate
  `c² * V_C_y / (2 c²) = V_C_y / 2`).

### K5: ratio K_y / eta_bar

Direct division:

```text
K_y / eta_bar  =  [2 sqrt(5)(4 - alpha_s) / (alpha_s^2 - 4 alpha_s + 96)]
                  / [sqrt(5)(4 - alpha_s)/24]
              =  48 / (alpha_s^2 - 4 alpha_s + 96)
              =  N_pair^3 N_quark / (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)
```

with `48 = N_pair^3 × N_quark = 8 × 6`. At LO this reduces to
`N_pair^3 N_quark / (N_pair^4 N_quark) = 1/N_pair = 1/2` (K4).

### K6: OK² closed form via the Brocard polynomial P(α_s)

Standard identity (any triangle):

```text
OK^2  =  R^2 - 3 a^2 b^2 c^2 / (a^2 + b^2 + c^2)^2.
```

Using `abc = 4 Delta R` (with `Delta` the triangle area), this rewrites as

```text
OK^2  =  R^2 - 3 (4 Delta R)^2 / perim_sq^2
      =  R^2 (1 - 48 Delta^2 / perim_sq^2).
```

For our triangle:

```text
48 Delta^2 / perim_sq^2  =  48 * (eta_bar / 2)^2 / [(alpha_s^2 - 4 alpha_s + 96)/48]^2
                          =  240 (4 - alpha_s)^2 / (alpha_s^2 - 4 alpha_s + 96)^2.
```

Therefore

```text
OK^2  =  (1/4 + alpha_s^2 / 320) *
         [(alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2]
            / (alpha_s^2 - 4 alpha_s + 96)^2

      =  (80 + alpha_s^2) * P(alpha_s)
            / [320 (alpha_s^2 - 4 alpha_s + 96)^2]

with  P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2
                  =  alpha_s^4 - 8 alpha_s^3 - 32 alpha_s^2 + 1152 alpha_s + 5376.
```

This is the central NEW closed form: `OK^2` factors as
`R̄² × P(alpha_s) / perim_sq²`, with the polynomial `P(alpha_s)` to be
recognised in the next sub-section.

### K7: OK² at LO

At `alpha_s = 0`:

```text
P(0)              =  96^2 - 240 * 16  =  9216 - 3840  =  5376,
(80 + 0)          =  80,
(0 - 0 + 96)^2    =  9216,
OK^2 | LO         =  80 * 5376 / (320 * 9216)
                  =  21/144  =  7/48.
```

In structural integers:

```text
OK^2 | LO  =  (N_quark + 1) / (N_pair^4 N_color),

since N_quark + 1 = 7 and N_pair^4 N_color = 16 * 3 = 48.
```

### K8: Brocard axis slope at LO

```text
delta_x  =  K_x - O_x  =  (4 - alpha_s)(8 - alpha_s) / [2 (α_s² − 4α_s + 96)]  -  1/2
                       =  -4 (alpha_s + 8) / (alpha_s^2 - 4 alpha_s + 96),

delta_y  =  K_y - O_y  =  sqrt(5) [alpha_s^3 - 4 alpha_s^2 + 16 alpha_s + 320]
                          / [40 (alpha_s^2 - 4 alpha_s + 96)].
```

At `alpha_s = 0`:

```text
delta_x | LO  =  -32 / 96  =  -1/3,
delta_y | LO  =  sqrt(5) * 320 / [40 * 96]  =  sqrt(5)/12,
slope_{OK} | LO  =  delta_y / delta_x  =  (sqrt(5)/12) / (-1/3)
                 =  -sqrt(5)/4
                 =  -sqrt(N_quark - 1) / N_pair^2.
```

### K9: Brocard circle

The Brocard circle of any triangle passes through:

- The circumcenter `O`,
- The Lemoine (symmedian) point `K`,
- Both Brocard points `Ω₁`, `Ω₂` (the unique interior cevian-intersection
  points generating the Brocard angle `ω`).

Its centre is the midpoint of `OK`, and its radius is `OK/2`. For our
triangle:

```text
center M  =  (O + K) / 2,
radius_B^2  =  OK^2 / 4
            =  (80 + alpha_s^2) * P(alpha_s) / [1280 (alpha_s^2 - 4 alpha_s + 96)^2].

At LO:
  radius_B^2 | LO  =  7/192  =  (N_quark + 1) / (4 N_pair^4 N_color).
```

The runner verifies `|M - O|² = |M - K|² = radius_B²` symbolically.

### K10: P(α_s) — one polynomial, two classical bounds

**Brocard inequality** (any triangle): `cot(ω) ≥ √3`, i.e.
`ω ≤ π/6`, with equality iff equilateral. On the retained surface
the classical identity `cot(omega) = perim_sq / (4 Delta)` gives

```text
cot(omega_bar)^2 - 3
  =  [(alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2]
     / [80 (4 - alpha_s)^2]
  =  P(alpha_s) / [80 (4 - alpha_s)^2].
```

Thus the Brocard inequality reduces on this surface to
`P(alpha_s) >= 0`.

**Brocard circle existence** (any triangle): `OK² ≥ 0`, with equality
iff `O = K`, which happens iff the triangle is equilateral. On the
retained surface this also reduces to `P(alpha_s) ≥ 0` (the
`(80 + alpha_s^2)` and `320 (...)²` factors are strictly positive on
the physical range).

So on the protected-γ̄ surface, the **same polynomial `P(alpha_s)`
controls both classical bounds**: `P > 0` is equivalent to "the
triangle is non-equilateral", and the Brocard circle has positive
radius exactly when the Brocard inequality is strict. The equilateral
locus `P = 0` is the simultaneous limit
`omega_bar = pi/6 ⇔ OK = 0 ⇔ Brocard circle collapses to a point`.

Numerically, `P(α_s) > 0` on the entire physical α_s range (the
polynomial has no real roots in the physical range), so the unitarity
triangle is uniformly bounded away from the equilateral limit.

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| K1 K_x | `(4-α_s)(8-α_s)/[2(α_s² - 4α_s + 96)]` | sympy `simplify(diff) == 0` |
| K1 structural | `(N_pair²-α_s)(N_pair³-α_s)/[N_pair (...)]` | sympy `simplify(diff) == 0` |
| K2 K_y | `2√5(4-α_s)/(α_s² - 4α_s + 96)` | sympy `simplify(diff) == 0` |
| K2 structural | `N_pair √(N_quark-1)(N_pair²-α_s)/(...)` | sympy `simplify(diff) == 0` |
| K3 LO K_x | `1/N_quark = 1/6` | sympy `simplify(diff) == 0` |
| K3 LO K_y | `√(N_quark-1)/(2 N_quark) = √5/12` | sympy `simplify(diff) == 0` |
| K4 ratio | `K_y/V_3_y \| LO = 1/N_pair = 1/2` | sympy `simplify(diff) == 0` |
| K5 ratio | `N_pair³ N_quark / (...)` | sympy `simplify(diff) == 0` |
| K5 LO | `1/N_pair = 1/2` | exact rational |
| K6 OK² | `(80+α_s²) P(α_s)/[320 (...)²]` | sympy `simplify(diff) == 0` |
| K6 alt | `R̄² (1 - 48 Area²/perim⁴)` | sympy `simplify(diff) == 0` |
| K7 LO OK² | `(N_quark+1)/(N_pair⁴ N_color) = 7/48` | sympy `simplify(diff) == 0` |
| K8 slope LO | `-√(N_quark-1)/N_pair² = -√5/4` | sympy `simplify(diff) == 0` |
| K9 Brocard center | `M = (O+K)/2`, `\|M-O\|² = \|M-K\|² = OK²/4` | sympy `simplify(diff) == 0` |
| K9 LO Brocard r² | `(N_quark+1)/(4 N_pair⁴ N_color) = 7/192` | sympy `simplify(diff) == 0` |
| K10 P sweep | `OK² > 0` and `P(α_s) > 0` on physical α_s | numerical sweep PASS |

Numerical readout at canonical α_s sample points:

| `α_s(v)` | `K = (K_x, K_y)` | `O = (O_x, O_y)` | `OK` |
| ---: | ---: | ---: | ---: |
| 0 (LO) | (0.16667, 0.18634) | (0.50000, 0.00000) | 0.38188 |
| 0.10330 (canonical `alpha_s(v)`) | (0.16094, 0.18229) | (0.50000, -0.00577) | 0.38772 |
| 0.30 | (0.15012, 0.17438) | (0.50000, -0.01677) | 0.39869 |

The symmedian point sits well inside the triangle and `OK` varies
slowly across the α_s range.

## Science Value

### What this lets the framework state cleanly

Previously the framework had retained closed forms for the
**circumradius** `R̄` and **circumcenter** `O`, the **orthocenter**
`H` and **Euler line**, the **centroid** `G`, the **apex angle** `α̃`,
the **Brocard-angle bound** through the classical
`cot(omega)=perim_sq/(4 Delta)` identity, and the **Jarlskog** `J̄`.
The **symmedian (Lemoine) point** `K` and the
**Brocard circle** were not previously expressed in closed form.

This note delivers:

1. **NEW symmedian point `K` closed form** (K1, K2): a compact rational
   function of `α_s(v)` for both coordinates, with structural-integer
   recoding in `(N_pair, N_color, N_quark)`.

2. **NEW LO identity `K | LO = (rho | LO, eta | LO / 2)`** (K3): the
   symmedian point at LO is the midpoint between the apex `V_3 | LO` and
   its projection onto the hypotenuse. The y-coordinate ratio `1/N_pair`
   is forced by the right-angle property `α_LO = π/2`.

3. **NEW Brocard axis slope at LO** (K8):
   `slope_OK | LO = −√(N_quark − 1)/N_pair² = −√5/4`. Pure
   structural-integer ratio.

4. **NEW circumcenter-Lemoine distance closed form** (K6): `OK²` factors
   as `R̄² × P(α_s) / perim_sq²`, where `P(α_s)` is the same polynomial
   that governs the Brocard inequality.

5. **NEW Brocard circle closed form** (K9): center `M = (O+K)/2`,
   radius² = `OK²/4`. The Brocard circle is the natural geometric
   container for the Brocard angle (it passes through both Brocard
   points and the symmedian point).

6. **NEW deep observation: P(α_s) governs both Brocard bounds (K10).**
   The polynomial `P(α_s) = (α_s² − 4α_s + 96)² − 240(4 − α_s)²`
   simultaneously controls:
    - the Brocard inequality `cot(ω̄) ≥ √3` via
      `cot(omega)=perim_sq/(4 Delta)`,
    - the existence of the Brocard circle (`OK² ≥ 0`).
   The equilateral limit `ω̄ = π/6` is the SAME locus as `OK = 0`
   (Brocard circle collapse). On the retained surface `P(α_s) > 0`
   strictly, so both inequalities are strict — the unitarity triangle
   is uniformly bounded away from the equilateral limit, and the
   Brocard circle is uniformly non-degenerate.

### Why this counts as pushing the science forward

The Lemoine (symmedian) point `K` is the **isogonal conjugate of the
centroid** `G`: while `G` minimises sums of squared distances to the
sides, `K` maximises sums of squared distances to the sides. Both are
classical CP-symmetric (vertex-permutation) constructions on the
unitarity triangle. With the Brocard circle, the framework now has:

- The four classical triangle "centers" (`G`, `O`, `H`, `K`) all in
  retained closed form on the protected-γ̄ surface.
- The **Brocard axis** (line `OK`) — which contains both Brocard
  points and is the natural axis of the triangle's "shape symmetry".
- The **Brocard circle** — the natural circle through `O`, `K`, both
  Brocard points.

The K10 observation is the highest-leverage piece: a single polynomial
`P(α_s)` controls both the Brocard angle bound and the Brocard circle
radius. This **algebraically unifies two classical triangle inequalities
on the retained CKM surface**.

### Falsifiable structural claim

The closure (K1–K10) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
  + retained CKM_BARRED_CIRCUMRADIUS (R̄², circumcenter)
forces
  K | LO  =  (rho | LO, eta | LO / 2)   AND
  OK^2 | LO  =  (N_quark + 1) / (N_pair^4 N_color)  =  7/48.
```

Any framework revision moving the apex coordinate or the bare structural
integers would break the K3/K7 LO recoveries. The K10 observation that
`P(α_s)` controls both classical bounds is structurally rigid: any
algebraic perturbation that breaks the connection would have to perturb
one of `R̄`, perim_sq, or area, which are tied to retained authorities.

## What This Claims

- `(K1, K2)`: NEW retained closed forms for the symmedian point `K`.
- `(K3)`: NEW retained LO identity `K | LO = (rho | LO, eta | LO / 2)`.
- `(K4, K5)`: NEW ratio identities `K_y / V_3_y` (right-triangle
  property at LO) and `K_y / eta_bar` closed form.
- `(K6, K7)`: NEW retained closed form `OK²` and its LO value
  `(N_quark + 1)/(N_pair⁴ N_color) = 7/48`.
- `(K8)`: NEW retained Brocard-axis LO slope
  `-√(N_quark − 1)/N_pair² = -√5/4`.
- `(K9)`: NEW retained Brocard circle (center, radius²) closed forms.
- `(K10)`: NEW deep observation that the polynomial `P(α_s)`
  simultaneously governs the Brocard inequality AND the Brocard
  circle radius.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches; the K10 connection is
  self-contained through the classical Brocard-angle identity
  `cot(omega)=perim_sq/(4 Delta)` and `P(α_s)`'s appearance in `OK²`.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs and the closed forms
  are forced consequences of those inputs combined with classical
  triangle geometry.
- Does **not** depend on any α_s-running pipeline; all results live
  on the protected-γ̄ surface at canonical `α_s(v)`.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_symmedian_brocard_circle_closed_form.py
```

Expected:

```text
TOTAL: PASS=36, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs (`rho_bar`, `eta_bar`,
  `N_pair`, `N_color`, `N_quark`, `R̄²`, circumcenter) by direct text
  matching.
- Computes K1–K10 symbolically via sympy at the retained values and
  asserts each closed form by `simplify(diff) == 0`.
- Sweeps `α_s` to numerically certify `OK² > 0` and `P(α_s) > 0`
  across the physical range (K10 connection).
- Reports a numerical readout at canonical α_s sample points.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.
- [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — `R̄²`, circumcenter `O`.
- [`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — `α_LO = π/2` right-angle property used in K4.

**Companion barred-triangle closed forms (cited for context, not
load-bearing here):**

- [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — orthocenter `H`, centroid `G`, Euler line.
- [`CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md)
  — Pythagorean / sum-rule structure.
- [`CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — Jarlskog `J̄`.

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
