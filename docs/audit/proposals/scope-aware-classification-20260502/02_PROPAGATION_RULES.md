# Propagation Rules — `effective_status` computation

**Date:** 2026-05-02

This document specifies the new rule that
`docs/audit/scripts/compute_effective_status.py` would implement under the
proposal.

## Inputs to the rule

For a row R, the rule reads:

- `R.audit_status`
- `R.claim_type`
- `R.decoration_parent_claim_id` (only when `audit_status =
  audited_decoration`)
- For each `dep ∈ R.dependencies`: `dep.effective_status`
- The note's location: is it in `docs/` (active) or `archive_unlanded/`
  (archived)?

## Effective-status output enum

```text
retained
retained_no_go
retained_bounded
proposed_retained
decoration_under_<parent_claim_id>
audited_renaming
audited_conditional
audited_failed
audited_numerical_match
open_gate
unaudited
```

The `support`, `bounded`, `open`, and `unknown` values are removed.
`retained_bounded` is added.

## The rule, step by step

```python
def compute_effective_status(row, deps_effective):
    # Hard early returns
    if row.audit_status == "unaudited":
        return "unaudited"
    if row.audit_status == "audit_in_progress":
        return "unaudited"

    # Decoration: boxed under parent regardless of chain
    if row.audit_status == "audited_decoration":
        return f"decoration_under_{row.decoration_parent_claim_id}"

    # Terminal failure verdicts on active notes
    if row.audit_status == "audited_renaming":
        return "audited_renaming"
    if row.audit_status == "audited_numerical_match":
        return "audited_numerical_match"

    # Failed: archived versus active
    if row.audit_status == "audited_failed":
        if note_is_archived(row.note_path):
            return "retained_no_go"   # ratified failure record
        return "audited_failed"

    # Conditional: depends on something not yet ratified
    if row.audit_status == "audited_conditional":
        return "audited_conditional"

    # audit_status = audited_clean from here on
    assert row.audit_status == "audited_clean"

    # Open-gate: clean partial work, never propagates to retained
    if row.claim_type == "open_gate":
        return "open_gate"

    # Meta: not a claim, exclude from library
    if row.claim_type == "meta":
        return "meta"   # rendering note: hidden from publication tables

    # Now we have a clean theorem of some kind. Check chain.
    # Inheritance is monotone-down on the retained-grade frontier.
    chain_clean = all(
        d in {"retained", "retained_no_go", "retained_bounded"}
        for d in deps_effective
    )

    if not chain_clean:
        # Honest pending state. Auto-resolves when chain clears.
        return "proposed_retained"

    # Chain is clean. Promote by claim_type.
    if row.claim_type == "positive_theorem":
        return "retained"
    if row.claim_type == "no_go":
        return "retained_no_go"
    if row.claim_type == "bounded_theorem":
        return "retained_bounded"

    raise ValueError(f"unhandled claim_type {row.claim_type}")
```

## Inheritance and demotion semantics

**Monotone-down inheritance.** `retained`, `retained_no_go`, and
`retained_bounded` are equally valid as inputs to a downstream chain — each
is a clean ratified statement. A claim that depends only on members of this
set is eligible for its own clean propagation.

Any other dependency (`unaudited`, `proposed_retained`,
`audited_conditional`, `audited_renaming`, `audited_numerical_match`,
`audited_failed`, `decoration_under_*`, `open_gate`, `meta`) blocks the
downstream from propagating beyond `proposed_retained`.

This means: a downstream `audited_clean, claim_type=positive_theorem` whose
parent is `audited_conditional` becomes `proposed_retained`, not `retained`.
When the parent's conditional is resolved (re-audit or repair), the
downstream auto-promotes on the next pipeline run. No author intervention
required.

## What `proposed_retained` means under this rule

`proposed_retained` is no longer author-set. It is a *computed transient
state* meaning: "this claim's audit is clean, but its dependency chain has
not all reached retained-grade yet." Its function is to keep the audit
ledger honest about what is and is not yet effective, while making the
unblock automatic when upstream resolves.

This eliminates the current 122-row backlog of "support + audited_clean"
rows that need author relabel. Under the new rule, they would be
`proposed_retained` immediately upon clean audit, then promote to `retained`
the moment the upstream chain clears.

## Worked example: yesterday's 10 axiom-first thermo blocks

Assume the upstream chain (RP, spectrum cond, cluster decomp,
spin-statistics) is in the `audited_clean` state Codex already returned.

| Block | `claim_type` (proposed) | dep chain | result |
|---|---|---|---|
| 01 KMS | positive_theorem | RP + spectrum cond | `proposed_retained` until upstream → `retained` immediately after |
| 02 Hawking T_H | bounded_theorem (depends on Killing-horizon admission) | Block 01 + framework GR | `proposed_retained` → `retained_bounded` |
| 03 Bekenstein bound | bounded_theorem (depends on BH 1/4) | framework GR + BH 1/4 | `proposed_retained` until BH 1/4 closes |
| 04 microcausality | positive_theorem | RP + spectrum cond + cluster decomp | `proposed_retained` → `retained` |
| 05 first law | bounded_theorem (depends on BH 1/4) | Block 02 + BH 1/4 | `proposed_retained` until BH 1/4 closes |
| 06 Stefan-Boltzmann | positive_theorem | Block 01 + retained EW + emergent Lorentz + spin-statistics | `proposed_retained` → `retained` |
| 07 Reeh-Schlieder | positive_theorem | RP + spectrum cond + cluster decomp + Block 04 | `proposed_retained` → `retained` |
| 08 Unruh | positive_theorem | Block 01 + retained Lorentz kernel | `proposed_retained` → `retained` |
| 09 Birkhoff | positive_theorem | retained framework GR | `retained` immediately (chain already clean) |
| 10 GSL | bounded_theorem (depends on BH 1/4 + admitted NEC) | Block 01 + Block 02 + Block 05 + BH 1/4 | `proposed_retained` until BH 1/4 closes |

Result: 6 of the 10 blocks (01, 04, 06, 07, 08, 09) propagate to
`retained` (or `retained_bounded` for those with an honest narrow scope
admitted in the auditor's `claim_scope` field) the moment Codex confirms the
upstream chain. 4 stay at `proposed_retained` until the BH 1/4 carrier
science gap is closed — which is the actual remaining work, not a paperwork
issue.
