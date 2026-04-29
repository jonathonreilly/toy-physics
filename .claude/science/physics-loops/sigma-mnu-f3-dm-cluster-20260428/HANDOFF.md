# Lane 4F (Σm_ν) F3 DM-Cluster Cross-Bound Loop — HANDOFF

**Updated:** 2026-04-29T04:32Z
**Current branch:** `physics-loop/sigma-mnu-f3-dm-cluster-20260428`
**Loop status:** running
**Claim status:** open (Σm_ν not retained)
**Hard residual:** numerical Σm_ν retention; framework Ω_DM bound in
mild tension with observation at standard Planck admissions

## Cycles completed

| # | Type | Outcome |
|---|---|---|
| 1 | Audit | F3 DM cross-bound — structural tension identified |
| 2 | Fan-out | 5 orthogonal routes — structural tension confirmed |

## Cycle 1 result (2026-04-29)

**Artifact:** `docs/SIGMA_MNU_F3_DM_CROSS_BOUND_AUDIT_NOTE_2026-04-28.md`
**Runner:** `scripts/frontier_sigma_mnu_f3_dm_cross_bound_audit.py`
**Log:** `outputs/frontier_sigma_mnu_f3_dm_cross_bound_audit_2026-04-28.txt`
**Verification:** `PASS=14 FAIL=0`

### What this audit closes

- F3 cross-bound chain is **structurally identified**: (T-4F-α-2)
  + retained Ω_DM bound + admitted convention C_ν supplies a
  closed-form Σm_ν interval conditional on (L, Ω_b, h).
- Structural tension at Planck admission **identified**: framework's
  retained Ω_DM bound `[0.2677, 0.2697]` exceeds Planck CMB-derived
  Ω_DM `~0.265` by `~0.003-0.005`. At Planck admission `(L=0.6847,
  Ω_b=0.0493, h=0.6736)` the cross-bound predicts Σm_ν `∈ [-0.161,
  -0.076]` eV (negative).
- Favorable admission sub-region **mapped**: 42.9% of `(L, Ω_b, h)`
  grid yields Σm_ν > 0, 38.5% yields Σm_ν > 0.06 eV (compatible
  with osc lower bound).

### What this audit does not close

- Numerical Σm_ν retention. Cross-bound is conditional and in
  observational tension at standard Planck admissions.
- Framework's retained Ω_DM bound itself (still conditional on
  same-surface admitted DM family).
- Lane 5 two-gate dep that opens up h retention.

## Cycle plan

- **Cycle 2 (recommended):** stuck fan-out across other Σm_ν
  cross-bound routes (oscillation lower bound + Δm² splittings,
  N_eff + Δm² combination, retained 4F-α structural identity at
  alternative admission surfaces).
- **Cycle 3:** synthesis; honest stop or pivot.

## Stop conditions

- Audit and fan-out land; no more single-cycle attemptable routes
  on the retained surface.
- Runtime budget reached.
- Pivot to different lane (Lane 6 M1/M5-c Koide-conditional, or
  back to C1 review-loop pressure).

## Next exact action

Cycle 2 = stuck fan-out across alternative Σm_ν cross-bound
routes:

- **(F3-α)** oscillation Σm_ν lower bound (PDG ν-mass-squared
  splittings) — cross-bound from below;
- **(F3-β)** N_eff cross-bound (retained N_eff = 3.046 vs.
  observational fits);
- **(F3-γ)** retained `Ω_m,0 h²` admitted CMB peak-height pin —
  alternative admission surface;
- **(F3-δ)** Lane 4D Dirac global lift (conditional retained per
  prior session): does Dirac vs Majorana pick out a Σm_ν floor?
- **(F3-ε)** baryogenesis/eta admitted-input promotion (F2 from
  prior fan-out).

Synthesize agreements/contradictions and identify best remaining
attack frame on the sigma-mnu numerical retention question.
