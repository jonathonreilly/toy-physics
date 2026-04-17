# Finite-Rank Source-to-Metric Theorem Path via Exact Boundary Action and Coarse-Grained Exterior Law

**Date:** 2026-04-14  
**Script:** `scripts/frontier_finite_rank_source_to_metric_theorem.py`  
**Status:** exact finite-rank source-to-exterior theorem plus bounded scalar metric reduction; not full nonlinear GR

## Purpose

This is the finite-rank source-to-metric route in the current gravity program:
attack the finite-rank source-to-metric architecture directly, using the exact
finite-rank source family plus the retained bridge/action laws, and avoid the
current `eta_floor_tf` endpoint route entirely.

The goal is to see how far the exact finite-rank source stack can go as a clean
end-to-end GR architecture:

1. exact finite-rank source renormalization
2. exact microscopic boundary action / Dirichlet principle
3. unique coarse-grained exterior harmonic law
4. induced static isotropic metric reduction

## Exact theorem: finite-rank source determines the exterior harmonic field

For the exact finite-rank support operator already on the branch,

- `H_W = H_0 - P W P^T`
- `G_0 = H_0^-1`
- `G_S = P^T G_0 P`

the exact Woodbury/Dyson identity gives

- `G_W P = G_0 P (I - W G_S)^-1`

so every bare support source vector `m` induces the exact renormalized source

- `q_eff = (I - W G_S)^-1 m`

and the exact exterior field

- `phi = G_0 P q_eff`.

That is the exact finite-rank source-to-exterior theorem already supported by
the current gravity stack.

## Exact theorem: the same microscopic boundary action is stationary

Using the exact Schur-complement boundary action on the current bridge
surface,

- `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`

the exact finite-rank shell trace is recovered as the unique stationary point
with microscopic flux `j = (H_0 phi_ext)|_(Gamma_R)`.

So the finite-rank source family does not merely give an exterior harmonic
field. It also lands on the same exact microscopic boundary-action surface as
the retained bridge law.

## Bounded theorem: the exterior field coarse-grains to a near-vacuum isotropic metric

Shell averaging the exact finite-rank exterior field and projecting it onto
the unique radial harmonic law `phi_eff(r) = a/r` gives a static isotropic
`3+1` metric candidate with strongly reduced vacuum residual.

On the exact finite-rank family, the best matching radius in the current scan
is `R_match = 5.0`:

- direct same-source metric residual: `1.039e-02`
- coarse-grained radial-harmonic residual: `7.028e-06`
- improvement factor: `~1.48e3`

So the finite-rank family does support a clean source-to-exterior-metric
architecture at the scalar/isotropic level.

## Sharp blocker: the tensorial `3+1` matching map is still missing

The direct common-source metric candidate built from the exact finite-rank
field still has a nonzero Einstein residual.

That means the exact finite-rank source family does **not** by itself supply a
theorem-grade tensorial map from microscopic source data to the full `3+1`
metric.

What is missing is the same thing the current gravity frontier has already
localized elsewhere:

> a tensorial matching/completion principle that promotes the exact scalar
> exterior law to the full lapse-shift-spatial metric.

So route 3 is cleaner than the current `eta_floor_tf` endpoint route because
it starts from exact finite-rank source renormalization and exact retained
boundary/action laws, but it still stops at the scalar/static exterior sector.

## Verdict

The finite-rank source family gives a stronger exact/bounded architecture than
the current tensor residual route:

- exact finite-rank source-to-exterior closure: yes
- exact microscopic boundary-action closure: yes
- bounded coarse-grained source-to-metric reduction: yes
- full tensorial `3+1` closure / full nonlinear GR: no

So this route is a real end-to-end source architecture, but it still needs a
new tensorial matching principle before it can become full GR.
