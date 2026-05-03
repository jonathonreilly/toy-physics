# ε_1 from CP Chain — Stretch Attempt with Named Obstructions

**Date:** 2026-05-03
**Type:** stretch_attempt (output type c)
**Claim scope:** documents a worked stretch attempt at deriving the
leptogenesis CP-asymmetry parameter ε_1 from the framework's retained
CP-violation structure. Two paths are attempted (Path A: CKM CP-phase
chain → PMNS analog → lepton-sector ε_1 from heavy-Majorana
interference; Path B: cycle-06 Majorana null-space + framework's
exact source package → ε_1 via interference channels cp1, cp2).
Outcome: the structural ratio `cp1/cp2 = -√3` is exact and
forbidden-import-clean; the absolute scale of ε_1 inherits boundedness
from forbidden-import obstructions O2 (y_0² scale) and O3 (α_LM
mass scale).

**Status:** stretch attempt, audit-lane ratification required for
any retained-grade interpretation. This is not a closing derivation.

**Runner:** [`scripts/frontier_epsilon1_from_cp_chain.py`](./../scripts/frontier_epsilon1_from_cp_chain.py)

**Authority role:** sharpens cycle 09's Obstruction 1a (derive ε_1
from the framework's CP-violation structure, ckm_cp_phase chain).

## A_min (minimal allowed premise set)

- (P1, retained) Cycle 06 closing derivation:
  `SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02`
  (with-ν_R: unique `ν_R^T C P_R ν_R` operator).
- (P2, audited_conditional) `CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24`:
  retained CKM CP-phase identities `cos²(δ_CKM) = 1/6,
  sin²(δ_CKM) = 5/6, ρ = 1/6, η = √5/6, J_0 = α_s(v)³ √5/72`.
- (P3, support-grade) `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16`:
  exact source-surface package `γ = 1/2, E₁ = √(8/3), E₂ = √8/3`
  on the framework's neutrino-sector Hermitian chart.
- (P4, retained) `DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15`:
  exact heavy-basis diagonal normalization `K_00 = 2`.
- (P5, retained_bounded) Standard QFT loop functions
  `f_g(x) = √x/(x-1), f_v(x) = √x[1 - (1+x) ln((1+x)/x)]`
  (Peskin-Schroeder 1995, admitted-context external, role-labeled).
- (P6, retained_bounded) Fukugita-Yanagida 1986 ε_1 formula
  structure `ε_1 ∝ (1/8π) Σ Im[(Y_ν^† Y_ν)_{1k}^2] f(M_k/M_1)
  / (Y_ν^† Y_ν)_{11}` (admitted-context external, role-labeled).

## Forbidden imports

- **η_obs as derivation input**: not used.
- **m_top, sin²θ_W**: not used.
- **PDG values**: not used.
- **y_0 = G_weak²/64 with G_weak = 0.653**: identified as Obstruction
  O2 — admitted unit convention, load-bearing on absolute scale.
- **α_LM = α_bare/u_0 with u_0 = (PLAQ_MC)^(1/4) = 0.5934^(1/4)**:
  identified as Obstruction O3 — plaquette/CMT lattice scale,
  load-bearing on absolute scale.
- **No fitted selectors**.
- **No same-surface family arguments**.

## Background: framework's exact ε_1 formula

From `DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15`:

```text
ε_1 = |(1/(8π)) y_0² (cp1 · f_23 + cp2 · f_3) / K_00|
```

where:
- `cp1 = -2γE₁/3` and `cp2 = +2γE₂/3` are exact heavy-basis CP
  tensor channels (framework structural numbers);
- `f_23 = f_total((M_2/M_1)²)`, `f_3 = f_total((M_3/M_1)²)` are
  the standard QFT vertex+self-energy loop functions;
- `K_00 = 2` is the retained heavy-basis diagonal normalization;
- `y_0² = (G_weak²/64)²` is the Yukawa coupling-squared scale;
- `M_1, M_2, M_3` are heavy-Majorana mass-spectrum ratios in
  α_LM-units.

## Worked attempt

### Step 1: Derive the structural ratio cp1/cp2 = -√3

From P3 (DM_NEUTRINO_EXACT_H_SOURCE_SURFACE) the chart constants
are γ = 1/2, E₁ = √(8/3), E₂ = √8/3.

Substituting:

```text
cp1 = -2 · (1/2) · √(8/3) / 3 = -√(8/3)/3 = -√8/(3·√3) = -2√2/(3√3)
    = -2√6/9
cp2 = +2 · (1/2) · √8/3 / 3 = √8/9 = 2√2/9
```

