# SU(3) Fusion Engine via Cartan-Torus Character Orthogonality (PR 1)

**Date:** 2026-05-03
**Claim type:** positive_theorem
**Status:** retained — pure SU(3) representation theory; numerical character
orthogonality is exact up to machine precision (validated to 5e-15).
**Primary runner:** `scripts/frontier_su3_fusion_engine.py`
**Roadmap:** [`SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md`](SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md)
**Eventual target:** explicit `rho_(p,q)(6)` for the unmarked spatial Wilson
environment on the L_s=2 APBC spatial cube — closing the gauge-scalar
temporal observable bridge no-go ([PR #477](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)).

## 0. Headline

This is **PR 1 of a 5-PR engine roadmap** to build a properly-engineered
SU(3) tensor-network engine for evaluating boundary character measures
of finite SU(3) lattice gauge configurations. The eventual application
is to compute `rho_(p,q)(6)` for the L_s=2 APBC spatial cube and close
the gauge-scalar temporal observable bridge no-go quantitatively.

This PR delivers the **fusion-multiplicity engine**: given any SU(3)
irreps `lambda = (a, b)` and `mu = (p, q)` in the dominant-weight box,
compute the multiplicities `N^nu_(lambda, mu)` of all irreps `nu` in
the tensor product `lambda ⊗ mu = ⊕_nu N^nu_(lambda, mu) nu`. This is
the foundational primitive every subsequent PR (Wigner intertwiners,
Haar integrals, tensor-network contraction, cube Perron solve) needs.

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
[PASS] numerical noise: max integer residual 5.187e-15

SUMMARY: THEOREM PASS=10 FAIL=0
```

The maximum integer residual `5.187e-15` is at machine-precision floor;
integer rounding is unambiguous. Self-orthogonality
`<chi_λ, chi_λ> = 1` holds to `1.110e-16`.

## 3. Theorem statement

**Theorem (SU(3) fusion engine).** For every pair of SU(3) irreps
`lambda = (a, b)` and `mu = (p, q)` with `a, b, p, q ≥ 0`, there exist
non-negative integer multiplicities `N^nu_(lambda, mu)` such that

```text
lambda ⊗ mu = ⊕_nu N^nu_(lambda, mu) nu
```

(decomposition into irreducible SU(3) representations) with `nu` ranging
over irreps of SU(3). The runner
`scripts/frontier_su3_fusion_engine.py` computes
`N^nu_(lambda, mu)` for all triples in the dominant-weight box
`{(p, q) : 0 ≤ p, q ≤ NMAX}` via numerical character orthogonality on
the SU(3) Cartan torus (Section 1), with integer-rounding residual
machine-precision-bounded (verified `< 5.2e-15` at NMAX=4, n_grid=80).

The result satisfies all standard SU(3) fusion identities (Section 2:
V1-V9) including commutativity, singlet selection, dimension count,
crossing, and the fundamental Pieri rule.

**Proof sketch.** The Schur character formula for SU(3) (Section 1.1)
expresses each `chi_(p,q)` as an explicit polynomial in the Cartan
torus parameters. Character orthogonality (Section 1.3) follows from
Peter-Weyl; numerical evaluation gives `N^nu_(lambda, mu)` to
machine precision. Integer-rounding is justified by the residual
diagnostic. Validation (Section 2) cross-checks against standard
representation-theory identities. ∎

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

- Fusion multiplicities `N^nu_(lambda, mu)` for arbitrary SU(3) irreps
  in the dominant-weight box.
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
claim_type: positive_theorem
intrinsic_status: unaudited
deps: []   # self-contained; depends only on numpy and standard SU(3) rep theory
verdict_rationale_template: |
  Pure SU(3) representation theory: numerical character orthogonality on
  the Cartan torus computes fusion multiplicities N^ν_(λ,μ) for arbitrary
  SU(3) irreps. Validation suite (V1-V9) covers standard fusion
  identities (3⊗3̄, 3⊗3, 8⊗8, 6⊗6̄), commutativity, singlet selection,
  dimension count, crossing, and Pieri rule. All 10 checks PASS at
  NMAX=4, n_grid=80, with integer-rounding residual 5.2e-15 (machine
  precision floor). Engine exposes importable API for PRs 2-5 of the
  engine roadmap. No lattice-gauge or Wilson-plaquette dependencies; no
  forbidden imports. Self-contained foundation for the L_s=2 cube
  Perron solve in PR 5.
```

## 7. Cross-references

- Engine roadmap: [`SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md`](SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md)
- Eventual target: [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)
- Companion external lift: [`GAUGE_SCALAR_BRIDGE_KZ_EXTERNAL_LIFT_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_BRIDGE_KZ_EXTERNAL_LIFT_THEOREM_NOTE_2026-05-03.md) (PR #484)
- Companion staging note: [`GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_LOWER_BOUND_STAGING_NOTE_2026-05-03.md`](GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_LOWER_BOUND_STAGING_NOTE_2026-05-03.md) (PR #487)

## 8. Command

```bash
python3 scripts/frontier_su3_fusion_engine.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=10 FAIL=0
```
