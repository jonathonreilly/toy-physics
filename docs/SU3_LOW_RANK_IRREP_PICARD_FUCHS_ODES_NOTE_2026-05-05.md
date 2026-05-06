# SU(3) Low-Rank Irrep Character Coefficients: Picard-Fuchs ODE Catalog

**Date:** 2026-05-05
**Claim type:** bounded_theorem
**Status:** bounded computational theorem, unaudited.
**Depends on:** [`PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md)
**Primary runner:** [`scripts/frontier_su3_low_rank_picard_fuchs_odes_2026_05_05.py`](../scripts/frontier_su3_low_rank_picard_fuchs_odes_2026_05_05.py)
**Output:** [`outputs/su3_low_rank_pf_odes_2026_05_05.json`](../outputs/su3_low_rank_pf_odes_2026_05_05.json)

## Headline

For the SU(3) character coefficients

```
c_{(p,q)}(β) := ∫_{SU(3)} χ_{(p,q)}(U) exp(β · Re Tr U / 3) dU
```

the selected low-rank representatives
`(p, q) in {(0,0), (1,0), (1,1), (2,0), (2,1), (2,2), (3,0)}`
satisfy closed-form linear holonomic Picard-Fuchs ODEs in `beta` of
order 3 with explicit primitive-integer polynomial coefficients.

The order-3 structure is **uniform** — the same as the repo's V=1
(trivial irrep) result. The polynomial-coefficient degree grows with
the irrep weight: deg 2 for (0,0), deg 3 for (1,1), deg 4 for (1,0),
deg 5 for (2,0)/(2,1)/(2,2), deg 6 for (3,0).

By conjugation symmetry `c_{(q,p)} = c_{(p,q)}`, the same catalog also
covers the conjugate representatives. It does not claim coverage of
the full `(p,q) <= (3,3)` box.

These ODEs are explicit — verified to numerical error ≤ 3.1×10⁻⁸ vs
direct Bessel-determinant numerical evaluation on β ∈ [1, 8] — and
extend the repo's existing V=1 Picard-Fuchs runner-backed result to a
larger selected character set.

## ODE catalog

Each ODE has the form

```
Σ_{k=0..3} P_k(β) · c^{(k)}(β) = 0
```

with `P_k(β) ∈ ℤ[β]` listed below, primitive-integer normalization.

### (0,0) trivial — dim 1 (recovers the V=1 note)

```
P_0(β) = -β² - 10β
P_1(β) = -4β² - 2β + 120
P_2(β) = -β² + 60β
P_3(β) = 6β²
```

Verification error: **8.3 × 10⁻¹¹**.

### (1,0) fundamental — dim 3

```
P_0(β) = -β⁴ - 20β³ - 138β² - 240β - 1200
P_1(β) = -4β⁴ - 42β³ + 30β² + 1200β
P_2(β) = -β⁴ + 50β³ + 660β²
P_3(β) = 6β⁴ + 60β³
```

Verification error: **5.9 × 10⁻¹²**.

### (1,1) adjoint — dim 8

```
P_0(β) = -β³ - 13β² - 30β - 288
P_1(β) = -4β³ - 5β² + 78β
P_2(β) = -β³ + 66β²
P_3(β) = 6β³
```

Verification error: **5.1 × 10⁻¹²**.

### (2,0) symmetric — dim 6

```
P_0(β) = -β⁵ - 17β⁴ - 27β³ + 540β² + 2100β + 30240
P_1(β) = -4β⁵ - 30β⁴ + 321β³ + 1428β² - 9072β
P_2(β) = -β⁵ + 53β⁴ + 546β³ - 6048β²
P_3(β) = 6β⁵ + 42β⁴ - 504β³
```

Verification error: **1.6 × 10⁻⁸**.

### (2,1) — dim 15

```
P_0(β) = -β⁵ - 50β⁴ - 1320β³ - 14304β² - 64224β - 483840
P_1(β) = -4β⁵ - 162β⁴ - 3312β³ - 6048β² + 41472β
P_2(β) = -β⁵ + 20β⁴ + 1872β³ + 55296β²
P_3(β) = 6β⁵ + 240β⁴ + 4608β³
```

Verification error: **2.9 × 10⁻¹¹**.

### (2,2) — dim 27

```
P_0(β) = -β⁵ - 22β⁴ - 924β³ - 12960β² - 69696β - 691200
P_1(β) = -4β⁵ - 50β⁴ - 3060β³ - 6624β² - 8640β
P_2(β) = -β⁵ + 48β⁴ + 72β³ + 51840β²
P_3(β) = 6β⁵ + 72β⁴ + 4320β³
```

Verification error: **3.1 × 10⁻¹¹**.

### (3,0) — dim 10

```
P_0(β) = -β⁶ - 37β⁵ - 387β⁴ - 864β³ - 3888β² + 104976β + 734832
P_1(β) = -4β⁶ - 110β⁵ - 195β⁴ + 3564β³ + 16524β² - 81648β
P_2(β) = -β⁶ + 33β⁵ + 1782β⁴ + 972β³ - 75816β²
P_3(β) = 6β⁶ + 162β⁵ - 5832β³
```

Verification error: **3.1 × 10⁻⁸**.

## Numerical c_{(p,q)}(6) values

Computed via the Bessel-determinant identity used by the runner:

```
c_(0,0)(6) = 3.4414      (= J(6); cf. V=1 note)
c_(1,0)(6) = 4.3624
c_(1,1)(6) = 4.4673
c_(2,0)(6) = 2.8074
c_(2,1)(6) = 2.4927
c_(2,2)(6) = 1.2549
c_(3,0)(6) = 1.2065
```

## Method (creative-telescoping ansatz)

For each irrep R, the script:

1. Constructs the Bessel-determinant Taylor series for `c_R(β)` to
   high order (using Bars' identity with a sum over central-k bands of
   3×3 modified-Bessel determinants).
2. For each candidate (order r, polynomial-coefficient degree d),
   assembles the linear ansatz
   `Σ P_k(β) c^{(k)}(β) = 0` with unknowns `{p_{k,m}}`.
3. Matches Taylor coefficients of β → 0; this gives a linear system
   over ℚ.
4. Finds the smallest (r, d) for which a non-trivial null vector
   exists, picks primitive-integer normalization.
5. Verifies by (i) substituting back into more series coefficients than
   were used to solve, and (ii) numerically integrating from
   β=1 initial conditions against direct Bessel-determinant evaluation.

For the selected representatives in this note, the detected minimal
rank is order 3.

## Cited authorities

- **Bars (1980)**: `J(β) = Σ_{k∈ℤ} det[I_{i-j+k}(β/3)]_{i,j=0,1,2}`
  generalized to character integrals via Schur duality.
- **Wilf-Zeilberger creative telescoping** (J. Amer. Math. Soc. 1990).
- **Saito-Sturmfels-Takayama** (*Gröbner Deformations of Hypergeometric
  Differential Equations*).
- **Bernstein D-module theory**: any integral of `exp(β·polynomial) ·
  algebraic` over a compact algebraic group is holonomic in β; here
  `c_R(β)` integrates a fixed character (algebraic in coordinates)
  against `exp(β/3 · Re Tr U)`.
- [`PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md),
  the repo note for the trivial-irrep base case.

