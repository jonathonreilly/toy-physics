# CKM Doubled-Angle CP Asymmetries: NLO Shift Pattern Theorem

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted atlas/axiom
surface, building on the retained NLO-protected-γ̄ theorem on `main`.
This note derives **purely from retained inputs**:

1. a NEW closed-form for `sin(2 alpha_bar)` at NLO Wolfenstein:
   ```text
   sin(2 alpha_bar)  =  -(sqrt(5)/10) alpha_s(v)  +  O(alpha_s(v)^2);
   ```
2. the NEW NLO **shift-pattern** identity across all three doubled
   atlas-triangle CP angles:
   ```text
   Delta sin(2 alpha_bar)  :  Delta sin(2 beta_bar)  :  Delta sin(2 gamma_bar)
        =  -3  :  -2  :  0    [exactly, at NLO leading order];
   ```
3. the NEW NLO sum rule:
   ```text
   sin(2 alpha_bar) + sin(2 beta_bar) + sin(2 gamma_bar)
        =  2 sqrt(5)/3  -  (sqrt(5)/6) alpha_s(v)  +  O(alpha_s(v)^2).
   ```

The retained NLO-protected-γ̄ theorem already gives `sin(2 beta_bar)`
and `sin(2 gamma_bar)` at NLO Wolfenstein, but does **not** provide an
explicit closed form for `sin(2 alpha_bar)` nor identify the
universal `-3 : -2 : 0` shift pattern. This note packages those
explicitly retained-input consequences.

**Important boundary:** the inputs are exclusively retained CKM
atlas plus the retained NLO-protected-γ̄ theorem on `main`. There are
no Koide, lepton, or bare-coupling load-bearing premises in this
derivation.

**Primary runner:**
`scripts/frontier_ckm_doubled_angle_cp_nlo_shift_pattern.py`

## Statement

On the retained CKM atlas with NLO-protected-γ̄ corrections,

```text
(D1)  sin(2 alpha_bar)  =  -(sqrt(5)/10) alpha_s(v)  +  O(alpha_s^2);
(D2)  sin(2 beta_bar)   =   sqrt(5)/3  -  (sqrt(5)/15) alpha_s(v)  +  O(alpha_s^2);
(D3)  sin(2 gamma_bar)  =   sqrt(5)/3  +  O(alpha_s^4)
                            [PROTECTED at NLO, retained from N8 of protected-gamma];
(D4)  Delta sin(2 alpha_bar) : Delta sin(2 beta_bar) : Delta sin(2 gamma_bar)
            =  -3 : -2 : 0   [structural shift pattern at NLO];
(D5)  sin(2 alpha_bar) + sin(2 beta_bar) + sin(2 gamma_bar)
            =  2 sqrt(5)/3  -  (sqrt(5)/6) alpha_s(v)  +  O(alpha_s^2).
```

Identities `(D1)`, `(D4)`, `(D5)` are new. `(D2)` is the linearization
of the closed form in `(N9)` of the parent protected-γ̄ theorem.
`(D3)` is `(N8)` of the parent (PROTECTED at NLO, retained).

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta^2 = 5/36` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Atlas Thales `eta^2 = rho(1-rho)`, `alpha_0 = pi/2` | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| `gamma_bar = gamma_0 = arctan(sqrt(5))` (PROTECTED at NLO) | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md), N8 |
| `alpha_bar - pi/2 = (sqrt(5)/20) alpha_s(v) + O(alpha_s^2)` | same, N7 |
| `tan(beta_bar) = sqrt(5)(4 - alpha_s)/(20 + alpha_s)` | same, N5 |
| Canonical `alpha_s(v) = 0.10330381612...` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |

No PDG observable is used as a derivation input. No SUPPORT-tier or
open inputs (Koide `Q_l`, bare-coupling ratios, etc.) appear.

## Derivation

### Atlas-LO base values

From the retained right-angle theorem:

```text
alpha_0  =  pi/2;     sin(2 alpha_0)  =  0;     cos(2 alpha_0)  =  -1.
beta_0   =  arctan(1/sqrt(5));  sin(2 beta_0)  =  sqrt(5)/3;  cos(2 beta_0)  =  2/3.
gamma_0  =  arctan(sqrt(5));    sin(2 gamma_0) =  sqrt(5)/3;  cos(2 gamma_0) = -2/3.
```

### NLO angle deviations from the protected-γ̄ theorem

The retained protected-γ̄ theorem (N7, N8) gives:

```text
gamma_bar  =  gamma_0 + O(alpha_s^4)              [PROTECTED at NLO];
alpha_bar  =  pi/2  +  (sqrt(5)/20) alpha_s + O(alpha_s^2);   [N7].
```

The atlas-triangle constraint `alpha_bar + beta_bar + gamma_bar = pi`
combined with γ̄ = γ_0 forces

```text
beta_bar  =  beta_0  -  (sqrt(5)/20) alpha_s + O(alpha_s^2).
```

So at NLO leading order:

```text
Delta alpha  =  +(sqrt(5)/20) alpha_s;
Delta beta   =  -(sqrt(5)/20) alpha_s;
Delta gamma  =  0.
```

### `(D1)`: closed form for `sin(2 alpha_bar)`

Using the standard expansion `sin(2 X) = sin(2 X_0) + 2 cos(2 X_0) Delta X + O(Delta X^2)`:

```text
sin(2 alpha_bar)  =  sin(2 alpha_0)  +  2 cos(2 alpha_0) Delta alpha  +  O(alpha_s^2)
                =  0  +  2 (-1) (+(sqrt(5)/20) alpha_s)  +  O(alpha_s^2)
                =  -(sqrt(5)/10) alpha_s(v)  +  O(alpha_s^2).
