# Full GR: Axiom-First Path Survey

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Purpose:** clean-sheet memo of distinct end-to-end routes to full GR from the current framework, without assuming the current shell/tensor-boundary path is the only possible architecture.

## Current state of the gravity frontier

The current frontier has already established several exact pieces:

- weak-field gravity is retained
- restricted strong-field gravity is retained on the exact local `O_h` / star-supported class
- the shell-side scalar law is exact
- the bright tensor response is already localized to `E_x` and `T1x`
- the exact support-side scalar observable is exact:
  - `delta_A1 = phi_support(center)/Q - phi_support(arm_mean)/Q`
- the current blocker is that the tensor endpoint coefficients still come from a numerical `eta_floor_tf` pipeline, not an exact tensor observable

That means the remaining work is not “more of the same shell algebra.” It is to decide which end-to-end derivation architecture can most cleanly supply the missing exact tensor side.

The 10 routes below are meant as research architectures, not claims of closure.

## 1. Exact support-side tensor observable on the `A1 x {E_x, T1x}` block

- **One-line theorem idea:** derive an exact microscopic tensor observable on the support block and recover the tensor boundary coefficients from it.
- **Uses:** `A1` support reduction, exact shell amplitude law, exact `E_x/T1x` channel selection, exact support-side scalar observable `delta_A1`, exact local `O_h` / finite-rank source class.
- **Why cleaner:** it stays on the microscopic support side and avoids reading tensor data off sampled Einstein residuals.
- **Main risk/blocker:** the exact tensor observable may not exist as a simple support-block object; the current evidence only proves the scalar support law exactly.
- **Status:** promising.

## 2. Exact support-side Schur/Dirichlet tensor action

- **One-line theorem idea:** build the tensor completion from an exact support-side Schur complement or discrete Dirichlet principle on the `A1 x {E_x, T1x}` block.
- **Uses:** exact reduced shell law, exact microscopic Schur boundary action, exact discrete Dirichlet principle, exact `A1` block, bright-channel localization.
- **Why cleaner:** the atlas already shows the scalar shell trace is a stationary point of a discrete boundary functional; the tensor analogue may be the natural next exact object.
- **Main risk/blocker:** the current Schur/Dirichlet results are exact only for the scalar shell trace, not for the tensor endpoint coefficients.
- **Status:** promising.

## 3. Axiom-first spacetime lift from `S^3` and anomaly-forced time

- **One-line theorem idea:** derive the spacetime structure first from `S^3` topology plus anomaly-forced time, then derive GR as the unique compatible `3+1` lift.
- **Uses:** anomaly-forced time theorem, `S^3` boundary-link theorem, `S^3` cap uniqueness, `S^3` general-`R` extension, one-generation matter closure, three-generation structure.
- **Why cleaner:** it bypasses the shell/tensor frontier and tries to make spacetime itself emerge from the retained topology and chirality stack.
- **Main risk/blocker:** current retained topology tools support the `S^3` package, but not yet a full nonlinear Einstein equation derivation.
- **Status:** promising but speculative.

## 4. Observable-principle effective-action route

- **One-line theorem idea:** derive the gravitational action as the unique effective action compatible with the exact observable principle, CPT-even scalar generation, and the accepted Hilbert/locality reduction.
- **Uses:** observable principle from the axiom, exact CPT, exact `I_3 = 0`, single-axiom Hilbert/locality reduction.
- **Why cleaner:** it starts from the same kind of uniqueness logic that already worked for scalar observables and probability structure, and tries to apply it directly to gravity.
- **Main risk/blocker:** there is no current exact bridge showing the gravity action is uniquely fixed by that principle alone.
- **Status:** speculative.

## 5. Gauge-matter-first backreaction route

- **One-line theorem idea:** derive the source class completely from the gauge/matter stack, then derive GR as the unique backreaction law compatible with that exact matter source.
- **Uses:** native weak algebra, structural `SU(3)` closure, graph-first selector, left-handed charge matching, one-generation matter closure, three-generation structure, generation axiom boundary.
- **Why cleaner:** it could replace the current “metric from source” focus with a derivation of the allowed source stress-energy first, then gravity as the only compatible macroscopic response.
- **Main risk/blocker:** the matter stack is strong, but it does not yet force a full GR field equation on its own.
- **Status:** speculative.

