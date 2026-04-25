# Koide Q finite-range C3 kernel-source no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_finite_range_kernel_source_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Test whether a more physical source class than arbitrary Reynolds-projected
words can derive the missing Q law.  The added constraints are:

- finite-range kernel on the three-state `C_3` quotient;
- `C_3` translation equivariance;
- stochastic conservation;
- positivity;
- detailed balance with the uniform retained measure.

If these conditions forced the normalized second-order traceless source to
vanish, they would derive `K_TL=0`.

## Executable theorem

The general `C_3`-equivariant stochastic nearest-neighbor kernel is

```text
M(a,b) = (1-a-b) I + a C + b C^2.
```

Uniform stationarity is automatic:

```text
M 1 = 1.
```

Detailed balance sets `a=b=s`, giving

```text
M_s = (1-2s)I + s(C+C^2),     0 <= s <= 1/2.
```

The singlet/doublet eigenvalues are

```text
lambda_plus = 1
lambda_perp = 1 - 3s.
```

For the Markov generator/source `I-M_s`,

```text
source_plus = 0
source_perp = 3s.
```

Thus conservation kills the first-order singlet generator, but leaves the
second-order quotient source rate `s` free.

## Residual

```text
RESIDUAL_RATE = s_kernel_equiv_second_order_K_TL_source
RESIDUAL_SCALAR = s_kernel_equiv_second_order_K_TL_source
```

Setting the quotient source to zero is the special endpoint `s=0`; positivity
and detailed balance allow the full interval `0 <= s <= 1/2`.

## Why this is not closure

This packet proves that standard kernel constraints do not select the Koide
source-neutral law.  The uniform stationary distribution is first-order
probability data; it is not equal total energy on the normalized second-order
carrier.

## Falsifiers

- A retained locality or reflection-positivity theorem that collapses
  `0 <= s <= 1/2` to a unique source-neutral point.
- A physical identification of the Markov rate `s` with a retained scalar that
  maps to `K_TL=0` without target import.
- A non-Markov finite-range source theorem whose second-order block source is
  forced to vanish after normalization.

## Boundaries

- The runner covers nearest-neighbor finite-range stochastic kernels on the
  three-cycle, including the reversible detailed-balance subfamily.
- It does not exclude nonlocal kernels, non-stochastic source operators, or a
  new physical law coupling the kernel rate to the normalized carrier.

## Hostile reviewer objections answered

- **"Uniform stationary distribution should imply neutrality."**  It gives
  first-order probability neutrality.  The Q primitive is a second-order
  singlet/doublet energy-source law.
- **"Detailed balance should select the rate."**  It sets clockwise equal to
  counterclockwise; the common rate remains free.
- **"Positivity should eliminate the source."**  Positivity allows a whole
  interval of rates, including nonzero source splits.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_finite_range_kernel_source_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_FINITE_RANGE_KERNEL_SOURCE_NO_GO=TRUE
Q_FINITE_RANGE_KERNEL_SOURCE_CLOSES_Q=FALSE
RESIDUAL_RATE=s_kernel_equiv_second_order_K_TL_source
RESIDUAL_SCALAR=s_kernel_equiv_second_order_K_TL_source
```
