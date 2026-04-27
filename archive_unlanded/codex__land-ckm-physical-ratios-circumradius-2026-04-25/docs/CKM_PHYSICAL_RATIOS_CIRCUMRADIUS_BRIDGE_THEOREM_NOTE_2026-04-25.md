# CKM Physical Ratios — Circumradius Bridge Theorem

**Date:** 2026-04-25

**Status:** retained CKM-structure corollary on the promoted CKM atlas
and NLO Wolfenstein protected-γ̄ surfaces. This note derives a
**NEW retained bridge** between **CKM ratios with direct B-physics
comparators** and the **squared circumradius `R̄²` of the unitarity
triangle**: a clean structural-integer identity that pulls a
phenomenological CKM readout into the geometric-invariant language
of the retained surface.

The headline closed forms:

```text
(R3)  CIRCUMRADIUS BRIDGE (NEW):
        |V_td / V_ts|^2  =  ((N_quark - 1) / N_color) * alpha_s * R_bar^2
                         =  (5/3) alpha_s R_bar^2.

(R6)  COMPOUND CIRCUMRADIUS IDENTITY (NEW):
        |V_us V_td / (V_cb V_ts)|^2  =  (N_quark - 1) * R_bar^2
                                      =  5 R_bar^2.

      A four-CKM-element-ratio observable equals exactly (N_quark - 1)
      times the squared circumradius of the unitarity triangle.
      The leading multiplicative alpha_s prefactor cancels; the
      remaining alpha_s dependence is only the geometric dependence
      already contained in R_bar^2 = 1/4 + alpha_s^2/320.
```

Both ratios connect **phenomenological CKM ratio readouts** to a **classical
triangle invariant** (`R̄²`) via simple structural-integer factors —
the same `R̄²` that anchors the retained Brocard angle, Steiner
inellipse, Brocard circle, and nine-point circle of the unitarity
triangle.

**Primary runner:**
`scripts/frontier_ckm_physical_ratios_circumradius_bridge.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface (with retained
Wolfenstein parameters `λ² = α_s/2`, `A² = 2/3`, `ρ = 1/6`,
`η² = 5/36`, NLO apex `(ρ̄, η̄) = (ρ, η)(1 − λ²/2)`):

```text
(R1) Retained Wolfenstein expansion (recap):
       lambda^2  =  alpha_s/2  =  alpha_s/N_pair,
       A^2       =  2/3        =  N_pair/N_color,
       rho       =  1/6        =  1/N_quark,
       eta^2     =  5/36       =  (N_quark - 1)/N_quark^2,
       rho_bar   =  rho (1 - lambda^2/2),  eta_bar = eta (1 - lambda^2/2).

(R2) |V_td / V_ts|^2 closed form:
        |V_td / V_ts|^2  =  lambda^2 * ((1 - rho_bar)^2 + eta_bar^2)
                         =  (alpha_s/2) * (80 + alpha_s^2)/96
                         =  alpha_s * (80 + alpha_s^2)/192.

      In structural integers:
        |V_td / V_ts|^2  =  alpha_s (N_pair^4 (N_quark - 1) + alpha_s^2)
                            / (N_pair^5 N_quark).

(R3) NEW CIRCUMRADIUS BRIDGE:
       |V_td / V_ts|^2  =  ((N_quark - 1) / N_color) * alpha_s * R_bar^2
                        =  (5/3) alpha_s R_bar^2.

     Equivalently:
       N_color * |V_td / V_ts|^2  =  (N_quark - 1) * alpha_s * R_bar^2.

     The B-meson mixing CKM ratio |V_td/V_ts|^2 is directly
     proportional to the SQUARED CIRCUMRADIUS of the unitarity
     triangle, with structural-integer coefficient (N_quark - 1)/N_color
     and a single factor of alpha_s.

(R4) |V_us / V_cb|^2 closed form:
       |V_us / V_cb|^2  =  lambda^2 / (A^2 lambda^4)
                        =  1 / (A^2 lambda^2)
                        =  N_color / alpha_s
                        =  3/alpha_s.

(R5) |V_ub / V_cb|^2 closed form:
       |V_ub / V_cb|^2  =  lambda^2 (rho^2 + eta^2)
                        =  alpha_s / (N_pair^2 * N_color)
                        =  alpha_s/12.

