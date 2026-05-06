# Plaquette V=1 Picard-Fuchs ODE: Minimality Certificate Note

**Date:** 2026-05-06
**Claim type:** bounded_theorem
**Status:** bounded support theorem; audit status is set only by the independent audit lane
**Primary runner:** `scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py`
**Companion:** [`PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md) (the candidate ODE)

## Scope

This note records a bounded, exact-arithmetic certificate packet for the
V=1 single-plaquette Picard-Fuchs operator in
[`PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md).
It combines a finite Bessel-determinant Taylor/rank runner with standard
external D-module and creative-telescoping inputs. It does not update the
companion row's audit status or effective status; the independent audit lane
must decide whether this packet closes that parent row.

## Setup

Let
```text
J(β) = ∫_{SU(3)} exp(β · Re Tr U / 3) dU,
```
the V=1 single-plaquette SU(3) Wilson character integral, normalized so
that `J(0) = 1`. The PR #541 candidate operator is
```text
L = 6 β² ∂³  +  β(60 − β) ∂²  +  (−4β² − 2β + 120) ∂  −  β(β + 10) · 𝟙,
```
where `∂ = d/dβ`. The PR #541 claim is `L · J(β) = 0` as an analytic
identity.

The Bessel-determinant identity (Bars 1980 [3]) gives the absolutely
convergent sum representation
```text
J(β) = Σ_{k ∈ ℤ} det[I_{i−j+k}(β/3)]_{i,j ∈ {0,1,2}}                 (★)
```
where `I_n(z)` is the modified Bessel function of the first kind. This
is a closed-form identity, not an approximation.

## Bounded Certificate Claim

The runner certifies, in exact rational arithmetic at Taylor depth 40:

- `L · J` vanishes through the safe truncated range `[β^0, …, β^36]`;
- no lower-order ansatz with order `≤ 2` and coefficient degree `≤ 12`
  survives the matching system;
- at `(order=3, degree=2)`, the kernel is one-dimensional and matches `L`
  up to scalar;
- the checked higher-degree windows `(order=3, degree=2..6)` are consistent
  with polynomial multiples of `L`.

Conditioned on the cited external holonomicity/rank and
creative-telescoping machinery being applicable to this exact integral and
candidate, these certificates support the minimal-annihilator interpretation
of `L` for the V=1 integral. The runner alone is a bounded certificate packet,
not a repo-wide axiom or a thermodynamic-limit bridge.

## Proof outline

The support chain is:

  **Step 1 (existence).** Bernstein's theorem on holonomic D-modules
  guarantees that `J(β)` is annihilated by a non-zero polynomial-coefficient
  ODE.

  **Step 2 (algorithm).** Wilf-Zeilberger creative telescoping plus
  the Saito-Sturmfels-Takayama Gröbner-deformation algorithm turn the
  problem of finding `Ann(J)` into a finite linear-algebra problem at
  bounded `(order, coefficient-degree)`.

  **Step 3 (verification).** The candidate operator `L` of order 3 and
  coefficient degree 2 is checked against the Bessel-determinant Taylor
  expansion to depth 40 (vs. PR #541 depth 21) (deep certificate `[A]`,
  runner output) and against the induced 4-term recurrence on the `a_n`
  series coefficients in the checked window (certificate `[D]`).

  **Step 4 (lower-order exclusion).** A direct computational rank
  certificate `[B]` (runner output) shows that for every
  `(r, d) ∈ {1, 2} × {0, 1, …, 12}`, the linear system "find a
  non-trivial polynomial-coefficient operator of order ≤ r and
  coefficient-degree ≤ d that annihilates `J(β)`" has zero kernel —
  so no order ≤ 2 ODE annihilates `J(β)`.

  **Step 5 (uniqueness at minimal order).** A second rank certificate
  `[C]` shows the kernel at `(r=3, d=2)` is exactly one-dimensional,
  with the kernel direction equal (up to a non-zero scalar) to the
  PR #541 published operator `L`.

  **Step 6 (higher-degree consistency).** Certificate `[E]` checks
  that the kernel at `(r=3, d ≥ 3)` grows exactly as `d − 1`, the
  expected dimension contributed by polynomial multiples of `L`. No
  genuinely new generator appears at higher coefficient degree.

