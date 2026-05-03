# SU(3) Fusion Engine via Cartan-Torus Character Orthogonality (PR 1)

**Date:** 2026-05-03
**Claim type:** bounded_theorem
**Status:** bounded support theorem — finite-box engine check, unaudited.
**Primary runner:** `scripts/frontier_su3_fusion_engine.py`
**Roadmap:** `docs/SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md`
**Eventual target:** support a future explicit `rho_(p,q)(6)` computation for
the unmarked spatial Wilson environment on the L_s=2 APBC spatial cube,
under the open native bridge gate recorded in
`docs/GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md`.

## 0. Headline

This is **PR 1 of a 5-PR engine roadmap** to build a properly-engineered
SU(3) tensor-network engine for evaluating boundary character measures
of finite SU(3) lattice gauge configurations. The eventual application
is to compute `rho_(p,q)(6)` for the L_s=2 APBC spatial cube and submit
the bridge parent chain for independent audit once the native computation
exists.

This PR delivers the **finite-box fusion-multiplicity engine**: for the
default box `{0 <= p,q <= 4}` and `n_grid = 80`, compute the
multiplicities `N^nu_(lambda, mu)` returned by Cartan-torus character
orthogonality and validate them against standard SU(3) identities. This
is a bounded support primitive for later Wigner-intertwiner, Haar-integral,
tensor-network, and cube-Perron work.

The PR is self-contained: it depends only on standard SU(3)
representation theory (Schur character formula, Weyl-Vandermonde
measure on the Cartan torus). It uses no lattice-gauge primitives and
makes no claims about the Wilson plaquette or the bridge no-go directly.

## 1. Algorithm

### 1.1 SU(3) Schur character

The character of irrep `(p, q)` at the SU(3) Cartan element

```text
g(phi_1, phi_2) = diag(e^(i phi_1), e^(i phi_2), e^(-i (phi_1 + phi_2)))
```

is the Schur polynomial of partition `lambda = (p+q, q, 0)`:

```text
chi_(p,q)(g) = det[z_i^(lambda_j + 3-j)]_{i,j=1..3} / det[z_i^(3-j)]_{i,j=1..3}
             = det[z_i^(lambda_j + 3-j)] / Vandermonde(z)
```

where `z_i = exp(i phi_i)` and `Vandermonde(z) = (z_1-z_2)(z_1-z_3)(z_2-z_3)`.

### 1.2 Weyl-Vandermonde Haar measure

The SU(3) Haar measure restricted to class functions on the Cartan
torus is

```text
dW(phi_1, phi_2) = (1/|W|) |Vandermonde(z)|^2 (d phi_1 / 2 pi)(d phi_2 / 2 pi)
```

with Weyl group order `|W(SU(3))| = 6`. The runner normalizes this so that
`integral_(Cartan torus) 1 dW = 1`.

### 1.3 Fusion via character orthogonality

Tensor product decomposition is encoded by character multiplication:

```text
chi_lambda(g) * chi_mu(g) = sum_nu N^nu_(lambda, mu) chi_nu(g).
```

Multiplying both sides by `chi_nu(g)^*` and integrating against the
Weyl-Vandermonde Haar measure (using character orthogonality
`integral chi_nu chi_eta^* dW = delta_(nu, eta)`):

```text
N^nu_(lambda, mu) = integral_(Cartan torus) chi_lambda(g) chi_mu(g) chi_nu(g)^* dW(g).
```

This integer-valued integral is computed numerically with a uniform
`(phi_1, phi_2)` grid quadrature, then rounded to the nearest
non-negative integer. The integer-rounding residual is reported as a
diagnostic.

### 1.4 Truncation

The dominant-weight box `{(p, q) : 0 <= p, q <= NMAX}` truncates the
irrep enumeration. For PR 1 the runner default is `NMAX = 4`, giving
25 weights and 3049 nonzero fusion entries within the box.

## 2. Validation suite

The runner verifies nine independent identities:

| ID | Check | Pass criterion |
|---|---|---|
| V1 | `3 ⊗ 3̄ = 8 ⊕ 1` | `(1,0) ⊗ (0,1) = (1,1) ⊕ (0,0)` |
| V2 | `3 ⊗ 3 = 6 ⊕ 3̄` | `(1,0) ⊗ (1,0) = (2,0) ⊕ (0,1)` |
| V3 | `8 ⊗ 8 = 27 ⊕ 10 ⊕ 10̄ ⊕ 8 ⊕ 8 ⊕ 1` | `(1,1) ⊗ (1,1) = (0,0) + 2(1,1) + (3,0) + (0,3) + (2,2)` |
| V4 | `6 ⊗ 6̄ = 27 ⊕ 8 ⊕ 1` | `(2,0) ⊗ (0,2) = (0,0) + (1,1) + (2,2)` |
| V5 | Commutativity | `N^ν_(λ,μ) = N^ν_(μ,λ)` for all triples |
| V6 | Singlet selection | `N^(0,0)_(λ,μ) = δ_(μ, λ̄)` |
| V7 | Dimension count | `Σ_ν N^ν_(λ,μ) d_ν ≤ d_λ d_μ` (= when product fits in NMAX box) |
| V8 | Crossing | `N^ν_(λ,μ) = N^λ_(ν, μ̄)` |
| V9 | Fundamental Pieri | `(1,0) ⊗ (a,b) = (a+1,b) + (a-1,b+1) + (a,b-1)` |

**Observed run** (NMAX=4, n_grid=80, 25 weights, 25³ = 15625 triples):

```text
[PASS] V1: 3 ⊗ 3̄ = 8 ⊕ 1
[PASS] V2: 3 ⊗ 3 = 6 ⊕ 3̄
[PASS] V3: 8 ⊗ 8 = 27 ⊕ 10 ⊕ 10̄ ⊕ 8 ⊕ 8 ⊕ 1
[PASS] V4: 6 ⊗ 6̄ = 27 ⊕ 8 ⊕ 1
[PASS] V5: commutativity (asymmetric entries: 0)
[PASS] V6: singlet selection (errors: 0)
[PASS] V7: dimension count (overflow errors: 0)
[PASS] V8: crossing (errors: 0)
[PASS] V9: fundamental Pieri (errors: 0)
[PASS] numerical noise: max integer residual 3.553e-15

SUMMARY: BOUNDED PASS=10 FAIL=0
```

The maximum integer residual `3.553e-15` is at machine-precision floor
for this finite run; integer rounding is unambiguous on the checked box.
Self-orthogonality `<chi_λ, chi_λ> = 1` holds to `2.220e-16` on the
sampled rows reported by the runner.

## 3. Theorem statement

**Bounded theorem (SU(3) finite-box fusion engine).** At `NMAX = 4`
and `n_grid = 80`, the runner
`scripts/frontier_su3_fusion_engine.py` computes a finite fusion table
on the dominant-weight box `{(p, q) : 0 <= p, q <= 4}` using numerical
Cartan-torus character orthogonality. The returned table has
non-negative integer entries after rounding, maximum integer residual
`< 3.6e-15`, and satisfies the validation suite in Section 2:
standard landmarks V1-V4 plus commutativity, singlet selection,
dimension-count upper bound inside the truncation, crossing, and the
fundamental Pieri rule.

**Proof sketch.** The Schur character formula for SU(3) (Section 1.1)
expresses each `chi_(p,q)` as an explicit polynomial in the Cartan
torus parameters. Character orthogonality (Section 1.3) follows from
Peter-Weyl for exact SU(3) fusion multiplicities. The runner evaluates
that integral on a fixed Cartan grid, rounds the result, and reports the
rounding residual. The theorem claimed here is the bounded computational
surface: the finite default run is reproducible and passes the listed
identity checks. It is not a proof of arbitrary-representation fusion
outside the checked box. ∎

