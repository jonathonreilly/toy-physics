# Audit Low-Hanging-Fruit Leverage Map for Retained Promotion

**Date:** 2026-05-01
**Status:** support / audit-cohort assessment. This note is a navigation
artifact for the audit lane: it ranks the highest-leverage critical/high
audit blockers on `main` and assesses whether the unblocking work is
"low-hanging fruit" (small fix) or substantive science work.
**Lane:** audit-hygiene + audit-strategy. No physics claim is added or
removed.

---

## 0. Why this note exists

The campaign goal stated by the user was: *"review the critical audit rows
that we need to get to retained status for any low hanging fruit - if you
find it, fix it, make a PR."*

This note documents the answer: there are **two distinct cohorts** mixed in
the audit ledger, and they need different treatment.

- **Cohort A (genuinely low-hanging fruit, mechanically fixable):**
  runner-side stale-path bugs — runners that fail because they
  `read("docs/X.md")` for files deleted/moved by recent trim commits. Not
  load-bearing physics issues.
- **Cohort B (load-bearing audit objections, real science work):**
  critical/high `proposed_retained` rows whose audit verdicts identify
  genuine load-bearing dependencies on unratified upstream notes. These
  are not LHF; they are the lane's actual research frontier.

Cohort A was addressed by the campaign in PRs **#246** (Block 1) and
**#247** (Block 2). This note documents Cohort B as a leverage map for the
user/auditor to plan substantive science work.

## 1. Cohort A — runner-side stale-path bugs (FIXED)

The audit pipeline runs each runner in a restricted environment. When a
runner contains `read("docs/X.md")` and `X.md` no longer exists at that
path (was deleted or relocated by a trim commit), the runner raises
`FileNotFoundError` and the audit verdict lands as
`audited_conditional` / `audited_failed` with rationale "primary runner
returned nonzero in the restricted audit environment".

This is **not** a physics audit failure. It is a runner-hygiene bug.

The campaign's comprehensive scan (`grep -E 'read\("docs/[^"]+"\)' scripts/`)
found 16 such runners. All 16 are now addressed:

- PR #246 — 8 runners, 69 PASS / 0 FAIL after fix.
- PR #247 — 8 more runners, 89 PASS / 0 FAIL after fix.

After both PRs land and the audit pipeline re-runs, the affected rows
should re-audit on substantive physics merits rather than file-availability
noise. Most are leaf-criticality with author-declared `support` /
`bounded`; clearing the noise floor does NOT promote any of them to
retained.

## 2. Cohort B — critical/high audit blockers requiring science work

For each of the 76 retained rows on `main`, there are downstream audit
rows that depend on it. Many `proposed_retained` rows in the
critical/high tier are blocked by audit-conditional verdicts whose
rationale text identifies a *specific* unratified upstream authority.
These verdicts cannot be cleared by runner edits — the upstream chain
must close first.

Below is the leverage map sorted by **total transitive-descendant count**
(i.e., how many downstream rows would clean up if the named root was
unblocked). All counts are from the 2026-05-01T16:39Z audit-ledger
generation.

### 2.1 Top 8 root blockers by downstream impact

| rank | root claim_id | downstream proposed_retained crit/high | total transitive descendants | named blocking deps in `open_dependency_paths` |
|---|---|---:|---:|---|
| 1 | `minimal_axioms_2026-04-11` | 9 | **1010** | G_BARE_* family (6 notes): structural normalization, rigidity, two-Ward closure, two-Ward rep_B independence, same-1PI pinning, dynamical fixation obstruction |
| 2 | `neutrino_majorana_operator_axiom_first_note` | 5 | **733** | ANOMALY_FORCES_TIME_THEOREM, frontier_right_handed_sector.py, MINIMAL_AXIOM_INVENTORY, UNIFIED_AXIOM_BOUNDARY_NOTE |
| 3 | `left_handed_charge_matching_note` | 5 | **488** | (self-conditional: hypercharge formula `Q = T_3 + Y/2` not yet structurally derived) |
| 4 | `three_generation_structure_note` | 4 | **478** | THREE_GENERATION_OBSERVABLE_THEOREM_NOTE, PHYSICAL_LATTICE_NECESSITY_NOTE |
| 5 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | 6 | **455** | NATIVE_GAUGE_CLOSURE_NOTE, ALPHA_S_DERIVED_NOTE, ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24 |
| 6 | `gauge_vacuum_plaquette_bridge_support_note` | 4 | **434** | GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE, SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE, GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE, ...TENSOR_TRANSFER_PERRON_SOLVE_NOTE |
| 7 | `yt_ew_color_projection_theorem` | 4 | **385** | RCONN_DERIVED_NOTE, EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27, **circular dependency**: yt_ew_color_projection_theorem ↔ rconn_derived_note ↔ ew_current_matching... |
| 8 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | 8 | **371** | CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE, ALPHA_S_DERIVED_NOTE, WOLFENSTEIN_LAMBDA_A_..., CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE |

### 2.2 Why these are NOT LHF

For each of the top 8 roots, the audit verdict text says the load-bearing
step "still imports unratified direct authority" or "does not derive ...
as axiom-side outputs". These objections cannot be cleared by surface
edits or runner fixes. They require:

- (R1) Finishing the upstream derivation that the audit calls out.
  Example: `minimal_axioms_2026-04-11` waits on the **G_bare structural
  normalization theorem family** — six notes that propose to fix
  `g_bare = 1` from canonical normalization but currently rely on
  rigidity / two-Ward closure / same-1PI pinning that are themselves
  unratified.
