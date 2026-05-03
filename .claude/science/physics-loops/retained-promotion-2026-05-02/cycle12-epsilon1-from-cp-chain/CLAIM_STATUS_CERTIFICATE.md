# Cycle 12 (Retained-Promotion) Claim Status Certificate — ε_1 from CP Chain Stretch Attempt

**Block:** physics-loop/epsilon1-from-cp-chain-2026-05-03
**Note:** docs/EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03.md
**Runner:** scripts/frontier_epsilon1_from_cp_chain.py
**Target row:** `dm_leptogenesis_exact_kernel_closure_note_2026-04-15`
(audited_conditional). Sharpens cycle 09's
**Obstruction 1a**: derive ε_1 from the framework's CP-violation
structure (ckm_cp_phase chain).

## Block type

**Stretch attempt (output type (c)) with two paths attempted +
named obstructions.**

The cycle attempts BOTH paths called for in the cycle 12 prompt and
documents the structural ratios derived versus the specific
obstructions to a closing derivation.

## Promotion Value Gate (V1–V5)

### V1: SPECIFIC verdict-identified obstruction this PR closes/sharpens

Quoted directly from cycle 09's PR body (PR #411):

> **1a**: derive ε_1 from CP-violation structure (ckm_cp_phase chain)

And from cycle 09's note `Obstruction 1`:

> Obstruction 1: Package constants not derived from framework
> primitives. Specific repair targets: (1a) Derive ε_1 from the
> framework's CP-violation structure. Currently
> `ckm_cp_phase_structural_identity_theorem_note_2026-04-24`
> (audited_conditional, td=117) cites unratified upstream — needs
> retention.

**This PR's stretch attempt** sharpens that obstruction by:

1. Identifying the EXACT framework-internal CP-tensor structure:
   `cp1 = -2γE₁/3`, `cp2 = +2γE₂/3` from
   `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16`.
2. Deriving the EXACT structural ratio `cp1/cp2 = -√3` from the
   chart constants `γ = 1/2, E₁ = √(8/3), E₂ = √8/3`.
3. Attempting Path A (CKM → PMNS analog) and identifying the
   PMNS-phase derivation gap as the specific obstruction:
   PMNS chart selectors (`delta_PMNS · q_+ = Q_Koide`,
   `det(H) = E_2`) remain bounded support — not retained.
4. Attempting Path B (cycle-06 Majorana null-space → ε_1 via
   `cp1, cp2`) and identifying the y_0² + α_LM mass-scale
   imports as the load-bearing forbidden-import wall.
5. Documenting three specific obstructions sharper than cycle 09's.

### V2: NEW derivation contained

The parent leptogenesis cluster TREATS cp1, cp2 as a derived
exact-source package, but does NOT trace them upstream to the
retained CP-phase / matter-content chain. This PR provides:

1. **Derivation of cp1/cp2 = -√3** as a direct algebraic
   consequence of the chart constants `(γ, E₁, E₂)`, demonstrating
   that the framework's CP channels carry an exact structural ratio
   independent of any imported scale.
2. **Numerical verification** of `cp1 = -2√6/9 ≈ -0.5443`,
   `cp2 = 2√2/9 ≈ 0.3143` matching the exact_package values to 12
   digits.
3. **Path A worked attempt**: tracing how CKM
   `(ρ, η) = (1/6, √5/6)` and `J_0 = α_s(v)³ √5 / 72` would map
   into a PMNS-sector analog. Outcome: blocked by absence of a
   retained PMNS analog of the `1+5` projector split for the
   lepton-block.
4. **Path B worked attempt**: tracing how cycle 06's unique
   `ν_R^T C P_R ν_R` Majorana operator + the framework's
   `(γ, E₁, E₂)` PMNS chart constants combine to produce ε_1.
   Outcome: structural ratio `cp1/cp2 = -√3` is exact and
   forbidden-import-clean; but absolute scale (y_0², M_1 = M_Pl
   α_LM^8) inherits boundedness.
5. **Counterfactual demonstrations**: alternative chart constants
   (e.g., γ = 1, E₁ = E₂) break `cp1/cp2 = -√3`.
6. **Three named obstructions**:
   - **O1**: PMNS chart-constant retention (γ, E₁, E₂ via
     PMNS_SELECTOR_THREE_IDENTITY_SUPPORT remains support, not
     retained).
   - **O2**: Yukawa scale `y_0² = (G_weak²/64)²` imports
     `G_weak = 0.653` as admitted unit.
   - **O3**: Mass scales `M_1 = M_Pl α_LM^8` import
     plaquette/CMT `α_LM` as admitted upstream.

This is genuine new derivation content beyond existing notes'
parenthetical comments.

### V3: Audit lane couldn't already do this from existing retained primitives + standard math machinery

The audit lane in restricted one-hop context cannot synthesize:
- The cp1/cp2 = -√3 structural-ratio derivation,
- Path A vs Path B distinguished attempts,
- Identification of the y_0² + α_LM forbidden-import wall,
- Three sharpened obstructions for future cycles,

