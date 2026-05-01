# Branch-Mediated Entanglement on a Staggered Lattice

**Status:** bounded - bounded or caveated result note
## Status

`bounded companion`

## Script

- `/Users/jonreilly/Projects/Physics/scripts/frontier_bmv_entanglement.py`

## Rerun

Corrected minimum-image rerun on `2026-04-18` in the physics venv:

| G | overlap_1 | overlap_2 | product_overlap | S_quantum (nats) | S_mix (nats) | delta_S (nats) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.9805 | 0.9933 | 0.9740 | 0.06946 | 0.05476 | 0.01470 |
| 2 | 0.9274 | 0.9730 | 0.9023 | 0.19510 | 0.15605 | 0.03905 |
| 5 | 0.6722 | 0.8422 | 0.5662 | 0.52296 | 0.44604 | 0.07692 |
| 10 | 0.2369 | 0.5079 | 0.1203 | 0.68589 | 0.66482 | 0.02107 |
| 20 | 0.2111 | 0.1189 | 0.0251 | 0.69283 | 0.67069 | 0.02214 |
| 50 | 0.1258 | 0.0904 | 0.0114 | 0.69308 | 0.68521 | 0.00787 |

Norms stayed at `1.0000` for all four branch states at every tested `G`.

Peak entanglement:

- `S_quantum = 0.69308` nats at `G=50`
- `0.99991` bits
- `99.99%` of the two-branch maximum `ln(2)`

## Strongest Honest Interpretation

This corrected periodic rerun preserves a strong **branch-mediated
entanglement signal** on a fixed-adjacency staggered-lattice protocol with an
externally imposed two-branch source configuration.

- A shared geometry branch `(source present, source absent)` is imposed externally.
- Each particle evolves coherently under both branches.
- The quantum branch superposition yields larger reduced entropy than the corresponding classical branch mixture: `delta_S > 0` for every tested `G`.
- The signal grows monotonically in `S_quantum` over the tested sweep and saturates near the two-branch maximum.

That is a real positive result.

## What It Does Not Show

This is **not** a full Bose-Marletto-Vedral witness.

Reasons:

- The geometry/source superposition is inserted by hand rather than generated dynamically by the particles' own mass branches.
- The script does not implement the full local-operations-and-classical-communication exclusion logic used in BMV-style claims.
- The result is therefore a **branch-mediated entanglement witness on an externally imposed two-branch protocol**, not a standalone proof that gravity must be quantum.

## Bounded Claim

The live bounded claim is:

> On a 2D staggered lattice with a fixed externally imposed geometry-branch superposition, the shared branch coherently entangles two separated particles beyond the corresponding classical branch mixture, with `delta_S > 0` for all tested couplings and `S_quantum` saturating near `ln(2)`.

## Why Keep It

- Strong, clean signal with exact norm conservation.
- Useful bridge between the earlier geometry-superposition work and any future fully dynamical two-particle / self-generated branch protocol.
- Narrow enough to survive scrutiny.
