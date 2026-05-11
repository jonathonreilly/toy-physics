# Complex Selectivity Predictor Note

**Date:** 2026-04-06  
**Status:** proposed_retained narrow predictor card for complex-action survival on structured families
**Claim type:** bounded_theorem

**Audit-conditional perimeter (2026-05-10):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, `claim_type =
bounded_theorem`, `independence = fresh_context`, and load-bearing
step class `B`. The audit chain-closure explanation is exact: "The
conclusion relies on comparison rows and mismatch details whose
direct authorities are not in the supplied one-hop packet, especially
the original grown-basin positive row and the second-family
boundary-window statement. The supplied runner only renders
hard-coded rows, so it does not independently close the missing
comparison." The audit-stated repair target
(`notes_for_re_audit_if_any`) is exact: "missing_dependency_edge —
add direct deps for the original grown-basin complex-positive
authority and `docs/SECOND_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md`,
or remove the rows / details that rely on them; then re-audit the
finite comparison." The generated audit ledger remains the authority for any terminal status. The claim-scope is
audited (not legacy-migration): "Bounded predictor over the listed
structured-family cards: retained complex-action rows are claimed
to coincide with exact `gamma=0` plus anchor-local `TOWARD->AWAY`
crossover, while diagnosed boundary rows fail it." The five
one-hop dependencies registered in the audit `dep_effective_status`
block — `second_grown_family_complex_note` (retained),
`alt_connectivity_family_complex_failure_note` (retained no-go),
`third_grown_family_complex_boundary_note` (retained no-go),
`fourth_family_complex_boundary_note` (retained no-go), and
`fifth_family_complex_boundary_note` (retained_bounded) — are
load-bearing for the *diagnosed-boundary* side of the table. The
**unwired** load-bearing inputs flagged by the verdict are: the
**Original grown basin** complex-positive authority (`yes` retained
complex, anchor crossover `yes on nearby rows`); and the
**second-family** boundary-window statement (the `tighter
AWAY-at-gamma=0 boundary` row that distinguishes the second-family
positive from the second-family boundary closure). Until those
one-hop edges are wired, the safe read of this note is restricted
to the five already-supplied one-hop authorities; the headline
§"Final Verdict" sentence ("retained narrow predictor: complex-action
survival requires an anchor-local crossover; coarser basin geometry
does not predict it") is **conditional** on the two unwired inputs
landing as one-hop edges. Nothing in this edit promotes audit
status. See "Citation chain and audit-stated repair path
(2026-05-10)" below.

## Artifact Chain

- [`scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py`](/Users/jonreilly/Projects/Physics/scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py)
- [`logs/2026-04-06-complex-selectivity-predictor.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-complex-selectivity-predictor.txt)
- retained family cards:
  - [`archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md)
  - [`docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md)
  - [`docs/ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md)
  - [`docs/THIRD_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THIRD_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md)
  - [`docs/FOURTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FOURTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md)
  - [`archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md)
  - [`docs/FIFTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FIFTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md)

## Question

What is the smallest review-safe discriminator for when a complex-action
companion survives on a structured family?

## Comparison

| family | retained complex | exact gamma=0 | anchor crossover | basin shape | discriminator note |
| --- | --- | --- | --- | --- | --- |
| Original grown basin | yes | yes | yes on nearby rows | narrow and selective | anchor-local crossover survives on a nearby row neighborhood |
| Second-family complex | yes | yes | yes on the anchor row | tiny basin | exact gamma=0 + Born proxy + crossover survive narrowly |
| Alt connectivity family | no | yes | no | bounded sign-law basin only | sign-law survives, complex branch does not |
| Third grown family | no | yes | not stable across drift window | bounded drift basin | crossover is seed-selective and drift-sensitive; not retained |
| Fourth family quadrant | no | yes | no | narrow seed-selective sign basin | complex response stays boundary-like despite clean controls |
| Fifth family radial | yes | yes | yes on the anchor row | narrow anchor-row basin | anchor-local crossover survives, but only at the center row |

## Safe Read

- exact gamma=0 baseline is necessary, but not sufficient
- signed-source portability and weak-field linearity do not predict complex survival by themselves
- support width and seed selectivity are useful context, but they do not separate the positive families from the diagnosed boundaries cleanly
- the smallest stable discriminator we found is the anchor-local crossover: exact gamma=0 baseline plus `TOWARD -> AWAY` on the retained anchor row

## Exact Mismatch

- the original grown basin and the fifth-family radial slice retain the crossover only in a narrow local neighborhood
- the second-family complex slice retains it on the anchor row but loses it in the tighter boundary window
- the alt, third, and fourth families all fail the same crossover test in structurally different ways

## Final Verdict

**retained narrow predictor: complex-action survival requires an anchor-local crossover; coarser basin geometry does not predict it**

## Citation chain and audit-stated repair path (2026-05-10)

The audit verdict (2026-05-10, see top of note) flags two
load-bearing inputs that are not currently supplied as one-hop
audit-graph dependency edges on this row, and notes that the
supplied runner only renders hard-coded rows. The cited authority
chain is registered explicitly below so the wired and unwired
one-hop edges are visible.

| Cited authority | File / log | Audit-graph status (2026-05-10) | Role on this row |
|---|---|---|---|
| Active runner | [`scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py`](../scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py) | `runner_path` registered in `audit_ledger.json` | renders the hard-coded comparison rows in §Comparison; runner alone does not independently close the missing comparison rows because the row content is hard-coded |
| Audit-lane runner cache | [`logs/runner-cache/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.txt`](../logs/runner-cache/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.txt) | runner-cache copy under `scripts/runner_cache.py` | runner-cache replay verifying the row table |
| Wired one-hop dep — second family complex | [`docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`](SECOND_GROWN_FAMILY_COMPLEX_NOTE.md) | `retained` (per audit `dep_effective_status`) | supplies the second-family anchor-row complex retention |
| Wired one-hop dep — alt complex failure | [`docs/ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md`](ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md) | `retained_no_go` | supplies the alt-family complex-action failure |
| Wired one-hop dep — third family complex boundary | [`docs/THIRD_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](THIRD_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md) | `retained_no_go` | supplies the third-family complex boundary diagnosis |
| Wired one-hop dep — fourth family complex boundary | [`docs/FOURTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](FOURTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md) | `retained_no_go` | supplies the fourth-family complex boundary diagnosis |
| Wired one-hop dep — fifth family complex boundary | [`docs/FIFTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](FIFTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md) | `retained_bounded` | supplies the fifth-family anchor-row complex retention with diagnosed boundary |
| Unwired authority — original grown basin | [`archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md`](../archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md) (signed-source side) and [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md) (complex-action side) | not wired as one-hop edges (signed side is archived under `archive_unlanded/`); cited only in `source_notes` of the runner row | needed for the original grown-basin row (`retained_complex = yes`, `anchor_crossover = yes on nearby rows`) |
| Unwired authority — second-family boundary | [`docs/SECOND_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](SECOND_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md) | not wired as one-hop edge from this row | needed for the second-family boundary-window discriminator note ("exact gamma=0 + Born proxy + crossover survive narrowly", "loses it in the tighter boundary window") |
| Sibling archive — fifth-family stale runner | [`archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md`](../archive_unlanded/fifth-family-stale-runners-2026-04-30/FIFTH_FAMILY_COMPLEX_NOTE.md) | not wired as one-hop edge (archived) | source-context provenance for the fifth-family row |
| Repo baseline anchor | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | `unaudited` / `meta` | repo-baseline terminology anchor for the path-sum architecture |

The audit-stated repair path (verbatim from the audit
`notes_for_re_audit_if_any`) is to either (i) **add direct
dependency edges** for the original grown-basin complex-positive
authority and `docs/SECOND_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md`,
or (ii) **remove the rows / details that rely on them**, then
re-audit the finite comparison. Path (i) wires the two unwired
authorities as one-hop edges (preserves the full §Comparison
table; the original grown basin is currently archived, so this
route requires either un-archiving the relevant note or replacing
it with an in-`docs/` retained authority). Path (ii) narrows the
source comparison to the five wired one-hop authorities by dropping
the "Original grown basin" row and the second-family discriminator
detail "exact `gamma=0` + Born proxy + crossover survive narrowly".
Until one of those lands, the regenerated ledger leaves this row for
independent audit and the safe read is the partial bounded comparison over the
supplied authorities. The acknowledged residual is the absence of
the two listed one-hop audit-graph edges plus the runner's
hard-coded-row limitation (the runner cannot itself independently
close the missing comparison row content); everything else (the
§Safe Read summary on `gamma=0` necessity, the five wired
authorities, the discriminator-note table content for the wired
families) is supported by the listed cited authorities.

This rigorization edit only sharpens the conditional perimeter and
registers the cited authority chain; it does not promote audit
status, hand-author audit JSON, modify the §Comparison table, or
narrow the source claim. The claim boundary in §Final Verdict
continues to apply: the predictor is bounded over the listed
structured-family cards, not a universal family-portable
discriminator; until the two unwired inputs land as one-hop edges,
the headline reads as a **partial bounded predictor** over the
five wired authorities.
