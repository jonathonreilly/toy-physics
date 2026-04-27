# Science Worker Queue

**Status:** open queue, accepting workers.
**Generated:** 2026-04-27 from the audit-lane ledger after the first
~10% of audits landed.

This is the priority-ordered list of audit-surfaced science problems
that need dedicated workers. Each lane has a structured handoff doc
under `worker_lanes/` with the audit verdict, the load-bearing failure,
the repair target, and suggested approach. A worker (Claude / Codex
session) should be able to pick up a lane cold from its handoff doc
without further context.

## How this queue is generated

The audit lane (`docs/audit/`) ratifies claims from
`current_status: proposed_retained` to `effective_status: retained`
only when an independent auditor (Codex GPT-5.5 by default) confirms
the derivation closes from cited inputs. After the first 164 audits
landed on `main`, the ledger surfaced the failure modes summarized
below. Lanes are ordered by **load-bearing impact** — transitive
descendants the lane unblocks plus criticality tier.

## Lanes

| # | Lane | verdict | crit | desc | unblocks | handoff |
|---|---|---|---|---:|---|---|
| 1 | RCONN derivation → unblock EW color projection | `audited_conditional` | critical | 278 | EW couplings, sin²θ_W, 1/α_EM | [`worker_lanes/01_rconn_derivation.md`](worker_lanes/01_rconn_derivation.md) |
| 2 | Native gauge runners — registration + cross-confirm | `audited_conditional` | critical | 276 | SU(2)/SU(3) gauge structure backbone | [`worker_lanes/02_native_gauge_runners.md`](worker_lanes/02_native_gauge_runners.md) |
| 3 | Equivalence principle chain repair | `audited_failed` | high | 119 | gravity/GR program | [`worker_lanes/03_equivalence_principle.md`](worker_lanes/03_equivalence_principle.md) |
| 4 | YT UV-to-IR transport — first principles | `audited_numerical_match` | high | 120 | top mass m_t, Higgs vacuum stability | [`worker_lanes/04_yt_uv_to_ir_first_principles.md`](worker_lanes/04_yt_uv_to_ir_first_principles.md) |
| 5 | DM neutrino Z3 phase lift — derive or downgrade | `audited_renaming` | high | 119 | DM "flagship closed" package | [`worker_lanes/05_dm_neutrino_z3_phase_lift.md`](worker_lanes/05_dm_neutrino_z3_phase_lift.md) |

Total downstream impact: each lane closes a different region of the
package. Lanes 1 and 2 alone unblock ~554 descendants by inheritance
once they ratify.

## Workflow per lane

1. **Pick a lane** from the table above. Read the handoff doc end-to-end.
2. **Open a proposal branch** using the naming convention in the handoff
   doc (`claude/<lane-slug>-2026-04-27` or Codex equivalent).
3. **Do the science.** Each handoff doc gives a "suggested approach"
   section. Multiple paths may be open per lane (e.g., Path A: derive,
   Path B: structural, Path C: honest downgrade). Pick one.
4. **Land the work** as a focused PR. The audit lane will detect the
   note hash drift and reset affected rows to `unaudited`.
5. **Codex re-audits** under the standard rubric. Critical claims need
   cross-confirmation by a second independent auditor.
6. **Outcome:** `audited_clean` → ratifies to `retained`. Other verdict
   → re-iterate, or accept the narrower claim boundary.

## Scope rules

- These are **dedicated** science worker lanes, not general autopilot
  exploration. Stay scoped to the lane's repair target.
- **Honest downgrade is a valid outcome** for every lane. The audit
  lane's job is to surface unratified claims; turning a renaming into
  a support-tier observation is a real win.
- **Do not expand claim surface** while closing these lanes. Each
  lane either closes an existing claim or honestly narrows it; none
  is an opportunity to add new retained-tier claims.
- **No self-audit.** A worker that produces a lane's proposal cannot
  also audit it. Per `FRESH_LOOK_REQUIREMENTS.md`, the auditor must
  be in a different model family or a different human.

## What this queue does NOT include

- The 84 `audited_conditional` rows that are blocked only on
  unregistered runners or unregistered one-hop dependencies. Most of
  those are hygiene fixes, not science. They will resolve as the
  graph dependencies get registered through normal repo flow; no
  dedicated worker needed.
- The 22 leaf-level `audited_failed` rows. Those are isolated and
  can be triaged by individual contributors as they touch the affected
  notes.
- The 3 `audited_decoration` rows. Per `ALGEBRAIC_DECORATION_POLICY.md`,
  these get boxed under their parent claims rather than worked on as
  separate science problems.

## Re-running this queue

The queue is regenerated whenever the audit lane completes another
batch. The current snapshot reflects the audit state at ~10% coverage
(164 of 1614 claims audited). As more audits land, new high-leverage
lanes may appear; closed lanes drop off. Refresh by re-running the
audit pipeline and re-querying the ledger for `audited_failed`,
`audited_renaming`, `audited_conditional` (high+ criticality), and
`audited_numerical_match` rows.

## Cross-references

- Audit lane policy: [`README.md`](README.md)
- Auditor independence rules: [`FRESH_LOOK_REQUIREMENTS.md`](FRESH_LOOK_REQUIREMENTS.md)
- Decoration handling: [`ALGEBRAIC_DECORATION_POLICY.md`](ALGEBRAIC_DECORATION_POLICY.md)
- Audit prompt template: [`AUDIT_AGENT_PROMPT_TEMPLATE.md`](AUDIT_AGENT_PROMPT_TEMPLATE.md)
- Active audit ledger: [`AUDIT_LEDGER.md`](AUDIT_LEDGER.md)
- Pending audit queue (mechanical): [`AUDIT_QUEUE.md`](AUDIT_QUEUE.md) —
  this is different from the science worker queue: it lists claims
  awaiting a fresh-look audit, not science problems surfaced by
  completed audits.