Numerical:
- cp1 = -2√6/9 ≈ -0.5443310539518...
- cp2 = 2√2/9 ≈ 0.3142696805274...

Both match the exact_package values in `dm_leptogenesis_exact_common.py`
to 12 digits.

The structural ratio:

```text
cp1/cp2 = (-2√6/9) / (2√2/9) = -√6/√2 = -√3.
```

This is exact and dimensionless. It does NOT depend on y_0,
α_LM, or any imported scale.

**Counterfactual**: alternative chart constants
(γ=1, E₁=E₂=1) → cp1/cp2 = -1, not -√3. So the -√3 ratio is a
specific structural fingerprint of the (γ=1/2, E₁=√(8/3), E₂=√8/3)
chart.

### Step 2: Path A — CKM CP-phase chain → PMNS analog

From P2 (CKM_CP_PHASE_STRUCTURAL_IDENTITY) the retained CKM phase
identities are:

```text
cos²(δ_CKM) = 1/6, sin²(δ_CKM) = 5/6
ρ_CKM = 1/6, η_CKM = √5/6
ρ²_CKM + η²_CKM = 1/6
J_0 = λ⁶ A² η_CKM = α_s(v)³ √5/72
```

The structural origin is the retained `1+5` quark-block projector
split (with `w_A1 = 1/6, w_perp = 5/6`) plus the CP-radius
`r² = 1/6`.

**Question**: Does an analogous projector split + CP-radius exist
for the lepton block?

Lepton block dimension = 2×3 = 6 (same as quark, three generations
of doublets). If the analog `1+5` split + lepton CP-radius hold,
then by structural transport:

- ρ_PMNS = 1/6, η_PMNS = √5/6, sin²(δ_PMNS) = 5/6.

But this is NOT a retained derivation. The framework's PMNS sector
has:
- `PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21`: bounded
  support proposal, NOT retained.
- The selector laws `delta * q_+ = Q_Koide` and `det(H) = E_2`
  are explicitly flagged as "proposed inputs, not yet promoted".
- The recovered PMNS observables (`sin(delta_CP) = -0.990477`,
  `|Jarlskog| = 0.033084`) are heuristic multi-start search
  outputs.

So Path A produces a STRUCTURAL HYPOTHESIS (PMNS analog of CKM
projector split) but the hypothesis is not derivable from current
retained authorities. The audit-conditional CKM CP-phase theorem
itself remains audit-conditional, and the lepton-sector analog is
not retained-bounded.

**Path A outcome**: NOT closing. The CKM CP-phase chain does not
directly produce a retained PMNS phase, hence does not directly
produce a retained ε_1 input via heavy-Majorana interference.

### Step 3: Path B — cycle 06 + exact source package → ε_1

From P1 (cycle 06) the with-ν_R Majorana null-space has unique
operator `ν_R^T C P_R ν_R` — i.e., the framework's right-handed
neutrino sector admits one Majorana mass term, hence a heavy-basis
diagonalization.

From P3 (exact source package) the chart constants give cp1, cp2
with the structural ratio cp1/cp2 = -√3 (Step 1).

From P4 (K_00 = 2) the heavy-basis diagonal normalization is fixed.

From P5+P6 (admitted-context external) the standard ε_1 formula:

```text
ε_1 = |(1/(8π)) y_0² (cp1 · f_23 + cp2 · f_3) / K_00|
```

The structural-ratio identity from Step 1 + the admitted-context
loop functions give:

```text
ε_1 = (1/(8π·K_00)) · y_0² · |cp1| · |f_23 + (cp2/cp1) f_3|
    = (1/(8π·K_00)) · y_0² · (2√6/9) · |f_23 - (1/√3) f_3|
```

This is a structural decomposition: the framework predicts ε_1 as
the product of:
- a structural prefactor (1/(8π·K_00)) · (2√6/9) — exact;
- a Yukawa scale y_0² — IMPORTED (Obstruction O2);
- a loop-function combination |f_23 - (1/√3) f_3| — admitted-context
  external, depending on M_2/M_1 and M_3/M_1.

The mass ratios are:
- M_2/M_1 = (1 + α_LM/2)/(1 - α_LM/2) ≈ 1 + α_LM ≈ 1.106 (with α_LM
  imported from plaquette — Obstruction O3);
