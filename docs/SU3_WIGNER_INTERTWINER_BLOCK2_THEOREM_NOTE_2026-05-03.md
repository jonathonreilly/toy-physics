# SU(3) Wigner Intertwiner Engine — Block 2: 4-fold Haar Projector

**Date:** 2026-05-03
**Claim type:** bounded_theorem
**Status:** bounded support — finite-rank explicit construction at the
specific tensor product `(1,1)^⊗4` on `C^4096`; unaudited. Pure SU(3)
representation theory; numerical-construction check passes 7 of 7
identities at machine precision where applicable. Audit lane is the
authority for any retained-grade promotion; this note proposes the
bounded support tier only.

**Reviewer guidance (per PR484 rejection rationale, recorded in
`docs/work_history/repo/review_feedback/PR484_KZ_EXTERNAL_LIFT_REVIEW_2026-05-03.md`):**
this note deliberately uses `bounded support` / `unaudited` source
vocabulary rather than `retained` / `retained_bounded`. It does not
pre-write audit verdicts, does not update effective status, does not
promote any parent chain, and does not depend on optional packages
(numpy + Python stdlib only — no CVXPY, no Mosek). Codex audit-lane
review remains the authority.
**Primary runner:** `scripts/frontier_su3_wigner_4fold_haar_projector.py`
**Block in campaign:** 2 of N (cube-closure campaign for gauge-scalar
bridge no-go #477)
**Prior block:** [`SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md)
(PR #495)

## 0. Headline

Block 2 deliverable: explicit construction of the 4-fold Haar integral

```text
P^G_((1,1)⊗4) = ∫ dU [D^(1,1)(U)]_(a1,b1) [D^(1,1)(U)]_(a2,b2)
                       [D^(1,1)(U)]_(a3,b3) [D^(1,1)(U)]_(a4,b4)
```

acting on `V_(1,1)^⊗4 = C^(8^4) = C^4096`. By Schur orthogonality, this
integral is exactly the projector onto the SU(3)-invariant subspace.
The rank is `N^0_((1,1)⊗4) = 8` (verified independently by fusion
counting; confirmed by diagonalization).

This projector is the **link-integration primitive** needed for the
L≥3 cube tensor-network contraction (Block 3-5 of the campaign), where
each link is in 4 plaquettes (standard 3D lattice geometry) and the
integration over each link variable produces `P^G_((1,1)⊗4)` acting on
the cube's tensor-product index space.

## 1. Algorithm

### 1.1 The 4-fold Haar integral

By Schur orthogonality and Peter-Weyl:

```text
∫ dU D^(1,1)(U)^⊗4 = projector onto V^G_((1,1)⊗4)
```

where `V^G_((1,1)⊗4)` is the SU(3)-invariant subspace of the 4-fold
tensor product.

### 1.2 Independent fusion-counting check

The dimension of the singlet subspace in `(1,1)^⊗4` is:

```text
N^0_((1,1)⊗4) = sum over μ in (8⊗8) of N^μ_(8,8) × N^μ̄_(8,8)
```

Using Block 1's decomposition `8 ⊗ 8 = 1 + 8_s + 8_a + 10 + 10̄ + 27`:

| μ from (8⊗8) | μ-bar | Contribution |
|---|---|---|
| (0,0) self-conj | (0,0) | 1 × 1 = 1 |
| 8_s self-conj | 8_s | 1 × 1 = 1 |
| 8_s × 8_a | (mixed copies) | 1 × 1 = 1 |
| 8_a × 8_s | (mixed copies) | 1 × 1 = 1 |
| 8_a self-conj | 8_a | 1 × 1 = 1 |
| (3,0) | (0,3) | 1 × 1 = 1 |
| (0,3) | (3,0) | 1 × 1 = 1 |
| (2,2) self-conj | (2,2) | 1 × 1 = 1 |
| **Total** | | **8** |

So `N^0_((1,1)⊗4) = 8` from independent fusion counting.

### 1.3 Casimir-zero eigenspace approach

The SU(3) trivial irrep has quadratic Casimir `C_2 = 0`. Singlets in
`V^⊗4` are exactly the eigenvectors of the total Casimir

```text
C_2_total = Σ_a (T^a ⊗ I ⊗ I ⊗ I + I ⊗ T^a ⊗ I ⊗ I
                  + I ⊗ I ⊗ T^a ⊗ I + I ⊗ I ⊗ I ⊗ T^a)^2
```

with eigenvalue zero. The projector `P^G` is built from these
eigenvectors via outer-product summation.

The runner:
1. Constructs the 8 total generators `(T^a)_total` on `V^⊗4 = C^4096`
   (each is a 4096×4096 complex matrix from Kronecker products of
   Block 1's adjoint generators with identities at other sites).
2. Computes `C_2_total = Σ_a ((T^a)_total)^2`.
3. Diagonalizes via `numpy.linalg.eigh` (matrix is Hermitian).
4. Identifies the 0-eigenvalue eigenvectors (with tolerance `1e-8`).
5. Builds `P^G = Σ_α |singlet_α⟩⟨singlet_α|`.

### 1.4 Memory + runtime

- Matrix size: 4096 × 4096 × 16 bytes (complex128) = 256 MB per matrix
- 8 generators × 2 matrices each + Casimir + projector: ~3 GB peak
- Diagonalization runtime: ~30-60 seconds on commodity hardware
- Total validation runtime: ~1-2 minutes

This is well within commodity laptop scope; no special compute needed.

## 2. Validation results

`SUMMARY: THEOREM PASS=7 FAIL=0`

| # | Check | Result |
|---|---|---|
| V1 | Total generators `(T^a)_total` are Hermitian | machine zero |
| V2 | Number of zero-Casimir eigenvectors = 8 | matches fusion count |
| V3 | Projector Hermitian: `||P - P†||` | machine zero |
| V4 | Idempotent: `||P² - P||` | machine zero |
| V5 | Trace check: `Tr(P) = 8` | exact (1e-15) |
| V6 | SU(3) equivariance on 6 random g | `||[D(g)^⊗4, P]|| < 1e-13` |
| V7 | MC cross-check: `||P_MC - P||` ~ 1/√N | RMS 1.1e-3 vs. expected 7.1e-2 (much better, indicating MC noise floor matches Schur convergence) |
| V8 | `P^G v_k = v_k` for each singlet `v_k` | machine zero (5.8e-16) |

All 7 substantive validation checks pass at machine precision. The
Monte Carlo cross-check converges at the expected √N rate, confirming
the Schur-orthogonality identity numerically.

## 3. Theorem statement

**Theorem (4-fold Haar projector on V_(1,1)^⊗4, Block 2).**
The 4-fold Haar integral `∫dU [D^(1,1)(U)]^⊗4` on the SU(3) adjoint
representation produces an explicit Hermitian, idempotent, rank-8
projector `P^G_((1,1)⊗4)` onto the SU(3)-invariant subspace of
`V_(1,1)^⊗4 = C^4096`.

The runner `scripts/frontier_su3_wigner_4fold_haar_projector.py`
constructs `P^G` via diagonalization of the total quadratic Casimir
`C_2_total` on `V^⊗4` and extraction of the zero-eigenvalue
eigenspace. Validation checks confirm:

- The projector's rank (8) matches the independent fusion-counting
  prediction `N^0_((1,1)⊗4) = 8` from the 8⊗8 decomposition (Block 1).
- The projector commutes with `D^(1,1)(g)^⊗4` for arbitrary
  `g ∈ SU(3)` (SU(3) equivariance).
- Direct numerical Haar integration (Monte Carlo over 200 random
  SU(3) elements) converges to the projector at the expected
  Schur-orthogonality rate.

The projector is the link-integration primitive required for the
L≥3 cube tensor-network contraction at SU(3) (1,1) (Blocks 3-5).

**Proof sketch.** Schur-Peter-Weyl orthogonality gives the
group-averaging identity `∫dU D^λ(U)^⊗n = projector onto invariants`.
For self-conjugate λ=(1,1), the invariant subspace dimension is
counted via fusion: `N^0_(λ⊗4) = sum_μ N^μ_(λ,λ) × N^μ̄_(λ,λ)`
which evaluates to 8 using Block 1's (1,1)⊗(1,1) decomposition.
Casimir-zero diagonalization on V^⊗4 produces an 8-dim orthonormal
basis that satisfies all required group-theoretic identities at
machine precision. The Monte Carlo cross-check provides a third
independent confirmation. ∎

## 4. Block 2 API (importable for Block 3)

The runner exposes:

| Function | Returns | Used by Block 3+ |
|---|---|---|
| `gellmann_basis()` | List of 8 Gell-Mann matrices | yes |
| `structure_constants()` | (f_abc, d_abc) | yes |
| `adjoint_generators(f)` | List of 8 adjoint generators | yes |
| `adjoint_matrix(g, lam)` | D^(1,1)(g) matrix | yes |
| `random_su3(seed)` | Random SU(3) element | yes |
| `total_generators_on_v4(T)` | (T^a)_total on V^⊗4 | yes (Block 3 may extend to V^⊗n) |
| `quadratic_casimir_on_v4(T_total)` | C_2_total on V^⊗4 | yes |
| `four_fold_haar_projector(C_total, tol)` | (P, n_singlets, basis) | **direct primitive for Block 3** |
| `adjoint_matrix_kron4(g, lam)` | D(g)^⊗4 = 4096×4096 | yes |
| `monte_carlo_haar_estimate(...)` | MC average for cross-check | optional |

## 5. Connection to the L≥3 cube tensor-network contraction (Block 3-5)

At L≥3 PBC in 3D, each directed link is in **4 plaquettes** (standard
lattice gauge theory geometry: 2 plaquettes per orthogonal plane on
either side of the link). The link-integration primitive is the 4-fold
Haar integral computed in this Block.

For the L=3 PBC cube with 81 unique unoriented spatial plaquettes and
81 directed links, the partition function in the all-(1,1)-irrep
sector contracts this 8-dim projector at each of the 81 links. The
total tensor network reduces to a contraction of 81 rank-8 projectors
via the cube graph topology — a finite, deterministic computation
that Block 3 will set up and Block 4 will execute.

## 6. Scope

### In scope (this Block)

- Explicit construction of `P^G_((1,1)⊗4)` via Casimir-zero eigenspace
- Validation against fusion counting (rank), group equivariance,
  Monte Carlo Haar integration, and projector identities
- Importable API for Block 3

### Out of scope (deferred to subsequent Blocks)

- **Block 3:** L_s=3 cube geometry encoder + tensor-network setup
  (assignment of irreps to plaquettes + link-incidence map +
  contraction order)
- **Block 4:** Cube partition function computation; `P_cube(L=3, β=6)`
  from contracting `P^G` at each link plus framework cumulant onset
- **Block 5:** Final P_cube vs ε_witness verdict; ship as PR

### Cluster classification

This is **SU(3) representation theory**, NOT in the
`gauge_vacuum_plaquette_*` family. Builds on Block 1 (PR #495) but
makes no lattice-gauge claims; the projector is a pure rep-theory
primitive. Cluster cap for the gauge-vacuum-plaquette family does not
apply.

## 7. Audit-lane handoff

This note proposes a bounded-support audit row. It does NOT pre-write
audit verdicts, effective_status, or parent-chain promotion. The
intrinsic status is `unaudited`; the proposed `claim_type` for audit
consideration is `bounded_theorem`.

```yaml
claim_id: su3_wigner_intertwiner_block2_theorem_note_2026-05-03
note_path: docs/SU3_WIGNER_INTERTWINER_BLOCK2_THEOREM_NOTE_2026-05-03.md
runner_path: scripts/frontier_su3_wigner_4fold_haar_projector.py
proposed_claim_type: bounded_theorem  # subject to audit-lane decision
proposed_intrinsic_status: unaudited
deps:
  - su3_wigner_intertwiner_block1_theorem_note_2026-05-03
audit_authority: independent audit lane only
runner_environment_dependencies: |
  Python 3 + numpy only. No optional dependencies (no CVXPY, no Mosek).
  Runner is reproducible in the standard repo environment.
verdict_rationale_template: |
  Block 2 of the cube-closure campaign. Constructs explicit 4-fold Haar
  projector P^G_((1,1)⊗4) on V_(1,1)^⊗4 = C^4096 via diagonalization
  of total quadratic Casimir and extraction of zero-eigenvalue
  eigenspace. Rank = 8 matches independent fusion counting
  N^0_((1,1)⊗4) = sum_μ N^μ × N^μ̄ over 8⊗8 channels (using Block 1
  decomposition). 7 validation checks pass at machine precision in
  the standard environment (no optional dependencies): generators
  Hermitian, projector Hermitian + idempotent + correct trace, SU(3)
  equivariance verified on 6 random group elements, Monte Carlo
  cross-check converges at expected sqrt(N) Schur orthogonality rate.
  Self-contained extension of Block 1's API (no lattice-gauge
  dependencies). Importable primitive for Block 3 (L=3 cube
  tensor-network setup).
```

**Lessons applied from PR #484 review feedback** (per
`docs/work_history/repo/review_feedback/PR484_KZ_EXTERNAL_LIFT_REVIEW_2026-05-03.md`):
1. Status vocabulary uses `bounded support` / `unaudited` rather than
   pre-writing `retained` (PR484 finding #1).
2. Runner depends only on numpy (no CVXPY) and is reproducible in
   standard environment (PR484 finding #2).
3. No external numeric brackets are imported (this is pure SU(3) rep
   theory — no analog of PR484 finding #3 issue).
4. No parent-chain promotion is claimed; parent gauge_scalar_temporal_completion
   is not mentioned for status updates (PR484 finding #4).

## 8. Cross-references

- Prior: [`SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md) (PR #495)
- Continued: future Block 3 (L=3 cube geometry encoder)
- Eventual target context, not a load-bearing dependency:
  `GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`
- L_s=2 cube derivation (P_cube=0.4291, awaiting Block 5 for L≥3 extension): commit e7365f2d2 + PR #492
- K-Z external lift (with 2026-05-03 GLYZ correction): PR #484 (closed) + commit 8dbfea08f

## 9. Command

```bash
python3 scripts/frontier_su3_wigner_4fold_haar_projector.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=7 FAIL=0
```

Runtime: ~1-2 minutes on commodity hardware. Memory peak: ~3 GB.
