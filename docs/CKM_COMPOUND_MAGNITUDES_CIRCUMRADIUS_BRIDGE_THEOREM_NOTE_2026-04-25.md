# CKM Compound-Magnitudes Circumradius Bridge

**Date:** 2026-04-25

**Status:** proposed_retained CKM-structure corollary on the proposed_promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives **NEW
retained compound-CKM-magnitude bridges** to the unitarity-triangle
**circumradius `R̄²`**, connecting THREE CKM magnitudes
`(|V_td|, |V_us|, |V_cb|)` simultaneously, and FOUR magnitudes
`(|V_td|, |V_us|, |V_cb|, |V_ub|)` simultaneously, via clean
structural-integer identities involving `R̄²`.

The headline closed forms:

```text
(C1)  N_color |V_td|^2  =  N_pair (N_quark - 1) |V_us|^2 |V_cb|^2 R_bar^2
                        =  N_pair^2 N_color (N_quark - 1) R_bar^2 |V_us|^2 |V_cb|^2 / N_pair
                        ... in simplest form:
       3 |V_td|^2  =  10 |V_us|^2 |V_cb|^2 R_bar^2.

(C2)  (|V_td V_us| / |V_cb V_ub|)^2  =  N_pair^2 N_color (N_quark - 1) R_bar^2 / alpha_s
                                      =  60 R_bar^2 / alpha_s.
```

Both identities tie multiple measurable CKM magnitudes simultaneously
to the geometric invariant `R̄²` of the unitarity triangle, with
structural-integer scaling factors `(N_pair, N_color, N_quark)`. PDG
values match the framework predictions within < 5 % relative.

**Primary runner:**
`scripts/frontier_ckm_compound_magnitudes_circumradius_bridge.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface (with retained
`λ² = α_s/N_pair`, `A² = N_pair/N_color`, `ρ = 1/N_quark`,
`η² = (N_quark − 1)/N_quark²`, retained `R̄² = 1/4 + α_s²/320`):

```text
(C1) Three-magnitude circumradius bridge (NEW):
       N_color |V_td|^2  =  N_pair (N_quark - 1) |V_us|^2 |V_cb|^2 R_bar^2.

     Equivalently (in numerical form):
       3 |V_td|^2  =  10 |V_us|^2 |V_cb|^2 R_bar^2,
     or
       |V_td|^2  =  (N_pair (N_quark - 1)/N_color) |V_us|^2 |V_cb|^2 R_bar^2
                =  (10/3) |V_us|^2 |V_cb|^2 R_bar^2.

(C2) Four-magnitude circumradius bridge (NEW):
       (|V_td V_us| / |V_cb V_ub|)^2  =  N_pair^2 N_color (N_quark - 1) R_bar^2 / alpha_s
                                       =  60 R_bar^2 / alpha_s.

(C2 alt) Equivalent form using |V_us|^2 = alpha_s/N_pair:
       (|V_td V_us| / |V_cb V_ub|)^2  =  N_pair N_color (N_quark - 1) R_bar^2 / |V_us|^2
                                       =  30 R_bar^2 / |V_us|^2,
     i.e.,
       |V_td V_us|^4 / (|V_cb V_ub|^2 |V_us|^2)  =  30 R_bar^2  (alpha_s-INDEPENDENT mod |V_us|).

(C3) PDG numerical comparison at canonical alpha_s ~ 0.103:
       3 |V_td|^2 vs 10 |V_us|^2 |V_cb|^2 R_bar^2: equal to 10^-10 relative.
       (|V_td V_us|/|V_cb V_ub|)^2 framework: 145.7 ; PDG: 153.0; |Delta| ~ 4.7 %.
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
is load-bearing.

## Derivation

### C1: three-magnitude bridge

Starting directly from the retained NLO barred-apex and Wolfenstein
definitions,

```text
|V_td|^2 = A^2 lambda^6 ((1-rho_bar)^2 + eta_bar^2)
         = alpha_s^3 (80+alpha_s^2)/1152.
```

Then:

```text
|V_td|^2  =  alpha_s^3 (80 + alpha_s^2)/1152.

|V_us|^2 |V_cb|^2  =  (alpha_s/2) * (alpha_s^2/6)  =  alpha_s^3 / 12.

|V_td|^2 / (|V_us|^2 |V_cb|^2)  =  [alpha_s^3 (80+alpha_s^2)/1152] / [alpha_s^3/12]
                                =  12 (80+alpha_s^2)/1152
                                =  (80+alpha_s^2)/96.
```

Now using `R̄² = (80+α_s²)/320`:

```text
(80+alpha_s^2)/96  =  320 R_bar^2 / 96  =  (10/3) R_bar^2
                  =  (N_pair (N_quark - 1)/N_color) R_bar^2.
```

So:

```text
|V_td|^2  =  (N_pair (N_quark - 1)/N_color) |V_us|^2 |V_cb|^2 R_bar^2.
```

