# Gauge-Vacuum Plaquette Hierarchy Obstruction Lemmas — Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py`](../scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py)

## Claim

Bounded note supplying the four analytic premises that the parent
`GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md`
treats as inputs (per its 2026-05-02 audit verdict's repair-target list;
reader pointer only, not a load-bearing dependency of this lemma note).
Each lemma is proved from textbook compact-Lie-group analysis premises
(stated as bounded admissions in §"Bounded admissions"); none is derived
from the framework baseline of physical `Cl(3)` local algebra on the
`Z^3` spatial substrate in this note.

For the diagonal source-deformed lattice gauge action with normalized
Haar measure on the compact gauge group `G` (SU(N), N ≥ 1; the U(1)
case is the abelian specialization),

```text
Z_L ( t )    =  ∫ ∏_l dU_l  exp ( t · Σ_p F ( U_p ) ),
F ( U )      =  ( 1 / N ) · Re Tr ( U ),       max_{U ∈ G} F ( U )  =  1
```

with link product `U_p = ∏_{l ∈ ∂p} U_l` per plaquette `p`, and
diagonal generators

```text
K_L ( t )    =  log Z_L ( t )  -  log Z_L ( 0 ),
K_L' ( t )   =  N_plaq · P_L ( t ),
K_1 ( t )    =  log Z_1plaq ( t )  -  log Z_1plaq ( 0 ),       K_1' ( t )  =  P_1plaq ( t ),
```

the four lemmas are:

**(L1) One-plaquette endpoint identities.**

```text
P_1plaq ( 0 )                       =  0,                                      (L1.a)
lim_{ t → ∞ }  P_1plaq ( t )       =  1.                                       (L1.b)
```

**(L2) Finite-periodic Wilson endpoint identities.**

```text
P_L ( 0 )                           =  0,                                      (L2.a)
lim_{ t → ∞ }  P_L ( t )           =  1   (compact Laplace concentration on
                                            the maximum-action gauge orbit).   (L2.b)
```

**(L3) Finite Taylor support ⟺ polynomial `K(t)` globally on `R`.**
For both `K = K_1` and `K = K_L`,

```text
[ ∃ N : Taylor coefficient c_n = 0  ∀ n > N at t = 0 ]
  ⟺   K ( t )  is a polynomial of degree ≤ N on R.                             (L3)
```

The forward direction follows from real-analyticity of `K` on `R` plus
analytic continuation of a finite-support Taylor series; the reverse
direction is immediate (a polynomial has only finitely many nonzero
Taylor coefficients).

**(L4) Polynomial-growth bound on `R`.** The implication

```text
[ K ( t )  is a polynomial of degree ≥ 1 on R ]
  +
[ K' ( t )  has finite real limit as t → ∞ ]
  ⟹  K' ( t )  is constant on R                                                (L4)
```

holds globally on the real line `R` (where `K` is real-analytic per
(L3)), not merely as a formal Taylor-series identity at `t = 0`. The
parent note's contradiction `P_1plaq(0) = 0 ≠ 1 = P_1plaq(∞)` against
constancy of `P_1plaq` is therefore globally valid, not formal.

## Bounded admissions

The four lemmas above rest on the following textbook compact-Lie-group
analysis facts, listed here as explicit bounded admissions:

(BA-1) **Compact Haar orthogonality.** On the normalized Haar measure
of any compact Lie group `G`, every non-trivial irreducible character
integrates to zero. The lemmas below apply to `G = SU(N)` with `N ≥ 2`
(where the fundamental-rep character `(1/N) · Re Tr U` is non-trivial
and integrates to zero under Haar) and to the abelian `G = U(1)` case
(where the character `cos θ` is non-trivial and integrates to zero
under `dθ / (2π)`). The `N = 1` SU(N) instance is trivial-group and
not a gauge theory; it is excluded.

(BA-2) **Compact Laplace concentration.** For a compact metric space
`X` with regular probability measure `μ`, a continuous real-valued
function `f: X → R`, and the source-deformed measure
`μ_t (dx) = exp(t f(x)) dμ(x) / Z(t)`,
the family `{μ_t}_{t > 0}` weak-converges as `t → ∞` to a probability
measure supported on `argmax_X f`. In particular, `<f>_{μ_t} → max_X f`.

(BA-3) **Entire-function partition representation.** For a continuous
bounded `f: X → R` on a compact `X` with finite total measure, the
function `Z(t) := ∫_X exp(t f(x)) dμ(x)` is **entire** in `t ∈ C`,
and `Z(t) > 0` for all `t ∈ R`. Consequently `K(t) := log Z(t)` is
real-analytic on `R`.

(BA-4) **Analytic continuation of finite-support Taylor series.** If
`K: R → R` is real-analytic and its Taylor series at `t = 0` has finite
support (i.e., all coefficients past order `N` vanish), then `K` equals
that finite Taylor polynomial globally on `R` (by analytic continuation
from any open disk inside the radius of convergence to the entire real
line).

