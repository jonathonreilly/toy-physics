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

## Block 08 — Unruh T_U = a/(2π) from KMS + Lorentz kernel

### Branch-local self-review (2026-05-01)

- **theorem note:** [docs/AXIOM_FIRST_UNRUH_TEMPERATURE_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_UNRUH_TEMPERATURE_THEOREM_NOTE_2026-05-01.md)
- **runner:** [scripts/axiom_first_unruh_temperature_check.py](../../../../scripts/axiom_first_unruh_temperature_check.py)

#### Findings

- **F1 (no-issue):** all 5 tests pass at machine precision.
- **F2 (no-issue):** SI Earth-gravity Unruh temperature ~4×10⁻²⁰ K
  matches textbook value.
- **F3 (no-issue):** Bisognano-Wichmann modular identity Δ = exp(-2π K)
  numerically verified.

#### Disposition

- **disposition:** pass.
- **proposal-allowed:** false.
- **branch action:** commit, push, open stacked PR (base = Block 01 KMS).

#### Runner results summary (2026-05-01)

```text
Test 1 (Wick-rotation period 2 pi):                PASS
Test 2 (T_Unruh = a / (2 pi) sweep):               PASS
Test 3 (SI scale at Earth gravity ~4e-20 K):       PASS
Test 4 (T_Unruh / a = 1/(2 pi) universal):         PASS
Test 5 (Bisognano-Wichmann Delta = exp(-2 pi K)):  PASS

OVERALL: PASS
```
