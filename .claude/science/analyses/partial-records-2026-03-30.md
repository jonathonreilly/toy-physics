# Analysis: Partial Record Decoherence Curve

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-interference-partial-record-sweep.txt`
- Script: `scripts/interference_partial_record_sweep.py`

## Data Summary
- 21 record-probability values (0.00 to 1.00, step 0.05)
- 3 geometry configurations
- V measured at y=0, y=1, y=2, and mean_V

## Key Finding: V(y, p) = V(y, 0) × (1 - p) EXACTLY

The decoherence curve is perfectly linear at every screen position, every geometry:

**V(y, p) = V_coherent(y) × (1 - p)**

This holds to floating-point precision across all 21 p-values, all screen positions, all three geometries tested. There is no threshold, no phase transition, no surprise. It's the simplest possible functional form.

### Verification at y=0 (width=16, slit_sep=8):
V(y=0, 0.00) = 1.000, V(y=0, 0.50) = 0.500, V(y=0, 1.00) = 0.000
→ V = 1 - p exactly.

### Verification at y=1:
V(y=1, 0.00) = 0.963, V(y=1, 0.50) = 0.482, V(y=1, 1.00) = 0.000
→ V = 0.963 × (1 - p) exactly.

### Universal across geometries:
All three configurations (width=16/sep=8, width=24/sep=4, width=20/sep=12) show the same V = V_0 × (1-p) relationship.

## Physical Interpretation

The linear law has a simple explanation from the model's mechanics:

The amplitude at the barrier splits into recorded (√p) and unrecorded (√(1-p)) branches. The unrecorded branch interferes coherently; the recorded branch doesn't. The visibility of the coherent sector is V_0 × (1-p) because:
- The coherent amplitude is √(1-p) of the total
- Visibility depends on the ratio of coherent to total probability
- The coherent sector's probability is (1-p) of total
- Within the coherent sector, the interference pattern is identical to the p=0 case
- V = (coherent visibility) × (coherent fraction) = V_0 × (1-p)

This is not a dynamical result of the model — it's a mathematical consequence of the amplitude splitting rule. The model produces LINEAR decoherence, not threshold or quadratic behavior.

## Hypothesis Verdict
**SUPPORTED — the decoherence is gradual, not binary.** But the functional form (exactly linear) is the trivial mixing case, not a novel dynamical prediction. The null hypothesis (binary: V drops to 0 at any p > 0) is decisively falsified.

## Significance
- Confirms that the model CAN produce partial decoherence, not just all-or-nothing.
- The linear form V = V_0(1-p) is the trivial amplitude-splitting result, with no model-specific dynamics.
- To get non-trivial decoherence, the record mechanism would need to be more complex (e.g., records that partially affect the continuation structure rather than just sector-labeling).
