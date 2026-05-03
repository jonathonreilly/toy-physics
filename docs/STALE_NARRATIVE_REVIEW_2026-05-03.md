# Stale-Narrative Archival Review — 2026-05-03

**Type:** meta
**Status:** review inventory; not a claim, not an action plan

Audit-repair scan of all rows currently at `audit_status = audited_failed`. Per
[`docs/audit/STALE_NARRATIVE_POLICY.md`](audit/STALE_NARRATIVE_POLICY.md), failed
source notes are archived to `archive_unlanded/<cluster-tag>/` when "no durable
structural observation remains." Fresh failures pointing at specific fixable
steps are NOT archival candidates — those are science-side repair work.

## Inventory

| location | count |
|---|---:|
| Active in `docs/` (NOT for archival — fresh failures) | 7 |
| Already archived under `archive_unlanded/` | 44 |
| **Total audited_failed** | **51** |

## Active failed rows (7) — review verdicts

All 7 active failures are dated within the last 48 hours. Each verdict points at
a specific, fixable load-bearing step (math errors, missing runners, asserted
identifications). These are repair-work targets, not stale narratives.

| claim_id | criticality | td | audit_date | verdict_rationale (excerpt) |
|---|---|---:|---|---|
| `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | 294 | 2026-05-03 | Issue: The theorem as stated depends on imported OS/STW/Menotti reflection-positivity machinery, an unproved match between those theorem hyp... |
| `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | critical | 292 | 2026-05-03 | Issue: Step 1 misidentifies Cl(3) ⊗_R C as M_2(C) by halving the tensor-product dimension and ignoring the odd-complex-Clifford split. Why t... |
| `architecture_note_directional_measure` | critical | 289 | 2026-05-03 | Issue: The claim rests on listed empirical test outcomes and an empirically chosen beta = 0.8, but the packet provides no runner, no reprodu... |
| `bh_entropy_derived_note` | critical | 287 | 2026-05-03 | Issue: the chain is a finite-size numerical comparator to the BH coefficient, not a first-principles derivation, and the current runner is i... |
| `higgs_mass_from_axiom_note` | high | 60 | 2026-05-02 | Issue: the curvature-to-physical-Higgs-mass bridge is an asserted observable identification, and the 140.3 GeV headline is stale relative to... |
| `axiom_first_spin_statistics_theorem_note_2026-04-29` | medium | 2 | 2026-05-02 | Issue: the note treats A3's finite Grassmann partition as evidence that anticommutation is forced, then relies on a finite per-site Cl(3) mo... |
| `z3_conjugate_support_trichotomy_narrow_theorem_note_2026-05-02` | leaf | 0 | 2026-05-03 | Issue: the proof of T3 relies on the false general statement that exactly three permutation patterns whose union covers the 3x3 grid must be... |

## Already-archived clusters (44)

Stale-narrative archival has been applied correctly to the historical failed
rows. Distribution by archive-cluster directory:

| archive cluster | rows |
|---|---:|
| `archive_unlanded/staggered-backreaction-stale-runners-2026-04-30/` | 6 |
| `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/` | 5 |
| `archive_unlanded/stale-frames-2026-04-30/` | 3 |
| `archive_unlanded/fifth-family-stale-runners-2026-04-30/` | 3 |
| `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/` | 2 |
| `archive_unlanded/testable-ranking-stale-wrappers-2026-04-30/` | 2 |
| `archive_unlanded/portability-stale-extension-wrappers-2026-04-30/` | 2 |
| `archive_unlanded/source-resolved-green-stale-runners-2026-04-30/` | 2 |
| `archive_unlanded/raw-prompt-transcripts-2026-04-30/` | 1 |
| `archive_unlanded/poisson-self-consistency-stale-runners-2026-04-30/` | 1 |
| `archive_unlanded/causal-field-stale-runners-2026-04-30/` | 1 |
| `archive_unlanded/topology-stale-runners-2026-04-30/` | 1 |
| `archive_unlanded/gravity-distance-law-stale-runners-2026-04-30/` | 1 |
| `archive_unlanded/dm-abcc-finite-search-salvage-2026-04-30/` | 1 |
| `archive_unlanded/dm-neutrino-stale-runners-2026-04-30/` | 1 |
| `archive_unlanded/framework-bare-alpha-assumed-input-salvage-2026-04-30/` | 1 |
| `archive_unlanded/grown-transfer-stale-runners-2026-04-30/` | 1 |
| `archive_unlanded/h0125-unverifiable-numerical-diagnostics-2026-04-30/` | 1 |
| `archive_unlanded/if-program-unverifiable-closing-2026-04-30/` | 1 |
| `archive_unlanded/kernel-gravity-conflation-2026-04-30/` | 1 |
| `archive_unlanded/lattice-dense-spent-delay-window-salvage-2026-04-30/` | 1 |
| `archive_unlanded/grown-family-missing-artifacts-2026-04-30/` | 1 |
| `archive_unlanded/session-summary-stale-aggregates-2026-04-30/` | 1 |
| `archive_unlanded/family-card-incomplete-artifacts-2026-04-30/` | 1 |
| `archive_unlanded/process-triage-unreproducible-state-2026-04-30/` | 1 |
| `archive_unlanded/unified-basin-signed-source-salvage-2026-04-30/` | 1 |
| `archive_unlanded/work-history-unverifiable-portability-2026-04-30/` | 1 |

## Recommendation

1. **Do NOT archive the 7 active failures.** Each has a specific verdict
   pointing at a fixable load-bearing step. The science team should address
   them as repair work (or downgrade scope) before any archival decision.

2. **Re-review in 7-14 days.** If a row remains `audited_failed` with no
   science-side response by then, treat the narrative as stale and archive
   per policy.

3. **The 44 already-archived rows are correctly handled** — `seed_audit_ledger.py`
   preserves their `audited_failed` status as negative-result history while
   removing them from the active citation graph.

## Cross-references

- [`docs/audit/STALE_NARRATIVE_POLICY.md`](audit/STALE_NARRATIVE_POLICY.md)
- [`docs/audit/AUDIT_LEDGER.md`](audit/AUDIT_LEDGER.md)