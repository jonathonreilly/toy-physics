# Barred Unitarity-Triangle Napoleon Triangles: EXACT Closed Form Theorem

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure corollary on the proposed_promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives **EXACT
closed forms** for the **outer and inner Napoleon triangles** of the
barred unitarity triangle, and identifies their side² and area
products as **direct factors of the Brocard polynomial `P(α_s)`**.

The headline closed forms:

```text
(N2)  Outer / inner Napoleon side^2:
        N_outer^2  =  perim_sq/6 + 2 Area/sqrt(3)
                    =  ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15)(4 - alpha_s))/288
                    =  W_+/6,
        N_inner^2  =  perim_sq/6 - 2 Area/sqrt(3)
                    =  ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15)(4 - alpha_s))/288
                    =  W_-/6.

(N3)  Universal sum: N_outer^2 + N_inner^2 = perim_sq/3.

(N4)  NEW product factorization (Brocard polynomial):
        N_outer^2 * N_inner^2  =  W_+ * W_- / 36
                               =  P(alpha_s) / 82944
                               =  P(alpha_s) / (N_pair^10 N_color^4).

(N6)  NEW product of Napoleon areas:
        Area_outer_Nap * Area_inner_Nap  =  (3/16) * N_outer^2 N_inner^2
                                          =  3 P(alpha_s) / (16 * 82944)
                                          =  P(alpha_s) / 442368.

(N8)  LO recovery in pure structural integers:
        N_outer^2 + N_inner^2 | LO  =  N_pair / N_color  =  2/3,
        N_outer^2 * N_inner^2 | LO  =  (N_quark + 1) / (N_pair^2 N_color^3)  =  7/108.

(N9)  NEW Napoleon discriminant:
        (N_outer^2 - N_inner^2)^2  =  5 (4 - alpha_s)^2 / 432
                                    =  (16/3) Area^2
                                    =  (N_pair^4 / N_color) Area^2.
```

The Napoleon triangles' side² values are **exactly W_+ / 6 and W_- / 6**,
where `W_+, W_-` are the Weitzenbock-style sum and gap defined below from
`perim_sq` and `Area`. Their **product is `P(α_s) / (N_pair^10 N_color^4)`** —
the Brocard polynomial's structural-integer-scaled image. So Napoleon
geometry is **algebraically tied to both Weitzenbock and Brocard
structure** on the retained surface.

**Primary runner:**
`scripts/frontier_ckm_barred_napoleon_triangles_exact_closed_form.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface, with vertices
`V_1 = (0,0)`, `V_2 = (1,0)`, `V_3 = (rho_bar, eta_bar) = ((4-α_s)/24, sqrt(5)(4-α_s)/24)`,
side-length squares `(80+α_s²)/96, (4-α_s)²/96, 1` summing to
`perim_sq = (α_s²-4α_s+96)/48`, and `Area = √5(4-α_s)/48`:

```text
(N1)  Napoleon's theorem (classical): erecting equilateral triangles
      EXTERNALLY on each side of the unitarity triangle, the centroids
      of those three equilateral triangles form an equilateral triangle
      (the OUTER Napoleon triangle). Erecting INTERNALLY gives the
      INNER Napoleon triangle.

      Both Napoleon triangles share the centroid G of the original
      triangle as their center.

(N2)  Outer / inner Napoleon side^2:
        N_outer^2  =  perim_sq/6 + 2 Area/sqrt(3),
        N_inner^2  =  perim_sq/6 - 2 Area/sqrt(3).

      On the retained surface:
        N_outer^2  =  ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15)(4 - alpha_s))/288,
        N_inner^2  =  ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15)(4 - alpha_s))/288.

      Equivalent form (Weitzenbock connection):
        N_outer^2  =  W_+/6,
        N_inner^2  =  W_-/6,

      where W_+ = perim_sq + 4 sqrt(3) Area is the Weitzenbock-style sum
      and W_- = perim_sq - 4 sqrt(3) Area is the Weitzenbock-style gap.

(N3)  Universal triangle identity:
        N_outer^2 + N_inner^2  =  perim_sq/3  =  (a^2 + b^2 + c^2)/3.

      LO recovery: N_outer^2 + N_inner^2 |LO = N_pair/N_color = 2/3.