These six steps define the bounded certificate surface. All-order promotion,
including whether this discharges the companion row's missing bridge, remains
audit-owned.

## Detailed proof

### Step 1 (existence). Bernstein 1972.

**Theorem (Bernstein 1972 [1]; Sabbah; Hotta-Takeuchi).** If `f, g` are
polynomial functions on a smooth affine algebraic variety `X` and `μ`
is an algebraic top form, then for the parameter integral
```text
F(s) = ∫_X g(x) · exp(s · f(x)) μ(dx)
```
defined on the appropriate region of `s`, `F(s)` is a holonomic
function of `s` — i.e., it is annihilated by a non-zero linear
polynomial-coefficient differential operator in `s`.

**Application.** `SU(3)` is a smooth compact algebraic group of real
dimension 8 with Haar measure. The function `Re Tr U / 3` extends to a
polynomial in matrix coordinates of `SU(3)`. By Aomoto-Gelfand
specialization of Bernstein's theorem, `J(β)` is holonomic in `β`. ∎

The rank bound from Bernstein's theorem can be made effective; for
SU(N) Wilson character integrals, the standard reduction to the
maximal-torus Weyl integral gives the bound `rank(J) ≤ N` (this is the
Aomoto-Gelfand rank for the Weyl-integral Vandermonde measure). For
N = 3 we have `rank(J) ≤ 3`, immediately consistent with the order-3
ODE we exhibit.

### Step 2 (algorithm). Wilf-Zeilberger 1990; Saito-Sturmfels-Takayama 2000.

**Theorem (Wilf-Zeilberger 1990 [2]).** For a definite-summation
operand `T(n, β)` that is holonomic in both `n` and `β`, the
creative-telescoping algorithm produces a non-zero polynomial-coefficient
operator `L(β, ∂_β)` such that `L · Σ_n T(n, β) = 0`, in finite time.
Moreover, the smallest such operator (in the term order specified by
Saito-Sturmfels-Takayama [4]) is the minimal annihilator.

**Application.** In the Bessel-determinant identity (★), each summand
`D_k(β) = det[I_{i−j+k}(β/3)]_{i,j ∈ {0,1,2}}` is a polynomial in 9
modified-Bessel functions. The Bessel ODE `z² I_n''(z) + z I_n'(z) − (z² + n²) I_n(z) = 0`
makes each `I_n(β/3)` holonomic in β, and the determinant is therefore
a polynomial in 9 holonomic functions, hence holonomic by D-module
closure under finite products. The infinite sum over `k` converges
exponentially (since `I_n(β/3) ~ (β/6)^|n| / |n|!` for large `|n|` at
fixed `β`) and preserves holonomicity by the Borel-Moore / D-module
direct image construction.

The creative-telescoping algorithm therefore produces an annihilating
operator for `J(β)` algorithmically. The PR #541 derivation IS this
WZ output. ∎

### Step 3 (verification). Direct Taylor + recurrence.

