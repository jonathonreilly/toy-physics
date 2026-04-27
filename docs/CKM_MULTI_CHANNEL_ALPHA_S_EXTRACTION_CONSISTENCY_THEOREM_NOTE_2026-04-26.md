# CKM Multi-Channel α_s Extraction Consistency Theorem

**Date:** 2026-04-26

**Status:** proposed_retained CKM-structure corollary on the proposed_promoted CKM atlas
+ NLO Wolfenstein protected-γ̄ surfaces. This note derives the
**framework's multi-channel α_s extraction consistency** — the
retained CKM magnitude identities allow α_s to be extracted
**independently** from each of the four primary CKM magnitudes
`(|V_us|, |V_cb|, |V_ub|, |V_td|)` via clean structural-integer
formulas. **The framework predicts that all four extractions agree.**
PDG central values confirm this consistency to **1.75 %** relative spread.
Within the explicit small-integer scan
`(N_pair' in {1,2,3,4}, N_color' in {1,2,3,4,5})`, with
`N_quark' = N_pair' N_color'`, **no other assignment gives a smaller
four-channel spread**, providing an empirical uniqueness check for the
framework's structural integers.

The headline closed forms — **the four extraction channels**:

```text
(E1)  alpha_s_from_|V_us|  =  N_pair * |V_us|^2  =  2 * |V_us|^2.

(E2)  alpha_s_from_|V_cb|  =  sqrt(N_quark) * |V_cb|  =  sqrt(6) * |V_cb|.

(E3)  alpha_s_from_|V_ub|  =  (N_pair * N_quark^2 * |V_ub|^2)^(1/3)
                            =  (72 * |V_ub|^2)^(1/3).

(E4)  alpha_s_from_|V_td|  =  numerical inversion of
                              |V_td|^2 = alpha_s^3 (80 + alpha_s^2)/1152.
```

PDG-extracted values (using PDG central CKM magnitudes):

| Channel | α_s extracted |
| --- | ---: |
| E1: from |V_us| | 0.1006 |
| E2: from |V_cb| | 0.1004 |
| E3: from |V_ub| | 0.1017 |
| E4: from |V_td| | 0.1022 |

**Mean: 0.1012, spread: 0.0018, relative spread: 1.75 %.**

All four PDG-extracted values agree to within 1.75 % — consistent with
combined PDG measurement precision and NLO Wolfenstein uncertainty.

**Uniqueness:** scanning small-integer alternative assignments
`(N_pair' ∈ {1,2,3,4}, N_color' ∈ {1,2,3,4,5})` with `N_quark' = N_pair'·N_color'`,
the framework's `(2, 3, 6)` gives the **minimum** multi-channel extraction
spread vs PDG. NO other small-integer assignment is consistent.

**Primary runner:**
`scripts/frontier_ckm_multi_channel_alpha_s_extraction_consistency.py`

## Statement

On the retained NLO Wolfenstein protected-γ̄ surface, the framework's
retained CKM magnitude identities give closed forms for each
CKM magnitude as a structural-integer-scaled function of α_s:

```text
|V_us|^2  =  alpha_s/N_pair                          =  alpha_s/2,
|V_cb|^2  =  alpha_s^2/N_quark                       =  alpha_s^2/6,
|V_ub|^2  =  alpha_s^3/(N_pair * N_quark^2)          =  alpha_s^3/72,
|V_td|^2  =  alpha_s^3 (N_pair^4(N_quark-1) + alpha_s^2)/(N_pair^7 N_color^2)
          =  alpha_s^3 (80 + alpha_s^2)/1152.
```

Each formula can be **inverted** to extract α_s from the corresponding
measured magnitude:

```text
(E1) alpha_s_from_|V_us|  =  N_pair * |V_us|^2.
(E2) alpha_s_from_|V_cb|  =  sqrt(N_quark) * |V_cb|.
(E3) alpha_s_from_|V_ub|  =  (N_pair * N_quark^2 * |V_ub|^2)^(1/3).
(E4) alpha_s_from_|V_td|  =  numerical inversion of |V_td|^2 closed form.
```

