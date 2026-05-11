# Persistent Record Side-Bit Note

**Date:** 2026-04-03  
**Status:** bounded refinement tested
**Claim type:** bounded_theorem

**Audit-conditional perimeter (2026-05-08):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
packet contains retained bounded parents for the baseline matched
comparison and overlap-kernel model, but it does not include the
side-bit runner output or log that generated the new side-bit values.
The missing step is an included computation or retained authority
verifying the side-bit table and its implementation." This
rigorization edit only sharpens the boundary of the conditional
perimeter; nothing here promotes audit status. The supported content
of this note is the methodological framing — the side-bit
implementation rule, the matched-comparison protocol, and the
qualitative "modest improvement on soft-overlap, no node-label win"
read; the numerical table at N ∈ {8, 12, 18} is registered against
[`logs/2026-04-03-persistent-record-sidebit-matched-compare.txt`](../logs/2026-04-03-persistent-record-sidebit-matched-compare.txt)
but the third-decimal drift across reruns is documented inline (e.g.
side-bit `gamma=1.0` at N=12 reads ~0.5685–0.5698 across runs). The
side-bit runner stdout from
[`scripts/persistent_record_overlap_kernel.py --side-bit`](../scripts/persistent_record_overlap_kernel.py)
is the registered re-derivation harness; a future runner-cache deposit
of the side-bit row would close the missing-stdout gap and is the
prescribed repair path.

## Purpose

Follow up the persistent-record overlap-kernel pilot with the smallest useful
record-geometry refinement:

- keep the same mesoscopic worldtube-count record cells
- add one extra persistent packet-side / slit-side marker bit

The goal was to test the next sharper question from the matched comparison:

- can a slightly richer persistent record geometry improve the bounded
  comparison against node-label **without** giving up the residual
  branch-overlap structure?

## Implementation

The existing persistent-record script now supports:

- [`persistent_record_overlap_kernel.py`](../scripts/persistent_record_overlap_kernel.py)
  with `--side-bit`

The side bit is implemented as one additional persistent marker cell:

- written on the first recorded mass interaction
- chosen from the incoming packet side relative to the center line
- retained alongside the existing worldtube-count record state

The matched harness now also supports side-bit variants:

- [`persistent_record_matched_compare.py`](../scripts/persistent_record_matched_compare.py)

Relevant log:

- [`2026-04-03-persistent-record-sidebit-matched-compare.txt`](../logs/2026-04-03-persistent-record-sidebit-matched-compare.txt)

## Matched result (`2` seeds, `gamma = 1.0`)

The numerical values below are the frozen 2026-04-03 record. Live runner
output drifts in the third decimal across reruns (e.g. side-bit `gamma=1.0`
at `N=12` reads `~0.5685-0.5698` and side-bit detector counts at `N=18` read
`~121-123`). The qualitative read is unchanged: side-bit modestly improves
the soft-overlap lane but does not beat node-label on this bounded slice.

| N | node | persistent trace | persistent `gamma=1.0` | side-bit trace | side-bit `gamma=1.0` |
|---|---:|---:|---:|---:|---:|
| 8  | 0.7971 | 0.8317 | 0.8672 | 0.8323 | 0.8644 |
| 12 | 0.5128 | 0.5349 | 0.6099 | 0.5284 | ~0.569 |
| 18 | 0.7121 | 0.7511 | 0.7314 | 0.7702 | ~0.727 |

Lower purity is better.

Mean detector-sector counts:

- base persistent trace / soft: `8.5, 30.0, 91.5`
- side-bit trace / soft: `9.5, 37.5, 121.0`

## What changed

### Positive

- the side bit improves the **soft-overlap** persistent lane on the bounded
  slice:
  - `N = 12`: `0.6099 -> 0.5685`
  - `N = 18`: `0.7314 -> 0.7270`
- so the extra side memory is not a null perturbation; it does add useful
  branch discrimination while keeping the overlap-kernel architecture intact

### Constraint

- the side bit does **not** beat node-label on raw purity
- the side bit does **not** improve the exact-trace lane uniformly:
  - it helps at `N = 12`
  - but worsens `N = 18` trace purity (`0.7511 -> 0.7702`)

## Safe read

The bounded safe wording is:

- one extra persistent packet-side bit is a **real but modest improvement** to
  the soft-overlap persistent-record lane
- it narrows the gap to node-label on the bounded matched slice
- but it still does **not** produce a new winner on raw decoherence

So the answer to the sharper follow-up question is:

- **partly yes** for the residual-connection lane
- **not yet** for beating node-label outright

## Best next move

The next bounded improvement should target not just side identity, but
**side + local packet placement** together.

The clean next test is:

1. keep the worldtube counts
2. keep the single side bit
3. add one extra bounded packet-placement bit near the retained packet band
4. rerun the same matched `N = 8, 12, 18` table

That is now more justified than sweeping larger `N` on the current side-bit
state alone.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [persistent_record_matched_compare_note](PERSISTENT_RECORD_MATCHED_COMPARE_NOTE.md)
- [persistent_record_overlap_kernel_note](PERSISTENT_RECORD_OVERLAP_KERNEL_NOTE.md)
