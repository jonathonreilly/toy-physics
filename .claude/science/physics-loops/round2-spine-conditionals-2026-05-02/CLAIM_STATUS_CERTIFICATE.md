# Claim-Status Certificate — round2-spine-conditionals-2026-05-02

This certificate records the actual current-surface status, dependency
classes, and audit posture for each science block in this loop.

## Block summary

This branch narrows three critical-tier source notes to match audit
verdict repair targets. It does NOT attempt to land any retained-grade
proposal; the certificate lane is **proposed_audit_pending**, and
independent audit is REQUIRED before any of these rows can move to
`retained_bounded` / `retained` status.

## Per-row certificate

### three_generation_structure_note (290 desc, critical)

```yaml
actual_current_surface_status: audited_conditional (pre-edit)
                              -> unaudited (post-edit, hash changed)
target_claim_type: bounded_theorem
conditional_surface_status: retained_bounded if next audit ratifies the
  narrowed corner/no-quotient algebra scope only
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  Audit verdict (2026-05-02, commit 92f1812b5) explicitly named
  "narrow this row to the exact bounded corner/no-quotient algebra only"
  as the repair target. This edit applies that narrowing in source-note
  prose: claim scope reduced to exact 8 = 1 + 1 + 3 + 3 corner algebra,
  C(3,1) = 3 hw=1 degeneracy, irreducible M_3(C), no-proper-quotient,
  no-rooting. Substrate-physicality upgrade is now explicitly
  out-of-scope and delegated to cross-referenced sibling notes (all of
  which are currently audited_conditional).
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

### anomaly_forces_time_theorem (287 desc, critical)

```yaml
actual_current_surface_status: audited_conditional (pre-edit)
                              -> unaudited (post-edit, hash changed)
target_claim_type: bounded_theorem (was: positive_theorem)
conditional_surface_status: retained_bounded if next audit ratifies the
  conditional derivation under the four named external admissions
hypothetical_axiom_status: null
admitted_observation_status: |
  Four explicit external bridge admissions, all named in source-note
  Claim scope:
  (i)   ABJ anomaly-to-inconsistency for chiral gauge theory
  (ii)  opposite-chirality SU(2)-singlet completion in this Cl(3)/Z^3
  (iii) Clifford-volume-element chirality is the only grading
  (iv)  ultrahyperbolic codimension-1 obstruction (Craig-Weinstein 2009)
claim_type_reason: |
  Audit verdict (2026-05-02) named four unclosed bridge premises. This
  edit narrows source-note prose to a bounded_theorem claim conditional
  on those four explicitly-named external admissions. Step 4 of the
  proof now explicitly flags the ultrahyperbolic obstruction as a
  literature import. Step 5 (Conclusion) reads as a conditional
  derivation under the four admissions, not an unconditional 3+1
  derivation.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

### yukawa_color_projection_theorem (285 desc, critical)

```yaml
actual_current_surface_status: unaudited (already narrowed by prior
  commit d956cdd7d on 2026-05-02 14:04; hash a77d1a2b...)
target_claim_type: positive_theorem (exact algebraic identity)
conditional_surface_status: retained if next audit ratifies the
  narrowed Fierz channel-fraction = 8/9 scope on graph-visible primitives
hypothetical_axiom_status: null
admitted_observation_status: |
  Fierz identity (admitted standard math) and the SU(N_c) generator
  algebra (admitted standard math); neither is observed data.
claim_type_reason: |
  Source note already narrowed by review-loop landing d956cdd7d:
  scope reduced to the SU(N_c) Fierz channel-fraction identity
  F_adjoint = (N_c² - 1)/N_c² = 8/9 at N_c = 3. The physical-Higgs-Z
  bridge (Z_phi^phys / Z_phi^lattice = R_conn -> sqrt(8/9) y_t
  correction) is explicitly out of scope and delegated to the
  lattice -> physical matching cluster (PR #274).

  All 3 graph-visible deps now retained_bounded:
   - ew_current_fierz_channel_decomposition_note_2026-05-01
   - native_gauge_closure_note
   - graph_first_su3_integration_note

  Runner: scripts/frontier_ew_current_fierz_channel_decomposition.py
  (PASS=31 FAIL=0 verifying the scoped claim).

  No further source-note edit needed; row is already in correct state
  for next clean audit.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Block-level disposition

```yaml
review_loop_disposition: pass (self-review on the narrowing edits;
  the auditor's published repair targets are explicitly matched; no
  retained-grade promotion is asserted by this block)
audit_required_before_effective_retained: true (for all three rows)
target_independent_auditor: codex-current (or codex-gpt-5.5 fresh
  context); same auditor MUST NOT review own prior verdicts
proposed_repo_weaving:
  - none in this branch; weaving deferred to audit landing
known_open_lanes:
  - First-principles unconditional 3+1 derivation (anomaly_forces_time)
  - Substrate-physicality theorem promotion (three_generation_structure)
  - Physical-Higgs-Z bridge derivation (yukawa, separate cluster)
```

## Why this is honest narrowing not dishonest fix

For each row, the audit verdict explicitly named a "repair target" or
list of unclosed bridge premises. The narrowing applied here matches
those named repair targets exactly:

- three_generation: verdict literally said "narrow this row to the
  exact bounded corner/no-quotient algebra only".
- anomaly_forces_time: verdict named four unclosed bridge premises;
  this edit moves them all into the explicit Claim scope as external
  admissions and downgrades positive_theorem -> bounded_theorem.
- yukawa: prior review-loop landing already narrowed the source note
  to the class-A Fierz channel-fraction identity, removing the
  class-F renaming step that the audit had flagged.

No retained-grade language is asserted by this branch.
