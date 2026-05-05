# Structured Mirror Reconciliation Note

**Date:** 2026-04-03  
**Status:** bounded - bounded or caveated result note
**Primary runner:** [`scripts/structured_mirror_reconciliation.py`](../scripts/structured_mirror_reconciliation.py) (canonical structured-growth on joint-validator harness; slow ~118s, AUDIT_TIMEOUT_SEC=240)

This note freezes the comparison between the committed canonical structured
mirror validator and the newer quick linear Born claims.

## Question

Is the structured-mirror geometry itself Born-clean under a linear
propagator, or was the clean Born number coming from a different slit /
field / harness choice?

## Canonical evidence on `main`

The committed joint validator for the structured-growth family is:

[`scripts/structured_mirror_joint_validation.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_joint_validation.py)
with saved output:

[`logs/2026-04-03-structured-mirror-joint-validation.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-structured-mirror-joint-validation.txt)

That validator reports a linear structured-growth lane that is physically
interesting but not Born-clean:

| N | `pur_cl` | gravity | Born `|I3|/P` |
|---|---:|---:|---:|
| 25 | `0.833±0.013` | `+3.863±0.225` | `2.51e-01±9.56e-02` |
| 30 | `0.878±0.015` | `+4.904±0.282` | `1.71e-01±2.69e-02` |
| 40 | `0.932±0.009` | `+6.620±0.181` | `1.71e-01±2.47e-02` |

So the canonical structured-growth validator is **not** Born-clean.

## What the reconciliation script tests

The new dedicated comparison script is:

[`scripts/structured_mirror_reconciliation.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_reconciliation.py)

It compares four harnesses on the same structured-growth geometry:

1. canonical threshold slits + physical mass field
2. threshold slits + flat field
3. audit-style top-K slit selection + flat field
4. audit-style top-K slit selection + physical mass field

## Reconciliation

The discrepancy is **not** a geometry bug. It is a harness discrepancy:

- the structured-growth geometry itself is physically interesting and retains
  positive gravity plus nontrivial decoherence
- but the Born value is highly sensitive to how the barrier apertures are
  selected and whether the physical field is present
- the canonical validator remains O(1e-1), not machine-clean
- the audit-style top-K slit selection can make the Born number look much
  better or much worse, so it is not a substitute for the canonical harness

## Safe conclusion

- Structured mirror growth is a real geometry result.
- It is **not** yet Born-clean on the retained canonical linear validator.
- The earlier `8e-17` claim is not synthesis-safe for the structured-growth
  lane as currently retained in `main`.
- The review-safe Born-clean growth-family result remains the exact 2D mirror
  lane, not the structured-growth lane.

