# Investigation: 1-Node Zero-Effect in Gravity Sweep

## Date
2026-03-30

## Anomaly
A single persistent node at (10, 4) produces zero deflection AND zero action change — identical to the free (no persistent nodes) case. 2+ adjacent nodes produce immediate strong effects.

## Hypotheses Tested

### 1. Bug: derive_local_rule ignores single nodes
Evidence for: None — derive_local_rule stores persistent_nodes faithfully.
Evidence against: The function passes nodes through without filtering.
Verdict: RULED OUT

### 2. Artifact: Persistence support requires neighbor connectivity
Evidence for: `derive_persistence_support()` line 2694 computes:
`support[node] = sum(neighbor in active_nodes for neighbor in neighbors) / len(neighbors)`
A single node has zero persistent neighbors → support = 0.0 → field = 0.0 → no distortion.
Evidence against: None — this is exactly what the code does.
Verdict: **CONFIRMED**

### 3. Genuine: The model's axiom requires self-maintaining PATTERNS
Evidence for: Axiom 2 states "Stable objects are persistent self-maintaining patterns." A single isolated event cannot self-maintain because it has no persistent neighbors to sustain it. The support function correctly implements this axiom.
Evidence against: None.
Verdict: **CONFIRMED** — this is the correct behavior per the model's axioms.

## Root Cause
The persistence support function measures what fraction of a node's neighbors are also persistent. A single node has 0% persistent neighbors, so its support is 0.0, the delay field is zero everywhere, and the distorted rule equals the free rule.

This is NOT a bug. It's Axiom 2 in action: persistence requires a self-maintaining pattern, not an isolated point. The 2-node onset in the gravity sweep marks the minimum configuration where mutual neighbor support becomes nonzero — each node is a neighbor of the other.

## Resolution
The sanity FLAG is resolved. The 1-node zero-effect is correct model behavior. The gravity mechanism requires a persistent PATTERN (≥2 adjacent nodes), not a single event. This is consistent with the project's core axiom that "stable objects are persistent self-maintaining patterns."

## Status
RESOLVED
