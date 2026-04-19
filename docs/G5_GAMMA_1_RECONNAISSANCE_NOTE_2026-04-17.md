# G5 / Γ_1 Reconnaissance Note

**Date:** 2026-04-17
**Status:** preparatory reconnaissance note — extracts the exact retained definition of `Γ_1`, the Dirac-bridge theorem's first-order and second-order claims on the hw=1 triplet, and the precise form of the charged-lepton-mass sub-object that any G5 closure must determine. Written in the main session while the Anthropic rate limit prevented spawning a dedicated Agent-10 runner.
**Authority role:** reconnaissance / scope-sharpening note for the next G5 attack lane on the retained `Γ_1` structure. Does **not** claim any closure, any new theorem, or any promotion; strictly narrows the target.

## Motivation

Agent 9's test `G5_CLOSES_VIA_G1_H = NO_NATURAL_MATCH`
([G5_VIA_G1_H_CHARGED_LEPTON_NOTE.md](./G5_VIA_G1_H_CHARGED_LEPTON_NOTE.md))
routed the G5 attack away from the G1 retained affine Hermitian `H(m, δ, q_+)`
and toward the separate retained object `Γ_1`. This note extracts what `Γ_1`
actually is on `main` by reading its canonical authority:

- [DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
  — the canonical retained definition of `Γ_1`.
- [G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md](./G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md)
  — how `Γ_1` is used in the G1 closure.

## The exact retained definition of `Γ_1`

From the Dirac-bridge theorem:

1. **Ambient space.** `Γ_1` lives on `C^16`, the full staggered Cl(3) + chirality
   carrier space on one retained lattice site. Not on `H_hw=1` directly.

2. **Family.** `Γ_1` is the weak-axis-1 element of the retained local spatial
   Higgs family
   ```
   M(phi) = phi_1 Γ_1 + phi_2 Γ_2 + phi_3 Γ_3
   ```
   with `Γ_i` the three spatial Clifford-vector generators on `C^16`.

3. **Exact properties.**
   - `Γ_1` is Hermitian.
   - `Γ_1^2 = I_16`.
   - `{Γ_1, γ_5} = 0` (chiral off-diagonal).
   - `P_L Γ_1 P_L = P_R Γ_1 P_R = 0`.

4. **EWSB selection.** After the exact selector `V_sel = 32 Σ_{i<j} φ_i² φ_j²`
   picks axis minima at `e_1, e_2, e_3`, the retained branch-convention axis
   is axis-1, so `M_weak = Γ_1`.

5. **Exclusion of `Xi_5`.** `Xi_5` commutes with `γ_5` (chirality-preserving)
   and is therefore not a post-EWSB Dirac Yukawa surface; `Γ_1` wins on the
   local chiral surface.

## What the Dirac-bridge theorem says about hw=1 — the critical subtlety

The Dirac-bridge theorem proves TWO things about `Γ_1` on the generation
triplet `T_1 ⊂ C^16` (i.e. the retained `hw=1` triplet):

**Claim 1 (first-order vanishing).**
```
P_{T_1} Γ_1 P_{T_1} = 0.
```
The direct restriction of `Γ_1` to the hw=1 triplet is **identically zero**.

**Claim 2 (second-order unit return).**
```
P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} = I_3.
```
The effective second-order return operator on `T_1`, with the intermediate
state running through the on-site singlet `O_0` plus the weight-2 triplet
`T_2`, is the identity on the three-generation space.

### The correct G5 target after this reading

**The charged-lepton effective Dirac operator on the hw=1 triplet is NOT
`Γ_1` itself. It is a second-order (or higher) effective operator whose
leading piece is `I_3`.**

At the order the Dirac-bridge theorem computes, the three generations are
mass-degenerate. Physical charged-lepton masses `(m_e, m_μ, m_τ)` must come
from **corrections to this leading-order identity**. Those corrections must:

1. Break the `I_3` degeneracy into three distinct eigenvalues.
2. Preserve the axis-basis diagonality (because G1 / Physicist-H's
   `U_e = I_3` bridge depends on it).
3. Be sourced by retained framework objects (no post-axiom invention).

## Implication for G5

Agent 9's candidate list needs to be updated with this refined picture:

**Old formulation** (Agent 9 G5 status note): "what retained primitive fixes
the three diagonal entries of `Γ_1`?"

**Corrected formulation** (after this reconnaissance): "what retained
framework corrections to the second-order effective return
`P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1}` break the leading-order `I_3`
degeneracy into a diagonal mass matrix `diag(m_e, m_μ, m_τ)` that
satisfies Koide `Q = 2/3`?"

This is an important structural sharpening. The "three diagonal entries"
language in Agent 9's note is *imprecise* — `Γ_1`'s direct restriction to
`T_1` is zero. The actual target is the **perturbative structure of the
second-order return**.

## Known precedent on main — the analogous neutrino-sector blocker

The same Dirac-bridge theorem already identifies an analogous open problem
on the **neutrino** side:

> **Still open** (from [DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)):
> derive the neutrino-sector base normalization and suppression law for the
> effective second-order `T_1` return induced by `Γ_1`, strong enough to
> justify or refute the candidate scale `y_ν ∼ α_LM^2`.

So the neutrino side has an open **normalization + suppression theorem**
for the second-order return. The charged-lepton side needs the **analogous
theorem with generation-resolved eigenvalues** — not a single suppression
scale `y_ν`, but three distinct `(y_e, y_μ, y_τ)` values.

## Candidate deployment primitives (refined from Agent 9)

With the second-order-return picture in hand, the three candidate
deployment primitives refine as follows:

**Candidate Γ-1 (refined): Casimir deployment at second order.** Agent 6's
exact `(C_F − T_F)^{−1/4} = (6/5)^{1/4}` identity is a color-sector
statement (SU(3)_c Casimirs). For CHARGED LEPTONS (color-singlet), `C_F`
and `T_F` in SU(3)_c both vanish. The lepton-side analogue would have to
use SU(2)_L × U(1)_Y Casimirs instead. Candidate relations to probe:
- SU(2)_L: `C_F^{(2)} = 3/4`, `T_F^{(2)} = 1/2`, `C_A^{(2)} = 2`.
- `C_F^{(2)} - T_F^{(2)} = 1/4`.
- Hypercharge combinations per species on hw=1: the hw=1 species carry
  distinct lattice-translation characters (see Agent 2 Z_3 cross-check),
  but share the same SM hypercharge within a sector. So direct Casimir
  insertion is species-blind on hw=1 unless it's weighted by something
  else.

Tentative conclusion: naive lepton-Casimir deployment is likely blocked by
the same taste ⊗ species orthogonality theorem that killed Agent 7's
SU(2)_L lane. This candidate is **likely negative**.

**Candidate Γ-2 (refined): Higgs-VEV dressing of the second-order return.**
The second-order return runs through `P_{O_0} + P_{T_2}`. If the Higgs VEV
introduces a species-dependent propagator weight at that intermediate step,
the return matrix breaks away from identity. Concretely: the Higgs family
`M(φ)` at the axis point `e_1` gives `M = Γ_1`, but *fluctuations* around
that axis produce species-resolved corrections. The retained
`V_sel = 32 Σ_{i<j} φ_i² φ_j²` selector is a SCALAR on the Higgs family —
it's species-democratic. The candidate is: find a retained
**species-resolved** Higgs object on the hw=1 triplet that propagates
through `P_{O_0} + P_{T_2}` with distinct weights per generation.

**Candidate Γ-3 (refined): Joint PMNS + Koide pinning through G1's
retained H.** Both the neutrino `H(m, δ, q_+)` and the charged-lepton
effective return live on the same hw=1 algebra. A joint-source theorem
would claim that pinning the same retained source simultaneously fixes
`(H eigenvectors) → PMNS angles` AND `(Γ_1 effective second-order
eigenvalues) → Koide ratio`. This requires identifying the retained
source structure shared by both operators.

## Outstanding questions a resumed Agent 10 must answer

1. **Is the second-order return on `T_1` really identity, or does the
   Dirac-bridge theorem only prove it up to an overall normalization?**
   Read the runner `scripts/frontier_dm_neutrino_dirac_bridge_theorem.py`
   carefully to see the exact verified identity.

2. **What retained objects beyond `Γ_1, P_{O_0}, P_{T_2}` appear in the
   expanded second-order expression before the identity simplification?**
   Those are candidate deployment primitives.

3. **Does the retained `V_sel` selector or its Hessian at `e_1` carry
   species-resolved information?** `V_sel` is at fourth order in `φ`;
   its Hessian at `e_1` may couple species asymmetrically through the
   `Γ_1` algebra.

4. **What is the retained relation between the Higgs scale `v` and the
   charged-lepton sector?** The `v = 246.28 GeV` hierarchy theorem is
   retained; it sets the overall lepton mass scale but not the ratios.
   Agent 6's `Q_d/Q_ℓ` identity exists because the ratios involve only
   dimensionless Casimirs. What's the lepton-sector dimensionless
   invariant?

5. **If the answer to (4) is "there is no retained lepton-sector
   dimensionless invariant that resolves the generation index",** then
   G5 requires an actual new retained object on `main`, and the
   lepton-Koide value `Q_ℓ = 2/3` is currently at best an *unretained*
   observational fact. State that outcome as the clean honest verdict.

## Exactly-sized next Agent-10 brief

When Anthropic rate limits reset, the resumed Agent-10 should:

1. Read this reconnaissance note + the Dirac-bridge theorem note + the
   G1 Physicist-H closure note.
2. Read `scripts/frontier_dm_neutrino_dirac_bridge_theorem.py` for the
   exact verified identities.
3. Symbolically construct the second-order effective return operator on
   `T_1` expanded in Higgs fluctuations `φ = e_1 + ε`.
4. Expand to O(ε²) and identify the species-resolved structure.
5. Test whether the resulting perturbed diagonal satisfies Koide at the
   V_sel-fourth-order level or a retained higher-order extension.
6. Produce a verdict in the four-outcome format: `CLOSES_G5 / PARTIAL /
   OPEN / UNDERDETERMINED` per the original Agent-10 brief, corrected to
   reflect the second-order-return formulation.

## Dependency contract

- `frontier_dm_neutrino_dirac_bridge_theorem.py` must PASS on live main
  (runner for the `Γ_1` definition).
- `frontier_g1_physicist_h_pmns_as_f_h.py` must PASS on live main
  (runner for G1's use of `Γ_1`).
- Agent 9's runner `frontier_g5_via_g1_h_charged_lepton.py` must be the
  scope-predecessor (already established).

## What this note does not claim

- No closure of G5.
- No promotion of any relation to retained theorem status.
- No new framework axiom or operator.
- No quantitative result — this note is strictly scope-reconnaissance.

## Status

**RECONNAISSANCE ONLY.** Main-session prep for the rate-limited Agent 10
retry at ~1pm EDT 2026-04-17.
