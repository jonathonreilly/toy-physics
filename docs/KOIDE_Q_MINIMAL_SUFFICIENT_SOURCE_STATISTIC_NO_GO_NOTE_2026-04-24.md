# Koide Q minimal sufficient source-statistic no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_minimal_sufficient_source_statistic_no_go.py`  
**Status:** no-go; sufficient-statistic language does not retain the needed
source quotient

## Theorem Attempt

Use operational indistinguishability or minimal sufficient statistics to derive
the quotient-center anonymity law.  The reduced scalar observable jets of the
`P_plus` and `P_perp` slots are identical, so perhaps the physical source must
identify them and prepare the uniform source state.

## Result

Negative under current retained structure.

The restricted scalar-jet experiment has one sufficient class:

```text
jet_plus = jet_perp = [1, -1, 2, -6, 24, -120]
```

But identical likelihoods do not determine the hidden prior over labels.  The
mixture evidence is independent of:

```text
p = (w, 1-w).
```

So all of these remain compatible with the restricted scalar experiment:

```text
w = 1/3, 1/2, 2/3.
```

Only `w=1/2` gives `K_TL=0`.  Choosing it still requires a quotient-preparation
law.

## Retained-Experiment Countermodel

The full retained experiment includes the central label observable:

```text
Z = P_plus - P_perp.
```

Adding that retained coordinate separates the two slots exactly:

```text
plus_full = [jet, +1]
perp_full = [jet, -1]
```

The `Z` expectation is:

```text
<Z> = 2w - 1.
```

Thus the full retained sufficient statistic is label-resolving, and `w=1/3`
remains an exact non-closing countermodel.

## Residual

```text
RESIDUAL_SCALAR = source_prior_w_minus_one_half_after_scalar_statistic_quotient
RESIDUAL_LABEL = retained_Z_label_makes_full_sufficient_statistic_label_resolving
RESIDUAL_PRIMITIVE =
  derive_physical_experiment_excludes_Z_label_and_quotient_prepares
```

## Hostile Review

- **Target import:** none.  The midpoint is named only as the residual
  condition after deriving the state space.
- **External empirical input:** none.
- **Hidden source-free law:** not promoted.
- **Missing axiom link:** exact.  Sufficiency is relative to a chosen
  experiment; choosing the scalar-only experiment and quotient-preparing is the
  extra physical law.
- **Closure claim:** rejected.  The runner prints
  `Q_MINIMAL_SUFFICIENT_SOURCE_STATISTIC_CLOSES_Q=FALSE`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_minimal_sufficient_source_statistic_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
PASSED: 13/13
KOIDE_Q_MINIMAL_SUFFICIENT_SOURCE_STATISTIC_NO_GO=TRUE
Q_MINIMAL_SUFFICIENT_SOURCE_STATISTIC_CLOSES_Q=FALSE
RESIDUAL_SCALAR=source_prior_w_minus_one_half_after_scalar_statistic_quotient
RESIDUAL_LABEL=retained_Z_label_makes_full_sufficient_statistic_label_resolving
RESIDUAL_PRIMITIVE=derive_physical_experiment_excludes_Z_label_and_quotient_prepares
```

## Consequence

Minimal-sufficient-statistic language is useful review hygiene, but it does not
produce retained positive closure.  The route either leaves the hidden prior
free or explicitly deletes the retained `Z` label, which is the missing source
quotient in another form.
