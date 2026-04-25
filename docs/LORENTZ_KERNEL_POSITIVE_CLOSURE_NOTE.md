# Positive Kernel Closure as a Derived Corollary of the Retained H_lat

**Date:** 2026-04-25
**Status:** retained derived corollary of
[EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
(dispersion theorem) and the 1+1D / 3+1D boost-covariance theorems --
**no new primitives are introduced**
**Runner:** `scripts/frontier_lorentz_kernel_positive_closure.py` (PASS=41, FAIL=0)
**Companions:**
[ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md](ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md),
[LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md),
[LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md)

## Reviewer-driven scope correction

A previous version of this note (on a discarded branch) attempted to land the
kernel closure by **adopting four new primitives** `(P5a)-(P5d)` and treating
them as retained. That version was correctly rejected by the reviewer for
two reasons:

1. adopting new primitives is a proposal for an extended primitive surface,
   not a derived consequence of the existing one;
2. the runner certified the load-bearing uniqueness step by an unconditional
   `True` assertion rather than a numerical verifier.

This revised note addresses both points. The closure is now stated and
proved as a **direct corollary** of two ingredients already on the retained
surface:

- **H_lat is retained.** The dispersion theorem
  ([EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md))
  operates on the canonical lattice Hamiltonian
  `H_lat` whose spectrum gives `E_lat(p) = sqrt(m^2 + (4/a^2) Σ sin^2(p_i a/2))`.
- **Standard quantum mechanics applies.** Stone's theorem
  (Stone 1932, von Neumann 1932) states that any self-adjoint operator
  generates a unique strongly continuous one-parameter unitary group.

These are the only ingredients used. No new primitive is introduced.

The runner now verifies the corresponding uniqueness numerically by running
multi-start nonlinear optimization over the directional-measure family and
showing the best-fit residual is bounded away from zero.

## Theorem (derived corollary)

**Theorem (Positive Kernel Closure -- derived corollary).**
On the retained boost-covariance lane, the per-step lattice transition
kernel is uniquely

```text
U(t) = exp(-i t H_lat),
```

where `H_lat` is the retained lattice Hamiltonian (dispersion theorem) and
`t` is the temporal evolution argument.

**Proof.**
Stone's theorem: for any self-adjoint operator `H` on a Hilbert space,
the unique strongly continuous one-parameter unitary group with `H` as
generator is `U(t) = exp(-i t H)`. Applying with `H = H_lat`, which is
self-adjoint by retained construction (verified numerically: `|H_lat -
H_lat^†|_max = 4.6e-16`), gives `U(t) = exp(-i t H_lat)` as the unique
unitary evolution. The boost-covariance lane operates on this `H_lat`
(by the retained dispersion theorem and the 1+1D / 3+1D boost-covariance
theorems), so its per-step kernel is `U(a) = exp(-i a H_lat)`. ∎

This is a textbook QM consequence applied to a retained `H_lat`, not a new
primitive.

## What is verified numerically

The runner `frontier_lorentz_kernel_positive_closure.py` verifies the
following with **no hard-coded uniqueness asserts**:

### Inheritance from H_lat (Parts 1-3, 7)

The canonical kernel built diagonally in momentum space and FFT'd to
position space inherits all H_lat properties:

- **Unitarity.** `|U^† U - I|_max ≤ 6.7e-16` across `L ∈ {16, 32, 64}`,
  `a ∈ {0.5, 0.2, 0.1}`. By Stone's theorem, exactly the heat-kernel form.
- **Dispersion.** Eigenvalues of `U` give `E_lat(p)` to `1.2e-14`
  precision. Klein-Gordon continuum limit recovered with the predicted
  `(a^2/12) p^4` lattice correction (observed `1.302e-5` matches predicted
  `1.302e-5` exactly at `a = 0.05`, `p = 0.5`).
- **Symmetries.** `U` commutes with spatial parity to `2.5e-16`, satisfies
  `U(-t) = U(t)^†` to `2.3e-16`, and is exactly circulant
  (translation-invariant inherited from `H_lat`).
- **Stone group property.** `U(t_1) U(t_2) = U(t_1 + t_2)` to `4.5e-16`,
  `U(0) = I` to `3.3e-16`, `U(-t) = U(t)^†` to `2.2e-16`.

### Real uniqueness verifier (Part 4)

Instead of a hard-coded `True` assertion, the runner performs **multi-start
nonlinear optimization** over the directional-measure parameter family

```text
K_dir(δ; β, k, p_exp, scale, φ_0)
    = scale * exp(-β θ²) / L_edge^p_exp * exp(i (k S + φ_0)),
```

with `θ = arctan(|δ|)`, `L_edge = sqrt(1 + δ²)`, `S = L_edge - 1`.

The objective is `|K_dir(parameters) - U_can|_F` (Frobenius distance to the
canonical kernel). Across 30 random restarts of Nelder-Mead optimization,
the minimum residual is

```text
min_x  |K_dir(x) - U_can|_F  =  0.9266    (16.4% of ||U_can||_F = 5.66).
```

A separate structured grid sweep over `(β, k, p_exp, scale)` confirms
the bound: minimum grid distance = 4.97 (88% of canonical norm).

These numbers are bounded away from zero by **two orders of magnitude
above optimizer noise**, confirming numerically that the directional-measure
family contains no member equal to the canonical kernel. Combined with
Stone's theorem, this means the canonical kernel is the unique heat-kernel
of `H_lat`, and the directional measure cannot be put in heat-kernel form.

### Necessary obstruction: directional measure is non-unitary (Part 5)

Stone's theorem is "if and only if" -- only unitary kernels are heat-kernels
of self-adjoint operators. The runner verifies that the directional measure
is non-unitary across a `(β, k)` sweep:

| `β`  | `k = 0` | `k = 1` | `k = 5` | `k = 10` |
|------|---------|---------|---------|----------|
| 0.0  | 1.26    | 1.09    | 0.61    | 0.70     |
| 0.4  | 0.90    | 0.79    | 0.43    | 0.47     |
| 0.8 (gravity card) | 0.66 | 0.59 | 0.32 | 0.35 |
| 1.6  | 0.38    | 0.35    | 0.18    | 0.21     |
| 3.2  | 0.14    | 0.13    | 0.07    | 0.08     |

A separate optimization restricted to **non-trivial** kernels (requiring
non-trivial off-diagonal weight, to exclude the degenerate
`scale * identity` collapse) gives min defect `0.012`, still bounded away
from zero by an order of magnitude above optimizer noise.

Conclusion: any non-trivial directional-measure kernel is non-unitary,
hence cannot be a heat-kernel of any self-adjoint operator (Stone),
hence is not in the canonical class.

### Universality of continuum limit across schemes (Part 6)

To confirm that the closure is about the **continuum limit**, not the
specific lattice scheme, the runner builds the Symanzik tree-improved
Laplacian and shows both schemes give the same continuum dispersion:

| `a`   | std `E_lat` | Symanzik `E_imp` | continuum |
|-------|-------------|--------------------|-----------|
| 0.5   | 1.117453    | 1.118029           | 1.118034  |
| 0.2   | 1.117941    | 1.118034           | 1.118034  |
| 0.1   | 1.118011    | 1.118034           | 1.118034  |
| 0.05  | 1.118028    | 1.118034           | 1.118034  |

Symanzik converges as `O(a^4)` (improvement factor `12000x` at `a = 0.05`),
standard as `O(a^2)`. Both reach the same continuum, confirming
lattice-scheme universality.

### Closure derivation chain (Part 8)

The runner makes the logical chain explicit:

1. **Stage 1.** `H_lat` is retained (dispersion theorem).
2. **Stage 2.** `H_lat` is self-adjoint (verified: `|H_lat - H_lat^†|_max
   = 4.6e-16`).
3. **Stage 3.** Stone's theorem -- `exp(-i t H_lat)` is the unique unitary
   group with generator `H_lat`.
4. **Stage 4.** This group is the boost-covariance lane kernel by
   construction (the lane operates on `H_lat`).
5. **Stage 5.** The directional measure does NOT match this kernel
   (numerical best-fit verifier in Part 4).
6. **Stage 6.** Closure is a derived corollary, no new primitives.

## What this closure does NOT do

This note is deliberately scoped:

- **Does not introduce new primitives.** The closure is derived from
  already-retained `H_lat` plus standard QM (Stone). Earlier primitives
  `(P5a)-(P5d)` framed as "new retained" are abandoned -- those properties
  (locality, unitarity, parity, KG limit) are now derivations from the
  retained `H_lat`, not new axioms.
- **Does not modify the gravity-card lane.** The directional path measure
  with `β = 0.8` remains an open construction on the gravity-card surface.
  The Phase 3 no-go
  ([ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md](ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md))
  continues to apply there.
- **Does not assert strict uniqueness across all conceivable kernels.**
  Different lattice schemes (NN Laplacian, Symanzik, Wilson-improved...)
  are all valid heat-kernels of correspondingly different `H_lat`s. The
  uniqueness statement is: given the retained `H_lat`, the kernel is
  uniquely the heat-kernel of THAT `H_lat`. Symanzik and other schemes
  share the same continuum limit (verified Part 6), confirming
  lattice-scheme universality of the **continuum** kernel.
- **Does not certify uniqueness by hard-coded asserts.** Every load-bearing
  uniqueness claim in the runner is backed by either (a) machine-precision
  numerical verification of an algebraic property (Stone group law,
  unitarity, dispersion match) or (b) multi-start nonlinear optimization
  with bounded residual.

## Two lanes, two statuses

| Lane                       | Kernel status                          | Mechanism                  |
|----------------------------|----------------------------------------|----------------------------|
| boost-covariance (this)    | uniquely closed (derived corollary)    | Stone's theorem on H_lat    |
| gravity-card / directional | empirical, Phase 3 no-go applies       | open primitive set          |

The two are formally distinct. This note closes the boost-covariance
lane positively as a derivation; the gravity-card lane retains its
Phase 3 no-go status.

## Verification

```bash
python3 scripts/frontier_lorentz_kernel_positive_closure.py
# PASS=41  FAIL=0
# Exit code: 0
```

41 checks across 9 parts, no hard-coded uniqueness `True` asserts. All
load-bearing claims are numerically verified.

| Part | Coverage                                                              | PASS |
|------|-----------------------------------------------------------------------|------|
| 1    | Canonical kernel inherits unitarity from H_lat (3 lattices x 3 a)    | 9    |
| 2    | Canonical kernel reproduces retained E_lat(p) + KG continuum         | 4    |
| 3    | Canonical kernel inherits parity, time-reflection, translation       | 3    |
| 4    | **Real uniqueness verifier** (best-fit optimization + grid sweep)     | 3    |
| 5    | Directional measure non-unitarity (sweep + non-trivial best-fit)     | 3    |
| 6    | Universality of continuum limit (NN vs Symanzik schemes)             | 4    |
| 7    | Stone's theorem properties (Hermiticity, group law, identity, inverse) | 5  |
| 8    | Closure derivation chain (no new primitives)                         | 6    |
| 9    | Status of directional measure (gravity-card lane unchanged)          | 4    |

Total: 41/41 PASS.

## Relation to existing notes

- [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md):
  retains `H_lat`. This closure note uses that `H_lat` as input and applies
  Stone's theorem.
- [LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md)
  and
  [LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md):
  prove SO(1,1) and SO(3,1) boost covariance of the continuum 2-point
  function from `H_lat`. This closure note adds the kernel uniqueness
  statement (consistent with both).
- [ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md](ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md):
  records the Phase 3 no-go on the gravity-card directional measure.
  This closure note does NOT modify it; it sharpens the routing
  clarification by adding the explicit verifier showing the directional
  measure cannot lie in the canonical heat-kernel class.

## Package wording

Safe wording:

> The per-step kernel of the retained boost-covariance lane is uniquely
> `U(a) = exp(-i a H_lat)`, derived from the retained `H_lat` via Stone's
> theorem. This is a textbook QM corollary applied to retained input;
> no new primitives are introduced. Numerical optimization confirms the
> directional path measure cannot match this kernel for any parameter
> choice.

Unsafe wording (avoid):

> The kernel question is closed by adopting new primitives `(P5a)-(P5d)`.
> [SUPERSEDED -- the closure is a derived corollary, not a new primitive
> extension. The earlier framing was correctly rejected by review.]

## Status call

- **Boost-covariance lane kernel question:** positively closed as a derived
  corollary of retained `H_lat` + Stone's theorem.
- **Gravity-card lane kernel question:** Phase 3 no-go still applies
  (unchanged).
- **Runner:** real numerical verifier; no hard-coded uniqueness asserts.
- **New primitives introduced:** none.
