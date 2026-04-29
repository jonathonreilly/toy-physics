# Goal: Lane 4F (Σm_ν) — F3 DM-Cluster Cross-Bound Audit

**Slug:** `sigma-mnu-f3-dm-cluster-20260428`
**Branch:** `physics-loop/sigma-mnu-f3-dm-cluster-20260428`
**Lane:** 4 (Neutrino) — sub-target 4F-β (numerical Σm_ν retention)

## Primary target

Audit the F3 attack frame from the prior session's 4F Phase-2 fan-out:
**DM relic abundance cross-bound** for Σm_ν via the retained
algebraic identity

```text
Σm_ν = (1 - L - R - Ω_b - Ω_DM) × C_ν × h²
```

(per `NEUTRINO_LANE4_4F_SIGMA_M_NU_FUNCTIONAL_FORM_THEOREM_NOTE_2026-04-28.md`).

The retained DM thermal-bounding theorem
(`DM_FULL_CLOSURE_SAME_SURFACE_THERMAL_BOUNDING_THEOREM_NOTE_2026-04-17.md`)
supplies Ω_DM intervals conditional on retained same-surface
admitted-family content. Does this bounded Ω_DM cross-bound, applied
to (T-4F-α-2), supply a bounded Σm_ν interval?

## Why this loop

Per the prior session's Phase-2 fan-out (PR #167), F3 was rated
**MEDIUM-HIGH** for single-cycle attemptability. F1 (Lane 5 (C1)
absolute-scale gate) was rated HIGH and is now in the
`hubble-c1-absolute-scale-gate-20260428` loop (cycles 1-6 closed).
F3 is the strongest remaining single-cycle continuation for
numerical Σm_ν retention.

## Phase-1 (this loop)

Single audit cycle: identify the strength of the Ω_DM cross-bound,
its conditional dependencies, and the resulting Σm_ν bound interval.
Output: AUDIT-grade structural identification of the cross-bound
chain, the retained content it depends on, and the structural gap
before Σm_ν becomes bounded.

## Stop conditions

- Runtime budget reached.
- Single-cycle audit produces the cross-bound inventory.
- Pivot if a single-cycle stretch becomes clear from the audit.
