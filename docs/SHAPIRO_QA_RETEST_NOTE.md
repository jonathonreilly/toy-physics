# Shapiro QA Retest Note

**Date:** 2026-04-06
**Status:** bounded - bounded or caveated result note
**Primary runner:** [`scripts/shapiro_phase_lag_probe.py`](../scripts/shapiro_phase_lag_probe.py) (positive: portable, seed-stable discrete Shapiro-delay observable with exact zero control and family spread <2e-4 rad)

## Cited authorities (one hop)

The 2026-05-03 citation-graph repair registers the load-bearing one-hop deps
listed under §Scope as proper markdown links. The two archive_unlanded
references in §Scope are intentionally not registered as audit-graph
authorities (archived narrative, no active claim).

- [`SHAPIRO_DELAY_NOTE.md`](SHAPIRO_DELAY_NOTE.md)
  — retained Shapiro-phase delay reference whose canonical replay this
  note QA-confirms.
- [`SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md`](SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md)
  — retained static-discriminator boundary reference whose smallest
  control this note replays.
- [`SHAPIRO_FAMILY_PORTABILITY_NOTE.md`](SHAPIRO_FAMILY_PORTABILITY_NOTE.md)
  — portable-family scope used in the QA replay control.

## Scope

Focused QA pass on the Shapiro-phase lane:

- `scripts/shapiro_phase_lag_probe.py`
- `scripts/shapiro_static_discriminator.py`
- retained notes:
  - `docs/SHAPIRO_DELAY_NOTE.md`
  - `docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md`
  - `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_COMPLEX_INTERACTION_NOTE.md`
  - `docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md`
  - `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/SHAPIRO_DIAMOND_BRIDGE_NOTE.md`

The goal was to replay the smallest controls, check for source-placement or
static-shape loopholes, and only file a tracker issue if a concrete defect
showed up.

## Retest

### Canonical phase lag replay

`python3 scripts/shapiro_phase_lag_probe.py --format text`

This replay is clean and matches the retained note:

- `c = inst`: `+0.0000 rad`
- `c = 2.0`: mean `+0.0401 rad`, spread `0.0001 rad`
- `c = 1.0`: mean `+0.0500 rad`, spread `0.0002 rad`
- `c = 0.5`: mean `+0.0621 rad`, spread `0.0002 rad`
- `c = 0.25`: mean `+0.0679 rad`, spread `0.0000 rad`

The zero control is exact, and the portable family spread stays at or below
`2e-4 rad`.

### Small static-discriminator control

I replayed the smallest boundary check on one retained family
(`Fam1 = drift 0.20, restore 0.70`) using the internal discriminator helpers.

Observed result:

- zero control: exact `0.0`
- causal lag:
  - `c = 2.0`: `+0.0373`
  - `c = 1.0`: `+0.0448`
  - `c = 0.5`: `+0.0569`
  - `c = 0.25`: `+0.0659`
- static cone shape:
  - exact match to the causal curve at the same `c` values
- static scheduling:
  - near-flat response around `+0.0445` to `+0.0450`

This confirms the boundary stated in `docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md`:
the phase lag is a real portable observable, but static cone-shape effects can
reproduce it exactly. Static scheduling does not.

## QA Read

- No source-placement bug was found in the retained phase-lag replay.
- No static-shape loophole was found beyond the already documented boundary:
  static cone shape is a lookalike, not a defect.
- The static-discriminator script is computationally heavier than the canonical
  phase-lag probe, but that is a cost characteristic, not a correctness issue.

## Conclusion

**clean retest discipline confirmed**

The Shapiro-phase lane replays correctly, the exact zero controls survive, and
the static-cone boundary result remains consistent with the retained notes.
No concrete tracker issue was added.
