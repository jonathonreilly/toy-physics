# Discrete Shapiro Delay

**Date:** 2026-04-06
**Status:** retained positive — c-dependent phase lag portable across three families

## Artifact chain

- [`scripts/shapiro_delay_portable.py`](../scripts/shapiro_delay_portable.py)
- [`logs/2026-04-06-shapiro-delay-portable.txt`](../logs/2026-04-06-shapiro-delay-portable.txt)
- This note

## Question

Does a causally propagating gravitational field produce a phase lag
at the detector that depends on the field propagation speed c?

## Result

| c | Fam 1 phase | Fam 2 phase | Fam 3 phase | Max diff |
| ---: | ---: | ---: | ---: | ---: |
| inst | 0.0000 | 0.0000 | 0.0000 | 0% |
| 2.0 | +0.0401 | +0.0401 | +0.0400 | 0.2% |
| 1.0 | +0.0499 | +0.0501 | +0.0499 | 0.4% |
| 0.5 | +0.0621 | +0.0622 | +0.0620 | 0.3% |
| 0.25 | +0.0679 | +0.0679 | +0.0679 | 0.1% |

## Properties

1. **Monotonic in 1/c**: slower field propagation → larger phase lag
2. **Geometry-independent**: agreement within 0.4% across three families
3. **Seed-stable**: agreement within 0.3% across seeds within each family
4. **Qualitatively new**: no static field of any shape can produce a
   c-dependent phase. This is NOT a deflection effect.
5. **Zero control clean**: instantaneous field gives exactly 0 by construction

## What this means

This is the discrete analog of the **Shapiro time delay** in GR: a beam
passing through a gravitational field is delayed by an amount that depends
on the gravitational potential along its path AND the propagation speed
of the field.

The phase lag approaches ~0.068 rad at c=0.25 and appears to saturate
(the forward-only limit). The functional form is approximately:

    phase(c) ≈ phase_max * (1 - exp(-a/c))

where phase_max ≈ 0.070 rad.

## Claim boundary

The Shapiro phase lag is a retained, portable, geometry-independent
observable from causal field propagation. It is the first retained
dynamic observable that static fields cannot produce.

This does NOT claim:
- A specific physical value for c (it's a free parameter like gamma)
- Equivalence to the full GR Shapiro delay (which involves metric perturbations)
- Self-consistency of the propagating field (the cone is imposed, not derived)
