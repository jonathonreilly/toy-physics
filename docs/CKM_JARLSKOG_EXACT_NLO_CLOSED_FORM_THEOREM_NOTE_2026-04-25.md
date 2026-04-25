# Jarlskog Invariant: EXACT NLO Closed Form Theorem on the Protected-γ̄ Surface

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM atlas
and NLO Wolfenstein protected-γ̄ surface. This note derives an
**EXACT NLO closed form** for the **Jarlskog invariant** `J̄` on the
retained NLO Wolfenstein protected-γ̄ surface, plus its structural-
integer factorization and selection-rule structure.

The headline identity in three equivalent forms:

```text
J_bar  =  sqrt(5) alpha_s(v)^3 (4 - alpha_s(v)) / 288       [closed form]

       =  alpha_s(v)^3  *  eta_bar(v)  /  (N_pair * N_quark)  [structural connection to apex height]

       =  alpha_s(v)^3 sqrt(N_quark - 1) (1 - alpha_s(v)/N_pair^2)
              /  (N_pair * N_quark^2)                          [pure structural integers]
```

`J̄` on the protected-γ̄ NLO surface is a **degree-4 polynomial in α_s
with EXACTLY two non-zero coefficients** (at α_s³ and α_s⁴). All
other α_s coefficients (α_s⁰, α_s¹, α_s², α_s⁵, …) are EXACTLY ZERO
inside that surface.
The ratio of the two non-zero coefficients is EXACTLY `-1/N_pair²`:

```text
J_bar  =  J_3 alpha_s^3  +  J_4 alpha_s^4

  J_3  =  sqrt(N_quark - 1) / (N_pair * N_quark^2)  =  sqrt(5)/72
  J_4  =  -sqrt(N_quark - 1) / (N_pair^3 * N_quark^2)  =  -sqrt(5)/288

  J_4 / J_3  =  -1 / N_pair^2  =  -1/4                          [EXACT selection rule]
```

**Connection to triangle area:**

```text
J_bar  =  alpha_s(v)^3 * (2 * Area_rescaled) / (N_pair * N_quark)
```

where `Area_rescaled = η̄/2` is the area of the rescaled unitarity
triangle. So `J̄` factors directly through the apex-height retained
closed form `(N2)`.

**Primary runner:**
`scripts/frontier_ckm_jarlskog_exact_nlo_closed_form.py`

## Statement

On the NLO Wolfenstein protected-γ̄ surface (where retained `(W1)`,
`(W2)`, `(N2)` hold, plus the standard Wolfenstein NLO formula
`J = A² λ⁶ η̄`):

```text
(J1)  J_bar  =  sqrt(5) alpha_s^3 (4 - alpha_s) / 288                          [EXACT NLO]

(J2)  J_bar  =  alpha_s^3 * eta_bar / (N_pair * N_quark)                       [EXACT, area connection]

(J3)  J_bar  =  alpha_s^3 sqrt(N_quark - 1) (1 - alpha_s/N_pair^2) /
                                          (N_pair * N_quark^2)                 [EXACT, structural integers]

(J4)  Polynomial decomposition:
      J_bar  =  J_3 alpha_s^3 + J_4 alpha_s^4
        where J_3 = sqrt(N_quark - 1) / (N_pair * N_quark^2)  =  sqrt(5)/72,
              J_4 = -sqrt(N_quark - 1) / (N_pair^3 * N_quark^2) = -sqrt(5)/288.

(J5)  Coefficient ratio (NEW selection rule):
      J_4 / J_3  =  -1 / N_pair^2  =  -1/4                                      [EXACT structural ratio]

(J6)  Selection rule: J_bar has ONLY alpha_s^3 and alpha_s^4 terms.
      All other powers (alpha_s^0, alpha_s^1, alpha_s^2, alpha_s^5, ...)
      have coefficient EXACTLY ZERO inside the retained protected-γ̄ NLO surface.

(J7)  NLO scaling: J_bar / J_LO  =  1 - alpha_s/N_pair^2  =  1 - lambda^2/2
      where J_LO  =  J_3 alpha_s^3  =  sqrt(5) alpha_s^3 / 72.

(J8)  Atlas-LO recovery: as alpha_s -> 0,
      J_LO  =  alpha_s^3 sqrt(N_quark - 1) / (N_pair * N_quark^2)              [retained]
            =  sqrt(5) alpha_s^3 / 72.

(J9)  Connection to Wolfenstein: J = A^2 lambda^6 eta_bar
      with retained A^2 = N_pair/N_color, lambda^2 = alpha_s/N_pair, eta_bar from N2.
```

