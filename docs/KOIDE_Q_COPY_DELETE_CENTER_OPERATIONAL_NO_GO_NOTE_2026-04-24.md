# Koide Q operational copy/delete center no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_copy_delete_center_operational_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use operational classicality of the retained center labels:

```text
center labels can be copied/deleted
  -> label-counting source
  -> K_TL = 0.
```

## Executable theorem

On the abstract two-label algebra, the copy map is:

```text
Delta |+> = |++>
Delta |perp> = |perp perp>.
```

The delete effect is:

```text
epsilon(+) = epsilon(perp) = 1.
```

The runner verifies:

```text
(epsilon tensor id) Delta = id
(id tensor epsilon) Delta = id
m Delta = id.
```

So the label algebra is a special classical copy/delete structure.

## Obstruction

Copy/delete structure fixes which labels are classical.  It does not fix which
classical distribution is prepared.

For

```text
p(u) = (u, 1-u),
```

the copied state is:

```text
Delta p(u) = (u, 0, 0, 1-u),
```

and both marginals return `p(u)`.

The source-neutral state is only:

```text
u = 1/2.
```

The retained rank state is also a valid classical label state:

```text
u = 1/3
Q = 1
K_TL = 3/8.
```

## Exchange escape hatch

An abstract swap of the two labels would force `u=1/2`, but the charged-lepton
carrier does not retain that swap:

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

## Residual

```text
RESIDUAL_SCALAR = center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_PRIOR = unbiased_center_label_preparation_not_forced_by_copy_delete
```

## Why this is not closure

Operational copy/delete is not strong enough.  It gives the right algebraic
stage for the special-Frobenius candidate, but it does not select the physical
source distribution.  Choosing the uniform label source is an additional prior
or symmetry.

## Falsifiers

- A retained operational principle that the charged-lepton source is the
  maximally mixed classical state of the center-label system.
- A physical reason the rank-state distribution is not preparable as a center
  label source.
- A retained symmetry exchanging center labels despite the rank-1/rank-2
  carrier obstruction.

## Boundaries

- Covers abstract center-label copy/delete and its action on all classical
  distributions.
- Does not refute a stronger physical preparation theorem for the center source.

## Hostile reviewer objections answered

- **"The labels are classical."**  Yes.  Classicality does not imply a uniform
  source distribution.
- **"The delete map treats labels equally."**  It is an effect, not a prepared
  state.
- **"Use the maximally mixed label state."**  That is exactly the residual
  source prior.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_copy_delete_center_operational_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_COPY_DELETE_CENTER_OPERATIONAL_NO_GO=TRUE
Q_COPY_DELETE_CENTER_OPERATIONAL_CLOSES_Q=FALSE
RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_PRIOR=unbiased_center_label_preparation_not_forced_by_copy_delete
```
