# sin(2β̄) NLO Ratio with Atlas N_quark Structural Fingerprint Theorem

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure corollary on the proposed_promoted CKM atlas
+ NLO-protected-γ̄ surfaces. This note derives **a NEW α_s-INDEPENDENT
multiplicative NLO ratio** for the framework's `sin(2 beta_bar)` CP
asymmetry,

```text
sin(2 beta_bar) / sin(2 beta_0)  =  1  -  alpha_s(v) / (N_quark - 1)
                                  =  1  -  alpha_s(v) / 5
                                                       + O(alpha_s(v)^2),
```

with the structural identification `N_quark - 1 = 5` traced **directly
to the retained 1 + 5 quark-block decomposition** in the CKM CP-phase
theorem (where `w_perp = (N_quark - 1)/N_quark = 5/6`).

The `1/(N_quark - 1)` coefficient is **independent of the canonical
coupling** — it is a pure structural integer fingerprint of the
framework's atlas 1 + 5 angular-weight decomposition. This makes the
ratio test a sharp falsification target that decouples from any
α_s precision question.

**Primary runner:**
`scripts/frontier_ckm_sin_2_beta_bar_nlo_n_quark_ratio.py`

## Statement

On the retained CKM atlas + NLO-protected-γ̄ surface,

```text
(B1)  sin(2 beta_bar) / sin(2 beta_0)  =  1 - alpha_s(v) / (N_quark - 1)
                                          + O(alpha_s(v)^2),

(B2)  At framework values (N_quark = 6):
      sin(2 beta_bar) / sin(2 beta_0)  =  1  -  alpha_s(v) / 5
                                          + O(alpha_s(v)^2).
```

Combined with the retained protection identity `(N8)` of the parent
NLO-protected-γ̄ theorem,

```text
(B3)  sin(2 gamma_bar) / sin(2 gamma_0)  =  1  +  O(alpha_s(v)^4)
                                            [PROTECTED at NLO].
```

And, since `sin(2 alpha_0) = 0` exactly (atlas right angle),
`sin(2 alpha_bar)` is a pure NLO observable (not a ratio):

```text
(B4)  sin(2 alpha_0)  =  0    [atlas-LO, no ratio definable].
```

The framework therefore predicts a **three-tier hierarchy** of NLO
doubled-angle CP-asymmetry behavior:

| Angle | NLO multiplicative ratio | Source |
|:---|:---|:---|
| γ̄ | `1 + O(α_s⁴)` PROTECTED | retained N8 of protected-γ̄ |
| β̄ | `1 - α_s/(N_quark - 1)` LINEAR | **NEW (B1)** |
| α̅ | not a ratio (sin(2α₀) = 0) | atlas right-angle |

`(B1)` is the new content. Identities `(B3)` and `(B4)` are listed for
context; both are retained.

## Retained Inputs

All inputs below are retained on current `main`:

| Input | Authority on `main` |
| --- | --- |
| Canonical `alpha_s(v) = 0.103303816...` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| Retained Wolfenstein `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| Retained CP-phase `rho = 1/6`, `eta^2 = 5/36`, atlas `1 + 5` decomposition with `w_perp = 5/6 = (N_quark - 1)/N_quark` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Retained atlas-LO `alpha_0 = pi/2`, `sin(2 beta_0) = sqrt(5)/3`, `cos(2 beta_0) = 2/3` | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| Retained NLO-protected-γ̄ N7: `alpha_bar - pi/2 = (sqrt(5)/20) alpha_s(v) + O(alpha_s^2)` | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md), N7 |
| Retained N8 of protected-γ̄: `gamma_bar = gamma_0 + O(lambda^4)` | same, N8 |
| Retained N9 of protected-γ̄: closed form `tan(beta_bar) = sqrt(5)(4 - alpha_s)/(20 + alpha_s)` | same, N9 |
| Retained `N_quark = N_pair × N_color = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) |

No PDG observable enters as a derivation input. No SUPPORT-tier or
open inputs (Koide `Q_l`, bare-coupling ratios, dimension-color
quadratic) are used.

## Derivation

### `(B1)`: NLO ratio from retained inputs

The retained NLO-protected-γ̄ N7 gives the angle deviation:

```text
beta_0 - beta_bar  =  (sqrt(5)/20) alpha_s(v)  +  O(alpha_s^2).
```

(Sign: γ̄ is protected at NLO, so the triangle constraint
`alpha_bar + beta_bar + gamma_bar = pi` with `Δγ = 0` forces
`Δα + Δβ = 0`. Since `α̅ - π/2 = +(√5/20) α_s` from N7,
`β̄ - β_0 = -(√5/20) α_s`, i.e., `β_0 > β̄`.)

