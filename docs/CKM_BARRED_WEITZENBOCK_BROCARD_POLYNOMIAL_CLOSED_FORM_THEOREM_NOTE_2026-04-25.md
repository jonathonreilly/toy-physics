# Barred Unitarity-Triangle Weitzenbock Inequality + Brocard-Polynomial Unification: EXACT Closed Form Theorem

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure corollary on the proposed_promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives the
**EXACT closed form for the classical Weitzenbock inequality**
(`a² + b² + c² ≥ 4√3 · Area`) applied to the barred unitarity
triangle on the retained NLO Wolfenstein protected-γ̄ surface, and
identifies it as the **fifth distinct closed-form representation** of
the Brocard polynomial `P(α_s)`. Combined with the existing
representations from the companion theorems on the Brocard angle,
the Steiner inellipse, and Marden's theorem, this completes a
**five-form algebraic unification** of `P(α_s)` as the **universal
equilateral excess polynomial** of the retained CKM unitarity triangle.

The headline closed forms:

```text
(W2)  Weitzenbock sum:
        W_+  =  (a^2 + b^2 + c^2) + 4 sqrt(3) Area
             =  ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15)(4 - alpha_s)) / 48.

(W3)  Weitzenbock gap (deficit from equilateral):
        W_-  =  (a^2 + b^2 + c^2) - 4 sqrt(3) Area
             =  ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15)(4 - alpha_s)) / 48.

(W4)  Product factorization:
        W_+ * W_-  =  P(alpha_s) / 2304
                   =  P(alpha_s) / (N_pair^8 N_color^2).

(W5)  LO recovery:
        W_+ | LO  =  (N_quark + sqrt(N_color (N_quark - 1))) / N_color  =  (6 + sqrt(15))/3,
        W_- | LO  =  (N_quark - sqrt(N_color (N_quark - 1))) / N_color  =  (6 - sqrt(15))/3,
        W_+ | LO * W_- | LO  =  (N_quark + 1) / N_color  =  7/3.

(W7)  Five-form unification of P(alpha_s):
        (a) Raw:         P = (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2,
        (b) Brocard:     P = 80 (4 - alpha_s)^2 (cot^2(omega_bar) - 3),
        (c) Weitzenbock: P = 2304 ((perim_sq)^2 - 48 Area^2),                     [NEW]
        (d) Steiner:     P = 746496 (S'^2 - 4 P'),
        (e) Marden:      P = 9216 |V_3^2 - V_3 + 1|^2.
```

`sqrt(15)` plays a central role here: it is exactly
`sqrt(N_color (N_quark − 1))`, the **natural irrationality of the
retained surface**. The Weitzenbock sum / gap split factors P(α_s)
through Q[√15], giving a NEW characterization of `P(α_s) > 0` strictly:
each factor of `P(α_s)` over Q[√15] is a quadratic with strictly
negative discriminant, so `P(α_s)` has no real roots at all.

**Primary runner:**
`scripts/frontier_ckm_barred_weitzenbock_brocard_polynomial_closed_form.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface (where
`tan(γ̄) = √5` is α_s-protected; vertex
`V_3 = (rho_bar, eta_bar) = ((4-α_s)/24, sqrt(5)(4-α_s)/24)` is retained;
side-length squares
`a² = (80+α_s²)/96, b² = (4-α_s)²/96, c² = 1` follow):

```text
(W1)  Weitzenbock inequality on the retained surface:
        a^2 + b^2 + c^2  >=  4 sqrt(3) Area_triangle.

      Numerical sweep across alpha_s in [0, 3.0] confirms strict inequality.

(W2)  Weitzenbock sum closed form:
        W_+  =  perim_sq + 4 sqrt(3) Area
             =  ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15)(4 - alpha_s)) / 48,

      where sqrt(15) = sqrt(N_color (N_quark - 1)) = sqrt(3 * 5).

(W3)  Weitzenbock gap closed form (deficit from the equilateral lower bound):
        W_-  =  perim_sq - 4 sqrt(3) Area
             =  ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15)(4 - alpha_s)) / 48.

