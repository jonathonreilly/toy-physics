# Gauge-Vacuum Plaquette Finite Tensor-Word Packet — Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status:** bounded - finite truncated tensor-word packet only; no
parent theorem status change or untruncated transfer claim.
**Primary runner:** [`scripts/frontier_gauge_vacuum_plaquette_finite_tensor_word_packet.py`](../scripts/frontier_gauge_vacuum_plaquette_finite_tensor_word_packet.py)

## Claim

This note is the **split note for one finite tensor-word packet**. It
responds to prior audit feedback that allowed a source row scoped only
to the finite packet, without claiming the broader parent theorem. It
does **not** claim the parent structural matrix-element identity
`z_(p,q)^env(beta) = <chi_(p,q), (T_beta^env,tensor)^(L_perp-1)
eta_beta^env>`. It claims only three explicit numerical properties of
one specific matrix constructed at `beta = 6` from canonical truncated
local ingredients.

**Construction.** On the truncated dominant-weight box `0 ≤ p, q ≤
NMAX = 4` and Wilson Bessel mode sum truncated to `MODE_MAX = 80`,
build:

```text
diag_c   :=  diag( normalized )                                           (1)
            where  normalized[(p,q)]  =  c_(p,q)(6) / ( d_(p,q) · c_(0,0)(6) )
            on the NMAX = 4 box, computed from the Wilson character
            integral via Schur-Weyl Bessel-determinant truncated to
            MODE_MAX = 80 modes,

N_f      :=  fundamental-rep fusion-multiplicity matrix on the box,    (2)
N_fbar   :=  anti-fundamental fusion-multiplicity matrix on the box,

tensor_word
         :=  diag_c · ( N_f + N_fbar ) · diag_c · ( N_f + N_fbar )^T · diag_c.  (3)
```

This is a real square matrix indexed by `(p, q) ∈ [0..4]² → [0..24]`
(25 dominant-weight states), built only from `c_(p,q)(6)` truncated
Wilson coefficients, the corresponding `SU(3)` representation
dimensions `d_(p,q)`, and integer-valued fusion multiplicities `N_f,
N_fbar` on the same box.

**Bounded properties (load-bearing).** The constructed `tensor_word`
matrix satisfies the three structural properties below at the
numerical precision specified:

(P1) **Nonnegativity of matrix entries.**

```text
tensor_word[i, j]  ≥  0   for all i, j ∈ [0..24].                         (P1)
```

(P2) **Conjugation-swap symmetry.** Let `S` denote the
conjugation-swap permutation matrix that sends `(p, q) → (q, p)` on
the box. Then

```text
S · tensor_word  =  tensor_word · S    (entry-wise equal at machine
                                        precision).                       (P2)
```

(P3) **Nonnegative boundary amplitude under unit-vector readout.**
Let `boundary0` be the unit vector pointing at the `(0, 0)` index.
Then

```text
amp  :=  tensor_word · boundary0 ;
amp[i]  ≥  0   for all i ∈ [0..24].                                       (P3)
```

**Derived corollary of (P2)** (not a separate load-bearing property):
since `(0, 0)` is fixed by the conjugation-swap (i.e., `S · boundary0 =
boundary0` because `(0, 0) → (0, 0)` under `(p, q) → (q, p)`), property
(P2) immediately yields

```text
S · amp  =  S · tensor_word · boundary0
         =  tensor_word · S · boundary0    [by (P2)]
         =  tensor_word · boundary0
         =  amp.                                                          (P3-corollary)
```

The runner verifies (P1), (P2), (P3) at full numpy double-precision
tolerance on the explicit matrix constructed from the truncated
canonical inputs, and additionally verifies the (P3-corollary) numerical
identity to confirm the chain `S · boundary0 = boundary0` plus (P2)
combine consistently.

## Bounded admissions

(BA-1) **Canonical truncated local Wilson coefficients.** The values
`c_(p,q)(6)` on the `NMAX = 4` weight box, truncated to the
`MODE_MAX = 80` Bessel mode sum in the Schur-Weyl determinant
representation, are imported from
[`GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md`](GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md)
which checks the same construction by two independent integrators (Schur-Weyl
Bessel-determinant and Weyl-Cartan torus integration) at the same
truncation parameters.

(BA-2) **`SU(3)` fundamental and anti-fundamental fusion
multiplicities.** The integer-valued matrices `N_f` and `N_fbar`
encode the standard `SU(3)` Clebsch-Gordan multiplicities for tensor
products with the fundamental rep `(1, 0)` and anti-fundamental rep
`(0, 1)`, restricted to the `NMAX = 4` dominant-weight box. These are
elementary `SU(3)` representation theory; the runner constructs them
directly via the standard six-neighbor recurrence. Admitted as a
bounded textbook input on the truncated box.

(BA-1)–(BA-2) are bounded inputs, not derived from the physical `Cl(3)`
local algebra on the `Z^3` spatial substrate in this note. They are
textbook compact-Lie-group facts on the finite truncated box.

## Proof-Walk