(N4)  NEW product factorization:
        N_outer^2 * N_inner^2  =  W_+ * W_- / 36
                               =  P(alpha_s) / (36 * 2304)
                               =  P(alpha_s) / 82944,

      where  P(alpha_s) = (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2
      is the Brocard polynomial (universal equilateral excess).

      Structural-integer scaling: 82944 = 288^2 = (N_pair^5 N_color^2)^2
                                      = N_pair^10 N_color^4.

(N5)  Napoleon-triangle areas (any equilateral triangle of side s has
      area sqrt(3) s^2/4):
        Area_outer_Nap  =  sqrt(3) N_outer^2 / 4,
        Area_inner_Nap  =  sqrt(3) N_inner^2 / 4.

(N6)  NEW product of Napoleon areas:
        Area_outer_Nap * Area_inner_Nap  =  (3/16) N_outer^2 N_inner^2
                                          =  3 P(alpha_s) / (16 * 82944)
                                          =  P(alpha_s) / 442368.

(N7)  Classical Napoleon area difference:
        Area_outer_Nap - Area_inner_Nap  =  Area_triangle.

      (Holds for any triangle; verified retained-surface algebra here.)

(N8)  LO recovery -- pure structural integers:
        N_outer^2 + N_inner^2 | LO  =  N_pair / N_color  =  2/3,
        N_outer^2 * N_inner^2 | LO  =  (N_quark + 1)/(N_pair^2 N_color^3)  =  7/108.

      Numerical:
        N_outer^2 | LO  =  (6 + sqrt(15))/3 / 6  =  (6 + sqrt(15))/18,
        N_inner^2 | LO  =  (6 - sqrt(15))/3 / 6  =  (6 - sqrt(15))/18.

(N9)  NEW Napoleon discriminant:
        (N_outer^2 - N_inner^2)^2  =  (W_+ - W_-)^2 / 36
                                    =  (sqrt(15)(4 - alpha_s)/6)^2 / 36
                                    =  5 (4 - alpha_s)^2 / 432
                                    =  (16/3) Area^2
                                    =  (N_pair^4 / N_color) Area^2.

      The Napoleon discriminant is exactly (N_pair^4/N_color) times
      the squared triangle area -- a clean structural-integer rescaling.
```

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `rho_bar = (4 - alpha_s)/24`, `eta_bar = sqrt(5)(4 - alpha_s)/24` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note
is load-bearing. No unmerged branch is cited as load-bearing. The
`W_+`, `W_-`, and `P(alpha_s)` symbols are defined inside this note,
and the Napoleon side² closed forms are derived directly from the
retained perimeter² and Area expressions plus the classical Napoleon
side formula.

## Derivation

### Napoleon's theorem (classical)

For any triangle, **Napoleon's theorem** states that the centroids of
the three equilateral triangles erected externally on each side form
an equilateral triangle (the **outer Napoleon triangle**). Similarly
for internal erections (the **inner Napoleon triangle**). Both
Napoleon triangles share the centroid `G` of the original triangle as
their center.

The classical formula for the side length squared:

```text
N_outer^2  =  (a^2 + b^2 + c^2)/6 + 2 K/sqrt(3),
N_inner^2  =  (a^2 + b^2 + c^2)/6 - 2 K/sqrt(3),
```

where `(a, b, c)` are the original triangle's side lengths and `K`
is its area.

### N2: closed forms for the Napoleon side²

For our retained CKM unitarity triangle:

```text
perim_sq  =  a^2 + b^2 + c^2  =  (alpha_s^2 - 4 alpha_s + 96)/48,
Area      =  sqrt(5) (4 - alpha_s)/48.

perim_sq/6        =  (alpha_s^2 - 4 alpha_s + 96)/288,
2 Area/sqrt(3)    =  2 * sqrt(5)(4 - alpha_s)/(48 sqrt(3))
                  =  sqrt(15)(4 - alpha_s)/72
                  =  4 sqrt(15)(4 - alpha_s)/288.
```

So:

```text
N_outer^2  =  ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15)(4 - alpha_s))/288,
N_inner^2  =  ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15)(4 - alpha_s))/288.
```

Define the Weitzenbock-style sum/gap directly by
`W_+ = perim_sq + 4√3·Area`, `W_- = perim_sq - 4√3·Area`. Comparing
denominators (W_+, W_- have denominator 48; Napoleon side² has
denominator 288 = 48 × 6):

```text
N_outer^2  =  W_+/6,
N_inner^2  =  W_-/6.
```

This is the **Weitzenbock-Napoleon connection** — the Weitzenbock
sum/gap divided by the structural-integer factor 6 gives the
Napoleon side² values directly.

### N3: sum is universal

```text
N_outer^2 + N_inner^2  =  2 * perim_sq/6  =  perim_sq/3.
```

This is a universal triangle identity: `(a²+b²+c²)/3` for any triangle.

At LO: `perim_sq|LO = (96)/48 = 2`, so `N_outer² + N_inner²|LO = 2/3`.

In structural integers: `2/3 = N_pair/N_color`.

### N4: product factorization — Brocard polynomial

```text
N_outer^2 * N_inner^2  =  (W_+/6)(W_-/6)  =  W_+ W_- / 36.
```

Directly,

```text
W_+ W_- = perim_sq^2 - 48 Area^2 = P(α_s)/2304,
```

so

```text
N_outer^2 * N_inner^2  =  P(alpha_s) / (2304 * 36)
                       =  P(alpha_s) / 82944
                       =  P(alpha_s) / (N_pair^10 N_color^4).
