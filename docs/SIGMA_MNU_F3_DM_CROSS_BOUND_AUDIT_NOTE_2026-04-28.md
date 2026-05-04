# Lane 4F (Σm_ν) — F3 DM Cross-Bound Audit

**Date:** 2026-04-28
**Status:** support / branch-local **cross-bound audit** note on
`physics-loop/sigma-mnu-f3-dm-cluster-20260428`. Cycle 1 of the
F3 loop. Audit-grade. Identifies the strength and structural
limits of the DM cross-bound chain for numerical Σm_ν retention.
**Lane:** 4 — Neutrino quantitative closure (sub-target 4F-β)
**Loop:** `sigma-mnu-f3-dm-cluster-20260428`
**Runner:** `scripts/frontier_sigma_mnu_f3_dm_cross_bound_audit.py`
**Log:** `outputs/frontier_sigma_mnu_f3_dm_cross_bound_audit_2026-04-28.txt`

---

## 0. Context

The prior session's PR #167 landed the support-level structural
identity (`NEUTRINO_LANE4_4F_SIGMA_M_NU_FUNCTIONAL_FORM_THEOREM_NOTE_2026-04-28.md`)

```text
(T-4F-α-2)   Σm_ν = (1 - L - R - Ω_b - Ω_DM) × C_ν × h²
```

