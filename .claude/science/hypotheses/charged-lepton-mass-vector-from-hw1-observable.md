# Hypothesis: Charged-Lepton Mass-Square-Root Vector from hw=1 Observable-Principle Kernel

## Date
2026-04-17

## Statement
On the retained `Cl(3)` on `Z^3` framework surface, the normalized
charged-lepton mass-square-root vector `v_L = (sqrt(m_e), sqrt(m_mu), sqrt(m_tau)) / ||.||`
is the unique output of the additive CPT-even source-response curvature
of `log|det(D + J)|` restricted to the retained `hw=1` triplet, evaluated on
the minimal `3+1` APBC block and Z_3-character-diagonalized by the induced
`C_{3[111]}` cycle. That unique vector has Koide `Q = (sum m) / (sum sqrt(m))^2 = 2/3`
as an exact algebraic consequence and fixes the remaining independent
mass-ratio degree of freedom to one specific algebraic function of
`alpha_LM`, matching the observed charged-lepton hierarchy without
importing any quark, lepton, or fitted mass datum.

## Prediction

Quantitative, in three layers, all of which must hold:

1. **Structural layer:** the hw=1 `M_3(C)` observable algebra admits a
   unique real ray `[v_L]` for which the source-response curvature of the
   `log|det(D + J)|` generator is stationary, CPT-even, and positive on the
   retained minimal `3+1` APBC block.

2. **Koide layer:** for that unique `v_L`, the invariant
   `Q := (|v_L|^2 dot 1) / ((v_L dot 1)^2)` evaluates to exactly `2/3` as an
   algebraic rational, not a floating-point near-miss, with the
   `(+1)`-eigenspace component `|P_+ v_L|` equal to the
   `(omega, omega^2)`-eigenspace component `|P_w v_L|` by an exact
   algebra-internal identity.

3. **Residual-ratio layer:** the position of `v_L` on the Koide cone is
   fixed by one further invariant of the observable-principle kernel,
   predicted here to be an explicit algebraic function of the canonical
   same-surface `alpha_LM = 0.0907...` and the exact Z_3 character data, and
   matching the observed
   `m_mu / m_tau = 0.0594...`
   and
   `m_e / m_mu = 0.00484...`
   within either PDG precision (if parameter-free) or an explicit
   framework-native systematic budget (if any bridge step is used).

Numerical targets, normalized:

- observed `v_L / ||.|| ~ (0.0165, 0.2369, 0.9713)`
- observed `Q ~ 0.6668` (must be `2/3 = 0.66667` exactly in the framework)
- observed `m_mu / m_tau ~ 0.0594`
- observed `m_e / m_mu ~ 0.00484`

## Falsification Criteria

Composite TOE-grade bar — any one of the following kills the hypothesis:

- **Structural kill:** the hw=1 `M_3(C)` algebra admits no real 3-vector
  satisfying all three of (stationarity, CPT-even positivity, minimal APBC
  surface) whose direction is within 1% of the observed `v_L` unit vector.
  This is a purely algebraic check and requires no numerics.

- **Koide kill:** the framework derivation yields `Q =/= 2/3` as an
  exact algebraic output. Any finite correction `Q = 2/3 + delta` with
  `delta != 0` at the theorem-output level also kills the claim, because
  the observation is `Q = 2/3` to `~10^-4` precision and the hypothesis is
  exact-theorem grade.

- **Residual-ratio kill:** the derived second independent mass ratio
  (either `m_mu / m_tau` or, equivalently, the Koide-cone position)
  disagrees with observation by more than PDG precision for a
  parameter-free derivation, or by more than the explicit
  framework-native systematic budget if any bridge step is invoked. The
  systematic budget must be stated upfront, analogous to the
  `YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md` convention on `main`.

- **Uniqueness kill:** the derivation produces a family of admissible
  vectors rather than a unique ray. This means the algebra is too
  permissive and the match is cherry-picked rather than forced, which is
  the composite null hypothesis below.

## Null Hypothesis

Composite — all three must be ruled out independently:

