# Charged-Lepton Koide-Cone Attempt Note

**Date:** 2026-04-17
**Status:** exact attempt / first results — Steps 1–5 of the derivation confirmed symbolically; Step 6 (Koide-cone forcing) **open** on the minimal L_t=4 APBC block
**Script:** `scripts/frontier_charged_lepton_hw1_observable_curvature.py`
**Authority role:** first-results note for the charged-lepton Koide derivation
attacking gap G5 (charged-lepton mass hierarchy). Rigorously establishes the
algebraic layer (identities that make Koide equivalent to an equal-character-
weight condition on the retained hw=1 triplet) and honestly reports that the
three candidate forcing mechanisms (A, B, C) proposed in the derivation do not
independently close the cone-forcing step on the minimal retained surface.

## Safe statement

On the retained `Cl(3)` on `Z^3` framework surface, the runner
`frontier_charged_lepton_hw1_observable_curvature.py` **symbolically establishes**
the following five facts from the hypothesis derivation:

1. **Retained primitives are exact.** The hw=1 triplet supports the three
   translation characters `(-1,+1,+1), (+1,-1,+1), (+1,+1,-1)`, the three
   rank-1 translation projectors `P_1, P_2, P_3` resolving the identity, and
   the induced `C_{3[111]}` cycle with `C e_i = e_{i+1 mod 3}` and
   `C P_i C^{-1} = P_{i+1 mod 3}`. Together `{P_1, P_2, P_3, C}` generate
   the full 9-dimensional `M_3(C)` on `H_{hw=1}`. This is a direct
   re-validation of the three-generation observable theorem authority.

2. **Species curvature kernel has a clean closed form on L_t=4 APBC.** The
   observable-principle Matsubara sum
   `K_ii^{(spec)} = 4 \sum_\omega 1 / (m_i^2 + u_0^2 (3 + sin^2 \omega))`
   evaluates on the four APBC frequencies `\omega_n \in {\pi/4, 3\pi/4, 5\pi/4,
   7\pi/4}` to exactly `16 / (m_i^2 + (7/2) u_0^2)`. The constant `7/2` here
   is the same `7/2 = 3 + 1/2` that produces the `(7/8)^{1/4}` selector in
   the `v = 246.28 GeV` hierarchy theorem, so the charged-lepton curvature
   sits on the same retained selector surface.

3. **C_3-invariance forces a two-parameter circulant `(a, b)` form of `K`**,
   with exactly two spectral eigenvalues `\alpha = a + 2b` (trivial character)
   and `\beta = a - b` (nontrivial characters, doubled by reality). This is
   verified directly against the cycle operator, including an explicit
   algebraic eigenvector check using the primitive cube root
   `\omega = -1/2 + i \sqrt{3}/2`.

4. **Plancherel identities are exact.** For any real spectral vector
   `\lambda = (\lambda_1, \lambda_2, \lambda_3)`,
   `|\lambda|^2 = a_0^2 + 2 |z|^2` and `(\sum_i \lambda_i)^2 = 3 a_0^2`,
   where `a_0 = (\lambda_1 + \lambda_2 + \lambda_3)/\sqrt{3}` and
   `z = (\lambda_1 + \bar{\omega} \lambda_2 + \omega \lambda_3)/\sqrt{3}`.

5. **Koide-cone algebraic equivalence is exact.** The Koide relation
   `3 \sum_i \lambda_i^2 = 2 (\sum_i \lambda_i)^2` is equivalent — not
   approximately, but as an algebraic identity — to
   `a_0^2 = 2 |z|^2`. On that surface, `Q = (\sum m)/(\sum \sqrt{m})^2 = 2/3`
   exactly.

In other words, the algebraic half of the Koide story is rigorously on the
retained surface. If the physical spectral vector lands on the
`a_0^2 = 2|z|^2` cone, `Q = 2/3` holds as a theorem output.

## What this does not claim

This note does **not** claim:

- that the charged-lepton spectral vector is *forced* onto the Koide cone by
  the retained framework. The cone-forcing step (Step 6 of the derivation) is
  **open** on the minimal `L_t = 4` APBC block, and all three candidate
  mechanisms laid out in the hypothesis fail independently when evaluated
  there:

  - **Candidate A (spontaneous C_3 breaking):** the only C_3-invariant
    quadratic free energy has the form
    `F = \alpha a_0^2 + 2 \beta |z|^2`. Its stationary points under
    fixed `|\lambda|^2` are the pure-trivial axis (`z = 0`) or the pure-
    nontrivial axis (`a_0 = 0`), **unless** `\alpha = \beta`. That equality
    is itself the Candidate-B question; Candidate A does not force it.

  - **Candidate B (observable-principle character symmetry):** on the
    minimal `L_t = 4` APBC block, the off-diagonal curvature `K_{ij}` with
    `i \ne j` (the parameter `b`) evaluates to zero because the three
    hw=1 sectors sit in orthogonal translation-character eigenspaces and
    no cross-sector propagator appears at quadratic order. With `b = 0`
    the circulant becomes `a \cdot I_3`, and the spectral vector collapses
    onto the trivial-character axis (`|z| = 0`), which is **off** the
    Koide cone. Promoting the kernel to a non-minimal block where
    `b \ne 0` and `\alpha = \beta` is still forced is a genuinely open
    structural claim, not an output of the retained additive-CPT-even
    unique-generator chain on the minimal surface alone.

  - **Candidate C (L_t = 4 selector / Z_3 orbit arithmetic):** the
    arithmetic is correct: uniform `1/3`-weight averaging over the three
    Z_3 characters combined with reality-forced doubling of the
    nontrivial-character norm gives `a_0^2 = 2 |z|^2`. But the
    uniform-weight prerequisite (nonzero nontrivial-character weight in
    the kernel) is exactly Candidate B's failing half. Candidate C
    therefore closes the arithmetic step but inherits the structural
    obstruction and does not independently force the cone;

