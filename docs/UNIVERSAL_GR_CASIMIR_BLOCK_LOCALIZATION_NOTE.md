# Universal GR Casimir Block Localization on `PL S^3 x R`

**Claim type:** positive_theorem
**Status authority:** source-note proposal only; audit verdict and effective
status are set by the independent audit lane.
**Date:** 2026-04-14
**Updated:** 2026-05-16 (proof-walk pass; explicit class-A derivation aligned
to runner; cached runner output quoted)
**Role:** direct universal route / canonical block-localization theorem step
**Primary runner:** [`scripts/frontier_universal_gr_casimir_block_localization.py`](../scripts/frontier_universal_gr_casimir_block_localization.py)
**Cached runner output:** [`logs/runner-cache/frontier_universal_gr_casimir_block_localization.txt`](../logs/runner-cache/frontier_universal_gr_casimir_block_localization.txt)
(`runner_sha256 = c5a083df65acce488cb6bff71b524452838db1a058578f02fdbf89fd8dbb0536`; `exit_code = 0`; `status = ok`; `PASS=8 FAIL=0 TOTAL=8`).

## Claim (block-localization theorem)

Let `V := Sym^2(R^4)` be the real 10-dimensional space of symmetric `4 x 4`
real matrices in coordinate order `(t, x, y, z)`, equipped with the
Frobenius inner product `<a, b> := sum_{i,j} a_{ij} b_{ij}`. Let `SO(3)` act
on `V` by `rho(R) h := R^T h R` with `R = diag(1, R_3)` and `R_3 in SO(3)`,
i.e. the spatial-block `SO(3)` action holding the temporal index fixed.
Let `B := (e_0, e_1, ..., e_9)` be the orthonormal frame on `V` defined in
[Representation Fixed in the Packet](#representation-fixed-in-the-packet)
below.

Define the rank-2 projector

```
Pi_A1 := diag(1, 0, 0, 0, 1, 0, 0, 0, 0, 0)     (matrix on V in basis B)
```

onto `(h_tt, (h_xx + h_yy + h_zz)/sqrt(3))`, and let
`Pi_perp := I - Pi_A1` be the rank-8 complement projector. Let
`G_x, G_y, G_z` be the infinitesimal generators of `rho` on `V` in basis
`B`, restricted to the complement, and define the Casimir operator

```
C := G_x^2 + G_y^2 + G_z^2  on  range(Pi_perp).
```

Define `P_lapse, P_shift, P_trace, P_shear` to be the spectral projectors
of `C` together with the trivial-irrep refinement on `range(Pi_A1)`:

- `P_lapse := diag(1, 0, 0, 0, 0, 0, 0, 0, 0, 0)`
- `P_trace := diag(0, 0, 0, 0, 1, 0, 0, 0, 0, 0)`
- `P_shift := lift_to_V(Pi_{C = -2} on range(Pi_perp))`
- `P_shear := lift_to_V(Pi_{C = -6} on range(Pi_perp))`

**Theorem (block-localization).** With definitions as above, the following
exact identities hold over `Q[sqrt 2, sqrt 3, sqrt 6]` SymPy radicals:

1. **(T1) Basis is orthonormal.** The Gram matrix `(<e_i, e_j>)_{i,j}` of
   `B` is the `10 x 10` identity.
2. **(T2) Generators close `so(3)` exactly.** `[G_a, G_b] = epsilon_{abc}
   G_c` for `(a, b, c) in {(x, y, z), (y, z, x), (z, x, y)}` up to
   orientation sign, computed entrywise.
3. **(T3) `Pi_A1` is `SO(3)`-invariant.** `Pi_A1 G_a Pi_perp = 0` and
   `Pi_perp G_a Pi_A1 = 0` for each `a in {x, y, z}`. Equivalently, the
   subspace `range(Pi_A1)` and its orthogonal complement `range(Pi_perp)`
   are each `so(3)`-stable.
4. **(T4) Complement Casimir spectrum.** In the displayed complement
   ordering `(h_{tx}, h_{ty}, h_{tz}, q_1, q_2, h_{xy}, h_{xz}, h_{yz})`
   with `q_1 := (h_{xx} - h_{yy})/sqrt 2`,
   `q_2 := (h_{xx} + h_{yy} - 2 h_{zz})/sqrt 6`,
   the complement Casimir is diagonal:
   `diag(C) = (-2, -2, -2, -6, -6, -6, -6, -6)`,
   off-diagonal entries identically zero. Hence the spectrum is `-2` with
   multiplicity `3` and `-6` with multiplicity `5`.
5. **(T5) Rank table.** `rank(P_lapse) = 1`, `rank(P_shift) = 3`,
   `rank(P_trace) = 1`, `rank(P_shear) = 5`.
6. **(T6) Projector algebra.** `{P_lapse, P_shift, P_trace, P_shear}` is
   exact, mutually orthogonal, idempotent, and complete (sums to `I_10`).
7. **(T7) Equivariance.** `[P_block, G_a] = 0` for each
   `P_block in {P_lapse, P_shift, P_trace, P_shear}` and each
   `a in {x, y, z}`.
8. **(T8) Coordinate landing.** In basis `B`, `P_shift` projects exactly
   onto the shift coordinates `(h_{tx}, h_{ty}, h_{tz})` and `P_shear`
   projects exactly onto the traceless-symmetric spatial coordinates
   `(q_1, q_2, h_{xy}, h_{xz}, h_{yz})`.

**Interpretation.** With the real anti-Hermitian convention used here, the
eigenvalues `-2` and `-6` are `-j(j+1)` for `j = 1` and `j = 2`. So the
complement decomposes representation-theoretically as the `j = 1`
shift-vector block plus the `j = 2` traceless spatial-shear block, and the
`Pi_A1` block decomposes into the two trivial-irrep summands lapse and
spatial trace.

## Scope and audit boundary

This is a representation-level block-localization theorem on
`V = Sym^2(R^4)` with the spatial-block `SO(3)` action `rho(R) h = R^T h R`,
`R = diag(1, R_3)`. The note proves the canonical four-block decomposition
`V = range(P_lapse) (+) range(P_shift) (+) range(P_trace) (+) range(P_shear)`
with explicit ranks, exact projector algebra, and exact `so(3)`-equivariance.

It does **not** prove:

- a choice of preferred frame inside the degenerate `j = 1` (shift) block or
  the `j = 2` (shear) block — these are `SO(3)`-irreducible representation
  spaces, so no canonical frame exists internally without an external
  selector;
- a full complement-frame bundle on the spatial section of `PL S^3 x R`;
- a distinguished connection on the spatial section;
- the identification of the block-localized universal Hessian with the
  Einstein/Regge operator blockwise; that requires a separate dynamics step
  named in
  [`UNIVERSAL_GR_CONSTRAINT_ACTION_STATIONARITY_NOTE.md`](UNIVERSAL_GR_CONSTRAINT_ACTION_STATIONARITY_NOTE.md)
  (cited for context, not load-bearing here).

## Bounded admissions

Every step in the proof-walk below relies only on the elementary
linear-algebra facts collected here. These are bounded textbook inputs, not
new repo axioms.

- **(BA-1) Real linear algebra on `Sym^2(R^4)`.** Frobenius inner product
  `<a, b> = sum_{i,j} a_{ij} b_{ij}`, additivity, and standard matrix
  arithmetic over `R`.
- **(BA-2) Orthogonality of `SO(3)`.** For `R_3 in SO(3)`,
  `R_3^T R_3 = R_3 R_3^T = I_3` and `det(R_3) = 1`. Hence
  `R = diag(1, R_3)` satisfies `R^T R = I_4` and `det(R) = 1`.
- **(BA-3) `so(3)` Lie algebra structure constants.** The three real
  antisymmetric `3 x 3` generators `(A_x, A_y, A_z)` defined by
  `(A_a)_{ij} = -epsilon_{aij}` (matching the runner's
  `so3_generator`) satisfy `[A_a, A_b] = epsilon_{abc} A_c` (up to
  orientation sign convention; the runner's `closes_so3` accepts both
  signs to be orientation-agnostic).
- **(BA-4) Exact arithmetic in
  `K := Q[sqrt 2, sqrt 3, sqrt 6]`.** All entries appearing in
  `B`, `Pi_A1`, the lifted generators, the Casimir, and its spectral
  projectors lie in `K`. Equality `sp.simplify(expr) == 0` over `K` is
  decidable in SymPy; the runner uses this decision procedure for every
  check.
- **(BA-5) Spectral theorem in finite dimensions.** A self-adjoint
  (symmetric in real basis) linear operator on a finite-dimensional inner
  product space has a unique decomposition into orthogonal projectors onto
  its eigenspaces. Specialization: a real diagonal matrix has spectral
  projectors equal to the indicator diagonals on its eigenvalues.

(BA-1) through (BA-5) are the only bounded admissions. No physical input is
load-bearing in the present theorem.

## Representation fixed in the packet

Coordinate order is `(t, x, y, z)`. The orthonormal polarization frame `B`
on `V = Sym^2(R^4)` (Frobenius inner product) is:

1. `e_0 = h_tt`                          (lapse)
2. `e_1, e_2, e_3 = h_tx, h_ty, h_tz`   (shift)
3. `e_4 = (h_xx + h_yy + h_zz) / sqrt 3` (spatial trace)
4. `e_5 = (h_xx - h_yy) / sqrt 2`        (shear `q_1`)
5. `e_6 = (h_xx + h_yy - 2 h_zz) / sqrt 6` (shear `q_2`)
6. `e_7, e_8, e_9 = h_xy, h_xz, h_yz`   (shear off-diagonal)

with the off-diagonal symmetric tensors normalized as
`(E_{ab} + E_{ba}) / sqrt 2`. Spatial rotations act by `rho(R) h := R^T h R`
with `R = diag(1, R_3)`, `R_3 in SO(3)`. The infinitesimal generators on
`V` are

```
(G_a)_{ij} := <e_i, A_a^T e_j + e_j A_a>,         a in {x, y, z},
```

where `A_a` is the embedded skew `4 x 4` generator
`A_a := diag(0, 0, 0, 0) +` (the canonical `3 x 3` axis rotation `A_a^{3D}`
embedded in indices `(1, 2, 3)`), per the runner constructor
`so3_generator` and `lifted_generator`.

## Proof-walk

Each step is a class-(A) algebraic identity reducible to (BA-1)–(BA-5). The
runner executes the corresponding check at exact precision in
`K = Q[sqrt 2, sqrt 3, sqrt 6]`. Step numbers are aligned to the
theorem-statement parts (T1)–(T8) above and to the eight `record(...)` calls
in
[`scripts/frontier_universal_gr_casimir_block_localization.py`](../scripts/frontier_universal_gr_casimir_block_localization.py).

| Step | Claim (T#) | Reduction | Runner check |
|---|---|---|---|
| 1 | (T1) `Gram(B) = I_10` | (BA-1): direct Frobenius pairing of each `(e_i, e_j)` reduces to a `K`-rational sum; off-diagonal pairings vanish by mutual support / sign cancellation; diagonal pairings normalize by construction. | `basis_orthonormal == True` |
| 2 | (T2) `[G_a, G_b] = epsilon_{abc} G_c` | (BA-3) on the embedded `R^3` factor; lifted to `V` by linearity of `rho` and the Leibniz identity `(rho_*[A, B])(h) = rho_*(A)(rho_*(B)(h)) - rho_*(B)(rho_*(A)(h))` for the conjugation action `R . h = R^T h R`. The runner checks each pair entrywise. | `so3_closure_exact == True` |
| 3 | (T3) `Pi_A1 G_a Pi_perp = Pi_perp G_a Pi_A1 = 0` | (BA-2): the spatial trace `tr(h_{ij})` is `SO(3)`-invariant under `R_3 in SO(3)` because `tr(R_3^T h_{ij} R_3) = tr(h_{ij})` (cyclic trace plus `R_3 R_3^T = I_3`). The lapse `h_tt` is trivially `SO(3)`-invariant because `R` fixes the `t` index by `R = diag(1, R_3)`. So `rho(R)` carries `range(Pi_A1) = span(e_0, e_4)` into itself; infinitesimally, `G_a` carries `range(Pi_A1)` into itself, so the off-diagonal blocks of `G_a` between `range(Pi_A1)` and `range(Pi_perp)` are zero. | `A1_complement_mixing_zero == True` |
| 4 | (T4) `diag(C) = (-2, -2, -2, -6, -6, -6, -6, -6)`, off-diagonal zero | Direct sum `G_x^2 + G_y^2 + G_z^2` is computed entrywise over `K` (BA-4) on the 8D complement in basis `B`. The entries of `G_a` in basis `B` are themselves `K`-rational by (BA-1), (BA-2), and the construction of `B`; the matrix-product entries are then `K`-rational. Diagonalness of `C` in this specific basis is a property of the basis choice `B` (the shift sub-basis `(h_{tx}, h_{ty}, h_{tz})` and the shear sub-basis `(q_1, q_2, h_{xy}, h_{xz}, h_{yz})` are pre-tuned to the irreducible-representation decomposition `j = 1 (+) j = 2`); the runner verifies that this particular tuning gives diagonal `C` exactly. The diagonal values `-2` and `-6` then correspond to `-j(j+1)` for `j = 1` and `j = 2` in the real anti-Hermitian convention; multiplicities `3 = (2j + 1)|_{j=1}` and `5 = (2j + 1)|_{j=2}` follow from (BA-5) applied to the diagonal matrix. | `Casimir diagonal on complement = [-2, -2, -2, -6, -6, -6, -6, -6]`; `Casimir off-diagonal zero on complement = True` |
| 5 | (T5) ranks `(1, 3, 1, 5)` | (BA-5) applied to the diagonal Casimir: the indicator diagonal on `C = -2` has rank 3 (three matching entries) and the indicator diagonal on `C = -6` has rank 5 (five matching entries). The trivial-irrep refinement on `range(Pi_A1)` splits into `range(P_lapse)` (rank 1, `e_0`) and `range(P_trace)` (rank 1, `e_4`). | `ranks = {lapse: 1, shift: 3, trace: 1, shear: 5}` |
| 6 | (T6) projector algebra exact | The four projectors are diagonal in basis `B` with disjoint support, so orthogonality `P_i P_j = 0 (i != j)` and idempotence `P_i^2 = P_i` are entrywise identities; completeness follows from the union of their supports covering `{0, 1, ..., 9}`. (BA-1), (BA-5). | `projector complete = True`; `projector orthogonal = True`; `projector idempotent = True` |
| 7 | (T7) `[P_block, G_a] = 0` | Each spectral projector commutes with the operator whose eigenspace it projects onto (BA-5). For `C`-eigenprojectors `P_shift` and `P_shear`, this gives `[P_shift, C] = [P_shear, C] = 0`. The stronger statement `[P_shift, G_a] = [P_shear, G_a] = 0` follows because each `G_a` preserves each `C`-eigenspace (consequence of (T3) plus the fact that `[G_a, C] = 0` on the complement by Casimir-element centrality in `U(so(3))`). For `P_lapse` and `P_trace`, equivariance is the trivial-irrep statement: lapse and spatial-trace channels carry the trivial representation and are pointwise fixed by `rho(R)`; infinitesimally, `G_a` acts as zero on `range(P_lapse)` and on `range(P_trace)`. | `commutes: lapse=True, trace=True, shift=True, shear=True` |
| 8 | (T8) coordinate-landing diagonals | By the definition of the projectors as spectral projectors of the diagonal Casimir on the complement in basis `B`, `P_shift = diag(0, 1, 1, 1, 0, 0, 0, 0)` on the complement (selecting `(h_{tx}, h_{ty}, h_{tz})`) and `P_shear = diag(0, 0, 0, 1, 1, 1, 1, 1)` on the complement (selecting `(q_1, q_2, h_{xy}, h_{xz}, h_{yz})`). | `diag P_shift on complement = [1, 1, 1, 0, 0, 0, 0, 0]`; `diag P_shear on complement = [0, 0, 0, 1, 1, 1, 1, 1]` |

Every load-bearing input above is in (BA-1)–(BA-5). Chain closes from the
admitted bounded textbook linear-algebra package alone. No retained-grade
upstream theorem is invoked as a premise for the block-localization claim
on the abstract pair `(V, rho)`; the cluster's upstream notes (listed in
[Provenance and non-dependencies](#provenance-and-non-dependencies)) supply
context that motivates the choice of representation and the physical block
labels, but are not load-bearing for the algebraic theorem itself.

## Cached runner output

The runner is fully reproducible and self-contained (imports `sympy` only;
constructs every check from scratch). Cached output is at
[`logs/runner-cache/frontier_universal_gr_casimir_block_localization.txt`](../logs/runner-cache/frontier_universal_gr_casimir_block_localization.txt)
with `runner_sha256 = c5a083df65acce488cb6bff71b524452838db1a058578f02fdbf89fd8dbb0536`
and `exit_code = 0`. Key cached values:

```text
basis_orthonormal = True
so3_closure_exact = True
A1_complement_mixing_zero = True
Casimir diagonal on complement = [-2, -2, -2, -6, -6, -6, -6, -6]
Casimir off-diagonal zero on complement = True
ranks = {'lapse': 1, 'shift': 3, 'trace': 1, 'shear': 5}
projector complete = True
projector orthogonal = True
projector idempotent = True
commutes: lapse=True, trace=True, shift=True, shear=True
diag P_shift on complement = [1, 1, 1, 0, 0, 0, 0, 0]
diag P_shear on complement = [0, 0, 0, 1, 1, 1, 1, 1]

[EXACT] PASS: the displayed 10D polarization basis is exactly orthonormal
[EXACT] PASS: the lifted spatial generators close the SO(3) Lie algebra exactly
[EXACT] PASS: Pi_A1 is invariant and its complement is an invariant subrepresentation
[EXACT] PASS: the complement Casimir has exactly the j=1 and j=2 split
[EXACT] PASS: the spectral projectors define a canonical shift/shear split on the complement
[EXACT] PASS: the four block projectors are exact, orthogonal, and complete
[EXACT] PASS: the block projectors commute with the universal SO(3) generators
[EXACT] PASS: in the current canonical basis the Casimir projectors land on the expected coordinates

PASS=8 FAIL=0 TOTAL=8
```

## Verification

Re-run from a clean working tree with:

```bash
PYTHONPATH=scripts python3 scripts/frontier_universal_gr_casimir_block_localization.py
```

Expected (matches cache):

```text
PASS=8 FAIL=0 TOTAL=8
```

All checks are class-(A) exact algebraic identities over
`K = Q[sqrt 2, sqrt 3, sqrt 6]` decided by `sp.simplify(...) == 0`. The
runner has no random sampling, no numeric tolerance, and no fitted
constants.

## Provenance and non-dependencies

The following cluster siblings are cited for **context**, not as
load-bearing premises of the block-localization theorem above:

- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  records the exact scalar observable generator `W[J]` used to motivate the
  Hessian whose representation-theoretic block structure is the present
  theorem's subject.
- [`S3_ANOMALY_SPACETIME_LIFT_NOTE.md`](S3_ANOMALY_SPACETIME_LIFT_NOTE.md)
  records the kinematic background `PL S^3 x R` whose tangent
  representation is `Sym^2(R^4)` with the spatial-block `SO(3)` action used
  here.
- [`UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md`](UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md)
  records the tensor-valued variational candidate
  `S_GR^cand[h] := (1/2) D^2 W[g_*](h, h)` whose linear operator the
  present projectors block-diagonalize.
- [`UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md`](UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md)
  records the symmetric `3 + 1` quotient kernel of that candidate.
- [`UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md`](UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md)
  records the rank-2 `Pi_A1` projector onto lapse + spatial trace as the
  exact invariant section of the localization orbit. The present note
  proves the orthogonal-complement `SO(3)`-decomposition of `Pi_perp` into
  the `j = 1` shift block and the `j = 2` shear block, extending the A1
  picture to a complete four-block decomposition.

None of these sibling notes is invoked as a load-bearing premise for the
present block-localization theorem on the abstract pair `(V, rho)`. The
theorem closes from (BA-1)–(BA-5) plus the explicit construction of
`(B, Pi_A1, G_a, C, P_block)` in the runner. The cluster references are
**informational** pointers that anchor the physical interpretation of the
algebraic blocks as lapse / shift / trace / shear in the universal GR
route. The citation graph builder follows markdown-link arrows; the
dependency edges above are recorded so the audit graph keeps the
information links visible, without promoting any upstream row by this
note.

## Forbidden-imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions are load-bearing on retention.
- No same-surface family arguments.
- No new axioms introduced — the theorem is on abstract `Sym^2(R^4)` with
  a generic spatial-block `SO(3)` action. The framework `MINIMAL_AXIOMS_2026-05-03`
  baseline is named in plain text only as the broader cluster context and
  is not load-bearing for the block-localization claim.
- No new repo vocabulary — block labels (lapse, shift, trace, shear) are
  standard `3 + 1` ADM terminology and the runner's record strings use
  only those plus standard linear-algebra terms (Casimir, projector,
  rank, commutator, idempotent, orthogonal, complete).
- Runner imports: `sympy` only. No `numpy`, no I/O, no external data.

## What this theorem does NOT close

- No preferred basis is chosen inside the degenerate `j = 1` shift block
  or the `j = 2` shear block. These are irreducible `SO(3)`
  representations; no canonical internal frame exists without an external
  selector.
- No full complement-frame bundle or distinguished connection on the
  spatial section of `PL S^3 x R` is claimed.
- No identification of the block-localized universal Hessian with the
  Einstein/Regge operator is claimed. That requires a separate dynamics
  theorem inside the shift and shear channels.
- No promotion of any upstream cluster sibling (observable principle,
  spacetime lift, variational candidate, quotient uniqueness, A1
  invariant section) is implied. Each remains at its current audit row.
