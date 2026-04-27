# Inverse Problem Graph Requirements Note

**Date:** 2026-04-04  
**Status:** bounded graph-requirements harness on the proposed_retained 3D valley-linear family

## Artifact chain

- Script: [`scripts/inverse_problem_graph_requirements.py`](/Users/jonreilly/Projects/Physics/scripts/inverse_problem_graph_requirements.py)
- Log: [`logs/2026-04-04-inverse-problem-graph-requirements.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-inverse-problem-graph-requirements.txt)

This note turns the earlier doc-only inverse-problem claim into a real,
bounded harness on the retained 3D valley-linear family.

The question is deliberately narrow:

- how much graph structure is actually required for Newton+Born to survive?

The tested perturbations are:

- baseline regular lattice
- 70% random edge deletion
- asymmetric graph with `z > 0` edges removed
- transverse jitter of node positions
- sparse NN-only connectivity

Controls included when cheap:

- `k = 0` with field on
- no-field with `k > 0`

## Safe read

The intended interpretation is bounded:

- if gravity stays TOWARD and Born stays machine-clean across a perturbation,
  then the graph is forgiving enough for existence on that slice
- if the `k = 0` and no-field controls stay near zero, then the phase-valley
  mechanism is doing the work, not an amplitude-only bias

That is the strongest safe version of the inverse-problem claim:

- graph structure controls precision and sign, not just magnitude
- field coupling and phase coupling are the core existence conditions
- the result is a bounded robustness / existence statement, not a universal
  theorem

The actual frozen run is mixed, and that is the important part:

- baseline, asymmetry, jitter, and sparse connectivity remain TOWARD
- the heavy 70% random edge-deletion row flips AWAY
- Born stays machine-clean on every tested perturbation
- `k = 0` and no-field controls stay at zero

So the inverse problem is not "almost any graph works" in the strong sense.
The honest conclusion is narrower:

- the retained family is robust to several natural perturbations
- but heavy edge deletion is too much and can reverse the sign
- the graph is still a real part of the story, even though it is not the main
  source of the mechanism

## Relation to the existing derivation notes

Read this with:

- [`docs/NEWTON_DERIVATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/NEWTON_DERIVATION_NOTE.md)
- [`docs/ACTION_UNIQUENESS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ACTION_UNIQUENESS_NOTE.md)
- [`docs/PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md)

The inverse problem is now narrower than the derivation:

- the derivation asks what selects the mass law
- this note asks what graph structure is minimally required for the already-
  selected valley-linear gravity to survive

## Best next move

The next honest step is to freeze the actual run of the harness and then decide:

- if the perturbations preserve gravity and Born, the graph is forgiving and
  the model really is a universality-class story
- if a perturbation breaks the effect, the requirement is more specific than
  the current doc-only note suggests

Either way, this note should stay bounded to the tested perturbation set.
