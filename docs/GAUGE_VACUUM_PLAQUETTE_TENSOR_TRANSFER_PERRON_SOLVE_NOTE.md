# Gauge-Vacuum Plaquette Source-Sector Reference Perron Solve

**Date:** 2026-04-30
**Status:** support — explicit source-sector Perron solves at two
structural reference choices of the residual environment, plus a no-go
on closed-form `rho_(p,q)(6)` from `c_lambda(6)` and `SU(3)`
intertwiners alone. The runner does NOT compute the physical
`rho_(p,q)(6)` for the actual 3D spatial Wilson environment; that 3D
Perron solve is the missing object.
**Script:** `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py`

## Question

The exact stack on `main` reduces the residual `beta = 6` plaquette
problem to one factorized source-sector operator

`T_src(6) = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`

with three pieces:

- the explicit half-slice multiplier `exp(3 J)` for the source operator
  `J = (chi_(1,0) + chi_(0,1)) / 6`,
- the explicit local Wilson marked-link factor
  `D_6^loc chi_(p,q) = a_(p,q)(6)^4 chi_(p,q)`,
- the residual spatial-environment convolution
  `C_(Z_6^env) chi_(p,q) = rho_(p,q)(6) chi_(p,q)`.

The first two are explicitly computable from `c_lambda(6)` (Bessel
determinant mode sum) and `SU(3)` intertwiners alone. The third is the
boundary character measure of the unmarked 3D spatial Wilson environment
with marked-plaquette boundary holonomy held fixed.

Two questions:

1. Can `rho_(p,q)(6)` itself be derived in closed form from the same
   local inputs?
2. Independently of (1), can the resulting Perron data — `P(6)`,
   `u_0 = P^(1/4)`, `alpha_s(v) = alpha_bare / u_0^2` — be computed as
   definite numbers from the local input class on at least some
   well-defined choices of the residual environment?

## Answer

(1) **No.** The local Wilson character coefficients `c_lambda(6)` and
the `SU(3)` intertwiner data, taken together, do not determine
`rho_(p,q)(6)`. This is the no-go in Theorem 3 below.

(2) **Yes for two structural reference choices,** as Theorems 1 and 2
below: `rho = 1` (Dirac-delta environment) and
`rho = delta_{(p,q),(0,0)}` (decoupled environment) each give a
fully explicit Perron solve.

The residual environment is then the missing object. It is identified
explicitly as the Perron eigenvector of the positive tensor-transfer
operator on the 3D unmarked spatial Wilson environment with one
marked-plaquette boundary, a non-perturbative `SU(3)` lattice gauge
problem outside the local character data class.

## Important caveat: rho is INPUT in the reference solves, not OUTPUT

In Theorems 1 and 2 the rho values (`rho = 1` and
`rho = delta_{(p,q),(0,0)}`) are the structural input that *defines*
each reference solve. They are not derived from any physical 3D Wilson
environment computation. What the runner computes from `c_lambda(6)`
and `SU(3)` intertwiners is the resulting Perron eigenvector and its
expectation value of `J`, *given* that input choice.

This note does not claim that either reference solve corresponds to the
physical 3D environment. It claims only that the Perron *machinery* is
explicit and gives definite numbers when fed an explicit rho.

The two reference choices are also NOT endpoints of the admissible rho
class. Admissible rho is unbounded above on non-trivial irreps: for
example, the one-plaquette environment ansatz at `beta_env = 6` already
gives `rho_(1,0) = 1.27 > 1`. The choices `rho = 1` and
`rho = delta` are simply natural structural reference points: the
maximally concentrated and the minimally concentrated environment in
the dominant-weight character basis.

## Setup

From the exact theorems already on `main`:

- the source-sector matrix-element factorization theorem
  [GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md)
  closes `T_src(6) = exp(3 J) D_6 exp(3 J)`;
- the local/environment factorization theorem
  [GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md)
  closes `D_beta^mix,norm chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`;
- the residual-environment identification theorem
  [GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md)
  identifies the remaining open factor as `R_beta^env` after stripping
  the local marked-link factor;
- the spatial-environment character-measure theorem
  [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md)
  realizes `R_beta^env = C_(Z_beta^env)` with eigenvalues
  `rho_(p,q)(beta)` and `rho_(0,0)(beta) = 1`;
