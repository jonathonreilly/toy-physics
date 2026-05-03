# Route Portfolio — Composite-Higgs Mechanism (Cycle 20)

Five independent routes, scored on `claim-state upgrade potential`,
`hard-residual pressure`, `artifactability in single cycle`, `risk of
overclaim`, with explicit selection rationale.

## Scoring rubric (route patterns reference)

For each route, score 0-3 on:

- **U** = claim-state upgrade potential (could it close a cycle 08 obstruction?)
- **N** = novelty (new content beyond cycles 06/07/08/15/16/18?)
- **A** = artifactability within single cycle (can a runner verify it?)
- **H** = hard-residual pressure (tackles a cycle 08 obstruction directly?)
- **R** = risk of overclaim (NEGATIVE: -3 = high risk, 0 = clean)
- **B** = blast radius (multiple obstructions addressed?)

Total = U + N + A + H + R + B. Maximum theoretical = 15.

## Route A — Z3 cluster-driven mechanism

**Description.** The framework's retained Koide Z3 scalar potential
`V(m) = V₀ + (c1+c2/2)m + (3/2)m² + (1/6)m³` operates on a 1D scalar
coordinate `m = Tr(K_Z3^sel)` derived from the Clifford involution
`T_m² = I_3`. Could this Z3-symmetric scalar potential modify the
top-condensate prediction by providing a new selector that suppresses
the up-quark Yukawa magnitude? Hypothesis: Z3 operates on the
*generation index* of the up-type quark sector; the dominant
condensate is then `Z3-symmetric`, which forbids the unbalanced
top-condensate channel.

**Claim**: Z3 selector picks a *generation-symmetric* combination
`(q̄_L^1 u_R^1 + q̄_L^2 c_R^2 + q̄_L^3 t_R^3)` that has a different
mean-field condensation behavior than single-channel BHL.

