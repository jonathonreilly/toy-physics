# Analysis: Mutual Gravitation

## Date
2026-03-30

## Key Findings

### 1. Mutual gravitation confirmed
Two masses each pull paths toward themselves. With both present, the path from A→B is more strongly curved (ad=-18.46) than with either alone (ad=-12.58). The path midpoint shifts from the free-path position toward the midpoint between the masses.

### 2. Path bending scales with mass size (sublinearly)
Action_diff vs node count for a single mass:
2 nodes: -8.58, 5 nodes: -13.18, 10 nodes: -15.73

The relationship is approximately logarithmic — consistent with the field being a discrete Green's function (which scales as ln(support_area) for a 2D source).

### 3. Superposition FAILS — gravitational interaction is nonlinear
The combined action from two masses is ~50% less than the sum of individual actions:
ad_both = -16.15, ad_1 + ad_2 = -24.49 (deviation = -51.6%)

This nonlinearity comes from the stationary-action path optimization: the path adjusts its shape to the combined field, and the optimal path in the combined field is NOT the sum of the optimal paths in individual fields.

This is physically significant: the model's gravity is NOT a linear superposition of individual potentials at the level of path selection. The potential field itself IS linear (it's solved by a linear relaxation), but the path-to-action mapping introduces nonlinearity because the path changes shape in response to the combined field.

### 4. Symmetric mass placement cancels deflection (as expected)
Equal masses above and below produce zero net deflection for centered paths, even though the action changes significantly. This is the same y-symmetry mechanism that protects V(y=0)=1 in the interference regime.

## Significance
This is the model's version of Newton's law of mutual gravitation: two persistent patterns create delay-field distortions that bend paths toward each other. The key departure from Newtonian gravity is the strong nonlinearity (~50% superposition failure) — the model's gravity is NOT simply additive at the level of path deflection, even though the underlying potential is linear. This is an inherent property of path optimization in nonlinear landscapes.