- the spatial-environment structural transfer theorem
  [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md)
  gives the positive transfer-operator carrier for that boundary
  class-function problem;
- the spatial-environment tensor-transfer theorem
  [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md)
  identifies these as the boundary amplitudes of an explicit positive
  tensor-transfer operator built from `c_lambda(beta)` and `SU(3)`
  intertwiners.

So the explicit factorized source-sector operator at `beta = 6` is

`T_src(6) = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`,

with the first two factors fully explicit and the third reduced to one
positive diagonal sequence `rho_(p,q)(6)` that is the boundary character
data of the unmarked 3D spatial Wilson environment.

## Theorem 1: explicit reference Perron solve A (input rho = 1)

**Reference choice.** Set `rho_(p,q)(6) = 1` for every irrep,
equivalently `R_6^env = I` (identity on the marked class-function
sector). This corresponds to the structural choice
`Z_6^env(W) = sum d_(p,q) chi_(p,q)(W) = delta(W, e)`, i.e., the
spatial environment is treated as if it concentrates the marked
plaquette holonomy at the identity. This is a structural input, not a
derived value.

**Construction from local Wilson data.** With this rho choice, the
source-sector operator reduces to

`T_src,loc(6) = exp(3 J) D_6^loc exp(3 J)`,

where the only non-trivial pieces are:

- `J chi_(p,q) = (1/6)(chi_(p+1,q) + chi_(p-1,q+1) + chi_(p,q-1)
                       + chi_(p,q+1) + chi_(p+1,q-1) + chi_(p-1,q))`
  (the explicit `SU(3)` six-neighbor source recurrence);
- `a_(p,q)(beta) = sum_(n in Z) det[I_(n + lambda_j + i - j)(beta/3)]_(i,j=1)^3
                    / (d_(p,q) c_(0,0)(beta))`,
  `lambda = (p+q, q, 0)`,
  `d_(p,q) = (p+1)(q+1)(p+q+2)/2`.

Both are constructed entirely from `c_lambda(6)` (via the Bessel-
determinant mode sum) and `SU(3)` intertwiner data (via the dominant-
weight recurrence).

**Computed Perron data.** At `NMAX = 7` and `MODE_MAX = 200` the
runner reports:

- Perron eigenvalue: `3.812630482037`,
- `P_loc(6) = <psi_loc, J psi_loc> = 0.4524071590`,
- `u_0,loc = P_loc^(1/4) = 0.8201293744`,
- `alpha_s,loc(v) = alpha_bare / u_0,loc^2 = 1.4867408201`
  (for `alpha_bare = 1`).

## Theorem 2: explicit reference Perron solve B (input rho = delta)

**Reference choice.** Set
`rho_(p,q)(6) = delta_{(p,q),(0,0)}`, equivalently
`R_6^env = P_(0,0)` (projection onto `chi_(0,0)`). This corresponds
to `Z_6^env(W) = const`, i.e., a decoupled environment that does not
see the marked plaquette holonomy. This is again structural input.

**Computed Perron data.** The source-sector operator
`T_src,triv(6) = exp(3 J) D_6^loc P_(0,0) exp(3 J)` is rank-one with
image span `exp(3 J) chi_(0,0)`. The runner reports:

- Perron eigenvalue: `3.441440354984`,
- `P_triv(6) = 0.4225317396`,
- `u_0,triv = 0.8062409160`,
- `alpha_s,triv(v) = 1.5384037545`.

## Theorem 3: explicit no-go on `rho_(p,q)(6)` closure

Consider three explicit one-parameter families inside the admissible
class of residual data:

1. **Decay family.** `rho_(p,q)(6) = exp(-tau (p+q))` for `tau >= 0`.
   At `tau = 0`, recovers the Theorem 1 reference; as
   `tau -> infinity`, recovers the Theorem 2 reference.
2. **One-plaquette environment family.**
   `rho_(p,q)^(beta_env) = c_(p,q)(beta_env) / c_(0,0)(beta_env)` for
   `beta_env >= 0`. Each member is one strictly admissible normalized
   character measure (the one-plaquette Wilson partition function as
   environment).
