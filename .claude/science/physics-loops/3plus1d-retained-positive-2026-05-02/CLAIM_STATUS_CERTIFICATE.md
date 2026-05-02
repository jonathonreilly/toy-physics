# Claim Status Certificate — 3+1d Retained-Positive

**Date:** 2026-05-02
**Loop slug:** `3plus1d-retained-positive-2026-05-02`
**Branch:** `claude/3plus1d-retained-positive-2026-05-02`
**Block:** anomaly_forces_time_theorem narrowing

## Actual current-surface status

```yaml
actual_current_surface_status: bounded-support
target_claim_type: bounded_theorem
conditional_surface_status: |
  After re-audit, the rewritten theorem is expected to land as
  bounded_theorem with narrowed scope: the only residual external
  bridge premise is the standard ABJ inconsistency implication for
  chiral gauge theories in 3+1d. Three of the prior four admissions
  (singlet completion uniqueness, Clifford-volume chirality, ultra-
  hyperbolic Cauchy obstruction) have been discharged on retained-
  clean Cl(3)/Z^3 primitives in this revision. The audit verdict is
  not predicted by this branch-local certificate.
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  The rewritten note is still conditional on a single named
  literature import (Adler 1969 / Bell-Jackiw 1969). Closing that
  import on retained-clean lattice primitives requires upstream
  re-audit of reflection positivity, microcausality, and a yet-to-
  be-written lattice Wess-Zumino consistency theorem. Those steps
  are out of scope for this physics-loop campaign.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Dependency classes

The rewritten theorem load-bears on:

- `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29`
  (retained, positive_theorem, audited_clean) — Step 3.
- `cpt_exact_note` (retained, positive_theorem, audited_clean) — Step 3.
- `staggered_fermion_card_2026-04-10` (retained_bounded, bounded_theorem,
  audited_clean) — Step 3 cross-reference.
- `native_gauge_closure_note` (retained_bounded, bounded_theorem,
  audited_clean) — Step 2 (gauge closure for "no other gauge factor").
- `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`
  (retained, positive_theorem, audited_clean) — Step 2.
- `lh_anomaly_trace_catalog_theorem_note_2026-04-25`
  (unaudited, positive_theorem) — Step 1 anomaly arithmetic
  (cross-reference; computation is also in-line in the runner).

## Open imports

- (i) ABJ anomaly-to-inconsistency for chiral gauge theories in 3+1d
  (Adler 1969 / Bell-Jackiw 1969). This is the **single** residual
  external bridge premise after the 2026-05-02 narrowing.

## Review-loop disposition

Review-loop has not been run yet for this block. Local self-check:

- The narrowing is *honest*: three of four admissions are genuinely
  discharged on retained-clean primitives; the fourth genuinely
  remains a literature import.
- The rewritten note explicitly states this and provides a roadmap to
  closing (i) on retained-clean lattice primitives.
- The runner still passes (PASS=86 FAIL=0).
- The audit ledger pipeline runs OK with no new errors.

## Intended audit `claim_type`

`bounded_theorem` with narrowed scope (one external bridge premise:
ABJ inconsistency).

## Independent-audit handoff

Required. The rewritten theorem expects a fresh audit cycle to:

1. Verify that the discharge of admissions (ii)-(iv) on retained-clean
   primitives is sound.
2. Verify that the residual admission (i) is correctly named as the
   *only* remaining literature import.
3. Update the row's `audit_status` to `audited_clean` /
   `audited_conditional` based on the verdict.

This branch-local certificate proposes the narrowing; it does not
ratify it.
