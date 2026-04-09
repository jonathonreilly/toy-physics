# F~M Transfer: Grown vs Fixed Lattice

**Date:** 2026-04-06
**Status:** retained positive — mass-law transfer agrees within uncertainty

## Artifact chain

- [`scripts/fm_transfer_grown_companion.py`](../scripts/fm_transfer_grown_companion.py)
- [`logs/2026-04-06-fm-transfer-grown-companion.txt`](../logs/2026-04-06-fm-transfer-grown-companion.txt)

## Question

Does the weak-field mass scaling exponent (F~M) agree between the grown
geometry (drift=0.2, restore=0.7) and the regular lattice companion?

## Result

| Family | F~M | Uncertainty |
| --- | ---: | ---: |
| Fixed lattice | 0.9901 | (single geometry) |
| Grown (6 seeds) | 0.9870 | +/- 0.0097 |

Difference: 0.0031 (0.3 sigma). Agreement within uncertainty.

Per-seed values: 0.999, 0.970, 0.981, 0.990, 0.997, 0.985.

## Claim boundary

Mass-law transfer agrees within uncertainty on the retained grown-row
neighborhood (drift=0.2, restore=0.7).

This does NOT claim:
- Geometry-generic F~M transfer
- Transfer at other drift/restore values
- Transfer of other observables (distance law, decoherence, etc.)