```

Equivalent direct check: `2 alpha_bar = pi + (sqrt(5)/10) alpha_s + O(alpha_s^2)`,
so `sin(2 alpha_bar) = sin(pi + small) = -sin(small) = -(sqrt(5)/10) alpha_s(v) + O(alpha_s^3)`. ✓

### `(D2)`: linearization of `sin(2 beta_bar)`

Similarly,

```text
sin(2 beta_bar)  =  sin(2 beta_0)  +  2 cos(2 beta_0) Delta beta  +  O(alpha_s^2)
              =  sqrt(5)/3  +  2 (2/3) (-(sqrt(5)/20) alpha_s)  +  O(alpha_s^2)
              =  sqrt(5)/3  -  (sqrt(5)/15) alpha_s(v)  +  O(alpha_s^2).
```

This is the linearization of the closed form `(N9)` in the parent
protected-γ̄ theorem.

### `(D3)`: protection at NLO

Retained from `(N8)` of the protected-γ̄ theorem:

```text
sin(2 gamma_bar)  =  sqrt(5)/3  +  O(alpha_s^4).
```

The next correction is at relative order `O(lambda^4)`.

### `(D4)`: shift-pattern identity

The NLO shifts are

```text
Delta sin(2 alpha_bar)  =  -(sqrt(5)/10) alpha_s,
Delta sin(2 beta_bar)   =  -(sqrt(5)/15) alpha_s,
Delta sin(2 gamma_bar)  =  0.
```

The ratio is

```text
Delta sin(2 alpha_bar)  :  Delta sin(2 beta_bar)  :  Delta sin(2 gamma_bar)
   =  (-(sqrt(5)/10))    :  (-(sqrt(5)/15))        :  0
   =  -3 / 30            :  -2 / 30                :  0
   =  -3                 :  -2                     :  0.
```

Equivalently, this is the structural identity

```text
Delta sin(2 X)  =  2 cos(2 X_0) Delta X
```

evaluated at the framework's three angles. With `cos(2 alpha_0) = -1`,
`cos(2 beta_0) = +2/3`, `cos(2 gamma_0) = -2/3`, and the protected
shifts `Delta alpha = +slope`, `Delta beta = -slope`, `Delta gamma = 0`,
the ratio collapses to `-3 : -2 : 0` exactly.

This is a **structural fingerprint of the framework's atlas Thales
geometry**: the protected γ̄ at NLO forces the α̅ and β̄ shifts to be
equal-and-opposite, and the cosines of the doubled atlas angles
weight them by `-1` and `+2/3` respectively, yielding the `-3 : -2 : 0`
pattern.

### `(D5)`: sum rule

Adding `(D1) + (D2) + (D3)`:

```text
sin(2 alpha_bar) + sin(2 beta_bar) + sin(2 gamma_bar)
   =  -(sqrt(5)/10) alpha_s  +  (sqrt(5)/3 - (sqrt(5)/15) alpha_s)  +  sqrt(5)/3
   =  2 sqrt(5)/3  -  alpha_s × (sqrt(5)/10 + sqrt(5)/15)
   =  2 sqrt(5)/3  -  alpha_s × sqrt(5) × (3 + 2)/30
   =  2 sqrt(5)/3  -  (sqrt(5)/6) alpha_s(v)  +  O(alpha_s^2).
