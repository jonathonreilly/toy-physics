# Atomic `alpha(0)` Threshold-Moment No-Go

**Date:** 2026-05-01  
**Loop:** `lane2-atomic-scale-20260428`  
**Science block:** 01  
**Runner:** `scripts/frontier_atomic_alpha0_threshold_moment_no_go.py`  
**Status:** exact reduction / no-go boundary for Lane 2. This is not retained
`alpha(0)` and not retained Rydberg closure.

## Question

Can Lane 2 retain the low-energy Coulomb coupling `alpha(0)` from retained
`alpha_EM(M_Z)` and the structural asymptotic coefficient `b_QED = 32/3`
alone?

## Verdict

No. The retained charge/count surface fixes the QED weights and the
above-threshold coefficient, but one-loop transport to low energy also needs
the threshold moment

```text
T_EM = sum_f N_c(f) Q_f^2 log(M_Z / m_f^eff)
```

plus any finite threshold / hadronic matching convention below quark
thresholds. Current Lane 2 does not retain those data and is not allowed in
this run to work the charged-lepton mass lane.

## Exact Reduction

For the retained charged spectrum,

```text
sum_f N_c Q_f^2 = 8
b_QED = (4/3) sum_f N_c Q_f^2 = 32/3.
```

When all species share the same active logarithm `L`, the standard one-loop
formula reduces to the prior firewall:

```text
1/alpha_low = 1/alpha(M_Z) + (b_QED / 2 pi) L.
```

For threshold-resolved decoupling the same formula is

```text
1/alpha_low
  = 1/alpha(M_Z)
    + (2 / 3 pi) sum_f N_c Q_f^2 log(M_Z / m_f^eff)
    + Delta_match.
```

Thus `b_QED` is only the sum of weights. It is not the weighted log moment.

## No-Go Boundary

The route

```text
alpha_EM(M_Z) + b_QED = 32/3 => alpha(0)
```

does not pass. Two threshold assignments with the same retained species and
same weights can produce different low-energy inverse couplings. Conversely,
at one loop, different individual threshold assignments with the same
weighted moment produce the same transport result. The missing theorem is
therefore sharper than "do QED running": it is a retained threshold/matching
moment theorem, or an exact insensitivity theorem showing the moment is not
needed at the target status.

## Comparator Illustration

Using the existing comparator value `1/alpha(0) = 137.035999084` only after
the reduction is proved, the target moment is

```text
T_EM = (1/alpha(0) - 1/alpha(M_Z)) * (3 pi / 2).
```

With `1/alpha(M_Z) = 127.67`, this gives `T_EM ~= 44.136`. If hidden as one
common effective threshold over total weight `8`, it is equivalent to

```text
L_eff ~= 5.517
m_eff ~= M_Z exp(-L_eff) ~= 0.366 GeV.
```

That hadronic-scale number is a selector, not a framework derivation.

## Import Ledger

| Item | Role | Status in this artifact |
|---|---|---|
| `alpha_EM(M_Z)` | high-scale endpoint | retained/derived input already on repo surface |
| retained charges/counts | weights `N_c Q_f^2` | retained structural input |
| `b_QED = 32/3` | above-threshold sum of weights | exact support ingredient |
| `T_EM` | weighted threshold log moment | exposed open prerequisite |
| charged-lepton threshold masses | logs for `e`, `mu`, `tau` | open dependency; Lane 6 not worked here |
| quark/hadronic effective thresholds | logs and matching below hadronic scales | open Lane 1/Lane 3/hadronic dependency |
| `Delta_match` | finite/hadronic matching convention | open or comparator-only |
| `alpha(0)` | low-energy Coulomb coupling | not retained by this note |

## Verification

Recorded command:

```text
PYTHONPATH=scripts python3 scripts/frontier_atomic_alpha0_threshold_moment_no_go.py
```

Expected summary:

```text
SUMMARY: PASS=25 FAIL=0
STATUS: exact reduction/no-go boundary for alpha(0) transport.
```

## Review-Loop Notes

- The proof uses synthetic threshold logs before any `alpha(0)` comparator is
  printed.
- The `alpha(0)` comparator appears only to identify the hidden effective
  threshold moment a fit would require.
- The artifact does not derive charged-lepton, quark, or hadronic thresholds.
- Lane 6 appears only as an upstream dependency record.
