# Native Gauge Closure Note: Graph-First Gauge Closure on Z^3

**Date:** 2026-04-12
**Status:** proposed_retained exact native `SU(2)` + proposed_retained structural `SU(3)`; bounded abelian factor (`+1/3`, `-1` on the left-handed surface)
**Claim boundary authority:** this note
**Scripts:** `scripts/frontier_non_abelian_gauge.py`, `scripts/frontier_graph_first_selector_derivation.py`, `scripts/frontier_graph_first_su3_integration.py`

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

## Retained Positive: Graph-First Structural `SU(3)` Closure

The structural color lane is now closed on a graph-first surface that does not
depend on a hand-chosen tensor-factor presentation.

### The retained graph-first chain

1. The taste cube `V = {0,1}^3` carries three canonical one-step axis shifts
   `S_1, S_2, S_3`.
2. For `H(\phi) = \sum_i \phi_i S_i`, the first nontrivial even invariant is
   \[
   V_{\mathrm{sel}}(\phi)
   = \mathrm{Tr}\,H(\phi)^4 - \frac{1}{8}\big(\mathrm{Tr}\,H(\phi)^2\big)^2
   = 32 \sum_{i<j}\phi_i^2 \phi_j^2.
   \]
3. After normalization `p_i = \phi_i^2 / \sum_j \phi_j^2`, this becomes
   \[
   F(p) = \sum_{i<j} p_i p_j = \frac{1}{2}\left(1 - \sum_i p_i^2\right),
   \]
   whose minima are exactly the three axis vertices.
4. Each selected axis gives a canonical graph decomposition into:
   - a 2-point fiber along the selected axis
   - a 4-point base on the remaining two coordinates
5. The selected-axis shift/parity pair generates the weak `su(2)` on the graph
   fibers.
6. The residual swap of the complementary axes acts canonically on the base and
   splits it as `3 ⊕ 1`.
7. The joint commutant is therefore `gl(3) ⊕ gl(1)`, with compact semisimple
   part `su(3)`.

### Numerical verification

| Test | Result | Error |
|------|--------|-------|
| Graph-first selector derivation | `63/63` pass | 0 fail |
| Axis minima with residual `Z_2` stabilizer | Exact on all 3 axes | 0 |
| Graph-first `SU(3)` integration theorem | `111/111` pass | 0 fail |
| Joint commutant dimension | `10` on all 3 selected axes | Exact |
| Embedded Gell-Mann closure | `su(3)` on all 3 selected axes | `< 10^-15` |

### What is retained for publication

- exact native cubic `Cl(3)` / `SU(2)` algebra
- derived graph-first weak-axis selector on the canonical cube-shift surface
- structural `su(3)` closure from the selected graph axis plus residual cubic
  swap
- unique traceless abelian direction with eigenvalues `+1/3` on the
  `6`-dimensional symmetric/weak-doublet block and `-1` on the
  `2`-dimensional antisymmetric/weak-doublet block

### What remains bounded

- the abelian factor is still best described as **hypercharge-like** or
  left-handed charge matching until the anomaly-complete chiral completion
  theorem is written cleanly
- downstream phenomenology remains separate from this structural closure
- this note closes the gauge-structure backbone, not the full Standard Model
  matter-completion story

### Prior art that must be cited

- Furey (2014-2024): SU(3) from Cl(6)/division algebras
- Stoica (2018): SM algebra from Cl(6)
- Trayling & Baylis (2001): SM gauge group from Cl(7)
- Shirokov (2025): SU(3) in ternary Clifford algebra

---

## Reading Rule

Use this note as the publication-facing claim boundary for the CI(3) / `Z^3`
gauge lane on `main`.

- safe retained reading:
  - exact native cubic `Cl(3)` / `SU(2)` algebra
  - derived graph-first weak-axis selector
  - structural graph-first `su(3)` closure
- still bounded:
  - abelian factor as hypercharge-like / left-handed matched
  - all downstream phenomenology
- do not treat broader CI(3) / `Z^3` derivation memos or phenomenology notes as
  retention authority unless they are separately promoted with bounded wording
