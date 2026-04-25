# Koide Q dagger-Frobenius retention no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_dagger_frobenius_retention_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

The special-Frobenius center reduction showed an exact conditional route:

```text
special Frobenius center counit -> equal center-label weights -> K_TL = 0.
```

This audit asks whether the special Frobenius structure is forced by the
retained real `C_3` carrier and its inherited dagger/inner product.

## Executable theorem

The retained carrier projectors have:

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

The inherited Hilbert-Schmidt inner product gives Frobenius weights:

```text
lambda_plus : lambda_perp = Tr(P_plus) : Tr(P_perp) = 1 : 2.
```

For a two-idempotent Frobenius algebra,

```text
m o Delta = diag(1/lambda_plus, 1/lambda_perp).
```

Specialness requires:

```text
m o Delta = beta id,
```

which is equivalent to:

```text
lambda_plus = lambda_perp.
```

The runner verifies that no positive weights satisfy both:

```text
lambda_plus : lambda_perp = 1 : 2
lambda_plus = lambda_perp.
```

The strengthened runner also identifies the exact replacement needed to get
label counting from the retained carrier.  A weighted Hilbert-Schmidt form with

```text
G_label = P_plus + (1/2) P_perp
```

gives

```text
Tr(G_label P_plus) = 1
Tr(G_label P_perp) = 1.
```

The retained Hilbert density is instead `G_H = I`, which gives the rank weights
`1:2`.  Therefore the label-counting dagger is equivalent to inserting a
specific non-Hilbert central density.

## Consequence

The special label-counting dagger gives:

```text
(lambda_plus,lambda_perp) = (1,1)
Q = 2/3
K_TL = 0.
```

The inherited carrier dagger gives:

```text
(lambda_plus,lambda_perp) = (1,2)
Q = 1
K_TL = 3/8.
```

## Residual

```text
RESIDUAL_SCALAR = label_counting_dagger_not_inherited_from_rank_carrier
RESIDUAL_PRIMITIVE = physical_choice_of_center_Frobenius_counit
RESIDUAL_DENSITY = G_label_central_density_not_retained_as_physical_source
```

## Why this is not closure

Special Frobenius is a serious candidate source law, but it is not forced by
the inherited retained carrier.  To close `Q`, a physical theorem must explain
why charged-lepton sources use the label-counting center dagger/counit rather
than the Hilbert/rank dagger inherited from the real representation.

## Falsifiers

- A retained physical principle that replaces the Hilbert/rank dagger with the
  special label-counting dagger for source observables.
- A theorem showing the charged-lepton center is a copy/delete classical system
  whose counit is the physical second-order source functional.
- A proof that the rank trace is not an admissible source state despite being
  inherited from the retained carrier.

## Boundaries

- This no-go is against deriving special Frobenius from the inherited carrier
  alone.
- It does not refute a future independent physical principle selecting the
  special center counit.

## Hostile reviewer objections answered

- **"Special Frobenius still closes conditionally."**  Correct.  The unresolved
  question is why specialness is retained physics.
- **"The inherited trace is the obvious physical one."**  If so, it gives the
  rank state and does not close.
- **"Use the center labels, not micro-ranks."**  That is precisely the missing
  source-selection law.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_dagger_frobenius_retention_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_DAGGER_FROBENIUS_RETENTION_NO_GO=TRUE
Q_DAGGER_FROBENIUS_RETENTION_CLOSES_Q=FALSE
RESIDUAL_SCALAR=label_counting_dagger_not_inherited_from_rank_carrier
RESIDUAL_PRIMITIVE=physical_choice_of_center_Frobenius_counit
RESIDUAL_DENSITY=G_label_central_density_not_retained_as_physical_source
```
