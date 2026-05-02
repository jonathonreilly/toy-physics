# Claim Status Certificate — Block 08 (Unruh temperature)

**Date:** 2026-05-01
**Block:** 08 — Unruh T_U = a/(2π)
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block08-unruh-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block01-kms-20260501`
**Note:** [docs/AXIOM_FIRST_UNRUH_TEMPERATURE_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_UNRUH_TEMPERATURE_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_unruh_temperature_check.py](../../../../scripts/axiom_first_unruh_temperature_check.py)
**Log:** [outputs/axiom_first_unruh_temperature_check_2026-05-01.txt](../../../../outputs/axiom_first_unruh_temperature_check_2026-05-01.txt)

## Status fields

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on retained Lorentz kernel + Block 01 KMS support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Inherits Block 01 KMS upstream support classification (audit-pending)."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Dependency classes

| Dep | Class | Source |
|---|---|---|
| Block 01 KMS support | support, audit-pending | this PR's base |
| Retained Lorentz kernel | retained | LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE |
| Retained emergent Lorentz | retained | EMERGENT_LORENTZ_INVARIANCE_NOTE |
| Standard Rindler coords / Bisognano-Wichmann | admitted-context | standard SR/AQFT |

## Review-loop disposition

- branch-local self-review: `pass` (parallel structure to Block 02
  Hawking; T_U = a/(2π) verified at machine precision; SI Earth-gravity
  scale ~4 × 10⁻²⁰ K recovered).
- formal `/review-loop`: deferred.

## Status conclusion

This block is a **derived support theorem** that completes the
horizon-thermodynamics triple
`(T_Hawking, T_Unruh, T_dS)` (de Sitter horizon temperature
follows by the same argument).

It is **not** suitable for `proposed_retained` until Block 01 KMS
is ratified retained.
