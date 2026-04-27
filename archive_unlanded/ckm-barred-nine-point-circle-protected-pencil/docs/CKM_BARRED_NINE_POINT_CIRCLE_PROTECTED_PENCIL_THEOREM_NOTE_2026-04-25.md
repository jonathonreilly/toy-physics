# Barred Unitarity-Triangle Nine-Point Circle + Protected Coaxial Pencil: EXACT Closed Form Theorem

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives the
**EXACT closed forms** for the **nine-point circle** of the barred
unitarity triangle (center, radius, and all 9 canonical points) on
the retained NLO Wolfenstein protected-γ̄ surface, and identifies a
**deep structural property: TWO of the nine canonical points are
α_s-INVARIANT**, forcing the family of nine-point circles to be a
**COAXIAL PENCIL** through these two fixed points.

The headline observations:

```text
(NP7)  M_c  =  (1/2, 0)             [alpha_s-INVARIANT]

       Forced by V_1 = (0, 0), V_2 = (1, 0) being alpha_s-fixed on the
       retained surface.

(NP8)  H_b  =  (1/N_quark, sqrt(N_quark - 1)/N_quark)  =  (1/6, sqrt(5)/6)
                                                        [alpha_s-INVARIANT]

       Forced by tan(gamma_bar) = sqrt(5) being alpha_s-protected on the
       retained surface (the line V_1 V_3 has alpha_s-invariant slope sqrt(5),
       so the foot of perpendicular from V_2 = (1, 0) onto V_1 V_3 is
       alpha_s-invariant). H_b equals the LO apex V_3 | LO.

(NP9)  |M_c - H_b|  =  1/2  =  R_bar | LO         [alpha_s-INVARIANT]

       The frozen distance equals the LO circumradius.

(NP10) PENCIL THEOREM: as alpha_s varies, the nine-point circle is a
       one-parameter family of circles ALL passing through M_c and H_b.
       The family forms a COAXIAL PENCIL of circles with common chord
       M_c H_b.

(NP11) The locus of nine-point centers N9(alpha_s) traces a STRAIGHT LINE
       in the (rho_bar, eta_bar) plane:
         8 sqrt(5) N9_x  -  20 N9_y  =  sqrt(5).
       This is the line of centers of the coaxial pencil.
```

**Primary runner:**
`scripts/frontier_ckm_barred_nine_point_circle_protected_pencil.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface, with vertices
`V_1 = (0,0)`, `V_2 = (1,0)`, `V_3 = (rho_bar, eta_bar) = ((4-α_s)/24, sqrt(5)(4-α_s)/24)`,
retained circumcenter `O = (1/2, -α_s sqrt(5)/40)`, retained orthocenter
`H = (rho_bar, (20 + α_s)/(24 sqrt(5)))`:

```text
(NP1) The nine-point circle of the unitarity triangle passes through 9
      canonical points: 3 side midpoints, 3 altitude feet, 3
      orthocenter-vertex midpoints (Feuerbach 1822, Brianchon 1820).

(NP2) Center N9 = (O + H)/2 closed form:
        N9_x  =  (16 - alpha_s)/48
              =  (N_pair^4 - alpha_s)/(N_pair^4 N_color),

        N9_y  =  sqrt(5) (10 - alpha_s)/120
              =  sqrt(N_quark - 1) (N_pair (N_quark - 1) - alpha_s)
                 / (N_pair^3 N_color (N_quark - 1)).

(NP3) Radius squared:
        R9^2  =  R_bar^2 / 4  =  (80 + alpha_s^2)/1280
             =  (N_pair^4 (N_quark - 1) + alpha_s^2) / (N_pair^8 (N_quark - 1)).

(NP4) The three SIDE MIDPOINTS:
        M_a  =  (V_2 + V_3)/2  =  ((28 - alpha_s)/48, sqrt(5)(4 - alpha_s)/48),
        M_b  =  (V_1 + V_3)/2  =  ((4 - alpha_s)/48, sqrt(5)(4 - alpha_s)/48),
        M_c  =  (V_1 + V_2)/2  =  (1/2, 0).

(NP5) The three ALTITUDE FEET:
        H_a  =  foot from V_1 onto V_2 V_3
             =  (5(4 - alpha_s)^2/(6(80 + alpha_s^2)),
                 sqrt(5)(4 - alpha_s)(20 + alpha_s)/(6(80 + alpha_s^2))),
        H_b  =  foot from V_2 onto V_1 V_3
             =  (1/6, sqrt(5)/6),                              [alpha_s-INVARIANT]
        H_c  =  foot from V_3 onto V_1 V_2 = base
             =  (rho_bar, 0)  =  ((4 - alpha_s)/24, 0).

