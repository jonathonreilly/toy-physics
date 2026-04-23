# Three-Generation Matter Structure Note

**Date:** 2026-04-15
**Status:** retained
**Scripts:** `scripts/frontier_generation_fermi_point.py`, `scripts/frontier_generation_rooting_undefined.py`, `scripts/frontier_generation_axiom_boundary.py`, `scripts/frontier_three_generation_observable_theorem.py`
**Authority role:** canonical main-branch note for the retained three-generation matter-structure row

## Safe statement

The framework retains a three-generation matter structure on the physical-lattice surface:

- the exact corner/orbit algebra gives `8 = 1 + 1 + 3 + 3`
- the three `hw=1` species are the lightest nonzero-mass species on `Z^3`
- rooting is not a well-defined operation in Hamiltonian `Cl(3)` on `Z^3`
- the retained `hw=1` triplet carries an exact irreducible retained generation
  algebra, so no proper exact quotient survives on that surface
- exact observable-sector semantics on the accepted Hilbert surface already
  force the retained `hw=1` triplet to be physically distinct species
  structure within the accepted theory
- on the accepted one-axiom Hilbert/locality/information surface, the
  substrate-level physical-lattice reading is also derived rather than carried
  as a separate live premise

This is the safe retained statement used in the current paper package.

## Canonical derivation stack

1. `frontier_generation_fermi_point.py` establishes the exact spectral side:
   eight Brillouin-zone corners, Wilson mass by Hamming weight, and the exact
   `1 + 3 + 3 + 1` degeneracy structure with `C(3,1)=3`.
2. `frontier_generation_rooting_undefined.py` proves that no proper taste
   projection preserves the Hamiltonian `Cl(3)` structure; the triplet sectors
   cannot be removed by a legitimate rooting operation on this formulation.
3. `frontier_three_generation_observable_theorem.py` proves that the retained
   `hw=1` triplet already carries the full exact retained generation algebra
   `M_3(C)`, so no proper exact quotient exists even before flavor.
4. `frontier_physical_lattice_necessity.py` now closes the narrower but
   important semantics step that exact observable separation + no proper exact
   quotient + accepted Hilbert semantics already force the retained `hw=1`
   triplet to be physically distinct species sectors of the accepted theory.
5. `frontier_generation_axiom_boundary.py` is now retained only as the
   reduced-stack witness showing why the older five-item memo listed the
   substrate premise explicitly.
6. `frontier_physical_lattice_necessity.py` also closes the fixed-stack/fixed-surface
   boundary result that regulator reinterpretation is not an equivalent reading
   of the same accepted framework stack and cannot preserve the accepted fixed
   quantitative surface; it also closes the stronger statement that no
   nontrivial regulator-style family preserves both accepted live invariants
   `alpha_s(v)` and `v`, and therefore that the physical-lattice reading is
   forced once the retained package contract is imposed. On the accepted
   one-axiom Hilbert/locality/information surface it goes further and derives
   the substrate-level physical-lattice reading itself.

## Boundary

The retained statement is structural, not maximal:

- retained: physical three-generation structure in the framework
- retained: no-proper-quotient theorem on the retained `hw=1` generation surface
- retained: public physical-lattice / no-rooting boundary for the
  triplet sectors
- not retained: a first-principles `1+1+1` mass hierarchy
- not retained: a pure-spatial chiral-regulator theorem divorced from the
  anomaly-forced time step

The remaining open work now belongs to:

- stronger theorem packaging of the one-axiom substrate-necessity result if we
  ever want to move it from support theorem to public theorem box
- generation hierarchy / flavor structure
- full chirality / mass-spectrum tasks beyond the retained generation surface

For the clean public chirality / anti-rooting boundary, see
[THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md](./THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md).
For the exact retained-generation algebra theorem, see
[THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md).
For the exact no-same-stack / no-same-surface regulator reinterpretation
closure, see
[PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md).

## Validation

- [frontier_generation_fermi_point.py](./../scripts/frontier_generation_fermi_point.py)
- [frontier_generation_rooting_undefined.py](./../scripts/frontier_generation_rooting_undefined.py)
- [frontier_generation_axiom_boundary.py](./../scripts/frontier_generation_axiom_boundary.py)
- [frontier_three_generation_observable_theorem.py](./../scripts/frontier_three_generation_observable_theorem.py)
- [frontier_physical_lattice_necessity.py](./../scripts/frontier_physical_lattice_necessity.py)

Current main-branch runner state:

- `frontier_generation_fermi_point.py`: `EXACT PASS=7`, `BOUNDED PASS=1`
- `frontier_generation_rooting_undefined.py`: `PASS=37`, `FAIL=0`
- `frontier_generation_axiom_boundary.py`: `PASS=31`, `FAIL=0`
- `frontier_three_generation_observable_theorem.py`: `PASS=47`, `FAIL=0`
- `frontier_physical_lattice_necessity.py`: closed no-same-stack /
  no-same-surface regulator reinterpretation; triplet species semantics forced
  on the accepted Hilbert surface; substrate physicality forced on the
  accepted one-axiom framework surface
