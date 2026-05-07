# Bridge Gap — New-Physics Opening (12h Campaign Goal)

**Slug:** bridge-gap-new-physics-20260506
**Started:** 2026-05-06
**Runtime budget:** 12h unattended
**Mode:** campaign
**Worktree:** `/Users/jonreilly/Projects/Physics/.claude/worktrees/lucid-shamir-41757b`

## High-level goal

Pursue the new-physics opening identified in [`docs/BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md):
the framework's gauge action is *admitted* as Wilson, not derived from
Cl(3)/Z³. Heat-kernel is the Casimir-native alternative. The seven exhausted
routes consolidated in [`docs/BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md)
all assumed Wilson; under the framework's actually-derived action, the four
cluster-obstruction lanes (yt_ew M, gauge-scalar bridge, Higgs mass, Koide-
Brannen) are different problems.

## Block plan (12h budget, ~90m deep blocks)

### Block 01 (highest priority): Cl(3) gauge metric → Brownian time t
- **Question:** what specific Brownian time t(β) does the canonical Cl(3)
  connection normalization `Tr(T_a T_b) = δ_{ab}/2` force on the SU(3)
  gauge manifold under the framework's g_bare = 1, β = 6?
- **Method:** induced bi-invariant metric on SU(3) → Brownian motion speed
  → small-U matching to Wilson → extract t(β) at canonical normalization.
- **Target deliverable:** bounded support theorem giving exact rational
  (or transcendental closed-form) `t(β=6)` derived from A1 + A2 +
  canonical normalization, using only Schur orthogonality + standard
  Lie-algebra metric machinery as admissible standard machinery.

### Block 02: Single-plaquette ⟨P⟩_HK,1plaq(6) under derived t
- **Question:** evaluate `⟨P⟩_HK,1plaq(6) = exp(-2·t(6)/3)` using Block
  01's t(6) and the retained Casimir `C_2(1,0) = 4/3`.
- **Target deliverable:** closed-form ⟨P⟩_HK,1plaq(6), cross-validated
  against the V=1 PF ODE construction (which gives Wilson 0.4225) to
  show explicit numerical difference.

### Block 03: Thermodynamic ⟨P⟩_HK(6) under Casimir-diagonal action
- **Question:** does the multi-plaquette HK partition function close in
  closed-form via Casimir-diagonal character algebra, in contrast to
  Wilson's Bessel-determinant case?
- **Target deliverable:** either a closed-form thermodynamic ⟨P⟩_HK(6)
  evaluation, or a sharp obstruction analogous to Wilson's no-go but
  demonstrably different in structure.

### Block 04: Action-form uniqueness — does Cl(3) force HK over Wilson?
- **Question:** does the canonical Cl(3) connection normalization +
  small-a continuum matching uniquely select HK among the family
  {Wilson, HK, Manton, Cl(3)-volume-form}? Or are multiple actions
  consistent with the framework's primitives?
- **Target deliverable:** if HK uniquely forced → bounded support
  theorem closing the action-form question; if multiple consistent
  → exact negative boundary identifying the additional structural
  primitive needed to select between them.

### Block 05+ (if runtime remains): Cl(3) ⊗ Cl(3) → Spin(6) ≅ SU(4) embedding
- The framework's per-site Cl(3) tensor on adjacent sites naturally
  gives a larger group via `Cl(3) ⊗ Cl(3) ⊃ Spin(6) ≅ SU(4) ⊃ SU(3) × U(1)`.
  This is an unexamined route per round-3 action-form-derivation agent.
  Investigate whether this gives the framework's actually-derived gauge
  group (with U(1)_Y as a free byproduct).

## Hard constraints (forbidden imports)

- NO PDG observed values (⟨P⟩(6) ≈ 0.5934, M_Z, m_H, etc.) as derivation inputs
- NO lattice MC empirical measurements as derivation inputs (4D MC FSS as
  comparator only)
- NO fitted matching coefficients
- NO same-surface family arguments
- NO load-bearing literature numerical comparators
- Standard Clifford / Lie-algebra / character-expansion machinery is
  admissible standard machinery (Schur orthogonality, Casimir formulas,
  heat-kernel matching, etc.)
- Menotti-Onofri 1981, Drouffe-Zuber 1983 are admissible references for
  the heat-kernel-Wilson matching machinery (NOT for derivation values)

## Hard wording bans (per controlled vocabulary + skill protocol)

- No bare `retained` / `promoted` in branch-local Status: lines
- No `retained branch-local`, `would become retained`, `promote to retained`
- No `retained on the actual surface` when premises are conditional/admitted
- Use `bounded support theorem`, `exact support theorem`, `open`, `no-go`,
  `demotion` instead

## Stop conditions

- 12h runtime exhausted
- Corollary exhaustion (every remaining ranked opportunity is one-step
  variant of landed cycle)
- Volume cap: 5 PRs per 24h
- Cluster cap: 2 PRs per parent-row family
- Global queue exhaustion (all viable targets blocked by human judgment)

## Cross-references

- Parent: [`docs/BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md)
- Sister negative: [`docs/BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md)
- Demoted fallback: [`docs/BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md`](../../../../docs/BRIDGE_GAP_INDUSTRIAL_SDP_BATTLE_PLAN_2026-05-06.md)
- Casimir retained: [`docs/SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](../../../../docs/SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
- Wilson-as-import: [`docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](../../../../docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
- Probe script: [`scripts/probe_heat_kernel_su3_plaquette.py`](../../../../scripts/probe_heat_kernel_su3_plaquette.py)
