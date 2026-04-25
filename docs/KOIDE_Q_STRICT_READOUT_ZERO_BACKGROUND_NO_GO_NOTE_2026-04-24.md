# Koide Q Strict-Readout Zero-Background No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_strict_readout_zero_background_no_go.py`  
**Status:** executable no-go for promoting strict source-response readout to
retained-only Q closure

## Theorem Attempt

Derive the remaining `Z`-erasure/source-domain law from the retained statement
that charged-lepton scalar observables are local source-response coefficients
of `W[J]` at a zero-source expansion point.

## Result

The audit separates two different meanings of "zero source":

```text
probe zero:
  take derivatives with respect to a local probe J at J=0 around a chosen
  background K_bg;

background zero:
  choose K_bg=0 as the physical charged-lepton selector.
```

The retained source-response calculus gives the first.  Q closure needs the
second.

For the reduced generator

```text
W_probe = log(1 + K_+ + J_+) + log(1 + K_perp + J_perp) - W(K_bg),
```

the zero-probe derivative is

```text
dW_probe/dJ|0 = (1/(1+K_+), 1/(1+K_perp)).
```

So `J=0` does not imply `K_bg=0`.

## Exact Counterbackground

On the normalized trace-2 carrier, trace normalization leaves

```text
K_bg(t) = diag(t, -t/(2t+1)).
```

Then

```text
Y(t) = diag(1/(1+t), (2t+1)/(1+t)).
```

The zero-background member `t=0` conditionally gives

```text
K_TL = 0
Q = 2/3.
```

But the exact nonzero background

```text
t = 1/4
```

is still source-response compatible and gives

```text
Y = diag(4/5, 6/5)
Q = 5/6
K_TL = 5/24.
```

## Residual

The surviving coordinate is the `Z` source coefficient:

```text
1/2 tr(Z K_bg(t)).
```

It vanishes only after choosing `t=0`.  Therefore strict readout does not
derive retained-only Q closure; it sharpens the missing law to:

```text
RESIDUAL_SCALAR=derive_physical_background_source_zero_equiv_Z_erasure
```

## Verdict

```text
KOIDE_Q_STRICT_READOUT_ZERO_BACKGROUND_NO_GO=TRUE
Q_STRICT_READOUT_ZERO_BACKGROUND_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_PHYSICAL_BACKGROUND_SOURCE_IS_ZERO=TRUE
RESIDUAL_SOURCE=probe_zero_readout_allows_nonzero_traceless_background
COUNTERBACKGROUND=t_1_over_4_Q_5_over_6_K_TL_5_over_24
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_strict_readout_zero_background_no_go.py
python3 -m py_compile scripts/frontier_koide_q_strict_readout_zero_background_no_go.py
```
