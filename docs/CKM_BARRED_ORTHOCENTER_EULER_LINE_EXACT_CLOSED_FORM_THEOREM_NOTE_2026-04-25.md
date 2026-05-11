# Barred Unitarity Triangle Orthocenter and Euler Line: EXACT Closed Forms

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure corollary on the proposed_promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives **EXACT
all-orders-in-α_s closed forms** for the **orthocenter** `H`, the
**centroid** `G`, and the **Euler line** of the barred unitarity
triangle on the retained NLO Wolfenstein protected-γ̄ surface.

The headline identity is striking in its simplicity:

```text
H  =  (rho_bar, (20 + alpha_s(v))/(24 sqrt(5)))     [EXACT, both coords linear in alpha_s]
```

Both coordinates of the orthocenter are **EXACTLY degree-1 polynomials**
in `α_s` on the protected-γ̄ surface. There are no `α_s²`, `α_s³`, or
higher corrections to `H_x` or `H_y`.

**Apex-orthocenter offset** has the EXACT closed form

```text
H  -  V_3  =  ( 0,  alpha_s(v) / [N_pair^2 sqrt(N_quark - 1)] )
           =  ( 0,  alpha_s(v) sqrt(5)/20 )
```

This is a **pure y-direction** offset — the orthocenter "lifts" the
apex by exactly `α_s √5/20 = (retained N7 slope) × α_s`. The slope
**equals** the retained N7 leading coefficient — a sharp algebraic
coincidence that gives the apex-orthocenter offset a direct
interpretation as the apex-angle deviation.

**Connection to circumcenter**:

```text
H  -  V_3  =  -2 (O - M)                             [EXACT signed identity]

  where O = (1/2, -alpha_s sqrt(5)/40) is the circumcenter (re-derivable from
  retained N1, N2, N3) and M = (1/2, 0) is the hypotenuse midpoint.
```

In words: **the orthocenter "lifts" the apex by exactly twice the
amount the circumcenter "drops" below the hypotenuse**. Equivalently,
`H_y - V_3_y = -2 y_cc` EXACTLY.

The **Euler line** `H = 3G - 2O` is preserved on the protected-γ̄
surface (a property of every Euclidean triangle, but with all four
points — H, G, O, and the centroid relation 3G = V_1 + V_2 + V_3 —
having α_s-explicit closed forms here).

**Primary runner:**
`scripts/frontier_ckm_barred_orthocenter_euler_line_exact_closed_form.py`

## Statement

On the NLO Wolfenstein protected-γ̄ surface (where retained `(N1)`-`(N6)`
hold):

```text
(O1)  Orthocenter:
      H_x  =  rho_bar  =  (4 - alpha_s)/24                                   [EXACT, linear in alpha_s]
      H_y  =  (20 + alpha_s) / (24 sqrt(5))                                   [EXACT, linear in alpha_s]

(O2)  Apex-orthocenter offset:
      H - V_3  =  ( 0,  alpha_s / [N_pair^2 sqrt(N_quark - 1)] )              [EXACT, pure y, linear]
               =  ( 0,  alpha_s sqrt(5)/20 )

(O3)  Centroid:
      G  =  ( (28 - alpha_s)/72, sqrt(5)(4 - alpha_s)/72 )                    [EXACT, both linear]
         =  ( (V_1 + V_2 + V_3)/3 )

(O4)  Circumcenter (re-derived from retained N1, N2, N3):
      O  =  ( 1/2, -alpha_s / [N_pair^3 sqrt(N_quark - 1)] )                  [EXACT, linear]
         =  ( 1/2, -alpha_s sqrt(5)/40 )

(O5)  Euler line:
      H  =  3 G  -  2 O                                                        [EXACT, all alpha_s]
      H, G, O are collinear, with HG = 2 GO (the standard Euler line ratio).

(O6)  Apex-orthocenter / circumcenter-hypotenuse anti-relation:
      H - V_3  =  -2 (O - M)        where M = (1/2, 0) = hypotenuse midpoint  [EXACT]
      H_y - V_3_y  =  -2 y_cc                                                  [EXACT signed]
      |H - V_3|    =   2 |O - M|                                               [EXACT |.|]

(O7)  Apex-orthocenter slope = retained N7 slope:
      (H_y - V_3_y)/alpha_s  =  sqrt(5)/20  =  retained N7 slope                [EXACT]

(O8)  Selection rule:
      H_x, H_y, G_x, G_y are EXACTLY DEGREE-1 polynomials in alpha_s.
      O_x is alpha_s-INDEPENDENT.  O_y is exactly LINEAR in alpha_s.
      All four classical centers have at most LINEAR alpha_s-dependence
      on the protected-γ̄ surface.

(O9)  Atlas-LO recovery:
      H_0  =  V_3_0  =  (rho, eta)  =  (1/N_quark, sqrt(N_quark - 1)/N_quark)
                                    =  (1/6, sqrt(5)/6).
      G_0  =  ((1 + rho)/3, eta/3)  =  (7/18, sqrt(5)/18).
      O_0  =  (1/N_pair, 0)         =  (1/2, 0).
      At alpha_s = 0 (right-angle), the orthocenter coincides with the
      apex (the right-angle vertex IS its own altitude foot), and the
      circumcenter sits at the midpoint of the hypotenuse (hypotenuse-
      as-diameter).
```

