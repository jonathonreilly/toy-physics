# alpha_LM Geometric-Mean Identity Theorem

Date: 2026-04-24

Status: proposed_retained structural identity on the accepted coupling chain.

**Primary runner:** [`scripts/frontier_alpha_lm_geometric_mean_identity.py`](../scripts/frontier_alpha_lm_geometric_mean_identity.py) (PASS=38/0)

## Statement

On the retained plaquette/coupling surface,

```text
alpha_bare = 1 / (4 pi)
u_0        = <P>^(1/4)
alpha_LM   = alpha_bare / u_0
alpha_s(v) = alpha_bare / u_0^2
```

the intermediate Lepage-Mackenzie coupling is exactly the geometric mean of
the bare coupling and the retained lattice-scale strong coupling:

```text
alpha_LM^2 = alpha_bare * alpha_s(v).
```

Equivalently,

```text
log alpha_LM = (log alpha_bare + log alpha_s(v)) / 2,

alpha_LM / alpha_bare = alpha_s(v) / alpha_LM = 1 / u_0.
```

## Proof

By the retained definitions,

```text
alpha_LM^2
  = (alpha_bare / u_0)^2
  = alpha_bare^2 / u_0^2
  = alpha_bare * (alpha_bare / u_0^2)
  = alpha_bare * alpha_s(v).
```

The logarithmic and constant-ratio forms are immediate restatements for
positive couplings.

## Structural Content

The plaquette weight enters the retained coupling triple with exponents
`0, 1, 2`:

```text
alpha_bare : alpha_LM : alpha_s(v)
  = alpha_bare : alpha_bare/u_0 : alpha_bare/u_0^2.
```

The arithmetic progression in powers of `u_0^(-1)` forces a geometric
progression in the coupling values. Thus the three named couplings contain
only two independent inputs on this surface: the bare normalization and the
plaquette fourth-root density.

This is useful bookkeeping because any downstream lane that uses
`alpha_LM` and `alpha_s(v)` should not count them as independent knobs.

## Retained Numerical Evaluation

Using the retained plaquette value `<P> = 0.5934`,

```text
u_0        = 0.8776813811986843
alpha_bare = 0.07957747154594767
alpha_LM   = 0.09066783601728631
alpha_s(v) = 0.10330381612226712
```

and therefore

```text
alpha_LM^2              = 0.00822065648805752
alpha_bare * alpha_s(v) = 0.00822065648805752
```

up to floating-point roundoff.

## Boundaries

This theorem does not derive the plaquette value `<P> = 0.5934`; it only uses
the retained value already carried by the plaquette lane.

It does not derive or alter the one-decade running bridge from `alpha_s(v)` to
`alpha_s(M_Z)`.

It is not an additional independent empirical prediction. It is an exact
constraint among already-retained coupling definitions. A failure would mean
the retained coupling definitions had been changed, not that a new physical
observable had separately failed.

It does not apply unchanged to a different tadpole-improvement convention or
to a non-Wilson coupling normalization unless that convention preserves the
same powers of `u_0`.

## Reproduction

Run:

```bash
python3 scripts/frontier_alpha_lm_geometric_mean_identity.py
```

The runner verifies the symbolic identity, the retained numerical evaluation,
the logarithmic and constant-ratio forms, and a positive-`u_0` parametric scan.
