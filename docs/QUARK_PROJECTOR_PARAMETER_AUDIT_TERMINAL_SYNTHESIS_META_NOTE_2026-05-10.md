# Quark Projector Parameter Audit Terminal Synthesis Meta Note

**Date:** 2026-05-10
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal; pipeline-derived status set only after independent audit
review.
**Authority role:** records the structural block on the critical leaf
[`quark_projector_parameter_audit_note_2026-04-19`](QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md):
its dep chain terminates at an `audited_numerical_match` upstream verdict
that cannot repair as a small bounded source note. Documents the finding
so future automated audit-backlog or retained-promotion campaigns do not
spend cycles attempting to close this leaf.
**Companion to:**
- [`docs/audit/README.md`](audit/README.md) (audit-lane policy: definition-as-derivation, terminal verdicts)
- [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md) (sibling terminal-block synthesis template)
**Primary runner:** [`scripts/frontier_quark_projector_parameter_audit_terminal_synthesis.py`](../scripts/frontier_quark_projector_parameter_audit_terminal_synthesis.py)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim. This note
records what the existing audit verdicts already establish about the
projector-parameter-audit dep chain; it does not promote theorems,
modify retained content, reclassify any audit row, or propose a new
derivation. It is a backward-looking synthesis citing already-applied
audit verdicts as the authority.

## Naming

Throughout this note:
- **"the leaf"** = [`docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`](QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md) — claim_id `quark_projector_parameter_audit_note_2026-04-19`
- **"the projector ray dep"** = [`docs/QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md`](QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md) — claim_id `quark_projector_ray_phase_completion_note_2026-04-18`
- **"the carrier-completion dep"** = [`docs/QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md`](QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md) — claim_id `quark_cp_carrier_completion_note_2026-04-18`
- **"terminal verdict"** = an `audited_*` verdict that is not `audited_clean` and that the audit lane records as terminal (`audited_numerical_match`, `audited_renaming`, `audited_failed`, `audited_decoration`); per [`docs/audit/README.md`](audit/README.md) lines 87-88, terminal non-clean verdicts on active claims block retained propagation.
- **"definition-as-derivation"** = the audit-lane failure mode named in [`docs/audit/README.md`](audit/README.md) where a symbol is defined via a numerical fit against external comparators and then re-presented as if derived; one of the four failure modes the audit lane was built to detect.

## Leaf claim under review

`quark_projector_parameter_audit_note_2026-04-19` — current ledger row:

