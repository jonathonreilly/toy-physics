# Barred Unitarity-Triangle Orthic Triangle: EXACT Closed Form Theorem

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives the
**EXACT closed forms** for the **orthic triangle** of the barred
unitarity triangle — the triangle whose vertices are the three
altitude feet `(H_a, H_b, H_c)` — including its sides, area, and a
**STRIKING LO DEGENERACY** where two of the three orthic vertices
coincide, forcing the orthic triangle to collapse to a line segment
exactly when the original triangle has its right angle at the apex.

The headline closed forms:

```text
(O2)  Orthic vertices:
        H_a  =  (5(4 - alpha_s)^2/(6(80 + alpha_s^2)),
                 sqrt(5)(4 - alpha_s)(20 + alpha_s)/(6(80 + alpha_s^2))),
        H_b  =  (1/6, sqrt(5)/6)                          [alpha_s-INVARIANT],
        H_c  =  ((4 - alpha_s)/24, 0).

(O3)  Orthic side-length squares:
        |H_b H_c|^2  =  (80 + alpha_s^2)/576       =  a^2 cos^2(gamma_bar),
        |H_a H_c|^2  =  (4 - alpha_s)^2 (20 + alpha_s)^2 / (576 (80 + alpha_s^2))
                                                    =  b^2 cos^2(beta_bar),
        |H_a H_b|^2  =  alpha_s^2/(80 + alpha_s^2)  =  c^2 cos^2(alpha_bar).

(O4)  Orthic area (clean closed form):
        Area_orthic  =  sqrt(5) alpha_s (4 - alpha_s)(20 + alpha_s)
                        / (144 (80 + alpha_s^2)).

(O5)  STRIKING LO DEGENERACY:
        At alpha_s = 0 (LO right-angle theorem alpha_LO = pi/2):
          H_a | LO  =  H_b | LO  =  V_3 | LO  =  (1/6, sqrt(5)/6).

        Two altitude feet coincide at the LO right-angle apex V_3 | LO,
        and the orthic triangle DEGENERATES (collapses to the line
        segment from V_3 | LO to H_c | LO = (1/6, 0)).
        Area_orthic | LO  =  0.

(O6)  Nine-point circle identity: orthic triangle's circumcircle =
      nine-point circle of the original unitarity triangle.

(O7)  Area-ratio closed form:
        |Area_orthic / Area_triangle|
            =  alpha_s (20 + alpha_s) / (3 (80 + alpha_s^2)).

(O8)  Second boundary degeneracy at alpha_s = 4 (where 4 - alpha_s = 0):
      the original triangle itself degenerates (V_3 -> V_1). The
      orthic closed forms extend continuously to zero area at this
      singular boundary, even though the collapsed side makes the
      literal altitude-foot construction degenerate.
```

**Primary runner:**
`scripts/frontier_ckm_barred_orthic_triangle_exact_closed_form.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface, with vertices
`V_1 = (0,0)`, `V_2 = (1,0)`, `V_3 = (rho_bar, eta_bar)` and altitude
feet `H_i` (foot of altitude from `V_i` onto the opposite side):

```text
(O1) The orthic triangle is the triangle with vertices (H_a, H_b, H_c).
     It is inscribed in the nine-point circle of the original triangle
     as the altitude-foot subtriangle. For acute triangles, the orthic angles are
     pi - 2A, pi - 2B, pi - 2C; for obtuse triangles (one angle > pi/2),
     the orthic-angle pattern is modified.

(O2) Orthic vertices:
       H_a  =  (5(4 - alpha_s)^2/(6(80 + alpha_s^2)),
                sqrt(5)(4 - alpha_s)(20 + alpha_s)/(6(80 + alpha_s^2))),
       H_b  =  (1/6, sqrt(5)/6),
       H_c  =  ((4 - alpha_s)/24, 0).

     Note: H_b is alpha_s-INVARIANT, sitting at the LO apex location
     V_3 | LO (forced by the alpha_s-protected slope tan(gamma_bar) = √5
     of line V_1 V_3).

