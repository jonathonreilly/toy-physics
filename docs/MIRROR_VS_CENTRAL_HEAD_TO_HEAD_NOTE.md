# Mirror vs Central Head-To-Head Note

**Date:** 2026-04-03
**Status:** review-safe comparison summary

This note compares the retained mirror chokepoint pocket against the
best dense central-band hard-geometry lane using the already-retained
artifact chain on `main`.

Fairness note:

- the central-band lane reports `pur_min`
- the mirror lane reports `pur_cl`
- so the ranking below should be read as a full lane comparison, not a raw
  purity-to-purity contest

Script:
[`scripts/mirror_vs_central_head_to_head.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_vs_central_head_to_head.py)

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

## Conclusion

The mirror result is now artifact-backed and genuinely interesting, but it does
**not** beat the dense central-band lane as the best joint lane.

The clean ranking is:

1. Dense central-band + layer norm
2. Mirror chokepoint / Z2-protected transfer

So the mirror pocket is best described as a **bounded challenger with strong
small-N gravity and symmetry protection**, not the new retained joint winner.
