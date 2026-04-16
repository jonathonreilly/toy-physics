# Generation Axiom Boundary Note

**Date:** 2026-04-16
**Status:** exact support theorem on the retained three-generation surface and
the residual substrate-boundary question
**Script:** `scripts/frontier_generation_axiom_boundary.py`
**Authority role:** canonical main-branch tool note for the physical-lattice / taste-artifact boundary

## Safe statement

The framework's physical-lattice axiom is no longer the exact boundary between
the retained `hw=1` triplet and physical species semantics. That narrower point
now closes on the accepted Hilbert surface.

More precisely:

- exact observable separation + no-proper-quotient closure + accepted Hilbert
  semantics already force the retained `hw=1` triplet to be physically
  distinct species sectors of the accepted theory
- what remains explicit is the global substrate-level question of whether the
  lattice is fundamental rather than a regulator-family surrogate
- that substrate premise remains explicit on the current accepted stack: it is
  not yet derived from the other accepted algebraic and dynamical inputs
- the newer
  [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
  now closes the stronger retained-package point that this regulator reading is
  **not** an equivalent reading of the same accepted framework stack and that,
  once the retained matter closure plus live `alpha_s(v)`/`v` package are
  imposed, the physical-lattice reading is the unique surviving interpretation

## Why this belongs in the toolbox

This is not just narrative framing. It is a reusable obstruction/support theorem
for any future lane that depends on the physical-lattice reading of the Brillouin-zone
species structure.

It is directly reusable for:

- three-generation defenses
- anti-rooting / physical-lattice arguments
- reviewer-facing taste-artifact objections
- future flavor and mass-hierarchy work that builds on the triplet sectors
- no-same-stack / no-same-surface regulator-reinterpretation arguments

## Relation to the retained matter stack

This note supports but does not replace:

- [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md)
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
- [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)

Those notes carry the retained claim surfaces.
This note isolates the exact remaining boundary after the new semantics result
so the physical interpretation stays clean and reusable.

The clean current division of labor is:

- this note:
  residual substrate-boundary memo and the still-explicit status of the
  physical-lattice premise
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md):
  exact retained-generation no-proper-quotient theorem
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md):
  exact no-same-stack / no-same-surface regulator reinterpretation closure,
  exact retained observable-species semantics on the accepted Hilbert surface,
  plus retained-package conditional necessity, while keeping the
  substrate-level physical-lattice premise itself explicit rather than derived

## Validation

- primary runner:
  [frontier_generation_axiom_boundary.py](./../scripts/frontier_generation_axiom_boundary.py)

Current main-branch runner state:

- `frontier_generation_axiom_boundary.py`: `PASS=31`, `FAIL=0`;
  triplet physicality closed on the accepted Hilbert surface, residual
  explicit boundary narrowed to substrate-level physicality
