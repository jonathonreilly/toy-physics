# Claim Status Certificate — Block 04 (Microcausality / Lieb-Robinson)

**Date:** 2026-05-01 (originally) / 2026-05-02 (reframed under scope-aware classification)
**Block:** 04 — Microcausality / Lieb-Robinson on A_min
**Slug:** `24h-axiom-first-derivations-20260501`
**Branch:** `physics-loop/24h-axiom-first-block04-microcausality-20260501`
**Base:** origin/main (independent of Blocks 01-03)
**Note:** [docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md](../../../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
**Runner:** [scripts/axiom_first_microcausality_check.py](../../../../scripts/axiom_first_microcausality_check.py)
**Log:** [outputs/axiom_first_microcausality_check_2026-05-01.txt](../../../../outputs/axiom_first_microcausality_check_2026-05-01.txt)

## Framework

Reframed under the scope-aware classification framework adopted 2026-05-02
(audit-lane proposal #291). Authors do not assign tiers; auditor records
`claim_type` and `audit_status`; pipeline derives `effective_status`.

## Author classification (non-authoritative hint to auditor)

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "Equal-time strict locality [O_x, O_y]=0 for x≠y on Cl(3) tensor structure (M1); Lieb-Robinson lightcone bound ‖[α_t(O_x), O_y]‖ ≤ 2‖O_x‖‖O_y‖exp(-d + v_LR|t|) with v_LR=2erJ on framework's finite-range Hamiltonian (M2); continuum spacelike microcausality in the smooth-limit Lorentz regime (M3)."
admitted_context_inputs:
  - Lieb-Robinson 1972 estimate (theorem-grade lattice-statistics reference)
upstream_dependencies:
  - axiom_first_reflection_positivity_theorem_note_2026-04-29 (Codex audited_clean cross_family; awaiting framework-adoption sweep to lift effective_status)
  - axiom_first_spectrum_condition_theorem_note_2026-04-29 (Codex audited_conditional — needs RP citation registered as ledger dep)
  - axiom_first_cluster_decomposition_theorem_note_2026-04-29 (Codex audited_clean cross_family; awaiting framework-adoption sweep)
  - emergent_lorentz_invariance_note (retained)
  - lorentz_kernel_positive_closure_note (retained)
runner_classified_passes: 4 PASS, including small-t scaling t^d at 3-4 sig figs across d=2,3,4
```

## Expected `effective_status` after audit

If Codex returns `audit_status = audited_clean` and `claim_type =
positive_theorem`:

- **Path A** (RP + cluster_decomp upstream both reach retained, spectrum
  condition's dep-registration repair lands): `effective_status = retained`
  immediately on next pipeline run.
- **Path B** (spectrum condition stays `audited_conditional`):
  `effective_status = proposed_retained` (computed transient state, auto-
  resolves when spectrum condition's dependency-registration is repaired
  and re-audited).

The block 04 chain has **no admitted load-bearing physics input** beyond
the Lieb-Robinson 1972 lattice-statistics theorem reference. Only the
upstream chain status gates promotion.

## Dependency chain status snapshot (2026-05-02)

| Dep | Today's `effective_status` (post adoption) |
|---|---|
| RP | support (Codex audited_clean; awaiting lift via new propagation rule) |
| Spectrum cond | audited_conditional (Codex flagged: register RP as ledger dep) |
| Cluster decomp | support (Codex audited_clean; awaiting lift) |
| Emergent Lorentz | retained |
| Lorentz kernel | retained |

The spectrum-condition `audited_conditional` is the load-bearing block. A
single mechanical fix (registering RP as a one-hop dependency in the ledger
row, then re-running the pipeline) unblocks Block 04's promotion under the
new framework.

## Review-loop disposition

- branch-local self-review: `pass` (theorem proof matches runner; small-t
  scaling t^d agrees to 3-4 sig figs).
- formal `/review-loop`: deferred to integration-time.
- formal Codex audit: pending under new prompt template
  ([`PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md`](../../../../docs/audit/proposals/scope-aware-classification-20260502/PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md)).

## Audit hand-off

What the auditor needs to evaluate this note:

1. The note itself.
2. The five cited authority notes (RP, spectrum cond, cluster decomp,
   emergent Lorentz, Lorentz kernel) plus `MINIMAL_AXIOMS_2026-04-11.md`.
3. The runner script and its output.
4. The new audit prompt template.

Block 04 completes the framework's local-algebra structure together with
Block 07 (Reeh-Schlieder cyclicity) and the Apr 29 axiom-first foundations.
