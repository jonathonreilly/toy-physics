# Examples — Recent campaign work under the new model

**Date:** 2026-05-02

This document walks through real recent claims from the repo and shows
exactly what happens to each under the proposed scope-aware classification.
Designed to give the reviewer a concrete feel for whether the new model
preserves nuance or papers over distinctions.

## Example A — Yesterday's 24h axiom-first thermo campaign (Block 01-10)

| Block | Note | Today's `current_status` / `audit_status` / `effective_status` | Proposed `claim_type` | Proposed `effective_status` |
|---|---|---|---|---|
| 01 KMS | `AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | positive_theorem | proposed_retained → retained when upstream RP+spec ratify |
| 02 Hawking T_H | `AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | bounded_theorem (Killing-horizon admission) | proposed_retained → retained_bounded once upstream chain clears |
| 03 Bekenstein | `AXIOM_FIRST_BEKENSTEIN_BOUND_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | bounded_theorem (depends on BH 1/4) | proposed_retained → retained_bounded once BH 1/4 closes |
| 04 microcausality | `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | positive_theorem | proposed_retained → retained when upstream chain clears |
| 05 first law | `AXIOM_FIRST_FIRST_LAW_BH_MECHANICS_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | bounded_theorem (admitted Wald-Noether) | proposed_retained → retained_bounded |
| 06 Stefan-Boltzmann | `AXIOM_FIRST_STEFAN_BOLTZMANN_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | positive_theorem | proposed_retained → retained |
| 07 Reeh-Schlieder | `AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | positive_theorem | proposed_retained → retained |
| 08 Unruh | `AXIOM_FIRST_UNRUH_TEMPERATURE_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | bounded_theorem (Bisognano-Wichmann admission) | proposed_retained → retained_bounded |
| 09 Birkhoff | `AXIOM_FIRST_BIRKHOFF_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | positive_theorem | proposed_retained → retained (framework GR is already retained) |
| 10 GSL | `AXIOM_FIRST_GENERALIZED_SECOND_LAW_THEOREM_NOTE_2026-05-01.md` | support / unaudited / support | bounded_theorem (admitted NEC + Hawking 1971 area theorem) | proposed_retained → retained_bounded |

**Today's outcome:** all 10 stuck at `support` indefinitely.
**Proposed outcome:** 4 become `retained` outright (01, 04, 06, 07, 09 once
upstream is clean); 6 become `retained_bounded` with explicit scopes.
Block 09 (Birkhoff) is the cleanest example — its only upstream is
`framework GR` which is already retained, so under the new model it
auto-promotes to `retained` immediately.

The bounded-theorem cases are honest: each note already says explicitly
"this is conditional on admitted Wald" or "this is conditional on
Bisognano-Wichmann". Under the new model that conditional becomes the
canonical `claim_scope` field on the audit row, propagated downstream
verbatim. Today, downstream consumers have to re-read the prose to
discover the bound; under the new model they read the structured field.

## Example B — Apr 29 axiom-first foundations

The five upstream support notes from yesterday's analysis:

| Note | Today's status | Codex audit | Proposed `claim_type` | Proposed `effective_status` |
|---|---|---|---|---|
| RP `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md` | support / `audited_clean` cross-family | clean | positive_theorem | retained (chain to A_min is clean) |
| Spectrum cond `AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md` | support / `audited_conditional` (RP not registered as ledger dep) | conditional | positive_theorem (after the dep registration is fixed) | retained after fix |
| Cluster decomp `AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md` | support / `audited_clean` | clean | positive_theorem | retained |
| Spin-statistics `AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md` | support / `audited_clean` | clean | positive_theorem | retained |
| BH 1/4 `BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md` | bounded / unaudited / `audited_conditional` (propagated from related Planck row) | conditional via inheritance | bounded_theorem (admitted Wald + bridge premise) | retained_bounded once Codex audit ratifies the bounded scope, OR remains audited_conditional if the bridge premise itself isn't admitted-context grade |

**Today's outcome:** clean audits sit at `support` because authors didn't
relabel.
**Proposed outcome:** four propagate to `retained` immediately upon Codex
audit; BH 1/4 propagates to `retained_bounded` honestly with the conditional
recorded as `claim_scope`.

## Example C — Honest bounded science (DM eta freezeout-bypass)

From `MEMORY.md`: "DM eta freezeout-bypass: bounded theorem; m_DM = N_sites·v
candidate, G1 SU(3) lane open."

| Today | Proposed |
|---|---|
| `current_status: bounded` (author honestly bounding the claim) | `claim_type: bounded_theorem` (auditor's reading matches) |
| `audit_status: audited_conditional` (depends on G1 SU(3) lane being open) | `audit_status: audited_conditional` (unchanged) |
| `effective_status: bounded` (under-states audit verdict) | `effective_status: audited_conditional` (matches verdict) |

The new model is more honest: the conditional verdict propagates as
`audited_conditional`, not `bounded`. When the G1 SU(3) lane closes (the
real science work), the row becomes `audited_clean` + `bounded_theorem`,
and `effective_status` propagates to `retained_bounded`.

## Example D — Stretch attempt with named residual (Koide Q V7.3)

From `MEMORY.md`: "V7.3 (commit 302cd9e3) scoped to 'retained promotion
theorem' matching Codex V5/V6 landing pattern; substantive R1+R2→CD/CRIT
residual derivation lands cleanly with conditional Q closure corollary;
runner PASS=56 FAIL=0".

| Today | Proposed |
|---|---|
| `current_status: support` (or a "retained promotion theorem" composite) | `claim_type: open_gate` (auditor reads "conditional Q closure corollary" as named-residual stretch attempt) |
| `audit_status: pending` | `audit_status: audited_clean` (the partial work that is shown closes cleanly; the residual is honestly named) |
| `effective_status: ` ambiguous | `effective_status: open_gate` (never propagates to retained; correctly marks this as work-in-progress) |

The `open_gate` `claim_type` lets the audit ledger track what this note
*actually is* — a stretch attempt with a named residual — without conflating
it with a closed theorem. Future closure of the residual would be a separate
new note that cites the open_gate row.

## Example E — Pure decoration

Hypothetical example: a note that derives `α_s² = 0.01395` from the retained
`alpha_s = 0.1181` row.

| Today | Proposed |
|---|---|
| `current_status: support` (author wrote a tool note) | `claim_type: decoration` (auditor: load-bearing class A, single parent, no new content) |
| `audit_status: audited_decoration` | `audit_status: audited_decoration` (unchanged) |
| `effective_status: audited_decoration` (boxed) | `effective_status: decoration_under_alpha_s_derived_note` (boxed; rendering shows it as a corollary inside the parent note's section in publication tables) |

Under both models the decoration is boxed under the parent. The new model
makes the parent relationship explicit in `effective_status` so the
publication-renderer doesn't need a separate lookup.

## Example F — Active open-gate work (Hubble C1 carrier metrology)

From `MEMORY.md`: "Hubble constant derivation … late-time (C1) absolute-scale
gate is the remaining conditional premise."

| Today | Proposed |
|---|---|
| `current_status: open` (the C1 gate is open work) | `claim_type: open_gate` |
| `audit_status: pending` | `audit_status: audited_clean` (the carrier-metrology audit work that *was done* closes for the bounded scope it claims) |
| `effective_status: open` | `effective_status: open_gate` (never propagates to retained; signals to downstream that this is the load-bearing open lane) |

Same outcome, but the new `open_gate` value is more semantically precise
than the old `open` (which was used for both "active gate" and
"audit-pending unknown").

## Example G — README / lane index (currently `unknown`)

`docs/lanes/ACTIVE_WORKING_LANES_2026-04-26.md`:

| Today | Proposed |
|---|---|
| `current_status: unknown` (no parseable Status line) | `claim_type: meta` (auditor identifies this as a navigation/index doc) |
| `audit_status: unaudited` (clutters queue) | `audit_status: unaudited`, but `claim_type: meta` excludes it from the audit queue's priority list |
| `effective_status: unknown` | `effective_status: meta` (publication renderers hide it; audit queue ignores it) |

The 985 currently-`unknown` rows that bloat the queue get cleanly excluded
without dropping them from the citation graph (they may still cite or be
cited by other notes for navigation).

## Net assessment

Across all seven examples:

- The new model is at least as informative as the current one, and
  **strictly more informative** in 6/7 cases.
- The new model makes existing implicit information explicit (e.g.
  `claim_scope` for bounded theorems, `decoration_parent` for boxed
  consequences, `open_gate` for stretch attempts).
- No example loses meaning under the migration.
- Several examples that today have stuck states (yesterday's 10 blocks,
  the Apr 29 axiom-first chain) get unstuck.
