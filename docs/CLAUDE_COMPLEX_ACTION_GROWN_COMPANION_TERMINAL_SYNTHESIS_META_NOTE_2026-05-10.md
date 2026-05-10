# Claude Complex Action Grown Companion Terminal Synthesis Meta Note

**Date:** 2026-05-10
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal; pipeline-derived status set only after independent audit
review.
**Authority role:** records the structural block on the critical leaf
[`claude_complex_action_grown_companion_note`](CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md):
the runner imports its load-bearing grown geometry from
[`scripts/gate_b_grown_joint_package.py`](../scripts/gate_b_grown_joint_package.py)
without that module being registered as a one-hop dependency edge in
the leaf's `deps[]` array, and without that module's authority being
retained-grade. Documents the finding so future automated audit-backlog
or retained-promotion campaigns do not spend cycles attempting to close
this leaf through routes that do not address the recorded
`missing_dependency_edge` repair class.
**Companion to:**
- [`docs/audit/README.md`](audit/README.md) (audit-lane policy:
  retained-grade dependencies, terminal verdicts, repair classes)
- [`QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md`](QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md)
  (PR #959 — sibling terminal-block synthesis on the quark projector chain)
- [`DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md)
  (PR #960 — sibling terminal-block synthesis on the DM leptogenesis transport chain)
- [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
  (parallel terminal-synthesis template)
**Primary runner:** [`scripts/frontier_claude_complex_action_grown_companion_terminal_synthesis.py`](../scripts/frontier_claude_complex_action_grown_companion_terminal_synthesis.py)
**Cached output:** [`logs/runner-cache/frontier_claude_complex_action_grown_companion_terminal_synthesis.txt`](../logs/runner-cache/frontier_claude_complex_action_grown_companion_terminal_synthesis.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim. This note is
backward-looking: it cites already-recorded upstream audit verdicts in
[`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json) and
synthesises the structural consequence for the leaf. It does not
promote theorems, does not modify retained content, does not propose
new derivations, and does not reclassify any audit row. No new
vocabulary, claim type, or framing is introduced. All terminal-verdict
language used here (`audited_conditional`, `missing_dependency_edge`,
`retained-grade dependencies`) is repo-canonical and matches the audit
lane's existing field values per
[`docs/audit/README.md`](audit/README.md).

## Context

This is the third of three backward-looking deprioritization syntheses
documenting critical leaves whose audit cannot close as currently
structured. The first synthesis (PR #959) covers the quark projector
parameter audit chain; the second (PR #960) covers the DM leptogenesis
transport status chain. This note covers the
`claude_complex_action_grown_companion_note` leaf, identified in the
same sweep. Each of the three leaves has the same structural shape: the
audit-lane verdict already records the precise structural block, and
no bounded source-note repair closes that block — the chain cannot
retain as currently structured.

## Naming

Throughout this note:
- **"the leaf"** =
  [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md) —
  claim_id `claude_complex_action_grown_companion_note`
- **"the runner"** =
  [`scripts/complex_action_grown_companion.py`](../scripts/complex_action_grown_companion.py) —
  the leaf's `runner_path` per the live ledger
- **"the imported module"** =
  [`scripts/gate_b_grown_joint_package.py`](../scripts/gate_b_grown_joint_package.py) —
  the runner's `from scripts.gate_b_grown_joint_package import grow`
  load-bearing geometry import; carries claim_id
  `gate_b_grown_joint_package_note`
- **"missing dependency edge"** = the audit-lane repair class for an
  authority that exists or is named but is not wired as a direct
  dependency, per [`docs/audit/README.md`](audit/README.md) lines 192-193

## Leaf claim under review

`claude_complex_action_grown_companion_note` — current ledger row:

- `claim_type`: `positive_theorem`
- `audit_status`: `unaudited` (current row, after note-hash drift
  invalidation that re-seeded the prior `audited_conditional` verdict;
  see `previous_audits[]` `archived_for_note_hash` entries)
- `criticality`: `critical`
- `transitive_descendants`: 400
- `direct_in_degree`: 6
- `load_bearing_score`: 11.647
- `deps`: `[]` (empty — the imported grown-geometry module is **not**
  registered as a one-hop dependency edge, which is the recorded
  structural block)

The leaf is one of the highest-fan-in audit-pending rows on the
gravity-grown lane. Its 400 transitive descendants make it
cost-amortisation-attractive at first glance, but the recorded
auditor verdicts localise the block to a single missing-dependency-edge
gate that no bounded source-note repair satisfies.

## Terminal upstream block

The leaf has been audited four times. The relevant facts from
`previous_audits[]` (most-recent first):

### Audit 4 (archived 2026-05-10, hash drift) — `audited_conditional`

| Field | Value |
|---|---|
| `auditor_family` | `codex-gpt-5.5` |
| `audit_status` | `audited_conditional` |
| `chain_closes` | `false` |
| `independence` | `cross_family` |
| `auditor_confidence` | `high` |
| `open_dependency_paths` | `["scripts/gate_b_grown_joint_package.py"]` |

Auditor `chain_closure_explanation` (verbatim):

> "The runner numerically computes the reported propagation, Born proxy,
> weak-field scaling, and gamma sweep, but it imports the
> grown-geometry generator from `scripts.gate_b_grown_joint_package`
> without that dependency being provided. The retained grown-row
> geometry and its accepted status are therefore an imported premise in
> the restricted packet."

Auditor `verdict_rationale` (verbatim):

> "The stdout is consistent with the note's reported narrow numerical
> results, aside from a small Born-proxy value discrepancy within the
> same machine-clean scale. The runner is not a trivial printout and
> does perform propagation and scaling checks, but the load-bearing
> grown geometry comes from an unprovided imported module rather than a
> closed derivation from the axiom inside the packet. With no cited
> retained authority supplied for that grown row, the conclusion
> remains conditional on the missing geometry dependency."

Auditor `notes_for_re_audit_if_any` (verbatim):

> "missing_dependency_edge: provide the grow implementation and
> retained-grade authority or certificate for the drift=0.2,
> restore=0.7 grown row, then re-audit whether the numerical replay
> closes from that supplied dependency."

### Audit 3 (archived 2026-05-04, criticality bump) — `audited_conditional`

| Field | Value |
|---|---|
| `auditor_family` | `codex-gpt-5` |
| `audit_status` | `audited_conditional` |
| `chain_closes` | `false` |
| `independence` | `fresh_context` |
| `invalidation_reason` | `criticality_increased:high->critical` |

Auditor `chain_closure_explanation` (verbatim):

> "The source note relies on unprovided retained-status premises for
> the grown row and the exact-lattice complex-action carryover, and
> the current runner did not complete the full frozen gamma sweep in
> this audit pass. Partial observed output supports only the
> gamma=0/Born-proxy boundary, not the full claimed replay."

Auditor `verdict_rationale` (excerpt — repair target verbatim):

> "Repair target: provide one-hop retained authorities for the grown
> row and exact-lattice carryover, and make the runner reproducibly
> emit the full gamma/F~M/crossover table in an audit-bounded run."

### Audit 2 (archived 2026-05-03, criticality bump) — `audited_clean` (legacy backfill)

| Field | Value |
|---|---|
| `auditor_family` | `codex-gpt-5` |
| `audit_status` | `audited_clean` (backfilled at `criticality=leaf`) |
| `independence` | `cross_family` |
| `invalidation_reason` | `criticality_increased:leaf->high` |

This entry was a scope-aware classification migration backfill at
`criticality=leaf` (per the recorded `audit_state_snapshot.criticality`
= `leaf`). It was invalidated when the leaf's criticality bumped from
`leaf` to `high`, and the subsequent fresh-context audit (Audit 3)
reverted the verdict to `audited_conditional` on the explicit
unprovided-retained-status-premise grounds. This audit does **not**
support a current retained-grade reading: it predates the
criticality-bump policy fixes (PR #907 / PR #925) and was already
re-audited under the corrected policy.

### Audit 1 (archived 2026-04-27) — `unaudited`

Initial seed; no auditor; no rationale. Recorded for completeness.

### Convergent finding across the conditional verdicts

Both `audited_conditional` verdicts (Audits 3 and 4) localise the same
structural block. Audit 3 phrases it as "unprovided retained-status
premises for the grown row"; Audit 4 names the specific imported
module (`scripts/gate_b_grown_joint_package`) and tags the repair class
explicitly as `missing_dependency_edge`. The two independent
fresh-context auditors (one `cross_family`, one `fresh_context`)
converge on the same gate. The auditor language is repo-canonical
(`missing_dependency_edge`, `retained-grade authority`,
`imported premise`) and matches [`docs/audit/README.md`](audit/README.md)
hard rule 2 ("Open gates block propagation. ... `unaudited` ... are not
retained-grade dependencies") and the `missing_dependency_edge` repair
class definition.

The imported module's claim_id `gate_b_grown_joint_package_note`
currently carries `audit_status=unaudited` and `effective_status=unaudited`
in the live ledger. Per hard rule 2, an `unaudited` row is not a
retained-grade dependency — even if the dep edge were registered, the
chain would still not close to retained without the upstream first
reaching `audited_clean` and retained-grade itself.

## Repair surface analysis

The leaf cannot retain while its load-bearing grown geometry is
imported from a module that is (a) not registered as a one-hop
dependency in the leaf's `deps[]` array, and (b) not itself
retained-grade. Per [`docs/audit/README.md`](audit/README.md) hard rule
1 ("Retained grade is audit-only ... only from `claim_type +
audited_clean + retained-grade dependencies`"), the chain cannot
promote without one of the following structural repairs:

1. **Register the dep + retain the upstream.** Add
   `gate_b_grown_joint_package_note` (or its retained equivalent) as
   an explicit `deps[]` edge in the source note via citation, and have
   that module audited to `audited_clean` with retained-grade
   dependencies of its own — the latter being a separate audit-lane
   work item, not a leaf-level edit.
2. **Inline the grown-geometry construction into the source note
   itself with full closure proof.** Replace the runner's
   `from scripts.gate_b_grown_joint_package import grow` with a
   self-contained construction whose closure is proved inside the
   leaf's packet, removing the imported-premise gate entirely.

### Why neither path is a small bounded source note

Path 1 requires the upstream `gate_b_grown_joint_package_note` —
currently `unaudited` with no retained-grade dependency closure of its
own — to first land its own `audited_clean` verdict with retained-grade
dependencies. The upstream module implements the runner-defined
`drift=0.2, restore=0.7` grown geometry that the leaf depends on; the
recorded auditor "Repair target" in Audit 3 explicitly names "one-hop
retained authorities for the grown row and exact-lattice carryover"
as the requirement. Per hard rule 1, that retained derivation must
itself proceed from `claim_type + audited_clean + retained-grade
dependencies`. This is a substantial open theorem in its own right —
not a small bounded source note in the style of recent audit-backlog
cycles per
[`docs/AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md`](AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md).

Path 2 requires inlining the runner-defined grown-graph construction
(currently sourced from `scripts.gate_b_grown_joint_package.grow`) plus
a closure proof from `Cl(3)` on `Z^3` per the framework's minimal
axioms (see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)).
The geometry is a parameterised growth model, not a single-identity
construction; reproducing it inline with closure proof is comparable in
scope to landing the upstream `gate_b_grown_joint_package_note` itself
as a retained theorem. It is not a single-identity bounded source note.

Either path is substantial open derivation work, not a small bounded
edit. Both paths are open theorems whose scope exceeds the
audit-backlog campaign's bounded-note repair surface.

## Status

```yaml
claim_type: meta
proposal_allowed: false
proposal_allowed_reason: |
  This note is a backward-looking synthesis citing already-applied
  audit verdicts. It does not propose any new derivation, theorem,
  or admission. It only records the structural block on the leaf
  imposed by the recorded `audited_conditional` verdicts on
  `claude_complex_action_grown_companion_note` and the
  `missing_dependency_edge` repair class flagged by the most recent
  fresh-context auditor. It is not a new derivation. The audit lane
  remains the sole authority for changing any row's `audit_status`
  or `effective_status`.
authority_chain:
  - claude_complex_action_grown_companion_note (audited_conditional
    twice on independent fresh-context audits, most recent
    auditor=codex-gpt-5.5 with auditor_confidence=high; both
    verdicts localise the block to the same imported-premise gate)
  - gate_b_grown_joint_package_note (unaudited; not retained-grade;
    the leaf's runner imports `grow` from this module's
    `scripts/gate_b_grown_joint_package.py` per the runner source)
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## What this note does NOT do

1. Promote any audit row to retained, bounded, or closed.
2. Reclassify the recorded `audited_conditional` verdicts on the leaf
   (Audits 3 and 4) or the prior-cycle `audited_clean` legacy backfill
   (Audit 2, already invalidated and re-audited under the corrected
   criticality-bump policy).
3. Modify the leaf's text, the runner's source, or the upstream
   imported module.
4. Add a new axiom or new bounded theorem.
5. Introduce new vocabulary, new tags, new claim types, or new
   framings on this dep chain. Repo-canonical language only
   (`missing_dependency_edge`, `audited_conditional`,
   `retained-grade dependencies`, `imported premise`).
6. Propose a derivation or repair theorem for the upstream
   `gate_b_grown_joint_package_note`. (No new derivation is proposed;
   the synthesis is purely a citation of existing recorded verdicts.)
7. Override the audit lane's recorded `effective_status` or
   `effective_status_reason` for any row.

## Recommendation for future campaigns

Concrete operational recommendation for automated audit-backlog
campaigns and retained-promotion campaigns:

1. **Do not** spawn audit-backlog campaign cycles attempting to close
   `claude_complex_action_grown_companion_note` until either (a) the
   upstream `gate_b_grown_joint_package_note` is registered as a
   one-hop dep edge AND has reached `audited_clean` with retained-grade
   dependencies of its own, or (b) the runner-defined grown geometry
   is inlined into the leaf's source note with a closure proof.
   The leaf's current `unaudited` status reflects note-hash-drift
   re-seeding, not a new repair surface.
2. **Do not** spawn retained-promotion campaign attempts on the
   leaf itself while the load-bearing grown geometry remains an
   imported premise. The two independent `audited_conditional`
   verdicts converge on the same `missing_dependency_edge` block
   (Audit 4 uses that exact repair-class label); per
   [`docs/audit/README.md`](audit/README.md) hard rules 1-2, the only
   legitimate path is structural repair of the imported-premise gate,
   not numerical-replay re-attempts.
3. **Do not** spawn audit-backlog campaign cycles attempting to close
   `gate_b_grown_joint_package_note` standalone as a small bounded
   note. The upstream module implements a parameterised grown-graph
   construction whose retained closure must itself proceed from
   `claim_type + audited_clean + retained-grade dependencies` per
   hard rule 1; landing that as `audited_clean` is a substantial open
   theorem in its own right, not a bounded source-note edit.
4. **Do not** introduce new vocabulary, new tags, new claim_types, or
   new framings on this dep chain. The audit lane's existing language
   (`missing_dependency_edge`, `imported premise`, `audited_conditional`,
   `retained-grade dependencies`) is sufficient and is the only
   language that should be used in further synthesis or repair work.
5. The cheapest unblocking action, if one is to be undertaken at all,
   is the open retained derivation of the runner-defined grown row at
   `drift=0.2, restore=0.7` named in the auditor's recorded
   `notes_for_re_audit_if_any`. That work belongs in its own
   retained-theorem landing path on the upstream
   `gate_b_grown_joint_package_note`, not in audit-backlog or
   retained-promotion campaign cycles on the leaf.

## Cross-references

- Audit-lane policy: [`docs/audit/README.md`](audit/README.md)
  (terminal verdicts at lines 87-88; hard rules 1-2 at lines 106-113;
  `missing_dependency_edge` repair class at lines 192-193)
- Sibling terminal-block syntheses:
  [`QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md`](QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md)
  (PR #959),
  [`DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md)
  (PR #960)
- Synthesis-template authority:
  [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- Leaf source note:
  [`CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)
- Leaf runner source:
  [`scripts/complex_action_grown_companion.py`](../scripts/complex_action_grown_companion.py)
- Imported-premise module source:
  [`scripts/gate_b_grown_joint_package.py`](../scripts/gate_b_grown_joint_package.py)
- Audit ledger row data:
  [`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json)
- Campaign-level synthesis template:
  [`AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md`](AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md)
- Audit-lane policy fixes preceding this note: PR #907 (criticality-bump
  policy fix), PR #925 (one-shot restoration of over-aggressively
  invalidated audits)

## Validation

```bash
python3 scripts/frontier_claude_complex_action_grown_companion_terminal_synthesis.py
```

Runner verifies, against the live
[`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json):

1. The leaf row `claude_complex_action_grown_companion_note` exists
   with `criticality=critical`, and its `runner_path` matches what
   this synthesis cites
   (`scripts/complex_action_grown_companion.py`).
2. The leaf's `deps[]` array does **not** contain
   `gate_b_grown_joint_package_note` (PASS — confirms the
   `missing_dependency_edge` block still applies; FAIL means the dep
   edge has been added and this synthesis is stale).
3. The leaf's `previous_audits[]` contains at least one
   `audited_conditional` verdict whose
   `chain_closure_explanation` cites the imported-premise issue
   (PASS — confirms the recorded structural block).
4. The synthesis itself is `claim_type=meta` and does not declare a
   pipeline `effective_status`.

If any of the cited verdicts changes (for example, a new audit
re-review, a dep-edge addition, or a new note version), the runner
flags the synthesis as stale (`FAIL`) and the synthesis must be
re-audited. PASS=N FAIL=0 indicates the synthesis is consistent with
the current ledger.

## Review-loop rule

Going forward:

1. The structural block on this critical leaf is **terminal pending
   either retained derivation of the upstream
   `gate_b_grown_joint_package_note` or inlined-with-closure-proof
   replacement of the imported grown geometry**. New audit-backlog or
   retained-promotion campaign sub-cycles targeting this leaf or its
   imported-premise upstream must explicitly cite a new bounded or
   retained theorem that addresses the auditor's recorded
   `missing_dependency_edge` repair class for the specific upstream
   module being attacked, not numerical-replay re-attempts on the
   leaf.
2. If the upstream `gate_b_grown_joint_package_note` is later audited
   to `audited_clean` with retained-grade dependencies, this synthesis
   becomes stale and the runner will FAIL — that signals a
   re-evaluation is in order.
3. The two independent fresh-context `audited_conditional` verdicts
   (`codex-gpt-5` Audit 3 and `codex-gpt-5.5` Audit 4) remain the
   authoritative repo-internal record of why the leaf is
   chain-non-closing on the current dep chain and why a retained-grade
   promotion is structurally blocked while the imported-premise gate
   stands.
