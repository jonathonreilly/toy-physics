# Self-Consistency Structured-Null Note (2026-04-11)

**Status:** bounded - bounded or caveated result note
## Scope

This rerun replaces the earlier ad hoc random controls in
`frontier_self_consistency_test.py` with two cleaner moment-matched structured
nulls on the same fixed `10x10` periodic staggered surface:

1. `ShiftedNull`: exact torus shift of the static-from-initial field
2. `PhaseNull`: phase-scrambled field with the same torus power spectrum,
   mean, and standard deviation as the static-from-initial field

The goal is narrower than a full architecture-wide closure: determine whether
the fixed-surface self-consistency claim survives cleaner null controls.

## Corrected fixed-surface result

Canonical rerun output:

- `SelfConsist`: sign margin `+30`, width ratio `0.3554`, boundary alpha `0.145434`
- `StaticInit`: sign margin `+40`, width ratio `0.3563`, boundary alpha `0.159548`
- `ShiftedNull`: sign margin `+11`, width ratio `0.4847`, boundary alpha `0.134795`
- `PhaseNull`: mean sign margin `+21.4 +/- 31.1`, width ratio `0.4012 +/- 0.0186`,
  boundary alpha `0.131728 +/- 0.011976`

Key comparisons:

- `SelfConsist` vs `StaticInit`:
  deterministic separation on this fixed surface
- `StaticInit` vs `ShiftedNull`:
  deterministic separation on this fixed surface
- `StaticInit` vs `PhaseNull`:
  width `3.4 sigma`, boundary alpha `3.3 sigma`
- `SelfConsist` vs `PhaseNull`:
  width `3.5 sigma`, sign margin `0.4 sigma`, boundary alpha `1.6 sigma`

## Interpretation

The self-consistency claim is **strengthened**, but only in a narrower and more
honest form.

What improved:

- The earlier result no longer depends on crude iid random controls.
- A matched smooth structured null still fails to reproduce the self-consistent
  width response.
- A simple torus shift of the static field fails strongly, so packet-field
  alignment is load-bearing on this surface.

What narrowed:

- The strongest surviving discriminator is width contraction, not sign margin.
- The `PhaseNull` still retains substantial positive sign response (`4/5`
  positive margins), so this rerun does not turn the lane into a clean
  sign-selective closure.
- Different structured nulls are themselves separated (`6.3 sigma` on the best
  metric), so the fixed-surface claim remains method-sensitive.

## Bottom line

The fixed-surface self-consistency result survives cleaner structured nulls and
is therefore more credible than the earlier random-control framing. The honest
retained statement is:

> On the corrected `10x10` periodic staggered torus, iterative backreaction is
> distinguished from matched static structured nulls, with the cleanest
> surviving separation in width contraction.

This is a strengthened fixed-surface result, not a universal architecture-wide
closure. A next stronger version would need:

- a better matched structured control ensemble than a single shift and a single
  phase-scramble family
- an open-boundary or Wilson cross-check
- a non-periodic rerun to avoid torus-specific alignment effects