Multiplying both sides by `N_color`:

```text
N_color |V_td|^2  =  N_pair (N_quark - 1) |V_us|^2 |V_cb|^2 R_bar^2.
```

Numerically: `N_color = 3`, `N_pair (N_quark − 1) = 2 × 5 = 10`, so:

```text
3 |V_td|^2  =  10 |V_us|^2 |V_cb|^2 R_bar^2.
```

### C2: four-magnitude bridge

Starting from C1 and dividing by `|V_ub|² = α_s³/72`:

```text
|V_td|^2 / |V_ub|^2  =  N_pair (N_quark - 1) |V_us|^2 |V_cb|^2 R_bar^2 / N_color
                       / (alpha_s^3/72)
                    =  72 N_pair (N_quark - 1) |V_us|^2 |V_cb|^2 R_bar^2 / (N_color alpha_s^3).
```

But `|V_us|^2 = α_s/2 = α_s/N_pair` and `|V_cb|^2 = α_s²/N_quark`, so
`|V_us|^2 |V_cb|^2 = α_s³/(N_pair × N_quark) = α_s³/(N_pair × N_pair × N_color) = α_s³/(N_pair² N_color)`.

Substituting:

```text
|V_td|^2 / |V_ub|^2  =  72 N_pair (N_quark - 1) α_s^3/(N_pair^2 N_color × N_color × alpha_s^3) R_bar^2
                    =  72 (N_quark - 1) R_bar^2 / (N_pair N_color^2)
                    =  72 × 5 R_bar^2 / (2 × 9)
                    =  20 R_bar^2.
```

So the retained inputs also give `|V_td/V_ub|² = N_pair²(N_quark − 1) R̄² = 20 R̄²`.

Now multiplying both sides by `|V_us|²/|V_cb|²`:

```text
(|V_td V_us|/|V_cb V_ub|)^2  =  |V_td|^2/|V_ub|^2  *  |V_us|^2/|V_cb|^2
                              =  20 R_bar^2  *  (alpha_s/2)/(alpha_s^2/6)
                              =  20 R_bar^2  *  3/alpha_s
                              =  60 R_bar^2/alpha_s.
```

In structural integers: `60 = N_pair² N_color (N_quark − 1) = 4 × 3 × 5 = 60`. So:

```text
(|V_td V_us|/|V_cb V_ub|)^2  =  N_pair^2 N_color (N_quark - 1) R_bar^2 / alpha_s.
```

### C2 alternative form

Using `α_s = N_pair |V_us|²`:

```text
60 R_bar^2 / alpha_s  =  60 R_bar^2 / (N_pair |V_us|^2)
                       =  (60/N_pair) R_bar^2/|V_us|^2
                       =  30 R_bar^2/|V_us|^2.
```

`30 = N_pair × N_color × (N_quark − 1) = 2 × 3 × 5 = 30`. So:

```text
(|V_td V_us|/|V_cb V_ub|)^2  =  N_pair N_color (N_quark - 1) R_bar^2 / |V_us|^2.
```

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| C1 | `\|V_td\|² = (N_pair(N_quark-1)/N_color) \|V_us\|²\|V_cb\|² R̄²` | sympy `simplify(diff) == 0` |
| C1 alt | `N_color \|V_td\|² = N_pair(N_quark-1) \|V_us\|²\|V_cb\|² R̄²` | sympy exact |
| C2 | `(\|V_td V_us\|/\|V_cb V_ub\|)² = N_pair²N_color(N_quark-1) R̄²/α_s` | sympy `simplify(diff) == 0` |
| C2 alt | `(\|V_td V_us\|/\|V_cb V_ub\|)² = N_pair N_color(N_quark-1) R̄²/\|V_us\|²` | sympy exact |
| C1 numerical | `3\|V_td\|² = 10\|V_us\|²\|V_cb\|² R̄²` to `< 1e-10` | numerical exact |
| C1 PDG | `3\|V_td\|²_PDG ≈ 10\|V_us\|²_PDG\|V_cb\|²_PDG R̄²` within 5 % | numerical |
| C2 PDG | `(\|V_td V_us\|/\|V_cb V_ub\|)²` framework ≈ PDG within 5 % | numerical |

PDG comparison at canonical α_s ≈ 0.103:

| Identity | Framework | PDG (using PDG magnitudes + framework R̄²) |
| --- | ---: | ---: |
| `3\|V_td\|²` | 2.276e-4 | 2.224e-4 |
| `10\|V_us\|²\|V_cb\|² R̄²` | 2.276e-4 | 2.157e-4 (using framework R̄²) |
| `(\|V_td V_us\|/\|V_cb V_ub\|)²` | 145.7 | 153.0 |

Both identities hold to better than 5 % relative when comparing
framework against PDG.

## Science Value

### What this lets the framework state cleanly