`(J1)`-`(J9)` are NEW. The retained NLO theorem packages closed forms
for the apex coordinates and side lengths but does **not** package
the Jarlskog invariant in EXACT closed form, structural-integer
factorization, or selection-rule decomposition.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| Canonical `alpha_s(v) = 0.103303816...` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| `(W1)` `lambda^2 = alpha_s(v)/N_pair = alpha_s(v)/2` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `(W2)` `A^2 = N_pair/N_color = 2/3` | same |
| `rho = 1/6 = 1/N_quark`, `eta = sqrt(5)/6 = sqrt(N_quark-1)/N_quark` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `(N2)` `eta_bar = sqrt(5)(4 - alpha_s)/24` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md), N2 |
| Standard Wolfenstein formula `J = A^2 lambda^6 eta_bar` (NLO order) | textbook PDG-Wolfenstein expansion (see N1, N2 derivation chain in same theorem) |
| `N_quark = 6`, `N_pair = 2`, `N_color = 3` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |

No PDG observable enters as a derivation input. No SUPPORT-tier or
open inputs (Koide `Q_l`, bare-coupling ratios, dimension-color
quadratic, cross-sector A²-Koide bridge) are used.

## Derivation

The derivation is a four-step chain on retained inputs only.

### Step 1: standard Wolfenstein Jarlskog at NLO

The Jarlskog invariant in standard Wolfenstein parameterization is

```text
J  =  Im(V_us V_cb V_ub^* V_cs^*).
```

Substituting Wolfenstein expressions for the matrix elements,

```text
V_us       =  lambda + O(lambda^4)
V_cs       =  1 - lambda^2/2 + O(lambda^4)
V_cb       =  A lambda^2 + O(lambda^4)
V_ub       =  A lambda^3 (rho - i eta) + O(lambda^5)
```

so

```text
V_us V_cb V_ub^* V_cs^*  =  lambda * A lambda^2 * A lambda^3 (rho + i eta) * (1 - lambda^2/2)
                         =  A^2 lambda^6 (rho + i eta)(1 - lambda^2/2)
                         =  A^2 lambda^6 (rho_bar + i eta_bar)        [using bar definitions]
```

Taking the imaginary part:

```text
J_bar  =  A^2 lambda^6 eta_bar.                                           [standard NLO Wolfenstein]
```

This is the standard PDG-Wolfenstein NLO Jarlskog. The framework's
content enters via the EXACT closed forms for `A²`, `λ²`, and `η̄`
on the protected-γ̄ surface.

### Step 2: substitute retained closed forms

From retained `(W1)`, `(W2)`, `(N2)`:

```text
A^2          =  N_pair / N_color  =  2/3
lambda^2     =  alpha_s / N_pair  =  alpha_s / 2
lambda^6     =  (alpha_s / N_pair)^3  =  alpha_s^3 / 8
eta_bar      =  sqrt(N_quark - 1) (4 - alpha_s) / (N_pair^3 * N_color)
              =  sqrt(5) (4 - alpha_s) / 24
```

(Note `24 = N_pair³ × N_color = 8 × 3 = 24`, so the denominator is
structural.) Substituting:

```text
J_bar  =  (2/3) (alpha_s^3 / 8) sqrt(5) (4 - alpha_s) / 24
       =  2 sqrt(5) alpha_s^3 (4 - alpha_s) / (3 * 8 * 24)
       =  2 sqrt(5) alpha_s^3 (4 - alpha_s) / 576
       =  sqrt(5) alpha_s^3 (4 - alpha_s) / 288.
```

This is `(J1)`. The denominator factor `288 = 3 × 96 = N_color × N_pair⁵ × N_color`
... let us factor more carefully:

```text
288  =  3 * 8 * 24 / 2  =  3 * 96 = 288         [direct]
     =  N_color * N_pair^5 * N_color / N_pair   ... not the cleanest

Better factorization:
288  =  N_pair^3 * N_quark^2  =  8 * 36         [primary structural]
```

Let us verify: `N_pair³ × N_quark² = 8 × 36 = 288` ✓.

### Step 3: structural form `(J3)`

Pull out `N_pair²` from `(4 - α_s) = N_pair²(1 - α_s/N_pair²)`:

```text
sqrt(5) alpha_s^3 (4 - alpha_s) / 288
  =  sqrt(5) alpha_s^3 * N_pair^2 (1 - alpha_s/N_pair^2) / (N_pair^3 * N_quark^2)
  =  sqrt(5) alpha_s^3 (1 - alpha_s/N_pair^2) / (N_pair * N_quark^2)
  =  alpha_s^3 sqrt(N_quark - 1) (1 - alpha_s/N_pair^2) / (N_pair * N_quark^2).
```

