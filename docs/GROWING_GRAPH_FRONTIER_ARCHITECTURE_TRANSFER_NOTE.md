# Growing Graph Frontier Architecture Transfer Note

**Date:** 2026-04-06  
**Status:** retained architecture lesson for the current graph-growth cleanup lane

## Artifact Chain

- [`docs/GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md)
- [`docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md)
- [`docs/INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md)
- [`docs/GROWING_GRAPH_FRONTIER_EXPANSION_PROXY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GROWING_GRAPH_FRONTIER_EXPANSION_PROXY_NOTE.md)
- [`docs/GROWING_GRAPH_DYNAMIC_LIMIT_DIAGNOSTIC_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GROWING_GRAPH_DYNAMIC_LIMIT_DIAGNOSTIC_NOTE.md)

## Purpose

This note answers one narrow question:

- does the early graph-ladder / Gate B architecture work apply to the current
  graph-growth cleanup lane?

The answer is yes, but only in a very specific way.

## What Transfers

The old graph-ladder work says the same thing in several places:

- [`docs/GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md)
- [`docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md)
- [`docs/INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md)

The transferable lessons are:

1. **Connectivity construction is the bottleneck.**
   - fixed connectivity survives position noise better than recomputed geometry
   - naive KNN+floor rules can kill the far-field package
   - geometry-sector or other structured local rules can do better than pure KNN,
     but only on the tested family

2. **Sign is the first real boundary.**
   - the graph phase-diagram scout says sign fails before Born on the harsher
     ladders
   - that means the graph-growth story should keep a signed-frontier observable,
     not just a transport amplitude

3. **The old ladder is a design guide, not a universal transfer theorem.**
   - it suggests where to spend effort
   - it does not rescue the current fixed `h = 0.125` continuum bridge
   - it does not turn the dynamic propagation lane into a clean order parameter

## What Does Not Transfer

The early ladder work does **not** justify:

- a de Sitter or cosmology headline
- a transport/decoherence derivation from dynamic propagation
- a universal graph theorem
- a rescue of the closed fixed-family `h = 0.125` bridge

The current dynamic-propagation diagnostic already shows why:

- frontier delay is the retained expansion observable
- dynamic propagation is noisy, seed-dependent, and not monotone

## Current Applied Lesson

For the present graph-growth cleanup lane, the old architecture work should be
used like this:

- keep frontier-delay growth as the headline observable
- treat dynamic-propagation repair as a bounded no-go unless it beats the static
  control cleanly
- if a new connectivity rule is proposed, compare it against the old lessons:
  - does it preserve the signed far-field package?
  - does it survive a static-control audit?
  - does it beat KNN/floor or just rename the bottleneck?

## Final Verdict

**old graph-ladder architecture applies as a connectivity-design guide, not as a rescued transport law**