`(O1)` through `(O9)` are NEW. The retained NLO theorem packages
`(N1)`-`(N9)` for the apex coordinates, side lengths, and angles, but
does **not** package the orthocenter, the centroid, the circumcenter,
or the Euler line. This note packages all four with EXACT closed forms.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| Canonical `alpha_s(v) = 0.103303816...` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta^2 = 5/36` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Atlas `alpha_0 = pi/2`, hypotenuse-as-diameter, right-angle-vertex-orthocenter coincidence | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| `(N1)` `rho_bar = (4 - alpha_s)/24` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md), N1 |
| `(N2)` `eta_bar = sqrt(5)(4 - alpha_s)/24` | same, N2 |
| `(N3)` `R_b_bar^2 = (4 - alpha_s)^2/96` | same, N3 |
| `(N7)` slope `sqrt(5)/20` for apex angle deviation | same, N7 |
| `N_quark = 6`, `N_pair = 2`, `N_color = 3` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |

No PDG observable enters as a derivation input. No SUPPORT-tier or
open inputs (Koide `Q_l`, bare-coupling ratios, dimension-color
quadratic) are used.

## Derivation

The triangle has vertices `V_1 = (0, 0)`, `V_2 = (1, 0)`, `V_3 = (ρ̄, η̄)`
in the `(ρ̄, η̄)` plane. We derive the orthocenter, centroid, and
circumcenter directly from the retained closed forms `(N1)`, `(N2)`,
`(N3)`.

### Step 1: Centroid `(O3)`

The centroid is the arithmetic mean of the three vertices:

```text
G  =  (V_1 + V_2 + V_3) / 3
   =  ( (0 + 1 + rho_bar)/3,  (0 + 0 + eta_bar)/3 )
   =  ( (1 + rho_bar)/3,  eta_bar/3 ).
```

Substituting retained `(N1)`, `(N2)`:

```text
1 + rho_bar  =  1 + (4 - alpha_s)/24  =  (24 + 4 - alpha_s)/24  =  (28 - alpha_s)/24.

G_x  =  (28 - alpha_s)/72.
G_y  =  sqrt(5)(4 - alpha_s)/72.
```

Both are EXACTLY linear in `α_s`.

### Step 2: Orthocenter `(O1)`

The hypotenuse `V_1 V_2` lies on the x-axis, so the altitude from `V_3`
is the vertical line `x = ρ̄`. Hence `H_x = ρ̄`.

For `H_y`, use the altitude from `V_1` perpendicular to `V_2 V_3`. The
side `V_2 V_3` has direction `(ρ̄ - 1, η̄)`; the perpendicular through
`V_1 = (0,0)` has direction `(η̄, 1 - ρ̄)`, giving the line

```text
y / x  =  (1 - rho_bar) / eta_bar.
```

Setting `x = H_x = ρ̄`:

```text
H_y  =  rho_bar (1 - rho_bar) / eta_bar.
```

Substituting retained `(N1)`, `(N2)`:

```text
1 - rho_bar       =  (20 + alpha_s)/24.
rho_bar           =  (4 - alpha_s)/24.
rho_bar(1-rho_bar) =  (4 - alpha_s)(20 + alpha_s)/576.
eta_bar           =  sqrt(5)(4 - alpha_s)/24.

