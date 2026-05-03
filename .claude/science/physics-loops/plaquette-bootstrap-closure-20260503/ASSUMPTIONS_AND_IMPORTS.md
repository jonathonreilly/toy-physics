# ASSUMPTIONS AND IMPORTS — Plaquette Bootstrap Closure

**Date:** 2026-05-03

## A. Retained framework primitives (load-bearing, no admission)

| # | Primitive | Authority |
|---|---|---|
| A1 | Local algebra `Cl(3)` | `MINIMAL_AXIOMS_2026-04-11.md` (A1) |
| A2 | Spatial substrate `Z³` | `MINIMAL_AXIOMS_2026-04-11.md` (A2) |
| A3 | Finite local Grassmann / staggered-Dirac partition | `MINIMAL_AXIOMS_2026-04-11.md` (A3) |
| A4 | Canonical Wilson normalization `g_bare = 1`, β=6 | `MINIMAL_AXIOMS_2026-04-11.md` (A4) + `G_BARE_RIGIDITY_THEOREM_NOTE.md` |
| A5 | Klein-four V = Z₂ × Z₂ acts on APBC temporal phases | derived from A1-A4 |
| A6 | Action `S` is V-invariant on minimal `L_s = 2` APBC block | derived from A3 |
| A7 | Closed-form determinant on minimal block: `\|det(D + m)\| = ∏_ω [m² + u_0²(3 + sin²ω)]^4` | `HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md` |
| **A11** | **Reflection positivity (R1-R4) on A_min**: `⟨Θ(F) · F⟩ ≥ 0` for any F polynomial in Λ_+; bilinear form structure; Hermitian transfer matrix `T : H_phys → H_phys`; non-negative spectrum | **`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`** (audit-pending support tier) |

**A11 is the load-bearing positivity input for the bootstrap.** With reflection
positivity, the Gram matrix `G_ij = ⟨Θ(W_i) · W_j⟩` of any finite set of
Wilson-loop observables `{W_i}` localized in `Λ_+` is positive semidefinite.

## B. Admitted bridges introduced by this campaign

| # | Bridge | Class | Justification |
|---|---|---|---|
| BB1 | Wilson loop Gram matrix `G_ij = ⟨Θ(W_i) W_j⟩ ⪰ 0` (PSD) for any finite set `{W_i}` localized in Λ_+ | Direct corollary of A11 (RP theorem R2) | The RP theorem proves R2 = "the map F ↦ G(F, F') = ⟨Θ(F) · F'⟩ is a positive semi-definite Hermitian sesquilinear form on the algebra A_+." Restricted to Wilson loops, this gives PSD Gram matrices. |
| BB2 | Lattice Migdal-Makeenko loop equation in form `Z⁻¹ ∂Z/∂U_link` relations (one-link Schwinger-Dyson) | Standard lattice gauge-theory identity (Wilson 1974; Eguchi-Kawai 1982) | Standard lattice loop equation; not framework-specific. Used as an algebraic identity relating Wilson loop expectations. |

## C. Forbidden imports

- PDG / experimental values (no role)
- Lattice MC `⟨P⟩(β=6) = 0.5934` as load-bearing (comparator only)
- Hard-coded bootstrap bracket from literature (Kazakov-Zheng 2022 ⟨P⟩ ∈ [0.59, 0.61] at λ≈1.35 is comparator only)
- Industrial SDP solver outputs (CVXPY/Mosek not in environment)

## D. Comparators (admitted-context only)

- Canonical lattice MC: `⟨P⟩(β=6) ≈ 0.5934` (`PLAQUETTE_SELF_CONSISTENCY_NOTE`)
- Bridge-support stack analytic upper-bound candidate: `P(6) ≈ 0.59353` (`PLAQUETTE_SELF_CONSISTENCY_NOTE`)
- Kazakov-Zheng 2022 SU(∞) bootstrap bracket near λ≈1.35: `⟨P⟩ ∈ [0.59, 0.61]` at L_max=16 ([arXiv:2203.11360](https://arxiv.org/abs/2203.11360))
- Kazakov-Zheng 2024 finite N bootstrap: SU(2) at 0.1% precision in physical range ([arXiv:2404.16925](https://arxiv.org/abs/2404.16925))

## E. Cluster-obstruction context

The lattice → physical matching cluster obstruction
(`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`)
covers cycles 5, 9, 11, 17 of audit-backlog-campaign-20260502. The
bootstrap approach is INDEPENDENT of this cluster: it does not attempt
a non-perturbative lattice → physical matching theorem. Instead, it
provides a different analytical attack on `⟨P⟩(β=6)` via reflection
positivity + loop equations.

## F. Relationship to the prior `vev-v-singlet-derivation-20260502` campaign

This campaign is INDEPENDENT of the prior `vev-v-singlet-derivation`
campaign:

- Block 01 of the prior campaign (PR [#408](https://github.com/jonathonreilly/cl3-lattice-framework/pull/408)) addressed the EW v derivation via H2 (f_vac V-singlet route). Independent of plaquette bootstrap.
- Block 03 of the prior campaign (PR [#410](https://github.com/jonathonreilly/cl3-lattice-framework/pull/410)) attempted H1 Route 1 mean-field saddle for ⟨P⟩(β=6); this campaign attempts H1 Route 3 bootstrap, which is structurally different (positivity + loop equations vs mean-field saddle).

## G. Net analytical-bound expectation

Realistic expectation for the analytical lower bound from small-truncation
(L_max = 2 to 4) bootstrap:

- Pure 2x2 PSD: gives `Var(P) = ⟨P²⟩ - ⟨P⟩² ≥ 0`. Weak bound on its own.
- Combined with Migdal-Makeenko one-link equation: relates `⟨P²⟩` to `β · ⟨P⟩` etc. → an analytical inequality on `⟨P⟩(β)`.
- Expected analytical bound at β=6: probably loose (e.g., `⟨P⟩ ≥ 0.4` or similar), but NEW in the framework's retained surface.

If the analytical bound emerges cleanly, it IS a new exact-support theorem.
If it doesn't tighten beyond trivial bounds, the output is a named-obstruction
stretch attempt with explicit identification of why small-truncation is
insufficient.
