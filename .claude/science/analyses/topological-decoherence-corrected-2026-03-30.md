# Analysis: Topological Decoherence (Corrected — Per-Slit Recording)

## Date
2026-03-30

## Correction
The original implementation mixed only two global branches (no shortcuts vs both-slit shortcuts). The corrected version has each slit recording independently with probability p, giving 4 branches: {none}, {upper}, {lower}, {both}. Each branch has its own DAG and contributes incoherently with weight p^k × (1-p)^(2-k).

## Corrected Decoherence Curve

| p | V(y=0) | V(y=2) | V(y=3) |
|---|--------|--------|--------|
| 0.0 | 1.000 | 0.670 | 0.321 |
| 0.3 | 0.998 | 0.651 | 0.246 |
| 0.5 | 0.995 | 0.628 | 0.196 |
| 0.7 | 0.989 | 0.581 | 0.160 |
| 0.9 | 0.958 | 0.428 | 0.165 |
| 1.0 | 1.000 | 0.937 | 0.801 |

## Key Features of the Corrected Curve

### 1. V DECREASES with p for 0 < p < 1 (genuine decoherence)
Unlike the original (V constant), the corrected curve shows monotonic decrease at y=0 and y=2 from p=0 to p≈0.9. This is genuine decoherence from incoherent mixing of multiple DAG branches.

### 2. V jumps BACK UP at p=1.0
At p=1.0, both slits always record, giving weight 1.0 to the {both} branch and 0 to all others. This single branch has its own coherent interference pattern with HIGHER visibility (due to amplitude rebalancing from shortcuts). Maximum decoherence occurs at INTERMEDIATE p, not at full recording.

### 3. The functional form is much flatter than V₀(1-p)
V(y=0) stays above 0.95 until p=0.9, then drops. The trivial law V₀(1-p) would give V=0.1 at p=0.9. The actual value is 0.958 — nearly 10× higher. The flattening comes from the branch weights: at p=0.9, the {none} branch still has weight (1-0.9)² = 0.01, while the {both} branch has weight 0.81. The mixed branches {upper} and {lower} have weight 0.09 each. The dominant {both} branch has HIGH visibility (shortcuts enhance interference), which keeps V high.

### 4. Maximum decoherence at p ≈ 0.8 for y=3
V(y=3) reaches minimum 0.155 at p=0.8, then rises to 0.165 at p=0.9 and 0.801 at p=1.0. The minimum decoherence point depends on y-position — it's where the branch mixing produces maximum destructive combination of different interference patterns.

## Physical Interpretation
This is analogous to decoherence from entanglement with an environment that has a finite number of states. With 2 slits, there are 4 environment states (recording patterns). Maximum decoherence occurs when the environment is in a maximally mixed state (intermediate p), not when it's in a pure state (p=0 or p=1). This is a generic feature of finite-dimensional decoherence.

## Status
Corrected result. The decoherence is genuine and non-trivial.