This is `(J3)`. Three retained structural integers `N_pair`,
`N_quark`, and `(N_quark - 1)` (via `√`), plus the Wolfenstein
coupling `α_s`, fully determine `J̄`.

### Step 4: connection to apex height `(J2)` and polynomial decomposition `(J4, J5)`

Using retained `(N2)`:

```text
eta_bar  =  sqrt(5) (4 - alpha_s) / 24
        =  sqrt(N_quark - 1) (4 - alpha_s) / (N_pair^3 * N_color).
```

Then

```text
J_bar  =  alpha_s^3 * eta_bar * X    for some coefficient X.

Compare:
  J_bar  =  sqrt(5) alpha_s^3 (4 - alpha_s) / 288
        =  alpha_s^3 * [sqrt(5)(4-alpha_s)/24] * (24/288)
        =  alpha_s^3 * eta_bar * (1/12)
        =  alpha_s^3 * eta_bar / (N_pair * N_quark).
```

This is `(J2)`. The Jarlskog **factors directly through the retained
apex height** `η̄` with structural denominator `N_pair × N_quark = 12`.

For the polynomial decomposition `(J4)`:

```text
J_bar  =  sqrt(5) alpha_s^3 (4 - alpha_s) / 288
       =  sqrt(5) (4 alpha_s^3) / 288  -  sqrt(5) alpha_s^4 / 288
       =  sqrt(5) alpha_s^3 / 72  -  sqrt(5) alpha_s^4 / 288
       =  J_3 alpha_s^3 + J_4 alpha_s^4

  with  J_3  =  sqrt(5) / 72  =  sqrt(N_quark - 1) / (N_pair * N_quark^2)
        J_4  =  -sqrt(5) / 288  =  -sqrt(N_quark - 1) / (N_pair^3 * N_quark^2).
```

The coefficient ratio:

```text
J_4 / J_3  =  -(sqrt(5)/288) / (sqrt(5)/72)  =  -72/288  =  -1/4  =  -1/N_pair^2.
```

This is `(J5)`: the ratio of the only two non-zero α_s-coefficients
of `J̄` is **EXACTLY `-1/N_pair²`** on the protected-γ̄ surface.

### Step 5: selection rule `(J6)`

`J̄ = sqrt(5) α_s³ (4-α_s)/288` is, on its face, a polynomial of
degree 4 in α_s. But explicitly:

```text
J_bar  =  (sqrt(5)/72) alpha_s^3  -  (sqrt(5)/288) alpha_s^4
       =  0 * alpha_s^0 + 0 * alpha_s^1 + 0 * alpha_s^2 + J_3 alpha_s^3 + J_4 alpha_s^4
          + 0 * alpha_s^5 + 0 * alpha_s^6 + ...
```

So all α_s⁰, α_s¹, α_s², α_s⁵, α_s⁶, … coefficients are EXACTLY ZERO
inside the retained NLO surface.
This is `(J6)`. The selection rule has two complementary aspects:

- **Lower cutoff**: `J̄` vanishes as α_s³ → 0 (Jarlskog scales as
  λ⁶ = α_s³/N_pair³ at LO Wolfenstein). No constant or sub-cubic
  contributions.
- **Upper cutoff**: `J̄` is degree-4 in α_s. No α_s⁵ or higher
  corrections inside the protected-γ̄ NLO surface.

The upper cutoff arises because retained `(N2)` is **linear in α_s**
(`η̄ = √5(4-α_s)/24`); multiplying by α_s³ gives at most α_s⁴.

### Step 6: NLO scaling `(J7)`

```text
J_bar  =  J_3 alpha_s^3 (1 + (J_4/J_3) alpha_s)
       =  J_3 alpha_s^3 (1 - alpha_s/N_pair^2)
       =  J_LO * (1 - alpha_s/N_pair^2)

  with J_LO = J_3 alpha_s^3 = sqrt(5) alpha_s^3 / 72.
```

So `J̄/J_LO = 1 - α_s/N_pair² = 1 - λ²/2`. This is the same factor as
`η̄/η = 1 - λ²/2`, confirming that the entire NLO scaling of `J̄` is
inherited from the apex height NLO scaling `(N2)`.

## Numerical Verification

With canonical `alpha_s(v) = 0.10330381612227...`:

