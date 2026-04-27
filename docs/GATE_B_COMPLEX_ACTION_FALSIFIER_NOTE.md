# Gate B Complex-Action Falsifier Note

**Date:** 2026-04-05  
**Status:** tiny falsification-first complex-action probe on the proposed_retained Gate B grown row

## Artifact chain

- [`scripts/gate_b_complex_action_falsifier.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_complex_action_falsifier.py)
- [`logs/2026-04-05-gate-b-complex-action-falsifier.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-complex-action-falsifier.txt)

## Question

Does the smallest absorptive / complex-action-style modification on the
retained Gate B moderate-drift grown row change detector escape in a way that
is not just bookkeeping drift?

This probe stays narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- one far-field source position: `z = 3`
- one detector observable: `P_det` on the final layer
- one escape ratio: `escape(gamma) = P_det(gamma) / P_det(0)`
- one required guardrail: `gamma = 0` must exactly reproduce the baseline on
  the same row

## Frozen result

The retained row stays exact at `gamma = 0` by construction.

Aggregated over seeds `0..3`:

| `gamma` | mean `escape(gamma)` | mean `delta_z` |
| --- | ---: | ---: |
| `0.05` | `0.215` | `-4.89e-03` |
| `0.10` | `0.047` | `-9.90e-03` |
| `0.20` | `0.002` | `-2.00e-02` |
| `0.50` | `0.000` | `-4.82e-02` |

The raw detector baseline is large on this row, but the escape ratio is the
meaningful observable here. What matters is the relative change against the
`gamma = 0` baseline.

## Safe read

The narrow, honest statement is:

- `gamma = 0` reproduces the retained Gate B row exactly
- increasing `gamma` suppresses detector escape sharply
- the detector centroid also shifts slightly away from the mass side
- this is a real effect on the retained grown row, but it is still only a
  tiny falsification probe, not a retained complex-action theory

## Guardrail note

This probe does **not** re-freeze Born on the same row.
That guardrail is inherited from the retained Gate B grown joint-package note:

- [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)

So the safe read is:

- complex-action-style attenuation has a visible detector effect on the
  retained Gate B row
- the result is bounded and useful as a falsifier
- it is not yet a broader generated-geometry complex-action branch

## Branch implication

This is enough to keep the tiny probe alive as a bounded positive.

The next question is not whether `gamma` can move the detector.
It can.

The next question is whether any geometry-aware version of the same idea can
survive the generated-family bridge without becoming a pure support artifact.