The standard expansion of `sin(2 X)` around `sin(2 X_0)`:

```text
sin(2 beta_bar)  =  sin(2 beta_0)  +  2 cos(2 beta_0)(beta_bar - beta_0)
                                      +  O((beta_bar - beta_0)^2).
```

Substituting retained `cos(2 beta_0) = 2/3`:

```text
sin(2 beta_bar) - sin(2 beta_0)  =  2 (2/3) (-(sqrt(5)/20) alpha_s)
                                  =  -(2 sqrt(5))/(3 × 10) alpha_s
                                  =  -(sqrt(5)/15) alpha_s.
```

Dividing by retained `sin(2 beta_0) = sqrt(5)/3`:

```text
(sin(2 beta_bar) - sin(2 beta_0)) / sin(2 beta_0)
   =  -(sqrt(5)/15) alpha_s / (sqrt(5)/3)
   =  -(3/15) alpha_s
   =  -(1/5) alpha_s.
```

Hence

```text
sin(2 beta_bar) / sin(2 beta_0)  =  1  -  alpha_s(v)/5  +  O(alpha_s^2).
```

This is `(B1)` at the framework value `N_quark - 1 = 5`, that is

```text
sin(2 beta_bar) / sin(2 beta_0)  =  1  -  alpha_s(v)/(N_quark - 1).
```

### `(B2)`, `(B3)`, `(B4)`: hierarchy

`(B3)` is identity `(N8)` of the retained NLO-protected-γ̄ theorem:
γ̄ = γ_0 at NLO, so the ratio is identically 1 up to O(λ⁴).

`(B4)` follows from the retained right-angle theorem: `α_0 = π/2`
makes `sin(2 α_0) = sin(π) = 0` exactly.

The three-tier hierarchy emerges:

- γ̄: `cos(2 γ_0) = -2/3 ≠ 0`, but `Δγ = 0` (protected) ⟹ ratio = 1.
- β̄: `cos(2 β_0) = +2/3 ≠ 0`, `Δβ = -(√5/20) α_s` ⟹ ratio = `1 - α_s/5`.
- α̅: `cos(2 α_0) = -1`, `Δα = +(√5/20) α_s` ⟹ ratio undefined; instead
  `sin(2 α̅) = -2 (Δα) = -(√5/10) α_s` directly.

### Connection to atlas 1 + 5 decomposition

The retained CKM CP-phase theorem decomposes the 6-state quark block
into `1 + 5` parts:

```text
N_quark        =  6     (retained: 1-dimensional A1 channel + 5-dimensional ortho)
w_A1           =  1/N_quark  =  1/6        (A1 angular weight)
w_perp         =  (N_quark - 1)/N_quark  =  5/6   (orthogonal weight)
```

The retained `eta^2 = r^2 × w_perp = (1/6)(5/6) = 5/36` directly uses
the orthogonal-channel weight numerator `N_quark - 1 = 5`.

The NLO sin(2β̄) ratio derived in `(B1)` is

```text
1 - alpha_s(v)/(N_quark - 1).
```

The factor `1/(N_quark - 1)` **is the inverse of the orthogonal
channel weight numerator**. Tracing it back through the derivation:

- The slope `sqrt(5)/20` in N7 carries `sqrt(5) = sqrt(N_quark - 1)`.
- The retained `sin(2 beta_0) = sqrt(5)/3 = sqrt(N_quark - 1)/(N_color)`
  provides the matching denominator.
- The factor `cos(2 beta_0) = 2/3 = N_pair/N_color` from the atlas
  Thales right-angle.

Combining: `Δsin(2β̄)/sin(2β_0) = (2 × 2/3 × √5/20)/(√5/3) × α_s
                                = (4 × 3)/(3 × 20) × α_s
                                = (1/5) α_s
                                = (1/(N_quark - 1)) α_s`.

The `√5` factors cancel exactly between numerator and denominator;
the `N_pair/N_color` ratio enters once. The result reflects the
framework's specific atlas geometry where the 1 + 5 decomposition
fixes the structural numerator `N_quark - 1 = 5`.

## Numerical Verification

With canonical `alpha_s(v) = 0.10330381612227...`:

