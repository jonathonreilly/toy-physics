# Gravitomagnetic Portability Note

**Date:** 2026-04-06  
**Status:** retained narrow positive - the odd-in-v phase correction is portable across the three retained grown families

## Artifact Chain

- [`scripts/gravitomagnetic_portability.py`](../scripts/gravitomagnetic_portability.py)
- [`logs/2026-04-06-gravitomagnetic-portability-probe.txt`](../logs/2026-04-06-gravitomagnetic-portability-probe.txt)
- [`docs/MOVING_SOURCE_CROSS_FAMILY_NOTE.md`](../docs/MOVING_SOURCE_CROSS_FAMILY_NOTE.md)
- [`docs/VECTOR_MAGNETIC_EXTENSION_NOTE.md`](../docs/VECTOR_MAGNETIC_EXTENSION_NOTE.md)

## Question

Starting from the retained moving-source antisymmetric Shapiro correction on `69d92a5`, does the odd-in-velocity phase correction survive across the three portable grown families, or does it stay local to one family?

## Exact Controls

- exact zero-source control: `0.000` on the static and moving lanes by construction
- matched static-source control at `v = 0`: `0.000` on all three families by construction

## Portability Table

| family | drift | restore | delta(+v) | delta(-v) | odd component | antisym residual |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| portable family 1 | 0.20 | 0.70 | +0.0032 | -0.0035 | +0.0034 | -0.00015 |
| portable family 2 | 0.05 | 0.30 | +0.0030 | -0.0034 | +0.0032 | -0.00020 |
| portable family 3 | 0.50 | 0.90 | +0.0034 | -0.0036 | +0.0035 | -0.00010 |

## Cross-Family Summary

- delta(+v) spans `0.0030` to `0.0034` across the three families
- the odd component spans `0.0032` to `0.0035`
- the largest antisymmetry residual is `0.00020`, i.e. below `4%` of the peak-to-peak odd signal
- exact zero and static-source controls stay flat
- the sign of the correction flips with `v` on every family

## Safe Read

- the odd-in-v moving-source phase correction survives the exact zero control
- the matched `v = 0` static control stays flat
- the correction is portable across the three retained grown families
- the residual even part is small compared with the odd component
- this remains a proxy-level gravitomagnetic observable, not a full magnetic theory

## Final Verdict

**retained positive: the odd-in-v gravitomagnetic phase correction is portable across the three retained grown families, with antisymmetry residual below 4% of the peak-to-peak odd signal**