simultaneously. Each of cp1, cp2 individually is one-hop visible,
but the structural-ratio derivation tying both to chart-constant
identities is multi-hop. The Path A vs Path B comparison requires
synthesizing cycle 06's Majorana derivation, the CKM CP-phase
theorem, the DM_NEUTRINO_EXACT_H_SOURCE_SURFACE theorem, and the
PMNS_SELECTOR_THREE_IDENTITY_SUPPORT bounded status — that's
4-hop synthesis the audit lane in one-hop scope cannot do.

### V4: Marginal content non-trivial

Yes:
- Structural ratio cp1/cp2 = -√3 is exact and arithmetically
  verifiable (not a textbook identity, not a definition restated):
  it follows from the specific structural choices γ=1/2, E₁=√(8/3),
  E₂=√8/3 — alternative choices would break it.
- Counterfactual: with γ=1, E₁=E₂=1 → cp1/cp2 = -1, not -√3.
- The two-path attempt structure produces specific obstruction
  identification not present in cycle 09.
- Path A blockage is a specific scientific finding: framework's
  CKM CP-phase chain does NOT directly map to lepton CP via a
  shared `1+5` projector — the lepton block's structure differs.

### V5: Not a one-step variant of an already-landed cycle in this campaign

| Cycle | Lane | Math |
|-------|------|------|
| 01 | matter content (anomaly) | Diophantine cubic-anomaly |
| 02 | matter content (Witten Z₂) | π_4 parity |
| 03 | observable principle | Cauchy multiplicative-additive |
| 04 | hypercharge uniqueness | Cubic in continuous Y |
| 05 | gravity (staggered) | Kogut-Susskind translation |
| 06 | Majorana null-space | synthesis 01+02+04 + null-space |
| 07 | EWSB Q = T_3 + Y/2 | EWSB derivation + Higgs ID |
| 08 | composite-Higgs | rep-theory arithmetic |
| 09 | η cosmology | numerical near-fits |
| 10 | GR atlas closure | overlap/cocycle algebra |
| 12 (this) | ε_1 from CP chain | source package → leptogenesis |

Cycle 12 is the **first cycle to connect** the source-package
structural-ratio identity (cp1/cp2 = -√3) to the leptogenesis ε_1
chain. Different math (chart-constant arithmetic + loop-function
admission + heavy-Majorana hierarchy structure), different lane
(connecting cycle 06's lepton-sector Majorana null-space to the
DM/leptogenesis cluster), and the first cycle in the campaign to
attempt the CP-chain → leptogenesis bridge.

Not a one-step variant.

## Outcome classification (per prompt)

**(c) Stretch attempt with named obstructions.**

Partial progress:
- Structural ratio `cp1/cp2 = -√3` is exact and forbidden-import-clean.
- Path B (cycle-06 → ε_1 structure) is the more promising route
  than Path A (CKM analog → PMNS).
- Three obstructions named, each with concrete repair targets.

**Not a closing derivation** because:
- y_0² and α_LM are forbidden-import-conditional inputs.
- PMNS chart constants (γ, E₁, E₂) are bounded support, not
  retained.
- The absolute scale of ε_1 is consequently bounded, not exact.

## Forbidden imports check

- η_obs (PDG / Planck observed value): NOT consumed as derivation
  input. ε_1 prediction is framework-internal.
- m_top: NOT consumed.
- sin²θ_W: NOT consumed.
- Davidson-Ibarra ceiling formula: cited as admitted-context
  literature (standard QFT comparator, role-labeled), not consumed
  as derivation input.
- Fukugita-Yanagida 1986: cited only for ε_1 formula structure
  (admitted-context external authority on heavy-Majorana
  CP-asymmetry).
- Peskin-Schroeder 1995 loop functions f_g, f_v: admitted-context
  external, role-labeled.
- y_0 (Yukawa scale via G_weak): IDENTIFIED AS LOAD-BEARING
  IMPORT BLOCKING CLOSURE — listed as Obstruction O2.
- α_LM (plaquette/CMT scale): IDENTIFIED AS LOAD-BEARING IMPORT
  BLOCKING CLOSURE — listed as Obstruction O3.
- No fitted selectors consumed.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this stretch attempt:
- Cycle 09's Obstruction 1a is sharpened to two specific
  forbidden-import obstructions (O2: y_0², O3: α_LM scale).
- The structural ratio cp1/cp2 = -√3 becomes a retained-bounded
  identity on the framework's CP-channel package.
- Future cycles can target ONE of: (a) derive y_0² from primitives,
  (b) derive α_LM mass-scale ratios from primitives, (c) promote
  PMNS chart-constant support to retained.

## Honesty disclosures

- This PR is a STRETCH ATTEMPT, not a closing derivation.
- The CKM CP-phase chain (Path A) does NOT directly map to lepton
  CP — the framework's CP-violation structure for leptons goes
  through a different path (cycle 06's Majorana null-space +
  PMNS chart, not through an analog of the 1+5 quark projector).
- The structural ratio cp1/cp2 = -√3 is a retained-bounded
  identity but the absolute scale of ε_1 inherits boundedness from
  the y_0² and α_LM imports.
- The framework's 0.928 prediction for ε_1/ε_DI is
  framework-internal; this PR does not retire that boundedness.
- Audit-lane ratification required; no author-side tier asserted.
