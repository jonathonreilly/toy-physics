# Vector / Magnetic Extension Note

**Date:** 2026-04-06  
**Status:** retained narrow extension positive, bounded to a moving-source signed response with null circulation candidate

## Artifact Chain

- [`docs/MOVING_SOURCE_RETARDED_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MOVING_SOURCE_RETARDED_PORTABILITY_NOTE.md)
- [`docs/SOURCE_RESOLVED_TRANSVERSE_PROPAGATING_GREEN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_RESOLVED_TRANSVERSE_PROPAGATING_GREEN_NOTE.md)
- [`docs/ELECTROSTATICS_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ELECTROSTATICS_CARD_NOTE.md)
- [`docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md)
- [`scripts/vector_magnetic_extension_probe.py`](/Users/jonreilly/Projects/Physics/scripts/vector_magnetic_extension_probe.py)
- [`logs/2026-04-06-vector-magnetic-extension-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-vector-magnetic-extension-probe.txt)
- [`logs/2026-04-06-moving-source-retarded-portability-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-moving-source-retarded-portability-probe.txt)
- [`logs/2026-04-05-source-resolved-transverse-propagating-green.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-transverse-propagating-green.txt)

## Question

Is there one bounded response that is genuinely beyond the scalar electrostatics
card, but still narrow enough to keep out of Maxwell or magnetic-theory
inflation?

This lane is intentionally strict:

- exact zero / neutral controls first
- one minimal moving-source signed-response pocket on an exact compact family
- one circulation-like plaquette probe as a null cross-check
- no claim of a full vector field theory
- no claim of real magnetic induction

## Result

The narrowest defensible positive is:

- a signed moving-source centroid response survives the exact zero baseline
- the response does not collapse into the matched static control
- the centroid bias flips sign with the source motion `v`
- the circulation-like plaquette probe stays exactly null, so there is no
  magnetic-style loop survivor in this compact family

Moving-source proxy:

- exact zero-source static max `|delta_y| = 0.000e+00`
- exact zero-source moving max `|delta_y| = 0.000e+00`
- exact zero-source max `|plaquette circulation| = 0.000e+00`
- matched static control at `v = 0` gives `delta_y vs static = +0.000000e+00`
- `v = +1.00` gives `delta_y vs static = +2.084652e-05`
- `v = -1.00` gives `delta_y vs static = -2.084652e-05`

Circulation-like cross-check:

- final-layer plaquette circulation stays at `+0.000e+00` on the probed
  central plaquettes
- no signed loop observable survives this exact compact family
- the only live vector-like response is the odd-in-`v` centroid shift

## Safe Read

The strongest review-safe statement is:

- the current scalar electrostatics card is not the whole story
- there is one bounded signed-response extension tied to source motion
- the circulation-like candidate collapses back to null on this compact exact
  family
- the effect is still small, proxy-level, and architecture-bounded

What this does **not** claim:

- not full electromagnetism
- not a magnetic induction law
- not a gauge-field derivation
- not a general vector-theory closure

## Final Verdict

**retained narrow extension positive: a bounded odd-in-v moving-source centroid response survives, while the circulation-like candidate freezes at null**
