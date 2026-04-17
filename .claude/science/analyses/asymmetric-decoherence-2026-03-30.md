# Analysis: Asymmetric Decoherence

## Date
2026-03-30

## Key Finding: Delay-field distortion does NOT cause decoherence — even asymmetrically

V remains ~1.000 at y=0 and unchanged at all off-center positions for ALL p from 0.0 to 0.9, for both symmetric AND asymmetric field distortion, at cluster radii 1 and 2. Only p=1.0 (which changes the sector-labeling, not just the field) produces any visibility change.

## Why this happens

The interference visibility depends on the EXISTENCE of paths (topology) and their RELATIVE phase at the detector, not on the absolute amplitude/phase along each path. The phase sweep already covers all possible relative phases between the two slits. Changing the delay field modifies the amplitude and phase along individual edges, but:

1. Both sectors (recorded/free) traverse the SAME DAG (same path topology)
2. The phase sweep scans all relative phases anyway
3. Visibility = (max-min)/(max+min) of the phase sweep — invariant to path-independent amplitude rescaling

The delay-field distortion changes WHERE in the phase sweep the max/min occur, but not their ratio. This is because the distortion affects all paths through a given region equally (it's a field, not a path-specific perturbation).

## The broader insight: TOPOLOGICAL vs FIELD decoherence

The model has two ways to affect interference:
1. **Topology changes** (add/remove nodes, change the DAG) → MASSIVE effect (I₃ up to 10⁹, complete visibility destruction)
2. **Field changes** (modify delays/amplitudes on existing edges) → ZERO effect on visibility

This is because the model's interference is a TOPOLOGICAL property of the causal DAG. The field determines quantitative details (which phase gives the max, how much probability reaches each detector position) but the interference structure (whether V=0 or V>0) is purely topological.

This is a distinctly discrete-network finding: on a continuous manifold, any local perturbation can destroy interference. On a discrete causal DAG, only topological changes matter.

## Hypothesis Verdict
**REFUTED** — asymmetric delay-field distortion does not produce non-trivial decoherence. Decoherence in this model requires topological DAG changes, not field perturbations.

## Significance
This establishes a clean separation: interference = topology, gravity = field. The two mechanisms are INDEPENDENT on a fixed DAG. Records that only distort the field cannot cause decoherence; records must change the DAG structure itself. This constrains what kind of record mechanism could produce decoherence in the model.
