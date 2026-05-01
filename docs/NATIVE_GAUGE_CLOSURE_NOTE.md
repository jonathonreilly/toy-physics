# Native Gauge Closure Note: Graph-First Gauge Closure on Z^3

**Date:** 2026-04-12
**Status:** proposed_retained audit target: exact native cubic `Cl(3)` / `SU(2)` plus ledger-ratified graph-first selector and structural `SU(3)` dependencies; bounded hypercharge-like left-handed abelian surface only
**Claim boundary authority:** this note
**Primary runner:** `scripts/frontier_non_abelian_gauge.py`

This note is the publication-facing aggregator for the gauge-structure
backbone. The fresh audit packet has a narrow boundary:

- exact native cubic `Cl(3)` / `SU(2)` is checked directly by the primary
  runner;
- the graph-first selector and graph-first structural `SU(3)` claims are
  imported only through their ledger-ratified notes and runners;
- the abelian factor is bounded to the left-handed `+1/3` / `-1` eigenvalue
  surface, not a full anomaly-complete `U(1)_Y` theorem.

The two load-bearing graph-first sub-claims are:

- [graph-first weak-axis selector derivation](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)
  (runner: `scripts/frontier_graph_first_selector_derivation.py`)
- [graph-first `SU(3)` integration theorem](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  (runner: `scripts/frontier_graph_first_su3_integration.py`)

Each sub-claim has its own status, runner, and audit row. In the current
ledger, both dependencies are audit-ratified with `effective_status = retained`.
This aggregator asks the fresh audit to combine those retained dependencies
with the native `SU(2)` result computed by the primary runner above.

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
The retained boundary here is narrower: the cubic taste algebra supplies an
exact native `Cl(3)` / `SU(2)` structure on the `Z^3` graph surface. Gravity,
Born-rule, dimensional-selection, and phenomenology claims are separate audit
lanes and are not ratified by this note.

### What is retained for publication

- Cl(3) on Z³ produces exact SU(2) with correct generators, Casimir, and
  chiral structure
- The mechanism is topological (bipartite → Z₂ → Cl(3) → su(2))
- No free parameters or choices involved
- this section does not identify the abelian factor or any downstream
  phenomenology

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

### Bounded left-handed abelian corollary

On the same selected-axis graph surface, the unique traceless abelian
direction has eigenvalues `+1/3` on the `6`-dimensional
symmetric/weak-doublet block and `-1` on the `2`-dimensional
antisymmetric/weak-doublet block. This is the only abelian statement carried
by this note.

### What remains bounded

- the abelian factor is described as **hypercharge-like** or left-handed
  charge matching only
- anomaly-complete `U(1)_Y` closure belongs to a separate chiral matter
  completion theorem
- downstream phenomenology remains separate from this structural closure
- this note is an audit target for the gauge-structure backbone, not the full
  Standard Model matter-completion story

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
  - abelian factor as hypercharge-like / left-handed matched only
  - anomaly-complete `U(1)_Y`
  - all downstream phenomenology
- do not treat broader CI(3) / `Z^3` derivation memos or phenomenology notes as
  retention authority unless they are separately promoted with bounded wording