(NP6) The three ORTHOCENTER-VERTEX MIDPOINTS:
        P_1  =  (V_1 + H)/2  =  ((4 - alpha_s)/48, (20 + alpha_s)/(48 sqrt(5))),
        P_2  =  (V_2 + H)/2  =  ((28 - alpha_s)/48, (20 + alpha_s)/(48 sqrt(5))),
        P_3  =  (V_3 + H)/2  =  ((4 - alpha_s)/24, sqrt(5)(10 - alpha_s)/60).

      All 9 points verified to lie on the nine-point circle (sympy-exact).

(NP7) NEW: M_c = (1/2, 0) is alpha_s-INVARIANT.
      Reason: both V_1 = (0, 0) and V_2 = (1, 0) are alpha_s-fixed on the
      retained surface (only V_3 = (rho_bar, eta_bar) moves with alpha_s).
      Their midpoint is therefore alpha_s-fixed.

(NP8) NEW: H_b = (1/N_quark, sqrt(N_quark - 1)/N_quark) = (1/6, sqrt(5)/6)
      is alpha_s-INVARIANT.
      Reason: the line V_1 V_3 has slope eta_bar/rho_bar = sqrt(5) =
      tan(gamma_bar), which is alpha_s-protected on the retained surface
      (retained N4: tan(gamma_bar) = sqrt(5) is exact at all NLO orders).
      The foot of perpendicular from V_2 = (1, 0) onto a line through the
      origin with slope m depends only on m and not on the specific point
      on the line. Hence H_b is invariant under alpha_s.

      Numerical: H_b equals the LO apex V_3 | LO = (1/6, sqrt(5)/6).

(NP9) NEW: |M_c - H_b|^2 = 1/4, i.e. |M_c - H_b| = 1/2 = R_bar | LO.
      The frozen distance between the two alpha_s-invariant points equals
      exactly the LO circumradius. This is alpha_s-invariant.

(NP10) PENCIL THEOREM (NEW):
       As alpha_s varies, the nine-point circle of the retained NLO
       Wolfenstein protected-gamma_bar unitarity triangle traces a
       one-parameter family of circles, ALL passing through the two
       alpha_s-invariant points M_c = (1/2, 0) and H_b = (1/6, sqrt(5)/6).

       This family is a COAXIAL PENCIL of circles, with common chord
       M_c H_b. The chord is alpha_s-invariant; the radical axis of the
       pencil is the perpendicular bisector of M_c H_b.

(NP11) The LOCUS OF NINE-POINT CENTERS N9(alpha_s) is a STRAIGHT LINE in
       the (rho_bar, eta_bar) plane, with equation
          8 sqrt(5) N9_x  -  20 N9_y  =  sqrt(5).
       This is the LINE OF CENTERS of the coaxial pencil.
```

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `rho_bar = (4 - alpha_s)/24`, `eta_bar = sqrt(5)(4 - alpha_s)/24`, `tan(gamma_bar) = sqrt(5)` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |
| `R_bar^2 = 1/4 + alpha_s^2/320`, circumcenter `O` | [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md) | retained |
| Orthocenter `H = (rho_bar, (20 + alpha_s)/(24 sqrt(5)))` | [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note
is load-bearing. No unmerged branch is cited.

## Derivation

### NP2, NP3: nine-point circle center and radius

The nine-point circle is the unique circle through the 9 canonical
points (Feuerbach 1822). Its center is the midpoint of `OH`:

```text
N9 = (O + H) / 2.
```

For our triangle, with retained `O = (1/2, -α_s √5/40)` and
`H = (rho_bar, (20 + α_s)/(24 √5))`:

```text
N9_x  =  (1/2 + (4 - alpha_s)/24)/2
      =  (12 + (4 - alpha_s))/(2 * 24)
      =  (16 - alpha_s)/48.

N9_y  =  (-alpha_s sqrt(5)/40 + (20 + alpha_s)/(24 sqrt(5)))/2
      =  ((20 + alpha_s) sqrt(5)/120 - alpha_s sqrt(5)/40)/2
      =  sqrt(5)((20 + alpha_s) - 3 alpha_s)/240
      =  sqrt(5)(20 - 2 alpha_s)/240
      =  sqrt(5)(10 - alpha_s)/120.