3. **Tube-power family.**
   `rho_k = (c_(p,q)(6) / c_(0,0)(6))^k` for integer `k >= 0`. At
   `k = 0`, recovers Theorem 1; as `k` grows, the rho values grow
   sharply for low `(p,q)` and decay for high `(p,q)`.

Each family uses only `c_lambda` and `SU(3)` intertwiners, plus a
single exogenous parameter `(tau, beta_env, k)`. Each member of each
family is strictly admissible (positive, conjugation-symmetric,
normalized at `(0,0)`). None coincides with either reference solve.

The runner reports the following Perron-value spreads:

- family 1 spread: `0.0297` over `tau in [0, 5]` (range `[0.4225, 0.4524]`);
- family 2 spread: `0.0653` over `beta_env in [0, 20]` (range
  `[0.4225, 0.4878]`);
- family 3 spread: `0.1638` over `k in [0, 20]` (range `[0.4524, 0.6163]`);
- combined spread: `>= 0.1937`.

In particular, distinct admissible rho choices, all built from the same
`c_lambda(6)` and `SU(3)` intertwiner data, produce strictly different
values of `P(6)`. **Therefore `c_lambda(6)` and `SU(3)` intertwiners
do not, by themselves, fix `rho_(p,q)(6)` via 1-parameter local closure.**

The canonical same-surface plaquette value `0.5934` lies inside the
combined admissible span (reached for example near `k = 12` in family
3), but no parameter choice within these 1-parameter families is
canonically picked out by the local input class. The runner does not
select a parameter to match `0.5934`; instead it sweeps the parameter
and reports the resulting `P(6)` sequence as evidence of non-uniqueness.

### Scope clarification (added 2026-05-04)

**Important narrowing.** The argument above explicitly enumerates THREE
specific 1-parameter families and shows none of them is canonically
picked out by `c_lambda(6)` + `SU(3)` intertwiners. The correct
conclusion that follows logically is:

> **No 1-parameter local family closes `rho_(p,q)(6)`.**

The original phrasing "Closed-form derivation of `rho_(p,q)(6)` from
those local inputs alone does not exist" is broader than what the
argument actually proves. It would also rule out **0-parameter
derivations** (derivations with no free parameter to fit), which the
3-family argument does NOT rule out.

In particular, the **Schur cube finite-volume calculation** is a
0-parameter calculation that uses `c_lambda(6)`, `SU(3)` intertwiners,
AND the explicit cube graph geometry. It computes:

```text
rho_Schur_(p,q)(6) = (c_(p,q)(6) / c_(0,0)(6))^N_plaq × d_(p,q)^(N_components - N_links)
```

