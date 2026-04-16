# Three-Generation / Chirality Boundary Note

**Date:** 2026-04-15
**Status:** retained support note on `main`
**Scripts:** `scripts/frontier_generation_fermi_point.py`,
`scripts/frontier_generation_rooting_undefined.py`,
`scripts/frontier_three_generation_observable_theorem.py`,
`scripts/frontier_generation_axiom_boundary.py`,
`scripts/frontier_anomaly_forces_time.py`
**Authority role:** canonical reviewer-facing support note for the
three-generation / chirality boundary on the current package surface

## Safe statement

The framework's retained matter claim is:

- exact `8 = 1 + 1 + 3 + 3` orbit structure on the physical `Z^3` surface
- the `hw = 1` triplet is retained as physically distinct species structure on
  the accepted Hilbert surface
- rooting is not a well-defined operation in Hamiltonian `Cl(3)` on `Z^3`
- the retained `hw=1` triplet already carries an exact irreducible generation
  algebra, so no proper exact quotient survives on that retained surface
- chirality is not claimed on the purely spatial surface by itself; it enters
  only in the full framework through anomaly-forced time and the resulting
  one-generation right-handed completion

This is the safe reviewer-facing boundary for the current paper.

## What the framework is and is not claiming

### Claimed

1. The Brillouin-zone corner algebra is exact and gives `1 + 1 + 3 + 3`.
2. On the accepted Hilbert surface, exact observable separation plus
   no-proper-quotient closure already force the retained `hw=1` triplet to be
   physically distinct species structure.
3. In this Hamiltonian `Cl(3)` formulation, rooting / taste-removal is
   undefined as an allowed operation.
4. On the retained generation surface, the exact operator algebra is
   irreducible, so no proper exact quotient exists even before flavor.
5. The full-framework chirality claim is carried by anomaly-forced time and
   the one-generation matter-closure theorem, not by a purely spatial
   projection argument.
6. Regulator reinterpretation is not an equivalent reading of the same
   accepted framework stack; it requires extra continuum / rooting /
   renormalization structure not present in that stack.

### Not claimed

1. A conventional fourth-root resolution inside regulator staggered LQCD.
2. A theorem that a purely spatial local chiral lattice regulator evades
   Nielsen-Ninomiya on its usual hypothesis surface.
3. A full axiom-internal removal of the substrate-level physical-lattice premise.
4. A full flavor-hierarchy or mass-spectrum closure from the generation note
   alone.

## Reviewer-facing interpretation

The clean response to the usual rooting / Nielsen-Ninomiya objection is:

- the project does **not** claim that a conventional regulator lattice with
  doublers has been repaired by a legal rooting trick
- instead, the project takes the lattice as physical
- on that physical-lattice surface, the triplet sectors are retained as
  species structure because rooting is undefined in the Hamiltonian `Cl(3)`
  formulation and because the retained `hw=1` generation algebra itself admits
  no proper exact quotient
- chirality is then supplied in the full framework by anomaly-forced time and
  anomaly cancellation, not by pretending the purely spatial `Z^3` surface is
  already a finished chiral continuum regulator

So the current package is not claiming a loophole in the usual no-go theorem.
It is claiming a different theory surface.

## Canonical support stack

1. [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md)
   carries the retained three-generation claim itself.
2. [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
   carries the exact retained-generation no-proper-quotient theorem.
3. [GENERATION_AXIOM_BOUNDARY_NOTE.md](./GENERATION_AXIOM_BOUNDARY_NOTE.md)
   isolates the physical-lattice axiom boundary.
4. [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
   closes the no-same-stack / no-same-surface regulator reinterpretation
   boundary, closes the narrower observable-species semantics step on the
   accepted Hilbert surface, and also the stronger loophole that a nontrivial
   regulator-style family could preserve both accepted live invariants
   `alpha_s(v)` and `v`, so on the retained package contract the
   physical-lattice reading is forced as the unique surviving interpretation,
   while keeping the substrate-level physical-lattice premise itself explicit.
5. [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
   carries the full-framework chirality / right-handed completion claim.
6. [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)
   supplies the single-clock `3+1` and chirality step.

## Paper-safe wording

> The framework retains a three-generation matter structure on the physical
> lattice surface. The exact Brillouin-zone orbit algebra gives `8 = 1 + 1 + 3
> + 3`; rooting is not a well-defined operation in Hamiltonian `Cl(3)` on
> `Z^3`; and the retained `hw=1` triplet already carries an exact irreducible
> generation algebra, so no proper exact quotient survives on that retained
> surface. Exact translation observables therefore separate the triplet sectors
> as physically distinct species on the accepted Hilbert surface. Regulator
> reinterpretation is not an equivalent reading of the same accepted framework
> stack because it requires extra continuum/rooting/RG structure not present
> there. The still-explicit premise is the substrate-level physical-lattice
> reading, not the triplet-species semantics themselves. Chirality is not
> claimed on the pure spatial surface alone, but in the full framework through
> anomaly-forced time and the one-generation matter-closure theorem.

## Validation

- [frontier_generation_fermi_point.py](./../scripts/frontier_generation_fermi_point.py)
- [frontier_generation_rooting_undefined.py](./../scripts/frontier_generation_rooting_undefined.py)
- [frontier_three_generation_observable_theorem.py](./../scripts/frontier_three_generation_observable_theorem.py)
- [frontier_generation_axiom_boundary.py](./../scripts/frontier_generation_axiom_boundary.py)
- [frontier_physical_lattice_necessity.py](./../scripts/frontier_physical_lattice_necessity.py)
- [frontier_anomaly_forces_time.py](./../scripts/frontier_anomaly_forces_time.py)

Current main-branch runner state:

- `frontier_generation_fermi_point.py`: `EXACT PASS=7`, `BOUNDED PASS=1`
- `frontier_generation_rooting_undefined.py`: `PASS=37`, `FAIL=0`
- `frontier_three_generation_observable_theorem.py`: `PASS=47`, `FAIL=0`
- `frontier_generation_axiom_boundary.py`: `PASS=31`, `FAIL=0`
- `frontier_physical_lattice_necessity.py`: closed no-same-stack /
  no-same-surface regulator reinterpretation; residual premise necessity still
  explicit