## Why this matters for the famous-problem attack

The framework's existing reduction theorem
`GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md`
expresses `⟨P⟩(β=6, L→∞)` via the boundary character measure
`ρ_{(p,q)}(6)` of the 3D unmarked spatial Wilson environment with
marked-plaquette boundary. The framework's `Theorem 3` no-go
`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`
proves that `c_R(6)` and SU(3) intertwiners alone cannot fix
`ρ_{(p,q)}(6)`; the residual is genuinely 3D-geometric.

What this catalog gives the framework:
- Exact symbolic structure for every `c_R(β)` in the selected low-rank
  set — these are the local Wilson-action factors.
- A **complete analytic basis** for character-truncation studies:
  any truncated approximation to `⟨P⟩(β=6, L→∞)` can now be expressed
  in terms of `{c_R(β)}` PF-ODE solutions plus a finite-rank tensor
  contraction with `ρ_{(p,q)}(6)`.
- The remaining open object is sharper: derive `ρ_{(p,q)}(6)` for the
  3D unmarked Wilson environment.

## What this does NOT close

- `⟨P⟩(β=6, L→∞) = 0.5934` analytic closed form (the famous open
  lattice problem). PR #539's 5-volume FSS numerical comparator
  remains outside this note.
- The boundary character measure `ρ_{(p,q)}(6)` is provably NOT
  determined by the `c_R(6)` data alone (framework's existing
  Theorem 3 no-go). This catalog gives the local-Wilson side; the
  3D-environment side needs separate machinery.

## Claim boundary

This note claims only the runner-backed ODE catalog for the selected
low-rank representatives above, together with numerical verification
against the Bessel-determinant evaluator on `beta in {2,4,6,8}`. It
does not claim the full `(p,q) <= (3,3)` box, literature priority, a
thermodynamic-limit Wilson plaquette value, or a derivation of the
boundary character measure `rho_{(p,q)}(6)`.

## Reusable artifact

[`scripts/frontier_su3_low_rank_picard_fuchs_odes_2026_05_05.py`](../scripts/frontier_su3_low_rank_picard_fuchs_odes_2026_05_05.py)
— derives all 7 PF ODEs from scratch via creative-telescoping ansatz,
verifies each numerically, writes output JSON.

[`outputs/su3_low_rank_pf_odes_2026_05_05.json`](../outputs/su3_low_rank_pf_odes_2026_05_05.json)
— machine-readable ODE coefficients for downstream consumers.

## Ledger hint

- **claim_id:** `su3_low_rank_irrep_picard_fuchs_odes_note_2026-05-05`
- **note_path:** `docs/SU3_LOW_RANK_IRREP_PICARD_FUCHS_ODES_NOTE_2026-05-05.md`
- **runner_path:** `scripts/frontier_su3_low_rank_picard_fuchs_odes_2026_05_05.py`
- **claim_type:** `bounded_theorem`
- **dependency_chain:**
  - `PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md` (V=1 PF ODE)