- `claim_type`: `bounded_theorem`
- `audit_status`: `unaudited` (current row, after criticality-bump invalidation that re-seeded a prior `audited_conditional` verdict per [PR #907 / #925 lane](audit/data/audit_ledger.json) — see `previous_audits[]` invalidation_reason `criticality_increased:high->critical`)
- `criticality`: `critical`
- `transitive_descendants`: 379
- `direct_in_degree`: 20
- `load_bearing_score`: 18.57
- `deps`: [`quark_projector_ray_phase_completion_note_2026-04-18`, `quark_cp_carrier_completion_note_2026-04-18`]

The leaf is one of the highest-fan-in audit-pending rows on the quark
lane and has been re-seeded `unaudited` after the audit-lane criticality
bump from `high` to `critical`.

## Terminal upstream verdict

The leaf's two non-retained blocking deps:

### 1. `quark_projector_ray_phase_completion_note_2026-04-18`

- `claim_type`: `bounded_theorem`
- `audit_status`: `unaudited`
- `criticality`: `critical`
- `deps`: [`quark_cp_carrier_completion_note_2026-04-18`] (single dep — itself routes through the carrier-completion dep below)

The projector-ray-and-phase completion is itself unaudited, but its only
upstream is the carrier-completion dep. Any closure path through this
node necessarily inherits the carrier dep's verdict.

### 2. `quark_cp_carrier_completion_note_2026-04-18` — TERMINAL

- `claim_type`: `bounded_theorem`
- `audit_status`: `audited_numerical_match` (terminal non-clean)
- `effective_status`: `audited_numerical_match`
- `effective_status_reason`: `terminal_audit`
- `cross_confirmation.status`: `confirmed` (independent fresh-context auditors `codex-gpt-5.5-backlog-sweep-2026-04-29` + `codex-fresh-context-20260430-08-quark-cp` agreed on the verdict in cross-family review)
- `auditor_confidence`: `high`

Auditor rationale (verbatim from the recorded `verdict_rationale`):

> "Issue: The claimed completion is produced by solving large free
> complex carriers `xi_u` and `xi_d` against the CKM/mass-ratio target
> surface. Why this blocks: The runner verifies a tuned numerical match
> on an expanded ansatz, but the carriers are solved rather than derived
> and are not perturbative; the chain does not establish retained
> physical closure. Repair target: Provide an independent derivation or
> retained upstream theorem fixing `xi_u` and `xi_d`, including carrier
> normalization/readout and determinant-neutral constraint, then have
> the runner test that derived point rather than fit it. Claim boundary
> until fixed: Bounded numerical support that such an extended carrier
> surface can fit the listed targets."

Magnitudes recorded in the carrier-completion note itself
([`docs/QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md`](QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md) lines 75-80):

```
xi_u = +0.340735 - 0.063203 i
xi_d = +0.078186 + 0.108371 i
|xi_u| / c13_u(base) ~ 101.9
|xi_d| / c13_d(base) ~ 6.64
```

The carriers dominate the bare Schur 1-3 term in the up sector by two
orders of magnitude — they are large free fitted complex coefficients,
not small perturbative completions.

### Judicial third audit (2026-04-30)

The leaf row itself was previously the subject of a judicial third-pass
audit (recorded under `cross_confirmation.mode = judicial_third_pass`,
`status = third_confirmed_second`). The judge `codex-judge-20260430-phase-b-quark-param`
sided with the second auditor's `audited_conditional` verdict against
the first auditor's `audited_numerical_match` verdict, with the
following recorded rationale:

> "The second auditor's reading holds because the row depends on
> bounded upstream projector/carrier notes and cross-note exact-support
> inputs, while the up-sector amplitude remains solved rather than
> derived. The first numerical-match verdict missed the unresolved
> dependency/status boundary."

The judicial review explicitly localized the structural block to the
upstream carrier-completion dep, which was subsequently itself audited
to `audited_numerical_match` (terminal) by independent fresh-context
auditors. The judicial audit is the strongest available repo-internal
authority on this leaf's dep-chain status.

## Repair surface analysis

The leaf cannot be retained while
`quark_cp_carrier_completion_note_2026-04-18` carries the terminal
verdict `audited_numerical_match`. Per [`docs/audit/README.md`](audit/README.md)
hard rule 1 ("Retained grade is audit-only ... only from `claim_type +
audited_clean + retained-grade dependencies`") and hard rule 2 ("Open
gates block propagation ... terminal non-clean audit verdicts are not
retained-grade dependencies"), the chain cannot promote without:

1. Either repairing the upstream carrier-completion dep — which requires
   an independent first-principles derivation of `xi_u`, `xi_d`
   including carrier normalization, readout, and determinant-neutral
   constraint, with the runner testing that derived point rather than
   fitting it (the auditor's recorded "Repair target");
2. Or rerouting the leaf's load-bearing step around the carrier
   completion entirely.

### Why option 1 is not a small bounded source note

The recorded auditor "Repair target" describes a substantial open
derivation: a retained upstream theorem fixing two complex carrier
coefficients with their normalization, readout convention, and
determinant-neutral constraint, where the resulting carriers must
reproduce the empirical CKM target surface without numerical fitting.
The `|xi_u| / c13_u(base) ~ 101.9` magnitude rules out a small
perturbative correction theorem; the up-sector carrier alone is two
orders of magnitude larger than the bare Schur term, so any retained
derivation must produce that magnitude from first principles, not
absorb it as a leading-order correction.

This is the classic definition-as-derivation failure mode the audit
lane was built to detect (see [`docs/audit/README.md`](audit/README.md)
"What this lane does", failure mode 1: "a new symbol is defined as a
small-integer ratio, then 'shown' to match data by name substitution"
— here generalized to "a complex carrier is defined by numerical
optimization against external comparators, then 'shown' to close the
target surface").

A repair landing as a narrow bounded source note in the style of recent
audit-backlog cycles (campaign-style 1-identity-at-a-time bounded notes
per [`docs/AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md`](AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md))
is structurally insufficient: the carriers are not parameterized
by a single small-integer ratio, and the empirical target surface is
not a single observable. The retained derivation must be a positive
theorem of comparable scope to e.g. the staggered-Dirac realization gate
or the SU(3) ladder closure, not a one-identity bounded note.

### Why option 2 is not available

The leaf's deps in the ledger are exactly:

```
deps = [
  quark_projector_ray_phase_completion_note_2026-04-18,
  quark_cp_carrier_completion_note_2026-04-18,
]
```

The projector-ray dep itself routes through the carrier-completion dep
(its `deps = [quark_cp_carrier_completion_note_2026-04-18]`). There is
no alternative dep listed in the leaf or its single direct upstream
that bypasses the carrier completion. Any rerouting would require
adding a new dep edge — i.e., wiring an as-yet-unwritten retained
theorem into the leaf's chain — which is identical in scope to option 1.

## Status

```yaml
claim_type: meta
proposal_allowed: false
proposal_allowed_reason: |
  This note is a backward-looking synthesis citing already-applied
  audit verdicts. It does not propose any new derivation, theorem,
  or admission. It only records the structural block on the leaf
  imposed by the terminal `audited_numerical_match` verdict on
  `quark_cp_carrier_completion_note_2026-04-18`. The audit lane
  remains the sole authority for changing any row's `audit_status`
  or `effective_status`.
authority_chain:
  - quark_cp_carrier_completion_note_2026-04-18 (audited_numerical_match,
    terminal, cross-confirmed by two independent fresh-context auditors)
  - quark_projector_parameter_audit_note_2026-04-19 (judicial third
    audit confirmed audited_conditional against audited_numerical_match)
expected_seed:
  audit_status: unaudited
  claim_type: meta
  effective_status: unaudited
```

## What this note does NOT do

1. Promote any row to retained.
2. Demote `quark_cp_carrier_completion_note_2026-04-18` from its
   recorded `audited_numerical_match` verdict.
3. Reclassify the leaf or its deps.
4. Propose a new theorem, derivation, or carrier-completion mechanism.
5. Rename, retag, or introduce new vocabulary for the dep chain.
6. Modify any retained content.
7. Open or close any audit row.

## Recommendation for future campaigns

Concrete operational recommendation for automated audit-backlog
campaigns and retained-promotion campaigns:

1. **Do not** spawn audit-backlog campaign cycles attempting to close
   `quark_projector_parameter_audit_note_2026-04-19` until the upstream
   `xi_u`, `xi_d` carrier-derivation gap lands as a separate retained
   theorem. The leaf's current `unaudited` status reflects criticality-
   bump-driven re-seeding, not a new repair surface.
2. **Do not** spawn retained-promotion campaign attempts on the
   carrier-completion dep `quark_cp_carrier_completion_note_2026-04-18`
   itself. Its `audited_numerical_match` verdict is cross-confirmed by
   two independent fresh-context auditors and the `effective_status`
   is recorded as `terminal_audit`. Per [`docs/audit/README.md`](audit/README.md)
   the only legitimate path is an independent retained derivation of
   `xi_u`, `xi_d` shipped as a separate positive theorem; once that
   theorem is `audited_clean` and retained, the carrier-completion
   chain may be revisited via re-audit.
3. **Do not** spawn audit-backlog campaign cycles attempting to close
   `quark_projector_ray_phase_completion_note_2026-04-18` standalone.
   Its only dep is the terminal-verdict carrier-completion dep, so
   any closure attempt that does not first repair the upstream is
   structurally blocked.
4. **Do not** introduce new vocabulary, new tags, new claim_types, or
   new framings on this dep chain. The audit lane's existing language
   for terminal verdicts (`audited_numerical_match`, `terminal_audit`,
   `definition-as-derivation`) is sufficient and is the only language
   that should be used in further synthesis or repair work.
5. The cheapest unblocking action, if one is to be undertaken at all,
   is the open carrier-derivation theorem named in the auditor's
   recorded `Repair target`. That work belongs in its own retained-
   theorem PR, not in audit-backlog or retained-promotion campaign
   cycles on this leaf.

## Cross-references

- Audit-lane policy: [`docs/audit/README.md`](audit/README.md) (terminal verdicts at lines 87-88; hard rules 1-2; definition-as-derivation failure mode in "What this lane does")
- Sibling terminal-block synthesis: [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- Leaf source note: [`docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`](QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
- Projector-ray dep source note: [`docs/QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md`](QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md)
- Carrier-completion dep source note: [`docs/QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md`](QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md)
- Audit ledger row data: [`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json)
- Sibling synthesis-template authority: [`docs/AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md`](AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md)

## Validation

```bash
python3 scripts/frontier_quark_projector_parameter_audit_terminal_synthesis.py
```

Runner verifies (against the live audit ledger):

1. `quark_cp_carrier_completion_note_2026-04-18` carries
   `audit_status == "audited_numerical_match"` (PASS — the synthesis
   is current). If the verdict has changed, the runner FAILs and the
   synthesis is stale and needs re-audit.
2. `quark_projector_ray_phase_completion_note_2026-04-18` exists in
   the ledger.
3. `quark_projector_parameter_audit_note_2026-04-19` exists in the
   ledger and lists both expected blocking deps.
4. This note is `claim_type = meta` and does not declare pipeline
   status.

## Review-loop rule

Going forward:

1. The dep-chain block on
   `quark_projector_parameter_audit_note_2026-04-19` is **terminal
   pending an open retained derivation of `xi_u`, `xi_d`**. New
   audit-backlog or retained-promotion campaign cycles on this leaf
   or its deps must not be spawned until that derivation lands as
   a separate retained theorem.
2. If the upstream `audited_numerical_match` verdict is revisited
   via re-audit at a later date, this synthesis becomes stale and
   the runner will FAIL — that signals a re-evaluation is in order.
3. The judicial third audit on the leaf
   (`codex-judge-20260430-phase-b-quark-param`) remains the
   authoritative repo-internal record of why the leaf is
   `audited_conditional`-equivalent on its bounded-theorem scope and
   why a retained-grade promotion is structurally blocked on the
   current dep chain.