**Score:**
- U = 1 (modifies cycle 08 O2 framing but doesn't close it)
- N = 2 (Z3+condensate is new structural combination)
- A = 1 (artifact would mostly be qualitative — Z3 acting on
  generation index is a structural assertion, not a calculation)
- H = 1 (only addresses cycle 08 O2; not O1 or O3)
- R = -1 (risk of overclaim: Z3 acts on Koide selected slice for
  *charged leptons*, not necessarily on the quark generation index;
  asserting it does without derivation = stretch beyond evidence)
- B = 1 (only one obstruction)

**Total: 5**

**Verdict**: weak. Z3 on its own gives 1D scalar, but the doublet
condensate needs SU(2) structure. Z3 doesn't directly address O1 or O3.
Demoted to **support component within Route B**.

## Route B — Multi-channel condensation with Z3 phase relations (SELECTED)

**Description.** Cycle 08 noted three bilinears with matching quantum
numbers: `q̄_L u_R` (Φ̃-like), `q̄_L d_R` (Φ-like), `l̄_L e_R` (Φ-like).
The framework's Koide Z3 structure gives 3-state scalar dynamics on the
selected slice — equivalent to a Z3 cyclic group acting on a triplet.
**Hypothesis**: the three matching bilinears condense
**simultaneously** with **specific Z3 phase relations** (1, ω, ω²) where
ω = exp(2πi/3). This:

1. **Spreads EWSB across three channels** (addresses cycle 08 **O2**:
   single-channel BHL prediction `m_top ~ 600 GeV` does NOT apply when
   condensation is multi-channel; the effective top Yukawa is suppressed
   by the multi-channel structure).
2. **Selects channels by Z3 representation** (addresses cycle 08 **O3**:
   the three bilinears are not arbitrary; they are precisely the three
   Z3-charged components of a single Z3-covariant composite scalar).
3. **Provides a candidate mechanism** (addresses cycle 08 **O1**: even
   though we still need the framework's strong-coupling sector to give
   a nonzero condensate magnitude, the **direction** is structurally
   forced by Z3 phase covariance).

**New structural content**:

- Identification of the Z3 triplet `(q̄_L u_R, q̄_L d_R, l̄_L e_R)` as
  the natural composite-Higgs building block.
- Z3 phase relation forces a 3-channel condensate sum
  `Φ_eff = ⟨q̄_L u_R⟩ + ω ⟨q̄_L d_R⟩ + ω² ⟨l̄_L e_R⟩` (or cyclic
  permutation thereof).
- 9-dimensional vs 1-dimensional condensate basin (8/9 vs 1/9 from
  the EW Fierz channel decomposition).
- Mass-ratio constraint: if all three condensates have the same
  magnitude, the up-, down-, and charged-lepton mass ratios at the
  EW scale acquire structural relations.
- Effective top Yukawa: dominant channel only carries
  `1/(N_z3) = 1/3` of the EWSB strength → suppression factor 1/√3
  on the BHL top-mass prediction.

**Score:**
- U = 2 (sharpens all three cycle 08 obstructions with concrete
  mechanism; full closure would require strong-coupling magnitude
  derivation, which is honestly NOT in scope)
- N = 3 (multi-channel Z3-phased condensate is genuinely new — not
  in cycles 06, 07, 08, 11, 15, 16, 17, 18)
- A = 2 (runner can verify quantum-number arithmetic for Z3 triplet,
  Z3 phase covariance, mass-ratio constraints, multi-channel
  effective Yukawa formula at exact rational precision)
- H = 3 (directly attacks all 3 of cycle 08's named obstructions
  with one mechanism — meets the corollary-churn guard since this
  introduces a NEW load-bearing premise: Z3 acts on the
  generation-index doubled up the bilinear triplet)
- R = -1 (risk: identifying Z3 from the lepton mass-tower context
  with Z3 acting on quark-bilinear generation index is a STRUCTURAL
  hypothesis, not a derivation; explicitly named as the new
  load-bearing premise to be attacked by future cycles)
- B = 3 (addresses all three cycle 08 obstructions)

**Total: 12**

**Verdict**: strongest route. Selected for execution.

**Key obstructions still named after Route B:**
- New Obstruction (NO1): need to derive that Z3 indeed acts on
  generation index of quark bilinears (not just on charged-lepton
  mass-tower). This is the **load-bearing premise** of Route B.
- New Obstruction (NO2): need to derive that the three condensate
  magnitudes are equal (Z3 phase relation gives directions, not
  magnitudes; equal magnitudes is an additional Z3-symmetry
  assertion).
- New Obstruction (NO3): need to derive the strong-coupling
  *magnitude* of the condensate (cycle 08 O1 inherits to here).

## Route C — Dimensional argument from g_2² = 1/4

**Description.** Cycle 15 retained `g_2² |_lattice = 1/(d+1) = 1/4`.
Run this through the lattice → continuum chain and check whether the
naïve top-condensate calculation (BHL) is using the wrong IR coupling.
At the lattice scale, the effective composite Yukawa
`y_eff = g_2² × (loop factor) × (UV cutoff factor)` could give a
qualitatively different prediction.

**Score:**
- U = 1 (would partially close O2 but not O1 or O3)
- N = 1 (this is essentially cycle 15's running surface re-applied;
  cycle 15 already named SU(2) staircase running as the residual)
- A = 2 (runner could compute `y_eff` from g_2² in various conventions)
- H = 1 (corollary-churn: this is one-step relabeling of cycle 15)
- R = -2 (high risk of being cycle-15-relabeling)
- B = 1

**Total: 2**

**Verdict**: corollary churn vs cycle 15. Rejected.

## Route D — Composite from cycle 06 Majorana null-space

**Description.** Cycle 06 found unique Majorana operator
`ν_R^T C P_R ν_R` on derived rep. If the heavy-neutrino Majorana sector
ALSO produces a SU(2)_L-doublet-valued condensate via seesaw mixing,
the EW scale could tie to the seesaw scale.

**Score:**
- U = 0 (cycle 06 explicitly classifies Majorana as
  `(1, 1)_0` — the SU(2)_L singlet, not doublet; no doublet
  condensate from this operator alone)
- N = 1 (combining seesaw with EWSB is a known literature pattern)
- A = 1
- H = 0 (does NOT address O1, O2, or O3 directly)
- R = -3 (high risk: cycle 06 explicitly says Majorana is gauge-singlet;
  asserting it triggers EWSB without a structural bridge = overclaim)
- B = 0

**Total: -1**

**Verdict**: structurally inconsistent with cycle 06. Rejected.

## Route E — Non-Higgs EWSB (no fundamental scalar)

**Description.** Pure dynamical EWSB without a fundamental scalar field.
Verify the unbroken combination matches `Q = T_3 + Y/2`.

**Score:**
- U = 0 (cycle 07 already gives Q = T_3 + Y/2 conditionally; this just
  re-asserts it)
- N = 0 (literature: technicolor, top-condensate, walking technicolor —
  all known)
- A = 1 (runner could enumerate non-Higgs mechanisms)
- H = 0
- R = -1 (would produce literature reproduction)
- B = 0

**Total: 0**

**Verdict**: too broad for single cycle; literature reproduction.
Rejected.

## Selection: Route B

Route B's score of **12** dominates the portfolio. It is the only route
that:

1. Tackles all three cycle 08 obstructions with one mechanism;
2. Introduces a genuinely new load-bearing premise (Z3 on quark
   bilinears) that is testable via runner;
3. Avoids corollary-churn vs cycles 15, 18;
4. Honestly names new obstructions (NO1, NO2, NO3) for what remains.

Stretch attempt output type (c) — sharpens cycle 08 with mechanism +
new obstructions. Closing derivation (a) NOT achieved on the strong-
coupling magnitude; that's the Nature-grade hard residual.

## Stuck fan-out check (workflow §7)

Per route patterns reference: before declaring no route viable, generate
3-5 orthogonal premises. The five routes above ARE the orthogonal
premises:

- A: Z3 alone (generation-index selector)
- B: Z3 + multi-channel composite (selected)
- C: dimensional / IR running
- D: seesaw mixing
- E: non-Higgs (technicolor)

Synthesis: A and B share the Z3 core, but B adds the multi-channel
composite structure that gives Z3 something to act on within the
EW-doublet sector. C is corollary churn. D is structurally inconsistent
with cycle 06. E is literature reproduction. Route B is the unique
non-rejected route.

## Selected Route B execution plan

See `ARTIFACT_PLAN.md`.
