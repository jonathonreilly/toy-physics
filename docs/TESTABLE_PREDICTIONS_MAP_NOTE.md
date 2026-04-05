# Testable Predictions Map

**Date:** 2026-04-05  
**Status:** ranked map of the strongest retained testables across the current
science portfolio

This note is not a claim note.

It is the most useful way to answer the question:

- what can we actually test now?
- what is still only a theory-side discriminator?
- what could plausibly go to a lab, an analog simulator, or a tabletop
  platform without overselling the model?

## Ranking

1. Exact-lattice wavefield phase-lag discriminator
2. Diamond / NV lock-in quadrature test
3. Wide-lattice `h^2+T` distance-law replay
4. Grown trapping / frontier transport
5. Split-shell generated-family bridge

## 1. Exact-Lattice Wavefield Phase-Lag Discriminator

- Observable: detector-line phase-ramp slope and span, plus the wave / same-
  site response ratio
- Null: zero-source exact recovery and the same-site-memory baseline with no
  stable phase ramp
- What is retained: exact zero-source reduction, `TOWARD`, near-linear `F~M`,
  and a coherent detector-line phase ramp with `R^2 ~ 0.96`
- What still needs hardening: transfer off the exact lattice
- Test class: theory-side discriminator first, then analog-simulator-testable
  if a wave or interferometric platform can emulate the phase ramp

Why this is strong:

- it is the cleanest phase-sensitive retained observable in the repo
- it already separates a wave-like update from a same-site control
- it is more diagnostic than a scalar amplitude readout

Why it might fail in a broader test:

- the phase ramp may remain exact-lattice specific
- a real analog platform may reproduce only the null, not the slope

## 2. Diamond / NV Lock-In Quadrature Test

- Observable: `X`, `Y`, and `phi = atan2(Y, X)` under a driven source
- Null: after calibration, the quasi-static baseline gives `Y ~ 0` and flat
  phase
- What is retained: the retained retarded / wavefield lane and the new
  diamond protocol note
- What still needs hardening: a calibrated amplitude estimate and a real lab
  sensitivity budget
- Test class: tabletop / lab-facing

Why this is strong:

- it is the most realistic experiment-facing discriminator in the repo
- it is differential and lock-in friendly
- it does not depend on absolute gravity amplitude claims

Why it might fail:

- the quadrature may vanish after calibration
- the signal may be absorbed by instrument lag or thermal/mechanical cross-talk

## 3. Wide-Lattice `h^2+T` Distance-Law Replay

- Observable: far-tail exponent of the detector response versus source
  separation
- Null: a non-retained or mis-ordered lattice slice that does not preserve the
  far-tail fit
- What is retained: independent wide replay on `main` with Born at machine
  precision, `10/10` TOWARD, and far-tail `b^(-1.05)` with `R^2 = 0.990`
- What still needs hardening: whether the far tail is truly asymptotic rather
  than a finite-lattice replay
- Test class: theory-side and analog-simulator-testable

Why this is strong:

- it is the most reproducible distance-law result currently retained
- it is already a clean, reviewable frontier result

Why it might fail:

- the exponent may steepen on larger windows
- the far tail may remain slice-dependent

## 4. Grown Trapping / Frontier Transport

- Observable: escape ratio plus frontier-shell radial moment shift
- Null: exact `eta = 0` grown baseline
- What is retained: monotone escape decrease and monotone outward frontier
  shift on the retained grown row
- What still needs hardening: a stronger frontier observable than transport
  plus a cleaner link to a horizon-like interpretation
- Test class: theory-side first, then analog transport platform

Why this is strong:

- it is a real structural transport observable, not just raw attenuation
- it is stricter than the older escape-only probe

Why it might fail:

- it may stay a transport-only probe without becoming structural horizon
  physics

## 5. Split-Shell Generated-Family Bridge

- Observable: detector support `N_eff`, sign counts, and weak-field `F~M`
- Null: the compact generated-family bridge and its retained closed family
- What is retained: broader support and partial recovery on the split-shell
  family
- What still needs hardening: a clean weak-field law on the generated family
- Test class: theory-side, and possibly analog graph / transport simulator

Why this is strong:

- it is the first real reopening after the compact bridge was closed
- it shows the geometry family matters, not just the field rule

Why it might fail:

- the law remains too weak for a real generated-family closure
- the bridge may stay geometry-limited

## Safe Use Cases

- If you want a clean lab-facing story, the diamond / NV quadrature test is
  the best current choice.
- If you want the strongest internal theory discriminator, the exact-lattice
  wavefield phase-ramp lane is still the most informative.
- If you want the strongest retained finite-lattice gravity result, the
  wide-lattice distance-law replay is the one to cite carefully.

## What Is Still Theory-Only

- self-gravity / Poisson backreaction as a real new mechanism
- any clean emergent-gamma equivalence
- any full continuum theorem
- any horizon theory

Those are still active moonshot targets, not retained predictions.

## Final Verdict

**best current testables are phase-sensitive, differential, and control-heavy**

The practical order is:

1. exact-lattice wavefield phase-ramp discriminator
2. diamond / NV lock-in quadrature test
3. wide-lattice distance-law replay
4. grown trapping / frontier transport
5. split-shell generated-family bridge
