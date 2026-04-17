# Analysis: Lorentz Symmetry Test

## Date
2026-03-30

## Key Findings

### 1. The retained update √(dt²-dx²) is EXACTLY Lorentz-invariant
Max boost drift = 1.11×10⁻¹⁵ (machine epsilon) across all test velocities and edge configurations. The model's "proper time" equivalent is an exact Lorentz scalar.

This is NOT a coincidence — the retained update is defined as √(delay² - link_length²), which is algebraically identical to the Minkowski interval √(dt² - dx²). The Lorentz boost is defined as the transformation that preserves this quantity. So the invariance is built into the definitions.

### 2. The action (spent delay) is NOT Lorentz-invariant
Spent delay = dt - √(dt²-dx²) varies from 0.268 (v=0) to 0.000 (v=0.5, light-like) to 0.792 (v=0.9). The action depends on the frame — it's NOT a Lorentz scalar.

However: the STATIONARY ACTION PATH (the path that minimizes total spent delay) IS frame-independent by the variational principle. The action value changes but the optimal path doesn't. This is the model's version of "physics is the same in all frames" — not through invariance of the Lagrangian, but through invariance of the extremal principle.

### 3. Signal speed = 1 exactly at zero field
delay(field=0) = link_length exactly, giving signal speed = 1 in natural units. This is the model's speed of light.

### 4. Gravitational time dilation emerges naturally
delay(field>0) = link_length × (1 + field) > link_length. Signals slow down near massive objects. The ratio retained/delay = √(1 - 1/(1+field)²) → 1 as field → ∞, meaning nearly all the delay becomes retained update (proper time). At field=0, retained/delay = 0 (all delay is "spent" — the light-like limit).

### 5. The retained/delay ratio is universal across edge types
At any given field value, retained/delay is the SAME for horizontal (1,0), vertical (0,1), and diagonal (1,1) edges:
- field=0.01: 0.1404 for all edge types
- field=0.50: 0.7454 for all edge types
- field=1.00: 0.8660 for all edge types

This universality follows from the formula: retained/delay = √(1 - 1/(1+field)²), which depends only on field, not on link_length.

## Significance

The model has Minkowski-like structure built into its local edge properties:
- **√(dt²-dx²) is Lorentz-invariant** (proper time)
- **Signal speed = 1** (speed of light)
- **Gravity slows signals** (time dilation)
- **The retained/delay ratio is universal** (frame-independent proper-time fraction)

These are not emergent properties — they're consequences of the action formula's algebraic structure. But they establish that the model's local dynamics are COMPATIBLE with special-relativistic structure, even though the model doesn't assume continuous spacetime.

The fact that the ACTION (spent delay) is NOT Lorentz-invariant is important: it means the model's dynamics are NOT simply "discretized special relativity." The variational principle (stationary action path) provides frame-independence through a different mechanism than Lagrangian invariance.