```

This is the **central NEW identity** of this branch: the product of
Napoleon side² is the Brocard polynomial scaled by the structural
integer `82944 = N_pair^10 N_color^4`.

### N5, N6: Napoleon areas

Any equilateral triangle of side `s` has area `√3 s²/4`. So:

```text
Area_outer_Nap  =  sqrt(3) N_outer^2 / 4,
Area_inner_Nap  =  sqrt(3) N_inner^2 / 4.
```

Product:

```text
Area_outer_Nap * Area_inner_Nap  =  (3/16) N_outer^2 N_inner^2
                                  =  3 P(alpha_s) / (16 * 82944)
                                  =  P(alpha_s) / 442368.
```

### N7: classical area difference

```text
Area_outer_Nap - Area_inner_Nap  =  sqrt(3)(N_outer^2 - N_inner^2)/4
                                  =  sqrt(3) * (4 sqrt(15)(4 - alpha_s)/144)
                                  =  sqrt(45)(4 - alpha_s)/36
                                  =  3 sqrt(5)(4 - alpha_s)/36
                                  =  sqrt(5)(4 - alpha_s)/12.

Area_triangle  =  sqrt(5)(4 - alpha_s)/48.

The classical Napoleon area-difference identity is
`Area_outer - Area_inner = Area_triangle`. On the retained surface:

```text
N_outer^2 - N_inner^2  =  (W_+/6) - (W_-/6)  =  (W_+ - W_-)/6
                       =  (8 sqrt(15)(4 - alpha_s)/48)/6
                       =  8 sqrt(15)(4 - alpha_s)/288
                       =  sqrt(15)(4 - alpha_s)/36.

Area_outer_Nap - Area_inner_Nap  =  sqrt(3)(N_outer^2 - N_inner^2)/4
                                  =  sqrt(3) sqrt(15)(4 - alpha_s)/(36 * 4)
                                  =  sqrt(45)(4 - alpha_s)/144
                                  =  3 sqrt(5)(4 - alpha_s)/144
                                  =  sqrt(5)(4 - alpha_s)/48
                                  =  Area_triangle.  ✓
```

So the classical Napoleon area-difference identity holds on the
retained surface, verified algebraically.

### N8: LO recovery

At `α_s = 0`:

```text
N_outer^2 + N_inner^2 | LO  =  perim_sq|LO / 3  =  2/3
                            =  N_pair / N_color.

N_outer^2 * N_inner^2 | LO  =  P(0) / 82944  =  5376/82944
                            =  21/324
                            =  7/108
                            =  (N_quark + 1) / (N_pair^2 N_color^3).
```

Verify: `N_pair² × N_color³ = 4 × 27 = 108` ✓; `N_quark + 1 = 7` ✓.