```

Radius squared = `R_bar²/4` (universal Feuerbach identity):

```text
R9^2  =  R_bar^2 / 4  =  (1/4 + alpha_s^2/320)/4  =  (80 + alpha_s^2)/1280.
```

### NP4-NP6: the 9 canonical points

Direct computation:

- **Side midpoints**: `M_a = (V_2 + V_3)/2`, `M_b = (V_1 + V_3)/2`,
  `M_c = (V_1 + V_2)/2`.
- **Altitude feet**: `H_i = foot of perpendicular from V_i onto opposite side`.
  Standard formula: from point `P` onto line through `A, B`,
  `F = A + ((P-A)·(B-A))/|B-A|² × (B-A)`.
- **Orthocenter-vertex midpoints**: `P_i = (V_i + H)/2`.

All 9 points have closed-form coordinates on the retained surface
(see Statement above). The runner verifies `|X - N9|² = R9²` for each
point via `sympy.simplify` to zero.

### NP7: M_c is α_s-invariant

`M_c = (V_1 + V_2)/2 = ((0+1)/2, (0+0)/2) = (1/2, 0)`. Since `V_1` and
`V_2` are α_s-fixed (only `V_3` moves on the retained surface), so is
their midpoint.

### NP8: H_b is α_s-invariant — the protected slope theorem

The line `V_1 V_3` passes through the origin with slope
`eta_bar/rho_bar = sqrt(5)`. **This slope is α_s-protected** on the
retained surface (retained `N4`: `tan(γ̄) = √5` is exact NLO).

For any line through the origin `y = m x` with α_s-protected slope
`m`, the foot of perpendicular from `V_2 = (1, 0)` is

```text
H_b  =  (1, 0) - (m·1 - 1·0)/(1 + m^2) × (m, -1)
     =  (1, 0) - m/(1 + m^2) × (m, -1)
     =  (1 - m^2/(1 + m^2),  m/(1 + m^2))
     =  (1/(1 + m^2),  m/(1 + m^2)).
```

For `m = √5 = √(N_quark - 1)`:

```text
H_b  =  (1/(1 + 5),  sqrt(5)/(1 + 5))
     =  (1/6,  sqrt(5)/6)
     =  (1/N_quark,  sqrt(N_quark - 1)/N_quark).
```

`H_b` depends ONLY on the slope `m`, NOT on which point on the line we
take. Since the slope is α_s-protected, `H_b` is α_s-invariant.

**Numerical observation**: `H_b = (1/6, √5/6)` is exactly the LO apex
`V_3 |_{α_s = 0}`. So as α_s varies on the retained surface, the
altitude foot `H_b` stays frozen at the LO apex location, while the
NLO apex `V_3` itself moves toward the origin (since `4 - α_s < 4`).

### NP9: invariant chord length

```text
|M_c - H_b|^2  =  (1/2 - 1/6)^2 + (0 - sqrt(5)/6)^2
              =  (1/3)^2 + 5/36
              =  4/36 + 5/36
              =  9/36
              =  1/4.
```

So `|M_c - H_b| = 1/2`. At LO, `R_bar |_LO = √(80/320) = 1/2`. So the
frozen chord length equals exactly the LO circumradius.

### NP10: pencil theorem

The **power of a point** `P` with respect to a circle with center `C`
and radius `r` is `Pow(P) = |P - C|² - r²`. A point `P` lies on the
circle iff `Pow(P) = 0`.

For `P = M_c` and the nine-point circle:

```text
Pow(M_c)  =  |M_c - N9|^2 - R9^2  =  0   for ALL alpha_s.
```

Sympy verifies this exactly (the difference simplifies to identically
zero). Same for `H_b`. So **both M_c and H_b lie on every nine-point
circle in the family**, making the family a **coaxial pencil** with
common chord `M_c H_b`.

### NP11: line of centers

To find the locus of `N9(α_s)` as α_s varies:

```text
N9_x  =  (16 - alpha_s)/48
=> alpha_s  =  16 - 48 N9_x.

N9_y  =  sqrt(5)(10 - alpha_s)/120
      =  sqrt(5)(10 - (16 - 48 N9_x))/120
      =  sqrt(5)(48 N9_x - 6)/120
      =  sqrt(5)(8 N9_x - 1)/20.

