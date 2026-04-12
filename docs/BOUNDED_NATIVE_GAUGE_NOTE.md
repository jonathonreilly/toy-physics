# Native Gauge Note: SU(2) Derived + SU(3) Commutant Theorem

**Date:** 2026-04-12 (updated after basis-independence proof)
**Status:** SU(2) DERIVED | SU(3) commutant theorem PROVEN (basis-independent) | U(1)_Y identification OPEN
**Authority:** CI3_Z3_PUBLICATION_RETAIN_AUDIT_2026-04-12.md
**Scripts:** `frontier_non_abelian_gauge.py`, `frontier_su3_commutant.py`, `frontier_su3_basis_independence.py`

---

## Retained Positive: Native Cubic SU(2)

The staggered lattice on Z³ produces exact SU(2) gauge structure through the
following chain, which is entirely determined by graph topology:

1. Z³ is bipartite → Z₂ parity ε = (-1)^{x+y+z}
2. Staggered fermion hopping → η phases (η_x=1, η_y=(-1)^x, η_z=(-1)^{x+y})
3. Taste doubling → 2³ = 8 internal species
4. η phases → Clifford algebra Cl(3) in taste space
5. Cl(3) contains su(2) subalgebra → SU(2) gauge symmetry

### Numerical verification (all at machine precision)

| Test | Result | Error |
|------|--------|-------|
| Clifford algebra {Γ_μ, Γ_ν} = 2δ_{μν} I₈ | Exact | 0 |
| SU(2) generators [S_i, S_j] = iε_{ijk} S_k | Exact | < 10⁻¹⁵ |
| Casimir S² = 3/4 (j = 1/2) | Exact | < 10⁻¹⁵ |
| Isospin SU(2) [T_i, T_j] = iT_k | Exact | < 10⁻¹⁵ |
| Chiral symmetry {H_hop, P} = 0 | Exact | 0 |

This result is not new in isolation — staggered fermion taste algebras are
well-studied (Kogut & Susskind 1975, Golterman & Smit 1984, Sharpe 2006).
The contribution is connecting it to the framework's single-axiom derivation
chain: the same Cl(3) that produces SU(2) also produces gravity (via
self-consistent Poisson), the Born rule (via unitarity), and d=3 selection.

### What is retained for publication

- Cl(3) on Z³ produces exact SU(2) with correct generators, Casimir, and
  chiral structure
- The mechanism is topological (bipartite → Z₂ → Cl(3) → su(2))
- No free parameters or choices involved
- U(1) from edge phases is also confirmed (Coulomb law, R²=0.9995)

---

## SU(3): Commutant Theorem (basis-independent, proven)

**The commutant of the derived SU(2) plus the residual cubic exchange symmetry
on Z³ is su(3) ⊕ u(1). This is now proven to be basis-independent and canonical.**

### The theorem (paper-usable claim)

Given the derived SU(2) sector (from bipartite Cl(3) bivectors) and the
weak-preserving residual cubic exchange symmetry SWAP₂₃ (a physical lattice
symmetry of Z³), the unique commutant in End(C⁸) is su(3) ⊕ u(1).

This is NOT "Cl(3) alone derives SU(3)." The correct claim is:
"Derived SU(2) plus residual cubic symmetry on Z³ forces su(3) ⊕ u(1)."

### Basis-independence (5 independent proofs)

| Test | Result | Script |
|------|--------|--------|
| All 3 weak-axis choices give dim 10 | YES — su(3) Killing form confirmed for each | frontier_su3_basis_independence.py |
| Double commutant theorem | Module decomposition C⁸=(2×3)+(2×1) is representation-independent | frontier_su3_basis_independence.py |
| 1000 Haar-random conjugations | 1000/1000 give dim 10, all su(3) | frontier_su3_basis_independence.py |
| Lattice η-phase construction | All 6 axis permutations → unitarily equivalent SU(2) | frontier_su3_basis_independence.py |
| 4 Cl(3) representations | All give commutant dim 16, Casimir 0.75 | frontier_su3_basis_independence.py |

### What is closed

- The algebra: su(3) ⊕ u(1) as commutant — PROVEN, basis-independent
- The subspace selection: 3+1 from Sym²(C²) + Anti²(C²) — PROVEN, canonical
- Basis-independence: any axis choice gives conjugate-equivalent result — PROVEN

### What remains open

**Physical identification of the abelian factor:**
The commutant gives su(3) ⊕ u(1) ⊕ u(1) (from su(3) center + explicit u(1)).
Identifying the surviving U(1) specifically as hypercharge U(1)_Y requires
a separate argument — either anomaly cancellation or charge assignment matching.
This is a **physical identification step**, not an algebraic existence question.
Agent running on this (frontier_hypercharge_identification.py).

### Claim hierarchy (for paper framing)

| Claim | Status | Strength |
|-------|--------|----------|
| "Derived SU(2) + cubic exchange → su(3) ⊕ u(1) uniquely" | PROVEN | Paper-defensible |
| "The commutant is basis-independent and canonical" | PROVEN | Paper-defensible |
| "The U(1) factor is hypercharge" | OPEN | Needs anomaly cancellation argument |
| "Cl(3) on Z³ alone derives the full SM gauge group" | NOT EARNED | Overclaim — do not use |

### Prior art that must be cited

- Furey (2014-2024): SU(3) from Cl(6)/division algebras
- Stoica (2018): SM algebra from Cl(6)
- Trayling & Baylis (2001): SM gauge group from Cl(7)
- Shirokov (2025): SU(3) in ternary Clifford algebra

---

## Relationship to other notes

This note supersedes the SU(3) claims in:
- `ULTIMATE_SIMPLIFICATION_NOTE.md` (overstates SU(3) closure)
- `COMPLETE_DERIVATION_CHAIN_2026-04-12.md` (presents SU(3) as derived)
- `REVIEW_THREAD_SUMMARY_2026-04-12.md` (labels SU(3) as "CLOSED")

Those documents remain useful as branch-local working notes but are NOT
the retention authority for publication-facing claims. This bounded note
IS the retention authority for the native gauge lane.
