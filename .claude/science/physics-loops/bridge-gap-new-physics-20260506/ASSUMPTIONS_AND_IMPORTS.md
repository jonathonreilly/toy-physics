# Assumption / Import Ledger — Bridge Gap New Physics Loop

**Date:** 2026-05-06
**Loop:** bridge-gap-new-physics-20260506

## A1+A2 — Retained framework axioms (only)

| ID | Statement | Status |
|---|---|---|
| A1 | Local algebra is `Cl(3)` per [`MINIMAL_AXIOMS_2026-05-03.md`](../../../../docs/MINIMAL_AXIOMS_2026-05-03.md) | retained |
| A2 | Spatial substrate is cubic lattice `Z^3` per [`MINIMAL_AXIOMS_2026-05-03.md`](../../../../docs/MINIMAL_AXIOMS_2026-05-03.md) | retained |

## Retained primitives (one-hop)

| Primitive | Statement | Authority |
|---|---|---|
| Per-site Hilbert dim | `dim_C H_x = 2`, Pauli realization | [`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](../../../../docs/CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md) |
| Canonical trace form | `Tr(T_a T_b) = δ_{ab}/2` (Gell-Mann normalization) | [`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](../../../../docs/G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md) |
| SU(3) fundamental Casimir | `C_2(1,0) = 4/3` exact | [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](../../../../docs/SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md) |
| SU(3) adjoint Casimir | `C_2(adj) = N_c = 3` exact | [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](../../../../docs/SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md) |
| Reflection positivity A11 | RP, transfer-matrix, OS reconstruction | [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| Single-clock evolution | strongly continuous unitary one-parameter group | [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](../../../../docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md) |
| Microcausality | Lieb-Robinson bound, finite-range hops | [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](../../../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) |
| V=1 Picard-Fuchs ODE | Single-plaquette Wilson integral satisfies exact rank-3 ODE | [`PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md`](../../../../docs/PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md) |
| Mixed-cumulant β⁵ | `P_full(β) = P_1plaq(β) + β⁵/472392 + O(β⁶)` exact | [`GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md`](../../../../docs/GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md) |

## Open gates / admitted-context inputs

| Item | Class | Authority |
|---|---|---|
| Staggered-Dirac realization (formerly A3) | OPEN GATE | [`MINIMAL_AXIOMS_2026-05-03.md`](../../../../docs/MINIMAL_AXIOMS_2026-05-03.md) |
| g_bare = 1 normalization (formerly A4) | OPEN GATE | [`MINIMAL_AXIOMS_2026-05-03.md`](../../../../docs/MINIMAL_AXIOMS_2026-05-03.md) |
| SU(3) gauge-group emergence | bounded (depends on staggered-Dirac gate) | [`MINIMAL_AXIOMS_2026-05-03.md`](../../../../docs/MINIMAL_AXIOMS_2026-05-03.md) |
| Physical-color identification | deferred bridge | [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md) audit_renaming 2026-05-04 |
| **Wilson plaquette action form** | **ADMITTED IMPORT** (not derived from Cl(3)) | [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](../../../../docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md) line 467 explicit |
| Heat-kernel-Wilson small-U matching | standard machinery (Menotti-Onofri 1981, Drouffe-Zuber 1983) | literature, narrow non-derivation role |
| Schur orthogonality / Lie-algebra rep theory | standard machinery | textbook, narrow non-derivation role |

## Forbidden imports (no load-bearing role)

| Item | Reason |
|---|---|
| PDG observed ⟨P⟩(β=6) ≈ 0.5934 | comparator only, NOT derivation input |
| 4D MC FSS ⟨P⟩(6) = 0.59400 ± 0.00037 | comparator only, NOT derivation input |
| PDG α_s(M_Z) = 0.1180 | comparator only |
| PDG m_H, v, M_Z, y_t | comparator only |
| Sommer scale r_0 = 0.5 fm | already admitted upstream (PR #258); inherited at admitted-tier |
| 4-loop QCD β-function | already admitted upstream; inherited |
| Fitted β_eff, fitted matching coefficients | forbidden |
| Same-surface family arguments | forbidden |
| Bessel-determinant Wilson character coefficients as derivation primitives | forbidden as motivation; allowed as definition |

## Counterfactual pass over implicit choices

For each implicit framework choice, name the alternative and the direction
the alternative opens.

| Choice | Standard | Alternative | Direction opened |
|---|---|---|---|
| Gauge action functional | Wilson | Heat-kernel, Manton, Cl(3)-volume-form | Each gives different ⟨P⟩(6); Wilson is the unexamined import |
| Gauge group | SU(3) | SU(2)×SU(2), Spin(6)≅SU(4)⊃SU(3)×U(1) | If Cl(3) tensor on adjacent sites gives larger group, U(1)_Y emerges as byproduct |
| Per-site Hilbert dim | 2 (Pauli) | 8 (full Cl(3)) | Different fermion sector content |
| Anisotropic ratio β_t/β_s | 1 (isotropic) | other ratios | Hamiltonian-limit access; per-route negative finding ([`GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md`](../../../../docs/GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md)) |
| Boundary conditions | APBC + Klein-four V | other BCs | Per-route negative finding (single-twist Z_3 ≡ PBC at L_s=2) |
| Character truncation NMAX | finite | infinite | Already exhausted as derivation lever |
| Bessel-determinant character coefficients | Wilson c_λ(β) | exp(-β·C₂/2) (HK-natural) | **Block 01-04 target** |

## Counterfactual conclusion

The single dominant unexamined choice is the **gauge action functional**.
All other counterfactuals have been investigated (per
[`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](../../../../docs/BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md))
and yield negatives or are ruled out by retained no-go theorems. The gauge
action functional is the single remaining attack lever within the framework's
existing primitives (no new axiom required — heat-kernel uses retained
Casimir; Wilson uses standard machinery; both are import-bearing in the
admitted-context sense, but heat-kernel's import is the SAME admitted-context
that already underwrites Casimir = 4/3, while Wilson's import is independent).

## A_min for Block 01

The minimal allowed premise set for Block 01 (deriving Brownian time t):

```
A_min(Block 01) = {
  A1 (Cl(3) local algebra),
  A2 (Z^3 spatial substrate),
  Tr(T_a T_b) = δ_{ab}/2 (canonical trace form, retained),
  C_2(1,0) = 4/3 (retained),
  C_2(adj) = 3 (retained),
  Schur orthogonality (standard machinery),
  Brownian motion on compact Lie groups (standard machinery),
  Heat-kernel small-U expansion (standard machinery),
  Wilson small-U expansion (standard machinery),
  g_bare = 1 (admitted-as-canonical, narrow non-derivation role)
}
```

Forbidden as derivation inputs:
```
{
  PDG/MC ⟨P⟩(6) values,
  Bessel-determinant Wilson c_λ(β) (only as definition, not as motivation),
  fitted β_eff or t,
  Sommer scale, 4-loop QCD running (already admitted upstream)
}
```