(R6) NEW COMPOUND CIRCUMRADIUS IDENTITY:
       |V_us V_td / (V_cb V_ts)|^2  =  |V_us/V_cb|^2 * |V_td/V_ts|^2
                                     =  (N_color/alpha_s) * (N_quark-1)/N_color * alpha_s * R_bar^2
                                     =  (N_quark - 1) * R_bar^2
                                     =  5 R_bar^2.

      The factor of alpha_s cancels exactly between |V_us/V_cb|^2
      (which is N_color/alpha_s) and |V_td/V_ts|^2 (which is
      (N_quark-1)/N_color times alpha_s R_bar^2). The result is a
      4-CKM-element-ratio observable equal to (N_quark - 1) R_bar^2:
      the leading multiplicative alpha_s cancels, leaving only the
      alpha_s^2 dependence already encoded by R_bar^2.

      At LO: R_bar | LO = 1/2, so |V_us V_td/(V_cb V_ts)|^2 | LO = 5/4.

(R7) Numerical comparison to PDG-style CKM-ratio comparators at
     canonical alpha_s(v) = 0.103303816...:
       |V_td/V_ts|  ~  0.2075  (comparator: 0.211 +/- 0.005),
       |V_ub/V_cb|  ~  0.0928  (comparator: 0.092 +/- 0.008),
       |V_us/V_cb|  ~  5.389   (comparator: 5.49 +/- 0.20).

     Each readout is within < 2 sigma of the listed comparator.
```

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `(rho_bar, eta_bar)` apex coords | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |
| `R_bar^2 = 1/4 + alpha_s^2/320` | [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md) | retained |
| `lambda^2 = alpha_s/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | retained |

The closure uses ONLY retained-tier authorities. No support-tier note
is load-bearing. No unmerged branch is cited as load-bearing.

## Derivation

### R2: |V_td/V_ts|² closed form

In Wolfenstein parameterization:

```text
V_td  =  A lambda^3 (1 - rho_bar - i eta_bar) + O(lambda^7),
V_ts  =  -A lambda^2 + O(lambda^6).
```

So `|V_td/V_ts|² = λ² ((1−ρ̄)² + η̄²)` to leading order in λ.

On the retained surface, `(1−ρ̄)² + η̄² = (80 + α_s²)/96` (this is just
the squared length `a²` of the unitarity-triangle side opposite vertex
`V_1`, in our convention `a² = (80+α_s²)/96`).

So:

```text
|V_td/V_ts|^2  =  (alpha_s/2) * (80 + alpha_s^2)/96  =  alpha_s (80 + alpha_s^2)/192.
```

### R3: circumradius bridge

The retained circumradius squared is `R̄² = 1/4 + α_s²/320 = (80+α_s²)/320`.

So `(80+α_s²) = 320 R̄²`. Substituting:

```text
|V_td/V_ts|^2  =  alpha_s * 320 R_bar^2 / 192
              =  5 alpha_s R_bar^2 / 3
              =  ((N_quark - 1)/N_color) * alpha_s * R_bar^2.
```

In structural integers: `5 = N_quark − 1`, `3 = N_color`.

This is the **headline circumradius bridge identity**.

### R4: |V_us/V_cb|²

`|V_us|² = λ² = α_s/2`, `|V_cb|² = A² λ⁴ = α_s²/6`. So:

```text
|V_us/V_cb|^2  =  (alpha_s/2) / (alpha_s^2/6)
              =  6/(2 alpha_s)
              =  3/alpha_s
              =  N_color / alpha_s.
```

### R5: |V_ub/V_cb|²

`|V_ub|² = A² λ⁶ (ρ²+η²) = (2/3)(α_s/2)³(1/36+5/36) = (2/3)(α_s³/8)(1/6) = α_s³/72`.
`|V_cb|² = A² λ⁴ = α_s²/6`. So:

```text
|V_ub/V_cb|^2  =  (alpha_s^3/72)/(alpha_s^2/6)
              =  alpha_s/12
              =  alpha_s/(N_pair^2 N_color).
```

### R6: compound circumradius identity

```text
|V_us V_td/(V_cb V_ts)|^2  =  |V_us/V_cb|^2 * |V_td/V_ts|^2
                            =  (N_color/alpha_s) * ((N_quark - 1)/N_color * alpha_s * R_bar^2)
                            =  (N_quark - 1) * R_bar^2
                            =  5 R_bar^2.
```