| Step | Argument | Load-bearing input |
|---|---|---|
| Construct `diag_c` from `c_(p,q)(6)` and `d_(p,q)` per (1) | algebraic substitution + (BA-1) | (BA-1) truncated Wilson coefficients |
| Construct `N_f`, `N_fbar` per (2) via standard six-neighbor `SU(3)` recurrence on the `NMAX = 4` box | (BA-2) `SU(3)` fusion multiplicities | (BA-2) elementary `SU(3)` rep theory |
| Construct `tensor_word` per (3) by direct matrix products | algebra over real entries | none beyond (BA-1)–(BA-2) |
| (P1) check `min(tensor_word) ≥ 0` by direct entry-wise minimum | numerical computation on the constructed matrix | runner-direct |
| (P2) check `‖S · tensor_word − tensor_word · S‖_∞ < 10⁻¹²` (machine precision) | numerical computation | runner-direct |
| (P3) check `min(tensor_word · boundary0) ≥ 0` by direct entry-wise minimum on the boundary amplitude | numerical computation | runner-direct |
| (P3-corollary, derived) verify `S · boundary0 = boundary0` exactly (trivially: `(0,0) → (0,0)` under conjugation swap), then check `‖S · amp − amp‖_∞ < 10⁻¹²` follows automatically from (P2) | derived from (P2) | runner-direct (consistency check) |

All steps are class-A algebraic / direct-numerical computations on the
explicitly constructed matrix. The chain closes from (BA-1)–(BA-2)
plus the runner's matrix construction; no further authority is invoked.

## Exact / Numerical Check

The runner verifies, on the full `NMAX = 4`, `MODE_MAX = 80` truncation:

(A) **Construction reproducibility.** `diag_c[(0,0)] = 1` exactly
(definition of normalization); `diag_c[(p,q)] = c_(p,q)(6) / (d_(p,q)
· c_(0,0)(6))` matches the Wilson-environment companion values on the
same box to machine precision (cross-check via the companion's
two-integrator agreement).

(B) **(BA-2) fusion-multiplicity construction.** `N_f` and `N_fbar`
have entries in `{0, 1}`, are conjugate to each other under `S`
(`S · N_f = N_fbar · S` and vice versa), and reproduce the standard
`SU(3)` six-neighbor recurrence on the `NMAX = 4` box.

(C) **(P1) nonnegativity.** `min_{i,j} tensor_word[i, j] ≥ 0` at
double precision.

(D) **(P2) conjugation-swap symmetry.** `‖S · tensor_word −
tensor_word · S‖_∞ < 10⁻¹²`.

(E) **(P3)** `min_i (tensor_word · boundary0)[i] ≥ 0`.

(F) **(P3-corollary, consistency)** `‖S · amp − amp‖_∞ < 10⁻¹²` follows
immediately from (P2) because `S · boundary0 = boundary0` (the
`(0, 0)` state is fixed by `(p, q) → (q, p)`). The runner verifies
both `S · boundary0 = boundary0` exactly and the numerical
`‖S · amp − amp‖_∞` bound to confirm the chain composes consistently;
this is a consistency check, not a separate load-bearing property.

(G) **Forbidden-import audit.** Imports limited to numpy + scipy
(family convention with the Wilson-environment companion
`frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py`).

## Dependencies

- [`GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md`](GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md)
  for the bounded truncated `c_(p,q)(6)` Wilson coefficients on the
  `NMAX = 4` box.
- `GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md`
  for parent context only. The parent's broader structural
  identification of spatial-environment boundary data with the
  tensor-transfer law remains its own claim.
- `MINIMAL_AXIOMS_2026-05-03.md` for the physical `Cl(3)` local
  algebra on the `Z^3` spatial substrate baseline.

## Boundaries

This note does **not**:

- claim the parent note's structural matrix-element identity
  `z_(p,q)^env(beta) = <chi_(p,q), (T_beta^env,tensor)^(L_perp-1)
  eta_beta^env>` between actual spatial-environment boundary
  amplitudes and the tensor-transfer operator readout. That identity
  is an assertion of the parent
  `GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md`,
  not of this bounded note. The truncated `tensor_word` matrix
  constructed here is one specific matrix object; the parent's
  matrix-element identity remains the open subject of the parent's
  audit row;
- close the full untruncated tensor-transfer construction at `beta = 6`
  (Perron solve, convergence/positivity beyond the `NMAX = 4` weight
  box and `MODE_MAX = 80` Bessel support, multi-tensor-word coverage);
- close `analytic P(6)` or any `χ_L(β)` expression;
- change any parent or companion source row.

What this note **does**: introduce a clean, narrow, bounded companion
that exhibits the three structural properties (P1)–(P3) of the one
specific `tensor_word` matrix actually constructed here. (BA-1)–(BA-2)
are admitted bounded textbook inputs.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_finite_tensor_word_packet.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
RESULT: one explicit positive matrix tensor_word constructed from
canonical truncated local Wilson coefficients (NMAX=4, MODE_MAX=80,
beta=6) and SU(3) fusion multiplicities verifies three structural
properties at double precision: (P1) nonnegativity of matrix entries,
(P2) conjugation-swap symmetry, (P3) nonnegative boundary amplitude
under (0,0)-component unit-vector readout. The boundary-amplitude
conjugation symmetry follows immediately from (P2) since (0,0) is
fixed by the conjugation swap (consistency check, not a separate
load-bearing property). The parent's broader matrix-element identity
z_(p,q)^env = <chi, T^L eta> is NOT claimed here; this is a
split-note bounded packet only.
```