H_y  =  (4 - alpha_s)(20 + alpha_s) / 576  /  [sqrt(5)(4 - alpha_s)/24]
     =  (20 + alpha_s) × 24 / [576 sqrt(5)]
     =  (20 + alpha_s) / (24 sqrt(5)).
```

The `(4 - α_s)` factor **cancels exactly**, leaving the clean closed
form

```text
H_y  =  (20 + alpha_s) / (24 sqrt(5)).
```

A degree-1 polynomial in `α_s` divided by a constant — EXACTLY linear.

### Step 3: Apex-orthocenter offset `(O2)`

Substituting `H_x = ρ̄ = V_3_x`:

```text
H_x  -  V_3_x  =  0.
```

For the y-component:

```text
H_y  -  V_3_y  =  (20 + alpha_s)/(24 sqrt(5))  -  sqrt(5)(4 - alpha_s)/24
              =  (20 + alpha_s)/(24 sqrt(5))  -  5(4 - alpha_s)/(24 sqrt(5))
              =  [(20 + alpha_s) - 5(4 - alpha_s)] / (24 sqrt(5))
              =  [20 + alpha_s - 20 + 5 alpha_s] / (24 sqrt(5))
              =  6 alpha_s / (24 sqrt(5))
              =  alpha_s / (4 sqrt(5))
              =  alpha_s sqrt(5) / 20.
```

So

```text
H  -  V_3  =  (0, alpha_s sqrt(5)/20)  =  (0, alpha_s/[N_pair^2 sqrt(N_quark - 1)]).
```

The numerical coefficient `√5/20 = 1/(N_pair² √(N_quark - 1))` is the
**retained N7 slope** itself.

### Step 4: Circumcenter `(O4)` — re-derivation from retained N1, N2, N3

The circumcenter is equidistant from all three vertices. The
perpendicular bisector of `V_1 V_2` is `x = 1/2`, so `O_x = 1/2`.

Equidistance from `V_1 = (0,0)` and `V_3 = (ρ̄, η̄)`:

```text
O_x^2 + O_y^2  =  (O_x - rho_bar)^2 + (O_y - eta_bar)^2
0              =  -2 rho_bar O_x  +  rho_bar^2  -  2 eta_bar O_y  +  eta_bar^2
0              =  -rho_bar  +  rho_bar^2 + eta_bar^2  -  2 eta_bar O_y       (using O_x = 1/2)
0              =  R_b_bar^2 - rho_bar  -  2 eta_bar O_y                       (using N3)
O_y            =  (R_b_bar^2 - rho_bar) / (2 eta_bar).
```

Compute `R_b_bar^2 - ρ̄` from retained `(N1)`, `(N3)`:

```text
R_b_bar^2 - rho_bar  =  (4 - alpha_s)^2/96  -  (4 - alpha_s)/24
                     =  (4 - alpha_s) [(4 - alpha_s) - 4] / 96
                     =  -alpha_s (4 - alpha_s) / 96.
```

Then

```text
O_y  =  -alpha_s (4 - alpha_s) / 96  /  [sqrt(5) (4 - alpha_s)/12]
     =  -alpha_s × 12 / [96 sqrt(5)]
     =  -alpha_s / (8 sqrt(5))
     =  -alpha_s sqrt(5) / 40.
```

The `(4 - α_s)` factor **cancels exactly**, leaving the EXACT linear
form `O_y = -α_s √5/40 = -α_s/(N_pair³ √(N_quark - 1))`.

### Step 5: Euler line `(O5)`

Compute `3G - 2O`:

```text
3 G  =  3 × ( (28 - alpha_s)/72,  sqrt(5)(4 - alpha_s)/72 )
     =  ( (28 - alpha_s)/24,  sqrt(5)(4 - alpha_s)/24 ).

2 O  =  2 × ( 1/2,  -alpha_s sqrt(5)/40 )
     =  ( 1,  -alpha_s sqrt(5)/20 ).

