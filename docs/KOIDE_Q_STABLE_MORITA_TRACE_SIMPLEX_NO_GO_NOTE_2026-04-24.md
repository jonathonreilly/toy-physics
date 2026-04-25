# Koide Q Stable Morita Trace-Simplex No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_stable_morita_trace_simplex_no_go.py`  
**Status:** executable no-go for deriving the stable Morita source law from Morita trace theory alone

## Theorem Attempt

Try to derive the stable Morita source-response law from Morita-invariant
traces.  On each simple matrix block `M_r`, the normalized trace/logdet is
stable under matrix amplification:

```text
log det(I+kI_{nr}) / (nr) = log(1+k).
```

The hoped-for result was that this forces equal coefficients on the charged
lepton reduced algebra:

```text
C plus M_2(C).
```

## Exact Audit

The runner verifies that stable Morita normalization deletes internal matrix
rank inside each simple block.  But on a semisimple algebra the stable traces
still form a center-state simplex:

```text
tau_lambda = lambda tau_plus + (1-lambda) tau_perp.
```

The source generator is:

```text
W_lambda = lambda log(1+k_plus) + (1-lambda) log(1+k_perp).
```

Thus:

```text
dW_lambda|0 = (lambda, 1-lambda).
```

## Conditional Positive

The equal center state closes the Q chain:

```text
lambda = 1/2
K_TL = 0
Q = 2/3.
```

## Counterstate

The retained rank/K0 center state is also stable inside each simple block:

```text
lambda = 1/3
K_TL = 3/8
Q = 1.
```

So stable Morita normalization alone does not choose the physical center
state.

## Hostile Review

This route audits the source trace simplex first, then evaluates consequences.
It uses only exact symbolic source-response algebra, with no empirical mass
data, observational pins, or target-value assumptions as inputs.

The exact residual is:

```text
derive_equal_center_state_after_stable_Morita_normalization.
```

## Verdict

```text
KOIDE_Q_STABLE_MORITA_TRACE_SIMPLEX_NO_GO=TRUE
Q_STABLE_MORITA_TRACE_SIMPLEX_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_EQUAL_CENTER_STATE_IS_PHYSICAL=TRUE
RESIDUAL_SCALAR=derive_equal_center_state_after_stable_Morita_normalization
RESIDUAL_Q=rank_K0_center_state_lambda_1_over_3_not_excluded
COUNTERSTATE=stable_Morita_rank_center_state_w_plus_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_stable_morita_trace_simplex_no_go.py
python3 -m py_compile scripts/frontier_koide_q_stable_morita_trace_simplex_no_go.py
```
