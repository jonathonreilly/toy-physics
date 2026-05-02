# Claim Status Certificate — Block 04 (Microcausality / Lieb-Robinson)

**Date:** 2026-05-01
**Block:** 04 — Microcausality / Lieb-Robinson bound from A_min + RP +
spectrum condition
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block04-microcausality-20260501`
**Base:** origin/main (independent of Blocks 01-03)
**Note:** [docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_microcausality_check.py](../../../../scripts/axiom_first_microcausality_check.py)
**Log:** [outputs/axiom_first_microcausality_check_2026-05-01.txt](../../../../outputs/axiom_first_microcausality_check_2026-05-01.txt)

## Status fields

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on A_min + retained RP + retained spectrum condition + retained cluster decomposition
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Depends on retained-but-audit-pending RP, spectrum-condition, and cluster-decomposition support notes. Per physics-loop SKILL retained-proposal certificate item 4, a chain of support cannot promote to proposed_retained until all dependencies are ratified retained on the current authority surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Dependency classes

| Dep | Class | Source |
|---|---|---|
| A1 (Cl(3) tensor structure) | A_min axiom | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| A2 (Z^3 graph metric) | A_min axiom | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| A3 (NN staggered Dirac, range r_h = 1) | A_min axiom | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| A4 (plaquette gauge, range r_g = 1) | A_min axiom | `docs/MINIMAL_AXIOMS_2026-04-11.md` |
| RP transfer matrix | retained support, audit-pending | `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` |
| Spectrum condition | retained support, audit-pending | `docs/AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md` |
| Cluster decomposition | retained support, audit-pending | `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md` |
| Lieb-Robinson 1972 estimate | admitted-context | standard lattice statistics theorem |
| Emergent Lorentz invariance for M3 | retained | `docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md`, `docs/LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md` |

## Open imports

The Lieb-Robinson 1972 estimate is admitted-context (theorem-grade
lattice-statistics reference). No new imports beyond the explicit
ledger.

## Review-loop disposition

- branch-local self-review: `pass` (theorem proof matches runner;
  small-t scaling t^d agrees to 3-4 significant figures across d=2,3,4;
  Lieb-Robinson bound holds at all (d, t) tested).
- formal `/review-loop`: deferred to integration-time.

## Status conclusion

This block is a **derived support theorem** on `A_min` plus retained
RP + spectrum condition + cluster decomposition. It is the framework's
**locality theorem** that complements the existing retained
cluster-decomposition theorem (which is the *spatial* decay theorem,
not the *spacetime* lightcone theorem).

It is **not** suitable for `proposed_retained` / `proposed_promoted`
status until all upstream support notes (RP, spectrum cond, cluster
decomp) are ratified retained.

## Audit hand-off requirement

If a later integration / review process wants to promote this note to
`proposed_retained`, it needs:

1. Upstream RP, spectrum cond, and cluster decomp support notes
   ratified retained.
2. Independent audit of the proof's Steps 1–3.
3. Independent verification of the 4-test runner pass.

Until then this note remains `support` per the controlled vocabulary.
