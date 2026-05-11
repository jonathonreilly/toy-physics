# Lorentz Kernel Positive Closure Note

**Date:** 2026-04-25
**Status:** proposed_retained derived corollary on the boost-covariance lane
**Runner:** `scripts/frontier_lorentz_kernel_positive_closure.py` (PASS=41, FAIL=0)
**Inputs:** [EMERGENT_LORENTZ_INVARIANCE_NOTE.md](EMERGENT_LORENTZ_INVARIANCE_NOTE.md),
[LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md),
[LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md](LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md)
**Companion no-go:** `ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md` (see-also; converted from markdown link to backticked form 2026-05-10 to break citation cycle-0015 — the companion no-go is a Phase-4 routing clarification on the separate directional-measure kernel question; the theorem below operates on the fixed `H_lat` surface and does not load-bearingly import any conclusion of the no-go)

## Scope

This note closes only the fixed-`H_lat` boost-covariance kernel question.
It does not close the separate gravity-card directional-measure kernel
problem. The word "positive" is a status call: this lane has a positive
derived closure. It is not a claim that the kernel matrix is
positive-definite.

A rejected predecessor attempted to add four new primitives. This version
does not. It uses only:

- the retained lattice Hamiltonian `H_lat` from the emergent-Lorentz
  dispersion theorem, with momentum-space spectrum
  `E_lat(p) = sqrt(m^2 + (4/a^2) sum_i sin^2(p_i a/2))`;
- standard quantum mechanics: Stone's theorem for self-adjoint generators.

## Theorem

**Theorem.** Given the retained lattice Hamiltonian `H_lat`, the
boost-covariance lane's one-parameter unitary evolution is uniquely

```text
U(t) = exp(-i t H_lat).
```

The per-step lattice propagator is therefore

```text
U(a) = exp(-i a H_lat).
```

**Proof.** Stone's theorem states that a self-adjoint operator `H`
generates a unique strongly continuous one-parameter unitary group
`U(t) = exp(-i t H)`. Applying this to the retained self-adjoint
`H_lat` gives the stated unitary propagator. The 1+1D and 3+1D
boost-covariance theorems operate on this fixed `H_lat` surface, so the
per-step kernel on that lane is `U(a)`. No additional primitive is used.

## What The Runner Verifies

The runner verifies the finite-lattice realization of this theorem and
keeps the gravity-card directional measure separated.

### 1. Inheritance From `H_lat`

The canonical propagator is built diagonally in momentum space and
FFT-transformed to position space. It inherits the expected properties:

- `|U^dagger U - I|_max <= 7.8e-16` across tested `L` and `a`;
- eigenvalue phases recover `E_lat(p)` to `3.2e-14`;
- the Klein-Gordon continuum limit is recovered with the expected
  `(a^2/12) p^4` lattice correction;
- parity, time-reflection, translation invariance, identity, inverse, and
  group law all hold to machine precision.

### 2. Directional-Measure Diagnostic

The runner tests the directional family

```text
K_dir(delta; beta, k, p_exp, scale, phi0)
  = scale * exp(-beta theta^2) / L_edge^p_exp * exp(i (k S + phi0)),
```

with `theta = arctan(|delta|)`, `L_edge = sqrt(1 + delta^2)`, and
`S = L_edge - 1`.

This is a diagnostic exclusion of the stated family on the tested lattice,
not a theorem over all conceivable kernels. On the bounded domain
`0 <= beta <= 5`, `0 <= k <= 20`, `0 <= p_exp <= 4`, and
`0 <= scale <= 50`, 30-start optimization gives

```text
min |K_dir - U_can|_F = 1.3705
relative residual     = 0.2423 of ||U_can||_F.
```

A structured grid sweep gives minimum distance `4.9742`. The candidate
directional family is therefore not numerically close to the canonical
`H_lat` propagator on this diagnostic surface.

### 3. Non-Unitary Obstruction For The Gravity-Card Directional Kernel

For the representative directional-measure sweep, the unitarity defect
`|K^dagger K - I|_max` stays bounded away from zero. At the gravity-card
representative `beta = 0.8`, `k = 5`, `p_exp = 2`, the defect is `0.3190`.

The non-trivial best-fit unitary defect over the bounded diagnostic domain
is `0.0236`. Since `exp(-i t H)` with self-adjoint `H` is unitary, these
non-trivial directional kernels are outside the canonical unitary-propagator
class tested here.

### 4. Lattice-Scheme Universality

The runner also compares the nearest-neighbor dispersion to a tree-level
Symanzik-improved dispersion. Both converge to the same continuum
Klein-Gordon dispersion. The improved scheme converges faster, but it does
not change the fixed-`H_lat` theorem: given a chosen self-adjoint
Hamiltonian, Stone fixes its unitary propagator.

## Two Lanes, Two Statuses

| Lane | Kernel status | Mechanism |
| --- | --- | --- |
| boost-covariance | positively closed | Stone theorem on retained `H_lat` |
| gravity-card directional measure | still open / Phase 3 no-go applies | separate empirical directional measure |

The two lanes are formally distinct. This note closes the first and leaves
the second unchanged.

## What This Does Not Claim

- It does not introduce new primitives.
- It does not derive the gravity-card directional-measure kernel.
- It does not assert uniqueness across all possible lattice actions or all
  conceivable kernels.
- It does not turn the finite optimization into a global analytic no-go.
  The analytic closure is Stone uniqueness for the retained `H_lat`; the
  optimization is a diagnostic guardrail for the directional candidate.

## Verification

```bash
python3 scripts/frontier_lorentz_kernel_positive_closure.py
# PASS=41  FAIL=0
```

The 41 checks cover unitarity, dispersion recovery, continuum correction,
discrete symmetries, Stone group law, diagnostic directional-family
non-match, directional non-unitarity, scheme universality, and the lane
status split.

## Safe Public Wording

> On the fixed `H_lat` boost-covariance lane, the per-step propagator is
> uniquely `U(a) = exp(-i a H_lat)` by Stone's theorem. This is a derived
> corollary of the retained lattice Hamiltonian, not a new primitive. The
> separate gravity-card directional-measure kernel remains open and is not
> closed by this theorem.