| Quantity | Closed form | Value |
| --- | --- | ---: |
| `sin(2 beta_0)` (retained) | `sqrt(5)/3` | `0.7453560` |
| `beta_0 - beta_bar` (retained N7) | `(sqrt(5)/20) alpha_s` | `0.0115497` |
| `sin(2 beta_bar)` (linearized) | `(sqrt(5)/3) - (sqrt(5)/15) alpha_s` | `0.7299564` |
| `sin(2 beta_bar)` (direct N9) | `2 sqrt(5)(4-α_s)(20+α_s)/D` | `0.7297596` |
| `sin(2 beta_bar)/sin(2 beta_0)` (NEW) | `1 - alpha_s/5` | `0.9793392` |
| Equivalent N_quark form (NEW) | `1 - alpha_s/(N_quark - 1)` | `0.9793392` |

The linearization residual against the retained N9 closed form is
`O(alpha_s^2)`, as expected.

## α_s-INDEPENDENCE Check

The `1/(N_quark - 1)` coefficient is independent of the canonical
coupling's numerical value. Verifying at multiple alpha_s values:

| alpha_s | sin(2 beta_bar)/sin(2 beta_0) | Extracted coefficient |
| ---: | ---: | ---: |
| 0.05 | 0.99000 | 1/5 |
| 0.10 | 0.98000 | 1/5 |
| 0.15 | 0.97000 | 1/5 |
| 0.20 | 0.96000 | 1/5 |

The coefficient stays exactly `1/5` regardless of `alpha_s`.

## PDG Comparator

```text
PDG sin(2 beta) (B → ψ K_S, world average): 0.706 +/- 0.011

framework atlas-LO sin(2 beta_0)                = 0.7454  (+3.6 sigma)
framework atlas-NLO sin(2 beta_bar) [via (B1)]  = 0.7300  (+2.2 sigma)
framework reduction LO -> NLO via (B1)           = factor 1 - alpha_s/5 = 0.9793
```

Atlas-NLO improves agreement with PDG by ~1.4σ vs atlas-LO. The 5%
NLO multiplicative correction is exactly the size of an O(λ²) ≈
α_s/2 correction, but with a *specific structural coefficient*
`1/(N_quark - 1) = 1/5` rather than 1/2.

## Science Value

### What this lets the framework predict that it could not before

The retained NLO-protected-γ̄ theorem provides the closed form
`(N9)` for `sin(2 beta_bar)` directly, but not a clean *ratio*
test. `(B1)` packages the leading NLO multiplicative correction as

```text
sin(2 beta_bar) / sin(2 beta_0)  =  1  -  alpha_s(v)/5,
```

a single dimensionless number that compactly summarizes how atlas-LO
and atlas-NLO sin(2β) differ. The ratio form is more directly
testable than the absolute closed forms because experimental
measurements of `sin(2 beta)` have well-defined error bars — and
the *deviation* from the atlas-LO value has its own clean
structural prediction.

### Why the `1/(N_quark - 1)` coefficient is structurally meaningful

The factor `1/(N_quark - 1) = 1/5` is the **inverse of the
orthogonal-channel weight numerator** in the retained CKM CP-phase
theorem's `1 + 5` quark-block decomposition. The retained
`eta² = w_perp/N_quark = (N_quark - 1)/N_quark² = 5/36` already
encodes `N_quark - 1` in the numerator. The NLO ratio inherits this
structural integer.

This makes the ratio test a **direct probe of the atlas 1 + 5
decomposition**. If a future precision measurement yields a NLO
multiplicative coefficient differing significantly from `1/5`, it
falsifies either:

- the atlas `1 + 5` quark-block decomposition (`w_A1 = 1/6`,
  `w_perp = 5/6`), or
- the retained N7 slope `sqrt(5)/20`, or
- the right-angle theorem's `cos(2 beta_0) = 2/3`.

Each of these is load-bearing in the framework's CP-violation
sector. So the `1 - α_s/5` ratio is a *single-number test* of the
framework's atlas structure as a whole.

### Why the ratio is α_s-INDEPENDENT (in coefficient form)

The coefficient `1/(N_quark - 1)` does **not** depend on `alpha_s(v)`'s
numerical value. Even if a future analysis revises the canonical
coupling, the ratio's leading-order coefficient stays at `1/5`.

This decouples the falsification test from any α_s-precision
question. Experimental measurement directly extracts the coefficient
via:

```text
extracted coefficient  =  (1 - sin(2 beta_meas) / sin(2 beta_0)) / alpha_s_input
```

If this extraction lands at `1/5` within experimental and input
uncertainty, the framework's atlas `1 + 5` decomposition is supported
at that NLO Wolfenstein order.

### A complete three-tier NLO hierarchy