- that Koide `Q = 2/3` is a retained framework *theorem*. Until at least
  one of Candidates A, B, C is closed on a well-defined block, the Koide
  identity remains an *algebraic equivalence* of a conditional cone on
  the retained triplet, not a theorem output of the framework;

- any numerical match against observed charged-lepton mass ratios. The
  runner imports only framework-native canonical values (`\alpha_{LM}`,
  `u_0`, `\langle P \rangle`) and does not exercise the Step-7 residual-ratio
  extraction or any systematic-budget step;

- a derivation of Koide universality across sectors (down-type quarks,
  up-type quarks, neutrinos). Prediction 3 of the derivation (up-type Koide)
  is a **separate** falsifiable claim that this runner does not test;

- absorption of the physical-lattice axiom boundary. That remains on its
  retained note and is unaffected by this attempt.

## Open obstructions

The runner makes explicit the structural gaps that a successor runner must
close before the Koide cone can be promoted to a retained theorem:

1. Find a non-minimal block on which the observable-principle off-diagonal
   curvature `b = K_{12}` is nonzero, yet the character-symmetry of
   `\log |\det(D+J)|` still forces `\alpha = \beta` (equivalently
   `\phi_+ = \phi_\perp` in the Legendre-transformed `F(v)`).

2. On such a block, prove that the spectral vector is the equal-weight
   Z_3 orbit representative (not a stationary point on the trivial or
   nontrivial axis). This is the uniqueness step that would rule out the
   algebraic-permissiveness null of the hypothesis.

3. Rule out the `b = 0` degenerate limit as a physical minimum of the
   C_3-equivariant free energy — either by showing that limit is a
   saddle or unstable under the same additive-CPT-even chain.

Any one of these, if rigorously closed, promotes the charged-lepton Koide
identity from "algebraic equivalence on a conditional cone" to "theorem
output of the retained surface."

## Dependency contract

This runner is self-contained and depends on the following retained
authorities (their runners must pass before this runner is trusted; the
runner does not re-execute them, matching the lightweight-attempt scope):

- `frontier_three_generation_observable_theorem.py` — retained hw=1
  algebra `M_3(C) = \langle P_1, P_2, P_3, C \rangle`, translation
  characters, cycle structure.
- `frontier_hierarchy_observable_principle_from_axiom.py` — unique
  additive CPT-even generator `W[J] = \log |\det(D+J)| - \log|\det D|`
  and the L_t=4 APBC Matsubara structure.
- `frontier_anomaly_forces_time.py` — retained `3+1` surface on which
  the APBC block is defined.
- `frontier_plaquette_self_consistency.py` — canonical `\alpha_{LM}`,
  `u_0`, `\langle P \rangle` values used as framework-native inputs.

No observed charged-lepton masses, quark masses, Yukawas, or fitted
values are imported. All numerical constants entering the runner are
framework-native.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the algebraic layer of the
> Koide identity is an exact theorem on the hw=1 triplet: the observable-
> principle curvature kernel `K` is forced to circulant form by the induced
> `C_{3[111]}` cycle, Plancherel decomposition gives
> `|\lambda|^2 = a_0^2 + 2|z|^2`, and Koide `Q = 2/3` is equivalent to the
> equal-character-weight surface `a_0^2 = 2|z|^2`. The corresponding forcing
> step — whether the physical spectral vector lands on that surface rather
> than on the trivial-character or nontrivial-character axis — remains open
> on the minimal `L_t = 4` APBC block: all three candidate mechanisms
> (spontaneous C_3 breaking, observable-principle character symmetry,
> `L_t = 4` selector arithmetic) fail independently at the minimal-block
> evaluation, for structurally distinct reasons that this attempt note
> isolates for the successor runner.

## Validation

- `scripts/frontier_charged_lepton_hw1_observable_curvature.py`

Current state:

- `frontier_charged_lepton_hw1_observable_curvature.py`: `PASS=28`, `FAIL=0`
- `KOIDE_FORCING_RESOLVED=FALSE` (by design: the honest first-results outcome)

## Status

**PROPOSED** — attempt recorded, weakest link of the derivation explicitly
isolated and passed through to the next theorem object. Promotion to
`CHARGED_LEPTON_KOIDE_CONE_NOTE.md` requires a successor runner closing at
least one of the three obstructions listed above.