(O3) Orthic side-length squared closed forms (using the universal
     identity |H_i H_j| = (side opposite the third vertex) × |cos angle|):

       |H_b H_c|^2  =  a^2 cos^2(gamma_bar)
                    =  (80 + alpha_s^2)/96  *  1/6
                    =  (80 + alpha_s^2)/576,

       |H_a H_c|^2  =  b^2 cos^2(beta_bar)
                    =  (4 - alpha_s)^2/96  *  (20 + alpha_s)^2/(6(80 + alpha_s^2))
                    =  (4 - alpha_s)^2 (20 + alpha_s)^2 / (576 (80 + alpha_s^2)),

       |H_a H_b|^2  =  c^2 cos^2(alpha_bar)
                    =  1  *  alpha_s^2/(80 + alpha_s^2)
                    =  alpha_s^2/(80 + alpha_s^2).

(O4) Orthic area:
       Area_orthic  =  2 |Area_triangle| |cos(alpha_bar) cos(beta_bar) cos(gamma_bar)|
                    =  sqrt(5) alpha_s (4 - alpha_s)(20 + alpha_s)
                       / (144 (80 + alpha_s^2)).

     In structural integers:
       Area_orthic
          =  sqrt(N_quark - 1) alpha_s (N_pair^2 - alpha_s) (N_pair^2(N_quark - 1) + alpha_s)
             / (N_pair^4 N_color^2 (N_pair^4 (N_quark - 1) + alpha_s^2)).

(O5) STRIKING LO DEGENERACY:
       At alpha_s = 0: H_a | LO = H_b | LO = V_3 | LO = (1/6, sqrt(5)/6).
       Area_orthic | LO = 0.

     Reason: at LO, alpha_LO = pi/2 (right angle at apex V_3, retained).
     For a right triangle with right angle at V_3:
       - Altitude from V_1 to leg V_2 V_3 lands at V_3 itself.
       - Altitude from V_2 to leg V_1 V_3 lands at V_3 itself.
     So H_a = H_b = V_3 at LO; the orthic triangle collapses to the
     line segment from V_3 | LO down to H_c | LO = (rho|LO, 0) = (1/6, 0).

(O6) Nine-point circle identity: orthic-circumcircle = nine-point circle.

     Both the original triangle's nine-point circle and the orthic
     triangle's circumcircle are the unique circle through H_a, H_b, H_c.
     Verified retained-surface algebraically: |H_i - N9|^2 = R9^2 for
     each i, where N9, R9 are the nine-point center and radius of the
     original triangle.

(O7) Area-ratio:
       |Area_orthic / Area_triangle|
          =  alpha_s (20 + alpha_s) / (3 (80 + alpha_s^2))
          =  alpha_s (N_pair^2 (N_quark - 1) + alpha_s)
             / (N_color (N_pair^4 (N_quark - 1) + alpha_s^2)).

(O8) Second boundary degeneracy at alpha_s = 4: the original triangle
     degenerates (V_3 -> V_1). The orthic closed forms have a continuous
     zero-area limit at this singular boundary; the literal altitude-foot
     construction is degenerate because the side V_1 V_3 has collapsed.
```

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `(rho_bar, eta_bar)` apex coords; `tan(γ̄) = √5` α_s-protected | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |
| `cos²(α̃)`, `sin²(α̃)` closed forms; LO right-angle `α_LO = π/2` | [`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note
is load-bearing. No unmerged branch is cited as load-bearing.

## Derivation

### O2: orthic vertices

For each vertex `V_i`, the foot of altitude `H_i` onto the opposite
side is computed via the standard projection formula. The retained
NLO Wolfenstein protected-γ̄ surface gives clean closed forms:

- `H_a` and `H_c` depend on `α_s`.
- **`H_b` is α_s-invariant** because the line `V_1 V_3` has slope
  `eta_bar/rho_bar = sqrt(5) = tan(γ̄)` which is α_s-protected on the
  retained surface. The foot of perpendicular from `V_2 = (1, 0)`
  onto a line through the origin with slope `m` is `(1/(1+m²), m/(1+m²))`
  depending only on `m`. So `H_b` is fixed at the LO apex location
  for all α_s.