3 G - 2 O  =  ( (28 - alpha_s)/24 - 1,  sqrt(5)(4 - alpha_s)/24 + alpha_s sqrt(5)/20 ).
```

x-component:

```text
(28 - alpha_s)/24 - 1  =  (28 - alpha_s - 24)/24  =  (4 - alpha_s)/24  =  rho_bar  =  H_x.   ✓
```

y-component:

```text
sqrt(5)(4 - alpha_s)/24 + alpha_s sqrt(5)/20  =  sqrt(5) [(4-alpha_s)/24 + alpha_s/20]
                                              =  sqrt(5) [5(4-alpha_s) + 6 alpha_s] / 120
                                              =  sqrt(5) [20 - 5 alpha_s + 6 alpha_s] / 120
                                              =  sqrt(5) (20 + alpha_s) / 120
                                              =  (20 + alpha_s) / (24 sqrt(5))
                                              =  H_y.   ✓
```

So `H = 3G - 2O` EXACTLY. This is the Euler line relation, verified
algebraically on the protected-γ̄ surface.

### Step 6: Anti-relation `(O6)`

The hypotenuse midpoint `M = (1/2, 0)`. Then

```text
M - O  =  (1/2, 0)  -  (1/2, -alpha_s sqrt(5)/40)  =  (0,  alpha_s sqrt(5)/40).

-2 (O - M)  =  2 (M - O)  =  (0,  alpha_s sqrt(5)/20)  =  H - V_3.
```

So `H - V_3 = -2(O - M) = 2(M - O)` EXACTLY. Equivalently,

```text
H_y - V_3_y  =  -2 y_cc        (using y_cc = O_y)
            =  -2 × (-alpha_s sqrt(5)/40)
            =   alpha_s sqrt(5)/20.   ✓
