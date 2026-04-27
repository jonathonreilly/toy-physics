# Lane 2: Register the missing gauge-closure runners → unblock native_gauge_closure

**Status:** OPEN — accepting workers (mostly hygiene, some science).
**Source claim:** [`native_gauge_closure_note`](../../../docs/NATIVE_GAUGE_CLOSURE_NOTE.md)
**Audit verdict:** `audited_conditional`
**Criticality:** `critical` · **Transitive descendants:** 276 · **Load-bearing class:** B (cross-note input verification)

The "exact native SU(2), graph-first SU(3)" backbone of the framework
sits here. The audit cannot ratify it because the supporting computations
are referenced by name but not registered as auditable inputs.

## Audit finding (verbatim from the ledger)

**Load-bearing step under audit:**

> Use this note as the publication-facing claim boundary for the
> Cl(3) / Z³ gauge lane on main: exact native Cl(3) / SU(2) algebra,
> derived graph-first weak-axis selector, and structural graph-first
> SU(3) closure.

**Why the chain does not close:**

The note aggregates three sub-results (SU(2) algebra, graph-first
selector, SU(3) integration), but the audit row has no one-hop
dependencies and no registered primary runner. The claimed publication
boundary therefore does not close from the allowed audit packet —
the auditor cannot verify what they cannot read.

**Open one-hop dependencies (currently unregistered):**

- `scripts/frontier_non_abelian_gauge.py`
- `scripts/frontier_graph_first_selector_derivation.py`
- `scripts/frontier_graph_first_su3_integration.py`

## Repair target

This is mostly **registration hygiene**, with one science-side gate:

1. Register each of the three scripts above as registered runners on
   the appropriate sub-claim notes.
2. Register the corresponding sub-claim notes as one-hop dependencies
   of `NATIVE_GAUGE_CLOSURE_NOTE.md`.
3. Either attach a primary runner to `NATIVE_GAUGE_CLOSURE_NOTE.md`
   directly, **or** split the boundary into separate auditable claims
   (one per sub-result).
4. Resolve the cross-confirmation status of `graph_first_su3_integration_note`
   and `graph_first_selector_derivation_note` (currently
   `audit_in_progress`, awaiting second auditor).

## Why this is high-leverage

276 descendants. The "native SU(2) and graph-first SU(3)" backbone is
upstream of the Standard Model gauge structure, anomaly cancellation,
and most of the EW/strong-sector machinery downstream. As long as this
lane sits at `audited_conditional`, the entire SM-gauge-structure
package on main reads as conditional in `effective_status`.

## Claim boundary while this lane is open

Per the audit verdict:

- It is safe to use `NATIVE_GAUGE_CLOSURE_NOTE.md` as a **bounded map**
  of intended gauge-lane claims and to say the listed components have
  supporting scripts.
- It is **not** safe to treat the combined gauge-structure backbone as
  audit-retained.

## Suggested approach (worker-side)

This is two parallel tracks:

### Track A: hygiene (most of the work)

1. Open the three scripts; verify they exist and run.
2. On each script's natural home note, add `**Primary runner:** scripts/...`
3. On `NATIVE_GAUGE_CLOSURE_NOTE.md`, replace the bare aggregator
   prose with explicit markdown links to the three sub-claim notes
   (so the citation graph picks them up as dependencies).
4. Re-run `bash docs/audit/scripts/run_pipeline.sh`. The hash drift
   resets the affected audit rows; Codex re-audits.

### Track B: cross-confirmation push

`graph_first_su3_integration_note` and `graph_first_selector_derivation_note`
are at `audit_in_progress` waiting for a second auditor. A second
independent auditor (Codex in a fresh session, or a human) running the
same prompt against these two claims will move them to `audited_clean`
if the verdicts match. Without the cross-confirmation, the parent
boundary cannot ratify.

## Success criteria

- All three sub-claim notes are registered with primary runners.
- All three are linked from `NATIVE_GAUGE_CLOSURE_NOTE.md` so the
  citation graph picks them up as dependencies.
- `graph_first_su3_integration_note` and `graph_first_selector_derivation_note`
  reach `audited_clean` after cross-confirmation.
- `native_gauge_closure_note` re-audits as `audited_clean`, then
  `effective_status = retained` after dependency propagation.

## Branch / worker conventions

- Hygiene track: `claude/native-gauge-runner-registration-2026-04-27`.
  Small commits, one per registration.
- Cross-confirmation track: separate Codex session running
  `AUDIT_AGENT_PROMPT_TEMPLATE.md` against the two pending claims.

## What this lane is NOT

- Not a re-derivation of SU(2) or SU(3) on the lattice. The
  derivations exist in the runners; they just aren't wired into the
  audit graph.
- Not a Yang-Mills attack. If the runners pass under audit, the
  combined boundary closes.
- Not a place to expand the gauge claim surface. Stay scoped.
