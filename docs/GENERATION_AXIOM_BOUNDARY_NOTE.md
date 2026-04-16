# Generation Axiom Boundary Note

**Date:** 2026-04-15
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
- the exact retained-generation theorem separately removes the remaining
  generation-surface reduction loophole
- that axiom is irreducible: it is not derivable from the other algebraic and dynamical axioms

## Why this belongs in the toolbox

This is not just narrative framing. It is a reusable obstruction/support theorem
for any future lane that depends on the physical-lattice reading of the Brillouin-zone
species structure.

It is directly reusable for:

- three-generation defenses
- anti-rooting / physical-lattice arguments
- reviewer-facing taste-artifact objections
- future flavor and mass-hierarchy work that builds on the triplet sectors

What it now does **not** need to carry alone is the retained-generation
no-proper-quotient argument. That exact retained-surface statement is now
handled separately by
[THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md).

## Relation to the retained matter stack

This note supports but does not replace:

- [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md)
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
- [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)

Those notes carry the retained claim surfaces.
This note isolates the exact axiom boundary that makes the physical interpretation
clean and reusable.

## Current division of labor

The current package cleanly splits the problem into two layers:

- **Exact retained-generation layer:**
  the `hw=1` triplet carries an exact irreducible retained generation algebra,
  so no proper exact quotient / rooting / reduction survives on that retained
  surface.
- **Global framework boundary:**
  whether those retained sectors are interpreted as physical species structure
  or as removable regulator artifacts still turns on the physical-lattice
  premise isolated by this note.

So the remaining open question is no longer a generation-surface reduction
loophole. It is the global physical-lattice premise itself.

For the current theorem attempt on that remaining question, see
[PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md).

## Validation

- primary runner:
  [frontier_generation_axiom_boundary.py](./../scripts/frontier_generation_axiom_boundary.py)

Current main-branch runner state:

- `frontier_generation_axiom_boundary.py`: `PASS=31`, `FAIL=0`