```text
(C1) CONSISTENCY PREDICTION:
       All four PDG-extracted alpha_s values agree to within < 5 % relative
       (NLO Wolfenstein precision plus PDG measurement uncertainty).

(C2) PDG VALIDATION:
       Mean of four extractions:   0.1012,
       Spread (max - min):         0.0018,
       Relative spread:            1.75 %.

       All four channels agree at alpha_s ~ 0.10 to better than 1.8 %.

(C3) UNIQUENESS ARGUMENT:
       Among small-integer alternative assignments
         (N_pair' in {1, 2, 3, 4}, N_color' in {1, 2, 3, 4, 5},
	      N_quark' = N_pair' * N_color'),
	   the framework's (2, 3, 6) gives the MINIMUM extraction spread
	   (1.75 %) vs PDG.

       Alternative assignments give at least 20 % spread -- inconsistent
       with PDG data.

(C4) FALSIFIABILITY:
       LHCb Upgrade II + Belle II precision targets test multi-channel
       consistency to ~ 1 % relative. Any persistent spread materially
       above the current ~1.8 % would force a framework revision
       (NNLO refinement or shift in retained structural integers).
```

## Retained Inputs

| Input | Authority on `main` | Tier |
| --- | --- | --- |
| `(rho_bar, eta_bar)` apex coords | [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) | retained |
| `N_pair = 2`, `N_color = 3`, `N_quark = 6` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) | retained |
| `rho = 1/6`, `eta = sqrt(5)/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | retained |
| `lambda^2 = alpha_s/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) | retained |

The closure uses ONLY retained-tier authorities.

## Derivation

### E1: α_s from |V_us|

From `|V_us|² = α_s/N_pair`:

```text
alpha_s  =  N_pair * |V_us|^2  =  2 |V_us|^2.
```

### E2: α_s from |V_cb|

From `|V_cb|² = α_s²/N_quark`:

```text
alpha_s^2  =  N_quark * |V_cb|^2,
alpha_s    =  sqrt(N_quark) * |V_cb|  =  sqrt(6) * |V_cb|.
```

### E3: α_s from |V_ub|

From `|V_ub|² = α_s³/(N_pair × N_quark²)`:

```text
alpha_s^3  =  N_pair * N_quark^2 * |V_ub|^2,
alpha_s    =  (N_pair * N_quark^2 * |V_ub|^2)^(1/3)  =  (72 * |V_ub|^2)^(1/3).
```

### E4: α_s from |V_td|

From `|V_td|² = α_s³(80 + α_s²)/1152` — a cubic-plus-quintic equation in α_s:

```text
1152 |V_td|^2  =  80 alpha_s^3 + alpha_s^5
```

This is a quintic in α_s, but for the physically relevant root
`α_s ∈ (0, 4)` it is monotonic and uniquely invertible. Numerical root-finding
(e.g., bisection on `[0.01, 0.5]`) gives α_s to arbitrary precision.

### PDG validation

Using PDG central values:

| Channel | PDG magnitude | α_s extracted |
| --- | ---: | ---: |
| E1: |V_us| | 0.2243 | 0.1006 |
| E2: |V_cb| | 0.0410 | 0.1004 |
| E3: |V_ub| | 0.00382 | 0.1017 |
| E4: |V_td| | 0.00861 | 0.1022 |

Mean = 0.1012, spread = 0.0018, relative spread = **1.75 %**.

### Uniqueness scan

Scanning small-integer alternatives over `(N_pair', N_color')` with
`N_quark' = N_pair' × N_color'`:

