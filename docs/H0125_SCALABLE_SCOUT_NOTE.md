# H=0.125 Scalable Scout Note

**Date:** 2026-04-06

**Status:** bounded no-go on the observed full-window rows; not retained.

This note records the shorter-axial-scale scout for the widened `h = 0.125`
dense `1/L^2 + h^2` bridge lane. It is narrower than the already-closed
full-window width-4 replay and asks whether shortening the axial scale opens
any genuinely wider or more scalable replay path worth keeping.

## Controls

- shorter-scale scout:
  - [`logs/2026-04-06-h0125-scalable-scout.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-scalable-scout.txt)
  - `phys_l = 4`
  - `phys_w = 3`
  - `h = 0.125`
  - full window
  - `z_mass = 1.5, 2.0, 3.0`
- retained comparator already closed elsewhere:
  - [`logs/2026-04-06-h0125-wide-full-window.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-h0125-wide-full-window.txt)
  - `phys_l = 6`
  - `phys_w = 4`
  - full window
  - `alpha = 0.499`

## Observed Row

- `phys_l = 4`, `phys_w = 3`, full window:
  - `Born = 6.50e-15`
  - clean `k = 0`
  - `TOWARD` gravity `+0.005594`
  - `alpha = 0.501`, `0.501`, `0.502` across `z_mass = 1.5, 2.0, 3.0`

## Readout

The shorter axial scale did not produce a rescue signal in the observed
full-window row. The retained width-4 comparator stays pinned at
`alpha = 0.499`, while the shorter-scale `phys_l = 4`, `phys_w = 3` scout
only reaches `alpha = 0.501`, `0.501`, `0.502` across the tested masses.

That is a clean bounded no-go for the observed full-window rows. There is no
review-safe basis here for a genuinely wider or more scalable replay path.
