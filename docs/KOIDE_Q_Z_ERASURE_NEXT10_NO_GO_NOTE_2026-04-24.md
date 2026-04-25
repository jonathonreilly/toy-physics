# Koide Q Z-Erasure Next-10 No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_z_erasure_next10_no_go.py`  
**Status:** ten-route executable no-go; Q remains open

## Purpose

Run the next ten concrete attacks on the surviving obstruction:

```text
Z = P_plus - P_perp
```

remains a stable `C3`-invariant source-visible separator after
observable/Morita reduction.

## Ten Attacks

1. Quotient ideal `Z=0`.
2. Traceless center annihilator.
3. Positivity/complete-positivity of source states.
4. Entropy maximization.
5. Minimax/decision principle.
6. Terminal coarse-graining.
7. Stable center exchange.
8. Gauge/BRST erasure.
9. Locality.
10. Retained naturality.

## Result

No retained-only closure.  The closing branches all explicitly supply the same
missing law:

```text
derive_physical_source_domain_quotient_killing_Z.
```

The exact counterstate remains:

```text
lambda = 1/3
Q = 1
K_TL = 3/8.
```

## Residual

```text
RESIDUAL_SCALAR=derive_physical_source_domain_quotient_killing_Z
RESIDUAL_SOURCE=stable_C3_invariant_label_functional_tr_Z_rho_not_excluded
COUNTERSTATE=rank_K0_center_state_lambda_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_z_erasure_next10_no_go.py
python3 -m py_compile scripts/frontier_koide_q_z_erasure_next10_no_go.py
```