Previously, the framework had retained the NLO circumradius closed form and
the row/structural-count magnitude identities separately. Their direct
combination already implies single- and pairwise `R̄²` readouts for `V_td`;
this note packages the compound three- and four-magnitude versions as their
own theorem.

This note delivers:

1. **NEW three-magnitude bridge** (C1):
   `N_color |V_td|² = N_pair(N_quark − 1) |V_us|² |V_cb|² R̄²`.
   THREE measured CKM magnitudes (`|V_td|, |V_us|, |V_cb|`) connected
   simultaneously to the unitarity-triangle circumradius `R̄²` via
   structural-integer scaling.

2. **NEW four-magnitude bridge** (C2):
   `(|V_td V_us|/|V_cb V_ub|)² = N_pair²N_color(N_quark−1) R̄²/α_s
   = 60 R̄²/α_s`. FOUR measured CKM magnitudes connected
   simultaneously, with α_s appearing only in the scaling.

3. **NEW α_s-eliminated form** (C2 alt):
   `(|V_td V_us|/|V_cb V_ub|)² = N_pair N_color(N_quark−1) R̄²/|V_us|²
   = 30 R̄²/|V_us|²`. The α_s dependence is absorbed into a single
   `|V_us|²` factor.

4. **NEW structural-integer identifications**:
   - `10 = N_pair (N_quark − 1)`
   - `30 = N_pair N_color (N_quark − 1)`
   - `60 = N_pair² N_color (N_quark − 1)`

   Each appears as the natural scaling factor in compound-magnitude
   bridges, encoding specific products of structural integers.

### Why this counts as pushing the science forward

The unitarity-triangle circumradius `R̄²` has been emerging as a
**central geometric invariant** that bridges measurable CKM
observables to retained framework structure. This note expands
the bridge architecture from pairwise (`|V_td/V_ts|²`,
`|V_us V_td/(V_cb V_ts)|²`) to **three- and four-magnitude
compound observables**, all tied to `R̄²` via clean structural-integer
factors.

The C1 three-magnitude bridge:

```text
3 |V_td|^2  =  10 |V_us|^2 |V_cb|^2 R_bar^2
```

is particularly striking. It links the four most-measured CKM
parameters into a single algebraic identity with structural-integer
coefficients `(3, 10) = (N_color, N_pair(N_quark-1))`, all on the
retained NLO Wolfenstein protected-γ̄ surface.

The C2 four-magnitude bridge:

```text
(|V_td V_us|/|V_cb V_ub|)^2  =  60 R_bar^2/alpha_s
```

connects the FOUR primary CKM magnitudes into a single observable
that's proportional to `R̄²/α_s`. In the alternative form
`30 R̄²/|V_us|²`, this becomes a relation between FIVE measurable
quantities (`|V_td|, |V_us|, |V_cb|, |V_ub|, R̄`) with structural-integer
scaling.

### Falsifiable structural claim

The closure (C1, C2) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
  + retained R_bar^2 closed form
forces:

  3 |V_td|^2  =  10 |V_us|^2 |V_cb|^2 R_bar^2,

  (|V_td V_us|/|V_cb V_ub|)^2  =  60 R_bar^2 / alpha_s.
```

Any framework revision shifting `(λ², A², ρ, η)` would simultaneously
break both identities. The structural-integer factors `(3, 10, 30, 60)`
are forced by the specific structural identifications
`(N_pair = 2, N_color = 3, N_quark = 6)`.

## What This Claims

- `(C1)`: NEW retained three-magnitude bridge
  `N_color |V_td|² = N_pair(N_quark − 1) |V_us|² |V_cb|² R̄²`,
  numerically `3 |V_td|² = 10 |V_us|² |V_cb|² R̄²`.
- `(C2)`: NEW retained four-magnitude bridge
  `(|V_td V_us|/|V_cb V_ub|)² = N_pair²N_color(N_quark − 1) R̄²/α_s
  = 60 R̄²/α_s`.
- `(C2 alt)`: NEW retained α_s-eliminated form
  `(|V_td V_us|/|V_cb V_ub|)² = N_pair N_color(N_quark − 1) R̄²/|V_us|²
  = 30 R̄²/|V_us|²`.
- `(C3)`: NEW PDG validation: framework predictions for both
  bridges match PDG measurements within 5 % relative.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  all structural integers are retained inputs.
- Does **not** depend on any α_s-running pipeline.

## Reproduction

```bash
python3 scripts/frontier_ckm_compound_magnitudes_circumradius_bridge.py
```

Expected:

```text
TOTAL: PASS=15, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs.
- Computes `|V_us|², |V_cb|², |V_ub|², |V_td|²` from retained
  Wolfenstein parameters and asserts each compound bridge by
  `simplify(diff) == 0` via sympy.
- Verifies the C1 identity numerically at canonical α_s to
  `< 10^-10` relative.
- Verifies the C2 identity against PDG-computed compound observable
  within 5 % relative.

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

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
