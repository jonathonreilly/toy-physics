# Analysis: Slit Reachability Audit

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-interference-slit-reachability-audit.txt`
- Script: `scripts/interference_slit_reachability_audit.py`

## Data Summary
- 10 test cases: 6 in the exact-zero V regime, 4 in the nonzero-V regime
- Per-slit amplitude decomposition at each screen position

## Key Finding: SINGLE-SLIT REACHABILITY CONFIRMED

Every exact-zero case (6/6) shows amplitude from ONE slit only. The other slit contributes exactly zero amplitude — not small, not canceling, but literally zero paths exist through it to that screen position.

Every nonzero-V case (4/4) shows amplitude from BOTH slits.

| Case | V regime | Diagnosis |
|------|----------|-----------|
| w=8, sep=8, y=1 | V=0 | SINGLE-SLIT (only slit_y=4) |
| w=8, sep=8, y=3 | V=0 | SINGLE-SLIT (only slit_y=4) |
| w=8, sep=8, y=5 | V=0 | SINGLE-SLIT (only slit_y=4) |
| w=12, sep=8, y=3 | V=0 | SINGLE-SLIT (only slit_y=4) |
| w=16, sep=8, y=5 | V=0 | SINGLE-SLIT (only slit_y=4) |
| w=8, sep=12, y=1 | V=0 | SINGLE-SLIT (only slit_y=6) |
| w=12, sep=8, y=1 | V>0 | BOTH slits |
| w=16, sep=8, y=1 | V>0 | BOTH slits |
| w=16, sep=8, y=3 | V>0 | BOTH slits |
| w=24, sep=8, y=5 | V>0 | BOTH slits |

**Zero exceptions.** The visibility threshold is exactly the point where paths through the second slit first become geometrically available on the discrete grid.

## Hypothesis Verdict
**CONFIRMED** — The exact-zero regime is caused by single-slit reachability (topological), not by perfect cancellation of two-slit amplitudes. This is a property of the discrete event network's causal DAG structure.

## Significance
This establishes that the visibility threshold is TOPOLOGICAL, not dynamical. It depends on whether paths physically exist on the grid, not on the details of the path-sum computation. This is a distinctly discrete-network feature with no continuum analogue.