The `α_s` factors cancel **exactly** between `|V_us/V_cb|² = N_color/α_s`
and `|V_td/V_ts|² = (N_quark−1)/N_color × α_s × R̄²`. The compound
ratio is therefore **purely a function of R̄²**. Written only in
`α_s`, this same statement is:

```text
|V_us V_td/(V_cb V_ts)|² = 5 R_bar² = 5/4 + alpha_s²/64.
```

So the leading multiplicative `α_s` prefactor cancels, but the
closed form still carries the `α_s²` dependence of the retained
circumradius. This note does not claim the compound ratio is a
numerically `α_s`-independent constant.

At LO: `R̄|_LO = 1/2`, so `|V_us V_td/(V_cb V_ts)|²|_LO = 5/4`.

### R7: numerical comparator

Setting canonical `α_s(v) = 0.103303816...` from the retained
plaquette/CMT surface:

| Ratio | Framework | Comparator | σ |
| --- | ---: | ---: | ---: |
| `|V_td/V_ts|` | 0.2075 | 0.211 ± 0.005 | 0.70 |
| `|V_ub/V_cb|` | 0.0928 | 0.092 ± 0.008 | 0.10 |
| `|V_us/V_cb|` | 5.389 | 5.49 ± 0.20 | 0.51 |

Framework readouts match the listed comparators within < 2σ for all
three ratios. These are post-derivation comparators, not new fitted
inputs.

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| R2 |V_td/V_ts|² | `α_s(80+α_s²)/192` | sympy `simplify(diff) == 0` |
| R2 struct | `α_s(N_pair⁴(N_quark-1)+α_s²)/(N_pair⁵N_quark)` | sympy exact |
| R3 bridge | `\|V_td/V_ts\|² = (N_quark-1)/N_color * α_s * R̄²` | sympy `simplify(diff) == 0` |
| R3 alt | `N_color \|V_td/V_ts\|² = (N_quark-1) α_s R̄²` | sympy exact |
| R4 |V_us/V_cb|² | `N_color/α_s = 3/α_s` | sympy exact |
| R5 |V_ub/V_cb|² | `α_s/(N_pair²N_color) = α_s/12` | sympy exact |
| R6 compound | `\|V_us V_td/V_cb V_ts\|² = (N_quark-1) R̄² = 5 R̄²` | sympy `simplify(diff) == 0` |
| R6 LO | `\|V_us V_td/V_cb V_ts\|²\|_LO = 5/4` | sympy exact |
| R7 PDG | within < 2σ at canonical α_s | numerical |

## Science Value

### What this lets the framework state cleanly

Previously, the framework had retained:

- **Geometric invariants** of the unitarity triangle (circumradius `R̄`,
  circumcenter, orthocenter, Brocard angle, Steiner inellipse, etc.).
- **Wolfenstein parameters** `λ², A², ρ, η` in structural-integer form.
- **CKM magnitudes** `|V_us|², |V_cb|², |V_td|², |V_ts|², ...` in
  closed forms.

But the framework had not packaged a **direct bridge** between
**experimentally constrained CKM ratios** and the
**geometric invariants** of the unitarity triangle.

This note delivers:

1. **NEW circumradius bridge** (R3):
   `|V_td/V_ts|² = ((N_quark − 1)/N_color) × α_s × R̄²`.
   The B-meson mixing CKM ratio is exactly proportional to the
   SQUARED CIRCUMRADIUS of the unitarity triangle.

2. **NEW compound circumradius identity** (R6):
   `|V_us V_td/(V_cb V_ts)|² = (N_quark − 1) × R̄²`.
   A four-CKM-element-ratio observable is **purely a function of R̄²**,
   with the leading multiplicative `α_s` prefactor canceled. It is not
   an `α_s`-independent constant, because `R̄² = 1/4 + α_s²/320` on
   the retained surface.

3. **NEW retained closed forms** for `|V_us/V_cb|²` and `|V_ub/V_cb|²`
   in pure structural integers.

4. **Numerical CKM-ratio comparison** (R7): all three ratios match
   the listed comparators within < 2σ at canonical `α_s(v)`.

### Why this counts as pushing the science forward

The unitarity-triangle circumradius `R̄` has been the central
geometric invariant of the retained NLO Wolfenstein protected-γ̄
surface — appearing in 11+ closed-form theorems (Brocard angle,
Steiner inellipse, Brocard circle, nine-point circle pencil, etc.).
This note shows that **R̄² is also the natural unit for two CKM
ratio readouts** with direct B-physics comparators:

