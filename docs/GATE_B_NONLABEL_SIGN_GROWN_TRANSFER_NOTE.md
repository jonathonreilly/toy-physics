# Gate B Non-Label Sign Grown Transfer Note

**Date:** 2026-04-06
**Status:** grown-row architecture test for the old geometry-sector idea

## Artifact chain

- [`scripts/GATE_B_NONLABEL_SIGN_GROWN_TRANSFER.py`](/Users/jonreilly/Projects/Physics/scripts/GATE_B_NONLABEL_SIGN_GROWN_TRANSFER.py)

## Question

Can the old Gate B geometry-sector / non-label connectivity architecture carry
the current fixed-field signed-source response on the retained grown row?

This note is intentionally narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- label-grown control vs position-based geometry-sector candidate
- exact zero-source and neutral same-point cancellation checks
- small charge-linearity sanity pass

## Interpretation target

- if the geometry-sector candidate preserves the zero / neutral controls and
  the sign-law charge response, the old architecture genuinely applies here
- if it collapses to zero or loses charge linearity, the old architecture was
  specific to the older Gate B families and does not transplant cleanly

## Frozen Result

Seed `0` retained grown-row replay:

| family | zero source | single `+1` | single `-1` | neutral `+1/-1` | double `+2` | charge exponent |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| label-grown control | `+0.000000e+00` | `-1.594422e-04` | `+1.594790e-04` | `+0.000000e+00` | `-3.188474e-04` | `0.999833` |
| geometry-sector candidate | `+0.000000e+00` | `-3.534838e-05` | `+3.533743e-05` | `+0.000000e+00` | `-7.070770e-05` | `1.000223` |

## Safe Read

The old architecture does genuinely apply to the current grown-row fixed-field
lane, but only in a narrowed form:

- the position-based geometry-sector candidate preserves the exact zero-source
  baseline
- the neutral same-point `+1/-1` control still reduces to zero
- the single-source sign response survives with the correct orientation
- the charge response remains linear to within the checked exponent
- the candidate is weaker than the label-grown control, so it is not a full
  family-wide replacement, but it is a real transfer positive rather than a
  zero response

## Final Verdict

**retained narrow grown-row transfer positive**
