# Gate B Complex-Action Falsifier Note

**Date:** 2026-04-05 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded tiny falsification-first complex-action probe — local detector-attenuation effect is verified on the named row, but the inherited Gate B / Born guardrail comes from an upstream bounded / unaudited note; not a tier-ratifiable complex-action branch claim.

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

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, leaf criticality):

> Issue: the runner verifies a finite detector-effect sweep, but the
> proposed_retained queue status is stronger than the source note's
> own bounded-falsifier scope, and the retained Gate B/Born
> guardrail is imported from `docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`,
> which is bounded and unaudited. Why this blocks: the audit can
> retain the local fact that gamma attenuates detector escape on
> this row, but it cannot ratify a retained complex-action branch
> or inherited retained-row guardrail through a bounded upstream.

## What this note does NOT claim

- A tier-ratifiable complex-action branch.
- An audit-clean upstream Gate B / Born guardrail.
- A theorem beyond the local detector-attenuation effect on the
  named row.

## What would close this lane (Path A future work)

A retained complex-action branch would require auditing the upstream
`GATE_B_GROWN_JOINT_PACKAGE_NOTE.md` and registering its retained
guardrails as audit-clean dependencies, plus extending the runner
beyond the single detector-attenuation row.