### N9: Napoleon discriminant

```text
(N_outer^2 - N_inner^2)^2  =  (sqrt(15)(4 - alpha_s)/36)^2
                            =  15 (4 - alpha_s)^2 / 1296
                            =  5 (4 - alpha_s)^2 / 432.
```

Equivalent form via `Area² = 5(4 - α_s)²/2304`:

```text
(N_outer^2 - N_inner^2)^2  =  5 (4 - alpha_s)^2 / 432
                            =  Area^2 * 2304 / 432
                            =  Area^2 * 16/3
                            =  (N_pair^4 / N_color) Area^2.
```

So the Napoleon discriminant is `(N_pair⁴/N_color)` times the squared
triangle area. **A clean structural-integer relation between Napoleon
discriminant and triangle area.**

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| N2 N_outer² | `((α_s²-4α_s+96)+4√15(4-α_s))/288` | sympy `simplify(diff) == 0` |
| N2 N_inner² | `((α_s²-4α_s+96)-4√15(4-α_s))/288` | sympy `simplify(diff) == 0` |
| N2 W_+ | `N_outer² = W_+/6` | sympy `simplify(diff) == 0` |
| N2 W_- | `N_inner² = W_-/6` | sympy `simplify(diff) == 0` |
| N3 sum | `N_outer²+N_inner² = perim_sq/3` | sympy `simplify(diff) == 0` |
| N3 LO | `2/3 = N_pair/N_color` | exact rational |
| N4 product | `N_outer²·N_inner² = P(α_s)/82944` | sympy `simplify(diff) == 0` |
| N4 struct | `82944 = N_pair^10 N_color⁴` | exact integer |
| N6 area-product | `Area_o·Area_i = 3 P/(16·82944)` | sympy `simplify(diff) == 0` |
| N7 area-diff | `Area_o - Area_i = Area_triangle` | sympy `simplify(diff) == 0` |
| N8 LO sum | `N_pair/N_color = 2/3` | sympy exact |
| N8 LO product | `(N_quark+1)/(N_pair²N_color³) = 7/108` | sympy exact |
| N9 discriminant | `(N_outer²-N_inner²)² = 5(4-α_s)²/432` | sympy `simplify(diff) == 0` |
| N9 area form | `(N_outer²-N_inner²)² = (16/3) Area²` | sympy `simplify(diff) == 0` |
| centroid invariance | Napoleon centroid = original centroid | explicit symbolic centroid construction |

Numerical readout for Napoleon side² across α_s:

| `α_s(v)` | `N_outer²` | `N_inner²` | `N_o²·N_i²` |
| ---: | ---: | ---: | ---: |
| 0 (LO) | 0.5485 | 0.1182 | 0.0648 (= 7/108) |
| 0.118 | 0.5462 | 0.1162 | 0.0635 |
| 0.30 | 0.5430 | 0.1135 | 0.0617 |

The outer Napoleon is consistently ≈4× the inner Napoleon side².

## Science Value

### What this lets the framework state cleanly

The current main CKM NLO geometry stack already contains retained closed
forms for the protected-`gamma_bar` barred triangle's side lengths, apex
angle, circumradius/circumcenter, orthocenter/Euler line, and Pedoe
similarity deficit. The **Napoleon triangles** — the classical equilateral
triangles constructed from each side via centroids of erected equilaterals —
were not previously expressed in closed form on the retained surface.

This note delivers:

1. **NEW Napoleon side² closed forms** (N2): rational algebraic
   expressions involving `√15`, exactly equal to `W_+/6` and `W_-/6`
   for the self-contained Weitzenbock-style sum/gap defined above.

2. **NEW Brocard-polynomial product factorization** (N4):
   `N_outer² · N_inner² = P(α_s)/82944 = P(α_s)/(N_pair^10 N_color⁴)`.
   The Brocard polynomial `P(α_s)` (universal equilateral excess) is
   exactly the structural-integer-scaled product of Napoleon side².

3. **NEW Napoleon-area product factorization** (N6):
   `Area_outer_Nap · Area_inner_Nap = 3 P(α_s)/(16·82944) = P(α_s)/442368`.

