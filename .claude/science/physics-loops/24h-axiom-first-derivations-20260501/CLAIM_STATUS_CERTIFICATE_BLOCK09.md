# Claim Status Certificate — Block 09 (Birkhoff theorem)

**Date:** 2026-05-01 (originally) / 2026-05-02 (reframed under scope-aware classification)
**Block:** 09 — Birkhoff theorem (vacuum spherical → Schwarzschild static)
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block09-birkhoff-20260501`
**Base:** origin/main (independent of Blocks 01-08)
**Note:** [docs/AXIOM_FIRST_BIRKHOFF_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_BIRKHOFF_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_birkhoff_check.py](../../../../scripts/axiom_first_birkhoff_check.py)
**Log:** [outputs/axiom_first_birkhoff_check_2026-05-01.txt](../../../../outputs/axiom_first_birkhoff_check_2026-05-01.txt)

## Framework

This certificate is reframed under the scope-aware classification framework
adopted 2026-05-02 (proposal package
[`docs/audit/proposals/scope-aware-classification-20260502/`](../../../../docs/audit/proposals/scope-aware-classification-20260502/)).
Under that framework: authors do not assign tiers; the auditor records
`claim_type` and `audit_status`; `effective_status` is derived by the audit
pipeline. This certificate is informational — the canonical surface is
`docs/audit/AUDIT_LEDGER.md` post-audit.

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Any spherically-symmetric vacuum (T_μν = 0) solution of the framework's retained discrete GR action is locally isometric to a piece of Schwarzschild and is therefore necessarily static, with metric (1 - 2GM/r) dt² + (1 - 2GM/r)⁻¹ dr² + r² dΩ²."
admitted_context_inputs:
  - spherically-symmetric metric ansatz (Hawking-Ellis 1973)
  - standard tensor calculus on framework smooth-limit equivalence surface
upstream_dependencies:
  - UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md (retained)
  - UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md (retained)
runner_classified_passes: 6 PASS, all class-A symbolic / class-C identity (per Test summary)
```

## Audit handoff

Audit status is set only by the independent audit lane. Review-loop does not
prefill an `audit_status` or promise an `effective_status`; after any clean
independent audit, the pipeline derives effective status from `claim_type` plus
dependency closure. If the auditor classifies the smooth-limit admission as a
bounded premise, the retained-family result should remain bounded rather than
being promoted by review prose.

## Dependency chain

| Dep | Today's `effective_status` | Affects propagation? |
|---|---|---|
| `universal_gr_discrete_global_closure_note` | retained | clean |
| `universal_qg_canonical_textbook_geometric_action_equivalence_note` | retained | clean |
| Spherically-symmetric ansatz | admitted-context (basic GR) | n/a |
| Standard tensor calculus | admitted-context (basic differential geometry) | n/a |

Chain is clean. Nothing in this block's dep chain blocks promotion.

## Review-loop disposition

- branch-local self-review: `pass` (algebraic chain verified; Schwarzschild
  satisfies all four diagonal R_μν = 0 conditions; ODE residual at <1e-15).
- formal `/review-loop`: deferred.
- formal Codex audit: pending. Block 09 is a candidate for the first
  retained promotion under the new framework because its upstream is the
  shortest of any block (only the framework GR action surface).

## Audit hand-off

What an auditor needs to evaluate this note:

1. The note itself.
2. The two cited authority notes (UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE
   and UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE).
3. The runner script and its output.
4. The new audit prompt template
   ([`PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md`](../../../../docs/audit/proposals/scope-aware-classification-20260502/PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md))
   which asks for `claim_type` and `claim_scope` alongside the standard
   verdict.

The auditor's `claim_type` and `audit_status` together with the dep chain
determine `effective_status` per the new rule.