The ODE `L · J = 0` is equivalent to a 4-term P-recurrence on the
Taylor coefficients `a_n = [β^n] J(β)`:
```text
6(N+1)(N+4)(N+5) a_{N+1} = N(N+1) a_N + 2(2N+3) a_{N−1} + a_{N−2}     (♢)
```
(derived from `L · J = 0` by extracting the coefficient of `β^N`;
see PR #541 runner for the explicit derivation).

**Certificate [A] (deep Taylor annihilation).** Using the Bessel-determinant
identity (★) we compute the Taylor coefficients `a_0, a_1, …, a_{40}`
exactly as rational numbers. Substituting into `L · J` and truncating
to the safe-degree range `[β^0, …, β^{36}]` gives **identically zero**
in `ℚ[β]`. This is the runner certificate `[A]`.

**Certificate [D] (recurrence consistency).** With the same exact `a_n`
from (★), the recurrence (♢) holds **exactly** for every `N` in
`[2, 39]`. This verifies the stated finite window. Extending that window
to the all-order identity requires the external holonomic/creative-telescoping
inputs listed above; the runner does not independently prove that all-order
extension. ∎

### Step 4 (lower-order exclusion). Rank certificate [B].

For each `(r, d) ∈ {1, 2} × {0, 1, …, 12}`, consider the affine
linear system in unknowns `{p_{k, m} : 0 ≤ k ≤ r, 0 ≤ m ≤ d}`:
```text
[β^N] of  Σ_{k=0..r} Σ_{m=0..d} p_{k,m} · β^m · J^{(k)}(β)  =  0,    (♦)
```
for `N = 0, 1, …, N_*`. This is a homogeneous linear system over `ℚ`
in `(r+1)(d+1)` unknowns. With `N_* > (r+1)(d+1)` and the matrix
of coefficients having full column rank `(r+1)(d+1)`, the system has
only the trivial solution.

**Certificate.** Runner output for ORDER=40 confirms that the rank of
the matching matrix at every tested `(r, d) ∈ {1, 2} × {0, 1, …, 12}`
equals the number of unknowns. Hence no non-trivial annihilator of
order ≤ 2 with polynomial coefficients of degree ≤ 12 exists.

**Scope beyond the checked degree.** The runner directly excludes the
listed finite degree window. Extension to all coefficient degrees is
conditional on the cited Bernstein/Aomoto-Gelfand rank input and on the
all-order identification of `L` as an annihilator. ∎

### Step 5 (uniqueness at minimal order). Rank certificate [C].

At `(r, d) = (3, 2)` the linear system (♦) has 12 unknowns. Runner
output confirms the rank of the matching matrix is 11, so the kernel
is exactly 1-dimensional. The unique kernel direction (extracted via
`sympy.Matrix.nullspace()`) is rationally proportional to the PR #541
operator `L`, with proportionality scalar 6 (after primitive-integer
normalization). This proves uniqueness of `L` among operators of order
≤ 3 and coefficient degree ≤ 2. ∎

### Step 6 (higher-degree consistency). Rank certificate [E].

For `(r, d) = (3, d')` with `d' ∈ {2, 3, …, 6}`, the runner verifies
that the kernel dimension is exactly `d' − 1`. This is the dimension
of the subspace `{p(β) · L : deg(p) ≤ d' − 2}` of polynomial multiples
of `L` (which trivially still annihilates `J`). No genuinely new
operator generator appears at higher `d'`. ∎

## What this packet supports vs. what it does not close

**Runner-backed:**

- `L · J(β) = 0` through the safe Taylor window `[β^0, …, β^36]`.
- Among all polynomial-coefficient differential operators of order
  ≤ 3 and coefficient degree ≤ 2, `L` is unique up to scalar.
- Among all polynomial-coefficient differential operators of order
  ≤ 2 and coefficient degree ≤ 12, no checked-window annihilator of `J`
  exists.
- Higher-degree checked windows through degree 6 are consistent with
  polynomial multiples of `L`.

**Bounded scope:**

- This is V=1 only. The thermodynamic-limit Wilson plaquette value
  `⟨P⟩(β=6, L→∞)` is NOT addressed by this note; it sits in
  `PLAQUETTE_4D_MC_FSS_RETAINED_THEOREM_NOTE_2026-05-05.md`.
- The Bernstein rank bound `rank(J) ≤ 3` is cited from the standard
  Aomoto-Gelfand theory; the proof of that bound is mathematical
  literature (not framework-internal).
- Numerical certificates `[B]` and `[E]` test bounded coefficient
  degrees `d ≤ 12` and `d ≤ 6`. Coupling these with the abstract
  Bernstein/WZ machinery is an import-supported theorem path, not a new
  repo-wide axiom.

## Cited authorities

[1] **Bernstein, J. N.** "The analytic continuation of generalized
    functions with respect to a parameter." *Functional Analysis and
    its Applications*, 1972, 6(4): 273–285. Established holonomic
    D-modules and the existence of Bernstein-Sato polynomials, hence
    the existence of finite-order ODEs annihilating
    parameter-dependent algebraic integrals.

[2] **Wilf, H. S. and Zeilberger, D.** "Rational functions certify
    combinatorial identities." *Journal of the American Mathematical
    Society*, 1990, 3(1): 147–158. Established creative telescoping
    as an algorithmic procedure for finding holonomic recurrences and
    ODEs satisfied by definite sums.

[3] **Bars, I.** "U(N) integral for the generating functional in
    lattice gauge theory." *Journal of Mathematical Physics*, 1980,
    21(11): 2678–2681. Established the determinant-of-Bessel-functions
    representation for `∫_{U(N)} exp(t · Re Tr U) dU` (and analogous
    SU(N)) used in (★).

[4] **Saito, M., Sturmfels, B., and Takayama, N.** *Gröbner
    Deformations of Hypergeometric Differential Equations*, Algorithms
    and Computation in Mathematics, vol. 6. Springer, 2000. Provides
    the algorithmic Gröbner-basis-of-D-modules infrastructure used in
    Step 5 (uniqueness).

[5] **Sabbah, C.** *Hodge Theory, Singularities and D-modules*, lecture
    notes, 2007 (and references therein for the rank-bound theory of
    Aomoto-Gelfand integrals).

[6] **Hotta, R., Takeuchi, K., and Tanisaki, T.** *D-Modules,
    Perverse Sheaves, and Representation Theory*, Birkhäuser, 2008.
    Standard reference for D-module direct image, holonomic-rank
    arithmetic.

## Parent-row use

This packet is intended as review-ready support for re-auditing the companion
Picard-Fuchs ODE row. It can be used by that independent audit only as follows:

1. **Holonomic existence.** Bernstein/Aomoto-Gelfand theory supplies the
   external finite-rank input.

2. **Algorithmic discovery.** Wilf-Zeilberger/Saito-Sturmfels-Takayama
   machinery is the external route that identifies the candidate operator.

3. **Exact certificates.** This runner supplies the finite Taylor/rank
   checks listed above, all in exact arithmetic.

The review loop does not prewrite the audit verdict. If the independent
auditor accepts the external imports and the finite certificates as closing
the missing bridge, the pipeline may update the companion row from that audit
result and dependency closure.

## Audit registration

```yaml
claim_id: plaquette_v1_picard_fuchs_ode_minimality_proof_note_2026-05-06
note_path: docs/PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md
runner_path: scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py
claim_type: bounded_theorem
claim_scope: >
  Bounded V=1 single-plaquette SU(3) Wilson-integral Picard-Fuchs
  exact-arithmetic certificate packet for the order-3 operator from
  PR #541, conditioned on the listed external D-module/creative-telescoping
  imports and excluding any thermodynamic-limit, multi-plaquette, or bridge
  promotion.
intrinsic_status: bounded_theorem
companion_for_reaudit: plaquette_v1_picard_fuchs_ode_note_2026-05-05
deps:
  - PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md (the candidate ODE)
  - Bernstein 1972 (D-module holonomicity)
  - Wilf-Zeilberger 1990 (creative telescoping)
  - Bars 1980 (Bessel-determinant identity)
  - Saito-Sturmfels-Takayama 2000 (Gröbner-deformation D-modules)
audit_authority: independent audit lane
```

## Command

```bash
python3 scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py
```

Expected summary:
```text
SUMMARY: CERTIFICATE PASS=5 FAIL=0
```

with output `outputs/su3_v1_picard_fuchs_minimality_2026_05_06.json`
recording per-certificate detail.