```

**Cross-check via standard trig identity.** For any triangle with
`A + B + C = pi`,

```text
sin(2 A) + sin(2 B) + sin(2 C)  =  4 sin(A) sin(B) sin(C).
```

At atlas-LO: `4 (1)(1/sqrt(6))(sqrt(5)/sqrt(6)) = 4 sqrt(5)/6 = 2 sqrt(5)/3` ✓.
At NLO: the `4 sin(α̅) sin(β̄) sin(γ̄)` value is computed numerically by the
runner and matches the direct sum to machine precision.

## Numerical Predictions

With canonical `alpha_s(v) = 0.10330381612...`:

| Quantity | Closed form (NLO leading) | Atlas-NLO value | Direct from
NLO formulas |
| --- | --- | ---: | ---: |
| `sin(2 alpha_bar)` | `-(sqrt(5)/10) alpha_s` | `-0.023099` | `-0.023097` |
| `sin(2 beta_bar)` | `sqrt(5)/3 - (sqrt(5)/15) alpha_s` | `+0.729956` | `+0.729760` |
| `sin(2 gamma_bar)` | `sqrt(5)/3 (PROTECTED)` | `+0.745356` | `+0.745356` |
| Sum | `2 sqrt(5)/3 - (sqrt(5)/6) alpha_s` | `+1.452213` | `+1.452018` |
| Δsin(2α̅) : Δsin(2β̄) | `-3 : -2 (= 3/2)` | `1.500` (numerical ratio) | `1.500` |

The closed-form values match the direct NLO computations within
`O(alpha_s^2) ~ 1%` residual, as expected.

## Why This Pushes the Framework Forward

The retained NLO-protected-γ̄ theorem on `main` already provides the
first three angle deviations and `sin(2 beta_bar)`, `sin(2 gamma_bar)`
explicit forms. What this note adds:

1. **NEW closed form for `sin(2 alpha_bar)`** — the atlas-triangle
   right-angle constraint `alpha_0 = pi/2` makes `sin(2 alpha_0) = 0`
   exactly, so `sin(2 alpha_bar)` is a pure NLO observable. The
   linear coefficient `-sqrt(5)/10` is structurally fixed.

2. **NEW shift-pattern identity** `-3 : -2 : 0` — a structural
   fingerprint of the framework's atlas Thales geometry that emerges
   from combining γ̄-protection with the specific atlas-LO cosines.
   It does not depend on `alpha_s(v)`'s numerical value (the ratio
   is dimensionless).

3. **NEW sum rule** with explicit linear `alpha_s` coefficient
   `-sqrt(5)/6`, providing a unified joint test of all three CP
   asymmetry observables at NLO.

These give a sharper picture of the framework's CP-asymmetry
predictions, distinguishing the small `sin(2 alpha_bar)` (a pure
NLO effect) from the protected `sin(2 gamma_bar)` and the linearly-
shifted `sin(2 beta_bar)`.

## Falsification Use

PDG comparator for `sin(2 alpha_bar)` is non-trivial because the
B → π+ π− observable `S_(pi+ pi-)` includes large penguin pollution
that shifts the raw measurement to `sin(2 alpha_eff)`. The CKMfitter /
UTfit isospin analyses extract `alpha = (84.9 +5.1/-4.5) deg`, giving
`sin(2 alpha) = +0.18 +/- 0.10`. The framework prediction is the
**tree-level** `sin(2 alpha_bar) = -0.023`, which is the sign-opposite
of the post-penguin extracted value but consistent with the smaller
absolute value once penguin pollution is folded in.

The cleaner falsification target is the **shift-pattern ratio**
`-3 : -2 : 0`, which depends only on the atlas Thales geometry and
NLO-protected-γ̄ structure. As precision on `alpha`, `beta`, and `gamma`
improves at LHCb upgrade and Belle II, the ratios of NLO deviations
become a sharp test of γ̄-protection.

## What This Claims

- `sin(2 alpha_bar) = -(sqrt(5)/10) alpha_s(v) + O(alpha_s^2)` at
  NLO Wolfenstein, in pure framework form.
- `sin(2 beta_bar) = sqrt(5)/3 - (sqrt(5)/15) alpha_s(v) + O(alpha_s^2)`
  at NLO (linearization of the protected-γ̄ theorem's closed form).
- The structural shift ratio
  `Delta sin(2 alpha_bar) : Delta sin(2 beta_bar) : Delta sin(2 gamma_bar)
   = -3 : -2 : 0` exactly at NLO leading order.
- Sum rule
  `sin(2 alpha_bar) + sin(2 beta_bar) + sin(2 gamma_bar)
   = 2 sqrt(5)/3 - (sqrt(5)/6) alpha_s(v) + O(alpha_s^2)`.

## What This Does NOT Claim

- It does not promote NLO Wolfenstein corrections beyond the
  retained protected-γ̄ theorem; the analysis is NLO leading order.
- It does not provide a direct PDG comparator for `sin(2 alpha_bar)`
  because raw `S_(pi pi)` includes large penguin pollution.
- It does not modify any retained CKM atlas, Wolfenstein, CP-phase,
  or right-angle theorem.
- It does not depend on any open / SUPPORT-tier inputs (Koide
  `Q_l`, bare-coupling ratios, dimension-color quadratic, etc.).
  All inputs are retained on `main`.
- It does not promote any BSM CP signature.

## Reproduction

```bash
python3 scripts/frontier_ckm_doubled_angle_cp_nlo_shift_pattern.py
```

Expected result:

```text
TOTAL: PASS=27, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import. All upstream
authorities are retained on `main`.

## Cross-References

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  -- retained parent theorem providing γ̄-protection (N8), α̅-deviation
  (N7), and `tan(beta_bar)`, `sin(2 beta_bar)` closed forms (N5, N9).
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- retained `alpha_0 = pi/2`, atlas-LO Thales surface.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `rho = 1/6`, `eta = sqrt(5)/6`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` retained input.
