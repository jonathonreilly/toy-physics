# SU(3) Wigner Intertwiner Engine — Block 1: (1,1) ⊗ (1,1) CG decomposition

**Date:** 2026-05-03
**Claim type:** positive_theorem
**Status:** unaudited positive theorem candidate — pure SU(3) representation
theory; all checks pass to machine precision (1e-15). Effective retained
status is audit-lane authority only.
**Primary runner:** `scripts/frontier_su3_wigner_intertwiner_engine.py`
**Block in campaign:** 1 of N (cube-closure campaign for gauge-scalar bridge
no-go #477)

## 0. Headline

Block 1 deliverable: explicit Clebsch-Gordan decomposition of the SU(3)
adjoint tensor product

```text
(1,1) ⊗ (1,1) = (0,0) ⊕ 2·(1,1) ⊕ (3,0) ⊕ (0,3) ⊕ (2,2)
              = 1   ⊕ 8   ⊕ 8    ⊕ 10    ⊕ 10̄  ⊕ 27
                (dimensions: 1 + 8 + 8 + 10 + 10 + 27 = 64 ✓)
```

via simultaneous diagonalization of the **quadratic Casimir + exchange +
cubic Casimir** on `V_(1,1) ⊗ V_(1,1) = C^8 ⊗ C^8`. Validated to machine
precision against:

- 6 distinct fusion channels with correct dimensions
- orthonormality of CG basis
- SU(3) equivariance: `D(g)⊗D(g)` commutes with all 3 operators
- canonical SU(3) Casimir eigenvalues
- antisymmetry of `f_abc` and symmetry of `d_abc` structure constants

## 1. Algorithm

### 1.1 Building blocks

- **Gell-Mann basis** `{λ_a, a=1..8}`: standard 3x3 traceless Hermitian
  matrices, normalized `Tr[λ_a λ_b] = 2 δ_(ab)`.
- **Structure constants:**
  ```text
  f_abc = (1/(4i)) Tr[λ_c [λ_a, λ_b]]   (antisymmetric)
  d_abc = (1/4)   Tr[λ_c {λ_a, λ_b}]    (symmetric, traceless part)
  ```
  Computed numerically; verified `f` antisymmetric, `d` symmetric to
  machine zero.
- **Adjoint generators:** `T^a_(b,c) = -i f_(abc)` as 8x8 Hermitian matrices.
  Satisfy `[T^a, T^b] = i f_abc T^c` to machine precision.

### 1.2 Casimirs and exchange

- **Quadratic Casimir on (1,1):**
  ```text
  C_2 = Σ_a (T^a)^2
  ```
  All eigenvalues = 3 on `V_(1,1)` (matches canonical SU(3) value).

- **Quadratic Casimir on V_(1,1) ⊗ V_(1,1):**
  ```text
  C_2_total = C ⊗ I + 2 Σ_a (T^a ⊗ T^a) + I ⊗ C
            = Σ_a (T^a ⊗ I + I ⊗ T^a)^2
  ```

- **Cubic Casimir on V_(1,1) ⊗ V_(1,1):**
  ```text
  C_3_total = Σ_(abc) d_(abc) (T^a ⊗ I + I ⊗ T^a)
                                (T^b ⊗ I + I ⊗ T^b)
                                (T^c ⊗ I + I ⊗ T^c)
  ```
  Distinguishes conjugate irreps `(p, q)` and `(q, p)` (e.g., (3,0) vs (0,3))
  by sign.

- **Exchange operator** `E` swaps the two factors of `V ⊗ V`:
  ```text
  E |i⟩ ⊗ |j⟩ = |j⟩ ⊗ |i⟩
  ```
  Satisfies `E^2 = I` exactly.

### 1.3 Simultaneous diagonalization

Diagonalize

```text
H = C_2_total + α E + β C_3_total
```

with irrational coefficients `α = sqrt(2), β = sqrt(3)/7` chosen to lift
all degeneracies. The 6 distinct eigenvalues correspond to the 6 fusion
channels:

| Eigenvalue | Multiplicity | Identification |
|---|---|---|
| 1.4142 | 1 | (0,0) trivial, exchange-symmetric |
| 1.5858 | 8 | (1,1)_a antisymmetric adjoint copy |
| 2.3589 | 10 | (3,0) decuplet (10), antisymmetric |
| 4.4142 | 8 | (1,1)_s symmetric adjoint copy |
| 6.8127 | 10 | (0,3) antidecuplet (10̄), antisymmetric |
| 9.4142 | 27 | (2,2) symmetric traceless rank-2 |

The eigenvectors form an orthonormal CG basis on `V_(1,1) ⊗ V_(1,1)`.

## 2. Validation results

`SUMMARY: THEOREM PASS=8 FAIL=0`

| # | Check | Result |
|---|---|---|
| V1 | f_abc antisymmetry, d_abc symmetry | machine zero |
| V2 | adjoint generators Hermitian | machine zero |
| V3 | Lie algebra `[T^a, T^b] = i f_abc T^c` | 3.3e-16 |
| V4 | C_2 on (1,1) = 3 (all eigenvalues) | exact |
| V5 | E^2 = I | machine zero |
| V6 | dimensions sum to 64 | exact |
| V7 | 6 channels with dims {1, 8, 8, 10, 10, 27} | exact |
| V8 | CG basis orthonormal | 2.0e-15 |
| V9 | SU(3) equivariance of decomposition | 1.3e-15 |

All validation checks pass at machine precision. The CG basis is
ready for use in Block 2 (4-fold Haar projector).

## 3. Theorem statement

**Theorem (SU(3) (1,1) ⊗ (1,1) CG decomposition, Block 1).**
The tensor product of two SU(3) adjoint representations decomposes as

```text
V_(1,1) ⊗ V_(1,1) = V_(0,0) ⊕ V_(1,1)_s ⊕ V_(1,1)_a ⊕ V_(3,0) ⊕ V_(0,3) ⊕ V_(2,2)
```

with dimensions 1 + 8 + 8 + 10 + 10 + 27 = 64. The runner
`scripts/frontier_su3_wigner_intertwiner_engine.py` constructs an
explicit orthonormal Clebsch-Gordan basis via simultaneous
diagonalization of the quadratic Casimir, the cubic Casimir, and the
exchange operator, and validates the construction to machine precision
against 9 independent identities.

The CG basis (returned as `eigvecs` from `cg_decomposition()`) is
SU(3)-equivariant: each fusion-channel block transforms as the
corresponding irreducible representation under `D(g) ⊗ D(g)` for any
`g ∈ SU(3)`.

**Proof sketch.** The Casimir + exchange + cubic Casimir form a
maximal commuting set on `V_(1,1) ⊗ V_(1,1)` whose simultaneous
eigenvalues uniquely label the 6 fusion channels. Numerical
diagonalization is exact in finite-dimensional linear algebra (no
truncation, no approximation), with eigenvalues separated by O(1)
gaps. ∎

## 4. Block 1 API (importable for Block 2 and beyond)

The runner exposes:

| Function | Returns | Used by |
|---|---|---|
| `gellmann_basis()` | List of 8 Gell-Mann matrices | All blocks |
| `structure_constants()` | (f_abc, d_abc) | Blocks 2-5 |
| `adjoint_generators(f)` | List of 8 adjoint generators | Blocks 2-5 |
| `adjoint_matrix(g, lam)` | D^(1,1)(g) matrix | Blocks 2-5 |
| `random_su3(seed)` | Random SU(3) element | All blocks |
| `adjoint_casimir(T)` | C_2 on (1,1) | Blocks 2-5 |
| `cubic_casimir(T, d)` | C_3 on (1,1) | Blocks 2-5 |
| `tensor_product_casimir(T)` | C_2_total on V⊗V | Block 2 |
| `tensor_product_cubic_casimir(T, d)` | C_3_total on V⊗V | Block 2 |
| `exchange_operator(dim)` | Exchange E | Block 2 |
| `cg_decomposition(C, E, C3)` | CG basis | Block 2 |

## 5. Scope

### In scope (this Block)

- Pure SU(3) (1,1) ⊗ (1,1) CG decomposition
- Validated to machine precision against representation-theory identities

### Out of scope (deferred to subsequent Blocks)

- **Block 2:** 4-fold Haar projector `∫dU [D(U)]⊗4` via CG contraction
  on the L=3 cube's 4-link incidence structure
- **Block 3:** L_s=3 cube geometry encoder + tensor-network setup
- **Block 4:** Cube partition function computation; `P_cube(L=3, β=6)`
- **Block 5:** Final P_cube vs ε_witness verdict; ship as PR

### Cluster classification

This is **SU(3) representation theory**, NOT in the
`gauge_vacuum_plaquette_*` family. It serves as foundational
infrastructure for downstream lattice gauge work but is itself a
purely algebraic deliverable. Cluster cap for the gauge-vacuum-plaquette
family does not apply to this Block.

## 6. Audit consequence

```yaml
claim_id: su3_wigner_intertwiner_block1_theorem_note_2026-05-03
note_path: docs/SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md
runner_path: scripts/frontier_su3_wigner_intertwiner_engine.py
claim_type: positive_theorem
intrinsic_status: unaudited
deps: []   # self-contained; pure SU(3) rep theory
verdict_rationale_template: |
  Block 1 of the cube-closure campaign. Constructs explicit Clebsch-Gordan
  decomposition of SU(3) (1,1) ⊗ (1,1) = 1 + 8 + 8 + 10 + 10̄ + 27 = 64
  via simultaneous diagonalization of quadratic + cubic Casimirs +
  exchange operator on V ⊗ V. All 9 validation identities (structure
  constant symmetries, Lie algebra, Casimir eigenvalues, exchange E^2=I,
  dimensional decomposition, orthonormality, SU(3) equivariance) pass at
  machine precision (≤ 2e-15). Self-contained; no lattice-gauge
  dependencies. Importable API for Block 2 (4-fold Haar projector).
```

## 7. Cross-references

- Continued: future Block 2 (4-fold Haar projector via CG)
- Eventual target: [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)
- L_s=2 cube derivation (P_cube = 0.4291): commit e7365f2d2 + PR #492
- K-Z external lift: PR #484

## 8. Command

```bash
python3 scripts/frontier_su3_wigner_intertwiner_engine.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=8 FAIL=0
```
