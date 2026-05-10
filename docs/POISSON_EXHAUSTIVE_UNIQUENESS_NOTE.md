# Poisson Exhaustive Uniqueness

**Claim type:** bounded_theorem (finite-grid candidate-enumeration diagnostic)
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_poisson_exhaustive_uniqueness.py`](../scripts/frontier_poisson_exhaustive_uniqueness.py)

## Audit context

This note was previously audited `audited_conditional` (verdict
2026-05-05) on the grounds that an earlier version asserted Poisson
uniqueness in the *continuous* fractional-Laplacian family and in the
continuum limit, while the runner only supplies a *finite-grid sampled*
diagnostic on `N = 16` against an explicitly enumerated, finite list of
candidate operators. The auditor's stated repair target was to prove or
cite within the packet a bridge theorem connecting the finite `N = 16`
sampled `beta(alpha)` table to continuous-`alpha` uniqueness and the
continuum `alpha = 1` Poisson selection, *or* to narrow the claim to
the finite candidate-enumeration scope that the runner supplies.

This revision takes the second path. It scopes the claim to the
explicitly enumerated 21-operator candidate set on the `N = 16` grid
that the runner actually evaluates, and lists the missing bridge
theorems as explicit out-of-scope items.

## Bounded claim (this note)

On the `N = 16` cubic grid with Dirichlet boundary conditions used by
[`scripts/frontier_poisson_exhaustive_uniqueness.py`](../scripts/frontier_poisson_exhaustive_uniqueness.py),
under the framework's self-consistent path-sum propagator iteration
with parameters `k = 5.0`, `G = 0.5`, `sigma = 2.0`, `mixing = 0.3`,
`tol = 1e-4`, `max_iter` as specified per part, and a centered
point source, the explicitly enumerated 21-operator candidate set
(below) yields the following observed selection pattern:

1. The standard nearest-neighbor 7-point Poisson operator
   `nabla^2 phi = -G rho` converges to a self-consistent attractive
   field with monotonically decaying `|phi(r)|` and a power-law fit
   exponent `beta` close to `1` (within finite-grid bias on `N = 16`).
2. Among the ten sampled fractional-power operators
   `L_alpha = (-nabla^2)^alpha`, the fitted `beta` value varies
   *monotonically* with `alpha` over the sampled set, so on this
   `N = 16` grid the `|beta - 1|` minimum is attained at a *unique*
   point of the *sampled* `alpha`-list (closest to Newtonian crossing
   on this grid is near `alpha ~ 1.5`, due to a finite-size bias that
   inflates all `beta` values).
3. Anisotropic Laplacians `wx d^2/dx^2 + wy d^2/dy^2 + wz d^2/dz^2`
   for the four enumerated weight tuples `(1,1,1), (2,1,1), (1,2,1),
   (3,1,1)` all converge with attraction (`beta in [1.14, 1.44]`).
4. The two enumerated non-local operators (the next-nearest-neighbor
   26-neighbor Laplacian and the exponentially-decaying long-range
   Laplacian at decay lengths `1.0` and `2.0`) *fail to converge* in
   the runner's self-consistent iteration with the runner's choice of
   mixing, boundary conditions, normalization, and iteration count.
5. The three enumerated higher-order stencils (2nd-order 7-point,
   4th-order 13-point, 6th-order 19-point) all converge with attraction
   and agree on `beta` to within `< 0.02`.

This is a finite, candidate-enumeration uniqueness diagnostic on the
`N = 16` grid, *not* a continuum-limit uniqueness theorem and *not* an
exhaustiveness theorem over all local symmetric graph-compatible
operators.

## Candidate enumeration (explicit, exhaustive within scope)

The "candidate set" for this bounded note is exactly the 21 operators
that the runner instantiates and tests, partitioned into four classes:

### Class 1 — sampled fractional Laplacians `L_alpha = (-nabla^2)^alpha`

Defined via the spectral decomposition `L_alpha = sum_i lambda_i^alpha
|v_i><v_i|` of the negated nearest-neighbor Laplacian on the `N = 16`
interior, evaluated at the ten sampled `alpha` values:

```text
alpha in { 0.25, 0.50, 0.75, 0.90, 1.00,
           1.10, 1.25, 1.50, 2.00, 3.00 }.
