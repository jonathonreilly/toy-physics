# Wilson Partner-Source Crossover Note

**Date:** 2026-04-11  
**Status:** bounded-retained candidate on frontier; not yet promoted  
**Scripts:**  
- `frontier_wilson_two_body_open.py`
- `frontier_wilson_two_body_laws.py`
- `frontier_wilson_partner_source_crossover.py`

## Question

The open-lattice Wilson two-body lane already shows a clean monotone partner-
source law on the audited `side=13, d=4, G=5, mu^2=0.22` surface:

- `|a_mut| ~ m_B^0.483`
- `R^2 = 0.9363`

The question here is whether that sublinear exponent bends toward linear
(`alpha -> 1`) on:

- larger open surfaces
- different separations
- a smaller `G` window

## Scan Surface

The crossover scan used the open 3D Wilson lattice only.

Surface:

- `side = 13, 15, 17`
- `G = 2, 3, 5`
- `d = 3, 4, 5, 6`
- `mu^2 = 0.22`
- `m_B = 0.5, 1.0, 1.5, 2.0, 3.0`

Observable:

- early-time mutual acceleration from `SHARED - SELF_ONLY`

Fit criterion:

- clean attractive rows only
- power law `|a_mut| ~ m_B^alpha`

## Result

Every scanned configuration remained attractive and clean.

Aggregate fit summary:

- clean fits found: `36/36`
- best clean fit: `side=13, G=2, d=3`
  - `alpha = 0.314`
  - `R^2 = 0.9962`
- alpha range across clean fits:
  - min `0.071`
  - max `0.594`
  - mean `0.419`

Representative fixed-separation behavior:

- `d=4` stays around `alpha ~ 0.42-0.48` across the open surfaces
- larger separations can push `alpha` upward somewhat
- but even the largest clean exponents remain well below `1`

## Interpretation

The open Wilson partner-source dependence is:

- monotone
- robust on larger open surfaces
- still clearly **sublinear**

So the better-surface scan does **not** show a crossover toward linear mass
scaling. The surface refinement improves cleanliness, but not the exponent
class.

Current best statement:

> On open 3D Wilson lattices, the mutual-attraction channel remains
> sublinear in partner source strength across `side=13,15,17` and
> `G=2,3,5`, with clean fits spanning `alpha=0.071-0.594` and a best clean
> fit of `alpha=0.314`.

## Guardrail

This note intentionally avoids `frontier_wilson_newton_law.py`. That script
still wraps a periodic box and is not a valid test of the open-lattice
surface.