on the retained cosmology bounded surface. Phase-2 of that loop's
fan-out enumerated six attack frames F1–F6 toward numerical Σm_ν
retention. F1 (Lane 5 (C1) absolute-scale gate) was closed by the
parallel `hubble-c1-absolute-scale-gate-20260428` loop's Cycles
1–6 (PR #168 + PR #169): exhaustive A1-A6 + orthogonal fan-out
returns "Cl_4(C) carrier-axiom extension required or accept (C1)
open".

This note executes F3 (DM relic abundance cross-bound) audit:
combine (T-4F-α-2) with the current-bank Ω_DM interval from
`DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_BOUNDING_THEOREM_NOTE_2026-04-17.md`
and verify the resulting Σm_ν cross-bound interval over an honest
admission range for the open layer (L, Ω_b, h).

## 1. Inputs

| Input | Tier | Value or interval | Source |
|---|---|---|---|
| `Σm_ν` functional form (T-4F-α-2) | support | algebraic identity | `NEUTRINO_LANE4_4F_SIGMA_M_NU_FUNCTIONAL_FORM_THEOREM_NOTE_2026-04-28.md` |
| `Ω_DM` interval | current-bank / unaudited | `[0.267709, 0.269718]` | `DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_BOUNDING_THEOREM_NOTE_2026-04-17.md` |
| `R = Ω_r,0` | admitted | `~9.182 × 10⁻⁵` | T_CMB + retained N_eff |
| `C_ν` | admitted convention | `93.14 eV` | T_CMB + retained N_eff bookkeeping |
| `L = Ω_Λ,0` | admitted | observational (Planck-like ~0.6847) | open-number reduction |
| `Ω_b` | admitted | observational (eta_obs, ~0.0493) | open-number reduction |
| `h = H_0/100` | open | research-level distant | Lane 5 two-gate dep (open) |
| Σm_ν oscillation lower bound | comparator only | `≥ 0.06 eV` | PDG; **NOT** a derivation input |

The framework's current-bank `Ω_DM` interval is **conditional on the
same-surface admitted DM family** `α(σ) = α_lo + σ(α_hi - α_lo)`
with σ in a narrow root interval. The current-bank itself is not
yet a selector law (per the DM thermal bounding theorem's "Honest
Status" §). The F3 cross-bound therefore inherits this conditional.

## 2. Theorem (audit)

> **Theorem (F3 cross-bound audit).** The current-bank `Ω_DM` interval
> from the DM thermal-bounding theorem, combined with (T-4F-α-2),
> supplies a closed-form Σm_ν cross-bound interval conditional on
> the admission triple `(L, Ω_b, h)`. At standard Planck-style
> admissions `(L, Ω_b, h) = (0.6847, 0.0493, 0.6736)` the cross-
> bound predicts `Σm_ν ∈ [-0.161, -0.076] eV`, **negative at both
> endpoints**. This represents a structural tension between the
> framework's current-bank `Ω_DM` interval and the standard observational
> matter-budget split, since the framework's `Ω_DM ∈ [0.2677,
> 0.2697]` exceeds the observationally-derived `Ω_DM ≈ 0.265` by
> roughly `0.003-0.005`. The cross-bound becomes physically
> consistent (`Σm_ν > 0`) on a sub-region of the `(L, Ω_b, h)`
> admission space; for the explicit grid `L ∈ [0.67, 0.70]`,
> `Ω_b ∈ [0.045, 0.055]`, `h ∈ [0.65, 0.75]`, `42.9%` of admission
> points yield `Σm_ν > 0` and `38.5%` yield `Σm_ν > 0.06 eV`
> (compatible with the oscillation lower bound).

### Proof.

The (T-4F-α-2) identity is algebraic on the matter-budget split

```text
Ω_m,0 = Ω_b + Ω_DM + Ω_ν,0 = 1 - L - R
```

(per `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`)
plus the CMB-neutrino-relic conversion `Ω_ν,0 h² = Σm_ν / C_ν`.
Substituting gives `Σm_ν = (1 - L - R - Ω_b - Ω_DM) C_ν h²`.

Plugging in the framework's current-bank Ω_DM interval at the Planck
admission `(L, Ω_b, h) = (0.6847, 0.0493, 0.6736)`:

```text
Ω_DM = 0.2677:  Σm_ν = (1 - 0.6847 - 9.18e-5 - 0.0493 - 0.2677) × 93.14 × 0.6736²
                     = -0.0017 × 93.14 × 0.4537 = -0.0761 eV (negative)

Ω_DM = 0.2697:  Σm_ν = (1 - 0.6847 - 9.18e-5 - 0.0493 - 0.2697) × 93.14 × 0.6736²
                     = -0.0037 × 93.14 × 0.4537 = -0.1610 eV (more negative)
```

Both endpoints negative. The runner verifies the interval
`Σm_ν ∈ [-0.161, -0.076] eV` at this admission point.

The structural tension arises because

```text
Σm_ν = Ω_ν,0 × C_ν × h²  >=  0   (physical)
   ⇔  Ω_ν,0 = Ω_m,0 - Ω_b - Ω_DM  >=  0
   ⇔  Ω_DM <= Ω_m,0 - Ω_b ≈ 0.315 - 0.0493 = 0.266
```

The framework's `Ω_DM` low endpoint `0.2677` already exceeds
`0.266`; high endpoint exceeds it by more. Hence at Planck-style
`(L, Ω_b)` the framework's `Ω_DM` bound has no room for `Ω_ν,0 ≥
0`.

The runner's grid scan over `(L, Ω_b, h) ∈ [0.67, 0.70] × [0.045,
0.055] × [0.65, 0.75]` (`462` grid points) shows that:

- `n_positive = 198` points (42.9%) yield `Σm_ν > 0`;
- `n_above_osc = 178` points (38.5%) yield `Σm_ν > 0.06 eV`;
- range `Σm_ν ∈ [-1.19, 0.90] eV` across the full grid;
- favorable admission region: `L ∈ [0.67, 0.685]`, `Ω_b ∈ [0.045,
  0.055]`, `h ∈ [0.65, 0.75]`.

The favorable region requires `L < 0.685` and/or `Ω_b > 0.0493`,
i.e., admissions slightly off the Planck central values. The
sensitivity check "loosen Ω_DM lower endpoint to 0.265" (a `~0.003`
shift) gives `Σm_ν ≈ 0.038 eV` at Planck admission, recovering
positivity but still below the `0.06 eV` oscillation lower bound.

Therefore F3 cannot supply numerical Σm_ν retention without either
(i) tightening the framework's `Ω_DM` interval by `~0.003-0.005` to
admit Planck CMB-derived `Ω_DM`, or (ii) loosening the framework's
same-surface DM family to a wider admission interval. Both are
research-level pivots beyond a single audit cycle. ∎

## 3. Numerical verification

The runner
`scripts/frontier_sigma_mnu_f3_dm_cross_bound_audit.py` verifies
all the steps:

1. (T-4F-α-2) algebraic identity on cosmology bounded surface;
2. matter-budget split closure: `1 = L + R + Ω_b + Ω_DM + Ω_ν,0`;
3. `Σm_ν` interval at Planck admission: `[-0.161, -0.076] eV`;
4. structural tension at Planck admission: both endpoints negative;
5. admission-grid scan (`7 × 6 × 11 = 462` points) returns
   `n_positive = 198` (42.9%), `n_above_osc = 178` (38.5%),
   `Σm_ν ∈ [-1.19, 0.90] eV`;
6. sensitivity: loosening `Ω_DM` low endpoint to `0.265` recovers
   `Σm_ν ≈ 0.038 eV` at Planck admission;
7. cross-bound chain is honest only as conditional bounded
   statement.

Output: `SUMMARY: PASS=14  FAIL=0`.

The runner uses no observed `Σm_ν`, no fitted DM coupling, no
framework-side carrier axiom. It uses only the support-level
(T-4F-α-2), the current-bank `Ω_DM` interval, the admitted convention
`C_ν = 93.14 eV`, and the admitted observational ranges `(L, Ω_b,
h)` treated as derivation inputs to be audited (NOT as proof
inputs).

## 4. What this audit closes

- F3 cross-bound chain is **structurally identified**: (T-4F-α-2)
  + current-bank Ω_DM interval + admitted convention `C_ν` supplies a
  closed-form `Σm_ν` interval conditional on `(L, Ω_b, h)`.
- Structural tension at Planck admission is **identified**: the
  framework's current-bank `Ω_DM` interval exceeds Planck CMB-derived
  `Ω_DM` by `~0.003-0.005`.
- Favorable admission sub-region is **mapped**: `42.9%` of the
  grid yields `Σm_ν > 0`, with admissions slightly off Planck
  central values.

## 5. What this audit does not close

- Numerical `Σm_ν` retention. The cross-bound is conditional and
  in observational tension at standard Planck admissions.
- The framework's current-bank `Ω_DM` interval itself. The interval is
  conditional on the same-surface admitted DM family, which is
  itself an open scientific question (per the DM thermal-bounding
  theorem's "Honest Status" §).
- The Lane 5 two-gate dependency that opens up `h` retention. Per
  the parallel `hubble-c1-absolute-scale-gate-20260428` loop's
  Cycles 1-6 (PR #168 + #169), Lane 5 (C1) gate requires either
  Cl_4(C) carrier-axiom extension or acceptance as open.

## 6. Implication for follow-on cycles

Cycle 2 options:

- **Option A:** investigate whether the framework can tighten the
  current-bank `Ω_DM` interval by `~0.003-0.005` via a sharpened DM
  same-surface family (would restore F3 cross-bound usability at
  Planck admissions);
- **Option B:** investigate whether a different admitted Ω_b
  (slightly higher than `0.0493`) gives a sub-region where Σm_ν
  > 0.06 eV (cross-bound usable on a non-Planck-central admission
  surface);
- **Option C:** stuck fan-out across other Σm_ν cross-bound
  routes (oscillation lower bound + ν-mass-squared splittings,
  N_eff + Δm² combination, etc.) per Deep Work Rules;
- **Option D:** honest stop with audit-grade structural tension
  finding and pivot to a different lane (e.g., Lane 6 M1/M5-c
  Koide-conditional).

Per Deep Work Rules and limited single-audit-cycle scope, this
note recommends **Option C** for Cycle 2 (stuck fan-out).

## 7. Cross-references

- 4F support-level functional form theorem:
  `NEUTRINO_LANE4_4F_SIGMA_M_NU_FUNCTIONAL_FORM_THEOREM_NOTE_2026-04-28.md`.
- DM thermal-bounding theorem:
  `DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_BOUNDING_THEOREM_NOTE_2026-04-17.md`.
- DM flagship lane status:
  `DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17.md`.
- Cosmology open-number reduction:
  `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`.
- Lane 5 (C1) gate audit + cycles 1-6 closure:
  `HUBBLE_LANE5_C1_GATE_RESIDUAL_PREMISE_ATTACK_AUDIT_NOTE_2026-04-28.md`,
  `HUBBLE_LANE5_C1_A1_GRASSMANN_NO_GO_NOTE_2026-04-28.md`,
  ... (PR #169 series).
- Loop pack:
  `.claude/science/physics-loops/sigma-mnu-f3-dm-cluster-20260428/`.

## 8. Boundary

This is an **audit** note, not a stretch attempt or no-go closure.
It does not retain `Σm_ν`, does not retire any open import, and
does not extend the framework. It identifies a **structural
tension** between the framework's current-bank `Ω_DM` interval and the
observational matter-budget split at standard Planck admissions,
and maps the favorable admission sub-region where the F3
cross-bound is consistent with positive `Σm_ν`.

The audit observes that the framework's current-bank `Ω_DM` interval,
while honest as a structural prediction, is in mild tension with
observation; tightening or loosening either bound requires
research-level work beyond a single audit cycle.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [dm_full_closure_same_surface_thermal_bounding_theorem_note_2026-04-17](DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_BOUNDING_THEOREM_NOTE_2026-04-17.md)
- [cosmology_open_number_reduction_theorem_note_2026-04-26](COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md)
- [hubble_lane5_c1_gate_residual_premise_attack_audit_note_2026-04-28](HUBBLE_LANE5_C1_GATE_RESIDUAL_PREMISE_ATTACK_AUDIT_NOTE_2026-04-28.md)