```

`alpha = 1.00` is the standard Poisson operator. `alpha < 1` is
sub-Laplacian; `alpha > 1` is super-Laplacian.

### Class 2 — enumerated anisotropic Laplacians

Four weight tuples `(wx, wy, wz)`:

```text
(1, 1, 1),   (2, 1, 1),   (1, 2, 1),   (3, 1, 1).
```

### Class 3 — enumerated non-local operators

Two operator constructions:

- next-nearest-neighbor Laplacian with 26 neighbors at distance-weighted
  coupling `1/distance`, normalized so the central interior diagonal
  matches the standard Laplacian scale `~ 6.0`;
- long-range Laplacian with exponentially-decaying coupling `exp(-d /
  decay_length)` over neighbors within `max_range = 2`, evaluated at
  decay lengths `1.0` and `2.0`. (Two decay-length samples → two
  operators; together with the NNN operator this gives three non-local
  candidates.)

### Class 4 — enumerated higher-order stencils for `nabla^2`

Three finite-difference stencils:

- 2nd-order 7-point standard stencil;
- 4th-order 13-point stencil with diagonal `-15/2`, distance-1 weight
  `4/3`, distance-2 weight `-1/12`;
- 6th-order 19-point stencil with diagonal `-49/6`, distance-1 weight
  `3/2`, distance-2 weight `-3/20`, distance-3 weight `1/90`.

Total enumerated candidates: `10 + 4 + 3 + 3 = 20` non-Poisson
candidates plus the standard Poisson baseline `= 21` operators. All 21
are instantiated, solved, and checked by the runner with identical
self-consistent-iteration parameters.

## What the diagnostic does *not* establish

This bounded note does *not* close any of the following items, each of
which the auditor previously named as out-of-scope for the runner:

- Continuum-limit identification of the `beta = 1` crossing with the
  *Poisson* `alpha = 1` operator. On `N = 16` the closest crossing is
  near `alpha ~ 1.5`; the analytic claim that this crossing flows to
  `alpha = 1` as `N -> infinity` requires a separate
  finite-size-extrapolation runner and a continuum
  fractional-Laplacian Green's-function scaling theorem, neither of
  which is provided here.
- Exhaustiveness over the full *continuous* fractional family `L_alpha`
  for `alpha in (0, infinity)` (the runner samples ten `alpha` values
  only).
- Exhaustiveness over the full class of *all* local symmetric
  graph-compatible operators (the runner enumerates the four classes
  above and no more).
- A separation of the non-local divergence into "physical" vs
  "numerical-conditioning" causes. The non-local convergence failures
  are observed under the runner's specific iteration scheme (mixing
  `0.1`, `max_iter = 40`, normalization to match the standard
  Laplacian's central diagonal, Dirichlet boundaries within a
  single-buffer layer); the auditor's prior verdict explicitly noted
  that under different regularization, mixing, or conditioning the
  non-local divergence may not reflect a structural incompatibility.
- Any retention upgrade of the parent
  [`GATE_B_POISSON_SELF_GRAVITY_NOTE.md`](GATE_B_POISSON_SELF_GRAVITY_NOTE.md)
  or
  [`POISSON_SELF_GRAVITY_LOOP_NOTE.md`](POISSON_SELF_GRAVITY_LOOP_NOTE.md)
  chains.
- Any continuum Poisson uniqueness theorem.

## Bridge theorems explicitly out of scope

The auditor's `notes_for_re_audit_if_any` field names the missing
bridge theorem(s). For the record, the items not provided in this
packet are:

1. A continuum fractional-Laplacian Green's-function scaling theorem
   identifying the `beta = 1` crossing with `alpha = 1` in the
   `N -> infinity` limit on `Z^3`.
2. A finite-size-extrapolation runner showing that the sampled
   `N = 16` crossing (near `alpha ~ 1.5`) flows to `alpha = 1` as
   `N` increases (e.g., `N in {8, 12, 16, 24, 32, 48}`).
3. An operator-family exhaustiveness theorem for *all* local symmetric
   graph-compatible operators on `Z^3` consistent with the framework's
   nearest-neighbor propagator connectivity.
4. A non-local-operator regularization-stability check that controls
   for iteration mixing, boundary conditions, and normalization, so
   the non-local convergence failures can be ascribed to the operator
   class rather than to numerical conditioning.

These four items are the named compute / theory frontier for any
later promotion of this row toward continuum Poisson uniqueness; this
note does not provide them and does not claim them.

## Method (runner)

The runner
[`scripts/frontier_poisson_exhaustive_uniqueness.py`](../scripts/frontier_poisson_exhaustive_uniqueness.py)
solves, for each of the 21 candidate operators above, the
self-consistent fixed-point iteration

```text
phi_{n+1}  =  (1 - mixing) * phi_n  +  mixing * L^{-1}( -G * rho_n ),
rho_n      =  | psi_n |^2  with  psi_n  the path-sum propagator amplitude
              evaluated against phi_n,
