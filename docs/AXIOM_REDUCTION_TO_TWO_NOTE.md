# Dimension Selection Support Theorem: d = 3 Squeeze

**Date:** 2026-04-16
**Status:** BOUNDED-RETAINED SUPPORT — does not replace front-door framing
**Related:** `AXIOM_REDUCTION_NOTE.md`, `DIMENSION_SELECTION_NOTE.md`,
`BOUND_STATE_SELECTION_NOTE.md`

## What this note is

A bounded support theorem showing that d = 3 is the unique spatial
dimension passing two independent on-lattice tests. This is useful
supporting evidence for the framework, but it does **not** replace the
live front-door framing.

## What this note is NOT

This note does **not** promote the public axiom framing to "two axioms."
The live front-door statement remains:

> We take `Cl(3)` on `Z^3` as the physical theory. Everything else is
> derived.

This is a one-axiom program on the accepted physical surface. The
`Cl(3)` on `Z^3` statement carries specific accepted structure:

1. the local algebra `Cl(3)`,
2. the cubic substrate `Z^3`,
3. microscopic dynamics on that surface,
4. the canonical normalization and evaluation surface.

These are not individually rederived from a more primitive "graph +
unitarity" pair in the current live package. The decomposition
A1 (graph) + A2 (unitarity) + C1 (d=3) in `AXIOM_REDUCTION_NOTE.md` is
a useful internal anatomy, but the public presentation is the accepted
one-axiom surface, not the decomposed version.

## The d = 3 squeeze (bounded support)

Within the family of d-dimensional lattice tests, the framework's own
self-consistency requirements pin d = 3 from two sides:

### Lower bound: d >= 3

**Source:** `DIMENSION_SELECTION_NOTE.md`, `frontier_dimension_selection.py`

Self-consistent propagator + gravitational field on d-dimensional lattices:

| d | Attractive gravity? | Mass law beta | Status |
|---|---|---|---|
| 1 | NO | 0.18 | excluded |
| 2 | NO | 0.27 | excluded |
| 3 | YES | 1.01 | passes |
| 4 | YES | 1.05 | passes |
| 5 | YES | 1.03 | passes |

The propagator phase coupling S = L(1 - phi) produces attractive
deflection only when the Poisson potential decays with distance, which
requires d >= 3. This step is cleanly on-lattice.

### Upper bound: d <= 3

**Source:** `BOUND_STATE_SELECTION_NOTE.md`, `frontier_bound_state_selection.py`

The d-dimensional Coulomb potential on a lattice Hamiltonian:

| d | Bound states | Stable atoms? |
|---|---|---|
| 2 | infinite (confining) | yes, but 2D |
| 3 | 8 (Rydberg series) | YES |
| 4 | 1 (marginal, fall-to-center) | NO |
| 5 | 0 | NO |

d = 3 is the unique dimension with a finite Rydberg series supporting
stable atomic bound states.

### Status of the upper bound

The spectral result (no stable bound states for d >= 4) is a real
on-lattice calculation. However, the decisive move is the admissibility
statement: if the framework's Hamiltonian has no stable bound states,
then there are no particles and no physics.

This is a reasonable framework-admissibility criterion — better described
as a **matter-support boundary theorem** than as a bare consequence of
A1 + A2. It is not anthropic in the casual sense, but it is a criterion
layered on top of the spectral calculation, not a pure derivation from
the two primitive inputs alone.

### Combined

```
Self-consistent gravity:  d >= 3
Stable bound states:      d <= 3
                          --------
                          d = 3 uniquely
```

This is a support squeeze, not a front-door derivation.

## What this means for the axiom count

The live front-door axiom count does not change:

| Framing | Statement | Status |
|---------|-----------|--------|
| **Public / front-door** | `Cl(3)` on `Z^3` (one axiom) | **current, unchanged** |
| Internal anatomy | A1 (graph) + A2 (unitarity) + C1 (d=3) | descriptive |
| This note | d = 3 has bounded on-lattice support | support theorem |

The d = 3 squeeze is interesting and may eventually contribute to a
stronger foundational claim, but the current live derivation stack does
not rederive the full accepted `Cl(3)` on `Z^3` surface from "graph +
unitarity" alone. Promoting to "two axioms, zero choices" would outrun
the current package.

## Boundary

This note is a bounded support theorem for dimension selection. It:

- does NOT replace the front-door framing
- does NOT change the public axiom count
- does NOT promote any claim beyond bounded-retained support
- DOES provide on-lattice evidence that d = 3 is uniquely selected
  by the framework's self-consistency requirements
- DOES identify the matter-support admissibility criterion as the
  remaining gap between "support" and "derivation"

## Reproducibility

```
python3 scripts/frontier_dimension_selection.py
python3 scripts/frontier_bound_state_selection.py
```