### O3: orthic side lengths

For any triangle, the universal identity gives:

```text
|H_i H_j|  =  (side opposite the third vertex)  *  |cos(angle at the third vertex)|.
```

For our retained triangle:
- `|H_b H_c| = a |cos(γ̄)| = √(80+α_s²)/24` since `a = √(80+α_s²)/(4√6)` and `|cos(γ̄)| = 1/√6`.
- `|H_a H_c| = b |cos(β̄)|`.
- `|H_a H_b| = c |cos(α̃)| = α_s/√(80+α_s²)` since `c = 1` and `|cos(α̃)| = α_s/√(80+α_s²)` (retained from apex-angle theorem).

### O4: orthic area

Standard identity:

```text
Area_orthic  =  2 |Area_triangle|  *  |cos(α̃) cos(β̄) cos(γ̄)|.
```

For our triangle:
- `|cos(α̃)| = α_s/√(80+α_s²)`,
- `|cos(β̄)| = (20+α_s)/√(6(80+α_s²))`,
- `|cos(γ̄)| = 1/√6`,
- `|Area_triangle| = √5(4-α_s)/48`.

Multiplying through:

```text
Area_orthic  =  2 * √5(4-α_s)/48 * α_s/√(80+α_s²) * (20+α_s)/√(6(80+α_s²)) * 1/√6
            =  2 * √5(4-α_s) α_s (20+α_s) / (48 * 6 * (80+α_s²))
            =  √5 α_s (4-α_s)(20+α_s) / (144 (80+α_s²)).
```

### O5: LO degeneracy

At `α_s = 0`, the apex angle `α̃|_LO = π/2` (retained right-angle
theorem). For a right triangle with right angle at `V_3`:
- Side `V_2 V_3` (a leg) is perpendicular to side `V_1 V_3` (the
  other leg).
- The altitude from `V_1` perpendicular to `V_2 V_3` is therefore
  parallel to `V_1 V_3` itself, hitting `V_2 V_3` at `V_3` (the
  vertex where the two legs meet).
- Similarly, the altitude from `V_2` to `V_1 V_3` hits at `V_3`.

So `H_a|_LO = H_b|_LO = V_3|_LO = (1/6, √5/6)`. The orthic triangle
degenerates to a line segment from `V_3|_LO` to `H_c|_LO = (1/6, 0)`.

Numerically: at `α_s = 0`, `Area_orthic | LO = √5 × 0 × 4 × 20 / (144 × 80) = 0` ✓.

### O6: nine-point circle identity

The nine-point circle of any nondegenerate triangle passes through the three
altitude feet `H_a, H_b, H_c`. So the orthic triangle's three vertices lie on
the nine-point circle, making that circle the orthic circumcircle. This is the
standard nine-point-circle altitude-foot property; no incircle/excircle
Feuerbach tangency theorem is being invoked.

The runner verifies symbolically that `|H_i - N9|² = R9²` for each
`i`, where `N9 = (O+H)/2` and `R9² = R̄²/4` are the retained
nine-point center and radius from the companion theorems.

### O7: area-ratio

```text
|Area_orthic / Area_triangle|  =  2 |cos(α̃) cos(β̄) cos(γ̄)|
                                =  2 * α_s/√(80+α_s²) * (20+α_s)/√(6(80+α_s²)) * 1/√6
                                =  α_s (20 + α_s) / (3 (80 + α_s²)).
```

In structural integers:
```text
|Area_orthic / Area_triangle|  =  α_s (N_pair² (N_quark - 1) + α_s)
                                  / (N_color (N_pair⁴ (N_quark - 1) + α_s²)).
```

### O8: second boundary degeneracy at α_s = 4

