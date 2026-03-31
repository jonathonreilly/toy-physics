# Write-Up: Decoherence Mechanisms in the Discrete Event-Network Model

## Abstract

We systematically tested four candidate decoherence mechanisms for the model's two-slit interference setup: trivial amplitude splitting (sector labels), symmetric delay-field distortion, asymmetric delay-field distortion, and topological DAG modification (shortcut edges). Only sector labeling and topological modification produce any visibility change. The key structural finding is that interference in this model is a TOPOLOGICAL property of the causal DAG — field perturbations on a fixed topology have zero decoherence effect. Topological records produce non-trivial V(p) ≠ V₀(1-p), with the surprising feature that DAG shortcuts can INCREASE visibility by rebalancing per-slit amplitude contributions.

## Results Summary

| Mechanism | V(p) law | Effect |
|-----------|---------|--------|
| Sector labels (trivial) | V₀(1-p) exactly | Linear decoherence, mathematically guaranteed |
| Symmetric field distortion | V unchanged | Zero effect — field preserves relative phase |
| Asymmetric field distortion | V unchanged | Zero effect — same DAG, same topology |
| Topological shortcuts (both slits) | V increases with p | DAG pruning equalizes amplitude balance |
| Topological shortcuts (one slit) | V(y=0) decreases, V(y=3) increases | Position-dependent, breaks symmetry |

## The Structural Principle

**Interference = Topology.** The model's interference structure is determined entirely by which paths exist on the causal DAG (topology), not by the amplitudes or phases along those paths (field). This is because:

1. The phase sweep already explores all relative phases between paths
2. Visibility = (max-min)/(max+min) is invariant to field-induced amplitude rescaling
3. Only changes to path EXISTENCE (adding/removing DAG edges) alter visibility

**Gravity = Field.** The delay-field distortion changes action values and path shapes but not the interference pattern. Gravity and interference are independent mechanisms on a fixed DAG.

## The Decoherence Constraint

For a record mechanism to produce decoherence in this model, it MUST change the causal DAG topology. Records that only create sector labels (amplitude splitting) give trivial linear decoherence. Records that only distort the delay field give zero decoherence. Only records that modify which events are causally connected can produce non-trivial decoherence.

This constrains the model's interpretation of Axiom 9 ("measurement is durable record formation that separates alternatives"): the "separation" must be TOPOLOGICAL — the record must change the causal structure of the network, not just tag paths with labels.

## Per-Slit Amplitude Analysis

The V-increase from topological shortcuts is explained by amplitude rebalancing:
- Normal DAG at y=3: far slit contributes 16.5% of near slit's amplitude
- Shortcut DAG at y=3: far slit contributes 50.2% of near slit's amplitude

More balanced amplitudes → higher fringe contrast. The shortcuts speed up arrival times, causing the DAG to prune 81 edges and add 39 (net -42). The pruning removes paths that were diluting the interference pattern — analogous to spatial filtering in optics.

## Open Questions

1. Can the model produce GENUINE decoherence (V decreasing monotonically with record strength) via topology changes that specifically destroy amplitude balance?
2. Is the interference=topology principle a consequence of the linear path-sum, or would it survive in a nonlinear generalization?
3. What is the physical interpretation of DAG-topology-changing records? In the model's language, these are records that change which events are causally accessible — a strong form of "separating alternatives."