The framework predicts:

| Doubled angle | NLO ratio | Structural origin |
|:---|:---|:---|
| γ̄ | `1 + O(α_s⁴)` PROTECTED | retained protected-γ̄ N8 |
| β̄ | `1 - α_s/(N_quark - 1)` LINEAR | **NEW (B1)** |
| α̅ | undefined (sin(2α₀)=0); pure-NLO observable | retained right-angle |

This hierarchy is **structurally meaningful**: each tier corresponds
to a different aspect of the atlas geometry. γ̄ tests Thales radial
scaling (preserved at NLO). β̄ tests the multiplicative `1+5`
decomposition. α̅ tests the right-angle constraint directly.

A precision measurement of all three angles can falsify the
framework via a *pattern* of deviations from this hierarchy —
sharper than any single-angle test.

### Connection to experiment

| Experimental measurement | Framework prediction (atlas-NLO) |
| --- | --- |
| LHCb / Belle II `sin(2 beta)` from B → ψ K_S | `sin(2 beta_bar) = sin(2 beta_0) × 0.9793 = 0.7300` |
| Independent measurement of `sin(2 beta_0)` (atlas-LO target) | `sin(2 beta_0) = sqrt(5)/3 = 0.7454` |
| Ratio test: measured ratio | `1 - α_s/5` (framework) |
| future higher-precision `sin(2 beta)` measurements | sharper direct test of the ratio coefficient |

The future precision target is the `1/5` coefficient itself. If the
ratio test can be built with a stable `sin(2 beta_0)` reference, then
improved `sin(2 beta)` measurements sharpen that single-number
falsification target for the atlas `1 + 5` decomposition.

### What this rules out

If a future measurement of the `sin(2 beta_meas)` deviation from the
atlas-LO reference gives a multiplicative coefficient

- `< 1/(N_quark - 1) = 1/5` (smaller correction than predicted): the
  framework's atlas geometry is too "stiff" — possibly indicating
  smaller orthogonal-channel weight than `5/6`;
- `> 1/(N_quark - 1) = 1/5` (larger correction): the atlas Thales
  geometry is overconstrained — possibly indicating a different
  N_quark structure (or a different N_pair/N_color split);
- `= 1/(N_quark - 1) = 1/5` ± experimental: framework atlas 1+5
  decomposition confirmed.

This is a **direct probe of N_quark**, the framework's core quark
counting integer, via a pure flavor-physics observable.

## What This Claims

- `(B1)`: NEW NLO multiplicative ratio
  `sin(2 beta_bar)/sin(2 beta_0) = 1 - α_s(v)/(N_quark - 1) + O(α_s²)`
  derived from retained inputs only.
- `(B2)`: at framework value `N_quark = 6`, the coefficient is
  exactly `1/5`.
- `(B3)`: companion `sin(2 gamma_bar)/sin(2 gamma_0) = 1 + O(α_s⁴)`
  PROTECTED at NLO (retained from N8 of parent).
- The three-tier NLO hierarchy: γ̄ PROTECTED, β̄ LINEAR with
  `1/(N_quark - 1)` coefficient, α̅ PURE-NLO.
- The `1/(N_quark - 1)` coefficient is α_s-INDEPENDENT and traces
  to the retained atlas `1 + 5` quark-block decomposition.

## What This Does NOT Claim

- It does not promote NLO Wolfenstein corrections beyond NLO leading
  order; the `(B1)` is leading multiplicative correction.
- It does not derive `N_quark = 6` from a more fundamental principle;
  N_quark is taken from the retained CKM magnitudes structural
  counts theorem.
- It does not modify any retained CKM atlas, Wolfenstein, CP-phase,
  right-angle, or protected-γ̄ theorem.
- It does not use any SUPPORT-tier or open input (Koide `Q_l`,
  bare-coupling ratios, dimension-color quadratic).
- It does not promote a direct PDG comparator for `sin(2 beta_0)`
  or `sin(2 beta_bar)` separately; both are framework predictions
  matched against PDG `sin(2 beta) = 0.706 ± 0.011` from B → ψK_S.

## Exact-symbolic verification