At `α_s = 4`: `ρ̄ = (4-4)/24 = 0`, `η̄ = √5(4-4)/24 = 0`, so
`V_3 → V_1 = (0, 0)`. The original unitarity triangle collapses.
The closed-form orthic area has a continuous zero-area limit there. At the
literal collapsed triangle, the side `V_1 V_3` has zero length, so the
altitude-foot construction is singular; the statement at `α_s = 4` is the
boundary value of the retained closed forms, not a nondegenerate triangle
claim.

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| O2 H_a | `(5(4-α_s)²/(6(80+α_s²)), √5(4-α_s)(20+α_s)/(6(80+α_s²)))` | sympy `simplify(diff) == 0` |
| O2 H_b | `(1/6, √5/6)` | sympy `simplify(diff) == 0` |
| O2 H_c | `((4-α_s)/24, 0)` | sympy `simplify(diff) == 0` |
| O3 |H_bH_c|² | `(80 + α_s²)/576` | sympy `simplify(diff) == 0` |
| O3 |H_aH_c|² | `(4-α_s)²(20+α_s)²/(576(80+α_s²))` | sympy `simplify(diff) == 0` |
| O3 |H_aH_b|² | `α_s²/(80+α_s²)` | sympy `simplify(diff) == 0` |
| O4 area | `√5 α_s (4-α_s)(20+α_s) / (144(80+α_s²))` | sympy & numerical match |
| O5 LO | `H_a\|LO = H_b\|LO = V_3\|LO` | sympy exact |
| O6 nine-point circle | `\|H_i - N9\|² = R9²` for each i | sympy `simplify(diff) == 0` |
| O7 ratio | `α_s(20+α_s)/(3(80+α_s²))` | sympy `simplify(diff) == 0` |
| O8 α_s=4 | `Area_orthic\|(α_s=4) = 0` | sympy exact |

Numerical readout:

| `α_s(v)` | `Area_orthic` | `Area_orthic/Area_triangle` |
| ---: | ---: | ---: |
| 0 (LO) | 0.0 | 0.0 |
| 0.10330 | 0.001571 | 0.00865 |
| 0.118 | 0.001788 | 0.00989 |
| 0.30 | 0.004369 | 0.02535 |
| 1.0 | 0.01208 | 0.08642 |
| 4 | 0.0 | boundary value 1/3 |

The orthic triangle is degenerate at α_s = 0 (right-angle limit)
and its continuous closed-form area also vanishes at α_s = 4
(full-triangle-degeneration boundary). It is non-degenerate strictly between.

## Science Value

### What this lets the framework state cleanly

Previously, the framework had retained closed forms for the original
unitarity triangle's circumradius, circumcenter, orthocenter,
centroid, Euler line, apex angle, Brocard angle, Symmedian point,
Brocard circle, Steiner inellipse, Marden foci, Weitzenbock excess,
Pedoe similarity-deficit metric, Brocard points, Napoleon triangles,
nine-point circle (with α_s-invariant pencil), and the Brocard
polynomial Vieta structure. The **orthic triangle** — formed by
the three altitude feet — was not previously expressed in closed
form on the retained surface.

This note delivers:

1. **NEW orthic-vertices closed forms** (O2): three altitude feet,
   one of which (`H_b`) is α_s-invariant via the protected-γ̄ slope.

2. **NEW orthic-side closed forms** (O3): each orthic side equals
   the original triangle's opposite side times the cosine of the
   third-vertex angle, all with retained-surface closed forms.

3. **NEW orthic-area closed form** (O4):
   `Area_orthic = √5 α_s (4-α_s)(20+α_s) / (144(80+α_s²))` in
   structural-integer form.

4. **NEW LO degeneracy result** (O5): at α_s = 0 the orthic
   triangle degenerates because two altitude feet coincide at
   the LO right-angle apex. This is **forced by the retained
   right-angle theorem** `α_LO = π/2`.

5. **NEW nine-point circle verification** (O6): the orthic circumcircle
   equals the original triangle's nine-point circle on the retained surface,
   verified symbolically.

6. **NEW area-ratio** (O7):
   `|Area_orthic/Area_triangle| = α_s(20+α_s)/(3(80+α_s²))` —
   a clean rational function in α_s.

7. **NEW second boundary degeneracy** (O8): at α_s = 4, the original
   triangle degenerates (`V_3 → V_1`). The Area_orthic polynomial in
   α_s vanishes at the LO right-angle locus α_s = 0 and at this
   vertex-collision boundary α_s = 4.