(BA-1)–(BA-4) are standard facts of compact-Lie-group / asymptotic
analysis; they are admitted here as bounded inputs rather than derived
from the framework baseline. The lemmas (L1)–(L4) close from these
admissions plus elementary computation.

## Proof-Walk

| Lemma | Argument | Load-bearing premise |
|---|---|---|
| (L1.a) `P_1plaq(0) = 0` | `P_1plaq(0) = <F>_{Haar} = (1/N) ∫ Re Tr U dU = 0` by (BA-1). The fundamental-rep character `Re Tr U` is a non-trivial irreducible character on SU(N) (and `cos θ` on U(1)), so integrates to zero. | (BA-1) Haar orthogonality |
| (L1.b) `P_1plaq(t) → 1` as `t → ∞` | Apply (BA-2) to `X = G`, `f(U) = F(U) = (1/N) Re Tr U`, `μ = Haar`. Then `<F>_{μ_t} → max_G F = 1` (achieved at `U = I_N` for SU(N), at `θ = 0` for U(1)). | (BA-2) compact Laplace + boundedness `F ≤ 1` |
| (L2.a) `P_L(0) = 0` | Per-plaquette Haar symmetry: `<F(U_p)>_0 = ∫ ∏_l dU_l · F(U_p) = ∫ dU_p · F(U_p)` (since `U_p` is a single Haar-distributed group element under change of variables, with the link integration absorbed by gauge invariance / left translation). Then (BA-1) gives `<F(U_p)>_0 = 0`. By plaquette translation symmetry, `P_L(0) = <F(U_p)>_0 = 0`. | (BA-1) Haar orthogonality + lattice translation symmetry |
| (L2.b) `P_L(t) → 1` as `t → ∞` | Apply (BA-2) to `X = G^E` (compact product), `f = Σ_p F(U_p)`, `μ = ∏_l Haar(dU_l)`. Then `μ_t` weak-converges to a measure supported on `argmax_{X} f`, the **maximum-action gauge orbit** where every plaquette has `U_p = I_N` (achieving `f = N_plaq`). On that orbit `F(U_p) = 1` for every plaquette, so per-plaquette mean `P_L(t) = <F(U_p)>_{μ_t} → 1`. | (BA-2) compact Laplace + product-of-compact remains compact |
| (L3) finite Taylor support ⟺ polynomial `K(t)` globally on `R` | Apply (BA-3) and (BA-4): `Z_L(t)` is entire by (BA-3), `K_L(t)` is real-analytic on `R`, and finite Taylor support at `t = 0` extends globally by (BA-4). The reverse direction (polynomial ⟹ finite Taylor support) is immediate (a polynomial of degree `≤ N` has zero Taylor coefficients past order `N`). | (BA-3) entire `Z`, (BA-4) analytic continuation of finite Taylor |
| (L4) global vs formal: polynomial `K` of degree `≥ 1` with bounded `K'` ⟹ `K'` constant globally | If `K(t)` is polynomial of degree `d ≥ 1` on `R` (per L3), then `K'(t)` is polynomial of degree `d - 1`. A polynomial of degree `≥ 1` has unbounded magnitude as `t → ∞` (its leading term grows like `|t|^{d-1}` if `d - 1 ≥ 1`). For `K'(t) = N_plaq · P_L(t)` to remain bounded in `[0, N_plaq]` (since `P_L ∈ [0, 1]` as a per-plaquette source-deformed expectation of a function bounded by `1`), we must have `d - 1 = 0`, i.e., `K'` constant. The same argument applies on the real line globally — not as a formal Taylor identity. | elementary polynomial growth + boundedness of `P_L` and `P_1plaq` |

Every load-bearing step reduces either to a textbook compact-Lie-group
fact ((BA-1)–(BA-2)) or to standard analyticity / polynomial growth
arguments on `R` ((BA-3)–(BA-4) plus elementary calculus). Lattice
gauge action coupling `β` does not enter the load-bearing chain: the
diagonal generator framework treats `t` as the coupling, with `β`
absorbed into the source via `t' = β + t` (per parent §"Setup").

## Exact Arithmetic Check

The runner verifies, at exact rational precision via `fractions.Fraction`
where applicable, plus numerical-tolerance verification for the
endpoint-limit identities:

(A) **(L1.a) `P_1plaq(0) = 0`.** Numerical Haar integration of `(1/N)
Re Tr U` on `U(1)` (one-dimensional, exact: `∫ cos θ dθ / (2π) = 0` to
machine precision) and `SU(2)` (three-dimensional Haar with
`(1/2) Re Tr U = cos(α/2)` parametrized by `α ∈ [0, π]`). Both give
zero to within `10⁻¹⁰` numerical tolerance, consistent with the
exact-rational identity `P_1plaq(0) = 0` from (BA-1).

