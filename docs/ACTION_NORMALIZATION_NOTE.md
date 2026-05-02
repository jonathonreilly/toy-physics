# Action Normalization: Convention-Locked Coupling Coefficient

**Status:** bounded - convention-locked support, not a c-fixing first-principles theorem
**Script:** `scripts/frontier_action_normalization.py`
**Date:** 2026-04-12 (NARROWED 2026-05-01)

## The Reviewer's Objection

"You chose S = L(1-f). If you chose S = L(1-2f), you'd get a different metric.
The coefficient is arbitrary."

## Summary of the Response (NARROWED)

The coefficient `c` in `S = L(1 - c*f)` is **not** independently observable: there
is a one-parameter rescaling degeneracy `(c, G) -> (c/a, a*G)` that leaves the
dynamics invariant. Once one names the convention identifying the lattice scalar
`f` with the physical Newtonian potential `Phi` and fixes the Poisson source
normalization, `c` is determined.

This note **does not** claim `c = 1` is fixed by a convention-free observable. The
earlier claim that "light bending fixes c=1" was retracted on review. The PPN
parameter gamma = 1 holds for any positive `c` once `Phi = c*f/2`, so PPN gamma
alone does not fix `c`.

## The Argument (Three Steps, Narrowed)

### 1. Self-consistency converges for the tested c values

The propagator-field self-consistency loop (propagate -> get density -> solve
Poisson -> propagate) converges for the positive `c` values tested in the
runner. Self-consistency alone does not select `c`.

### 2. Rescaling degeneracy

The transformation `(c, G) -> (c/a, a*G)` leaves the dynamics invariant because
the self-consistent loop depends only on the product `c*G`. This is verified
numerically: `c*phi_max` is approximately constant across rescalings at fixed
`c*G`. There is therefore a one-parameter family of equivalent theories
parameterized by `c`.

### 3. Convention fixes c

Once we adopt the framework's natural convention identifying the lattice
scalar `f` with the Newtonian potential `Phi`:

- Convention A: `f = Phi` with the standard Newtonian Poisson source
  `nabla^2 f = -4*pi*G*rho`. Matching the Schwarzschild weak-field metric
  `g_tt = -(1 - 2*Phi)` to the lattice metric `g_tt = -(1 - c*f)` forces
  `c = 2`.
- Convention B: the framework's actual choice `S = L(1 - f)` (i.e., `c = 1`)
  corresponds to a lattice Poisson source rescaled by a factor of 2 relative
  to textbook Newtonian. Matching forces this together with `c = 1`.

Both choices reproduce the Schwarzschild weak-field metric and PPN gamma = 1.
The difference is an overall convention on what `f` means and how the Poisson
equation is normalized, not new physics.

## Key Numerical Results (Narrowed)

| c    | Converges | beta  | Note                                        |
|------|-----------|-------|---------------------------------------------|
| 0.5  | Yes       | 1.28  | converges, deflection scales with c         |
| 1.0  | Yes       | 1.28  | framework choice (with absorbed factor 2)   |
| 2.0  | Yes       | 1.28  | textbook Newtonian convention               |
| 5.0  | Yes       | 1.28  | converges, deflection scales with c         |

The mass exponent `beta ~ 1.28` is a finite-size lattice artifact (`N=20`
grid, Dirichlet boundary). It is independent of `c` because the field is
perturbatively weak.

The earlier "Light Factor = 1 + c" entry in this table was a purely analytical
restatement of the (1+gamma) Schwarzschild deflection result. It cannot be
verified by the present propagator (the runner uses a single massive quantum
probe, with no separate null-ray channel). That column has been removed.

## Response to the Reviewer (Narrowed)

The objection is partially correct: the coefficient `c` is convention-dependent.
There is a literal `(c, G) -> (c/a, a*G)` rescaling freedom in the theory.

Within the framework, what fixes the coefficient is not a convention-free
observable but the natural convention adopted for what `f` means in terms of
the standard Newtonian potential `Phi` together with the Poisson source
normalization. The framework's choice of `S = L(1 - f)` corresponds to a
specific convention; the textbook Newtonian choice would give `S = L(1 - 2f)`.
Both reproduce Schwarzschild.

This is analogous to the ambiguity in the gauge potential `A` in
electromagnetism (modulo the analogous rescaling of charge): the freedom is
real, and it is fixed by convention, not by a convention-free measurement.

## Earlier Wording Retracted

The previous version of this note claimed `c = 1` is fixed by the
convention-free observable of the factor-of-2 light bending. That argument
was incorrect: PPN gamma = 1 (which IS the factor-of-2 light bending content)
holds for any positive `c` under the identification `Phi = c*f/2`. The runner's
former numerical "deflection ratio" verification (`defl(k=5)/defl(k=25)`)
compared two massive-probe momenta and had no analytical relation to the
`(1+c)` null-vs-massive deflection ratio. Both the bogus numerical table and
the convention-free claim have been removed from this runner and note.