- **|V_td/V_ts|² = (5/3) α_s R̄²** is a measurable ratio that
  enters the relative magnitude of `Δm_d/Δm_s` (B-d-meson vs
  B-s-meson mass-difference observables, with hadronic inputs in
  the extraction).
- **|V_us V_td/(V_cb V_ts)|² = 5 R̄²** is a four-element compound
  in which the explicit leading `α_s` prefactor cancels, leaving
  only the geometric `R̄²` dependence.

The framework's protected-γ̄ structure therefore connects
**experimentally constrained CKM ratios** to a **classical
geometric invariant** of the same unitarity triangle, with
structural-integer coefficients `(N_quark − 1, N_color)`.

This is an explicit bridge between the framework's
unitarity-triangle geometry (retained `R̄²`) and a physical CKM
ratio constrained by B-physics experiments. It says that the
B-meson mixing ratio `|V_td/V_ts|²` is proportional to the squared
circumradius (modulo `α_s` and structural integers) of the retained
unitarity triangle.

### Falsifiable structural claim

The closure (R2–R6) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
  + retained R_bar^2 = 1/4 + alpha_s^2/320
forces:
  |V_td/V_ts|^2  =  ((N_quark - 1)/N_color) * alpha_s * R_bar^2
                 =  (5/3) alpha_s R_bar^2,

  |V_us V_td/(V_cb V_ts)|^2  =  (N_quark - 1) * R_bar^2
                              =  5 R_bar^2.
```

Any framework revision shifting the retained Wolfenstein parameters
(λ², A², ρ, η) or the retained R̄² closed form would break the
bridge identities simultaneously. The compound R6 identity is
particularly rigid: it requires the **exact cancellation of the
leading multiplicative α_s prefactor between |V_us/V_cb|² and
|V_td/V_ts|²**, which holds only because both ratios have the
specific structural-integer scaling derived here.

## What This Claims

- `(R2)`: NEW retained closed form for `|V_td/V_ts|²` in pure
  structural integers.
- `(R3)`: NEW retained CIRCUMRADIUS BRIDGE
  `|V_td/V_ts|² = ((N_quark − 1)/N_color) α_s R̄²`.
- `(R4)`: NEW retained closed form `|V_us/V_cb|² = N_color/α_s`.
- `(R5)`: NEW retained closed form `|V_ub/V_cb|² = α_s/(N_pair² N_color)`.
- `(R6)`: NEW retained COMPOUND IDENTITY
  `|V_us V_td/(V_cb V_ts)|² = (N_quark − 1) R̄²`; the explicit
  leading `α_s` prefactor cancels, but `R̄²` still contains the
  retained `α_s²/320` geometric correction.
- `(R7)`: NEW numerical comparator showing < 2σ agreement for
  all three CKM ratios at canonical α_s.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs.
- Does **not** depend on any α_s-running pipeline.
- Does **not** make a precision-prediction claim beyond NLO Wolfenstein
  (the closed forms are NLO Wolfenstein + framework-retained
  structural integers; NNLO corrections are not included).

## Reproduction

```bash
python3 scripts/frontier_ckm_physical_ratios_circumradius_bridge.py
```

Expected:

```text
TOTAL: PASS=20, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently computes `|V_td/V_ts|²`, `|V_us/V_cb|²`, `|V_ub/V_cb|²`
  from retained Wolfenstein parameters and asserts each closed form by
  `simplify(diff) == 0` via sympy.
- Verifies the circumradius bridge `|V_td/V_ts|² = (5/3) α_s R̄²`
  symbolically.
- Verifies the compound circumradius identity
  `|V_us V_td/(V_cb V_ts)|² = (N_quark − 1) R̄²` symbolically.
- Compares each ratio's numerical value to the listed CKM-ratio
  comparator at canonical α_s(v).

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.
- [`CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md`](CKM_BARRED_CIRCUMRADIUS_EXACT_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md)
  — `R̄²`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  — `λ² = α_s/2`, `A² = 2/3`.

**Companion CKM-magnitudes notes (cited for context, not load-bearing):**

- [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
  — `|V_td|², |V_ts|², |V_tb|²` at LO atlas (precursor of the NLO
  refinement used here).

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