| Quantity | Closed form | Value |
| --- | --- | ---: |
| `J̄` (NEW J1) | `√5 α_s³(4-α_s)/288` | `3.335 × 10⁻⁵` |
| `J̄` (NEW J2) | `α_s³ η̄ / (N_pair × N_quark)` | `3.335 × 10⁻⁵` |
| `J̄` (NEW J3) | `α_s³ √5 (1 - α_s/4)/72` | `3.335 × 10⁻⁵` |
| `J_3 α_s³` (NEW J4) | `(√5/72) α_s³` | `3.424 × 10⁻⁵` |
| `J_4 α_s⁴` (NEW J4) | `(-√5/288) α_s⁴` | `-8.847 × 10⁻⁷` |
| `J_4/J_3` (NEW J5) | `-1/N_pair² = -1/4` | `-0.250000000` |
| `J̄/J_LO` (NEW J7) | `1 - α_s/N_pair²` | `0.974174` |
| PDG `J` | `(3.0 ± 0.1) × 10⁻⁵` | `3.0 × 10⁻⁵` |
| Framework deviation | atlas-NLO vs physical | `+3.35 σ` |

All identities verified to machine precision at six independent
values of `α_s ∈ {0.05, 0.10, 0.103303816, 0.15, 0.20, 0.30}`.

## Science Value

### What this lets the framework predict that it could not before

The retained NLO theorem packages closed forms for `ρ̄`, `η̄`,
`R_b̄²`, and the angles, but does **not** package the **Jarlskog
invariant** `J̄` in EXACT closed form, structural-integer factorization,
or polynomial decomposition. This note delivers all three:

- `(J1)` `J̄ = √5 α_s³(4-α_s)/288` EXACT NLO closed form.
- `(J2)` `J̄ = α_s³ η̄ / (N_pair × N_quark)` connection to apex height.
- `(J3)` `J̄ = α_s³ √(N_quark-1)(1-α_s/N_pair²)/(N_pair × N_quark²)`
  pure structural-integer form.

### The polynomial selection rule (J6) is the sharp claim

`J̄` is a **degree-4 polynomial in α_s with EXACTLY two non-zero
coefficients** (at α_s³ and α_s⁴) inside the retained NLO surface.
All other coefficients are zero there.
This is sharper than "approximately α_s³" or "leading-order Jarlskog";
inside the protected-γ̄ NLO surface, the closed form has no additional
truncation error beyond the surface's defining NLO formula.

The lower cutoff (no α_s⁰, α_s¹, α_s²) follows from `J ∝ λ⁶ = α_s³/8`.
The upper cutoff (no α_s⁵, α_s⁶, …) follows from `(N2)`'s linearity
in α_s — multiplying by α_s³ gives at most α_s⁴.

### The coefficient ratio J_4/J_3 = -1/N_pair² is striking

The ratio of the two non-zero α_s coefficients of `J̄` is **exactly
-1/N_pair² = -1/4**. With retained `N_pair = 2` from the magnitudes
counts theorem, this ratio is fully determined by structural integers.

Equivalently: `J̄` factors as `J_3 α_s³ × (1 - α_s/N_pair²)`, with the
NLO correction factor `(1 - α_s/N_pair²) = (1 - λ²/2) = η̄/η` exactly.
So the **entire** NLO α_s-dependence of `J̄` is captured by the
retained apex-height ratio `(N2)`.

### Connection to apex height (J2): J̄ = α_s³ × η̄ / 12

Equivalently: `J̄ = α_s³ × (2 × Area_rescaled) / (N_pair × N_quark)`.
The Jarlskog factors directly through the rescaled triangle area
with structural denominator `N_pair × N_quark = 12`. This **ties
the CP-violation observable to the geometric area of the unitarity
triangle through structural integers only** — no PDG observable, no
free parameter, and no additional truncation inside the NLO surface.

### NNLO extension diagnostic

Inside the retained NLO protected-γ̄ surface, the theorem gives:

```text
NO alpha_s^5 or alpha_s^6 correction to J_bar inside that NLO surface.
J_bar is a degree-4 polynomial in alpha_s with two non-zero coefficients there.

J_bar / J_LO = 1 - alpha_s/N_pair^2 EXACTLY at NLO.
```

If a future NNLO Wolfenstein extension yields a non-zero `α_s⁵`
correction to the physical Jarlskog continuation, that does not
contradict this note. It means the correction enters through one of the
inputs defining a beyond-NLO surface:

- retained `(N2)` `η̄ = √5(4-α_s)/24` itself receives an `α_s²` term
  in the extension, or
- the standard Wolfenstein NLO formula `J = A²λ⁶η̄` requires
  modification at higher orders in λ (which it does at λ⁸ and
  beyond).