| N_pair' | N_color' | N_quark' | E1 | E2 | E3 | E4 | spread | comment |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 3 | 3 | 0.0503 | 0.0710 | 0.0508 | 0.0693 | 34.30 % | inconsistent |
| 2 | 2 | 4 | 0.1006 | 0.0820 | 0.0776 | 0.0925 | 26.13 % | inconsistent |
| **2** | **3** | **6** | **0.1006** | **0.1004** | **0.1017** | **0.1022** | **1.75 %** | **CONSISTENT** |
| 2 | 4 | 8 | 0.1006 | 0.1160 | 0.1232 | 0.1107 | 20.01 % | inconsistent |
| 3 | 2 | 6 | 0.1509 | 0.1004 | 0.1164 | 0.1170 | 41.68 % | inconsistent |
| 3 | 3 | 9 | 0.1509 | 0.1230 | 0.1525 | 0.1311 | 21.16 % | inconsistent |

The framework's `(2, 3, 6)` is the **unique small-integer assignment
giving consistency with PDG** in the stated scan. The next-best alternative
has 20.01 % spread, inconsistent with current PDG data under this
four-channel readout.

This is a **strong empirical argument** for the framework's specific
structural integers.

## Numerical Verification

All identities verified via sympy:

| Identity | Form | Verified? |
| --- | --- | --- |
| E1 inversion | `α_s = N_pair × \|V_us\|²` | sympy `simplify(diff) == 0` |
| E2 inversion | `α_s = √N_quark × \|V_cb\|` | sympy `simplify(diff) == 0` |
| E3 inversion | `α_s = (N_pair × N_quark² × \|V_ub\|²)^(1/3)` | sympy `simplify(diff) == 0` |
| E4 closed form | `\|V_td\|² = α_s³(80+α_s²)/1152` | sympy exact |
| PDG consistency | spread < 5 % | numerical 1.75 % ✓ |
| Pairwise consistency | max pairwise < 5 % | numerical 1.75 % max ✓ |
| Uniqueness | (2,3,6) gives min spread vs alternatives | four-channel numerical scan ✓ |

## Science Value

### What this lets the framework state cleanly

Previously, the framework had retained:
- The Wolfenstein parameters as structural-integer combinations of
  `(N_pair, N_color, N_quark)` and α_s.
- Closed forms for each CKM magnitude in the retained CKM atlas.
- The α_s-independent structural ratios already packaged on the retained CKM surface.

This note delivers:

1. **NEW retained four-channel α_s extraction protocol** (E1-E4): each
   PDG-measured CKM magnitude gives an INDEPENDENT estimate of the
   framework's α_s value via the inverted retained CKM magnitude identities.

2. **NEW PDG consistency check**: all four extractions agree at
   **α_s ≈ 0.10 to within 1.75 %** relative spread, validating the
   framework against current experimental data without parameter tuning.

3. **NEW uniqueness argument**: scanning small-integer alternative
   assignments of `(N_pair, N_color, N_quark)` shows that the
   framework's `(2, 3, 6)` gives the unique minimum four-channel spread.
   The next-best assignment gives 20.01 % spread, incompatible with
   current data under this readout.

4. **NEW falsifiability envelope**: future LHCb Upgrade II + Belle II
   precision tests the multi-channel consistency to ~ 1 % relative.

### Why this counts as pushing the science forward

The retained structural integers `(N_pair, N_color, N_quark) = (2, 3, 6)`
have so far been **inputs** to the framework — derived from the underlying
Z³ + 3-color + 3-generation + 2-pair lattice structure. This note
**inverts the logic**: it shows that **PDG CKM central values, fed into the
framework's structural-integer formulas, uniquely select `(2, 3, 6)`
inside the stated small-integer scan**.

Specifically, **the multi-channel α_s extraction consistency requires
`(N_pair, N_color, N_quark) = (2, 3, 6)` within that scan**. Any other
assignment tested fails to give consistent α_s across the four CKM channels.

This is a **non-trivial empirical bootstrap**: if the framework's
structural integers were unknown a priori, current PDG CKM data would
**uniquely select them within the scan** as the small-integer assignment giving
multi-channel consistency.

