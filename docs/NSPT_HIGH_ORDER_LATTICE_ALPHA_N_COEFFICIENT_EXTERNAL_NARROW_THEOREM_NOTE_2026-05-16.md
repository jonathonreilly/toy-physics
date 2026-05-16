# NSPT High-Order Lattice α^N Coefficient — External Narrow Theorem

**Date:** 2026-05-16
**Claim type:** positive_theorem
**Scope:** external NSPT-style high-order perturbative coefficient framework
(Di Renzo-Onofri formalism), cited only as published lattice-perturbation
context. No framework substrate identification, hierarchy closure, scale
ratio derivation, or α_LM^16 substitution is claimed.
**Status authority:** source-note proposal only; independent audit sets any
audit result and pipeline-derived status.
**Runner:** [`scripts/frontier_nspt_high_order_lattice_alpha_N_coefficient_external_narrow.py`](../scripts/frontier_nspt_high_order_lattice_alpha_N_coefficient_external_narrow.py)
**Cache:** [`logs/runner-cache/frontier_nspt_high_order_lattice_alpha_N_coefficient_external_narrow.txt`](../logs/runner-cache/frontier_nspt_high_order_lattice_alpha_N_coefficient_external_narrow.txt)

## Claim

Let `U_x,μ ∈ SU(N_c)` be a lattice gauge link configuration on a
Euclidean hypercubic lattice and let `S[U]` denote the Wilson plaquette
action with bare coupling `α = g^2 / (4π)`. Numerical Stochastic
Perturbation Theory (NSPT, Di Renzo-Onofri) integrates the stochastic
Langevin equation

```text
∂_t U_x,μ(t) = - i (∇_x,μ S[U(t)]) U_x,μ(t) + i η_x,μ(t) U_x,μ(t)
```

(in symbolic Langevin time `t`, with Gaussian white noise `η_x,μ`)
order-by-order in a formal power series expansion

```text
U_x,μ(t) = exp( i Σ_{n≥1} α^(n/2) A_x,μ^(n)(t) ),
```

so that, after stochastic averaging, any gauge-invariant lattice
observable `O[U]` admits a determinate formal perturbative expansion

```text
O = Σ_{n≥0} c_n α^n,
```

with each coefficient `c_n` produced by iterating the truncated Langevin
update to order `n`. The coefficient series is well-defined at every
finite order; multiplication of two such series follows the standard
Cauchy product

```text
(Σ a_n α^n) (Σ b_n α^n) = Σ_n (Σ_{k=0}^{n} a_k b_{n-k}) α^n.
```

For the SU(3) Wilson plaquette this NSPT iteration has been carried out
to `n = 20` (Horsley, Perlt, Rakow, Schierholz et al., arXiv:0910.2795
and arXiv:1205.1659), producing explicit `c_n` for `n = 1, ..., 20` and
demonstrating that integer-order `α^N` coefficients of lattice
observables are a determinate, published computation.

## Boundary

This note records an external lattice-perturbation theorem and its
standard published context. It does not claim:

- that the NSPT lattice substrate is identified with the framework's
  substrate (lattice cell, taste, blocking, or any project-specific
  structure);
- that any published `c_n` for the Wilson plaquette is a framework
  hierarchy coefficient or a project-specific coupling;
- closure of any framework substitution, hierarchy formula, scale
  ratio, or physical observable;
- closure of the α_LM^16 substitution or any framework `α^N` hierarchy
  at integer `N`;
- any v/M_Pl or other dimensional scale ratio (NSPT produces
  coefficient series in `α`, not scale ratios);
- any numerical prediction or comparison with observation beyond the
  published lattice context;
- any new framework axiom or repo-wide premise.

Any later framework use must separately identify the framework substrate
with the NSPT iterates, identify a framework observable with an NSPT
lattice observable, and verify the substrate-specific bridge.

## External References

- F. Di Renzo, A. Mantovi, V. Miccio, F. Onofri, "Numerical Stochastic
  Perturbation Theory in the Schrödinger Functional", arXiv:hep-lat/0406001
  (2004).
- F. Di Renzo, L. Scorzato, "Numerical Stochastic Perturbation Theory for
  full QCD", arXiv:hep-lat/0408015 (2004).
- R. Horsley, G. Hotzel, E.-M. Ilgenfritz, R. Millo, H. Perlt, P. E. L.
  Rakow, Y. Nakamura, G. Schierholz, A. Schiller, "Wilson loops to 20th
  order numerical stochastic perturbation theory", arXiv:0910.2795 (2009).
- R. Horsley, H. Perlt, P. E. L. Rakow, G. Schierholz, A. Schiller,
  "Perturbative determination of the Wilson loops in lattice gauge
  theory using NSPT", arXiv:1205.1659 (2012).
- G. Parisi, Y.-S. Wu, "Perturbation theory without gauge fixing",
  Scientia Sinica 24 (1981), 483.

## Verification

The paired runner checks:

1. the NSPT Langevin-time iteration structure: discrete-time update
   rule `U(t + Δt) = exp(-i Δt ∇S - i √(Δt) η) U(t)` produces a formal
   power series in `α^(1/2)` order-by-order;
2. the coefficient series `O = Σ c_n α^n` is well-defined at every
   finite order on scalar / polynomial surrogates;
3. partial-sum convergence at small coupling: at `α = 1/10`, the
   partial sum to order 20 of a geometric surrogate stays within an
   explicit bound;
4. order-16 scalar arithmetic: `α^16 = (1/10)^16 = 10^-16` exactly in
   Fraction arithmetic;
5. Cauchy product: the product of two coefficient series follows the
   standard convolution formula `(a * b)_n = Σ_k a_k b_{n-k}`;
6. substrate-independence of the formal series structure: the algebra
   does not depend on the underlying gauge theory beyond the
   coefficients themselves;
7. integer-N structure: each coefficient `c_n` is a determinate
   computation at order `n`, demonstrated on a worked toy series;
8. source-note boundary checks excluding framework-substrate
   identification, hierarchy closure, scale ratio derivation, and
   α_LM^16 closure overclaims.

Expected runner result: `PASS=N`, `FAIL=0`.