- M_3/M_1 = α_LM^(7-8) · (1/(1-α_LM/2)) = α_LM^(-1)/(1-α_LM/2)
  (so M_3 >> M_1, exponentially separated).

For M_3 >> M_1, f_3 → 0 (the f_total function decays to zero as
x → ∞). Numerically with x_3 ~ 10^4 we have f_total(x_3) ≈
1/(2√x_3) → small. So:

```text
ε_1 ≈ (1/(8π·K_00)) · y_0² · |cp1| · f_23
    = (1/(8π·2)) · y_0² · (2√6/9) · f_total((M_2/M_1)²)
```

For M_2/M_1 ≈ 1 + α_LM, x_23 ≈ 1 + 2α_LM, and
f_total(x_23) ≈ -ln(α_LM)/2 + 1 in the near-degenerate limit.

The numerical prediction matches the framework's exact_package value:
ε_1 ≈ 2.4576 × 10^(-6), giving ε_1/ε_DI ≈ 0.928.

**Path B outcome**: PARTIAL PROGRESS. The structural ratio
cp1/cp2 = -√3 is exact and forbidden-import-clean. The
m_3-decoupled limit gives ε_1 ≈ (1/(8π·K_00)) · y_0² · |cp1| · f_23.
But:
- y_0² inherits boundedness from G_weak (Obstruction O2).
- α_LM inherits boundedness from plaquette/CMT (Obstruction O3).
- The chart constants γ, E₁, E₂ inherit support-not-retained
  status from PMNS_SELECTOR_THREE_IDENTITY_SUPPORT (Obstruction O1).

So Path B produces a FORBIDDEN-IMPORT-CONDITIONAL ε_1
prediction, not a retained closing derivation.

### Step 4: Synthesis — neither path closes; both paths sharpen

Path A blocks because lepton CP-violation in the framework does
NOT inherit from quark CP-violation via a retained mechanism.
The CKM CP-phase theorem (P2) is independent of the lepton sector.

Path B blocks because the framework's predicted ε_1 absolute scale
imports y_0² and α_LM as upstream-bounded inputs.

The structural ratio cp1/cp2 = -√3 is the **retained-bounded core**
that emerges from both paths combined: it is exact, dimensionless,
and forbidden-import-clean. Promoting it from "support-grade
identity" to "retained" requires resolving Obstruction O1
(retain γ, E₁, E₂ via PMNS chart structure).

## Named Obstructions

### Obstruction O1: PMNS chart constants γ, E₁, E₂ are support-grade

The chart constants γ = 1/2, E₁ = √(8/3), E₂ = √8/3 appear in
`PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21` as
"existing chart constants" but the support note explicitly says:

> The support proposal is the three-equation system... These two
> equations are the live candidate selector laws. The support
> package keeps them explicit as proposals rather than hiding them
> under retained language.

**Specific repair target**: produce a closing derivation that the
chart constants (γ, E₁, E₂) are forced by retained PMNS-sector
structure. Connects to retained Koide character infrastructure
(`Q_Koide = 2/3`, `SELECTOR² = 2/3`) but the bridge from Koide
character to the specific chart constants is not retained.

### Obstruction O2: Yukawa scale y_0² imports G_weak

In `dm_leptogenesis_exact_common.py`:

```python
G_WEAK = 0.653
Y0 = G_WEAK**2 / 64.0
Y0_SQ = Y0**2
```

`G_WEAK = 0.653` is an admitted unit convention (gauge coupling at
the weak scale). It does NOT appear in any retained derivation
chain as a structural number — it's a phenomenological input.

**Specific repair target**: derive the Yukawa scale y_0² from
framework primitives, e.g., from cycle 04's hypercharge structure +
cycle 02's SU(2) Witten parity + the SU(2) gauge coupling at the
EW symmetry-breaking scale. This is a substantial multi-step
derivation chain.

### Obstruction O3: Mass scales M_1, M_2, M_3 import α_LM

From `dm_leptogenesis_exact_common.py`:

```python
PLAQ_MC = 0.5934
u0 = PLAQ_MC ** 0.25
g_bare = 1.0
alpha_bare = g_bare**2 / (4.0 * PI)
ALPHA_LM = alpha_bare / u0
```

`PLAQ_MC = 0.5934` is the canonical plaquette-MC value, an
admitted lattice-scale convention. The mass spectrum
M_1 = M_Pl · α_LM^8, M_2 = M_Pl · α_LM^8 · (1+α_LM/2),
M_3 = M_Pl · α_LM^7 then inherits the α_LM scale.