The result has three high-value empirical qualities:

1. **Sharp, falsifiable predictions**: each of the four α_s extractions
   is a quantitative prediction, testable at current and future
   precision.
2. **Uniqueness**: the framework's structural integers `(2, 3, 6)` are
   uniquely selected by PDG central values among the scanned small-integer alternatives.
3. **Multi-channel consistency**: four independent extractions of the
   SAME quantity (α_s) agree across channels — a STRONG consistency
   check that any non-framework theory would have to reproduce.

### Falsifiable structural claim

The closure (E1-E4, C1-C3) is sharp:

```text
The retained NLO Wolfenstein protected-γ̄ surface
  + retained CKM_MAGNITUDES (N_pair = 2, N_color = 3, N_quark = 6)
forces:

  alpha_s_from_|V_us|, |V_cb|, |V_ub|, |V_td|
  to all agree at alpha_s ~ 0.10 within current PDG precision (~ 1.8 %).

  Among small-integer assignments (N_pair', N_color', N_quark' = N_pair' N_color'),
  ONLY (2, 3, 6) produces the minimum extraction spread across all four
  channels (next-best assignment gives 20.01 % spread).
```

Future precision improvements (LHCb Upgrade II + Belle II) test whether
this same four-channel consistency remains stable as the empirical errors
shrink.

## What This Claims

- `(E1-E4)`: NEW retained four-channel α_s extraction formulas, one
  per CKM magnitude.
- `(C1)`: NEW retained framework consistency prediction — all four
  extractions agree at canonical α_s.
- `(C2)`: NEW PDG validation — extractions agree to 1.75 % relative.
- `(C3)`: NEW uniqueness argument — `(N_pair, N_color, N_quark) = (2, 3, 6)`
  is the unique small-integer assignment consistent with PDG data.
- `(C4)`: NEW falsifiability — future precision tests to ~ 1 % relative.

## What This Does NOT Claim

- Does **not** modify any retained authority.
- Does **not** promote any support-tier theorem to retained.
- Does **not** cite unmerged branches as load-bearing.
- Does **not** introduce a new `d`-selector or `N_color`-selector;
  the uniqueness argument is empirical and scan-bounded (PDG central values prefer `(2, 3, 6)`),
  not a derivation of the structural integers from first principles.
- Does **not** depend on any α_s-running pipeline.
- Does **not** make a precision-prediction claim beyond NLO Wolfenstein.

## Reproduction

```bash
python3 scripts/frontier_ckm_multi_channel_alpha_s_extraction_consistency.py
```

Expected:

```text
TOTAL: PASS=17, FAIL=0
```

The runner:

- Reads each cited authority file from disk.
- Extracts the verbatim `Status:` line and prints it as ground-truth proof.
- Verifies tier label (retained vs support).
- Independently extracts retained inputs (`N_pair`, `N_color`, `N_quark`).
- Computes each of the four α_s extraction formulas symbolically
  (E1-E4, with E4 monotonicity and bisection) and asserts that each
  formula correctly inverts the corresponding retained CKM magnitude
  identity.
- Computes the four PDG-extracted α_s values and verifies pairwise
  consistency within 5 % relative.
- Scans small-integer alternative assignments
  `(N_pair' ∈ {1,2,3,4}, N_color' ∈ {1,2,3,4,5})` and verifies that
  the framework's `(2, 3, 6)` gives the MINIMUM extraction spread.

## Cross-References

**Retained-tier authorities used (each Status verified by extraction):**

- [`CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md`](CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md)
  — `(rho_bar, eta_bar)` apex coordinates.
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md)
  — `N_pair = 2`, `N_color = 3`, `N_quark = 6`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — `rho = 1/6`, `eta = sqrt(5)/6`.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  — `λ² = α_s/2`, `A² = 2/3`.

**NOT cited as derivation input:**

- Any support-tier note.
- Any unmerged branch.
- Any candidates-tier theorem.
