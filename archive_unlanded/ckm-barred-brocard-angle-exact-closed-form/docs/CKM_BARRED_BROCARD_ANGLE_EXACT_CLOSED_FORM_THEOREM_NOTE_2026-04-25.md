# Barred Unitarity-Triangle Brocard Angle: EXACT Closed Form Theorem

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives the
**EXACT closed form for the Brocard angle `ω̄`** of the barred unitarity
triangle, plus the supporting closed forms for the perimeter-squared
`a² + b² + c²`, `tan(ω̄)`, `cot(ω̄)`, the `(sin², cos²)` pair at LO in
**pure structural integers**, the Brocard inequality on the retained
surface, the standard cot-sum identity, and a NEW Brocard–Jarlskog
identity in the barred plane.

The headline closed form, in two equivalent representations:

```text
tan(omega_bar)  =  4 sqrt(5) (4 - alpha_s(v))  /  (alpha_s(v)^2 - 4 alpha_s(v) + 96)

                =  N_pair^2 sqrt(N_quark - 1) (N_pair^2 - alpha_s(v))
                   /  (alpha_s(v)^2 - N_pair^2 alpha_s(v) + N_pair^4 N_quark).
```

Numerator linear in `α_s(v)`, denominator a degree-2 polynomial in
`α_s(v)`. The LO recovery is striking:

```text
tan(omega_bar | LO)  =  sqrt(N_quark - 1) / N_quark  =  eta | LO  =  sqrt(5)/6.
```

So at LO **the Brocard angle of the unitarity triangle equals
`arctan(eta | LO)`**, identifying a classical triangle invariant
(`ω̄`) with the Wolfenstein imaginary part on the protected-γ̄ surface.

The `(sin², cos²)` pair at LO factor cleanly in retained integers:

```text
sin^2(omega_bar | LO)  =  (N_quark - 1)   /  (N_quark^2 + N_quark - 1)  =  5/41,
cos^2(omega_bar | LO)  =  N_quark^2        /  (N_quark^2 + N_quark - 1)  =  36/41.
```

**Primary runner:**
`scripts/frontier_ckm_barred_brocard_angle_exact_closed_form.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface (where `tan(γ̄) = √5`
is α_s-protected by retained `(N4)` and `tan(β̄)` carries the retained
closed form `(N5)`):

```text
(B1)  a^2 + b^2 + c^2  =  (alpha_s^2 - 4 alpha_s + 96) / 48
                       =  (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)
                          / (N_pair^4 N_color).

      LO recovery: a^2 + b^2 + c^2 |_{alpha_s = 0}  =  N_quark / N_color  =  2.

(B2)  cot(omega_bar)  =  (alpha_s^2 - 4 alpha_s + 96)
                          /  [4 sqrt(5) (4 - alpha_s)]

                      =  (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)
                          /  [N_pair^2 sqrt(N_quark - 1) (N_pair^2 - alpha_s)].

(B3)  tan(omega_bar)  =  4 sqrt(5) (4 - alpha_s)
                          /  (alpha_s^2 - 4 alpha_s + 96)

                      =  N_pair^2 sqrt(N_quark - 1) (N_pair^2 - alpha_s)
                          /  (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark).

(B4)  LO recovery:
        tan(omega_bar | LO)  =  sqrt(N_quark - 1) / N_quark  =  eta | LO  =  sqrt(5)/6
        omega_bar | LO       =  arctan(eta | LO)            ≈  20.4517 deg.

(B5)  Pure structural-integer LO trig:
        sin^2(omega_bar | LO)  =  (N_quark - 1)  /  (N_quark^2 + N_quark - 1)  =  5/41,
        cos^2(omega_bar | LO)  =  N_quark^2       /  (N_quark^2 + N_quark - 1)  =  36/41.

