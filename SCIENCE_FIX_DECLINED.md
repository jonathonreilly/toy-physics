# SCIENCE_FIX_DECLINED — universal_qg_optional_textbook_comparison_note

**Claim:** `universal_qg_optional_textbook_comparison_note`
**Category:** `audited_renaming` (Class E; descendants: 775; criticality: critical)
**Disposition:** SCIENCE_FIX_DECLINED — fold; the prompt's target verdict
(`audited_clean` at retained-grade) is structurally unreachable for this row
by the framework's own audit rubric.

## Auditor verdict context

The row's two most recent audits (2026-05-02 cluster2-narrow Claude and
2026-05-04 codex-cli-gpt-5.5) both returned `audited_renaming`. The 2026-05-04
audit also recorded `chain_closes: true` — the meta-packaging boundary closes
on its own terms with no missing dependency. Both audits give the same
load-bearing step:

> This note is packaging-only and is not a theorem, claim, or new authority surface.

The row is currently `unaudited` only because of an
`invalidation_reason: criticality_increased:high->critical` bump after the
2026-05-04 audit; the underlying scientific content of the note and runner
have not regressed.

## Why `audited_clean` is structurally unreachable here

Per `docs/audit/AUDIT_AGENT_PROMPT_TEMPLATE.md`, the verdict
`audited_renaming` is the prescribed outcome for any row whose load-bearing
step is class `(E)` (definition substitution) or `(F)` (renaming). The
template's tie-breaking section is explicit:

> `audited_clean` vs `audited_renaming` → choose `audited_renaming`. The
> burden is on the derivation to be unambiguously class (C) or genuine (A)
> over independent inputs.

This note's load-bearing step is a packaging-boundary declaration — class
`(E)` by construction, because the note **is** a packaging row and explicitly
disclaims theorem authority. There is no class-(C) computation hiding inside
that could be promoted, and adding one would convert the note from
packaging-row to theorem-row, which would be exactly the failure mode the
2026-05-02 and 2026-05-04 auditors flagged ("the audit cannot ratify the
seeded positive-theorem hint").

## Three repair routes considered

1. **Promote to a theorem with derivational content.**
   Infeasible / regressive. The note exists specifically as a stable citation
   target for "optional textbook comparison" callouts from downstream
   universal-QG notes (22 such inbound mentions, all guarded as packaging
   callouts per the runner's class-B check). Promoting it would (a)
   contradict the note's own §3 "What this note is *not* for" firewall, (b)
   create the seeded-positive-theorem mismatch the prior auditors named, and
   (c) duplicate work that belongs in the five separately-rowed
   `UNIVERSAL_QG_CANONICAL_*` claims cross-referenced in §4.

2. **Reclassify as `audited_decoration` of an upstream parent.**
   Blocked by missing parent. `audited_decoration` requires the parent to be
   a retained-grade closed claim. All five cross-referenced parent
   candidates are themselves currently `unaudited`:
   - `universal_qg_canonical_textbook_continuum_gr_closure_note`
   - `universal_qg_canonical_smooth_gravitational_weak_measure_note`
   - `universal_qg_canonical_textbook_geometric_action_equivalence_note`
   - `universal_qg_canonical_textbook_weak_measure_equivalence_note`
   - `universal_qg_continuum_bridge_reduction_note`

   None is retained-grade. Decoration cannot anchor against an unaudited
   parent under the rubric.

3. **Demote further.**
   Already at minimum. The note is already typed `meta` (the lowest
   claim_type), has `authority_role: zero`, has no markdown links to other
   docs, has no Citations section, and explicitly disclaims theorem / claim /
   new authority status. There is no further demotion available within the
   ledger's vocabulary.

## State of the existing repair

The 2026-05-06 commit `9ec2b66d0` ("review-loop: land universal QG meta
guard") already landed the zero-authority metadata invariant runner
(`scripts/universal_qg_optional_textbook_comparison_meta_check.py`) that the
2026-05-02 verdict flagged as missing ("With no cited authorities or runner,
the only closed item is the packaging boundary itself"). The runner currently
passes 10/10 checks (A=9, B=1) and certifies the Z0–Z5 zero-authority
invariant directly against the repository text. On the framework's terms the
row is already in its terminal, ratifiable shape — the appropriate verdict on
re-audit is the same `audited_renaming` the prior two auditors landed.

## Recommended next action (out of scope here)

Re-audit this row as-is. Per the framework's tie-breaking rules the verdict
will be `audited_renaming` with `chain_closes: true`, matching both prior
audits. That is the correct terminal state for a properly-scoped meta
packaging row. If/when a downstream consumer cites this note as one-hop
authority for a substantive textbook-comparison claim (which the §3 firewall
forbids and the runner's class-B inbound-context check actively enforces),
re-audit guidance is given in the prior `notes_for_re_audit_if_any`:

> Re-check only if this note is later used as authority for the underlying
> continuum-target closure; that would require auditing the actual upstream
> closure note.

## Contents

- `SCIENCE_FIX_DECLINED.md` (worktree root only) — this narrative.

No `docs/`, `scripts/`, or `docs/audit/**` files are touched. No audit
verdict is claimed. No audit-data file is modified. No overclaim of
derivation. The author-declared scope and the prior auditors' verdicts are
unchanged by this PR.