## 4. Engine API (importable for PRs 2-5)

The runner exposes the following functions for use in subsequent PRs:

| Function | Returns | Used by |
|---|---|---|
| `dim_su3(p, q)` | int | All |
| `conjugate_irrep(p, q)` | (int, int) | All |
| `dominant_weights_box(nmax)` | List[(int, int)] | All |
| `cartan_grid(n_grid)` | (np.ndarray, np.ndarray, float) | PRs 2, 3 |
| `vandermonde_squared(phi1, phi2)` | float | PRs 2, 3 |
| `haar_measure_normalized(n_grid)` | (np.ndarray, float) | PRs 2, 3 |
| `schur_character(p, q, phi1, phi2)` | complex | PRs 2, 3 |
| `character_table(weights, n_grid)` | np.ndarray | PRs 2, 3 |
| `fusion_multiplicity(...)` | (int, float) | PR 2 |
| `fusion_table(weights, chars, W, cell)` | (np.ndarray, float) | PR 2 |
| `fusion_decomposition(N_table, weights, lam, mu)` | Dict | PRs 4, 5 |

## 5. Scope

### In scope (this PR)

- Fusion multiplicities `N^nu_(lambda, mu)` for all triples in the
  default dominant-weight box `{0 <= p,q <= 4}`.
- Validation against standard representation-theory identities.
- Importable API for downstream PRs.

### Out of scope (deferred to PRs 2-5)

- **PR 2: Wigner intertwiner / Clebsch-Gordan engine.** Explicit
  intertwiner operators `C^nu_(lambda, mu): V_lambda ⊗ V_mu -> V_nu`.
- **PR 3: Haar integral primitives.** Single-link and multi-link
  Haar integrals via intertwiners.
- **PR 4: Tensor-network contraction engine.** Generic engine for
  contracting irrep assignments on a lattice graph.
- **PR 5: L_s=2 APBC spatial cube.** Explicit cube geometry encoder,
  computation of `Z_6^env(W)`, extraction of `rho_(p,q)(6)`, plug into
  source-sector factorization, compute `P(6)` and compare to
  `epsilon_witness`.

### Not making any claim about `<P>(6)` in this PR

This PR does NOT compute, bracket, or constrain `<P>(beta=6)`. It does
NOT bypass the gauge-scalar bridge no-go. It does NOT promote the
parent gauge-scalar-temporal-completion theorem. It is pure SU(3)
representation theory — a foundational primitive for the eventual cube
Perron solve in PR 5.

## 6. Audit consequence

```yaml
claim_id: su3_fusion_engine_pr1_theorem_note_2026-05-03
note_path: docs/SU3_FUSION_ENGINE_PR1_THEOREM_NOTE_2026-05-03.md
runner_path: scripts/frontier_su3_fusion_engine.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps: []   # self-contained; depends only on numpy and standard SU(3) rep theory
verdict_rationale_template: |
  Bounded SU(3) representation-theory engine check: numerical character
  orthogonality on the Cartan torus computes finite-box fusion
  multiplicities N^ν_(λ,μ) for NMAX=4 and n_grid=80. Validation suite
  (V1-V9) covers standard fusion
  identities (3⊗3̄, 3⊗3, 8⊗8, 6⊗6̄), commutativity, singlet selection,
  dimension count, crossing, and Pieri rule. All 10 checks PASS at
  NMAX=4, n_grid=80, with integer-rounding residual 3.6e-15 (machine
  precision floor). Engine exposes importable API for later bounded
  engine work. No lattice-gauge or Wilson-plaquette dependencies; no
  forbidden imports. This row does not close or promote the gauge-scalar
  bridge parent chain.
```

## 7. Cross-references

- Engine roadmap: `docs/SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md`
- Open bridge gate: `docs/GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md`

## 8. Command

```bash
python3 scripts/frontier_su3_fusion_engine.py
```

Expected summary:

```text
SUMMARY: BOUNDED PASS=10 FAIL=0
```