**Specific repair target**: derive α_LM mass-scale ratios
(in particular M_2/M_1 and M_3/M_1) from framework primitives
without admitting plaquette-MC or CMT scales. Connects to the
plaquette/CMT retained surface — but plaquette MC is itself
support-grade.

## What this claims

- (P1) The structural ratio `cp1/cp2 = -√3` is exact and
  forbidden-import-clean on the framework's CP-channel package.
- (P2) Path A (CKM CP-phase chain → PMNS analog) does NOT yield
  a retained ε_1 input — explicitly named obstruction.
- (P3) Path B (cycle 06 + exact source package → ε_1 formula) is
  the more promising route, but absolute-scale closure requires
  resolving Obstructions O2 and O3.
- (P4) Three named obstructions documented with specific repair
  targets.

## What this does NOT claim

- Does NOT derive ε_1 absolute scale from primitives (y_0² and
  α_LM are forbidden-import-conditional).
- Does NOT close cycle 09's Obstruction 1a — sharpens it into
  three sub-obstructions.
- Does NOT promote any author-side tier; audit-lane ratification
  required.
- Does NOT consume any PDG observed value as derivation input.
- Does NOT promote PMNS chart constants from support to retained.

## Cited dependencies

- (P1, retained) `SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02`
  (cycle 06).
- (P2, audited_conditional)
  `CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24`.
- (P3, support-grade)
  `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16`.
- (P4, retained)
  `DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15`.
- (P5, admitted-context external) Peskin-Schroeder 1995 loop
  functions f_g, f_v.
- (P6, admitted-context external) Fukugita-Yanagida 1986 ε_1
  formula structure.
- (Obstruction context) `PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21`
  (support, not retained).
- (Cycle 09 parent) `ETA_COSMOLOGY_DERIVATION_STRETCH_ATTEMPT_NOTE_2026-05-02`
  (sharpens its Obstruction 1a).
- (Leptogenesis chain)
  `DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15`,
  `DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16`.

## Forbidden imports check

- η_obs not consumed.
- m_top not consumed.
- sin²θ_W not consumed.
- y_0 (G_weak): IDENTIFIED AS Obstruction O2.
- α_LM (plaquette/CMT): IDENTIFIED AS Obstruction O3.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention beyond
  the explicitly-named O2/O3.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_epsilon1_from_cp_chain.py`](./../scripts/frontier_epsilon1_from_cp_chain.py)
verifies:

1. Exact algebraic identities for cp1, cp2:
   - cp1 = -2√6/9 (matching exact_package to 12 digits)
   - cp2 = 2√2/9 (matching exact_package to 12 digits)
2. **Structural ratio cp1/cp2 = -√3** verified to 12 digits.
3. Counterfactual: alternative chart constants (γ=1, E₁=E₂=1) →
   cp1/cp2 = -1, demonstrating the -√3 ratio is a specific
   structural fingerprint of (γ=1/2, E₁=√(8/3), E₂=√8/3).
4. CKM CP-phase identities (Path A):
   - cos²(δ_CKM) = 1/6, sin²(δ_CKM) = 5/6 verified.
   - η_CKM = √5/6 verified.
   - Path-A obstruction: PMNS analog not retained.
5. Path B numerical decomposition:
   - ε_1 prefactor (1/(8π·K_00)) · (2√6/9) computed exactly.
   - M_3 >> M_1 limit: f_3 → 0 verified.
   - ε_1 prediction matches framework's 2.4576 × 10^(-6) when
     y_0² and α_LM are accepted as imports.
6. Three named obstructions explicitly recorded.
7. Forbidden-import audit: y_0 and α_LM flagged as conditional
   inputs; no PDG values consumed; no fitted selectors.

## Cross-references

- [`ETA_COSMOLOGY_DERIVATION_STRETCH_ATTEMPT_NOTE_2026-05-02.md`](ETA_COSMOLOGY_DERIVATION_STRETCH_ATTEMPT_NOTE_2026-05-02.md) —
  cycle 09 parent; Obstruction 1a is sharpened by this PR.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) —
  retained CKM CP-phase chain (Path A).
- [`SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md`](SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md) —
  cycle 06 closing derivation, Majorana null-space.
- [`DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md`](DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md) —
  exact source package (γ, E₁, E₂).
- [`DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md) —
  K_00 = 2 normalization.
- [`DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md`](DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md) —
  framework's standard ε_1 formula and exact_package values.
- [`PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md`](PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md) —
  PMNS chart-constant support (Obstruction O1).