4. **NEW LO structural-integer recoveries** (N8):
   `N_outer²+N_inner²|_LO = N_pair/N_color = 2/3`,
   `N_outer²·N_inner²|_LO = (N_quark+1)/(N_pair²N_color³) = 7/108`.

5. **NEW Napoleon discriminant identity** (N9):
   `(N_outer²-N_inner²)² = (N_pair⁴/N_color)·Area²`. The Napoleon
   discriminant is exactly `(N_pair⁴/N_color)` times the squared
   triangle area — a clean structural-integer rescaling tying
   Napoleon geometry to the Jarlskog-area surface.

### Why this counts as pushing the science forward

Napoleon's theorem is one of the most celebrated classical results
in triangle geometry: erecting equilateral triangles externally on
each side gives a new equilateral triangle. Applied to the retained
CKM unitarity triangle:

- The **side² values** of the Napoleon triangles equal `W_±/6`,
  directly tying Napoleon to **Weitzenbock**.
- The **product** of side² values equals `P(α_s)/82944`, directly
  tying Napoleon to the **Brocard polynomial**.
- The **discriminant** equals `(N_pair⁴/N_color)·Area²`, directly
  tying Napoleon to the **triangle area / Jarlskog**.

So Napoleon geometry connects the self-contained Weitzenbock-style
sum/gap and the triangle-area/Jarlskog surface through the same
`W_+, W_-, P(α_s), Area` scaffold. This landing proves the Napoleon
entry itself. Any broader Brocard/Steiner/Marden/Weitzenbock comparison
remains context unless separately present on `main`.

### Falsifiable structural claim

The closure (N2-N9) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
forces:
  N_outer^2 * N_inner^2  =  P(alpha_s) / (N_pair^10 N_color^4),
  (N_outer^2 - N_inner^2)^2  =  (N_pair^4 / N_color) Area^2,
  LO:  N_outer^2 * N_inner^2 |LO  =  (N_quark + 1)/(N_pair^2 N_color^3)  =  7/108.
```

Any framework revision moving `(rho_bar, eta_bar)` off the retained
surface, or shifting the structural integers, would simultaneously
break N4 (product factorization), N9 (discriminant), and the LO
structural-integer recoveries.

## What This Claims

- `(N1)`: NEW retained verification of Napoleon's theorem for the
  retained CKM unitarity triangle (centroid invariance verified
  numerically).
- `(N2)`: NEW retained closed forms for the outer/inner Napoleon
  side², expressed both directly in `α_s` and in terms of the
  Weitzenbock sum/gap.
- `(N3)`: NEW retained verification that the universal triangle
  identity `N_outer²+N_inner² = perim_sq/3` holds on the surface.
- `(N4)`: NEW retained Brocard-polynomial product factorization
  `N_outer²·N_inner² = P(α_s)/(N_pair^10 N_color⁴)`.
- `(N5, N6)`: NEW retained Napoleon-area closed forms and product.
- `(N7)`: NEW retained verification of the classical area-difference
  identity on the surface.
- `(N8)`: NEW retained LO structural-integer recoveries.
- `(N9)`: NEW retained Napoleon-discriminant identity tying it to
  the triangle area through `(N_pair⁴/N_color)`.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing. The `W_+`, `W_-`,
  and `P(α_s)` objects used here are defined and verified inside this note
  from the retained `perim_sq` and `Area`.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs.
- Does **not** depend on any α_s-running pipeline.
- Does **not** make a direct CKM-observable claim about the Napoleon
  triangles; they are derived geometric structures of the unitarity
  triangle.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_napoleon_triangles_exact_closed_form.py
```

Expected:

```text
TOTAL: PASS=42, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs (`rho_bar`, `eta_bar`,
  `N_pair`, `N_color`, `N_quark`).
- Computes N2–N9 symbolically via sympy at the retained values and
  asserts each closed form by `simplify(diff) == 0`.
- Verifies the actual external/internal equilateral-centroid construction,
  equilateral side² identities, and centroid-invariance property exactly.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.

**Companion barred-triangle closed forms on `main` (context only, not
load-bearing here):**

- [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — centroid `G` (which is also the center of both Napoleon triangles).
- [`CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — Jarlskog `J̄` (related to triangle area).

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