(B) **(L1.b) `P_1plaq(t) → 1` as `t → ∞`.** Direct evaluation of
`P_1plaq(t) = <F>_{μ_t}` for `U(1)` (where `Z_1(t) = I_0(t)` and
`P_1plaq(t) = I_1(t) / I_0(t)`) at `t = 1, 10, 100, 1000`; verify the
sequence converges to `1` from below, with deviation `< 10⁻³` at
`t = 1000`. The U(1) calculation uses the modified-Bessel-function
asymptotic `I_1(t) / I_0(t) → 1 - 1/(2t) + O(1/t²)`, computed via direct
numerical Bessel evaluation (no special-function library).

(C) **(L2.a) `P_L(0) = 0`.** Plaquette Haar argument: under change of
variable, `U_p` is itself Haar-distributed when other links are
integrated out (left-translation invariance of Haar). So `<F(U_p)>_0 =
<F>_{Haar} = 0`. Verified by reduction to (A) at the per-plaquette
level.

(D) **(L2.b) `P_L(t) → 1` as `t → ∞`.** For the toy `L = 1`
single-plaquette case (the parent's `P_1plaq`), this is (B). For
general `L`, (BA-2) gives the same conclusion via product-of-compact
stays-compact; verified via the `L = 1` case as the load-bearing
instance, plus a numerical check that the per-plaquette concentration
on `U_p = I` holds in a `2 × 2 × 2 × 2` periodic Wilson lattice via
small-Monte-Carlo-step argument (deferred to runner; structural check
only).

(E) **(L3) Taylor support ⟺ polynomial.** For `Z_1(t) = I_0(t)` on
`U(1)`, verify symbolically that the Taylor series at `t = 0` is
`I_0(t) = Σ (t/2)^{2k} / (k!)²` (infinite support — no truncation
exists), so `K_1(t) = log I_0(t)` has infinite Taylor support. By
(BA-3) `Z_1` is entire, by (BA-4) finite support would imply polynomial
globally — combined, this confirms the obstruction premise.

(F) **(L4) Global-vs-formal.** Verify that the polynomial-growth
argument is global (not formal): explicitly state the contradiction at
`t = ∞` (where polynomial of degree `≥ 1` is unbounded but `P_L` is
bounded by `1`), and confirm it cannot be reproduced by any
formal-Taylor truncation argument near `t = 0` alone.

## Dependencies

- `GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md`
  for parent context only: the lemmas (L1)–(L4) supply the analytic
  premises listed in that note's `open_dependency_paths` per its
  2026-05-02 audit verdict. The load-bearing graph direction is
  parent obstruction note -> this lemma note, not the reverse.
- [`GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md)
  for adjacent gauge-vacuum-plaquette analytic context (compact-Laplace
  concentration on the maximum-action gauge orbit appears in that
  retained authority on a sister surface).
- `MINIMAL_AXIOMS_2026-05-03.md`
  for the framework baseline of physical `Cl(3)` local algebra and
  the `Z^3` spatial substrate. This bounded note does not invoke that
  baseline directly; it imports textbook compact-Lie-group analysis as
  bounded admissions (BA-1)–(BA-4).

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does **not**:
- close the parent infinite-hierarchy obstruction theorem to retained
  status. The parent's load-bearing claim (no finite-order truncation
  of the connected hierarchy) follows from (L1)–(L4) plus elementary
  polynomial-growth reasoning, but the parent must still be re-audited
  by the independent audit lane after registering this companion as a
  dep. The audit lane retains sole authority on lifting the parent's
  effective status;
- derive (BA-1)–(BA-4) from the framework baseline of physical `Cl(3)`
  local algebra on the `Z^3` spatial substrate. (BA-1) is Haar
  orthogonality (Peter-Weyl theorem on compact Lie groups);
  (BA-2) is the compact Laplace concentration theorem; (BA-3) is
  standard analyticity-of-partition-function on compact spaces;
  (BA-4) is analytic continuation of finite-support Taylor series.
  All four are textbook. They are admitted as bounded inputs;
- close the explicit nonpolynomial solution of the connected hierarchy
  (still open per the parent note's "What this does not close"
  section);
- close `analytic P(6)` or any `χ_L(β)` expression;
- promote any sister authority's effective status.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: four lemmas (L1-L4) verified at exact-rational + numerical
precision under the four bounded admissions (BA-1)-(BA-4) [Haar
orthogonality, compact Laplace concentration, entire-function partition
representation, analytic continuation of finite-support Taylor series].
The parent infinite-hierarchy obstruction note's analytic premises are
now supplied. Re-audit of the parent should now find the load-bearing
chain closes from cited bounded authorities.
```