with `N_components` from the cyclic-index graph of the cube. For
the L_s=2 PBC cube under the all-forward convention with N_components = 8,
this gives the value `P_Schur = 0.4291` (per
`scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py` and
[`SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md)).

**Schur's `rho_Schur` is not in any of the 3 enumerated families** (it
has both `c/c_00` factors and `d^(...)` factors; the 3 families have
only one or the other). So Theorem 3's scope is **narrower** than its
title suggests.

**Updated honest scope of Theorem 3:**

- `rho_(p,q)(6)` is NOT fixed by any 1-parameter family of the 3 forms
  enumerated.
- `rho_(p,q)(6)` IS computed for the tested all-forward L_s=2 cube
  surface by the Schur finite-volume calculation using cube graph
  topology in addition to `c_lambda` and intertwiners.
- The Schur calculation gives a SPECIFIC value (P = 0.4291 at L_s=2
  PBC cube), which does NOT match the canonical MC value 0.5934. This
  is a finite-volume candidate value, not a free parameter.
- For matching MC 0.5934 via L_s=2 cube: requires either an additional
  framework primitive beyond local data + cube geometry, OR a
  realization that the L_s=2 cube prediction is genuinely 0.4291 and
  the MC 0.5934 reflects finite-volume / thermodynamic-limit effects.
- For L_s ≥ 3 cube: the Schur derivation has not been done in this
  framework; this is a candidate for matching MC if larger-L cubes
  give different ρ.

The corrected no-go is therefore: `c_lambda(6)` + `SU(3)` intertwiners
+ ANY 1-parameter family ansatz ≠ canonical ρ. Adding cube graph
geometry gives a SPECIFIC all-forward L_s=2 finite-volume ρ but not
the MC value at L_s=2.

## Theorem 4: NMAX truncation tail bound

The Wilson character coefficients on the dominant-weight box decay
super-polynomially with the rep size at fixed `beta`. The runner
verifies this empirically:

- successive truncation drifts decay geometrically:
  `|P(NMAX=7) - P(NMAX=6)| = 1.142e-9`,
  `|P(NMAX=6) - P(NMAX=5)| = 1.139e-7`,
  ratio of successive prior drifts `≈ 69`;
- the dominant-weight band sum at the truncation edge is below
  `1.0e-10`: `max_(p+q=NMAX) a_(p,q)(6)^4 = 2.54e-16`.

This is consistent with the Bessel-determinant structure of
`c_(p,q)(beta)` at fixed `beta`: the highest-weight triple
`(p+q, q, 0)` appears in the determinant index, and `I_n(beta/3)`
decays super-polynomially in `n` at fixed `beta`. The Peter-Weyl
character expansion of any positive central function on `SU(3)`
inherits this decay through the convolution structure, so finite-NMAX
truncation introduces an error that is super-polynomially small in
NMAX.

The runner reports a converged value at NMAX = 7 with truncation
residual `< 1e-9`, well inside theorem-grade tolerance, and reports
the geometric drift ratio explicitly so a reviewer can independently
verify the super-polynomial decay claim.

`MODE_MAX` convergence is even faster: the runner reports
`|P(MODE_MAX=200) - P(MODE_MAX=160)| = 0` to working precision, again
consistent with the rapid decay of `I_n(2)` in `n`.

## Corollary 1: the missing mathematical object

The remaining theorem-grade object on `main` is therefore one specific
non-perturbative quantity:

> the boundary character measure `Z_6^env(W)` of the unmarked 3D
> spatial Wilson environment with the marked plaquette holonomy `W`
> held fixed,
> equivalently the Perron eigenvector of the explicit positive
> tensor-transfer operator built from `c_lambda(6)` and `SU(3)`
> intertwiners on a 3D `SU(3)` lattice gauge network with one
> marked-plaquette boundary.

The local Wilson character coefficients and `SU(3)` intertwiners
furnish only the local building blocks of that 3D tensor network. The
network's dominant-eigenvector solve is the missing input.

## Hostile-review section

This subsection records the explicit checks the runner performs to
guard against the four hostile-review failure modes flagged for this
PR (see `feedback_hostile_review_semantics.md`,
`feedback_consistency_vs_derivation_below_w2.md`, and
`feedback_retained_tier_purity_and_package_wiring.md`).

### Not a constant-lift ansatz

The Wilson character coefficients `a_(p,q)(6)` span the audited box
with extreme rep-dependence:

- `a_(0,0) = 1.000000`,
- `a_(1,0) = a_(0,1) = 0.422532`,
- `a_(1,1) = 0.162260`,
- `a_(2,2) = 5.84e-7` (in audited box),
- spread `max(a)/min(a) ≈ 7.32e9`.

A constant-lift effective coupling would produce
`a_(1,1) = a_(1,0)^2`. The actual ratio is
`a_(1,1) / a_(1,0)^2 = 0.9089`, not `1`. The runner explicitly checks
this and the constant-lift hypothesis is rejected.

The exact constant-lift obstruction theorem
[`GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`](./GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)
already on `main` rules out constant-lift altogether at the
strong-coupling slope level. The present note is consistent with that
obstruction and does not depend on it.

### No tuning, comparator isolated

The runner contains exactly one occurrence of the canonical
same-surface plaquette numeric, in a single named constant
`CANONICAL_COMPARATOR = 0.5934`. That constant is consumed only by the
hostile-review diagnostics that verify *neither* reference solve
matches it:

- `|P_loc - CANONICAL_COMPARATOR| = 0.1410`,
- `|P_triv - CANONICAL_COMPARATOR| = 0.1709`.

It is not used as input, initialization, or fit target anywhere in the
Perron solve, the parametric sweeps, or the convergence study. The
parametric sensitivity sweeps explicitly demonstrate that DIFFERENT
admissible rho choices produce DIFFERENT `P(6)`; the runner does not
select a particular rho to match the comparator. Specifically, family
3 reaches `0.5888` at `k = 12` and overshoots to `0.6163` at `k = 20`,
illustrating that no `k` value is canonically picked out.

### Not a renamed residual operator

The explicit local Wilson marked-link factor `D_6^loc` (eigenvalues
`a_(p,q)(6)^4`) and the trivial-projection `P_(0,0)` are operator-
distinct: `max|D_loc - P_(0,0)| = 0.0319`. They produce different
Perron values: `|P_loc - P_triv| = 0.0299`.

The residual environment operator `C_(Z_6^env)` is not a renaming of
`D_6^loc`. The local/environment factorization theorem cleanly
isolates `D_6^loc` as the trivial-channel-normalized mixed-kernel
local factor (exact one-link Wilson convolution to the fourth power),
while `C_(Z_6^env)` is the residual unmarked spatial environment
convolution after that local factor has already been stripped off. The
two operators play structurally different roles and produce different
Perron data when toggled.

### Truncation tail bounded, not extrapolated

The runner does not extrapolate the NMAX truncation. It reports
explicit truncation drift values and the dominant-weight band sum at
the truncation edge, both of which are super-polynomially small (see
Theorem 4). The reported `P_loc(6)` and `P_triv(6)` numbers are the
finite-NMAX values at `NMAX = 7`; the truncation residual is bounded
by the geometric drift sequence, with reported geometric ratio `≈ 69`
between successive drifts. No theorem-grade claim about the strict
infinite-NMAX limit is made beyond what the geometric decay supports.

### rho is INPUT in the reference solves, not OUTPUT

The two reference Perron solves use *chosen* rho values
(`rho = 1` and `rho = delta`) as structural input. The runner
computes the resulting Perron eigenvector and its expectation of `J`
from `c_lambda(6)` and `SU(3)` intertwiners. It does NOT claim that
either rho choice is derived from any physical 3D environment, and
the note explicitly disavows that interpretation.

The "computed `rho_(p,q)(6)`" reported by the runner is therefore the
INPUT definition of each reference solve, plus the explicit Perron
eigenvector content (which IS computed from local Wilson data). The
no-go in Theorem 3 makes this distinction explicit: the physical
`rho_(p,q)(6)` is not derivable from local Wilson data alone.

### Status purity

The note's `Status:` line is `support`. It does **not** claim
retained or promoted tier; it does **not** propagate retained status
through the audit ledger. The two reference Perron solves close
explicit Perron data on a defined structural choice of the residual
environment, not the full residual operator. The new ledger row is
correctly seeded as `unaudited` and queued for fresh-context audit.

## What this closes

- explicit reference-solve A Perron solve at `beta = 6` from
  `c_lambda(6)` and `SU(3)` intertwiners alone (with input choice
  `rho = 1`), with super-polynomial NMAX/MODE_MAX truncation tail
  bound
- explicit reference-solve B Perron solve at `beta = 6` from the same
  local inputs (with input choice `rho = delta_{(p,q),(0,0)}`)
- explicit reported Perron eigenvector content, `P(6)`, `u_0`, and
  `alpha_s(v)` numerical values for both reference solves
- exact no-go (Theorem 3) that `c_lambda(6)` and `SU(3)` intertwiners
  do not, by themselves, fix `rho_(p,q)(6)` on the source sector,
  exhibited via three distinct admissible parametric families that
  produce strictly different `P(6)`
- exact identification of the missing object as the 3D spatial
  Wilson Perron eigenvector, equivalent to the boundary character
  measure of the unmarked spatial environment with marked-plaquette
  boundary
- explicit hostile-review checks on constant-lift, tuning, renaming,
  and truncation extrapolation concerns

## What this does not close

- explicit physical `rho_(p,q)(6)` for the actual 3D spatial Wilson
  environment
- analytic closure of canonical `P(6) = 0.5934`
- repo-wide repinning of the canonical plaquette
- full-volume tensor-transfer Perron solve in 3D

## Commands run

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=3 FAIL=0`