### Why this counts as pushing the science forward

The orthic triangle is a CLASSICAL secondary structure of any
triangle — it's the triangle formed by the three altitude feet,
inscribed in the nine-point circle. For our retained
unitarity triangle, the orthic carries **two distinct degeneracy
loci** (α_s = 0 and the singular boundary α_s = 4), each tied to a
specific geometric feature:

- **α_s = 0 (LO)**: degeneracy forced by the retained right-angle
  theorem. The orthic collapses because two altitude feet coincide
  at the right-angle vertex itself. This is a **geometric
  consequence of the algebraic identity α_LO = π/2**.
- **α_s = 4**: degeneracy forced by `V_3 → V_1` (original
  triangle's vertex coalescence). This is a **degeneracy of the
  retained NLO Wolfenstein parametrization** at the boundary.

So the orthic-area polynomial `α_s × (4 - α_s) × (20 + α_s)` in the
numerator has two nonnegative zeros (`α_s = 0` and `α_s = 4`) plus one
unphysical zero (`α_s = -20`, outside the physical α_s range). The first is
the LO right-angle degeneracy; the second is the collapsed-apex boundary of
the retained NLO parametrization.

The α_s-invariance of `H_b` reappears
here as the orthic vertex that **stays frozen at the LO apex
location for all α_s**, while the other two orthic vertices `H_a, H_c`
move with α_s. This is one of the cleanest manifestations of the
protected-γ̄ structure on the retained surface.

### Falsifiable structural claim

The closure (O2-O8) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
  + retained right-angle theorem alpha_LO = pi/2
forces:
  H_b  =  (1/N_quark, sqrt(N_quark - 1)/N_quark)  [alpha_s-INVARIANT],
  Area_orthic  =  sqrt(N_quark - 1) alpha_s (N_pair^2 - alpha_s) (N_pair^2 (N_quark - 1) + alpha_s)
                  / (N_pair^4 N_color^2 (N_pair^4 (N_quark - 1) + alpha_s^2)),
  Area_orthic | LO  =  0  (LO degeneracy from H_a = H_b = V_3 collision).
```

Any framework revision breaking the protected slope `tan(γ̄) = √5`
would break the α_s-invariance of `H_b`. Any framework revision
breaking the right-angle theorem `α_LO = π/2` would break the LO
degeneracy of the orthic.

## What This Claims

- `(O2)`: NEW retained orthic-vertex closed forms.
- `(O3)`: NEW retained orthic side-length closed forms.
- `(O4)`: NEW retained orthic area in structural integers.
- `(O5)`: NEW retained LO degeneracy result (orthic collapses when
  H_a = H_b = V_3 at LO right-angle).
- `(O6)`: NEW retained nine-point-circle verification on the
  retained surface.
- `(O7)`: NEW retained orthic-to-original area ratio closed form.
- `(O8)`: NEW retained second boundary degeneracy at α_s = 4.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing; the
  α_s-invariance of `H_b` is derived directly here from the protected
  `tan(gamma_bar)=sqrt(5)` slope.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs.
- Does **not** depend on any α_s-running pipeline.
- Does **not** make a direct CKM-observable claim about the orthic
  triangle; it is a derived geometric structure of the unitarity
  triangle.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_orthic_triangle_exact_closed_form.py
```

Expected:

```text
TOTAL: PASS=25, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs.
- Computes O2-O8 symbolically via sympy and asserts each closed form
  by `simplify(diff) == 0` (with absolute-value handling for the
  signed-area case).
- Verifies that all three orthic vertices lie on the nine-point
  circle.
- Verifies the LO degeneracy `H_a|_LO = H_b|_LO = V_3|_LO` exactly.
- Verifies the second boundary degeneracy at α_s = 4.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates; `tan(γ̄) = √5` α_s-protected.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.
- [`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — apex-angle cos² closed form; LO right-angle `α_LO = π/2`.

**Companion barred-triangle closed forms (cited for context, not
load-bearing here):**

- [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — circumradius `R̄`.
- [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — orthocenter `H`, centroid `G`, Euler line.

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
