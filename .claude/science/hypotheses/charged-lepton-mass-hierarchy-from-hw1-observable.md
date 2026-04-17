# Hypothesis: Charged-Lepton Mass-Square-Root Vector from hw=1 Observable-Principle Kernel

## Date
2026-04-17

## Statement

On the retained `Cl(3)` on `Z^3` framework surface, the normalized
charged-lepton mass-square-root vector
`v_L = (√m_e, √m_μ, √m_τ) / ||·||` is the unique output of the
additive CPT-even source-response curvature of `log|det(D + J)|`
restricted to the retained `hw=1` triplet, evaluated on the minimal
`3+1` APBC block and `Z_3`-character-diagonalized by the induced
`C_{3[111]}` cycle. If that unique vector satisfies Koide
`Q = (Σ m) / (Σ √m)² = 2/3` as an exact algebraic consequence and
fixes the remaining independent mass-ratio degree of freedom to one
specific algebraic function of the retained coupling `α_{LM}`, the
hypothesis is confirmed; otherwise it is falsified.

## Prediction

Three layers must all hold:

1. **Structural.** The `hw=1` `M_3(ℂ)` observable algebra admits a
   unique real ray `[v_L]` for which the source-response curvature
   of the `log|det(D + J)|` generator is stationary, CPT-even, and
   positive on the retained minimal `3+1` APBC block.

2. **Koide.** For that unique `v_L`, the Koide invariant
   `Q ≡ (|v_L|² · 1) / (v_L · 1)²` evaluates to exactly `2/3` as an
   algebraic rational, not a floating-point near-miss, with the
   `(+1)`-eigenspace component `|P_+ v_L|` equal to the
   `(ω, ω²)`-eigenspace component `|P_ω v_L|` by an exact
   algebra-internal identity.

3. **Residual ratio.** The position of `v_L` on the Koide cone is
   fixed by one further invariant of the observable-principle
   kernel, predicted to be an explicit algebraic function of the
   canonical same-surface `α_{LM} = 0.0907…` and the exact `Z_3`
   character data, and matching the observed
   `m_μ / m_τ = 0.0594…` and `m_e / m_μ = 0.00484…` within either
   PDG precision (if parameter-free) or an explicit framework-native
   systematic budget (if any bridge step is used).

## Falsification Criteria (composite)

Any one of the following kills the hypothesis:

- **Structural kill.** The `hw=1` `M_3(ℂ)` algebra admits no real
  3-vector satisfying all three of (stationarity, CPT-even
  positivity, minimal-APBC surface) whose direction is within 1% of
  the observed `v_L` unit vector.

- **Koide kill.** The framework derivation yields `Q ≠ 2/3` as an
  exact algebraic output. Any finite correction `Q = 2/3 + δ` with
  `δ ≠ 0` at the theorem-output level kills the claim (observed `Q
  = 2/3` to `~ 10^{−4}` precision, and the hypothesis is exact-
  theorem grade).

- **Residual-ratio kill.** The derived second independent mass
  ratio disagrees with observation by more than PDG precision for a
  parameter-free derivation, or by more than the explicit
  framework-native systematic budget if any bridge step is invoked.

- **Uniqueness kill.** The derivation produces a family of
  admissible vectors rather than a unique ray — the algebra is too
  permissive and the match is cherry-picked rather than forced.

## Null Hypothesis (composite)

Three nulls to rule out independently:

1. **Algebraic permissiveness.** The `hw=1` `M_3(ℂ)` algebra with
   the `C_{3[111]}` cycle and the translation projectors admits a
   continuous family of 3-vectors compatible with Koide, so the
   match is tautological, not predictive. Ruled out only by a
   genuine uniqueness theorem on the ray `[v_L]`.

2. **RG radiative accident.** Koide `Q = 2/3` is a low-scale IR
   fixed-point of Standard Model RG running from generic UV
   boundary conditions, not a framework output. Ruled out only by
   showing the derivation is UV-anchored at the retained same-
   surface level rather than IR fixed-point-dependent.

3. **Numerical coincidence.** The match is floating-point
   happenstance at `~ 10^{−4}`. Ruled out only by producing `Q` as
   an algebraic rational `2/3` and the residual mass ratio as an
   explicit algebraic function of `α_{LM}` and exact character
   data.

## Outcome

This hypothesis resolves **negatively** on the retained framework
surface (see `charged-lepton-koide-cone-2026-04-17.md` derivation
chain and the review-note package). The structural equivalence
`Q = 2/3 ⟺ a_0² = 2|z|²` is rigorously established as an algebraic
identity on the `hw=1` triplet (Theorem 1), but the cone-forcing
step fails on the retained surface: six structural no-gos eliminate
every retained non-Higgs-Yukawa mechanism, and three framework-
derives routes close negatively, leaving three sharply-named
missing primitives for future retention.

The charged-lepton sector closes via observational pin at the same
`retained-map-plus-observational-promotion` class as the retained
neutrino-mixing closure, with strict-review verdict
`TRUE_NO_PREDICTION`.

## Relevant Prior Work

Retained framework results that are load-bearing inputs (each
independently re-validated via its authority runner):

- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` — exact `hw=1`
  observable algebra.
- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` — unique additive
  CPT-even scalar generator.
- `DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md` — Γ_1
  definition and retained second-order return identity on `hw=1`.
- `ANOMALY_FORCES_TIME_THEOREM.md` — retained `3+1` surface.
- `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — retained `α_{LM}`,
  `u_0 = ⟨P⟩^{1/4}`, etc.

No prior Koide-specific work was found in the repo at the time of
this hypothesis; the review-note package constitutes the first
systematic attack.

## Proposed Experiments

1. **Observable-algebra ray stationarity.** Symbolic derivation on
   the retained `hw=1` triplet. Runner target:
   `scripts/frontier_charged_lepton_observable_curvature.py`.

2. **Z_3 character diagonalization.** Character decomposition under
   `C_{3[111]}`. Runner target covers this within the above.

3. **Koide cone forcing.** Symbolic test of `|P_+ v| = |P_ω v|`.

4. **Uniqueness on the cone.** Kills the algebraic-permissiveness
   null.

5. **Residual-ratio algebraic extraction.**

6. **Sectoral universality cross-check.** Test across charged
   leptons, down-type quarks, up-type quarks.

7. **End-to-end packaged verification.** Single wrapper importing
   only retained authorities.

8. **Null-rejection audit.** Explicit exercise of each leg of the
   composite null.

9. **Systematic budget.** Named if any bridge step is invoked.

## Reusable Retained Inputs — Revalidation Contract

Every retained input is independently re-validated against its
authority runner before reuse; no imported numerical constant is
hardcoded. Runners pass on live `main` at the time of writing.

## Status
RESOLVED (negative on retained surface; see review-note package).

## Next Step

See `CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md` for
the consolidated review package and
`charged-lepton-koide-cone-2026-04-17.md` for the theorem-level
derivation chain.