1. **Algebraic permissiveness:** the hw=1 `M_3(C)` algebra with only the
   `C_{3[111]}` cycle and the translation projectors admits a continuous
   family of 3-vectors compatible with the Koide relation. Therefore the
   observed match is tautological, not predictive. Must be ruled out by
   exhibiting a genuine uniqueness theorem on the ray `[v_L]` once the
   observable-principle kernel is applied.

2. **RG radiative accident:** Koide `Q = 2/3` is an accidental low-scale
   IR fixed point of the Standard Model RG running from generic UV
   boundary conditions, independent of `Cl(3)` on `Z^3`. Must be ruled
   out by showing the framework derivation is UV-anchored
   (same-surface framework evaluation at the plaquette chain) rather
   than IR fixed-point-dependent.

3. **Numerical coincidence:** the match is floating-point happenstance
   at `~10^-4`. Must be ruled out by producing `Q` as an algebraic rational
   `2/3` and the residual mass ratio as an explicit algebraic function of
   `alpha_LM` and exact character data, not as a numerical solve.

## Relevant Prior Work

Direct Koide / charged-lepton-mass prior work in this repo: **none found.**
Grep for `Koide|koide`, `charged.?lepton.{0,20}mass`, `y_tau|y_mu|y_e`,
`m_e.{0,5}m_mu` returned no hits in the mass-ratio-derivation sense.

Retained framework results that will be load-bearing inputs (each must be
re-validated top-to-bottom against its own authority runner before reuse,
per the hypothesis scope):

- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` — exact `hw=1` observable
  algebra `M_3(C) = <P_1, P_2, P_3, C_{3[111]}>`, retained no-proper-quotient
  theorem; runner `frontier_three_generation_observable_theorem.py`.
- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` — unique additive CPT-even
  scalar generator `log|det(D + J)|` on the minimal `3+1` APBC block;
  runner `frontier_hierarchy_observable_principle_from_axiom.py`. This is
  the machinery that already closed the `v = 246.282...` GeV hierarchy
  theorem and is the strongest structural precedent in the package.
- `THREE_GENERATION_STRUCTURE_NOTE.md` — the `1 + 1 + 3 + 3` orbit
  algebra and Z_3 charge assignments
  `left: 0, +1, -1 / right: 0, -1, +1`.
- `ANOMALY_FORCES_TIME_THEOREM.md` — anomaly-forced `3+1` surface on
  which the APBC block is defined.