(W4)  Product factorization (NEW):
        W_+  *  W_-  =  (perim_sq)^2 - 48 Area^2
                     =  P(alpha_s) / 2304
                     =  P(alpha_s) / (N_pair^8 N_color^2),

      where  P(alpha_s)  =  (alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2

      is the Brocard polynomial. The Weitzenbock sum and gap are
      conjugate factors of P(alpha_s) under the Q[sqrt(15)] split.

(W5)  LO recovery in pure structural integers:
        W_+ | LO  =  (N_quark + sqrt(N_color (N_quark - 1))) / N_color
                  =  (6 + sqrt(15))/3,
        W_- | LO  =  (N_quark - sqrt(N_color (N_quark - 1))) / N_color
                  =  (6 - sqrt(15))/3,
        W_+ | LO * W_- | LO  =  (N_quark^2 - N_color (N_quark - 1)) / N_color^2
                              =  N_color (N_quark + 1) / N_color^2
                              =  (N_quark + 1) / N_color
                              =  7/3.

(W6)  Squared-form identity: (perim_sq)^2 - 48 Area^2 = P(alpha_s)/2304.

      This is the Weitzenbock-excess-squared in closed form on the retained
      surface, with structural-integer scaling 2304 = N_pair^8 N_color^2.

(W7)  FIVE-FORM UNIFICATION of P(alpha_s):
        (a) Raw         :  P  =  (alpha_s^2 - 4 alpha_s + 96)^2  -  240 (4 - alpha_s)^2.
        (b) Brocard     :  P  =  80 (4 - alpha_s)^2  (cot^2(omega_bar) - 3).
        (c) Weitzenbock :  P  =  2304  ((perim_sq)^2 - 48 Area^2).            [NEW]
        (d) Steiner     :  P  =  746496  (S'^2 - 4 P').
        (e) Marden      :  P  =  9216  |V_3^2 - V_3 + 1|^2.

      All five are equivalent on the retained surface; each encodes a
      different classical equilateral condition. The structural-integer
      scaling factors are:
        80 (4 - alpha_s)^2  -- alpha_s-DEPENDENT,
        2304  =  N_pair^8 N_color^2,
        746496  =  N_pair^10 N_color^6,
        9216  =  (N_pair^4 N_quark)^2.

(W8)  Brocard-Weitzenbock algebraic equivalence:
        cot(omega_bar)            =  perim_sq / (4 Area),
        Weitzenbock ratio         =  perim_sq / (4 sqrt(3) Area)  =  cot(omega_bar)/sqrt(3).

      The Brocard inequality cot^2(omega_bar) >= 3 and the Weitzenbock
      inequality (perim_sq)^2 >= 48 Area^2 are algebraically equivalent.
      Both become equality at omega_bar = pi/6 (equilateral), and both
      are governed by P(alpha_s) >= 0 on the retained surface.

(W9)  Root structure: P(alpha_s) factors over Q[sqrt(15)] as

        P(alpha_s = 4 - u)  =  (u^2 - 4(1 + sqrt(15)) u + 96)
                              * (u^2 - 4(1 - sqrt(15)) u + 96).

      Each quadratic factor has NEGATIVE discriminant (the discriminants
      are -32 sqrt(15) - 128 and 32 sqrt(15) - 128 ~ -4.06, both negative).
      So P(alpha_s) has no real roots at all -- the retained unitarity
      triangle is uniformly bounded away from equilateral across the
      ENTIRE real alpha_s axis, not just the physical range.
```

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `rho_bar = (4 - alpha_s)/24`, `eta_bar = sqrt(5)(4 - alpha_s)/24` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = N_pair * N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |
| Jarlskog `J̄ = √5(4-α_s)/24` (= 2 × Area on retained surface) | [`CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note
is load-bearing. No unmerged branch is cited as load-bearing — the
companion Brocard, Steiner, and Marden theorem branches are referenced
in W7 for context (the five-form unification observation), but each
form (b), (d), (e) of `P(α_s)` is independently re-derivable from the
retained inputs, and the runner verifies each form by direct symbolic
computation against the raw `P(α_s)` form (a).

## Derivation

### W1: Weitzenbock inequality on the retained surface

The classical **Weitzenbock inequality** states that for any triangle
with side lengths `(a, b, c)` and area `K`,

```text
a^2 + b^2 + c^2  >=  4 sqrt(3) * K,
```

with equality iff the triangle is equilateral. For the retained CKM
unitarity triangle on the protected-γ̄ surface:

```text
a^2 + b^2 + c^2  =  perim_sq  =  (alpha_s^2 - 4 alpha_s + 96) / 48,
4 sqrt(3) Area   =  4 sqrt(3) * sqrt(5) (4 - alpha_s) / 48
                 =  4 sqrt(15) (4 - alpha_s) / 48
                 =  sqrt(15) (4 - alpha_s) / 12.
```

`sqrt(15) = sqrt(3 * 5) = sqrt(N_color × (N_quark - 1))` — the
**natural irrationality of the retained surface**.

### W2, W3: Weitzenbock sum and gap

Define the sum and gap:

```text
W_+  =  perim_sq + 4 sqrt(3) Area
     =  ((alpha_s^2 - 4 alpha_s + 96) + 4 sqrt(15) (4 - alpha_s)) / 48,

W_-  =  perim_sq - 4 sqrt(3) Area
     =  ((alpha_s^2 - 4 alpha_s + 96) - 4 sqrt(15) (4 - alpha_s)) / 48.
```

`W_-` is the **Weitzenbock gap** — the deficit of the perimeter² from
the equilateral lower bound `4√3 · Area`. The Weitzenbock inequality
states `W_- ≥ 0`.

### W4: Product factorization

Direct computation of the product:

```text
W_+ * W_-  =  (perim_sq)^2 - 48 Area^2
           =  ((alpha_s^2 - 4 alpha_s + 96)^2 - 240 (4 - alpha_s)^2) / 2304
           =  P(alpha_s) / 2304.
```

This is a **difference-of-squares factorisation** of the Brocard
polynomial through the conjugate pair of `Q[sqrt(15)]` factors. The
scaling `2304 = 48² = N_pair⁸ N_color²` is purely structural-integer.

### W5: LO recovery

At `alpha_s = 0`:

```text
W_+ | LO  =  (96 + 16 sqrt(15)) / 48  =  (6 + sqrt(15)) / 3
            =  (N_quark + sqrt(N_color (N_quark - 1))) / N_color,

W_- | LO  =  (96 - 16 sqrt(15)) / 48  =  (6 - sqrt(15)) / 3
            =  (N_quark - sqrt(N_color (N_quark - 1))) / N_color.
```

Their product is

```text
W_+ | LO * W_- | LO  =  (N_quark^2 - N_color (N_quark - 1)) / N_color^2
                      =  (36 - 15) / 9  =  21/9  =  7/3
                      =  N_color (N_quark + 1) / N_color^2
                      =  (N_quark + 1) / N_color.
```

Pure structural-integer ratio at LO.

### W6: Squared-form identity

By construction, `(perim_sq)² − 48 Area² = W_+ · W_- = P(α_s)/2304`.
This is the **Weitzenbock excess squared in closed form**, equating the
Weitzenbock excess (the algebraic-positivity signature of the
inequality) to the Brocard polynomial divided by a structural-integer
scaling.

### W7: Five-form unification

The Brocard polynomial `P(α_s)` admits five distinct closed-form
representations on the retained surface:

| Form | Closed form | Scaling factor |
| --- | --- | --- |
| (a) Raw | `P = (α_s² − 4α_s + 96)² − 240(4 − α_s)²` | 1 |
| (b) Brocard | `P = 80(4 − α_s)² · (cot²(ω̄) − 3)` | `80(4 − α_s)²` |
| (c) Weitzenbock | `P = 2304 · ((perim_sq)² − 48 Area²)` | `2304 = N_pair⁸ N_color²` |
| (d) Steiner | `P = 746496 · (S'² − 4 P')` | `746496 = N_pair^10 N_color⁶` |
| (e) Marden | `P = 9216 · |V_3² − V_3 + 1|²` | `9216 = (N_pair⁴ N_quark)²` |

Each form encodes a different classical equilateral condition:
**(a)** the raw polynomial in `α_s`; **(b)** the Brocard inequality
`ω̄ ≤ π/6`; **(c)** the Weitzenbock inequality
`perim_sq ≥ 4√3 · Area`; **(d)** the Steiner inellipse semi-axis
discriminant (Steiner inellipse circular iff `P = 0`); **(e)** the
Marden foci coincidence (Steiner inellipse foci collapse iff `P = 0`).

All five become **algebraically equivalent on the retained surface**
because they all characterise the SAME equilateral limit. The
**single algebraic invariant `P(α_s)`** governs the entire equilateral
condition, manifesting in five different geometric guises with five
different (mostly α_s-independent) structural-integer scaling factors.

The Brocard form (b) is the only one with α_s-DEPENDENT scaling
`80(4 − α_s)²`. The other three (c, d, e) have α_s-INDEPENDENT
structural-integer scalings:

```text
2304    =  48^2          =  (N_pair^4 N_color)^2  =  N_pair^8 N_color^2,
746496  =  864^2         =  (N_pair^5 N_color^3)^2  =  N_pair^10 N_color^6,
9216    =  96^2          =  (N_pair^4 N_quark)^2  =  N_pair^8 N_quark^2.
```

### W8: Brocard-Weitzenbock algebraic equivalence

For any triangle, `cot(ω) = (a²+b²+c²)/(4·Area)`. So the **Weitzenbock
ratio** `(a²+b²+c²)/(4√3·Area)` equals `cot(ω̄)/√3`. The Brocard
inequality `cot²(ω̄) ≥ 3` is therefore algebraically identical to the
Weitzenbock inequality `(perim_sq)² ≥ 48·Area²`. Both reduce to the
equilateral condition at equality.

This is **not a new inequality**; the science value is in the
**dual algebraic representation**. The Brocard form (b) and the
Weitzenbock form (c) of `P(α_s)` are different algebraic
factorizations of the same classical inequality.

### W9: Root structure of P(α_s) over Q[√15]

Substituting `u = 4 − α_s` (so `α_s = 4 − u`), the Brocard polynomial
becomes a quartic in `u`. It factors over `Q[√15]` as

```text
P(alpha_s = 4 - u)  =  (u^2 - 4(1 + sqrt(15)) u + 96)
                       * (u^2 - 4(1 - sqrt(15)) u + 96).
```

Each quadratic factor has discriminant

```text
Delta_+  =  16 (1 + sqrt(15))^2 - 384  =  -128 + 32 sqrt(15)  ~  -4.06,
Delta_-  =  16 (1 - sqrt(15))^2 - 384  =  -128 - 32 sqrt(15)  ~  -252.
```

Both discriminants are NEGATIVE. So `P(α_s)` has **no real roots at
all** — the retained unitarity triangle is uniformly bounded away
from equilateral on the ENTIRE real α_s axis. The four complex roots
of `P(α_s)` come in two conjugate pairs:

```text
alpha_s_root  =  (2 - 2 sqrt(15)) +/- 2i (sqrt(5) - sqrt(3))
              =  (2 + 2 sqrt(15)) +/- 2i (sqrt(5) + sqrt(3))

      =  (2 -/+ 2 sqrt(N_color (N_quark - 1)))
         +/- 2i (sqrt(N_quark - 1) -/+ sqrt(N_color)).
```

In structural-integer form the roots involve `sqrt(N_color)`,
`sqrt(N_quark - 1)`, and `sqrt(N_color (N_quark - 1))`. The natural
irrationality of the retained surface is precisely the Q[√15] (i.e.
Q[√(N_color × (N_quark - 1))]) extension.

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| W1 sweep | `perim_sq > 4√3 Area` on `α_s ∈ [0, 3]` | numerical PASS |
| W2 W_+ | `((α_s²-4α_s+96)+4√15(4-α_s))/48` | sympy `simplify(diff) == 0` |
| W3 W_- | `((α_s²-4α_s+96)-4√15(4-α_s))/48` | sympy `simplify(diff) == 0` |
| W4 product | `W_+·W_- = P(α_s)/2304` | sympy `simplify(diff) == 0` |
| W4 struct | `2304 = N_pair⁸ N_color²` | exact integer |
| W5 LO W_+ | `(N_quark+√(N_color(N_quark-1)))/N_color` | sympy `simplify(diff) == 0` |
| W5 LO W_- | `(N_quark-√(N_color(N_quark-1)))/N_color` | sympy `simplify(diff) == 0` |
| W5 LO product | `(N_quark+1)/N_color = 7/3` | sympy exact |
| W6 squared | `(perim_sq)²-48 Area² = P/2304` | sympy `simplify(diff) == 0` |
| W7(a) Raw | `P = (α_s²-4α_s+96)²-240(4-α_s)²` | sympy `simplify(diff) == 0` |
| W7(b) Brocard | `P = 80(4-α_s)²(cot²(ω̄)-3)` | sympy `simplify(diff) == 0` |
| W7(c) Weitzenbock | `P = 2304((perim_sq)²-48 Area²)` | sympy `simplify(diff) == 0` |
| W7(d) Steiner | `P = 746496(S'²-4P')` | sympy `simplify(diff) == 0` |
| W7(e) Marden | `P = 9216·\|V_3²-V_3+1\|²` | sympy `simplify(diff) == 0` |
| W8 equiv | `Weitzenbock ratio = cot(ω̄)/√3` | sympy `simplify(diff) == 0` |
| W9 factoring | `P` over `Q[√15]` | sympy `simplify(diff) == 0` |
| W9 disc | both quadratic factor discriminants < 0 | numerical sweep |

## Science Value

### What this lets the framework state cleanly

Previously, the framework had retained closed forms for the Brocard
angle, Steiner inellipse, and Marden foci, with the deep observation
(from the companion theorems) that the polynomial
`P(α_s) = (α_s² − 4α_s + 96)² − 240(4-α_s)²` simultaneously controls
the Brocard inequality, the Steiner inellipse semi-axis discriminant,
and the Marden foci coincidence. The connection to the **Weitzenbock
inequality** — one of the most famous classical triangle inequalities —
was not previously made explicit.

This note delivers:

1. **NEW Weitzenbock closed forms** (W2, W3): the Weitzenbock sum and
   gap on the retained surface, with `√15` as the natural
   irrationality.

2. **NEW product factorization** (W4): `W_+ · W_- = P(α_s)/2304` —
   the Weitzenbock sum and gap are conjugate factors of the Brocard
   polynomial through the Q[√15] split.

3. **NEW LO recovery** (W5): the Weitzenbock product at LO equals
   `(N_quark + 1)/N_color = 7/3`, a pure structural-integer ratio.

4. **NEW five-form unification** (W7): the Brocard polynomial admits
   FIVE distinct closed-form representations on the retained surface,
   with structural-integer scaling factors revealing different
   algebraic guises of the equilateral condition.

5. **NEW root structure observation** (W9): `P(α_s)` factors over
   Q[√15] into two quadratics, each with strictly negative
   discriminant. So `P(α_s) > 0` on the ENTIRE real α_s axis (not
   just the physical range), and the retained unitarity triangle is
   uniformly bounded away from equilateral.

### Why this counts as pushing the science forward

The Weitzenbock inequality is one of the most studied classical
triangle inequalities, with countless refinements (Hadwiger-Finsler,
Pedoe, etc.). Connecting it to `P(α_s)` gives **the universal
equilateral excess polynomial of the retained CKM unitarity triangle
a clean physical interpretation as the Weitzenbock excess squared**.

The Q[√15] factorisation observation (W9) is structurally striking:
the natural irrationality of the retained surface is **exactly**
`√(N_color × (N_quark − 1))`, and the Brocard polynomial factors
through this irrationality into two conjugate quadratics, each with
strictly negative discriminant. This is **algebraic rigidity**: the
retained surface admits a single irrational extension Q[√15], and
within that extension `P(α_s)` factors into structurally-determined
conjugate pieces.

The five-form unification (W7) consolidates the picture: `P(α_s)` is
not just one polynomial in α_s — it is the **invariant signature of
the retained surface's non-equilateral structure**, manifesting in
classical triangle inequalities, classical triangle interior points,
and classical triangle inscribed conics. A single algebraic object
with five geometric interpretations.

### Falsifiable structural claim

The closure (W2-W7, W9) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
forces:
  W_+ * W_-  =  P(alpha_s) / (N_pair^8 N_color^2),
  W_+ | LO * W_- | LO  =  (N_quark + 1) / N_color  =  7/3,
  P(alpha_s) factors over Q[sqrt(N_color (N_quark - 1))] into two
  quadratics with strictly negative discriminants.
```

Any framework revision shifting `(rho_bar, eta_bar)` off the retained
protected-γ̄ surface, or changing structural integers, would break
W4, W5, AND W9 simultaneously. The Q[√15] factorisation is
particularly rigid: it depends on the specific equality
`240 = N_pair⁴ × N_color × (N_quark − 1) = 16 × 3 × 5`.

## What This Claims

- `(W1)`: NEW retained verification that the classical Weitzenbock
  inequality `a²+b²+c² ≥ 4√3 · Area` holds strictly on the retained
  unitarity triangle for all physical α_s.
- `(W2, W3)`: NEW retained closed forms for the Weitzenbock sum
  `W_+` and gap `W_-`, with `√15` as the natural irrationality.
- `(W4)`: NEW retained product factorization `W_+·W_- = P(α_s)/2304`
  — Brocard polynomial as the Weitzenbock sum-gap product.
- `(W5)`: NEW LO recovery
  `W_+|LO · W_-|LO = (N_quark+1)/N_color = 7/3` in pure
  structural integers.
- `(W6)`: NEW retained closed form for the Weitzenbock excess
  squared, `(perim_sq)² − 48 Area² = P(α_s)/2304`.
- `(W7)`: NEW five-form unification of `P(α_s)`, with the Weitzenbock
  form `(c)` adding to the previously-derived Brocard, Steiner, and
  Marden forms.
- `(W8)`: NEW algebraic equivalence
  `Weitzenbock ratio = cot(ω̄)/√3` between the Brocard and
  Weitzenbock inequalities.
- `(W9)`: NEW root-structure observation: `P(α_s)` factors over
  Q[√15] into two quadratics with strictly negative discriminants,
  so it has no real roots on the entire α_s axis.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing (each form of
  `P(α_s)` in W7 is independently re-derivable from retained inputs;
  the runner verifies each form by direct symbolic computation).
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs.
- Does **not** depend on any α_s-running pipeline; all results live
  on the protected-γ̄ surface at canonical `α_s(v)`.
- Does **not** make a direct CKM-observable claim about the
  Weitzenbock excess; it is a derived geometric quantity of the
  unitarity triangle.

## Reproduction

```bash
python3 scripts/frontier_ckm_barred_weitzenbock_brocard_polynomial_closed_form.py
```

Expected:

```text
TOTAL: PASS=28, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs (`rho_bar`, `eta_bar`,
  `N_pair`, `N_color`, `N_quark`, Jarlskog citation).
- Computes W1–W9 symbolically via sympy at the retained values and
  asserts each closed form by `simplify(diff) == 0`.
- Independently re-derives each of the FIVE forms of `P(α_s)` and
  matches against the raw form (a) — confirming the unification.
- Verifies the Q[√15] factorisation of `P(α_s)` and that both
  quadratic factor discriminants are strictly negative.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.
- [`CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — Jarlskog `J̄`.

**Companion barred-triangle closed forms (cited for context, not
load-bearing here):**

- [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — circumradius `R̄`.
- [`CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_APEX_ANGLE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — apex angle `α̃`.
- [`CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_ORTHOCENTER_EULER_LINE_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — orthocenter, centroid, Euler line.
- [`CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md)
  — Pythagorean structure.

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch (companion Brocard-angle, symmedian-Brocard-circle,
  and Steiner-inellipse-Marden branches are referenced only for
  context in the W7 unification observation; each form of `P(α_s)`
  is independently re-derived here from retained inputs).
- Any candidates-tier theorem.
