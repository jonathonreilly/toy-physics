# Generation Axiom Boundary Note

**Date:** 2026-04-16
**Status:** exact support theorem on the retained three-generation surface
**Script:** `scripts/frontier_generation_axiom_boundary.py`
**Authority role:** canonical main-branch tool note for the physical-lattice / taste-artifact boundary

## Safe statement

The framework's physical-lattice axiom is the exact boundary between:

- treating the `hw=1` triplet sectors as physical species structure
- treating them as removable taste artifacts

More precisely:

- with the physical-lattice axiom, the three-generation physicality chain closes
- without it, an explicit escape route remains through regulator-style interpretation
- that axiom is irreducible: it is not derivable from the other algebraic and dynamical axioms
- the newer
  [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
  now closes the narrower but important point that this regulator reading is
  **not** an equivalent reading of the same accepted framework stack

## Why this belongs in the toolbox

This is not just narrative framing. It is a reusable obstruction/support theorem
for any future lane that depends on the physical-lattice reading of the Brillouin-zone
species structure.

It is directly reusable for:

- three-generation defenses
- anti-rooting / physical-lattice arguments
- reviewer-facing taste-artifact objections
- future flavor and mass-hierarchy work that builds on the triplet sectors
- no-same-stack regulator-reinterpretation arguments

## Relation to the retained matter stack

This note supports but does not replace:

- [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md)
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
- [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)

Those notes carry the retained claim surfaces.
This note isolates the exact axiom boundary that makes the physical interpretation
clean and reusable.

The clean current division of labor is:

- this note:
  with-axiom / without-axiom boundary and irreducibility of the physical-lattice premise
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md):
  exact retained-generation no-proper-quotient theorem
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md):
  exact no-same-stack regulator reinterpretation closure, while keeping the
  physical-lattice premise itself explicit rather than derived

## Validation

- primary runner:
  [frontier_generation_axiom_boundary.py](./../scripts/frontier_generation_axiom_boundary.py)

Current main-branch runner state:

- `frontier_generation_axiom_boundary.py`: `PASS=31`, `FAIL=0`