- `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — the canonical `alpha_LM =
  <P>^(1/4)` chain used to produce the residual-ratio layer's algebraic
  input.
- `ALPHA_S_DERIVED_NOTE.md` — retained `alpha_s(v) = 0.1033...` used as
  an internal consistency cross-check against the cross-check lane.

Adjacent tools that already exist and may be cannibalized:

- `frontier_pmns_hw1_source_transfer_boundary.py` — hw=1 source/transfer
  boundary; the source side of that runner is the closest existing
  infrastructure to what the Koide attack needs.
- `frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py` —
  sole-axiom version, useful to rule out RG-accident null by showing
  UV-only data.
- `frontier_neutrino_dirac_two_higgs_canonical_reduction.py` — two-Higgs
  canonical class structure that is analogous to what the
  charged-lepton side requires.
- `frontier_mass_ratio_ckm_dual.py` and `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`
  — existence proof that the framework atlas can produce mass-ratio
  lanes (down-type quarks); demonstrates the bridge-conditioned
  extraction pattern we will want to beat in rigor.

## Proposed Experiments

Numbered, in order. Each numbered item is a theorem object with an
accompanying runner that must pass before the next item opens.

1. **Observable-algebra ray stationarity.** Symbolic derivation that on
   the retained `hw=1` triplet, the curvature of `log|det(D + J)|` with
   `J` restricted to charged-lepton-compatible sources is stationary on a
   specific 1-parameter family of real rays. Runner: new
   `frontier_charged_lepton_hw1_observable_curvature.py`, target
   `PASS=all`.

2. **Z_3 character diagonalization.** Prove that under the induced
   `C_{3[111]}` cycle the stationary family splits as
   `v = a * e_+ + b * e_w + c * e_w2` with real `a` and complex-conjugate
   `b, c`, and that CPT-even positivity forces `|b| = |c|` and a single
   real phase relation. Runner:
   `frontier_charged_lepton_z3_character_split.py`.

3. **Koide cone forcing.** Show that the stationary family
   restricted by CPT-even positivity and minimal APBC surface
   collapses to exactly the 45-degree cone
   `|P_+ v| = |P_w v|`, i.e. `Q = 2/3` exactly as an algebraic identity.
   Runner: `frontier_charged_lepton_koide_cone_forcing.py`. Success
   criterion: symbolic simplification yields `Q - 2/3 = 0` exactly, not
   numerically.

4. **Uniqueness on the cone.** Show that the further restriction
   from `log|det(D + J)|` curvature stationarity plus Z_3 character
   data plus same-surface `alpha_LM` fixes a unique ray on the
   Koide cone. Runner:
   `frontier_charged_lepton_koide_cone_uniqueness.py`. This is the
   step that kills the algebraic-permissiveness null.

5. **Residual-ratio algebraic extraction.** Evaluate the unique ray
   in the `(e_+, e_w, e_w2)` frame to extract the algebraic form of
   `m_mu / m_tau` and `m_e / m_mu` in terms of `alpha_LM` and exact
   character data. Runner:
   `frontier_charged_lepton_mass_ratio_extraction.py`. Compare to PDG
   values. Either parameter-free match at PDG precision, or explicit
   framework-native systematic budget, or the hypothesis dies.

6. **Cross-check via Z_3 character source-response (Option D).**
   Independent derivation of the same mass vector as the output of the
   exact Z_3-invariant source-response kernel on the hw=1 triplet, with
   left/right charges `(0, +1, -1)/(0, -1, +1)`. Runner:
   `frontier_charged_lepton_z3_source_response_crosscheck.py`. Success
   criterion: produces the same ray `[v_L]` as items 1-5 to symbolic
   equality, or reveals a non-trivial discrepancy that sharpens the
   structural claim.

7. **End-to-end packaged verification.** A single wrapper runner that
   imports only retained authorities (each revalidated top-to-bottom
   against its own authority runner), rebuilds the derivation from
   item 1 through item 6, and prints a single `KOIDE_DERIVED=TRUE/FALSE`
   plus `Q_exact=2/3`, the residual ratio, and deviation versus PDG.
   Runner: `frontier_charged_lepton_mass_vector_end_to_end.py`. This
   is the self-contained verification artifact for the hypothesis.

8. **Null-rejection audit.** A dedicated runner that explicitly
   exercises each leg of the composite null hypothesis:
   - algebraic permissiveness: prove uniqueness (from item 4);
   - RG accident: evaluate the derivation at two different APBC sizes
     and at the canonical framework surface versus a synthetic
     "observation-scale" deformation, show UV-anchoring;
   - numerical coincidence: print symbolic `Q - 2/3 = 0` and
     algebraic expressions for the residual ratio.
   Runner: `frontier_charged_lepton_null_rejection_audit.py`.

9. **Systematic budget.** If any bridge step is invoked (e.g. connecting
   the derived framework-scale mass ratios to PDG low-energy values via
   running), name it, compute the explicit systematic budget in the
   style of `YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md`, and publish it as
   the canonical uncertainty envelope for the derived ratios. Note:
   `CHARGED_LEPTON_MASS_VECTOR_SYSTEMATIC_BUDGET_NOTE.md`.

## Reusable Retained Inputs — Revalidation Contract

Per the hypothesis scope, every retained input must be re-validated
top-to-bottom against its authority runner before reuse. Explicit contract:

- each load-bearing runner in `Relevant Prior Work` is re-run fresh in
  the Koide attack branch;
- any failure aborts the attack and surfaces the regression in the
  wrapper runner (item 7) before any Koide-specific logic runs;
- no imported numerical constant is hardcoded: `alpha_LM`, `<P>`, and the
  Z_3 character data are recomputed from the axiom runners each time.

## Status
PROPOSED

## Next Step
Run `/first-principles` with this hypothesis as the target, to derive the
stationarity + character-split + cone-forcing theorem chain (items 1-3)
from the retained authorities, before any runner is written.