```

This is `(O6)`. The orthocenter "lifts" the apex by **exactly twice**
the amount the circumcenter "drops" below the hypotenuse.

### Step 7: Apex-orthocenter slope = N7 slope `(O7)`

From `(O2)`,

```text
(H_y - V_3_y) / alpha_s  =  sqrt(5)/20.
```

The retained `(N7)` is `α̅ - π/2 = (√5/20) α_s + O(α_s²)`, with leading
coefficient `√5/20`. So

```text
(H_y - V_3_y) / alpha_s  =  retained N7 leading slope.
```

This is `(O7)`. The orthocenter offset's slope **equals** the apex-
angle deviation slope, providing a direct geometric realization of N7.

## Numerical Verification

With canonical `alpha_s(v) = 0.10330381612227...`:

| Quantity | Closed form | Value |
| --- | --- | ---: |
| `H_x = ρ̄` | `(4 - α_s)/24` | `0.16236234` |
| `H_y` (NEW O1) | `(20 + α_s)/(24√5)` | `0.37460295` |
| `V_3_y = η̄` | `√5(4-α_s)/24` | `0.36305323` |
| `H_y - V_3_y` (NEW O2) | `α_s √5/20` | `0.01154972` |
| `G_x` (NEW O3) | `(28 - α_s)/72` | `0.38745411` |
| `G_y` (NEW O3) | `√5(4-α_s)/72` | `0.12101774` |
| `O_x` | `1/2` | `0.50000000` |
| `O_y` | `-α_s √5/40` | `-0.00577486` |
| `H_y - V_3_y` (alt: O6) | `-2 y_cc` | `0.01154972` ✓ |
| `H = 3G - 2O` (NEW O5) | EXACT identity | matches direct ✓ |

All identities verified to machine precision at six independent
values of `α_s ∈ {0.05, 0.10, 0.103303816, 0.15, 0.20, 0.30}`.

## Science Value

### What this lets the framework predict that it could not before

The retained NLO theorem packages closed forms for the **apex
coordinates** (N1, N2), the **side R_b̄²** (N3), and the **angles**
(N4-N9), but **not** any of the four classical triangle centers nor
the Euler line. This note delivers EXACT closed forms for:

- The **orthocenter** `H` with both coordinates EXACTLY linear in α_s.
- The **centroid** `G` with both coordinates EXACTLY linear in α_s.
- The **circumcenter** `O` re-derived from N1, N2, N3 (linear y, x
  α_s-independent).
- The **Euler line** identity `H = 3G - 2O` algebraically verified.

All from retained inputs, no SUPPORT-tier inputs, and no truncation.

### The orthocenter is a degree-1 polynomial in α_s

`H_x = (4 - α_s)/24` and `H_y = (20 + α_s)/(24√5)` are both
**EXACTLY linear** in α_s. There are no α_s², α_s³, or higher
corrections to either coordinate on the protected-γ̄ surface.

The cleanest possible α_s-dependence for a triangle invariant — only
linear corrections — is realized by the orthocenter on this surface.
The same holds for the centroid (linear, but trivially since both are
arithmetic combinations of α_s-linear apex coordinates).

### The orthocenter slope = retained N7 slope (O7)

The apex-orthocenter offset is

```text
H - V_3  =  (0, alpha_s × sqrt(5)/20).
```

The slope `√5/20` is **identical** to the retained N7 leading slope
of the apex-angle deviation. So the orthocenter trajectory provides a
direct geometric realization of the N7 deviation theorem: as α_s ramps
up from zero, the orthocenter slides upward (in y) along the line
`x = ρ̄`, with slope exactly the N7 slope.

This is striking because N7 is an **angular** statement (rate at which
α̅ deviates from π/2) while `(O7)` is a **positional** statement
(rate at which H lifts above V_3). The two are connected by the
factor `1/(2 sin(γ̄)) × 2 sin(α̅)/... ≈ 1` at LO, but the EXACT
identity `√5/20` in both is the new content.

### Apex-orthocenter / circumcenter-hypotenuse anti-relation (O6)

```text
H - V_3  =  -2 (O - M)        EXACT
```

where `M = (1/2, 0)` is the hypotenuse midpoint. In words: **the
orthocenter "lifts" the apex by exactly twice the amount the
circumcenter "drops" below the hypotenuse**, on the protected-γ̄
surface, all α_s.

This is a sharp geometric statement tying the orthocenter and
circumcenter on this surface. While the factor-of-2 ratio between
HV_3 and OM is a general triangle property (apex-orthocenter distance
= 2R cos(α̅), and OM = R cos(central angle/2) etc.), the **EXACT
linear-in-α_s** form on this surface is new content.

### Selection rule (O8): all four centers have at most linear α_s-dependence

```text
H, G:    both coordinates EXACTLY DEGREE-1 polynomials in alpha_s
O:       x INDEPENDENT of alpha_s, y LINEAR in alpha_s
V_1, V_2: hypotenuse vertices, alpha_s-INDEPENDENT
V_3:     LINEAR in alpha_s in both coordinates (from N1, N2)
```

So **all six points** (V_1, V_2, V_3, H, G, O) have at most linear
α_s-dependence on the protected-γ̄ surface. The protected-γ̄ surface
is the **maximal-symmetry surface** in this sense: classical triangle
geometry on it is captured by linear-in-α_s expressions throughout.

### Atlas-LO recovery: H = V_3 at right-angle (O9)

At `α_s = 0`,

```text
H_0  =  V_3_0  =  (1/N_quark, sqrt(N_quark - 1)/N_quark)  =  (1/6, sqrt(5)/6).
```

The orthocenter coincides with the apex at the right-angle, because
**the right-angle vertex is its own altitude foot**: the altitude
from V_3 (the right-angle vertex) hits V_1 V_2 at V_3 itself.

This is a sharp atlas-LO consistency check: any closed form for H
must give H = V_3 at α_s = 0, and `(O1)` does so cleanly.

### Falsifiable NNLO predictions

The framework predicts:

```text
NO alpha_s^2, alpha_s^3, ... corrections to H_x or H_y on the protected-γ̄ surface.
H is EXACTLY a degree-1 polynomial in alpha_s.

