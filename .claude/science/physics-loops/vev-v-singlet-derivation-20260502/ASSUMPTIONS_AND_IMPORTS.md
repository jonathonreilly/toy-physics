# ASSUMPTIONS AND IMPORTS — VEV V-Singlet Derivation Campaign

**Date:** 2026-05-02

This ledger lists what the campaign treats as **retained framework**, what is
**admitted bridge** (and which bridge the H2 reformulation aims to retire),
what is **forbidden import**, and what is **comparator-only**.

## A. Retained framework primitives (load-bearing, no admission)

| # | Primitive | Authority |
|---|---|---|
| A1 | Local algebra `Cl(3)` | `MINIMAL_AXIOMS_2026-04-11.md` (A1) |
| A2 | Spatial substrate `Z³` | `MINIMAL_AXIOMS_2026-04-11.md` (A2) |
| A3 | Finite local Grassmann / staggered-Dirac partition | `MINIMAL_AXIOMS_2026-04-11.md` (A3) |
| A4 | Canonical normalization `g_bare = 1`, plaquette/u_0 surface, minimal APBC hierarchy block | `MINIMAL_AXIOMS_2026-04-11.md` (A4) |
| A5 | Klein-four V = Z₂ × Z₂ acts on APBC temporal phases `z → z, -z, z*, -z*` | derived from A1-A4 (APBC structure) |
| A6 | Action `S` is V-invariant on the minimal `L_s = 2` APBC block | derived from A3 (staggered-Dirac action structure) |
| A7 | Exact closed-form determinant on `L_s = 2` APBC block: `\|det(D + m)\| = ∏_ω [m² + u_0²(3 + sin²ω)]^4` | `HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md` (Theorem) |
| A8 | Klein-four orbit closure on APBC temporal phases: `L_t=2` is unresolved sign pair, `L_t=4` is the unique minimal **resolved** closed orbit, `L_t > 4` splits | `HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md` + `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` Theorem 4 |
| A9 | Kernel ratio `A(L_t = 2) / A(L_t = 4) = 7/8` (exact algebraic identity from sum over Matsubara modes at sin²ω = 1 vs sin²ω = 1/2) | derived from A7 (direct calculation) |
| A10 | `Z` (partition function) is V-invariant when `S` is V-invariant (standard Haar/Grassmann measure invariance) | standard finite-dim Grassmann + V-equivariant integration |

## B. Admitted bridges in `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE` (the 5 from cycle 8 / PR #267)

| # | Bridge | Status under H2 reformulation |
|---|---|---|
| B1 | Scalar additivity: `W[J_1 ⊕ J_2] = W[J_1] + W[J_2]` | **TARGETED FOR RETIREMENT** — replaced by extensivity of `f_vac` (intensive per spacetime volume), which follows from `Z` factorizing on independent subsystems and `f_vac = -1/V log Z` |
| B2 | CPT-even phase blindness: `W` depends on \|Z\|, not phase | **TARGETED FOR RETIREMENT** — replaced by real-positivity of `Z` (staggered det D is positive real on real masses); no phase ever appears |
| B3 | Continuity / minimal regularity | **TARGETED FOR RETIREMENT** — replaced by analyticity of `Z[J]` in `J` (finite-dim Grassmann is polynomial in `J`, hence analytic) |
| B4 | Normalization choice | **MAY RETIRE** to natural zero of `f_vac` (ground-state energy density at zero source); worst case stays as a simple convention |
| B5 | Electroweak hierarchy baseline import: `M_Pl · α_LM^16 = 254.6432... GeV` | **NOT TARGETED** in this campaign — separate lane; depends on plaquette/`α_LM` chain |

## C. New admissions introduced by H2 reformulation (must be smaller than B1-B3)

| # | Admission | Why it is smaller than B1-B3 |
|---|---|---|
| C1 | The physical EW vacuum scale `v` is identified with the Casimir-like coefficient `v² = -∂²f_vac/∂m²\|_{m=0}` of the V-invariant free-energy density `f_vac` w.r.t. a homogeneous V-singlet mass source `m` | This is essentially the standard *definition* of the EW order-parameter scale as the curvature of the effective potential at the origin (matched to the Higgs-like sector). It replaces B1+B2+B3 with a single *physical identification* — and that identification is closer to standard EFT language. The framework already defines the physical EW order parameter the same way; H2 makes that definition the load-bearing primitive instead of a downstream consequence of W. |
| C2 | The vacuum at `m = 0` is V-singlet (Klein-four respects the unbroken sector) | This is consistent with A6 (action V-invariance) and is the standard statement that an unbroken global symmetry of the action is also a symmetry of the vacuum on a finite-volume Klein-four-symmetric block (no spontaneous breaking on the finite minimal block). Provable, not admitted. |

H2 is a strict reduction in admissions IF C1 is judged closer to a *definition*
than a *bridge*. If audit returns "C1 is itself a bridge of comparable
load-bearing weight to B1+B2+B3 combined," the reformulation is at best a
sideways move. Risk noted.

## D. Forbidden imports

- PDG observed values (`v_meas = 246.22 GeV`, `m_H`, `M_W/M_Z`, `sin²θ_W`)
- Lattice-MC empirical values as load-bearing (`⟨P⟩ = 0.5934` is bounded
  same-surface; usable only as comparator, never as derivation input)
- Hardcoded `(7/8)^(1/4)` in any runner — must be DERIVED from sums
- Same-surface family arguments (cf. memory `feedback_consistency_vs_derivation_below_w2`)
- Support-tier routes used to claim retained-tier equality (cf. memory
  `feedback_retained_tier_purity_and_package_wiring`)
- Trace-ratio identifications without action-level semantic verification
  (cf. memory `feedback_hostile_review_semantics`)

## E. Comparators (admitted-context only, never proof inputs)

- `v_meas = 246.22 GeV` — PDG-style measurement comparator
- `(7/8)^(1/4) = 0.967168210134` — already in the framework via
  `HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE`; H2 must DERIVE this same number
  via a different load-bearing route, not assert it
- `C_obs ≈ 0.96692` — empirical ratio v_meas / (M_Pl · α_LM^16)
- `M_Pl · α_LM^16 = 254.6432` — admitted hierarchy baseline (B5)

## F. Cluster-obstruction context

The lattice → physical matching cluster obstruction
(`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`, PR #274)
covers cycles 5, 9, 11, 17 (yt_ew matching, gauge-scalar bridge, Higgs mass
scalar normalization, Koide-Brannen). It does NOT directly cover the v
derivation chain. H2 is INDEPENDENT of the cluster obstruction — it does not
attempt a lattice → physical matching theorem. It instead reformulates the
load-bearing observable inside the framework's own retained surface.

If H2 succeeds, the v lane is closed (modulo B5 hierarchy baseline) without
requiring the cluster-obstruction Nature-grade matching theorem.
