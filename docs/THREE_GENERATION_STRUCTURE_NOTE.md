# Three-Generation Matter Structure Note

**Date:** 2026-04-14
**Status:** retained
**Scripts:** `scripts/frontier_generation_fermi_point.py`, `scripts/frontier_generation_rooting_undefined.py`, `scripts/frontier_generation_axiom_boundary.py`
**Authority role:** canonical main-branch note for the retained three-generation matter-structure row

## Safe statement

The framework retains a three-generation matter structure on the physical-lattice surface:

- the exact corner/orbit algebra gives `8 = 1 + 1 + 3 + 3`
- the three `hw=1` species are the lightest nonzero-mass species on `Z^3`
- rooting is not a well-defined operation in Hamiltonian `Cl(3)` on `Z^3`
- with the framework's physical-lattice axiom, the triplet sectors are treated
  as physical species structure rather than disposable taste artifacts

This is the safe retained statement used in the current paper package.

## Canonical derivation stack

1. `frontier_generation_fermi_point.py` establishes the exact spectral side:
   eight Brillouin-zone corners, Wilson mass by Hamming weight, and the exact
   `1 + 3 + 3 + 1` degeneracy structure with `C(3,1)=3`.
2. `frontier_generation_rooting_undefined.py` proves that no proper taste
   projection preserves the Hamiltonian `Cl(3)` structure; the triplet sectors
   cannot be removed by a legitimate rooting operation on this formulation.
3. `frontier_generation_axiom_boundary.py` isolates the only non-derived
   premise in the physical interpretation: once the lattice-is-physical axiom
   is accepted, the triplet sectors are physical species structure in the theory.

## Boundary

The retained statement is structural, not maximal:

- retained: physical three-generation structure in the framework
- retained: reviewer-facing physical-lattice / no-rooting boundary for the
  triplet sectors
- not retained: full quantitative flavor closure
- not retained: a first-principles `1+1+1` mass hierarchy
- not retained: a pure-spatial chiral-regulator theorem divorced from the
  anomaly-forced time step

That remaining work belongs to the CKM / flavor gate, not to the three-generation
closure itself.

For the clean reviewer-facing chirality / anti-rooting boundary, see
[THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md](./THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md).

## Validation

- [frontier_generation_fermi_point.py](./../scripts/frontier_generation_fermi_point.py)
- [frontier_generation_rooting_undefined.py](./../scripts/frontier_generation_rooting_undefined.py)
- [frontier_generation_axiom_boundary.py](./../scripts/frontier_generation_axiom_boundary.py)

Current main-branch runner state:

- `frontier_generation_fermi_point.py`: `EXACT PASS=7`, `BOUNDED PASS=1`
- `frontier_generation_rooting_undefined.py`: `PASS=37`, `FAIL=0`
- `frontier_generation_axiom_boundary.py`: `PASS=31`, `FAIL=0`
