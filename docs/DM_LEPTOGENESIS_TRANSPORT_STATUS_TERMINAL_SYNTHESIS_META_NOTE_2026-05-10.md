# DM Leptogenesis Transport Status Terminal Synthesis Meta Note

**Date:** 2026-05-10
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal; pipeline-derived status set only after independent audit
review.
**Authority role:** records the structural block on the critical leaf
[`DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md):
several of its load-bearing one-hop authorities now carry the audit
lane's `terminal_audit` flag (`audited_renaming`,
`audited_numerical_match`, and a `terminal_audit`-tagged
`audited_conditional` cluster). The leaf's own statement makes all
linked authorities load-bearing, so the chain cannot retain until those
upstream verdicts are independently re-derived.
**Companion to:**
- [`DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md)
  (the leaf this note synthesises around)
- [`AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md`](AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md)
  (campaign-level synthesis template)
- [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
  (parallel terminal-synthesis template)
**Primary runner:** [`scripts/frontier_dm_leptogenesis_transport_status_terminal_synthesis.py`](../scripts/frontier_dm_leptogenesis_transport_status_terminal_synthesis.py)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim. This note is
backward-looking: it cites already-recorded upstream audit verdicts in
[`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json) and
synthesises the structural consequence for the leaf. It does not
promote theorems, does not modify retained content, does not propose
new derivations, and does not reclassify any audit row. No new
vocabulary, claim type, or framing is introduced. All terminal-verdict
language used here (`audited_renaming`, `audited_numerical_match`,
`audited_conditional`, `terminal_audit`) is repo-canonical and matches
the audit lane's existing field values.

## Context

After PR #907 fixed the audit-lane criticality-bump policy and PR #925
restored audits over-aggressively invalidated pre-#907, a small cluster
of critical leaves was identified whose dep chains carry terminal
verdicts that cannot repair as bounded source notes. This note is the
second of two backward-looking syntheses documenting that finding so
future automated campaigns do not spend cycles attempting to close
these leaves through audit-backlog or retained-promotion routes. The
first synthesis covers the quark projector chain and lands in a
separate PR; this note covers the DM leptogenesis transport status
chain.

## Leaf claim under review

[`DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md)

| Field | Value |
|---|---|
| `claim_id` | `dm_leptogenesis_transport_status_note_2026-04-16` |
| `criticality` | `critical` |
| `transitive_descendants` | 351 (current ledger) |
| `load_bearing_score` | 15.959 |
| `direct_in_degree` | 15 |
| One-hop load-bearing deps | 8 (per the leaf's own "Citations" section) |
| `effective_status` | `unaudited` (`awaiting_audit`) |

The leaf's load-bearing statement (final paragraph of the leaf):

> Until each linked authority is retained by the independent audit
> lane, the registered edges make the chain traceable but do not
> promote this status note.

That is, all eight upstream authorities are load-bearing. The leaf is
a status inventory, not a constructive theorem with rerouting
alternatives.

## Terminal upstream verdicts

Of the eight one-hop deps registered by the leaf, **five carry the
audit lane's `terminal_audit` flag** as their
`effective_status_reason` in [`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json).
None of the five repairs as a bounded source note: each requires a new
axiom-level derivation (substantial open theorem work), per the audit
lane's own `notes_for_re_audit_if_any` text.

| # | Upstream dep | `audit_status` | Auditor's repair note |
|---|---|---|---|
| 1 | [`DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md) | `audited_renaming` | "Re-check only if a future packet includes an explicit axiom-level derivation or executable construction of `kappa_axiom[H]` rather than imported constants and True checks." |
| 2 | [`DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md) | `audited_numerical_match` | "Re-check with the source of `dm_leptogenesis_exact_common` and a retained derivation of `K_H`, `E_H(z)`, transport equations, boundary conditions, and normalizations from `Cl(3)` on `Z^3`." |
| 3 | [`DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md) | `audited_numerical_match` | "Re-check whether a later runner derives `canonical_h` / `D_-` directly from `Cl(3)` on `Z^3` instead of constructing a block with the desired Schur complement." |
| 4 | [`DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md) | `audited_conditional` (`terminal_audit`) | "Provide the retained Poisson/Newton-to-flat-Friedmann authority and the exact radiation-density / `g_*` normalization source, plus the `dm_leptogenesis_exact_common` implementation, then re-audit the full closure." |
| 5 | [`DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md) | `audited_conditional` (`terminal_audit`) | "Provide a retained authority or self-contained runner deriving the 28 bosonic and 90 fermionic relativistic degrees of freedom from `Cl(3)` on `Z^3` rather than hard-coding or importing them." |

The remaining three deps (`dm_leptogenesis_exact_kernel_closure_note_2026-04-15`,
`dm_leptogenesis_ne_projected_source_law_derivation_note_2026-04-16`,
`dm_leptogenesis_ne_projected_source_triplet_sign_theorem_note_2026-04-16`)
are currently `unaudited` (`awaiting_audit`) on the live ledger; they
do not contribute to the terminal-block surface analysed here, and
they are in principle repairable through standard audit review.

## Repair surface analysis

With five of eight load-bearing deps tagged `terminal_audit`, no
single-action win exists for this leaf. Per the leaf's own statement,
all linked authorities must be retained before the leaf itself can
promote — and the chain has no rerouting clause, so cutting one
terminal upstream is not enough.

To repair, every one of the five terminal upstreams would need an
independent axiom-level re-derivation, each of which is open theorem
work per the audit lane's recorded repair notes. Specifically:

- `kappa_axiom[H]` must be constructively derived from `Cl(3)` on
  `Z^3`, not introduced as a name (rows 1, 4).
- `K_H`, `E_H(z)`, transport equations, boundary conditions, and
  normalizations must be derived from the framework axiom rather than
  imported as constants from `dm_leptogenesis_exact_common` (rows 2,
  4).
- `canonical_h` and `D_-` must be derived from `Cl(3)` on `Z^3`
  rather than constructed to produce the target Schur complement
  numerically (row 3).
- The 28 bosonic and 90 fermionic relativistic degree-of-freedom
  counts must be derived from `Cl(3)` on `Z^3` rather than imported
  (row 5).

Each of these is a substantial open theorem in its own right. Until
they exist, the leaf's 351 transitive descendants remain in an
upstream-blocked state on this critical chain, and the cost
amortised over the descendant subgraph yields poor cost-per-node-fixed
for any campaign that targets the leaf directly.

## Status

```yaml
actual_current_surface_status: terminal-upstream synthesis (backward-looking)
proposal_allowed: false
proposal_allowed_reason: |
  This is a backward-looking synthesis citing already-recorded audit
  verdicts; it is not a new derivation. The leaf's pipeline status
  remains exactly what the independent audit lane has assigned:
  `unaudited`/`awaiting_audit` for the leaf itself, and the
  upstream-recorded `audited_renaming`,
  `audited_numerical_match`, and `audited_conditional` (with
  `terminal_audit` reason) verdicts for the five terminal-flagged
  deps. This synthesis does not promote, demote, or reclassify any of
  those rows.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Recommendation for future campaigns

Going forward, the audit-backlog campaign and retained-promotion
campaign frameworks should not allocate cycles to:

1. The leaf
   [`DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md)
   itself; or
2. Any of the five terminal-flagged upstream deps listed in the table
   above,

unless and until at least one of the five terminal upstreams has been
independently re-derived by new bounded or retained content that
addresses the auditor's recorded repair note for that specific row.

Concretely:

- Do **not** open audit-backlog campaign sub-cycles whose target is
  this leaf or any terminal-flagged upstream listed above.
- Do **not** open retained-promotion campaign attempts on this leaf.
- Do **not** treat the 351 transitive descendants of this leaf as a
  cost-justification for re-attacking the chain at the leaf level; the
  cost-per-node-fixed is dominated by the five upstream theorem
  re-derivations, not by leaf-level rework.
- Do **not** introduce new vocabulary, new claim types, or new framing
  to circumvent the recorded `terminal_audit` verdicts; per the
  repo-vocabulary policy, such attempts have been rejected even when
  the per-claim work is correct.

Legitimate future paths:

- A separate, narrowly scoped bounded theorem note that derives one of
  the five blocked objects (for example, an axiom-level construction
  of `kappa_axiom[H]`, or a derivation of `g_*=28+90` counts from
  `Cl(3)` on `Z^3`) — opened in its own PR, audited on its own
  authority, and only afterwards considered as a repair candidate for
  the corresponding terminal upstream.
- Independent audit-lane re-review of the two `audited_conditional`
  rows (`hrad_theorem`, `equilibrium_conversion_theorem`) if their
  underlying notes are themselves modified to address the recorded
  conditional repair targets; such re-reviews are the audit lane's
  prerogative, not this synthesis's.

## What this note does NOT do

1. Promote any audit row to retained, bounded, or closed.
2. Re-classify any of the five terminal-flagged upstream verdicts.
3. Modify the leaf or any upstream note's text or runner.
4. Add a new axiom or new bounded theorem.
5. Introduce new vocabulary, new claim types, or new framing.
6. Propose a derivation. (No new derivation is proposed; the synthesis
   is purely a citation of existing recorded verdicts.)
7. Override the audit lane's recorded `effective_status` or
   `effective_status_reason` for any row.

## Cross-references

- The leaf:
  [`DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md)
- The five terminal-flagged upstreams (live verdicts in
  [`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json)):
  [`DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md),
  [`DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md),
  [`DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md),
  [`DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_HRAD_THEOREM_NOTE_2026-04-16.md),
  [`DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_EQUILIBRIUM_CONVERSION_THEOREM_NOTE_2026-04-16.md)
- Synthesis template / parallel campaign:
  [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- Campaign-level synthesis template:
  [`AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md`](AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md)
- Audit-lane policy fix preceding this note: PR #907
  (criticality-bump policy fix), PR #925 (one-shot restoration of
  over-aggressively invalidated audits)

## Validation

```bash
python3 scripts/frontier_dm_leptogenesis_transport_status_terminal_synthesis.py
```

Runner verifies, against the live
[`docs/audit/data/audit_ledger.json`](audit/data/audit_ledger.json):

1. The leaf
   `dm_leptogenesis_transport_status_note_2026-04-16` is registered
   with `criticality=critical`.
2. The leaf has the eight one-hop deps named in the leaf's own
   "Citations" section.
3. Each of the five terminal-flagged upstreams has the
   `audit_status` and `effective_status_reason` claimed by this
   synthesis.
4. The synthesis itself is `claim_type=meta` and does not declare a
   pipeline `effective_status`.

If any of the five upstream verdicts changes (for example, a new
audit re-review or a new note version), the runner flags the synthesis
as stale (`FAIL`) and the synthesis must be re-audited. PASS=N FAIL=0
indicates the synthesis is consistent with the current ledger.

## Review-loop rule

Going forward:

1. The structural block on this critical leaf is **terminal at the
   audit-lane recorded layer**: five of eight one-hop deps carry
   `terminal_audit` reasons. Repair requires per-row axiom-level
   re-derivation, which is open theorem work outside the scope of
   audit-backlog or retained-promotion campaigns.
2. New audit-backlog or retained-promotion sub-cycles targeting this
   leaf or any terminal-flagged upstream must explicitly cite a new
   bounded or retained theorem that addresses the auditor's recorded
   repair note for the specific upstream row being attacked.
3. This synthesis does not select among repair paths; the audit lane
   has authority over which (if any) repair candidate retains a
   terminal upstream.
