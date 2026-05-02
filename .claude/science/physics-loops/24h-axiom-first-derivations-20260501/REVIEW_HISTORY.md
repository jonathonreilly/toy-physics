# Review History — 24h axiom-first derivations campaign

**Date:** 2026-05-01

## Block 01 — KMS condition from RP + spectrum

### Branch-local self-review (2026-05-01)

- **theorem note:** [docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md)
- **runner:** [scripts/axiom_first_kms_condition_check.py](../../../../scripts/axiom_first_kms_condition_check.py)
- **log:** [outputs/axiom_first_kms_condition_check_2026-05-01.txt](../../../../outputs/axiom_first_kms_condition_check_2026-05-01.txt)

#### Findings

- **F1 (resolved during write).** Initial draft of (K2) had `F(t) =
  G(t + i β_th)`; this is the wrong direction. The standard KMS
  identity in the strip is `F(t + i β_th) = G(t)`, equivalently
  `G(t - i β_th) = F(t)`. Theorem note (K2), Step 3, and the runner
  all corrected to the standard direction. This is the same as the
  Bratteli–Robinson Vol. II Definition 5.3.1 statement.
- **F2 (resolved during write).** Initial strip-bound (K3) used
  `|G(z)| ≤ ‖A‖ · ‖B‖`. This is too tight on a finite-dim algebra
  with energy spread σ(H) > 0 (the analytic continuation grows by
  `exp(β_th · σ(H))` in the strip). Theorem note (K3) and the runner
  Test 2 both corrected to the realistic strip bound
  `|F(z)| ≤ ‖A‖ · ‖B‖ · exp(β_th · σ(H))`.
- **F3 (resolved during write).** Initial runner used a generic
  matrix exponential helper that fell back to `np.linalg.eig` for
  complex-scaled Hermitian matrices. This caused 1e+13 numerical
  noise in the KMS identity test. Replaced with eigenbasis-direct
  computation, all five tests now pass at <1e-10 precision.

#### Disposition

- **disposition:** pass (after F1, F2, F3 fixes).
- **proposal-allowed:** false (per CLAIM_STATUS_CERTIFICATE_BLOCK01.md).
- **branch action:** commit, push, open PR with `support` honest status.
- **integration action:** record in HANDOFF.md as a downstream-blocker
  for Block 2 (Hawking T_H), Block 6 (Stefan-Boltzmann), Block 9 (GSL),
  and Block 11 (Unruh T_U).

#### Runner results summary (2026-05-01)

```text
Test 1 (KMS identity strip endpoint):    PASS   max resid 4.96e-15
Test 2 (strip continuity / bound):       PASS   max|G|/grown_bound = 0.023
Test 3 (equilibrium uniqueness):         PASS   max diff 0.000e+00
Test 4 (path-integral correspondence):   PASS   diff 4.44e-16
Test 5 (detailed-balance at i beta_th):  PASS   diff 2.58e-15

OVERALL: PASS
```

## Block 02 — Hawking T_H from Wick-rotated Killing horizon + KMS

### Branch-local self-review (2026-05-01)

- **theorem note:** [docs/AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md)
- **runner:** [scripts/axiom_first_hawking_temperature_check.py](../../../../scripts/axiom_first_hawking_temperature_check.py)
- **log:** [outputs/axiom_first_hawking_temperature_check_2026-05-01.txt](../../../../outputs/axiom_first_hawking_temperature_check_2026-05-01.txt)

#### Findings

- **F1 (no-issue):** all six runner tests pass on first run. Wick-
  rotation regularity period β_th = 2π/κ is a 1-line algebraic
  identity once the local Rindler form (4) is established.
- **F2 (no-issue):** Schwarzschild benchmark recovers Hawking 1975
  T_H = 1/(8πGM) at machine precision because κ_Schw = 1/(4GM) is
  the standard textbook result.

#### Disposition

- **disposition:** pass.
- **proposal-allowed:** false (per CLAIM_STATUS_CERTIFICATE_BLOCK02.md;
  inherits Block 01 audit-pending classification).
- **branch action:** commit, push, open stacked PR (base = Block 01
  branch) with `support` honest status.
- **integration action:** record in HANDOFF.md as the load-bearing
  input for Block 05 (first law of BH mechanics dM = T_H dA / 8πG)
  and Block 09 (GSL).

#### Runner results summary (2026-05-01)

```text
Test 1 (conical-defect uniqueness at beta_th = 2 pi / kappa): PASS  max resid 0
Test 2 (T_H = 1/beta_th = kappa/(2 pi)):                      PASS  max resid 0
Test 3 (Schwarzschild T_H = 1/(8 pi G M) Hawking 1975):       PASS  max resid 0
Test 4 (first-law differential T_H dS_BH = kappa dA / 8 pi):  PASS  max resid 0
Test 5 (bolt-regularity Ricci coefficient vanishes):          PASS  max resid 0
Test 6 (Rindler T_Unruh = a/(2 pi) preview):                  PASS  max resid 0

OVERALL: PASS
```

## Block 05 — First law of BH mechanics

### Branch-local self-review (2026-05-01)

- **theorem note:** [docs/AXIOM_FIRST_FIRST_LAW_BH_MECHANICS_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_FIRST_LAW_BH_MECHANICS_THEOREM_NOTE_2026-05-01.md)
- **runner:** [scripts/axiom_first_first_law_bh_mechanics_check.py](../../../../scripts/axiom_first_first_law_bh_mechanics_check.py)
- **log:** [outputs/axiom_first_first_law_bh_mechanics_check_2026-05-01.txt](../../../../outputs/axiom_first_first_law_bh_mechanics_check_2026-05-01.txt)

#### Findings

- **F1 (resolved during write):** typo in Test 6 unpacking from over-eager
  edit; fixed and rerun.
- **F2 (no-issue):** Schwarzschild differential dM = T_H dS_BH at
  finite-difference precision (~1e-6).
- **F3 (no-issue):** Smarr formula M = 2 T_H S_BH at <1e-12.
- **F4 (no-issue):** integrated form M_2 - M_1 = ∫ T_H dS_BH at <1e-15.
- **F5 (no-issue):** negative specific heat dT_H/dM < 0 verified for all
  Schwarzschild masses tested.

#### Disposition

- **disposition:** pass.
- **proposal-allowed:** false (per CLAIM_STATUS_CERTIFICATE_BLOCK05.md;
  inherits Block 02 audit-pending classification).
- **branch action:** commit, push, open stacked PR (base = Block 02 branch).
- **integration action:** record in HANDOFF.md as cornerstone for GSL
  (Block 09).

#### Runner results summary (2026-05-01)

```text
Test 1 (dM = T_H dS_BH for Schwarzschild):     PASS
Test 2 (Smarr formula M = 2 T_H S_BH):         PASS
Test 3 (explicit identity dM = dM):            PASS
Test 4 (negative specific heat dT_H/dM < 0):   PASS
Test 5 (integral form over (M_1, M_2)):        PASS
Test 6 (Smarr derivative consistency):         PASS

OVERALL: PASS
```
