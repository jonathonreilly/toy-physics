# Koide Q noncontextual center-state no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_noncontextual_center_state_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use noncontextual probability or a Gleason-style state theorem on the retained
center events:

```text
noncontextual center state
  -> unique equal label source
  -> K_TL = 0.
```

## Executable theorem

For the two center projections the noncontextual/additive state is:

```text
p(P_plus) = u
p(P_perp) = 1-u
p(1) = 1.
```

The runner verifies that this leaves the whole interval of center states.  The
source-neutral member is only:

```text
u = 1/2.
```

Every such state extends to a block-unitarily invariant density on the retained
rank-1/rank-2 carrier:

```text
rho(u) = diag(u, (1-u)/2, (1-u)/2).
```

## Obstruction

Noncontextuality fixes additivity, not preparation.  A rank-state source and
the equal-label source are both valid noncontextual center states:

```text
u = 1/3 -> Q = 1,   K_TL = 3/8
u = 1/2 -> Q = 2/3, K_TL = 0.
```

Gleason-style extension does not select the equal-label state; it supplies a
density matrix family.  The inherited full-carrier trace selects the rank state
`u=1/3`, not the label state `u=1/2`.

## Entropy escape hatch

A stronger reviewer-friendly attempt is to add a maximum-entropy or
indifference principle.  The runner now separates the two possible entropy
algebras.

On the quotient two-label algebra:

```text
H_label(u) = -u log u - (1-u) log(1-u)
dH_label/du = 0 -> u = 1/2
```

This would close the Q bridge.  But on the retained rank-1/rank-2 carrier the
block-unitarily invariant density is:

```text
rho(u) = diag(u, (1-u)/2, (1-u)/2)
S_carrier(u) = -u log u - (1-u) log((1-u)/2)
dS_carrier/du = 0 -> u = 1/3.
```

So maximum entropy does not supply a retained theorem until the entropy algebra
is specified.  Choosing `H_label` over `S_carrier` deletes the retained rank
data and is exactly the missing quotient-label source prior.

## Indifference escape hatch

An abstract swap of the two center atoms would force:

```text
p(P_plus) = p(P_perp)
u = 1/2.
```

That swap is not retained by the physical carrier:

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

Using it as an indifference principle chooses the quotient label algebra over
the retained rank data; that is a new source prior.

## Residual

```text
RESIDUAL_SCALAR = center_label_state_u_minus_one_half_equiv_K_TL
RESIDUAL_PRIOR = noncontextuality_does_not_prepare_uniform_center_state
RESIDUAL_ENTROPY_CHOICE = quotient_label_entropy_over_retained_carrier_entropy
```

## Why this is not closure

The route proves that the desired center state is admissible, not that it is
forced.  A Nature-grade closure still needs a physical law that prepares the
equal center-label source rather than a different noncontextual source.

## Falsifiers

- A retained physical preparation theorem excluding the rank-state center
  distribution.
- A retained automorphism exchanging the two center atoms despite the rank
  obstruction.
- A state-extension theorem that collapses the whole block-invariant density
  family to `u=1/2` without importing the target source law.

## Boundaries

- Covers finitely additive center states and block-unitarily invariant
  extensions to the retained rank-1/rank-2 carrier.
- Does not refute a stronger physical preparation principle for the center
  source.

## Hostile reviewer objections answered

- **"Gleason removes hidden variables."**  It does not choose a unique density
  matrix here.
- **"The center has two unlabeled atoms."**  The retained carrier labels them
  by inequivalent ranks and real C3 type.
- **"Use indifference."**  That is the residual prior unless the indifference
  symmetry is retained physically.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_noncontextual_center_state_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_NONCONTEXTUAL_CENTER_STATE_NO_GO=TRUE
Q_NONCONTEXTUAL_CENTER_STATE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=center_label_state_u_minus_one_half_equiv_K_TL
RESIDUAL_PRIOR=noncontextuality_does_not_prepare_uniform_center_state
RESIDUAL_ENTROPY_CHOICE=quotient_label_entropy_over_retained_carrier_entropy
```
