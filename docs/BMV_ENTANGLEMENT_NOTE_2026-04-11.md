# Branch-Mediated Entanglement on a Staggered Lattice

## Status

`bounded companion`

## Script

- `/Users/jonreilly/Projects/Physics/scripts/frontier_bmv_entanglement.py`

## Rerun

Rerun on 2026-04-11 in the physics venv:

| G | overlap_1 | overlap_2 | product_overlap | S_quantum (nats) | S_mix (nats) | delta_S (nats) |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.9804 | 0.9925 | 0.9730 | 0.07148 | 0.05509 | 0.01639 |
| 2 | 0.9270 | 0.9696 | 0.8988 | 0.20024 | 0.15669 | 0.04355 |
| 5 | 0.6719 | 0.8211 | 0.5517 | 0.53208 | 0.44630 | 0.08579 |
| 10 | 0.2435 | 0.4336 | 0.1056 | 0.68756 | 0.66320 | 0.02437 |
| 20 | 0.1831 | 0.2836 | 0.0519 | 0.69180 | 0.67629 | 0.01550 |
| 50 | 0.0967 | 0.2419 | 0.0234 | 0.69287 | 0.68847 | 0.00441 |

Norms stayed at `1.0000` for all four branch states at every tested `G`.

Peak entanglement:

- `S_quantum = 0.69287` nats at `G=50`
- `0.99961` bits
- `99.96%` of the two-branch maximum `ln(2)`

## Strongest Honest Interpretation

This script shows a strong **branch-mediated entanglement signal** on a
fixed-adjacency staggered-lattice protocol with an externally imposed
two-branch source configuration.

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

## Retained Claim

The retained claim is:

> On a 2D staggered lattice with a fixed externally imposed geometry-branch superposition, the shared branch coherently entangles two separated particles beyond the corresponding classical branch mixture, with `delta_S > 0` for all tested couplings and `S_quantum` saturating near `ln(2)`.

## Why Keep It

- Strong, clean signal with exact norm conservation.
- Useful bridge between the earlier geometry-superposition work and any future fully dynamical two-particle / self-generated branch protocol.
- Narrow enough to survive scrutiny.