Equivalently:  20 N9_y  =  sqrt(5)(8 N9_x - 1)
              8 sqrt(5) N9_x  -  20 N9_y  =  sqrt(5).
```

This is the equation of a STRAIGHT LINE — the **line of centers** of
the coaxial pencil.

For any coaxial pencil through two fixed points, the line of centers
is the perpendicular bisector of the common chord. Verify:

- Midpoint of `M_c H_b`: `((1/2 + 1/6)/2, (0 + √5/6)/2) = (1/3, √5/12)`.
- Slope of `M_c H_b`: `(√5/6 - 0)/(1/6 - 1/2) = (√5/6)/(-1/3) = -√5/2`.
- Perpendicular bisector has slope `2/√5 = 2√5/5`.

The line `8√5 x - 20 y = √5` rewrites as `y = (8√5/20) x - √5/20 =
(2√5/5) x - √5/20`. Slope `2√5/5` ✓. Passing through `(1/3, √5/12)`?
`y(1/3) = (2√5/5)(1/3) - √5/20 = 2√5/15 - √5/20 = 8√5/60 - 3√5/60 = 5√5/60 = √5/12` ✓.

So the line of centers is exactly the perpendicular bisector of the
common chord, as required by the pencil theorem.

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| NP2 N9_x | `(16 - α_s)/48` | sympy `simplify(diff) == 0` |
| NP2 N9_y | `√5(10 - α_s)/120` | sympy `simplify(diff) == 0` |
| NP3 R9² | `(80 + α_s²)/1280` | sympy `simplify(diff) == 0` |
| NP4 M_a, M_b, M_c | each on the circle | sympy `simplify(diff) == 0` |
| NP5 H_a, H_b, H_c | each on the circle | sympy `simplify(diff) == 0` |
| NP6 P_1, P_2, P_3 | each on the circle | sympy `simplify(diff) == 0` |
| NP7 M_c invariance | `d(M_c)/d(α_s) = 0` | sympy exact |
| NP8 H_b invariance | `d(H_b)/d(α_s) = 0` | sympy exact |
| NP8 H_b value | `(1/N_quark, √(N_quark-1)/N_quark) = (1/6, √5/6)` | sympy exact |
| NP9 chord length² | `\|M_c − H_b\|² = 1/4` | sympy exact |
| NP10 pencil M_c | `Pow(M_c) = 0` for all α_s | sympy `simplify == 0` |
| NP10 pencil H_b | `Pow(H_b) = 0` for all α_s | sympy `simplify == 0` |
| NP11 line of centers | `8√5 N9_x − 20 N9_y − √5 = 0` | sympy exact |

## Science Value

### What this lets the framework state cleanly

Previously, the framework had retained closed forms for the
circumradius `R̄`, circumcenter `O`, orthocenter `H`, centroid `G`,
and Euler line of the barred unitarity triangle. The **nine-point
circle** — which Feuerbach showed passes through 9 canonical points
(side midpoints, altitude feet, orthocenter-vertex midpoints) — was
implicit (since `N9 = (O+H)/2` and `R9 = R̄/2`) but had not been
expressed in explicit closed form, nor had its 9 canonical points
been derived.

This note delivers:

1. **NEW retained closed forms** (NP2-NP6) for the nine-point circle
   center, radius, and all 9 canonical points.

2. **NEW α_s-invariance result** (NP7-NP8): TWO of the 9 canonical
   points — `M_c` (midpoint of unit base) and `H_b` (foot of altitude
   from `V_2` onto `V_1V_3`) — are α_s-INVARIANT on the retained
   surface. The α_s-invariance of `H_b` is forced by the
   α_s-protected slope of `V_1V_3` (i.e., the retained `tan(γ̄) = √5`).

3. **NEW frozen-chord identity** (NP9): the distance between the two
   α_s-invariant points equals exactly the LO circumradius:
   `|M_c − H_b| = 1/2 = R̄|_LO`.

4. **NEW PENCIL THEOREM** (NP10): the family of nine-point circles
   parameterized by α_s is a **COAXIAL PENCIL** of circles through
   the two fixed points `M_c, H_b`. As α_s varies, the circle
   rotates and scales while always passing through the common chord
   endpoints.

5. **NEW LINE OF CENTERS** (NP11): the locus of nine-point centers
   `N9(α_s)` traces a STRAIGHT LINE in the `(ρ̄, η̄)` plane:
   `8√5 N9_x - 20 N9_y = √5`. This is the line of centers of the
   coaxial pencil, which equals the perpendicular bisector of the
   common chord `M_c H_b`.

### Why this counts as pushing the science forward

The α_s-protected `tan(γ̄) = √5` retained at NLO is **the central
algebraic feature** of the protected-γ̄ surface. This note shows
that the protected slope **forces a non-trivial geometric structure
on the family of nine-point circles**:

- One specific point of the nine-point circle (`H_b`) sits at the
  LO apex location, **frozen for all α_s**.
- Combined with the α_s-fixity of `V_1, V_2`, this gives **two
  α_s-invariant points** on every nine-point circle.
- The family of nine-point circles is therefore not just a generic
  one-parameter family — it is a **coaxial pencil** with two fixed
  carrier points and a fixed common chord.

The geometric interpretation is striking: as α_s varies, **the
nine-point circle pivots through the two fixed points `M_c, H_b`,
with its center sliding along a straight line in the plane**. This
is the same kind of "α_s-invariant geometric scaffold" that emerged
in the Pedoe metric (where α_s plays the role of a Euclidean
coordinate on the parameter space).

The line-of-centers result (NP11) is particularly clean: a SINGLE
LINE in the plane parameterizes the entire family of nine-point
circles. The framework's protected-γ̄ structure forces this
straightness.

### Falsifiable structural claim

The closure (NP7-NP11) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
forces:
  H_b  =  (1/N_quark, sqrt(N_quark - 1)/N_quark)  =  (1/6, sqrt(5)/6),
  |M_c - H_b|  =  1/2  =  R_bar | LO,
  Locus of nine-point centers:  8 sqrt(5) N9_x - 20 N9_y - sqrt(5) = 0  (straight line).
```

