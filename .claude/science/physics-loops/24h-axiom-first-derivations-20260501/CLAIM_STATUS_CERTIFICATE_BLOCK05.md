# Claim Status Certificate — Block 05 (First law of BH mechanics)

**Date:** 2026-05-01
**Block:** 05 — first law of BH mechanics dM = T_H dS_BH
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block05-firstlaw-20260501`
**Stacked PR base:** `physics-loop/24h-axiom-first-block02-hawking-20260501`
**Note:** [docs/AXIOM_FIRST_FIRST_LAW_BH_MECHANICS_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_FIRST_LAW_BH_MECHANICS_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_first_law_bh_mechanics_check.py](../../../../scripts/axiom_first_first_law_bh_mechanics_check.py)
**Log:** [outputs/axiom_first_first_law_bh_mechanics_check_2026-05-01.txt](../../../../outputs/axiom_first_first_law_bh_mechanics_check_2026-05-01.txt)

## Status fields

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on retained framework GR + retained BH 1/4 carrier + Block 02 Hawking T_H support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Inherits the Block 02 Hawking T_H upstream support classification, which itself depends on Block 01 KMS support which depends on retained-but-audit-pending RP and spectrum-condition support notes. Per physics-loop SKILL retained-proposal certificate item 4, a chain of support cannot promote to proposed_retained until the entire upstream chain is ratified retained on the current authority surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Dependency classes

| Dep | Class | Source |
|---|---|---|
| Framework GR action surface | retained | UNIVERSAL_GR_* family |
| BH 1/4 carrier composition | bounded support, audit-pending | BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29 |
| Block 02 Hawking T_H | support, audit-pending | AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01 (this PR's base) |
| Wald-Noether identity | admitted-context | (already admitted by upstream BH 1/4) |
| Bardeen-Carter-Hawking 1973 integrability | admitted-context | standard GR theorem |
| ADM mass identification | admitted-context | standard stationary GR |

## Open imports

No new imports. The Wald-Noether and BCH integrability inputs are
already paid for by the upstream chain.

## Review-loop disposition

- branch-local self-review: `pass` (theorem note matches runner;
  Schwarzschild differential dM = T_H dS_BH verified at finite-diff
  precision (~1e-6); Smarr formula M = 2 T_H S_BH at <1e-12;
  integrated form over (M_1, M_2) at <1e-15).
- formal `/review-loop`: deferred to integration-time.
- F1 (resolved during write): bug in Test 6 unpacking from over-eager
  edit; fixed and rerun.

## Status conclusion

This block is a **derived support theorem** on the framework's retained
GR + retained BH 1/4 + Block 02 Hawking T_H. It completes the
gravitational thermodynamics quartet `(M, T_H, S_BH, A)` and confirms
the framework's BH solutions satisfy the four laws of thermodynamics.

It is **not** suitable for `proposed_retained` / `proposed_promoted`
status until the upstream chain is fully ratified retained.

## Audit hand-off requirement

If a later integration / review process wants to promote this note to
`proposed_retained`, it needs:

1. Full upstream chain (RP + spectrum cond + Block 01 KMS + Block 02
   Hawking T_H + BH 1/4 carrier) ratified retained.
2. Independent audit of Steps 1–4 of the proof.
3. Independent verification of the 6-test runner pass.
4. Optional Kerr-Newman extension explicitly verified
   (currently recorded as corollaries only).

Until then this note remains `support` per the controlled vocabulary.