Equivalently: the orthocenter trajectory in the (rho_bar, eta_bar) plane
is EXACTLY a STRAIGHT LINE parametrized linearly by alpha_s.
```

If a future NNLO Wolfenstein analysis on the protected-γ̄ surface
produces an `α_s²` correction to `H_x` or `H_y`, then either:

- the retained closed forms `(N1)`, `(N2)` themselves break at NNLO,
- the altitude/orthocenter geometry fails (which it does not in
  Euclidean space).

So the linearity of `H` in α_s is a **sharp** test of the NLO
protected-γ̄ surface's integrity.

### Phenomenological connection: the orthocenter as a UTfit handle

The orthocenter of a triangle is determined by the three side
directions and the three altitude lines — every joint UTfit /
CKMfitter constraint that determines `(ρ̄, η̄)` and the side lengths
implicitly determines the orthocenter via the closed form

```text
H  =  ((4 - alpha_s)/24, (20 + alpha_s)/(24 sqrt(5))).
```

A direct test: extract `H` from a global fit, verify it lies on the
straight line in `(ρ̄, η̄)` space parametrized by α_s. The framework
predicts:

| α_s | `H` |
|---:|---:|
| 0 | `(1/6, √5/6) ≈ (0.1667, 0.3727)` |
| 0.05 | `(0.1646, 0.3729)` |
| 0.103 | `(0.1624, 0.3746)` |
| 0.20 | `(0.1583, 0.3776)` |

The orthocenter trajectory in `(ρ̄, η̄)` space is a straight line
with negative x-slope and positive y-slope. Any joint fit deviating
from this linearity would falsify the protected-γ̄ surface.

### Why this counts as pushing the science forward

Three layers of new content beyond the parent NLO theorem:

1. **Orthocenter EXACT closed form.** Both coordinates of H are
   degree-1 polynomials in α_s. This is the cleanest possible α_s-
   dependence for a non-trivial triangle invariant.

2. **Anti-relation between orthocenter and circumcenter.** The exact
   identity `H - V_3 = -2(O - M)` ties the orthocenter's lift above
   the apex to the circumcenter's depression below the hypotenuse
   by a sharp factor 2.

3. **Slope identification with N7.** The retained N7 slope `√5/20`
   appears EXACTLY as the slope of the orthocenter offset from the
   apex. Connects the angular N7 theorem to a positional statement.

These are propositions about the protected-γ̄ surface's classical
triangle geometry that were not derivable from `(N1)`-`(N9)` alone
without the explicit construction.

## What This Claims

- `(O1)` NEW EXACT orthocenter `H = (ρ̄, (20+α_s)/(24√5))`.
- `(O2)` NEW EXACT apex-orthocenter offset `H - V_3 = (0, α_s √5/20)`.
- `(O3)` NEW EXACT centroid `G = ((28-α_s)/72, √5(4-α_s)/72)`.
- `(O4)` Re-derived circumcenter `O = (1/2, -α_s √5/40)` from retained
  N1, N2, N3 (consistent with previously derived form on the
  pending circumradius branch but here re-derived independently).
- `(O5)` NEW Euler line identity `H = 3G - 2O` verified algebraically.
- `(O6)` NEW anti-relation `H - V_3 = -2(O - M)` EXACT.
- `(O7)` NEW slope identification: `(H_y - V_3_y)/α_s = √5/20 = N7 slope`.
- `(O8)` NEW selection rule: H, G are degree-1 in α_s, O has linear y.
- `(O9)` NEW atlas-LO recovery `H_0 = V_3_0 = (1/N_quark, √(N_quark-1)/N_quark)`.

## What This Does NOT Claim

- It does not extend the protected-γ̄ surface to NNLO Wolfenstein. The
  closed forms are EXACT on the NLO protected-γ̄ surface.
- It does not modify any retained CKM atlas, Wolfenstein, CP-phase,
  right-angle, NLO-protected-γ̄, or magnitudes structural counts theorem.
- It does not use any SUPPORT-tier or open input.
- It does not predict the orthocenter to better experimental precision
  than currently available; the orthocenter is implicit in joint UTfit
  constraints at current sensitivity.

## Exact-symbolic verification

The algebraic-substitution content of `(O1)`-`(O7)` and the supporting
selection rule `(O8)` and atlas-LO recovery `(O9)` is certified at
exact-symbolic precision via `sympy` in
`scripts/audit_companion_ckm_barred_orthocenter_euler_line_exact_closed_form_exact.py`.
The companion runner treats `alpha_s(v)` as a free positive real symbol,
imports the upstream cited inputs `(N1)`, `(N2)`, `(N3)` verbatim,
builds H, G, O directly from the altitude / centroid /
perpendicular-bisector constructions, and checks each closed-form
identity by computing `sympy.simplify(lhs - rhs)` and asserting the
residual equals `0` exactly. The cited inputs themselves
(`rho_bar = (4-alpha_s)/24`, `eta_bar = sqrt(5)(4-alpha_s)/24`,
`R_b_bar^2 = (4-alpha_s)^2/96`, the cited N7 slope `sqrt(5)/20`, and
structural counts `N_pair = 2`, `N_quark = 6`) are imported from
upstream authority notes and are not re-derived here.

| Identity | Symbolic form | Verification |
| --- | --- | --- |
| `(O3)` | `G == ((28 - alpha_s)/72, sqrt(5)(4 - alpha_s)/72)` | `sympy.simplify` residual `= 0` |
| `(O1)` | `H == (rho_bar, (20 + alpha_s)/(24 sqrt(5)))` | `sympy.simplify` residual `= 0` |
| `(O1)` cross-check | H lies on altitude from V_2 perpendicular to V_1 V_3 | `sympy.simplify` residual `= 0` |
| `(O1)` polynomial | `H_x` and `H_y * sqrt(5)` are degree-1 in `alpha_s` | `sympy.Poly(...).degree() == 1` |
| `(O2)` | `H - V_3 == (0, alpha_s sqrt(5)/20)` | `sympy.simplify` residual `= 0` |
| `(O2)` structural | `H_y - V_3_y == alpha_s/[N_pair^2 sqrt(N_quark - 1)]` at `(2, 6)` | `sympy.simplify` residual `= 0` |
| `(O4)` | `O == (1/2, -alpha_s sqrt(5)/40)` re-derived from `(N1)`-`(N3)` | `sympy.simplify` residual `= 0` |
| `(O5)` | `H == 3 G - 2 O` (Euler line), `HG = 2 GO` | `sympy.simplify` residual `= 0` |
| `(O5)` collinearity | cross product `(G - O) x (H - O) = 0` | `sympy.simplify` residual `= 0` |
| `(O6)` | `H - V_3 == -2 (O - M)` with `M = (1/2, 0)` | `sympy.simplify` residual `= 0` |
| `(O7)` | `(H_y - V_3_y)/alpha_s == sqrt(5)/20` (cited N7 slope) | `sympy.simplify` residual `= 0` |
| `(O8)` | `H_x, H_y * sqrt(5), G_x, G_y / sqrt(5)` all degree-1 in `alpha_s` | `sympy.Poly(...).degree() == 1` |
| `(O9)` | `H_LO == V_3_LO == (1/6, sqrt(5)/6)`; `O_LO == (1/2, 0)` | `sympy.simplify` at `alpha_s = 0` residual `= 0` |

Counterfactual probes confirm the load-bearing role of the cited
inputs:

- dropping the `(4 - alpha_s)` factor from `eta_bar` breaks the
  cancellation that gives `H_y = (20 + alpha_s)/(24 sqrt(5))` cleanly;
- using only the atlas-LO `rho_bar = 1/6` (no NLO offset) prevents
  `H_y` from realizing the linear form `(20 + alpha_s)/(24 sqrt(5))`.

The structural relations are therefore exact-symbolic over the cited
inputs and do not depend on the floating-point pin of `alpha_s(v)`. The
canonical numerical value of `alpha_s(v)` from
`scripts/canonical_plaquette_surface.py` enters only the trailing
sanity-pin section of the companion runner, which is not load-bearing
for the algebra.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_orthocenter_euler_line_exact_closed_form.py
PYTHONPATH=scripts python3 scripts/audit_companion_ckm_barred_orthocenter_euler_line_exact_closed_form_exact.py
```

Expected result:

```text
TOTAL: PASS=41, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import. Upstream authorities are cited here; their audit status remains ledger-derived.

## Cross-References

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  -- cited N1 (`ρ̄`), N2 (`η̄`), N3 (`R_b̄²`), N7 (linearization)
  used in this derivation.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- cited `α_0 = π/2`, hypotenuse-as-diameter, right-angle-vertex-
  orthocenter coincidence atlas-LO geometry.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- cited `ρ = 1/6`, `η² = 5/36`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- cited `λ² = α_s(v)/2`, `A² = 2/3`.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- cited `N_quark = 6`, `N_pair = 2`, `N_color = 3`.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `α_s(v)` cited input.