```

stopping when `max_residual < tol = 1e-4` or `max_iter` is reached.
For each converged result the runner fits `phi(r) ~ r^{-beta}` for `r`
along an axis from the source, records `beta`, the `R^2` of the linear
log-log fit, attractiveness sign, and monotonicity. The four classes
above correspond to the four tabulated parts of the runner output.

The runner is *strictly* a finite-grid candidate-enumeration diagnostic.
It does not interpolate `alpha`, does not extrapolate in `N`, does not
prove exhaustiveness over all symmetric local operators, and does not
distinguish numerical from structural divergence for non-local
candidates.

## Dependencies

- [`GATE_B_POISSON_SELF_GRAVITY_NOTE.md`](GATE_B_POISSON_SELF_GRAVITY_NOTE.md)
  for the parent gate context that this finite-grid diagnostic is a
  support row for. This note does not promote that gate.
- [`POISSON_SELF_GRAVITY_LOOP_NOTE.md`](POISSON_SELF_GRAVITY_LOOP_NOTE.md)
  for the self-consistent iteration setup that the runner shares.
- [`SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`](SELF_CONSISTENCY_FORCES_POISSON_NOTE.md)
  for the upstream argument that self-consistency picks out a Poisson
  channel; this note is a finite-grid candidate-enumeration check
  *within* that channel and does not extend it.

These are imported authorities. The row remains audit-driven for its
status; the source-note does not assert a status for itself.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_poisson_exhaustive_uniqueness.py
```

Expected (within the bounded scope above):

```text
Total operators tested: 21
Converged + attractive + monotonic: <subset of 21>
PART 1: monotonic beta(alpha) over the sampled 10 alpha values
PART 2: all 4 anisotropic Laplacians converge with attraction
PART 3: NN baseline converges, both non-local candidates diverge
PART 4: 2nd/4th/6th-order stencils converge consistently
```

The expected output is the runner's printed `GRAND SUMMARY` and `SAFE
CLAIMS` sections. Any line of the runner asserting "unique among all
local symmetric operators" or "in the continuous family" should be
read as referring *only* to the candidate set explicitly enumerated
above; that is the bounded scope of this note.

## Boundaries

This note does *not* close, *does not* promote, and *does not* claim:

- continuum-limit Poisson uniqueness;
- continuous-`alpha` uniqueness in `(-nabla^2)^alpha`;
- exhaustiveness over local symmetric graph-compatible operators
  beyond the 21 explicitly-enumerated candidates;
- a structural-vs-numerical separation of the non-local divergences;
- any retention upgrade of the Gate B self-gravity chain;
- any new repo-wide theory class or new vocabulary; "Poisson",
  "exhaustive uniqueness within candidate enumeration", and
  "fractional Laplacian" are repo-canonical.
</content>
</invoke>