# Complex Selectivity Compare Note

**Date:** 2026-04-06  
**Status:** narrow comparison card for signed-source portability vs complex-action selectivity
**Claim type:** bounded_theorem

**Audit-conditional perimeter (2026-05-10):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, `claim_type =
bounded_theorem`, `independence = fresh_context`, and load-bearing
step class `B`. The audit chain-closure explanation is exact: "The
supplied one-hop authorities support second-family complex retention
and signed-source positives for the alt, third, and fourth families,
but they do not supply the original grown-basin row, the alt
complex-action failure, the alt F~M transfer value, or the
second-family boundary tightening. Those missing inputs are
load-bearing for the selectivity split." The audit-stated repair
target (`notes_for_re_audit_if_any`) is exact:
"missing_dependency_edge - add the missing direct dependencies for
the original grown-basin comparison, alt complex failure / F~M
transfer, and second-family boundary tightening, then re-audit the
bounded selectivity split." The generated audit ledger remains the authority for any terminal status. The claim-scope is
audited (not legacy-migration): "Bounded comparison that the listed
signed-source family slices are more portable than the listed
complex-action slices." The four one-hop dependencies registered in
the audit `dep_effective_status` block — `second_grown_family_complex_note`
(retained), `alt_connectivity_family_sign_note`, `third_grown_family_sign_note`,
and `fourth_family_quadrant_note` (all `retained_bounded`) — are
load-bearing for the *signed-source* side of the table. The four
**unwired** load-bearing inputs flagged by the verdict are: the
**Original grown basin** comparison row (signed-source `retained
narrow basin positive` and complex `retained narrow gamma=0 -> AWAY
crossover on nearby rows`); the **alt connectivity family**
**complex-action failure** row (`clean boundary failure; no
TOWARD -> AWAY crossover`); the **alt** family `F~M = 0.999994`
weak-field transfer value; and the **second-family** boundary
tightening (`tiny basin, then a tighter AWAY-at-gamma=0 boundary`).
Until those one-hop edges are wired, the safe read of this note is
restricted to the four already-supplied retained one-hop authorities;
the headline §"Final Verdict" sentence ("retained selectivity split:
signed-source is family-portable, while complex-action is anchor-local
and boundary-sensitive") is **conditional** on the four unwired
inputs landing as one-hop edges. Nothing in this edit promotes audit
status. See "Citation chain and audit-stated repair path (2026-05-10)"
below.

## Artifact Chain

- [`scripts/COMPLEX_SELECTIVITY_COMPARE.py`](/Users/jonreilly/Projects/Physics/scripts/COMPLEX_SELECTIVITY_COMPARE.py)
- [`logs/2026-04-06-complex-selectivity-compare.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-complex-selectivity-compare.txt)
- retained family cards:
  - [`archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md`](/Users/jonreilly/Projects/Physics/archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md)
  - [`docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md)
  - [`docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md)
  - [`docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md)
  - [`docs/FOURTH_FAMILY_QUADRANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/FOURTH_FAMILY_QUADRANT_NOTE.md)

## Question

Why does signed-source transfer survive on multiple independent families while complex-action companions stay much more selective?

## Comparison

| family | signed-source result | weak-field response | complex-action result | mismatch |
| --- | --- | --- | --- | --- |
| Original grown basin | retained narrow basin positive | `F~M = 1.000` | retained narrow `gamma=0 -> AWAY` crossover on nearby rows | selective basin, not family-wide closure |
| Second-family complex | not the shared surface | `F~M = 1.000` | retained narrow anchor-row positive | tiny basin, then a tighter `AWAY`-at-`gamma=0` boundary |
| Alternative connectivity family | retained bounded positive | `F~M = 0.999994` | clean boundary failure; no `TOWARD -> AWAY` crossover | sign-law survives, complex branch does not |
| Third grown family | retained bounded basin positive | charge exponent `0.999842` | not retained on this slice | signed-source basin survives in the interior only |
| Fourth family quadrant | retained narrow basin | near-linear charge scaling | not retained on this slice | fresh family exists, but remains sign-law only |

## Safe Read

- signed-source transfer is the portable feature: exact zero / neutral controls survive on several distinct structured families
- weak-field linearity survives with the signed-source package across the retained grown, alt, third, and fourth family slices
- complex action is more selective: it needs the exact `gamma=0` anchor / crossover structure and fails cleanly on the alt family and the tightened second-family window

## Exact Mismatch

- the signed-source families share a common control surface
- the complex-action branch does not share that same surface; it lives on a more constrained `gamma` baseline plus crossover test
- the result is not a universal family theorem; it is a selectivity split between portable sign-law and basin-local complex action

## Final Verdict

**retained selectivity split: signed-source is family-portable, while complex-action is anchor-local and boundary-sensitive**

## Citation chain and audit-stated repair path (2026-05-10)

The audit verdict (2026-05-10, see top of note) flags four
load-bearing inputs that are not currently supplied as one-hop
audit-graph dependency edges on this row. The cited authority chain
is registered explicitly below so the wired and unwired one-hop
edges are visible.

| Cited authority | File / log | Audit-graph status (2026-05-10) | Role on this row |
|---|---|---|---|
| Active runner | [`scripts/COMPLEX_SELECTIVITY_COMPARE.py`](../scripts/COMPLEX_SELECTIVITY_COMPARE.py) | `runner_path` registered in `audit_ledger.json` | renders the hard-coded comparison rows in §Comparison; runner alone cannot independently close the missing comparison rows because the row content is hard-coded |
| Frozen runner output | [`logs/2026-04-06-complex-selectivity-compare.txt`](../logs/2026-04-06-complex-selectivity-compare.txt) | preserved log path | reproduces the hard-coded row table cited in §Comparison |
| Audit-lane runner cache | [`logs/runner-cache/COMPLEX_SELECTIVITY_COMPARE.txt`](../logs/runner-cache/COMPLEX_SELECTIVITY_COMPARE.txt) | runner-cache copy under `scripts/runner_cache.py` | runner-cache replay verifying the row table |
| Wired one-hop dep — second family | [`docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md`](SECOND_GROWN_FAMILY_COMPLEX_NOTE.md) | `retained` (per audit `dep_effective_status`) | supplies the second-family complex retention |
| Wired one-hop dep — alt sign | [`docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md`](ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md) | `retained_bounded` | supplies the alt-family signed-source positive |
| Wired one-hop dep — third family | [`docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md`](THIRD_GROWN_FAMILY_SIGN_NOTE.md) | `retained_bounded` | supplies the third-family signed-source basin |
| Wired one-hop dep — fourth family | [`docs/FOURTH_FAMILY_QUADRANT_NOTE.md`](FOURTH_FAMILY_QUADRANT_NOTE.md) | `retained_bounded` | supplies the fourth-family signed-source basin |
| Unwired authority — original grown basin signed-source | [`archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md`](../archive_unlanded/grown-transfer-stale-runners-2026-04-30/GROWN_TRANSFER_BASIN_NOTE.md) | not wired as one-hop edge (archived under `archive_unlanded/`); cited only in `source_notes` of the runner row | needed for the original grown-basin signed-source row |
| Unwired authority — original grown complex companion | [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md) | not wired as one-hop edge | needed for the original grown-basin complex-action row (`gamma=0 -> AWAY`) |
| Unwired authority — alt complex failure | [`docs/ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md`](ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md) | not wired as one-hop edge from this row | needed for the alt-family `clean boundary failure` row |
| Unwired authority — second-family boundary | [`docs/SECOND_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md`](SECOND_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md) | not wired as one-hop edge | needed for the second-family `tighter AWAY-at-gamma=0 boundary` |
| Repo baseline anchor | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | `unaudited` / `meta` | repo-baseline terminology anchor for the path-sum architecture |

The audit-stated repair path (verbatim from the audit
`notes_for_re_audit_if_any`) is to **add the missing direct
dependencies** for the original grown-basin comparison, the alt
complex failure / F~M transfer, and the second-family boundary
tightening, **then re-audit** the bounded selectivity split. Either
of two repair routes satisfies the missing-dependency-edge flag:
(a) wire each of the four listed unwired authorities as one-hop
audit-graph dependency edges from this row (preferred path; preserves
the full §Comparison table), or (b) **narrow** the source comparison
to the four currently-wired one-hop authorities (drop the original
grown-basin row, drop the alt complex-failure mismatch, drop the
second-family boundary-tightening mismatch). Until one of those
lands, the regenerated ledger leaves this row for independent audit,
and the safe read is the partial comparison over the supplied
retained authorities.
The acknowledged residual is the absence of the four listed one-hop
audit-graph edges; everything else (the §Safe Read summary on
signed-source portability, the runner-rendered hard-coded table,
the four wired retained authorities) is supported by the listed
cited authorities.

This rigorization edit only sharpens the conditional perimeter and
registers the cited authority chain; it does not promote audit
status, hand-author audit JSON, modify the §Comparison table, or
narrow the source claim. The claim boundary in §Final Verdict
continues to apply: the selectivity split is bounded over the
listed family slices, not a universal family theorem; until the
four unwired inputs land as one-hop edges, the headline reads as
a **partial bounded comparison** rather than the full selectivity
split.
