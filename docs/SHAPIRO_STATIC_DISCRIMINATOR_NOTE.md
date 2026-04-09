# Shapiro Static Discriminator

**Date:** 2026-04-06  
**Status:** boundary result - static cone shape can mimic the retained c-dependent phase lag exactly; static scheduling cannot

## Artifact Chain

- [`scripts/shapiro_static_discriminator.py`](../scripts/shapiro_static_discriminator.py)
- [`logs/2026-04-06-shapiro-static-discriminator.txt`](../logs/2026-04-06-shapiro-static-discriminator.txt)
- This note

## Question

Can any static field shape or static scheduling proxy mimic the retained
c-dependent phase lag from the causal propagating-field lane?

## Control Results

The control gate is clean:

- exact zero control stays exact
- the retained causal phase curve is portable across the three grown families

Measured mean curves:

| Mode | c=2.0 | c=1.0 | c=0.5 | c=0.25 |
| --- | ---: | ---: | ---: | ---: |
| causal dynamic cone | +0.0372 | +0.0446 | +0.0569 | +0.0662 |
| static cone shape | +0.0372 | +0.0446 | +0.0569 | +0.0662 |
| static scheduling | +0.0446 | +0.0445 | +0.0446 | +0.0450 |

## Discriminator Read

1. **Static cone shape is a perfect mimic.**
   - The frozen cone-shape proxy reproduces the full c-dependent causal
     phase curve to numerical precision on all three families.
   - This means the Shapiro-style phase lag is **not** a unique
     discriminator against static field-shape effects in this model.

2. **Static scheduling is not enough.**
   - A frozen activation delay produces only a near-flat phase response.
   - It does not reproduce the causal c-dependence.

## Conclusion

The strongest honest statement is:

- the Shapiro-style phase lag is a real, portable observable
- but it is **not** stronger than all static field-shape effects
- it is only stronger than the static scheduling proxy

So this lane gives us a **boundary**, not a clean uniqueness proof:
the observable is compatible with causal propagation, but a static cone-shape
field family can reproduce the same detector phase curve exactly.

## Claim Boundary

This does **not** claim:

- that the retained phase lag is falsified
- that the causal propagating-field lane is invalid
- that the static scheduling proxy is a full match

It **does** say:

- if we want a unique causal-propagation discriminator, we need a different
  observable than the detector-line phase lag alone
