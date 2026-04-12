# Bounded Native Gauge Note: Cl(3) / SU(2) on Z³

**Date:** 2026-04-12
**Status:** BOUNDED-RETAINED POSITIVE (SU(2)) + EXPLICIT OPEN (SU(3))
**Claim boundary authority:** this note
**Script:** `scripts/frontier_non_abelian_gauge.py`

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

## Explicit Open: Native Cubic SU(3)

**SU(3) emergence from the native cubic Cl(3) algebra is NOT closed.**

### What has been attempted

| Approach | Result | Status |
|----------|--------|--------|
| Hand-embedding 3-of-4 states | Compatible, 8/8 Gell-Mann | Not derived — subspace chosen by hand |
| Commutant of SU(2) + SWAP₂₃ | su(3) ⊕ u(1) uniquely | Side result — adds SWAP₂₃ beyond native Cl(3) |
| Taste breaking 1+3+3+1 | Splitting forces 3-fold degeneracy | Depends on modeled O(a²) breaking coefficients |
| Anomaly cancellation | SU(3) anomaly-free with 3+3* | Constrains but does not select |
| Confinement | Partial (small lattice, weak coupling) | Not conclusive |

### Honest assessment

The cubic taste algebra CONTAINS a compatible SU(3) embedding. Multiple
independent arguments (commutant, taste breaking, anomaly cancellation)
constrain the color group to be SU(3) rather than SU(4) or larger. But
none of these derives SU(3) purely from the native Cl(3) structure without
either:
- choosing a subspace by hand (original embedding)
- adding an identification layer (SWAP₂₃ commutant)
- importing modeled breaking coefficients (taste breaking)

### What would close this

A derivation showing that the Cl(3) algebra on Z³, combined ONLY with
structures already retained (bipartite Z₂, self-consistent Poisson, unitarity),
uniquely selects a 3-dimensional gauge subspace. Possible paths:
- Dynamical symmetry breaking from self-consistent field iteration
- A graph-theoretic criterion selecting the triplet
- Proof that the commutant argument follows from cubic symmetry alone
  (SWAP₂₃ IS a cubic symmetry, but the commutant chain needs explicit
  derivation from the lattice, not just identification)

### Prior art that must be cited

- Furey (2014-2024): SU(3) from Cl(6)/division algebras
- Stoica (2018): SM algebra from Cl(6)
- Trayling & Baylis (2001): SM gauge group from Cl(7)
- Shirokov (2025): SU(3) in ternary Clifford algebra

---

## Reading rule

Use this note as the publication-facing claim boundary for the CI(3) / `Z^3`
native gauge lane on `main`.

- safe retained reading: exact native cubic `Cl(3)` / `SU(2)` algebra
- explicit open boundary: native cubic `SU(3)`
- do not treat broader CI(3) / `Z^3` derivation memos or phenomenology notes as
  retention authority unless they are separately promoted with bounded wording