Any framework revision that **breaks the protected slope tan(γ̄) = √5**
would immediately break the α_s-invariance of `H_b` (the foot would
then move with α_s), and hence break the pencil theorem and the
straight-line locus of centers. Conversely, any framework that
preserves the protected slope automatically inherits the pencil and
line-of-centers structure.

## What This Claims

- `(NP2-NP6)`: NEW retained closed forms for the nine-point circle
  center, radius, and the 9 canonical points.
- `(NP7)`: NEW retained α_s-invariance of `M_c = (1/2, 0)`.
- `(NP8)`: NEW retained α_s-invariance of
  `H_b = (1/N_quark, √(N_quark - 1)/N_quark) = (1/6, √5/6)`,
  forced by the α_s-protected slope `tan(γ̄) = √5`.
- `(NP9)`: NEW retained α_s-invariant chord length
  `|M_c - H_b| = R̄|_LO = 1/2`.
- `(NP10)`: NEW retained PENCIL THEOREM — the family of nine-point
  circles is a coaxial pencil through `M_c` and `H_b`.
- `(NP11)`: NEW retained LINE OF CENTERS — the locus of `N9(α_s)`
  is the straight line `8√5 N9_x - 20 N9_y = √5`.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs.
- Does **not** depend on any α_s-running pipeline.
- Does **not** make a direct CKM-observable claim about the
  nine-point circle; it is a derived geometric structure.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_nine_point_circle_protected_pencil.py
```

Expected:

```text
TOTAL: PASS=32, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs (`rho_bar`, `eta_bar`,
  `tan(γ̄) = √5`, `N_pair`, `N_color`, `N_quark`, `R̄²`, orthocenter).
- Computes NP2-NP11 symbolically via sympy and asserts each closed
  form by `simplify(diff) == 0`.
- Verifies that all 9 canonical points lie on the nine-point circle
  symbolically.
- Confirms the α_s-invariance of `M_c` and `H_b` by symbolic
  differentiation.
- Verifies the pencil theorem by computing `Pow(M_c)` and `Pow(H_b)`
  with respect to the family.
- Verifies the line of centers symbolically.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates; `tan(γ̄) = √5` α_s-protected.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.
- [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — `R̄²`, circumcenter `O`.
- [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — orthocenter `H`, centroid `G`, Euler line.

**Companion barred-triangle closed forms (cited for context, not
load-bearing here):**

- [`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — apex angle `α̃`.

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch (Brocard-angle, Symmedian, Steiner-Marden,
  Weitzenbock, Pedoe, Brocard-points, Napoleon branches under review
  are referenced only for structural context).
- Any candidates-tier theorem.
