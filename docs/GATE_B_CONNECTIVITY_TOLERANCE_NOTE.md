# Gate B Connectivity Tolerance Note

**Date:** 2026-04-04  
**Status:** bounded Gate B replay frozen on disk, not a dynamics theorem

## One-line read

The replay supports a narrow but useful claim:

- position noise on a fixed connectivity backbone is tolerated
- once connectivity is recomputed from geometry, the response becomes mixed

That makes connectivity structure the real bottleneck in the current Gate B
lane, but it does **not** close Gate B.

## Primary artifact

- Script: [`scripts/gate_b_connectivity_tolerance.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_connectivity_tolerance.py)
- Log: [`logs/2026-04-04-gate-b-connectivity-tolerance.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-gate-b-connectivity-tolerance.txt)

## What was compared

The replay keeps the same valley-linear propagation law fixed and compares a
small architecture set:

- ordered lattice baseline
- jittered lattice with fixed connectivity
- templated growth with fixed-offset connectivity
- K-NN grown geometry
- snapped/grid-like connectivity

The main readout in this replay is a mass-side detector-window gain. The
`F~M` column in the log is a local response-slope probe, not a promoted
universal theorem.

## Frozen replay result

| architecture | toward | mean delta | local `F~M` |
|---|---:|---:|---:|
| ordered lattice | `66.7%` | `+0.000012` | `0.66` |
| jittered lattice | `75.0%` | `+0.000005` | `0.75` |
| templated growth | `27.8%` | `-0.000016` | `0.27` |
| K-NN grown | `55.6%` | `+0.000006` | `0.55` |
| snapped/grid-like | `58.3%` | `-0.000002` | `0.58` |

The jitter sweep on fixed connectivity is the cleanest tolerance check:

| jitter | toward | mean delta | local `F~M` |
|---|---:|---:|---:|
| `0.00` | `66.7%` | `+0.000012` | `0.66` |
| `0.10` | `55.6%` | `+0.000003` | `0.55` |
| `0.20` | `66.7%` | `+0.000009` | `0.67` |
| `0.30` | `47.2%` | `-0.000010` | `0.47` |
| `0.40` | `50.0%` | `-0.000003` | `0.50` |
| `0.50` | `75.0%` | `+0.000005` | `0.75` |

## Safe interpretation

- A fixed connectivity backbone survives substantial position noise.
- Geometry-recomputed connectivity is the first place the response becomes
  mixed.
- The response does not show a cliff at jitter `0.5`; it degrades gradually.
- The local response-slope probe stays in a bounded linear-response band rather
  than collapsing.

## What this is not

- A solved Gate B dynamics theorem.
- A proof that any growth rule will work.
- A proof that the current `F~M` values are universal constants.
- A replacement for the existing bounded Gate B prototype notes.

## Why it matters

This replay makes the remaining Gate B gap sharper:

- position noise is not the main failure mode
- connectivity construction is

So the next useful growth rule is not “more jitter tolerance” but a rule that
produces structured connectivity without turning the graph into a hand-imposed
lattice.