- (R2) Resolving a circular dependency. Example:
  `yt_ew_color_projection_theorem` ↔ `rconn_derived_note` ↔
  `ew_current_matching_ozi_suppression_theorem_note_2026-04-27` form a
  3-cycle. None can ratify until the cycle is broken by an external
  retained authority OR one node is reduced to a self-contained
  derivation.
- (R3) Adding a missing direct computation that a downstream chain quotes
  but that no upstream note actually performs. Example:
  `yt_ew_color_projection_theorem` audit explicitly calls for "missing
  direct EW-current matching coefficient computation".

None of these is a one-PR fix. Each is at minimum a cycle of theoretical
work plus a fresh-context audit pass.

### 2.3 Highest-leverage candidates by audit-friendly criteria

If a future campaign wants to make actual "retained promotion" progress,
the prioritization criteria are (in order):

1. **Cycle-breaking edges first.** The
   `yt_ew_color_projection ↔ rconn_derived ↔ ew_current_matching` 3-cycle
   blocks 385+ descendants. Breaking ONE edge of the cycle (i.e., reducing
   one note to a self-contained derivation that doesn't cite the others)
   would unblock the whole cycle.
2. **G_bare normalization family.** The 6-note G_bare cluster is the
   single biggest leverage point on `main`: 1010 downstream transitive
   descendants flow from `minimal_axioms_2026-04-11`. If the G_bare = 1
   fixation is closed at theorem-grade, almost half of the
   `proposed_retained` critical/high cohort propagates.
3. **`alpha_s_derived_note`.** Appears in two of the top-8 root chains
   (Wolfenstein, CKM-NLO). Because `alpha_s` chains into both the CKM
   atlas and the matter-mass program, ratifying it has cross-lane
   leverage.
4. **`left_handed_charge_matching_note`.** Self-conditional: the
   `Q = T_3 + Y/2` hypercharge readout is admitted as a textbook bridge
   rather than derived. Closing this one note unblocks 488 descendants.

## 3. Cohort A summary table (FIXED by this campaign)

For completeness, the 16 runner stale-path fixes:

| PR | block | runners fixed | verdicts expected after re-audit |
|---|---|---:|---|
| #246 | Block 1 | 8 dm_neutrino + dm_leptogenesis runners | 8 leaf rows: audited_conditional/failed → audited_clean (if no other issues) |
| #247 | Block 2 | 8 more runners (dm + gauge_vacuum) | 8 leaf/medium rows: same expected outcome |

These do NOT promote any row to `retained`. Author-declared status is
preserved (`support` / `bounded` / `unknown`); only the FileNotFoundError
noise floor is cleared.

## 4. Out-of-cohort observations

The audit ledger has a few rows that look like "almost retained" but are
actually stable. For completeness:

- **`kubo_fam2_refinement_note`** is the single row currently
  `effective_status: proposed_retained` (italicized in the ledger).
  `audit_status: unaudited`, no open_dependency_paths, no blocker. This
  is a classic "ready for fresh-context audit" candidate — but a
  context-tainted in-conversation audit cannot land `audited_clean`. A
  fresh-context auditor (Codex-GPT-5.5 or independent) would need to
  audit it under `independence: fresh_context`.
- The 76 already-retained rows are the framework's working core. None
  needs LHF intervention.
- `audited_decoration` (5), `audited_renaming` (48), `audited_numerical_match` (26)
  cohorts are not LHF candidates either: those verdicts are saying the
  note's load-bearing step is not actually a derivation, and "fixing"
  them means demoting the author's status to `support`/`bounded`, not
  promoting to `retained`.

## 5. Recommended next moves for the user

1. **Land PR #246 + PR #247** to clear the runner-side noise floor.
2. **Schedule fresh-context audits** for the queue's "Ready" critical
   items (currently 13 critical, 195 high). These need clean-room
   sessions with restricted inputs per the AUDIT_AGENT_PROMPT_TEMPLATE,
   not in-conversation work.
3. **Pick one root blocker** from §2.1 and assign a science-loop
   campaign to close it. The G_bare normalization family (root rank 1) is
   the single highest-leverage target.
4. **Resolve the yt_ew_color_projection 3-cycle** as a separate science
   block. This is medium complexity but very high leverage.
5. **Audit `kubo_fam2_refinement_note`** in a fresh context — it is the
   only currently-pending `proposed_retained` row and is the cleanest
   single-cycle audit-ratification candidate on `main`.

## 6. Forbidden-import role

This note introduces no new physical content, no new numerical comparators,
no new admitted observations. It is pure synthesis of audit ledger data
plus the campaign's own runner-fix output (Cohort A).

## 7. Safe wording

**Can claim:**
- "Audit-row LHF assessment based on the 2026-05-01 audit ledger."
- "16 runner stale-path bugs identified and fixed (PRs #246, #247)."
- "Critical/high audit blockers ranked by downstream transitive impact."
- "Cohort B blockers require substantive science work."

**Cannot claim:**
- bare "retained" / "promoted"
- "promoted X to retained"
- "closed audit on X"

## 8. Cross-references

- Block 1 PR #246 — DM-cluster runner stale-path cleanup
- Block 2 PR #247 — DM + gauge-vacuum runner stale-path cleanup (block 2)
- `docs/audit/AUDIT_LEDGER.md` — generated audit ledger
- `docs/audit/AUDIT_QUEUE.md` — pending audit queue (565 items)
- `docs/audit/AUDIT_AGENT_PROMPT_TEMPLATE.md` — fresh-context audit template
- `docs/audit/data/audit_ledger.json` — source of truth for this analysis