## 6. Exact finite-rank source-to-metric theorem

- **One-line theorem idea:** close full GR by proving that the exact finite-rank source family already determines the full exterior metric uniquely, including the tensor lift.
- **Uses:** finite-rank gravity residual note, coarse-grained exterior law, flux-fixed matching decomposition, star-support shell projector, restricted strong-field closure synthesis.
- **Why cleaner:** it uses already-retained exact source classes and pushes the remaining gap into a uniqueness theorem rather than a new numerical fit.
- **Main risk/blocker:** the current exact finite-rank results still leave a nonzero tensor completion gap between families.
- **Status:** promising.

## 7. Direct lattice Green/resolvent route to the full metric

- **One-line theorem idea:** derive the full metric directly from the lattice Green/resolvent structure of the source operator, without first passing through the current shell boundary language.
- **Uses:** exact resolvent identities, distributed-source spacetime closure, finite-support source theorem, exact exterior harmonic field, star-support shell projector.
- **Why cleaner:** it can skip the shell/tensor boundary narrative and ask whether the exact lattice operator already contains the full metric response in closed form.
- **Main risk/blocker:** this route still needs a tensor-valued readout of the resolvent data, not just the scalar harmonic exterior.
- **Status:** speculative.

## 8. Discrete `3+1` variational action route

- **One-line theorem idea:** derive a full discrete gravitational action on the framework side whose Euler-Lagrange equations are exactly the GR field equations on the retained class.
- **Uses:** exact microscopic boundary action, exact discrete Dirichlet principle, exact shell action, same-charge bridge, static isotropic vacuum bridge.
- **Why cleaner:** it converts the problem from “match a tensor residual” into “identify the correct action functional.”
- **Main risk/blocker:** the current action is exact only for the scalar shell/bridge package, not yet for the full tensor lift.
- **Status:** speculative.

## 9. Geometric RG / projective-shape flow route

- **One-line theorem idea:** promote the projective `A1` shape law and hierarchy-style scaling structure into a genuine geometric RG flow whose fixed point is the GR tensor law.
- **Uses:** hierarchy exponent lock, `u_0` scaling rule, exact reduced shell law, exact support-side scalar observable, projective `A1` shape law.
- **Why cleaner:** it matches the pattern already seen in the gravity frontier, where exact amplitude reduction is followed by a one-parameter shape law.
- **Main risk/blocker:** the current projective law is exact only on the reduced support scalar, not as a general tensor RG theorem.
- **Status:** speculative.

## 10. Obstruction-first theorem with a minimal new primitive

- **One-line theorem idea:** prove that full GR cannot close from the current stack without one new exact tensor boundary primitive, then axiomatize that primitive cleanly.
- **Uses:** scalar-only no-go, tensor-block localization, shell projective blindness result, support-side scalar law, exact local `O_h` / finite-rank comparison.
- **Why cleaner:** if closure is impossible on the current primitive set, this route prevents indefinite looping and gives the minimum missing theorem.
- **Main risk/blocker:** this is not a closure path by itself; it is a route to a sharper theory boundary.
- **Status:** dead for direct closure, useful as a diagnostic.

## Ranked top 3

1. **Exact support-side tensor observable on the `A1 x {E_x, T1x}` block.**  
   This is the most direct clean-sheet continuation of the current framework, but it is microscopic and exact rather than shell-fit driven.

2. **Axiom-first spacetime lift from `S^3` and anomaly-forced time.**  
   This is the best non-shell alternative. It has the right structural ingredients to try to build `3+1` gravity from topology and chirality instead of from the current tensor boundary path.

3. **Exact finite-rank source-to-metric theorem.**  
   This is the strongest source-side architecture already supported by the retained stack. It is narrower than full GR today, but it is cleaner than continuing to tune tensor residuals.

## Bottom line

The current shell/tensor-boundary route is not the only plausible architecture, but it is still the most localized one we have. The cleanest alternatives are:

- support-side tensor observable first
- topology/spacetime lift second
- finite-rank source-to-metric theorem third

None of these is yet a closed full-GR proof. This memo is only a path survey, not a closure claim.
