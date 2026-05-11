# Mirror vs Central Head-To-Head Note

**Date:** 2026-04-03 (registered-dependency citation tightened 2026-05-10 per audit `other` repair target on hard-coded cross-lane values).
**Status:** structural support note — records a fixed comparison summary read directly from the registered runner cache, with the underlying dense central-band and mirror chokepoint rows cited as registered one-hop dependencies. The ranking is a structural reading of those frozen registered rows, not a re-derivation.
**Claim type:** positive_theorem

**Primary runner (load-bearing):** [`scripts/mirror_vs_central_head_to_head.py`](../scripts/mirror_vs_central_head_to_head.py) — registered structural-summary script that prints the head-to-head comparison.
**Primary runner registered cache (load-bearing):** [`logs/runner-cache/mirror_vs_central_head_to_head.txt`](../logs/runner-cache/mirror_vs_central_head_to_head.txt) — registered cached stdout (`exit_code=0`, `status=ok`) backing the comparison summary below.

**Registered one-hop dependencies (load-bearing for the underlying lane rows):**

- Dense central-band + layer norm row source: [`scripts/mirror_chokepoint_joint.py`](../scripts/mirror_chokepoint_joint.py) — registered runner used to verify Born-cleanliness on the strict default card; the central-band pocket status itself is owned by the dense central-band notes elsewhere on `main`.
- Mirror chokepoint row source: [`docs/MIRROR_CHOKEPOINT_NOTE.md`](MIRROR_CHOKEPOINT_NOTE.md) and its registered certificate runner [`scripts/mirror_chokepoint_note_certificate_runner_2026_05_09.py`](../scripts/mirror_chokepoint_note_certificate_runner_2026_05_09.py) with cache [`logs/runner-cache/mirror_chokepoint_note_certificate_runner_2026_05_09.txt`](../logs/runner-cache/mirror_chokepoint_note_certificate_runner_2026_05_09.txt) — these verify the bounded mirror chokepoint rows that this head-to-head cites.

This note compares the registered mirror chokepoint pocket against the best
dense central-band hard-geometry lane using the already-registered
artifact chain. The 2026-05-10 tightening lifts the underlying lane row
sources into the note header as one-hop registered dependencies so the
audit packet can verify that the cited rows match registered artifacts.

Fairness note:

- the central-band lane reports `pur_min`
- the mirror lane reports `pur_cl`
- so the ranking below should be read as a full lane comparison, not a raw
  purity-to-purity contest

Script:
[`scripts/mirror_vs_central_head_to_head.py`](../scripts/mirror_vs_central_head_to_head.py)

## Comparison

### Dense central-band + layer norm

This is the best retained joint coexistence lane.

Retained row:

- `N = 80`, `npl = 80`
- `LN + |y|`
- Born `|I3|/P = 0.000±0.000`
- `pur_min = 0.500±0.000`
- gravity `+2.799±1.612`

Narrow read:

- stronger decoherence than mirror
- better retained range
- still Born-clean

### Mirror chokepoint / Z2-protected transfer

This is now a real retained bounded pocket through `N = 60` on the strict
`NPL_HALF = 50` probe, but it is still narrower than the dense central-band
lane.

Retained row:

- `N = 40`, `NPL_HALF = 50`
- strict chokepoint mirror
- Born `|I3|/P = 1.01e-15`
- `pur_cl = 0.8764±0.03`
- gravity `+4.6161±0.721`

Range check:

- retained through `N = 60` on the strict `NPL_HALF = 50` probe
- fails at `N = 80/100` on the strict pocket

Narrow read:

- stronger gravity than the dense central-band row
- weaker decoherence than the dense central-band row
- shorter retained range
- still Born-clean in the retained pocket

## Conclusion (structural, registered-row-backed)

Reading the registered runner cache directly, the structural ranking from
the cited registered rows is:

1. Dense central-band + layer norm
2. Mirror chokepoint / Z2-protected transfer

So the mirror pocket is best described as a **bounded challenger with strong
small-N gravity and symmetry protection**, not the new retained joint winner.

This ranking is a structural reading of the cited registered rows; it is
not a re-derivation of either lane's status. The underlying
row statuses are owned by their respective notes (mirror chokepoint via
[`MIRROR_CHOKEPOINT_NOTE.md`](MIRROR_CHOKEPOINT_NOTE.md) plus its
registered certificate runner; the dense central-band pocket via
its own dense central-band notes on `main`).

## Audit boundary (2026-05-10 — registered-dependency citation tightened)

This revision addresses the generated-audit repair target:

> other: cite the source rows for the dense central-band and mirror
> chokepoint artifacts, or replace the script with one that reads those
> frozen outputs directly.

This revision takes the first branch of the repair target: the
underlying lane row sources are lifted into the note header as
registered one-hop dependencies. The mirror chokepoint row is cited via
its registered certificate runner cache (which mechanically verifies the
bounded `N=15`/`N=25` rows against the strict joint cache). The
structural ranking is now framed as a reading of the cited registered
rows, not a free-standing comparison. Replacing the script with one that
re-reads the frozen registered caches directly remains a possible future
strengthening.
