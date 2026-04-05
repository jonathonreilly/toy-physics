# Graph Phase-Diagram Scout Note

**Date:** 2026-04-05  
**Status:** bounded phase-diagram scout on the retained 3D valley-linear family

## Artifact chain

- Script: [`scripts/graph_phase_diagram_scout.py`](/Users/jonreilly/Projects/Physics/scripts/graph_phase_diagram_scout.py)
- Log: [`logs/2026-04-05-graph-phase-diagram-scout.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-graph-phase-diagram-scout.txt)

## Question

Which observable fails first under bounded graph perturbations on the retained
3D valley-linear family?

The three observables tracked here are:

- sign
- Born
- exponent fidelity

The perturbation families are intentionally small:

- baseline
- asymmetric `z > 0` edge removal
- transverse jitter
- sparse NN-only connectivity
- a short edge-deletion ladder

The retained family and thresholds are fixed:

- `h = 0.5`
- `W = 8`
- `L = 12`
- Born threshold `<= 1e-12`
- exponent fidelity threshold `|F~M - 1| <= 0.05`

## Frozen result

The frozen table in the log file shows:

- baseline: sign TOWARD, Born machine-clean, `F~M = 1.000`
- asymmetry: sign TOWARD, Born machine-clean, `F~M = 1.000`
- jitter: sign TOWARD, Born machine-clean, `F~M = 1.000`
- sparse NN: sign TOWARD, Born machine-clean, `F~M = 1.000`
- delete 10%: sign TOWARD, Born machine-clean, `F~M = 1.000`
- delete 20%: sign TOWARD, Born machine-clean, `F~M = 1.000`
- delete 30%: sign TOWARD, Born machine-clean, `F~M = 1.000`
- delete 50%: sign TOWARD, Born machine-clean, `F~M = 1.000`
- delete 70%: sign flips AWAY, Born still machine-clean, exponent fit no longer survives the sign collapse

So in this bounded sweep:

- **sign fails first**
- **Born does not fail**
- **exponent fidelity survives until the sign collapse and then becomes unavailable**

## Safe interpretation

The retained 3D family is forgiving under moderate perturbations:

- baseline, asymmetry, jitter, sparse connectivity, and moderate edge deletion
  all preserve the sign, Born, and `F~M` fidelity

The first hard boundary in this scout ladder is the sign boundary:

- heavy `70%` edge deletion is where the TOWARD row flips AWAY in this short ladder
- Born remains clean on the same row

Important reconciliation with the retained boundary sweep:

- the separate retained `0.75-1.00` edge-deletion sweep on the same family did **not** reproduce a sign flip
- that sweep stayed TOWARD all the way down to `75%` retained edges
- so the `delete_70` failure here is best read as a broader-ladder boundary effect, not as a stable threshold for the retained family

That means the graph is still a real part of the story, but the earliest
observable to give way is sign, not Born.

## Recommendation

The concrete next hardening lane is:

- **a harsher damage ladder or a different graph family**

Why this lane:

- it is the first observable boundary exposed by the scout ladder
- the retained `0.75-1.00` sweep already showed that this is not a stable threshold on the same family
- a harsher ladder or another family is now the honest way to test whether the sign flip is real or family-specific

## Relation to the existing graph notes

Read this with:

- [`docs/INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/INVERSE_PROBLEM_GRAPH_REQUIREMENTS_NOTE.md)
- [`docs/BROKEN_GRAPH_ACTION_POWER_ROBUSTNESS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/BROKEN_GRAPH_ACTION_POWER_ROBUSTNESS_NOTE.md)
- [`docs/EDGE_DELETION_BOUNDARY_SWEEP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/EDGE_DELETION_BOUNDARY_SWEEP_NOTE.md)

Those notes established that the graph is forgiving but not irrelevant.
This scout narrows that further:

- sign can fail first in a short, harsher ladder
- Born remains machine-clean on the same rows
- the retained `0.75-1.00` boundary sweep does not support a stable sign-flip threshold on this family