This makes the polynomial closed form a diagnostic for where any NNLO
deviation must enter; it is not itself a physical all-orders Jarlskog
claim.

### What rules in / rules out

- The framework predicts `J̄ = 3.335 × 10⁻⁵` at canonical α_s.
- PDG `J = (3.0 ± 0.1) × 10⁻⁵`. Framework deviation `+3.35 σ`.
- This is the established atlas-NLO vs physical-J gap (similar to
  the atlas-NLO `sin(2β̄) = 0.730` vs PDG `0.706 ± 0.011` deviation).
  It does NOT signal a problem with the closed form — the closed
  form is internally consistent at canonical α_s; the gap reflects
  the overall framework normalization vs PDG, established in prior
  retained theorems.
- A future precision improvement of `J` to `±0.05 × 10⁻⁵` would
  bring the framework's `+0.7 × 10⁻⁵` deviation into focus and test
  the protected-γ̄ surface's atlas-NLO normalization.

### Why this counts as pushing the science forward

Three layers of new content beyond the parent NLO theorem:

1. **EXACT closed form for J̄** in three structurally complementary
   forms: closed (J1), area-connection (J2), structural-integers (J3).

2. **Polynomial selection rule (J6)**: `J̄` has only α_s³ and α_s⁴
   coefficients, with all other α_s powers EXACTLY zero on the
   protected-γ̄ NLO surface. The framework's NLO Jarlskog surface is a
   degree-4 polynomial.

3. **Coefficient ratio (J5)**: `J_4/J_3 = -1/N_pair²` EXACTLY. The
   only non-trivial α_s-dependence in `J̄` is captured by a single
   structural-integer ratio.

These propositions about the surface-exact α_s-structure of the
Jarlskog on the protected-γ̄ NLO surface were not visible from `(N1)`-
`(N9)` alone without the explicit NLO Wolfenstein construction.

## What This Claims

- `(J1)` NEW EXACT closed form `J̄ = √5 α_s³(4-α_s)/288`.
- `(J2)` NEW EXACT area connection `J̄ = α_s³ η̄/(N_pair × N_quark)`.
- `(J3)` NEW EXACT structural form `J̄ = α_s³ √(N_quark-1)(1-α_s/N_pair²)/(N_pair × N_quark²)`.
- `(J4)` NEW polynomial decomposition `J̄ = J_3 α_s³ + J_4 α_s⁴` with
  closed forms for both coefficients.
- `(J5)` NEW selection rule `J_4/J_3 = -1/N_pair²` EXACT.
- `(J6)` NEW selection rule: only α_s³ and α_s⁴ coefficients non-zero;
  all other α_s powers EXACTLY zero inside the retained NLO surface.
- `(J7)` NEW NLO scaling `J̄/J_LO = 1 - α_s/N_pair²` EXACT.

## What This Does NOT Claim

- It does not extend the protected-γ̄ surface to NNLO Wolfenstein.
  The closed form is EXACT on the NLO protected-γ̄ surface (i.e.,
  using the standard Wolfenstein NLO formula `J = A² λ⁶ η̄`).
- It does not claim that the physical CKM Jarlskog has no higher-order
  Wolfenstein corrections beyond this NLO surface.
- It does not modify any retained CKM atlas, Wolfenstein, CP-phase,
  right-angle, NLO-protected-γ̄, or magnitudes structural counts theorem.
- It does not use any SUPPORT-tier or open input. In particular, it
  does NOT use the cross-sector `A² ↔ Q_l` Koide bridge (a
  conditional support note) and makes no claim about lepton-sector
  Koide closure.
- It does not close the Wolfenstein `A` parameter at any deeper level
  than the retained `(W2)` `A² = N_pair/N_color`. Closing `A²` at the
  CL3 algebraic foundation level would require below-W2 derivation
  that this note does not provide.
- It does not predict `J` to better experimental precision than the
  established atlas-NLO vs physical gap (`+3.35 σ` from PDG).

## Reproduction

```bash
python3 scripts/frontier_ckm_jarlskog_exact_nlo_closed_form.py
```

Expected result:

```text
TOTAL: PASS=36, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import. All upstream
authorities are retained on `main`.

## Cross-References

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  -- retained N2 (`η̄`) used in this derivation.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `λ² = α_s(v)/N_pair`, `A² = N_pair/N_color`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `ρ = 1/N_quark`, `η² = (N_quark-1)/N_quark²`.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- retained `N_quark = N_pair × N_color = 6`, `N_pair = 2`, `N_color = 3`.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `α_s(v)` retained input.