(B6)  Brocard inequality on the retained surface:
        cot(omega_bar)  >=  sqrt(3)         (equivalently  omega_bar  <=  pi/6).

      Verified for all alpha_s in [0, 3.9] (the physically relevant range plus
      headroom); the polynomial
        ((alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2)
      is strictly positive on this interval.

(B7)  Cot-sum identity (independent path):
        cot(omega_bar)  =  cot(alpha_bar) + cot(beta_bar) + cot(gamma_bar),

      with the right-hand side computed directly from the retained
      `tan(gamma_bar) = sqrt(5)`, retained `tan(beta_bar)` closed form,
      and `alpha_bar = pi - gamma_bar - beta_bar`.

(B8)  Brocard - Jarlskog identity in the barred plane:
        2 J_bar (Wolfenstein-normalized)  =  (a^2 + b^2 + c^2) tan(omega_bar)

      i.e. the Jarlskog (twice the area, in the unit-base barred plane)
      factors as the perimeter-squared times `tan(omega_bar)`.
```

## Retained Inputs

Each authority is a retained-tier note on `main`. The runner extracts
the verbatim `Status:` line from each file and verifies the tier label.

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `rho_bar = (4 - alpha_s)/24`, `eta_bar = sqrt(5)(4 - alpha_s)/24`, `tan(gamma_bar) = sqrt(5)`, `tan(beta_bar)` closed form | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = N_pair * N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/N_quark = 1/6`, `eta = sqrt(N_quark - 1)/N_quark = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |
| `alpha_LO = pi/2` (atlas right angle); barred-triangle vertex layout | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) | retained |
| `lambda^2 = alpha_s(v)/N_pair`, `A^2 = N_pair / N_color` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note is
load-bearing. No unmerged branch is cited. No new selector for
`d`, `N_color`, or `N_pair` is asserted -- all structural integers are
retained inputs and the closed forms are forced consequences of those
retained values combined with classical triangle geometry.

## Derivation

### Vertex layout

In the barred `(rho_bar, eta_bar)` plane the unitarity triangle has

```text
V_1  =  (0, 0),
V_2  =  (1, 0),
V_3  =  (rho_bar, eta_bar)  =  ((4 - alpha_s)/24,  sqrt(5)(4 - alpha_s)/24).
```

The unit base `|V_1 V_2| = 1` is the standard Wolfenstein normalization.

### B1: perimeter² closed form

Side-length squares, by Pythagoras in the plane:

```text
a^2  =  |V_2 V_3|^2  =  (1 - rho_bar)^2 + eta_bar^2,
b^2  =  |V_1 V_3|^2  =  rho_bar^2 + eta_bar^2,
c^2  =  |V_1 V_2|^2  =  1.
```

On the protected-γ̄ surface, `eta_bar / rho_bar = sqrt(5)`, so

```text
b^2  =  rho_bar^2 + 5 rho_bar^2  =  6 rho_bar^2  =  N_quark rho_bar^2,

a^2  =  1 - 2 rho_bar + rho_bar^2 + eta_bar^2  =  1 - 2 rho_bar + 6 rho_bar^2.
```

Substituting `rho_bar = (4 - alpha_s)/24`:

```text
a^2 + b^2 + c^2  =  12 rho_bar^2 - 2 rho_bar + 2
                =  2 (6 rho_bar^2 - rho_bar + 1)
                =  (alpha_s^2 - 4 alpha_s + 96) / 48.
```

In retained-integer form (using `48 = N_pair^4 N_color`,
`96 = N_pair^4 N_quark`, `4 = N_pair^2`):

```text
a^2 + b^2 + c^2  =  (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)
                    / (N_pair^4 N_color).
```

LO recovery: at `alpha_s = 0` the numerator is `N_pair^4 N_quark` and
the denominator is `N_pair^4 N_color`, so the ratio collapses to
`N_quark / N_color = 6/3 = 2`.

### B2 / B3: Brocard angle closed form

The triangle's Cartesian area is `Area = eta_bar / 2` (base `1`, height
`eta_bar`). The classical Brocard formula states

```text
cot(omega)  =  (a^2 + b^2 + c^2) / (4 Area).
```

Substituting B1 and `Area = eta_bar / 2 = sqrt(5)(4 - alpha_s)/48`:

```text
cot(omega_bar)  =  [(alpha_s^2 - 4 alpha_s + 96)/48]
                    /  [4 sqrt(5)(4 - alpha_s)/48]
               =  (alpha_s^2 - 4 alpha_s + 96)
                    /  [4 sqrt(5)(4 - alpha_s)]
               =  (alpha_s^2 - N_pair^2 alpha_s + N_pair^4 N_quark)
                    /  [N_pair^2 sqrt(N_quark - 1) (N_pair^2 - alpha_s)].
```

Reciprocating gives B3:

```text
tan(omega_bar)  =  4 sqrt(5) (4 - alpha_s) / (alpha_s^2 - 4 alpha_s + 96).
```

Both forms are sympy-exact; the runner asserts the difference between
the computed and stated form is identically zero.

### B4: LO recovery `tan(ω̄|_LO) = η|_LO`

At `alpha_s = 0`:

```text
tan(omega_bar | LO)  =  4 sqrt(5) * 4 / 96  =  16 sqrt(5)/96  =  sqrt(5)/6
                     =  sqrt(N_quark - 1) / N_quark
                     =  eta | LO.
```

So at LO the Brocard angle of the barred triangle is `arctan(eta | LO)`,
i.e. the angle the apex `V_3 = (rho_LO, eta_LO) = (1/6, sqrt(5)/6)` makes
with the unit base in the LO plane. Numerically `omega_bar | LO ~ 20.4517°`,
well inside the Brocard bound `pi/6 = 30°`.

### B5: pure structural-integer `(sin², cos²)` at LO

From `tan(omega_bar | LO) = sqrt(5)/6`:

```text
tan^2(omega_bar | LO)        =  5/36                  =  (N_quark - 1) / N_quark^2,
1 + tan^2(omega_bar | LO)    =  41/36                 =  (N_quark^2 + N_quark - 1) / N_quark^2,

sin^2(omega_bar | LO)
  =  tan^2 / (1 + tan^2)
  =  (N_quark - 1) / (N_quark^2 + N_quark - 1)
  =  5/41,

cos^2(omega_bar | LO)
  =  1 / (1 + tan^2)
  =  N_quark^2 / (N_quark^2 + N_quark - 1)
  =  36/41.
```

The denominator structure `N_quark^2 + N_quark - 1` is the forced
combination produced by `1 + tan^2(omega_bar | LO)` once
`tan^2(omega_bar | LO) = (N_quark - 1)/N_quark^2` is substituted; it
is not a separate retained quantity.

### B6: Brocard inequality on the retained surface

The classical Brocard bound `omega <= pi/6` is equivalent to
`cot(omega) >= sqrt(3)`, i.e.

```text
(alpha_s^2 - 4 alpha_s + 96)^2  >=  48 sqrt(5)^2 (4 - alpha_s)^2
                                  =  240 (4 - alpha_s)^2.
```

The polynomial

```text
P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2  -  240 (4 - alpha_s)^2
```

is strictly positive on the physically relevant range. The runner
sweeps `alpha_s ∈ {0, 0.05, 0.1, 0.118, 0.15, 0.2, 0.3, 0.5, 1, 2, 3, 3.5, 3.9}`
and confirms `cot(omega_bar) >= sqrt(3)` throughout. (At `alpha_s = 0`
the LHS is `96^2 = 9216` and the RHS is `240 * 16 = 3840`, with
`P(0) = 5376 > 0`.)

### B7: cot-sum identity

The angles of the barred unitarity triangle are
`(alpha_bar, beta_bar, gamma_bar)`, summing to `pi`. The classical
identity

```text
cot(omega)  =  cot(alpha) + cot(beta) + cot(gamma)
```

holds for any triangle. Substituting the retained closed forms

```text
cot(gamma_bar)  =  1 / sqrt(5),
cot(beta_bar)   =  (1 - rho_bar) / eta_bar  =  (20 + alpha_s) / (sqrt(5)(4 - alpha_s)),
cot(alpha_bar)  =  -cot(gamma_bar + beta_bar),
```

and simplifying gives `cot(alpha_bar) + cot(beta_bar) + cot(gamma_bar)`
identically equal to the B2 closed form. The runner verifies
`sympy.simplify(cot_sum - cot_omega) == 0` on the symbolic surface.

### B8: Brocard - Jarlskog identity

The Jarlskog invariant in the barred Wolfenstein plane (with the unit
base normalized) equals twice the triangle area:

```text
J_bar (normalized)  =  2 * Area  =  eta_bar.
```

Combining with B2 and B1 gives

```text
2 J_bar  =  4 * Area  =  (a^2 + b^2 + c^2) * tan(omega_bar).
```

In closed forms:

```text
(a^2 + b^2 + c^2) * tan(omega_bar)
   =  [(alpha_s^2 - 4 alpha_s + 96)/48]
       *  [4 sqrt(5) (4 - alpha_s) / (alpha_s^2 - 4 alpha_s + 96)]
   =  sqrt(5) (4 - alpha_s) / 12
   =  2 * sqrt(5) (4 - alpha_s) / 24
   =  2 eta_bar
   =  2 J_bar.
```

This packages the Brocard angle and the Jarlskog (the sole CP-violating
combination of CKM elements) into a single algebraic identity in the
barred plane.

## Numerical Verification

All identities verified to **exact symbolic algebra** via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| B1 a²+b²+c² | `(α_s² - 4α_s + 96)/48` | sympy `simplify(diff) == 0` |
| B1 LO | `N_quark/N_color = 2` | `Rational(6, 3) == 2` |
| B1 structural | `(α_s² - N_pair²α_s + N_pair⁴N_quark)/(N_pair⁴N_color)` | sympy `simplify(diff) == 0` |
| B2 cot(ω̄) | `(α_s² - 4α_s + 96)/(4√5(4-α_s))` | sympy `simplify(diff) == 0` |
| B3 tan(ω̄) | `4√5(4-α_s)/(α_s² - 4α_s + 96)` | sympy `simplify(diff) == 0` |
| B3 structural | structural-integer form | sympy `simplify(diff) == 0` |
| B4 LO | `tan(ω̄\|LO) = √5/6` | sympy `simplify(diff) == 0` |
| B4 numerical | `ω̄\|LO ≈ 20.45°` | between 20.0° and 21.0° |
| B5 sin²\|LO | `5/41` | sympy `simplify(diff) == 0` |
| B5 cos²\|LO | `36/41` | sympy `simplify(diff) == 0` |
| B5 sin²+cos² | `1` | sympy `simplify(diff) == 0` |
| B6 Brocard ineq | `cot(ω̄) ≥ √3` on sweep | numerical sweep PASS |
| B7 cot-sum | `cot(α̃) + cot(β̄) + cot(γ̄) = cot(ω̄)` | sympy `simplify(diff) == 0` |
| B8 Brocard-Jarlskog | `2 J̄ = (a²+b²+c²) tan(ω̄)` | sympy `simplify(diff) == 0` |

Numerical readout at canonical sample points:

| `α_s(v)` | `tan(ω̄)` | `cot(ω̄)` | `ω̄` (deg) |
| ---: | ---: | ---: | ---: |
| 0 (LO) | 0.3727 | 2.6833 | 20.4517 |
| 0.118 (PDG-ish at M_Z) | 0.3640 | 2.7472 | 19.9907 |
| 0.30 (mid-range) | 0.3488 | 2.8673 | 19.2267 |

The Brocard angle stays in a narrow band around 20° across the
α_s range — a feature of the protected-γ̄ surface.

## Science Value

### What this lets the framework state cleanly

Previously the framework had retained closed forms for the **circumradius**
(`R̄`) and **circumcenter**, the **orthocenter** and **Euler line**, the
**apex angle** (`γ̄`), the right-angle property, and the **Jarlskog**
(`J̄`) of the barred unitarity triangle. The Brocard angle — the unique
angle `ω̄` such that there exist two distinguished interior points
(the two Brocard points) generating triple-equal-angle cevians — was
**not** previously expressed in closed form on the retained surface.

This note delivers:

1. **NEW closed form for `tan(ω̄)`** (B3): a compact rational function of
   `α_s(v)` with degree-1 numerator and degree-2 denominator. The
   structural-integer recoding shows the formula's full content in
   `(N_pair, N_color, N_quark)`.

2. **NEW LO identity `tan(ω̄|_LO) = η|_LO`** (B4): the Brocard angle of
   the unitarity triangle at LO equals the angle whose tangent is the
   Wolfenstein imaginary part. This is structurally striking because
   `ω̄` is a CP-symmetric triangle invariant (it doesn't single out any
   vertex), while `η` is the imaginary part of an apex coordinate — yet
   on the retained surface they coincide as `arctan`-conjugate angles.

3. **NEW pure structural-integer `(sin², cos²)` at LO** (B5):
   `(N_quark - 1)/(N_quark² + N_quark - 1)` and
   `N_quark²/(N_quark² + N_quark - 1)`, with a quadratic-in-`N_quark`
   denominator that is forced by the LO `tan² = (N_quark-1)/N_quark²`.

4. **NEW perimeter-squared closed form** (B1): on the protected-γ̄
   surface `a² + b² + c² = (α_s² - 4α_s + 96)/48`, which at LO collapses
   to `N_quark/N_color = 2`. This is the lattice-side of the
   Brocard formula `cot(ω) = (a²+b²+c²)/(4·Area)` and packages the
   triangle's "size" in a clean form.

5. **NEW Brocard inequality verification** (B6): the polynomial
   `(α_s² - 4α_s + 96)² - 240(4 - α_s)²` is strictly positive on the
   physical α_s range, certifying `ω̄ ≤ π/6` (the maximum, attained
   only at equilateral triangles).

6. **NEW Brocard - Jarlskog identity** (B8): in the barred plane,
   `2 J̄ = (a² + b² + c²) tan(ω̄)`. The Jarlskog (CP-violation invariant)
   factors into a "size" piece (perimeter²) and a "shape" piece (Brocard
   tangent). This separates the CP-violation magnitude from the
   triangle's degree-of-equilaterality on the retained surface.

### Why this counts as pushing the science forward

The Brocard angle is a classical triangle invariant that has not
previously appeared in CKM unitarity-triangle physics. As a derived
quantity of the protected-γ̄ surface it is:

- **Geometrically primary**: `ω̄` together with the side ratios encodes
  the triangle's shape up to similarity. Combined with `R̄`
  (already retained) it fixes the triangle's size and shape.
- **CP-symmetric**: invariant under permutations of the three vertices,
  so it doesn't privilege any one of `(α̃, β̄, γ̄)`. This makes it a
  natural "shape parameter" for the CKM triangle complementing the
  vertex-specific angles.
- **Bounded by `π/6`** with equality at equilateral. The actual value
  `ω̄ ≈ 20°` is large compared to `0` (degenerate, no CP violation)
  but well below `30°` (equilateral), so the unitarity triangle has
  a definite handedness inherited from the apex coordinate
  `(rho_bar, eta_bar) = (rho, eta)(1 - lambda²/2)`.
- **Tied to the Jarlskog** through B8: the product
  `(a² + b² + c²) tan(ω̄) = 2 J̄` reframes CP violation in the
  unitarity triangle as a shape-size factorization.

### Falsifiable structural claim

The closure (B3, B4, B5) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES_STRUCTURAL_COUNTS (N_pair = 2, N_color = 3, N_quark = 6)
forces
  tan(omega_bar | LO)  =  sqrt(5)/6  =  eta | LO.
```

Any framework revision moving `(rho, eta) = (1/6, sqrt(5)/6)` off the
retained protected-γ̄ surface would break the Brocard - eta identity at
LO. The B5 structural-integer `(sin², cos²)` at LO is also rigid:
shifting `N_quark` would shift both numerator and the
`N_quark² + N_quark - 1` denominator by structurally distinct amounts.

## What This Claims

- `(B1)`: NEW retained closed form `a² + b² + c² = (α_s² - 4α_s + 96)/48`.
- `(B2)`: NEW retained closed form for `cot(ω̄)`.
- `(B3)`: NEW retained closed form for `tan(ω̄)`.
- `(B4)`: NEW retained LO identity `tan(ω̄|_LO) = η|_LO = √5/6`.
- `(B5)`: NEW retained structural-integer `sin²(ω̄|_LO) = 5/41`,
  `cos²(ω̄|_LO) = 36/41`.
- `(B6)`: NEW verification of the Brocard inequality
  `cot(ω̄) ≥ √3` on the retained surface.
- `(B7)`: independent recovery of `cot(ω̄)` via the classical cot-sum
  identity `cot(α̃) + cot(β̄) + cot(γ̄)`.
- `(B8)`: NEW Brocard - Jarlskog identity
  `2 J̄ (normalized) = (a² + b² + c²) tan(ω̄)` in the barred plane.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches.
- Does **not** claim `ω̄` as a directly measured CKM observable; the
  Brocard angle is a derived geometric invariant of the barred
  triangle, computed from the retained `(rho_bar, eta_bar)` and the
  retained vertex layout.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs and the closed forms
  are forced consequences.
- Does **not** depend on any α_s-running pipeline; all results live on
  the protected-γ̄ surface at canonical `α_s(v)`.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_brocard_angle_exact_closed_form.py
```

Expected:

```text
TOTAL: PASS=32, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts the retained inputs (`rho_bar`, `eta_bar`,
  `tan(gamma_bar)`, `tan(beta_bar)`, LO `(rho, eta)`, `N_pair`,
  `N_color`, `N_quark`) by direct text matching.
- Computes B1–B8 symbolically via sympy at the retained values and
  asserts each closed form by `simplify(diff) == 0`.
- Sweeps `α_s` to numerically certify the Brocard inequality.
- Reports a numerical readout at canonical α_s sample points.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)`, `tan(gamma_bar) = sqrt(5)`, `tan(beta_bar)` closed form.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  — atlas vertex layout, `alpha_LO = pi/2`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  — `lambda^2 = alpha_s/N_pair`, `A^2 = N_pair/N_color`.

**Companion retained barred-triangle closed forms (not load-bearing here, but
part of the same surface):**

- [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — `R̄`, circumcenter coordinates.
- [`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — apex angle `γ̄` closed form.
- [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — orthocenter and Euler line.
- [`CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md)
  — Pythagorean / sum-rule structure.
- [`CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — `J̄` closed form (used in B8).

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