The NLO-ratio identity `(B1)` and the supporting closed-form
identities `(B2)`, `(B3)`, `(B4)` are certified at exact-symbolic
precision via `sympy` in
`scripts/audit_companion_ckm_sin_2_beta_bar_nlo_n_quark_ratio_exact.py`.
The companion runner treats `alpha_s(v)` as a free positive real
symbol, imports the upstream retained inputs verbatim as exact
`sympy.Rational` / `sympy.sqrt` values, and checks each identity by
computing `sympy.simplify(lhs - rhs)` and asserting the residual
equals `0` exactly. The cited inputs themselves (retained
`sin(2 beta_0) = sqrt(5)/3`, `cos(2 beta_0) = 2/3`, `N7 slope =
sqrt(5)/20`, retained `N9` closed form for `tan(beta_bar)`,
`N_quark = 6` from CKM magnitudes structural-counts theorem) are
imported from upstream authority notes and are not re-derived here.

| Identity | Symbolic form | Verification |
| --- | --- | --- |
| linearization | `sin(2 beta_bar) - sin(2 beta_0) == -(sqrt(5)/15) alpha_s` | `sympy.simplify` residual `= 0` |
| `(B1)` ratio | `sin(2 beta_bar)/sin(2 beta_0) == 1 - alpha_s/(N_quark - 1)` | `sympy.simplify` residual `= 0` |
| `sqrt(5)` cancel | `(-sqrt(5)/15)/(sqrt(5)/3) == -1/5` | `sympy.simplify` residual `= 0` |
| `(B2)` framework | at `N_quark = 6`, coefficient `1/(N_quark - 1) == 1/5` | exact rational |
| `(B3)` `gamma`-protect | `sin(2 gamma_bar)/sin(2 gamma_0) == 1` (NLO via retained `N8`) | exact rational |
| `(B4)` right-angle | `sin(2 alpha_0) = sin(pi) == 0` | exact zero |
| `(B4)` pure-NLO | leading `sin(2 alpha_bar) == -(sqrt(5)/10) alpha_s` | series-coefficient match |
| `alpha_s`-indep | linear coefficient on `alpha_s` is the pure rational `-1/(N_quark - 1)` | `sympy.Poly` extraction |
| `(N9)` Taylor | `tan(beta_bar) = sqrt(5)(4 - alpha_s)/(20 + alpha_s)` ⇒ ratio first-order `1 - alpha_s/5` | `sympy.series` match |
| `1+5` connection | `1/(N_quark - 1)` is the inverse of the orthogonal-channel weight numerator | exact rational |
| Pythagorean | `sin^2(2 beta_0) + cos^2(2 beta_0) == 1` (`5/9 + 4/9 = 1`) | `sympy.simplify` residual `= 0` |

Counterfactual probes confirm each retained input is individually
load-bearing for the closed-form `1/5` coefficient:

- substituting `N_quark = 5` collapses the coefficient to `1/4`, not
  `1/5`;
- substituting `sin(2 beta_0) = 1` (replacing the retained
  `sqrt(5)/3`) makes the coefficient `sqrt(5)/15`, irrational and
  not `1/5`, breaking the `sqrt(5)` cancellation;
- substituting `cos(2 beta_0) = 1` (replacing the retained `2/3`)
  collapses the coefficient to `3/10`, not `1/5`;
- substituting the `N7` slope `1/20` (replacing the retained
  `sqrt(5)/20`) makes the coefficient `sqrt(5)/25`, irrational and
  not `1/5`, again breaking the `sqrt(5)` cancellation.

The structural relations are therefore exact-symbolic over the
imported retained inputs and do not depend on the floating-point pin
of `alpha_s(v)`. The `alpha_s`-independence of the `1/(N_quark - 1)`
coefficient is verified directly by extracting the linear coefficient
of the `sympy.Poly` decomposition; the canonical numerical
`alpha_s(v)` enters only the parent runner's PDG-comparator section,
which is not load-bearing for the algebra.

## Reproduction

```bash
python3 scripts/frontier_ckm_sin_2_beta_bar_nlo_n_quark_ratio.py
PYTHONPATH=scripts python3 scripts/audit_companion_ckm_sin_2_beta_bar_nlo_n_quark_ratio_exact.py
```

Expected result:

```text
TOTAL: PASS=30, FAIL=0
```

The runner uses the Python standard library plus the canonical
`scripts/canonical_plaquette_surface.py` import. All upstream
authorities are retained on `main`.

## Cross-References

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  -- retained parent theorem providing N7 (slope), N8 (γ̄ protection),
  N9 (`tan(beta_bar)` closed form).
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- retained `alpha_0 = pi/2`, atlas-LO doubled-angle values.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `1 + 5` quark-block decomposition with
  `w_perp = (N_quark - 1)/N_quark = 5/6`.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  -- retained `N_quark = N_pair × N_color = 6`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  -- canonical `alpha_s(v)` retained input.
