# No-Go Ledger — Bridge Gap New Physics Loop

**Date:** 2026-05-06
**Loop:** bridge-gap-new-physics-20260506

## Globally retired routes (do NOT re-run)

Per [`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md),
the following seven routes are formally exhausted as Resolution-A levers
*assuming Wilson SU(3) Haar*:

| # | Route | Why exhausted |
|---|---|---|
| 1.1 | V≥2 Picard-Fuchs ODE lift | Rank explodes; finite-Λ ≠ thermodynamic limit |
| 1.2 | APBC Z_3 spatial twist + L_s ≥ 3 | Single-twist ≡ PBC; multi-direction shifts wrong way; L≈17 needed |
| 1.3 | SDP + Migdal-Makeenko on V-invariant block | Block too small for non-trivial MM; needs L_s ≥ 4 |
| 1.4 | Cl(3) HS + Klein-four positivity refinement | Wilson plaquette is grade-0 scalar; empty for ⟨P⟩ |
| 1.5 | RP-A11 cluster inequality | RP preserved by every β⁶-completion; gap ~1900× ε_witness |
| 1.6 | V-singlet temporal projection on ρ_(p,q)(6) | V acts on temporal Matsubara, not spatial (p,q) |
| 1.7 | Composite framework-unique levers (meta-analysis) | Each asset reduces to fermion-side, convention-fixing, or one-coefficient strong-coupling upgrade |

**Critical observation:** all seven routes assumed standard SU(3) Wilson
Haar as the gauge action. The new-physics opening identified in
[`BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md)
challenges that assumption — Wilson is admitted-as-import, not derived.

The seven exhausted routes do NOT exhaust ⟨P⟩_framework(6) under a
*different* (Cl(3)-native) gauge action.

## Other relevant retired no-gos

| Route | Authority |
|---|---|
| Constant-lift `P(β) = P_1plaq(Γ·β)` | [`GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`](../../../../docs/GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md) — Γ_cand = 1.555 incompatible with strong-coupling slope |
| Anisotropic Wilson via Cl(3) pseudoscalar / staggered-η | [`GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md`](../../../../docs/GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md) — neither mechanism forces orientation-dependent coupling |
| Source-sector Perron at L_s=2 alone | [`SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md`](../../../../docs/SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md) — gap 543× ε_witness, structurally fixed |
| Direct quenched ⟨P⟩_Wilson(β=6) closure | [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](../../../../docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md) — distinct β⁶-completions, no retained primitive distinguishes |
| Perron-Jacobi underdetermination | [`GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md`](../../../../docs/GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md) |
| Framework-point underdetermination | [`GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md`](../../../../docs/GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md) |

## Live attack lever (the new-physics opening)

**Gauge action functional derivation.** The framework's actual derived
gauge action is the missing primitive. Heat-kernel `S_HK = -log P_t(U)`
is the Casimir-natural alternative; Brownian time `t = t(β)` is forced
by canonical Cl(3) connection normalization at the framework's β = 6.

Block 01 of this loop derives `t(β=6)`. Subsequent blocks evaluate
single-plaquette and thermodynamic ⟨P⟩_HK(6) under the derived t.
